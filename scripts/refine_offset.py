"""반복 주기 후보를 초 단위로 정밀 보정 후 통반복 여부를 재검증.

사용법: python scripts/refine_offset.py <wav> <candidate_offset_sec> [probe_sec ...]

analyze_mix.py의 주기 후보는 스캔 간격(기본 120초)으로 양자화되어 있어
실제 오프셋과 최대 ±60초 어긋날 수 있다. 첫 프로브 지점에서 ±120초 범위를
슬라이드해 오프셋을 보정한 뒤, 나머지 프로브로 통반복(유사도 ~1.0)을 확인한다.
"""
import sys
import numpy as np
import librosa

WAV = sys.argv[1]
OFF = float(sys.argv[2])
PROBES = [float(x) for x in sys.argv[3:]] or [300, 900, 1500, 2400, 3000]


def cseq(t0, dur):
    y, sr = librosa.load(WAV, sr=None, offset=max(0, t0), duration=dur)
    c = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=4096)
    return c / (np.linalg.norm(c, axis=0, keepdims=True) + 1e-9), sr


def best_lag_sim(a, b):
    na = a.shape[1]
    best, blag = -1.0, 0
    for lag in range(0, b.shape[1] - na):
        s = float(np.mean(np.sum(a * b[:, lag:lag + na], axis=0)))
        if s > best:
            best, blag = s, lag
    return best, blag


t0 = PROBES[0]
a, sr = cseq(t0, 30)
WIN = 120
b, _ = cseq(t0 + OFF - WIN, 2 * WIN + 30)
sim, lag = best_lag_sim(a, b)
dt = 4096 / sr
refined = OFF - WIN + lag * dt
print(f"보정 오프셋: {refined:.1f}s = {refined/60:.2f}분 (후보 {OFF:.0f}s, 유사도 {sim:.3f})")

print("프로브 검증 (통반복이면 ~1.0):")
for t in PROBES:
    a, sr = cseq(t, 30)
    b, _ = cseq(t + refined - 8, 46)
    s, _ = best_lag_sim(a, b)
    print(f"  {t:6.0f}s vs +{refined:.1f}s: {s:.3f}", flush=True)
