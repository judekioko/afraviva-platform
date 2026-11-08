"""Synthesise an original 45s cinematic promo bed (no samples, no licensing).

Usage: python3 video/tools/make_music.py static/audio/promo-bed.mp3
"""
import subprocess, sys, wave
import numpy as np

SR, DUR, BPM = 44100, 45.0, 100
N = int(SR * DUR)
beat = 60 / BPM
rng = np.random.default_rng(7)
out = np.zeros((N, 2))


def add(sig, t0, gain=1.0, pan=0.0):
    i = int(t0 * SR)
    if i >= N:
        return
    sig = sig[: N - i]
    out[i : i + len(sig), 0] += sig * gain * (1 - max(pan, 0))
    out[i : i + len(sig), 1] += sig * gain * (1 + min(pan, 0))


def t_(d):
    return np.arange(int(SR * d)) / SR


def lowpass(x, k):  # simple one-pole filter
    a = np.exp(-2 * np.pi * k / SR)
    y = np.zeros_like(x)
    acc = 0.0
    for n in range(len(x)):
        acc = a * acc + (1 - a) * x[n]
        y[n] = acc
    return y


def kick():
    t = t_(0.45)
    f = 45 + 110 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)


def hat():
    t = t_(0.08)
    n = rng.standard_normal(len(t))
    n = n - lowpass(n, 6000)
    return n * np.exp(-t * 60) * 0.5


def boom(d=3.5):
    t = t_(d)
    sub = np.sin(2 * np.pi * 40 * t) * np.exp(-t * 1.1)
    n = lowpass(rng.standard_normal(len(t)), 900) * np.exp(-t * 2.2) * 2.5
    crash = (rng.standard_normal(len(t)) - lowpass(rng.standard_normal(len(t)), 4000)) * np.exp(-t * 2.5) * 0.35
    return sub * 1.2 + n * 0.6 + crash


def pad(freqs, d):
    t = t_(d)
    s = np.zeros_like(t)
    for f in freqs:
        for det in (-0.004, 0, 0.004):
            s += np.sin(2 * np.pi * f * (1 + det) * t) + 0.4 * np.sin(4 * np.pi * f * (1 + det) * t)
    env = np.minimum(t / 0.8, 1) * np.minimum((d - t) / 0.8, 1)
    return s / (len(freqs) * 3) * env


def pluck(f, d=0.5):
    t = t_(d)
    return (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)) * np.exp(-t * 6)


def riser(d):
    t = t_(d)
    n = rng.standard_normal(len(t))
    n = n - lowpass(n, 500)
    return n * (t / d) ** 2 * 0.6


m = lambda midi: 440 * 2 ** ((midi - 69) / 12)
# Am - F - C - G, two bars each
chords = [([57, 60, 64], 45), ([53, 57, 60], 41), ([48, 52, 55], 36), ([55, 59, 62], 43)]
bar = 4 * beat
CH = 2 * bar

# Strong opening hit, then a riser into a second hit as the title card ends.
add(boom(), 0.0, 0.9)
add(kick(), 0.0, 1.0)
add(riser(3.2), 0.6, 0.5)
add(boom(3.0), 4.0, 0.8)

for i in range(int((DUR - 0.5) / CH) + 1):
    notes, bass = chords[i % 4]
    t0 = i * CH
    add(pad([m(x) for x in notes], CH + 0.4), t0, 0.35)
    bass_sig = np.sin(2 * np.pi * m(bass - 12) * t_(CH)) * np.minimum(t_(CH) / 0.05, 1) * 0.5
    add(bass_sig, t0, 0.6)

# Drive: four-on-the-floor from 4s, hats, plucked arpeggio.
for b in range(int(DUR / beat)):
    t = b * beat
    if t >= 4.0:
        add(kick(), t, 0.8)
        add(hat(), t + beat / 2, 0.5, pan=0.3)
    if t >= 8.0:
        notes, _ = chords[int(t // CH) % 4]
        for k in range(2):
            add(pluck(m(notes[(b * 2 + k) % 3] + 12)), t + k * beat / 2, 0.22, pan=-0.3 if k else 0.3)

# Closing hit with the end card.
add(boom(3.0), 38.0, 0.7)

# Master: gentle fade in/out, normalise.
t = np.arange(N) / SR
out *= np.minimum(t / 0.02, 1)[:, None] * np.clip((DUR - t) / 2.5, 0, 1)[:, None]
out = np.tanh(out / np.abs(out).max() * 1.6) * 0.85

wav = "/tmp/promo-bed.wav" if len(sys.argv) < 3 else sys.argv[2]
with wave.open(wav, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype("<i2").tobytes())
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-b:a", "160k", sys.argv[1]], check=True)
