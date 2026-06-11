"""blue hour. — 새 작곡 (F장조, 78 BPM 로파이)

파이프라인: 작곡(이벤트 스케줄) -> tinysoundfont 렌더(GeneralUser GS 샘플)
          -> pedalboard 이펙트(로파이 톤) -> WAV
"""
import random
import numpy as np
import tinysoundfont
from pedalboard import Pedalboard, Compressor, Gain, LadderFilter, Limiter, Reverb
from pedalboard.io import AudioFile

SR = 44100
BPM = 78
BEAT = 60 / BPM
BAR = BEAT * 4
DUR = 180          # 렌더 길이(초)
SEED = 20260611

# ---------- 곡 데이터 ----------
# 진행: Fmaj7 - Am7 - Bbmaj7 - C7sus  (F장조 I - iii - IV - V7sus)
CHORDS = [
    [53, 57, 60, 64],   # Fmaj7
    [57, 60, 64, 67],   # Am7
    [46, 50, 53, 57],   # Bbmaj7
    [48, 53, 55, 58],   # C7sus
]
BASSL = [41, 45, 46, 36]            # F2 A2 Bb2 C2
SCALE = [57, 58, 60, 62, 64, 65, 67, 69]  # F장조 중간 음역

# 테마: 중간 음역(C4~A4), 부드럽게 오르내리다 F로 해결
THEME = [
    (0.5,  60, 1.0), (2,    65, 1.0), (3.5,  67, 1.5),   # Fmaj7
    (5,    64, 1.0), (6.5,  60, 1.5),                     # Am7
    (8.5,  62, 0.75), (10,   65, 1.0), (11,   69, 1.5),   # Bbmaj7
    (13,   67, 0.75), (14,   64, 0.75), (14.75, 65, 2.0), # C7sus -> F 해결
]

# ---------- 이벤트 스케줄 ----------
rnd = random.Random(SEED)
events = []  # (time, 'on'|'off', chan, key, vel)

def note(t, chan, key, dur, vel):
    events.append((t, 'on', chan, key, vel))
    events.append((t + dur, 'off', chan, key, 0))

swing = BEAT * 0.08
n_bars = int((DUR - 4) / BAR)

for bar in range(n_bars):
    t0 = 0.2 + bar * BAR
    ci = bar % 4

    # 코드 (채널0 일렉피아노, 아르페지오처럼 살짝 어긋나게)
    for i, m in enumerate(CHORDS[ci]):
        note(t0 + i * 0.018 + rnd.random() * 0.01, 0, m, BAR * 0.95, 48)
    if rnd.random() < 0.5:
        for i, m in enumerate(CHORDS[ci]):
            note(t0 + BEAT * 2.5 + i * 0.015, 0, m, BAR * 0.45, 34)

    # 베이스 (채널2 어쿠스틱 베이스)
    note(t0, 2, BASSL[ci], BEAT * 1.9, 92)
    if rnd.random() < 0.6:
        note(t0 + BEAT * 2.5, 2, BASSL[ci], BEAT * 1.3, 72)
    if rnd.random() < 0.25:  # 다음 코드로 가는 경과음
        note(t0 + BEAT * 3.5, 2, BASSL[(ci + 1) % 4] + 7, BEAT * 0.4, 60)

    # 드럼 (채널9): 고정 붐뱁
    note(t0, 9, 35, 0.3, 105)
    note(t0 + BEAT * 2.5, 9, 35, 0.3, 78)
    note(t0 + BEAT, 9, 38, 0.3, 58)
    note(t0 + BEAT * 3, 9, 38, 0.3, 58)
    for i in range(8):
        sw = swing if i % 2 == 1 else 0
        note(t0 + BEAT * 0.5 * i + sw, 9, 42, 0.2, 36 if i % 2 == 0 else 26)
    if bar % 4 == 3:
        note(t0 + BEAT * 3.5 + swing, 9, 46, 0.4, 32)

    # 멜로디 (채널1): 테마 변주, 4프레이즈마다 쉬어가기
    rest = (bar // 4) % 4 == 3
    skip = 0.55 if rest else 0.10
    start, end = (bar % 4) * 4, (bar % 4) * 4 + 4
    for p, n, d in THEME:
        if not (start <= p < end):
            continue
        if rnd.random() < skip:
            continue
        key = n
        v = rnd.random()
        if v < 0.12:  # 이웃 음으로 변주 (스케일 내)
            i = SCALE.index(n) if n in SCALE else -1
            if 0 < i < len(SCALE) - 1:
                key = SCALE[i + (1 if rnd.random() < 0.5 else -1)]
        jit = (rnd.random() - 0.5) * 0.04
        sw = swing if (p % 1) != 0 else 0
        note(t0 + (p - start) * BEAT + sw + jit, 1, key, d * BEAT * 1.2, 64 + rnd.randint(0, 12))

# ---------- 렌더 ----------
synth = tinysoundfont.Synth(samplerate=SR)
sfid = synth.sfload("GeneralUserGS.sf2")
synth.program_select(0, sfid, 0, 4)              # Electric Piano 1 (코드)
synth.program_select(1, sfid, 0, 4)              # Electric Piano 1 (멜로디)
synth.program_select(2, sfid, 0, 32)             # Acoustic Bass
synth.program_select(9, sfid, 128, 0, True)      # GM Drums

events.sort(key=lambda e: e[0])
out = []
cursor = 0  # 현재 프레임
for t, kind, ch, key, vel in events:
    f = int(t * SR)
    if f > cursor:
        buf = synth.generate(f - cursor)
        out.append(np.frombuffer(buf, dtype=np.float32).reshape(-1, 2).copy())
        cursor = f
    if kind == 'on':
        synth.noteon(ch, key, vel)
    else:
        synth.noteoff(ch, key)
out.append(np.frombuffer(synth.generate(int(2.5 * SR)), dtype=np.float32).reshape(-1, 2).copy())
audio = np.concatenate(out).T  # (2, frames)
print(f"렌더 완료: {audio.shape[1]/SR:.1f}초, peak {np.abs(audio).max():.3f}")

# ---------- 로파이 후처리 (원곡 실측 프로파일 반영) ----------
board = Pedalboard([
    LadderFilter(mode=LadderFilter.Mode.LPF12, cutoff_hz=1600),  # 먹먹한 톤
    Compressor(threshold_db=-18, ratio=3),
    Reverb(room_size=0.35, wet_level=0.10, dry_level=0.9),
    Gain(gain_db=4),
    Limiter(threshold_db=-1),
])
processed = board(audio, SR)

# 빈티지 크래클: 성긴 틱 + 옅은 히스 (필터 뒤에 섞어 고역 유지)
n = processed.shape[1]
crackle_rnd = np.random.default_rng(SEED)
ticks = (crackle_rnd.random(n) < 0.0004) * crackle_rnd.normal(0, 0.5, n)
hiss = crackle_rnd.normal(0, 0.0012, n)
processed = processed + (ticks * 0.05 + hiss)[None, :]

with AudioFile("blue-hour.wav", "w", SR, 2) as f:
    f.write(processed.astype(np.float32))
print("저장: blue-hour.wav")
