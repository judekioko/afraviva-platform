"""Original score for Act II (no samples, no licensing). It follows the delivery
cues in the narration timeline: warm -> serious, restrained -> rising -> majestic,
with a synthesised choir entering at "At Fatima... triumph".

Usage: python3 video/tools/make_act2_music.py video/src/act2-timeline.json static/audio/act2-music.mp3
"""
import json, subprocess, sys, wave
import numpy as np

tl = json.load(open(sys.argv[1]))
SR, DUR = 44100, tl["durationSec"]
N = int(SR * DUR)
BPM = 72
beat = 60 / BPM
bar = 4 * beat
rng = np.random.default_rng(5)
out = np.zeros((N, 2))
sec = {s["mode"]: s["startSec"] for s in tl["sections"]}
T_SERIOUS, T_RISING, T_MAJ = sec["serious"], sec["rising"], sec["majestic"]
T_VOICE_END = tl["voiceEndSec"]


def add(sig, t0, gain=1.0, pan=0.0):
    i = int(t0 * SR)
    if i >= N or len(sig) == 0:
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


def drum(f0, f1, decay, d, click=0.1, click_cut=1500):
    t = t_(d)
    f = f1 + (f0 - f1) * np.exp(-t * 35)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * decay)
    n = lowpass(rng.standard_normal(len(t)), click_cut) * np.exp(-t * 80) * click * 4
    return body + n


def timpani(d=3.0):
    t = t_(d)
    f = 70 + 40 * np.exp(-t * 14)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.6) + 0.4 * drum(110, 70, 5, d, 0.2)) * 1.1


def djembe_bass():
    return drum(150, 62, 9, 0.5, 0.15, 3000)


def djembe_slap():
    t = t_(0.18)
    n = rng.standard_normal(len(t))
    n = n - lowpass(n, 1800)
    return n * np.exp(-t * 38) * 0.8


def kalimba(f, d=1.6):
    t = t_(d)
    s = (np.sin(2 * np.pi * f * t) * np.exp(-t * 3.0)
         + 0.3 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 14)
         + 0.15 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 5))
    return s * np.minimum(t / 0.004, 1)


def pad(freqs, d, bright=0.25):
    t = t_(d)
    s = np.zeros_like(t)
    for f in freqs:
        for det in (-0.003, 0, 0.003):
            s += np.sin(2 * np.pi * f * (1 + det) * t) + bright * np.sin(4 * np.pi * f * (1 + det) * t)
    env = np.minimum(t / 1.6, 1) * np.minimum((d - t) / 1.6, 1)
    return s / (len(freqs) * 3) * env


FORMANTS = [(800, 110, 1.0), (1150, 130, 0.6), (2900, 220, 0.25)]  # "ah"


def choir(f, d, swell=2.5):
    """Additive 'ah' voice: harmonics shaped by formant peaks, vibrato, light breath."""
    t = t_(d)
    s = np.zeros_like(t)
    vib = 0.012 * np.sin(2 * np.pi * 5.2 * t + rng.uniform(0, 6))
    for kk in range(1, 28):
        fk = f * kk
        if fk > 5000:
            break
        amp = sum(g * np.exp(-(((fk - F) / bw) ** 2)) for F, bw, g in FORMANTS) / kk ** 0.5
        if amp > 1e-3:
            s += amp * np.sin(2 * np.pi * fk * t + kk * vib * 4)
    breath = (rng.standard_normal(len(t)) - lowpass(rng.standard_normal(len(t)), 2500)) * 0.02
    env = np.minimum(t / swell, 1) ** 1.5 * np.minimum((d - t) / 2.0, 1)
    return (s + breath) * env * 0.12


m = lambda x: 440 * 2 ** ((x - 69) / 12)
# chords as MIDI note lists (bass note first)
WARM = [[45, 57, 60, 64], [41, 53, 57, 60], [48, 55, 60, 64], [43, 55, 59, 62]]       # Am F C G
SERIOUS = [[38, 50, 53, 57], [45, 52, 57, 60], [41, 48, 53, 57], [40, 52, 55, 59]]     # Dm Am F Em, low
RISING = [[45, 57, 60, 64], [41, 53, 57, 60], [48, 55, 60, 64], [43, 55, 59, 62]]
MAJ = [[48, 55, 60, 64, 67], [43, 55, 59, 62, 67], [45, 57, 60, 64, 69], [41, 53, 57, 60, 65]]  # C G Am F


def mode_at(t):
    return "majestic" if t >= T_MAJ else "rising" if t >= T_RISING else "serious" if t >= T_SERIOUS else "warm"


def ramp(t, a, b):
    return float(np.clip((t - a) / (b - a), 0, 1))


CH = 2 * bar  # a chord lasts two bars
nch = int(np.ceil(DUR / CH))
for i in range(nch):
    t0 = i * CH
    mode = mode_at(t0)
    chords = {"warm": WARM, "serious": SERIOUS, "rising": RISING, "majestic": MAJ}[mode]
    notes = chords[(i % 4)]
    if mode == "warm":
        g = 0.28 + 0.1 * ramp(t0, 2.5, T_SERIOUS)
    elif mode == "serious":
        g = 0.2
    elif mode == "rising":
        g = 0.28 + 0.3 * ramp(t0, T_RISING, T_MAJ)
    else:
        g = 0.55
    add(pad([m(x) for x in notes[1:]], CH + 1.6, bright=0.35 if mode == "majestic" else 0.2), t0, g)
    bt = t_(CH)
    add(np.sin(2 * np.pi * m(notes[0]) * bt) * np.minimum(bt / 0.05, 1) * np.minimum((CH - bt) / 0.3, 1), t0, 0.32 if mode != "serious" else 0.4)

# WARM: gentle kalimba figure, sparse
t = 3.0
pent = [69, 72, 74, 76, 79]
n = 0
while t < T_SERIOUS - 1:
    add(kalimba(m(pent[[0, 2, 4, 2, 3, 1][n % 6]])), t, 0.14, pan=-0.3 if n % 2 else 0.3)
    t += beat * (1 if n % 6 != 5 else 2)
    n += 1

# SERIOUS: restrained heartbeat (two soft low thumps every two beats), no melody
t = T_SERIOUS + 1
while t < T_RISING - 1:
    add(drum(90, 48, 7, 0.9, 0.03, 600), t, 0.42)
    add(drum(85, 46, 8, 0.8, 0.03, 600), t + 0.28, 0.3)
    t += beat * 2
    
# RISING: kalimba arpeggio returns and percussion builds with the section
t = T_RISING
step = beat / 2
k = 0
while t < T_MAJ:
    r = ramp(t, T_RISING, T_MAJ)
    notes = RISING[int((t // CH) % 4)]
    add(kalimba(m(notes[1 + k % 3] + 12)), t, 0.1 + 0.14 * r, pan=0.3 if k % 2 else -0.3)
    if k % 4 == 0:
        add(djembe_bass(), t, 0.3 + 0.4 * r)
    if k % 8 == 6 and r > 0.25:
        add(djembe_slap(), t, 0.25 * r)
    t += step
    k += 1
# drum roll into the majestic section
for j in range(10):
    add(drum(150 - j, 90, 12, 0.3, 0.1, 2000), T_MAJ - 1.8 + j * 0.18, 0.15 + 0.05 * j)

# MAJESTIC: timpani on every bar, steady djembe, choir on the chords
add(timpani(4.0), T_MAJ - 0.05, 0.9)
t = T_MAJ
k = 0
while t < T_VOICE_END:
    if k % 8 == 0:
        add(timpani(2.5), t, 0.55)
    if k % 2 == 0:
        add(djembe_bass(), t, 0.4)
    if k % 8 == 6:
        add(djembe_slap(), t, 0.25)
    notes = MAJ[int((t // CH) % 4)]
    if k % 2 == 1:
        add(kalimba(m(notes[2] + 12)), t, 0.14, pan=0.3 if k % 4 == 1 else -0.3)
    t += step
    k += 1

# Choir: SATB-ish stack on each chord from the "triumph" line; final chord rings out.
ci = 0
t = T_MAJ
while t < DUR - 2:
    d = min(CH + 1.0, DUR - t)
    notes = MAJ[ci % 4]
    for j, nn in enumerate(notes[1:]):
        for octave in (0, 12):
            add(choir(m(nn + octave), d), t, 0.7 if octave == 0 else 0.4, pan=(-0.4, 0.4, -0.2, 0.2)[j % 4])
    t += CH
    ci += 1
add(timpani(5.0), T_VOICE_END + 0.3, 0.8)

# Master: fade in/out, soft limiting
tt = np.arange(N) / SR
out *= np.minimum(tt / 1.5, 1)[:, None] * np.clip((DUR - tt) / 3.5, 0, 1)[:, None]
out = np.tanh(out / np.abs(out).max() * 1.2) * 0.9
wav = "/tmp/act2-music.wav"
with wave.open(wav, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype("<i2").tobytes())
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-b:a", "160k", sys.argv[2]], check=True)
