"""장시간 lofi/jazz 믹스 범용 분석기 (verify_matcha.py 일반화 버전).

사용법: python scripts/analyze_mix.py <wav> [scan_interval_sec]

출력:
1. 총 길이
2. 전곡 스캔 타임라인 (BPM, 조성)
3. 반복 주기 자동 탐지: 스캔 지점 평균 크로마의 자기유사도로 후보 주기를 찾고,
   상세 크로마 시퀀스 정렬(유사도 ~1.0 = 통반복)로 검증
4. 대표 3지점 코드 진행
"""
import sys
import numpy as np
import librosa

WAV = sys.argv[1]
SCAN_STEP = int(sys.argv[2]) if len(sys.argv) > 2 else 120

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

KS_MAJ = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
KS_MIN = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

CHORD_TYPES = {
    "":     [0, 4, 7],
    "m":    [0, 3, 7],
    "maj7": [0, 4, 7, 11],
    "m7":   [0, 3, 7, 10],
    "7":    [0, 4, 7, 10],
}


def estimate_key(chroma_mean):
    best, best_r = None, -2
    for root in range(12):
        for prof, mode in ((KS_MAJ, "major"), (KS_MIN, "minor")):
            r = np.corrcoef(np.roll(prof, root), chroma_mean)[0, 1]
            if r > best_r:
                best_r, best = r, f"{NOTE_NAMES[root]} {mode}"
    return best, best_r


def best_chord(v):
    best, best_s = None, -1
    vn = v / (np.linalg.norm(v) + 1e-9)
    for root in range(12):
        for suf, ivs in CHORD_TYPES.items():
            tmpl = np.zeros(12)
            for k, iv in enumerate(ivs):
                tmpl[(root + iv) % 12] = 1.0 if k == 0 else 0.85
            tmpl /= np.linalg.norm(tmpl)
            s = vn @ tmpl
            if s > best_s:
                best_s, best = s, NOTE_NAMES[root] + suf
    return best


def fold_bpm(b):
    while b > 115:
        b /= 2
    while b < 55:
        b *= 2
    return b


def analyze(t0, dur=45, chords=False):
    y, sr = librosa.load(WAV, sr=None, offset=t0, duration=dur)
    onset = librosa.onset.onset_strength(y=y, sr=sr)
    tempo = librosa.feature.tempo(onset_envelope=onset, sr=sr)[0]
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    cm = chroma.mean(axis=1)
    key, r = estimate_key(cm)
    out = {"bpm": fold_bpm(tempo), "key": key, "key_r": r, "chroma_mean": cm}
    if chords:
        dt = 512 / sr
        group = max(1, int(2.0 / dt))
        seq = []
        for i in range(0, chroma.shape[1] - group, group):
            seq.append(best_chord(chroma[:, i:i + group].sum(axis=1)))
        out["dedup"] = [seq[0]] + [c for a, c in zip(seq, seq[1:]) if c != a]
    return out


def chroma_seq(t0, dur=30):
    y, sr = librosa.load(WAV, sr=None, offset=t0, duration=dur)
    c = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=4096)
    return c / (np.linalg.norm(c, axis=0, keepdims=True) + 1e-9), sr


def repeat_sim(t0, offset):
    """t0와 t0+offset 구간의 크로마 시퀀스를 ±5초 슬라이드로 정렬한 최대 유사도."""
    a, sr = chroma_seq(t0, 30)
    b, _ = chroma_seq(max(0, t0 + offset - 5), 40)
    na, nb = a.shape[1], b.shape[1]
    best = -1.0
    for lag in range(0, nb - na + 1):
        s = float(np.mean(np.sum(a * b[:, lag:lag + na], axis=0)))
        if s > best:
            best = s
    return best


def main():
    total = librosa.get_duration(path=WAV)
    print(f"파일: {WAV}")
    print(f"총 길이: {total:.1f}s = {total/60:.1f}분")

    print(f"\n=== 1) 전곡 {SCAN_STEP}초 간격 스캔 ===")
    times, feats = [], []
    for t0 in range(60, int(total) - 60, SCAN_STEP):
        a = analyze(t0)
        times.append(t0)
        feats.append(a)
        print(f"  {t0/60:6.1f}분: BPM {a['bpm']:6.1f}  | {a['key']:9s} (r={a['key_r']:.2f})", flush=True)

    print("\n=== 2) 반복 주기 탐지 (스캔 지점 평균 크로마 자기유사도) ===")
    C = np.array([f["chroma_mean"] / (np.linalg.norm(f["chroma_mean"]) + 1e-9) for f in feats])
    n = len(C)
    cands = []
    for p in range(2, n - 2):
        sims = np.sum(C[:n - p] * C[p:], axis=1)
        cands.append((float(np.mean(sims)), p))
    cands.sort(reverse=True)
    for s, p in cands[:5]:
        print(f"  주기 {p*SCAN_STEP/60:6.1f}분 (스캔 {p}칸): 평균 유사도 {s:.3f}")

    best_p = cands[0][1]
    offset = best_p * SCAN_STEP
    print(f"\n=== 3) 최우수 후보 주기 {offset/60:.1f}분 상세 검증 (통반복이면 ~1.0) ===")
    probes = [t for t in (60, 300, 600, 900, 1200) if t + offset + 60 < total]
    for t0 in probes:
        s = repeat_sim(t0, offset)
        print(f"  {t0}s vs {t0+offset}s: 유사도 {s:.3f}", flush=True)

    print("\n=== 4) 대표 3지점 코드 진행 ===")
    for frac in (0.05, 0.45, 0.85):
        t0 = int(total * frac)
        a = analyze(t0, 60, chords=True)
        print(f"\n--- {t0/60:.1f}분 ---")
        print(f"  BPM {a['bpm']:.1f} | {a['key']} (r={a['key_r']:.2f})")
        print(f"  코드: {' -> '.join(a['dedup'])}")


if __name__ == "__main__":
    main()
