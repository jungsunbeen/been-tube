"""ggg. 믹스의 소스 곡 수 추정.

질문: 30분 세트 안의 9~10개 트랙이 (a) 서로 다른 곡인가,
(b) 적은 수의 곡을 피치/템포 변주한 것인가?

방법: 각 트랙 구간에서 코드 진행 시퀀스(크로마)를 뽑아,
12가지 조옮김 × 여러 템포 비율로 정렬해 본 뒤 최대 유사도를 구한다.
같은 곡의 피치/템포 변주라면 어떤 조옮김·비율에서 유사도가 1에 가깝게 나온다.

캘리브레이션:
- 양성 기준: 1분 구간 vs 31분 구간(세트 통반복) → 유사도 ~1.0이어야 함
- 음성 기준: Paper Sun vs Paper Moon(실제 다른 곡) → 낮아야 함
"""
import sys
import numpy as np
import librosa

HOP = 4096
SR = 22050
EXCERPT = 90  # 각 트랙에서 자르는 길이(초)

# ggg-analy.md 타임라인 기준 트랙 대표 지점(분)
TRACKS = {
    "audio/ggg-orange-soda.wav": [1, 3, 7, 9, 11, 13, 15, 19, 21, 23, 25, 29],
    "audio/ggg-matcha.wav":      [1, 3, 7, 11, 13, 15, 19, 21, 23, 25, 27, 29],
}

RATIOS = np.linspace(0.7, 1.4, 11)  # 허용 템포 비율


def chroma_seq(path, t0, dur=EXCERPT):
    y, sr = librosa.load(path, sr=SR, offset=t0, duration=dur)
    c = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=HOP)
    # 프레임 정규화 (음량 무관하게)
    c = c / (np.linalg.norm(c, axis=0, keepdims=True) + 1e-9)
    return c.astype(np.float32)


def resample_seq(c, ratio):
    n = int(c.shape[1] * ratio)
    idx = np.linspace(0, c.shape[1] - 1, n)
    lo = np.floor(idx).astype(int)
    hi = np.minimum(lo + 1, c.shape[1] - 1)
    w = (idx - lo).astype(np.float32)
    return c[:, lo] * (1 - w) + c[:, hi] * w


def best_align(a, b, min_overlap_frames):
    """모든 lag에서 평균 코사인 유사도의 최대값 (a 고정, b 슬라이드)."""
    na, nb = a.shape[1], b.shape[1]
    best = -1.0
    # 유효 lag 범위: 최소 겹침 보장
    for lag in range(-(nb - min_overlap_frames), na - min_overlap_frames + 1, 2):
        s_a, e_a = max(0, lag), min(na, lag + nb)
        s_b, e_b = max(0, -lag), max(0, -lag) + (e_a - s_a)
        if e_a - s_a < min_overlap_frames:
            continue
        sim = float(np.mean(np.sum(a[:, s_a:e_a] * b[:, s_b:e_b], axis=0)))
        if sim > best:
            best = sim
    return best


def transposed_similarity(ca, cb):
    """12 조옮김 × 템포 비율에 대한 최대 정렬 유사도와 최적 파라미터."""
    min_ov = int(40 * SR / HOP / 1)  # 최소 40초 겹침
    best = (-1.0, 0, 1.0)
    for ratio in RATIOS:
        cb_r = resample_seq(cb, ratio)
        for rot in range(12):
            cb_t = np.roll(cb_r, rot, axis=0)
            s = best_align(ca, cb_t, min_ov)
            if s > best[0]:
                best = (s, rot, ratio)
    return best


def main():
    np.set_printoptions(precision=3)

    print("=== 캘리브레이션 ===")
    # 양성: orange soda 1분 vs 31.1분(세트 반복, 30.1분 오프셋)
    a = chroma_seq("audio/ggg-orange-soda.wav", 60)
    b = chroma_seq("audio/ggg-orange-soda.wav", 60 + 1806)
    s, rot, ratio = transposed_similarity(a, b)
    print(f"  [양성] orange soda 1분 vs 31.1분(통반복): {s:.3f} (rot={rot}, ratio={ratio:.2f})")

    # 음성: Paper Sun vs Paper Moon (서로 다른 곡)
    a = chroma_seq("audio/suno/Paper Sun.mp3", 30)
    b = chroma_seq("audio/suno/Paper Moon.mp3", 30)
    s, rot, ratio = transposed_similarity(a, b)
    print(f"  [음성] Paper Sun vs Paper Moon(다른 곡): {s:.3f} (rot={rot}, ratio={ratio:.2f})")

    # 양성2: Paper Sun vs 자기 자신 +5st 변주 (time_stretch 시뮬레이션 대신 크로마 롤)
    a = chroma_seq("audio/suno/Paper Sun.mp3", 30)
    b = np.roll(chroma_seq("audio/suno/Paper Sun.mp3", 30), 5, axis=0)
    b = resample_seq(b, 1.1)
    s, rot, ratio = transposed_similarity(a, b)
    print(f"  [양성2] Paper Sun vs 자기 +5st x1.1배속: {s:.3f} (rot={rot}, ratio={ratio:.2f})")

    for path, mins in TRACKS.items():
        name = path.split("/")[-1].replace(".wav", "")
        print(f"\n=== {name}: 트랙 쌍별 최대 조옮김 유사도 ===")
        seqs = [chroma_seq(path, m * 60) for m in mins]
        n = len(seqs)
        simmat = np.eye(n)
        for i in range(n):
            for j in range(i + 1, n):
                s, rot, ratio = transposed_similarity(seqs[i], seqs[j])
                simmat[i, j] = simmat[j, i] = s
                flag = " <== 같은 곡 의심" if s > 0.85 else ""
                print(f"  {mins[i]:2d}분 vs {mins[j]:2d}분: {s:.3f} (rot={rot:2d}, x{ratio:.2f}){flag}")

        # 단순 클러스터링: 유사도 > 0.85 이면 같은 소스로 연결
        parent = list(range(n))
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        for i in range(n):
            for j in range(i + 1, n):
                if simmat[i, j] > 0.85:
                    parent[find(i)] = find(j)
        clusters = {}
        for i in range(n):
            clusters.setdefault(find(i), []).append(mins[i])
        print(f"  --> 추정 소스 곡 수: {len(clusters)}")
        for c in clusters.values():
            print(f"      클러스터: {c}분")


if __name__ == "__main__":
    main()
