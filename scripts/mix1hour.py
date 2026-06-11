"""Paper Sun / Paper Moon — 1시간 로파이 믹스 생성.

ggg. 채널 공식 적용 (ggg-analy.md / compose2.py 주석 참고):
- 같은 곡을 조성(±1~2반음)·미세 템포·필터로 변주하며 A→B→A'→B'… 순환
- 변주는 pedalboard.time_stretch(Rubber Band) 한 번에 피치+템포 처리
- 3초 등파워 크로스페이드로 이어붙여 정확히 60분, 마지막 8초 페이드아웃
- 결과: mix-1hour.wav (16-bit PCM, 48kHz)
"""
import wave
import numpy as np
import pedalboard
from pedalboard import Pedalboard, LowpassFilter, HighShelfFilter, Limiter
from pedalboard.io import AudioFile

SR = 48000
TOTAL = 3600          # 정확히 60분
XFADE = 3.0           # 크로스페이드(초)
TAIL_FADE = 8.0       # 끝 페이드아웃(초)

SONGS = [
    "/Users/jungsunbeen/lofi/suno/Paper Sun.mp3",
    "/Users/jungsunbeen/lofi/suno/Paper Moon.mp3",
]

# (반음, 템포 배속, 필터) — 사이클마다 A·B 둘 다 같은 변주를 적용
VARIANTS = [
    ( 0, 1.000, None),
    (+1, 1.000, "bright"),
    (-1, 0.990, "dark"),
    (+2, 1.010, None),
    (-2, 1.000, "dark"),
    ( 0, 0.985, "dark"),
    (+1, 1.015, "bright"),
    (-1, 1.000, None),
    (+2, 0.990, "dark"),
    (-2, 1.010, "bright"),
]

FILTERS = {
    "dark":   Pedalboard([LowpassFilter(cutoff_frequency_hz=5500)]),
    "bright": Pedalboard([HighShelfFilter(cutoff_frequency_hz=4000, gain_db=1.5)]),
}


def load(path):
    with AudioFile(path) as f:
        audio = f.read(f.frames)  # (ch, n) float32
        assert f.samplerate == SR, f"{path}: {f.samplerate}"
    return audio


def trim_silence(audio, thresh_db=-45.0, pad=0.3):
    """양 끝의 거의 무음 구간 제거 (크로스페이드가 무음과 겹치지 않게)."""
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


def make_variant(src, src_rms, semitones, tempo, filt):
    if semitones == 0 and tempo == 1.0:
        out = src.copy()
    else:
        out = pedalboard.time_stretch(
            src, SR, stretch_factor=tempo, pitch_shift_in_semitones=semitones
        )
    if filt is not None:
        out = FILTERS[filt](out, SR)
    out *= src_rms / max(rms(out), 1e-9)  # 변주 간 음량 통일
    return trim_silence(out)


srcs = [load(p) for p in SONGS]
src_rms = [rms(s) for s in srcs]
print(f"로드 완료: {[round(s.shape[1]/SR,1) for s in srcs]}초, RMS {[round(r,4) for r in src_rms]}")

mix = np.zeros((2, TOTAL * SR), dtype=np.float32)
xf = int(XFADE * SR)
fade_in = np.sin(np.linspace(0, np.pi / 2, xf, dtype=np.float32)) ** 1.0
fade_out = np.cos(np.linspace(0, np.pi / 2, xf, dtype=np.float32))

cursor = 0  # 다음 세그먼트가 시작할 위치
seg_idx = 0
done = False
for cycle, (semi, tempo, filt) in enumerate(VARIANTS):
    if done:
        break
    for si in range(2):
        seg = make_variant(srcs[si], src_rms[si], semi, tempo, filt)
        n = seg.shape[1]
        # 등파워 크로스페이드: 첫 세그먼트 머리 빼고 머리/꼬리에 창 적용
        if seg_idx > 0:
            seg[:, :xf] *= fade_in
        seg[:, -xf:] *= fade_out
        end = cursor + n
        if end >= mix.shape[1]:
            seg = seg[:, : mix.shape[1] - cursor]
            mix[:, cursor:] += seg
            done = True
            print(f"seg{seg_idx:02d} cycle{cycle} {'AB'[si]} {semi:+d}st x{tempo} {filt or '-'}: 60분 도달, 종료")
            break
        mix[:, cursor:end] += seg
        print(f"seg{seg_idx:02d} cycle{cycle} {'AB'[si]} {semi:+d}st x{tempo} {filt or '-'}: "
              f"{n/SR:.1f}s @ {cursor/SR:.1f}s")
        cursor = end - xf
        seg_idx += 1

assert done, "변주 사이클이 60분을 채우지 못함 — VARIANTS를 늘릴 것"

tf = int(TAIL_FADE * SR)
mix[:, -tf:] *= np.linspace(1, 0, tf, dtype=np.float32) ** 1.5

peak = float(np.abs(mix).max())
print(f"피크(리미터 전) {peak:.3f}")
if peak > 0.985:
    # 전체 감쇠 대신 리미터로 크로스페이드 피크만 누름 (음량 유지)
    mix = Pedalboard([Limiter(threshold_db=-1.0, release_ms=120)])(mix, SR)
    print(f"피크(리미터 후) {float(np.abs(mix).max()):.3f}")

with wave.open("/Users/jungsunbeen/lofi/mix-1hour.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix.T * 32767).astype(np.int16).tobytes())
print(f"저장: mix-1hour.wav ({mix.shape[1]/SR/60:.2f}분)")
