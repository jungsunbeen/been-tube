"""도시 시리즈 1시간 로파이 믹스 빌더 (ggg. 검증 공식 적용).

ggg-analy.md 결론: ggg.는 곡을 변주하지 않는다. 서로 다른 곡 9~12개로
~31분 세트를 만들고 그 세트를 통째로 2회 반복해 1시간을 채울 뿐이다.
이 스크립트도 그대로 따른다 — 곡의 피치/멜로디/템포는 건드리지 않고,
믹싱 손질(무음 제거·음량 통일·등파워 크로스페이드)만 한다.

사용법:
    python scripts/build_mix.py florence
    python scripts/build_mix.py london

각 프로젝트의 트랙 순서는 아래 PROJECTS에 정의한다.
"""
import sys
import wave
import numpy as np
from pedalboard import Pedalboard, Limiter
from pedalboard.io import AudioFile

SR = 48000
XFADE = 3.0          # 곡 간 등파워 크로스페이드(초)
TAIL_FADE = 8.0      # 마지막 페이드아웃(초)
REPEAT = 2           # 세트 반복 횟수 (ggg 공식)

# 프로젝트별 트랙 순서 (audio/suno/<project>/ 기준 파일명)
PROJECTS = {
    "florence": [
        "Rain Gloss Piano(1).mp3",   # E장조  92  오프너
        "Vinyl Morning (1).mp3",     # A장조  83
        "Vinyl Morninglight.mp3",    # E장조  96
        "Waterlogged Vinyl (1).mp3", # C장조  72  깊은 다운
        "Train Window.mp3",          # D장조  92
        "Paper Moon.mp3",            # D#단조 81  단조 색채
        "Lantern Vinyl (1).mp3",     # B장조  76  중심곡(최장)
        "Paper Sun.mp3",             # C장조  81
        "Vinyl Snowfall (1).mp3",    # A#장조 76  와인드다운
        "Starry Loops.mp3",          # A장조  99  피날레
    ],
}


def load(path):
    with AudioFile(path) as f:
        audio = f.read(f.frames)            # (ch, n) float32
        sr = int(f.samplerate)
    if audio.shape[0] == 1:                  # 모노 → 스테레오
        audio = np.repeat(audio, 2, axis=0)
    if sr != SR:
        raise ValueError(f"{path}: 샘플레이트 {sr} != {SR}")
    return audio


def trim_silence(audio, thresh_db=-45.0, pad=0.3):
    """양 끝 거의 무음 구간 제거 (크로스페이드가 무음과 겹치지 않게)."""
    env = np.abs(audio).max(axis=0)
    above = np.where(env > 10 ** (thresh_db / 20))[0]
    if len(above) == 0:
        return audio
    p = int(pad * SR)
    s = max(0, above[0] - p)
    e = min(audio.shape[1], above[-1] + p)
    return audio[:, s:e]


def rms(audio):
    return float(np.sqrt(np.mean(audio ** 2)))


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in PROJECTS:
        sys.exit(f"사용법: python scripts/build_mix.py [{'|'.join(PROJECTS)}]")
    project = sys.argv[1]
    files = PROJECTS[project]
    base = f"/Users/jungsunbeen/lofi/audio/suno/{project}"

    # 1) 로드 → 무음 제거 → 음량 통일(중앙값 RMS 기준)
    tracks = [trim_silence(load(f"{base}/{f}")) for f in files]
    rmss = [rms(t) for t in tracks]
    target = float(np.median(rmss))
    for i, t in enumerate(tracks):
        t *= target / max(rmss[i], 1e-9)
    print(f"[{project}] {len(tracks)}곡 로드, 목표 RMS {target:.4f}")
    for f, t in zip(files, tracks):
        print(f"  {t.shape[1]/SR:6.1f}s  {f}")

    # 2) 세트 × REPEAT 순서로 펼치기
    playlist = tracks * REPEAT
    xf = int(XFADE * SR)
    # 등파워(사인/코사인) 크로스페이드 창
    t = np.linspace(0, np.pi / 2, xf, dtype=np.float32)
    fade_in, fade_out = np.sin(t), np.cos(t)

    # 3) 총 길이 = Σ길이 - (조인트 수 × xf)
    total = sum(t.shape[1] for t in playlist) - (len(playlist) - 1) * xf
    mix = np.zeros((2, total), dtype=np.float32)

    cursor = 0
    stamps = []
    for idx, seg in enumerate(playlist):
        seg = seg.copy()
        if idx > 0:
            seg[:, :xf] *= fade_in
        if idx < len(playlist) - 1:
            seg[:, -xf:] *= fade_out
        n = seg.shape[1]
        mix[:, cursor:cursor + n] += seg
        if idx < len(tracks):                # 첫 세트만 타임스탬프 기록
            stamps.append((cursor / SR, files[idx]))
        cursor += n - xf

    # 4) 마지막 페이드아웃 + 피크 리미터
    tf = int(TAIL_FADE * SR)
    mix[:, -tf:] *= np.linspace(1, 0, tf, dtype=np.float32) ** 1.5
    peak = float(np.abs(mix).max())
    print(f"피크(리미터 전) {peak:.3f}")
    if peak > 0.985:
        mix = Pedalboard([Limiter(threshold_db=-1.0, release_ms=120)])(mix, SR)
        print(f"피크(리미터 후) {float(np.abs(mix).max()):.3f}")

    # 5) 저장
    out = f"/Users/jungsunbeen/lofi/audio/output/{project}-1hour.wav"
    with wave.open(out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix.T * 32767).astype(np.int16).tobytes())
    print(f"\n저장: {out} ({total/SR/60:.2f}분, 세트 {REPEAT}회)")

    print("\n=== 유튜브 타임스탬프 ===")
    for sec, name in stamps:
        title = name.rsplit(".", 1)[0].replace(" (1)", "").replace("(1)", "")
        print(f"{int(sec)//60:02d}:{int(sec)%60:02d} {title}")
    set_len = total / REPEAT / SR
    print(f"{int(set_len)//60:02d}:{int(set_len)%60:02d} — set repeats —")


if __name__ == "__main__":
    main()
