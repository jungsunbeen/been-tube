"""스템 -> MIDI 전사 + ggg. 작곡 문법 추출 리포트."""
import numpy as np
import pathlib
import scipy.signal
import scipy.signal.windows
scipy.signal.gaussian = scipy.signal.windows.gaussian  # 신버전 scipy 호환 패치
import basic_pitch
from basic_pitch.inference import predict
ONNX_MODEL = pathlib.Path(basic_pitch.__file__).parent / "saved_models/icassp_2022/nmp.onnx"
from pedalboard.io import AudioFile

BPM = 83.0
BEAT = 60 / BPM
BAR = BEAT * 4

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
nn = lambda m: NOTE_NAMES[m % 12] + str(m // 12 - 1)

# ---------- 1) 베이스 / 건반 전사 ----------
def transcribe(path):
    _, midi, events = predict(path, ONNX_MODEL)
    midi.write(path.replace(".wav", ".mid"))
    # (start, end, pitch, amplitude)
    return sorted([(e[0], e[1], e[2], e[3]) for e in events])

print("전사 중... (bass)")
bass = transcribe("stem_bass.wav")
print("전사 중... (other=건반/멜로디)")
other = transcribe("stem_other.wav")

# 비트 그리드 원점: 첫 베이스 음을 마디 머리로 가정
t_origin = bass[0][0] if bass else 0.0
qbeat = lambda t: (t - t_origin) / BEAT  # 박 단위 위치

print(f"\n=== 베이스 (음 {len(bass)}개) ===")
print("마디내위치(박)  음   길이(박)  세기")
for s, e, p, a in bass[:24]:
    b = qbeat(s)
    print(f"  {b % 4:4.2f} (bar {int(b // 4):2d})   {nn(p):4s}  {(e - s) / BEAT:4.2f}   {a:.2f}")

# 마디별 베이스 루트 -> 진행
roots = {}
for s, e, p, a in bass:
    bar = int(qbeat(s) // 4)
    if a > 0.3:
        roots.setdefault(bar, []).append(p % 12)
prog = [NOTE_NAMES[max(set(v), key=v.count)] for k, v in sorted(roots.items())]
print("마디별 루트:", " ".join(prog))

print(f"\n=== 건반/멜로디 (음 {len(other)}개) ===")
pitches = [p for _, _, p, _ in other]
print(f"음역: {nn(min(pitches))} ~ {nn(max(pitches))}")
print(f"30초당 음 수: {len(other) / 2:.0f}")

# 동시발음(코드) vs 단선율(멜로디) 구분: 시작이 80ms 이내로 겹치면 코드 블록
other_sorted = sorted(other)
blocks, cur = [], [other_sorted[0]]
for ev in other_sorted[1:]:
    if ev[0] - cur[-1][0] < 0.08:
        cur.append(ev)
    else:
        blocks.append(cur); cur = [ev]
blocks.append(cur)

chords = [b for b in blocks if len(b) >= 3]
melody = [b[0] for b in blocks if len(b) == 1]
print(f"코드 블록 {len(chords)}개 / 단선율 음 {len(melody)}개")

print("\n코드 보이싱 (처음 8개):")
for b in chords[:8]:
    notes = sorted(set(p for _, _, p, _ in b))
    print(f"  bar {int(qbeat(b[0][0]) // 4):2d} @ {qbeat(b[0][0]) % 4:4.2f}박:", " ".join(nn(p) for p in notes))

print("\n멜로디 라인 (시간순 24개):")
for s, e, p, a in melody[:24]:
    b = qbeat(s)
    print(f"  bar {int(b // 4):2d} @ {b % 4:4.2f}박  {nn(p):4s} 길이 {(e - s) / BEAT:.2f}박 세기 {a:.2f}")

mel_p = [p for _, _, p, _ in melody]
if mel_p:
    print(f"멜로디 음역: {nn(min(mel_p))} ~ {nn(max(mel_p))}, 중앙 {nn(int(np.median(mel_p)))}")
    iv = np.diff(mel_p)
    print(f"인접 음 간격(반음) 분포: 중앙값 {np.median(np.abs(iv)):.0f}, 최대 {np.abs(iv).max()}")

# ---------- 2) 드럼 패턴 (대역별 온셋) ----------
with AudioFile("stem_drums.wav") as f:
    d = f.read(f.frames).mean(axis=0)
    sr = int(f.samplerate)

def band_onsets(x, sr, lo, hi, thresh_ratio):
    spec_hop = 512
    n = (len(x) // spec_hop) * spec_hop
    frames = x[:n].reshape(-1, spec_hop)
    win = np.hanning(spec_hop)
    S = np.abs(np.fft.rfft(frames * win, axis=1))
    freqs = np.fft.rfftfreq(spec_hop, 1 / sr)
    m = (freqs >= lo) & (freqs < hi)
    env = S[:, m].sum(axis=1)
    flux = np.maximum(np.diff(env), 0)
    th = flux.mean() + thresh_ratio * flux.std()
    on = []
    last = -10
    for i, v in enumerate(flux):
        if v > th and i - last > 4:
            on.append(i * spec_hop / sr); last = i
    return on

kick = band_onsets(d, sr, 30, 120, 2.0)
snare = band_onsets(d, sr, 180, 1200, 2.0)
hat = band_onsets(d, sr, 4000, 11000, 1.5)

print(f"\n=== 드럼 (60초) ===  kick {len(kick)} / snare {len(snare)} / hat {len(hat)}")
def grid16(ons):
    pos = sorted(set(round((qbeat(t) % 4) * 4) / 4 for t in ons))
    hist = {}
    for t in ons:
        g = round((qbeat(t) % 4) * 4) / 4
        hist[g] = hist.get(g, 0) + 1
    return sorted(hist.items(), key=lambda kv: -kv[1])[:6]
print("킥 위치(박, 빈도순):  ", grid16(kick))
print("스네어 위치(박, 빈도순):", grid16(snare))
print("햇 위치(박, 빈도순):  ", grid16(hat))
