"""fo. 스타일 단일 무드 작곡 — C장조권 64 BPM 고정 + 세컨더리 도미넌트 엔진.

fo-vege-acnh-analy.md에서 확인한 fo. 공식의 코드화:
- 키/템포 고정 (C장조권, 64 BPM) — 다양성은 조옮김이 아니라 코드 컬러로
- 다이어토닉 7th 순환(기능화성 전이표) 위에 세컨더리 도미넌트를 확률 삽입:
  E7→Am7, A7→Dm7, D7→G7, B7→Em7, C7→Fmaj7 (V7/타깃 = 타깃 루트의 완전5도 위)
- 보이싱은 직전 코드와 가장 가까운 옥타브를 고르는 최소 이동 보이스리딩
"""
import random
import numpy as np
import tinysoundfont
from pedalboard import Pedalboard, Compressor, Gain, LadderFilter, Limiter, Reverb
from pedalboard.io import AudioFile

SR = 44100
BPM = 64
BEAT = 60 / BPM
BAR = BEAT * 4
DUR = 124
SEED = 42
P_SECDOM = 0.45          # 마디 후반을 세컨더리 도미넌트로 쪼갤 확률
OUT = "audio/output/fo-style-demo.wav"

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
ROMAN = {1: "I", 2: "ii", 3: "iii", 4: "IV", 5: "V", 6: "vi"}
DIATONIC = {1: (0, "maj7"), 2: (2, "m7"), 3: (4, "m7"),
            4: (5, "maj7"), 5: (7, "7"), 6: (9, "m7")}
# 기능화성 전이표 (중복 = 가중치)
NEXT = {1: [6, 4, 2, 3, 4], 2: [5, 5, 3], 3: [6, 4], 4: [5, 2, 1], 5: [1, 1, 6], 6: [2, 4, 2]}
CHORD_IV = {"maj7": [0, 4, 7, 11], "m7": [0, 3, 7, 10], "7": [0, 4, 7, 10]}
PENTA = [60, 62, 64, 67, 69, 72, 74]  # C D E G A — 멜로디 재료

rnd = random.Random(SEED)


def chord_name(root_pc, q):
    return NOTE_NAMES[root_pc] + ("" if q == "maj" else q)


def gen_progression(n_bars):
    """마디별 [(시작박, 길이박, 루트pc, 타입, 라벨)] 목록 생성."""
    deg, bars = 1, []
    for _ in range(n_bars):
        nxt = rnd.choice(NEXT[deg])
        root, q = DIATONIC[deg]
        slots = [(0, 4, root, q, ROMAN[deg])]
        # 세컨더리 도미넌트: 다음 코드 루트의 완전5도 위 도미넌트 7th.
        # V7/I = G7은 다이어토닉 V와 같으므로 제외.
        if nxt != 1 and rnd.random() < P_SECDOM:
            sd_root = (DIATONIC[nxt][0] + 7) % 12
            slots = [(0, 2, root, q, ROMAN[deg]),
                     (2, 2, sd_root, "7", f"V7/{ROMAN[nxt]}")]
        bars.append(slots)
        deg = nxt
    return bars


def voice(root_pc, q, prev):
    """최소 이동 보이스리딩: 각 코드톤을 직전 보이싱 중심에 가장 가까운 옥타브로."""
    center = np.mean(prev) if prev else 64.0
    notes = []
    for iv in CHORD_IV[q]:
        pc = (root_pc + iv) % 12
        cands = [pc + 12 * o for o in range(3, 7) if 53 <= pc + 12 * o <= 76]
        notes.append(min(cands, key=lambda n: abs(n - center)))
    if rnd.random() < 0.4:  # 9th 컬러
        pc9 = (root_pc + 2) % 12
        cands = [pc9 + 12 * o for o in range(3, 7) if 60 <= pc9 + 12 * o <= 78]
        notes.append(min(cands, key=lambda n: abs(n - center - 5)))
    return sorted(set(notes))


events = []


def note(t, chan, key, dur, vel):
    events.append((t, 'on', chan, key, vel))
    events.append((t + dur, 'off', chan, key, 0))


n_bars = int((DUR - 4) / BAR)
prog = gen_progression(n_bars)

print("진행:")
for b, slots in enumerate(prog):
    lbl = " -> ".join(f"{chord_name(r, q)}({l})" for _, _, r, q, l in slots)
    print(f"  {b + 1:2d}: {lbl}")

swing = BEAT * 0.08
prev_voicing = None
for bar, slots in enumerate(prog):
    t0 = 0.2 + bar * BAR

    # 코드 + 베이스: 슬롯(통마디 또는 전반/후반)별로
    for beat_pos, beats, root_pc, q, _ in slots:
        ts = t0 + beat_pos * BEAT
        v = voice(root_pc, q, prev_voicing)
        prev_voicing = v
        for i, m in enumerate(v):
            note(ts + i * 0.02 + rnd.random() * 0.012, 0, m, beats * BEAT * 0.95, 42)
        bass = root_pc + 24 if root_pc >= 5 else root_pc + 36  # E1~G#2 영역
        note(ts, 2, bass, beats * BEAT * 0.7, 86)
        if beats == 4 and rnd.random() < 0.6:
            note(ts + BEAT * 1.45, 2, bass + 12, BEAT * 0.25, 46)  # 옥타브 고스트

    # 드럼: compose2의 성긴 붐뱁 그대로
    note(t0, 9, 35, 0.3, 76)
    if rnd.random() < 0.45:
        note(t0 + BEAT * (2 if rnd.random() < 0.5 else 2.5), 9, 35, 0.3, 56)
    note(t0 + BEAT, 9, 38, 0.3, 42)
    note(t0 + BEAT * 3, 9, 38, 0.3, 42)
    for i in range(8):
        if rnd.random() < 0.55:
            sw = swing if i % 2 == 1 else 0
            note(t0 + BEAT * 0.5 * i + sw, 9, 42, 0.2, 22 if i % 2 == 0 else 16)

    # 멜로디: 펜타토닉 띄엄띄엄, 4마디마다 한 마디 휴식
    if bar % 4 != 3:
        t = rnd.choice([0.5, 1.0, 1.25])
        last = rnd.choice(PENTA[2:5])
        while t < 3.6:
            if rnd.random() < 0.55:
                i = PENTA.index(last)
                last = PENTA[max(0, min(len(PENTA) - 1, i + rnd.choice([-2, -1, -1, 0, 1, 1, 2])))]
                sw = swing if (t % 1) != 0 else 0
                note(t0 + t * BEAT + sw, 1, last, rnd.choice([0.4, 0.6, 1.0]) * BEAT,
                     56 + rnd.randint(0, 14))
            t += rnd.choice([0.5, 0.75, 1.0, 1.5])

# ---------- 렌더 ----------
synth = tinysoundfont.Synth(samplerate=SR)
sfid = synth.sfload("models/GeneralUserGS.sf2")
synth.program_select(0, sfid, 0, 4)
synth.program_select(1, sfid, 0, 4)
synth.program_select(2, sfid, 0, 32)
synth.program_select(9, sfid, 128, 0, True)

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

with AudioFile(OUT, "w", SR, 2) as f:
    f.write(processed.astype(np.float32))
print(f"저장: {OUT}")
