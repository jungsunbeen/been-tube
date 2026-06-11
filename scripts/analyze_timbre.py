"""ggg. 원곡의 음색 특성 측정: 어떤 악기 계열인지 추정하기 위한 진단.

측정 항목
- 스펙트럼 중심(밝기): 낮을수록 어두운/먹먹한 톤
- 대역별 에너지 분포: 저음/중음/고음 비율
- 어택 날카로움: 음 시작이 퉁(플럭)인지 스르륵(키/패드)인지
"""
import sys
import wave
import numpy as np

WAV = sys.argv[1]
T0, T1 = 60, 90  # 분석 구간

w = wave.open(WAV, "rb")
sr = w.getframerate()
w.setpos(int(T0 * sr))
x = np.frombuffer(w.readframes(int((T1 - T0) * sr)), dtype=np.int16).astype(np.float64) / 32768.0
w.close()

win, hop = 4096, 2048
hann = np.hanning(win)
freqs = np.fft.rfftfreq(win, 1 / sr)

cents, roll, specs = [], [], []
for s in range(0, len(x) - win, hop):
    spec = np.abs(np.fft.rfft(x[s:s + win] * hann))
    p = spec ** 2
    tot = p.sum() + 1e-12
    cents.append((freqs * p).sum() / tot)
    cum = np.cumsum(p)
    roll.append(freqs[np.searchsorted(cum, 0.85 * cum[-1])])
    specs.append(p)
specs = np.array(specs)

bands = [(0, 200), (200, 800), (800, 2000), (2000, 5000), (5000, 11025)]
tot = specs.sum()
print(f"=== {WAV}  ({T0}~{T1}s) ===")
print(f"스펙트럼 중심(평균): {np.mean(cents):.0f} Hz")
print(f"85% 롤오프(평균):   {np.mean(roll):.0f} Hz")
print("대역별 에너지:")
for lo, hi in bands:
    m = (freqs >= lo) & (freqs < hi)
    print(f"  {lo:>5}-{hi:<5} Hz: {100 * specs[:, m].sum() / tot:5.1f}%")

# 어택 분석: 멜로디 대역(500-2500Hz) 엔벨로프의 상승 속도
m = (freqs >= 500) & (freqs < 2500)
env = specs[:, m].sum(axis=1)
env = env / env.max()
dt = hop / sr
rise = np.maximum(np.diff(env), 0)
peaks = np.where(rise > rise.mean() + 2.5 * rise.std())[0]
if len(peaks):
    # 각 온셋에서 피크까지 도달 시간
    times = []
    for pk in peaks[:60]:
        j = pk
        while j + 1 < len(env) and env[j + 1] > env[j]:
            j += 1
        times.append((j - pk) * dt)
    print(f"멜로디 대역 온셋 수(30초): {len(peaks)}")
    print(f"어택 도달 시간 중앙값: {np.median(times)*1000:.0f} ms  (짧을수록 퉁 하고 튀는 소리)")
