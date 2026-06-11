"""ggg-orange-soda.wav에서 코드 진행을 추정한다.

방식: STFT -> 크로마(12 음계 에너지) -> 코드 템플릿 매칭.
곡이 반복 구조이므로 일부 구간만 분석해도 전체 진행을 알 수 있다.
"""
import sys
import wave
import numpy as np

WAV = sys.argv[1] if len(sys.argv) > 1 else "ggg-orange-soda.wav"
SEGMENTS = [(60, 120), (600, 660), (1800, 1860)]  # 초반/중반/후반 1분씩

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# 코드 템플릿 (피치클래스 상대 인덱스)
CHORD_TYPES = {
    "":     [0, 4, 7],
    "m":    [0, 3, 7],
    "maj7": [0, 4, 7, 11],
    "m7":   [0, 3, 7, 10],
    "7":    [0, 4, 7, 10],
}

def load_segment(path, t0, t1):
    w = wave.open(path, "rb")
    sr = w.getframerate()
    w.setpos(int(t0 * sr))
    n = int((t1 - t0) * sr)
    data = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64)
    w.close()
    return data / 32768.0, sr

def chroma_frames(x, sr, win=8192, hop=4096):
    """프레임별 12차원 크로마 벡터."""
    freqs = np.fft.rfftfreq(win, 1 / sr)
    # 분석 대역: 60~2000Hz, 각 bin을 가장 가까운 피치클래스에 귀속
    band = (freqs >= 60) & (freqs <= 2000)
    midi = 69 + 12 * np.log2(freqs[band] / 440.0)
    pc = np.round(midi).astype(int) % 12
    hann = np.hanning(win)
    frames = []
    for s in range(0, len(x) - win, hop):
        spec = np.abs(np.fft.rfft(x[s:s + win] * hann)) ** 2
        v = np.zeros(12)
        np.add.at(v, pc, spec[band])
        frames.append(v)
    return np.array(frames), hop / sr

def best_chord(ch):
    ch = ch / (ch.sum() + 1e-9)
    best, best_s = None, -1
    for root in range(12):
        for suf, ivs in CHORD_TYPES.items():
            tmpl = np.zeros(12)
            for k, iv in enumerate(ivs):
                tmpl[(root + iv) % 12] = 1.0 if k == 0 else 0.85
            tmpl /= tmpl.sum()
            s = ch @ tmpl / (np.linalg.norm(ch) * np.linalg.norm(tmpl) + 1e-9)
            if s > best_s:
                best_s, best = s, NOTE_NAMES[root] + suf
    return best

def estimate_tempo(x, sr):
    """에너지 변화 자기상관으로 BPM 추정."""
    hop = 512
    n = (len(x) // hop) * hop
    e = (x[:n].reshape(-1, hop) ** 2).sum(axis=1)
    flux = np.maximum(np.diff(e), 0)
    flux -= flux.mean()
    ac = np.correlate(flux, flux, "full")[len(flux) - 1:]
    fps = sr / hop
    lo, hi = int(fps * 60 / 160), int(fps * 60 / 60)  # 60~160 BPM
    lag = lo + np.argmax(ac[lo:hi])
    return 60 * fps / lag

for t0, t1 in SEGMENTS:
    x, sr = load_segment(WAV, t0, t1)
    bpm = estimate_tempo(x, sr)
    ch, dt = chroma_frames(x, sr)
    # 2초(약 1마디) 단위로 평균 후 코드 판정
    group = max(1, int(2.0 / dt))
    chords = []
    for i in range(0, len(ch) - group, group):
        chords.append(best_chord(ch[i:i + group].sum(axis=0)))
    # 연속 중복 제거
    seq = [chords[0]] + [c for a, c in zip(chords, chords[1:]) if c != a]
    print(f"--- {t0}s ~ {t1}s  (BPM 추정: {bpm:.0f}) ---")
    print("  타임라인:", " ".join(chords))
    print("  변화 순서:", " -> ".join(seq))
    print()
