"""amber glow. — ggg. orange soda. 전사 데이터에서 추출한 문법으로 작곡.

전사로 확인된 레시피:
- A장조(E 믹솔리디안 색채), 베이스 루트: E(2마디) -> A -> B -> A 순환
- 베이스: 긴 루트(2~3박) + 옥타브 고스트 + 코드 전환 직전 경과음
- 코드: 5~6음 클러스터 보이싱 (add9/6th, A3~C#5), 풍성하게
- 멜로디: D4~A4 좁은 음역, 중앙 E4, 같은 음 반복, 당김음 위치, 띄엄띄엄
- 드럼: 매우 성기고 작게 (마디당 킥 1~2, 스네어 2·4 약하게)
"""
import random
import numpy as np
import tinysoundfont
from pedalboard import Pedalboard, Compressor, Gain, LadderFilter, Limiter, Reverb
from pedalboard.io import AudioFile

SR = 44100
BPM = 83
BEAT = 60 / BPM
BAR = BEAT * 4
DUR = 180
SEED = 777

# ---------- 레시피 기반 곡 데이터 ----------
# 4마디 순환: A6/9(베이스E) -> A6(베이스E) -> Bm7/A(베이스B) -> Amaj7(베이스A)
CHORDS = [
    [57, 59, 61, 64, 66],   # A6/9  (A B C# E F#)
    [57, 61, 64, 66, 69],   # A6    (A C# E F# A)
    [57, 59, 62, 66, 69],   # Bm7/A (A B D F# A)
    [57, 61, 64, 68],       # Amaj7 (A C# E G#)
]
BASSL = [28, 28, 35, 33]    # E1 E1 B1 A1
SCALE = [57, 59, 61, 62, 64, 66, 69]  # A B C# D E F# A — 멜로디 재료

# 테마: 전사된 프레이징 모방(같은 음 반복, 당김음, 좁은 음역) — 음 배열은 창작
THEME = [
    (1.25, 62, 0.8), (1.75, 59, 0.3), (2.5,  59, 0.25), (3.75, 59, 0.5),  # D B B B
    (4.5,  64, 0.5), (5.0,  64, 0.25), (5.6,  66, 0.5), (7.0,  62, 1.2),  # E E F# D~
    (8.75, 66, 0.25), (9.4,  66, 0.4), (10.0, 62, 0.6),                   # F# F# D
    (12.25, 64, 0.4), (12.75, 59, 0.4), (13.25, 57, 1.0), (14.5, 61, 1.3),# E B A C#~
]

rnd = random.Random(SEED)
events = []

def note(t, chan, key, dur, vel):
    events.append((t, 'on', chan, key, vel))
    events.append((t + dur, 'off', chan, key, 0))

swing = BEAT * 0.08
n_bars = int((DUR - 4) / BAR)

for bar in range(n_bars):
    t0 = 0.2 + bar * BAR
    ci = bar % 4

    # 코드: 풍성한 클러스터 보이싱, 마디 머리 한 번 길게
    for i, m in enumerate(CHORDS[ci]):
        note(t0 + i * 0.02 + rnd.random() * 0.012, 0, m, BAR * 0.97, 44)
    if rnd.random() < 0.35:  # 가끔 2박 반에서 윗 성부만 다시
        for m in CHORDS[ci][-3:]:
            note(t0 + BEAT * 2.5, 0, m, BAR * 0.4, 30)

    # 베이스: 긴 루트 + 옥타브 고스트 + 전환 경과음 (전사 패턴)
    root = BASSL[ci]
    note(t0, 2, root, BEAT * 2.8, 88)
    if rnd.random() < 0.7:
        note(t0 + BEAT * 1.45, 2, root + 12, BEAT * 0.25, 48)   # 옥타브 고스트
    if rnd.random() < 0.5:
        note(t0 + BEAT * 3.3, 2, root + 12, BEAT * 0.5, 58)
    nxt = BASSL[(bar + 1) % 4]
    if rnd.random() < 0.5:
        note(t0 + BEAT * 3.6, 2, nxt + 7, BEAT * 0.35, 50)      # 5도 어프로치

    # 드럼: 성기고 부드럽게 (전사: 마디당 킥 1~2, 모든 타격 소리 작음)
    note(t0, 9, 35, 0.3, 78)
    if rnd.random() < 0.45:
        note(t0 + BEAT * (2 if rnd.random() < 0.5 else 2.5), 9, 35, 0.3, 58)
    note(t0 + BEAT, 9, 38, 0.3, 44)
    note(t0 + BEAT * 3, 9, 38, 0.3, 44)
    for i in range(8):
        if rnd.random() < 0.6:  # 햇도 빈칸 많이
            sw = swing if i % 2 == 1 else 0
            note(t0 + BEAT * 0.5 * i + sw, 9, 42, 0.2, 24 if i % 2 == 0 else 18)

    # 멜로디: 테마 변주 (16박 = 4마디 주기), 4프레이즈마다 휴식
    rest = (bar // 4) % 4 == 3
    skip = 0.6 if rest else 0.12
    start, end = (bar % 4) * 4, (bar % 4) * 4 + 4
    for p, n, d in THEME:
        if not (start <= p < end):
            continue
        if rnd.random() < skip:
            continue
        key = n
        v = rnd.random()
        if v < 0.15 and n in SCALE:  # 이웃 음 변주
            i = SCALE.index(n)
            if 0 < i < len(SCALE) - 1:
                key = SCALE[i + (1 if rnd.random() < 0.5 else -1)]
        jit = (rnd.random() - 0.5) * 0.05
        sw = swing if (p % 1) != 0 else 0
        note(t0 + (p - start) * BEAT + sw + jit, 1, key, d * BEAT, 58 + rnd.randint(0, 14))

# ---------- 렌더 ----------
synth = tinysoundfont.Synth(samplerate=SR)
sfid = synth.sfload("GeneralUserGS.sf2")
synth.program_select(0, sfid, 0, 4)          # EP1 코드
synth.program_select(1, sfid, 0, 4)          # EP1 멜로디
synth.program_select(2, sfid, 0, 32)         # 어쿠스틱 베이스
synth.program_select(9, sfid, 128, 0, True)  # 드럼

events.sort(key=lambda e: e[0])
out, cursor = [], 0
for t, kind, ch, key, vel in events:
    f = int(t * SR)
    if f > cursor:
        buf = synth.generate(f - cursor)
        out.append(np.frombuffer(buf, dtype=np.float32).reshape(-1, 2).copy())
        cursor = f
    synth.noteon(ch, key, vel) if kind == 'on' else synth.noteoff(ch, key)
out.append(np.frombuffer(synth.generate(int(2.5 * SR)), dtype=np.float32).reshape(-1, 2).copy())
audio = np.concatenate(out).T
print(f"렌더: {audio.shape[1]/SR:.1f}초, peak {np.abs(audio).max():.3f}")

board = Pedalboard([
    LadderFilter(mode=LadderFilter.Mode.LPF12, cutoff_hz=1500),
    Compressor(threshold_db=-18, ratio=3),
    Reverb(room_size=0.4, wet_level=0.12, dry_level=0.88),
    Gain(gain_db=5),
    Limiter(threshold_db=-1),
])
processed = board(audio, SR)

crackle_rnd = np.random.default_rng(SEED)
n = processed.shape[1]
ticks = (crackle_rnd.random(n) < 0.0004) * crackle_rnd.normal(0, 0.5, n)
hiss = crackle_rnd.normal(0, 0.0012, n)
processed = processed + (ticks * 0.05 + hiss)[None, :]

with AudioFile("amber-glow.wav", "w", SR, 2) as f:
    f.write(processed.astype(np.float32))
print("저장: amber-glow.wav")
