"""Demucs API로 segment.wav를 4개 스템(드럼/베이스/멜로디 등)으로 분리."""
import numpy as np
import torch
import torchaudio.functional as AF
from demucs.pretrained import get_model
from demucs.apply import apply_model
from pedalboard.io import AudioFile

with AudioFile("segment.wav") as f:
    x = f.read(f.frames)          # (1, n) mono
    sr = f.samplerate

model = get_model("htdemucs")
model.eval()

wav = torch.tensor(x, dtype=torch.float32)
wav = wav.repeat(2, 1)                            # mono -> stereo
wav = AF.resample(wav, int(sr), model.samplerate) # 22050 -> 44100

ref = wav.mean(0)
mean, std = ref.mean(), ref.std()
wav = (wav - mean) / std

with torch.no_grad():
    sources = apply_model(model, wav[None], device="cpu", progress=True)[0]
sources = sources * std + mean

for name, src in zip(model.sources, sources):
    out = src.numpy()
    with AudioFile(f"stem_{name}.wav", "w", model.samplerate, 2) as f:
        f.write(out)
    rms = float(np.sqrt((out ** 2).mean()))
    print(f"stem_{name}.wav  rms={rms:.4f}")
