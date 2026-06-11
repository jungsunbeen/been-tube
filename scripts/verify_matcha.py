"""ggg-analy.md의 matcha 분석 내용을 librosa 기반으로 독립 검증한다.

검증 항목:
1. 구간별 BPM (주장: 1분~ 83, 10분~ 86, 30분~ 76)
2. 구간별 조성/코드 (주장: 초반 A장조권 F#m7-C#m7-Dmaj7-A,
   중반 C장조권 Dm7-G7-C-Gm7, 후반 플랫조 Fmaj7-Bbmaj7-Dbmaj7)
3. 전곡 2분 간격 스캔으로 조옮김 타임라인 확인
"""
import sys
import numpy as np
import librosa

WAV = sys.argv[1] if len(sys.argv) > 1 else "ggg-matcha.wav"

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Krumhansl-Schmuckler 조성 프로파일
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
    """옥타브 오류 보정: 55~115 범위로 접는다."""
    while b > 115:
        b /= 2
    while b < 55:
        b *= 2
    return b


def analyze(t0, dur=60, chords=False):
    y, sr = librosa.load(WAV, sr=None, offset=t0, duration=dur)
    onset = librosa.onset.onset_strength(y=y, sr=sr)
    tempo = librosa.feature.tempo(onset_envelope=onset, sr=sr)[0]
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    key, r = estimate_key(chroma.mean(axis=1))
    out = {"bpm_raw": tempo, "bpm": fold_bpm(tempo), "key": key, "key_r": r}
    if chords:
        dt = 512 / sr
        group = max(1, int(2.0 / dt))
        seq = []
        for i in range(0, chroma.shape[1] - group, group):
            seq.append(best_chord(chroma[:, i:i + group].sum(axis=1)))
        dedup = [seq[0]] + [c for a, c in zip(seq, seq[1:]) if c != a]
        out["chords"] = seq
        out["dedup"] = dedup
    return out


print("=== 1) 주장 구간 상세 검증 ===")
for t0, claim in [(60, "83 BPM / A장조권"), (600, "86 BPM / C장조권"), (1800, "76 BPM / 플랫조")]:
    a = analyze(t0, 60, chords=True)
    print(f"\n--- {t0}s~{t0+60}s (주장: {claim}) ---")
    print(f"  BPM: {a['bpm']:.1f} (raw {a['bpm_raw']:.1f})   조성: {a['key']} (r={a['key_r']:.2f})")
    print(f"  코드 변화: {' -> '.join(a['dedup'])}")

print("\n=== 2) 전곡 2분 간격 스캔 (조옮김 타임라인) ===")
total = librosa.get_duration(path=WAV)
print(f"총 길이: {total:.1f}s = {total/60:.1f}분")
for t0 in range(60, int(total) - 60, 120):
    a = analyze(t0, 45)
    print(f"  {t0//60:3d}분: BPM {a['bpm']:6.1f}  | {a['key']:9s} (r={a['key_r']:.2f})")
