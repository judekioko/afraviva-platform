"""Generate the promo voice-over with Kokoro (open-source, Apache-2.0) and time
each line into its scene slot.

Setup:  pip install kokoro-onnx soundfile numpy
        download kokoro-v1.0.onnx and voices-v1.0.bin from
        https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0
Usage:  python3 video/tools/make_voice.py <model_dir> static/audio/promo-voice.mp3
"""
import subprocess, sys
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

VOICE = "bm_george"
DUR, SR = 45.0, 24000
# (start sec, latest end sec, line)
LINES = [
    (0.9, 3.8, "AfraViva Media. Your partner for life."),
    (4.2, 7.0, "Good morning, Africa! Come behind the scenes with us."),
    (7.2, 11.9, "High-quality video and audio for TV, web and social media. We are ready when you are."),
    (12.3, 18.8, "Ask honestly, listen well, and let Africa speak for itself."),
    (19.3, 25.8, "Editing, colour grading and post-production. Hours of raw footage, shaped into something that inspires."),
    (26.3, 32.8, "Digital marketing, social media and media training, so your message lands with clarity and impact."),
    (33.3, 37.8, "Proud to partner with Veni Foras, The Letter House, LifeSite, and Pro Vita and Famiglia."),
    (38.4, 44.2, "We tell Africa's story. With truth, beauty and purpose. AfraViva Media. Your partner for life."),
]

model_dir, out_path = sys.argv[1], sys.argv[2]
k = Kokoro(f"{model_dir}/kokoro-v1.0.onnx", f"{model_dir}/voices-v1.0.bin")
track = np.zeros(int(DUR * SR), dtype=np.float32)
for start, end, text in LINES:
    slot = end - start
    samples, sr = k.create(text, voice=VOICE, speed=1.0, lang="en-gb")
    assert sr == SR
    speed = min(max(len(samples) / SR / slot, 1.0), 1.3)
    if speed > 1.0:
        samples, _ = k.create(text, voice=VOICE, speed=speed, lang="en-gb")
    got = len(samples) / SR
    print(f"{start:5.1f}s  {got:4.1f}s / {slot:3.1f}s  speed {speed:.2f}  {text[:40]}")
    i = int(start * SR)
    seg = samples[: len(track) - i]
    fade = int(0.03 * SR)
    seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
    track[i : i + len(seg)] += seg
track /= max(np.abs(track).max(), 1e-6) / 0.95
sf.write("/tmp/voice.wav", track, SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "/tmp/voice.wav", "-ar", "44100", "-ac", "2", "-b:a", "160k", out_path], check=True)
