"""렌더된 wav에서 슬롯 단위로 코드를 검출해 출력 (compose_fo.py 검증용).


사용법: python scripts/check_chords.py <wav> [slot_sec]
verify_matcha.py와 같은 크로마 템플릿 매칭. slot_sec 기본 1.875초
(= 64 BPM 반마디 — 세컨더리 도미넌트가 마디 후반 2박에 들어가므로).
"""
import sys
import numpy as np
import librosa

WAV = sys.argv[1]
SLOT = float(sys.argv[2]) if len(sys.argv) > 2 else 1.875

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
CHORD_TYPES = {
    "":     [0, 4, 7],
    "m":    [0, 3, 7],
    "maj7": [0, 4, 7, 11],
    "m7":   [0, 3, 7, 10],
    "7":    [0, 4, 7, 10],
}


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


y, sr = librosa.load(WAV, sr=22050, mono=True)
chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=512)
dt = 512 / sr
per_slot = int(SLOT / dt)
total = chroma.shape[1] * dt
print(f"{WAV}: {total:.1f}초, 슬롯 {SLOT}초")
line = []
for i, s0 in enumerate(range(0, chroma.shape[1] - per_slot, per_slot)):
    c = best_chord(chroma[:, s0:s0 + per_slot].sum(axis=1))
    line.append(f"{c:>6s}")
    if len(line) == 8:
        t = (i - 7) * SLOT
        print(f"  {t:6.1f}s | {' '.join(line)}")
        line = []
if line:
    print(f"  {'':6s} | {' '.join(line)}")
