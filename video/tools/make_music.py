"""Synthesise an original 45s warm, African-percussion promo bed (no samples,
no licensing): djembe/conga patterns, shekere shaker, kalimba melody, soft pad.

Usage: python3 video/tools/make_music.py static/audio/promo-bed.mp3
"""
import subprocess, sys, wave
import numpy as np

SR, DUR, BPM = 44100, 45.0, 104
N = int(SR * DUR)
beat = 60 / BPM
step = beat / 4  # 16th note
rng = np.random.default_rng(11)
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


def lowpass(x, k):
    a = np.exp(-2 * np.pi * k / SR)
    y = np.zeros_like(x)
    acc = 0.0
    for n in range(len(x)):
        acc = a * acc + (1 - a) * x[n]
        y[n] = acc
    return y


def drum(f0, f1, decay, d, click=0.15, click_cut=3000):
    """Membrane drum: pitch-dropping sine plus a short filtered noise strike."""
    t = t_(d)
    f = f1 + (f0 - f1) * np.exp(-t * 40)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * decay)
    n = rng.standard_normal(len(t))
    n = lowpass(n, click_cut) * np.exp(-t * 90) * click * 4
    return body + n


def djembe_bass():
    return drum(150, 62, 9, 0.5)


def djembe_tone():
    return drum(320, 210, 16, 0.3, click=0.2, click_cut=4000)


def djembe_slap():
    t = t_(0.18)
    n = rng.standard_normal(len(t))
    n = n - lowpass(n, 1800)
    return (n * np.exp(-t * 38) * 0.9 + np.sin(2 * np.pi * 420 * t) * np.exp(-t * 30) * 0.3)


def conga(f=250):
    return drum(f * 1.3, f, 20, 0.28, click=0.1, click_cut=2500)


def shaker(accent=1.0):
    t = t_(0.09)
    n = rng.standard_normal(len(t))
    n = n - lowpass(n, 5000)
    return n * np.minimum(t / 0.008, 1) * np.exp(-t * 45) * 0.35 * accent


def taiko(d=3.8):
    """Big ensemble hit: deep drum + warm noise bloom, used for the intro and end."""
    t = t_(d)
    f = 48 + 90 * np.exp(-t * 18)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.4)
    n = lowpass(rng.standard_normal(len(t)), 1200) * np.exp(-t * 3.0) * 1.2
    mid = drum(180, 90, 6, d, click=0.3) * 0.7
    return sub * 1.3 + n * 0.5 + mid


def kalimba(f, d=1.4):
    t = t_(d)
    s = (np.sin(2 * np.pi * f * t) * np.exp(-t * 3.2)
         + 0.35 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 14)
         + 0.15 * np.sin(2 * np.pi * f * 2.0 * t) * np.exp(-t * 5))
    return s * np.minimum(t / 0.004, 1)


def pad(freqs, d):
    t = t_(d)
    s = np.zeros_like(t)
    for f in freqs:
        for det in (-0.003, 0, 0.003):
            s += np.sin(2 * np.pi * f * (1 + det) * t) + 0.25 * np.sin(4 * np.pi * f * (1 + det) * t)
    env = np.minimum(t / 1.2, 1) * np.minimum((d - t) / 1.2, 1)
    return s / (len(freqs) * 3) * env


def riser(d):
    t = t_(d)
    n = lowpass(rng.standard_normal(len(t)), 2500)
    n = n - lowpass(n, 300)
    return n * (t / d) ** 2 * 0.9


m = lambda midi: 440 * 2 ** ((midi - 69) / 12)
# Am - F - C - G (warm, open), two bars each
chords = [([57, 60, 64], 45), ([53, 57, 60], 41), ([48, 52, 55], 36), ([55, 59, 62], 43)]
bar = 4 * beat
CH = 2 * bar
penta = [69, 72, 74, 76, 79, 81, 84]  # A minor pentatonic-ish for the kalimba

# Strong intro: ensemble hit, building riser and rolling drums, second hit at 4s.
add(taiko(), 0.0, 1.0)
add(riser(3.3), 0.6, 0.45)
for k in range(8):  # drum roll into the title change
    add(conga(230 + 12 * (k % 3)), 2.2 + k * step * 1.5, 0.35 + 0.05 * k, pan=-0.3 if k % 2 else 0.3)
add(taiko(3.2), 4.0, 0.85)

# Pad + soft bass (warm, no hard sub)
for i in range(int((DUR - 0.5) / CH) + 1):
    notes, bass = chords[i % 4]
    t0 = i * CH
    add(pad([m(x) for x in notes], CH + 0.6), t0, 0.32)
    bt = t_(CH)
    add(np.sin(2 * np.pi * m(bass - 12) * bt) * np.minimum(bt / 0.04, 1) * np.minimum((CH - bt) / 0.2, 1), t0, 0.35)

# Percussion groove from 4s: djembe bass/tone/slap, congas, shekere 16ths.
bar_idx = 0
t = 0.0
while t < DUR - 0.1:
    if t >= 4.0 - 1e-6:
        s = int(round((t - 4.0) / step)) % 16  # 16th-note step within the bar
        if s in (0, 6, 10):
            add(djembe_bass(), t, 0.75 if s == 0 else 0.55)
        if s in (4, 12):
            add(djembe_tone(), t, 0.4, pan=0.2)
        if s in (7, 15):
            add(djembe_slap(), t, 0.3, pan=-0.2)
        if t >= 8.0 and s in (2, 3, 8, 11, 14):
            add(conga(250 if s % 2 else 190), t, 0.3, pan=-0.35)
        add(shaker(1.4 if s % 4 == 2 else 0.7), t, 0.6, pan=0.4 if s % 2 else -0.4)
    t += step

# Kalimba melody from 8s: gentle pentatonic phrase over each chord, with an echo.
phrase = [0, 2, 4, 2, 3, 1, 2, 0]
t = 8.0
n = 0
while t < 38.0:
    idx = phrase[n % len(phrase)] + (n // 16 % 2)
    f = m(penta[idx % len(penta)])
    sig = kalimba(f)
    add(sig, t, 0.22, pan=-0.25)
    add(sig, t + step * 3, 0.1, pan=0.35)  # echo
    t += beat / 2 * (1 if n % 8 != 7 else 2)
    n += 1

# Closing: ensemble hit + chord swell with the end card.
add(taiko(3.2), 38.0, 0.8)
add(pad([m(x) for x in (57, 60, 64, 69)], 6.5), 38.0, 0.35)

tt = np.arange(N) / SR
out *= np.minimum(tt / 0.01, 1)[:, None] * np.clip((DUR - tt) / 2.5, 0, 1)[:, None]
out = np.tanh(out / np.abs(out).max() * 1.5) * 0.85

wav = "/tmp/promo-bed.wav" if len(sys.argv) < 3 else sys.argv[2]
with wave.open(wav, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype("<i2").tobytes())
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-b:a", "160k", sys.argv[1]], check=True)
