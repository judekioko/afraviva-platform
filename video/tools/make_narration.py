"""Voice the script in video/script/*.txt with Kokoro (open-source, Apache-2.0).

Each sentence is synthesised separately so the video gets exact timings.
Writes the voice-over mp3 and a timeline JSON used by the Remotion composition.

Setup:  pip install kokoro-onnx soundfile numpy ; model files as in make_voice.py
Usage:  python3 video/tools/make_narration.py <model_dir> video/script/act2.txt \
            static/audio/act2-voice.mp3 video/src/act2-timeline.json
"""
import json, re, subprocess, sys
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

model_dir, script_path, mp3_path, json_path = sys.argv[1:5]
SR = 24000
VOICE = "bm_george"
SPEED = {"warm": 0.95, "serious": 0.9, "rising": 0.95, "majestic": 0.9}
PAUSE_SENTENCE, PAUSE_PARAGRAPH, PAUSE_MODE = 0.35, 0.9, 1.6
LEAD_IN, TAIL = 2.5, 5.0

k = Kokoro(f"{model_dir}/kokoro-v1.0.onnx", f"{model_dir}/voices-v1.0.bin")

# Parse: @mode switches, blank line = paragraph break, each line split into sentences.
items, mode, new_par = [], "warm", False
for raw in open(script_path, encoding="utf-8"):
    line = raw.strip()
    if line.startswith("#"):
        continue
    if line.startswith("@"):
        mode, new_par = line[1:], True
        items.append({"mode_change": mode})
        continue
    if not line:
        new_par = True
        continue
    for sent in re.split(r"(?<=[.!?])\s+", line):
        items.append({"text": sent, "mode": mode, "par": new_par})
        new_par = False

chunks, timeline, t = [], [], LEAD_IN
chunks.append(np.zeros(int(LEAD_IN * SR), dtype=np.float32))
sections = []
for it in items:
    if "mode_change" in it:
        sections.append({"mode": it["mode_change"], "startSec": round(t, 2)})
        continue
    if it["par"] and timeline:
        gap = PAUSE_MODE if sections and sections[-1]["startSec"] == round(t, 2) else PAUSE_PARAGRAPH
    else:
        gap = PAUSE_SENTENCE if timeline else 0
    if gap:
        chunks.append(np.zeros(int(gap * SR), dtype=np.float32)); t += gap
        if sections and sections[-1]["startSec"] < t and not [x for x in timeline if x["startSec"] >= sections[-1]["startSec"]]:
            sections[-1]["startSec"] = round(t, 2)
    # "YES" is spoken as a word, not spelled out.
    spoken = it["text"].replace("YESes", "yeses").replace("YES", "yes")
    samples, sr = k.create(spoken, voice=VOICE, speed=SPEED[it["mode"]], lang="en-gb")
    dur = len(samples) / sr
    timeline.append({"text": it["text"], "mode": it["mode"], "startSec": round(t, 2), "endSec": round(t + dur, 2), "paragraphStart": bool(it["par"])})
    chunks.append(samples.astype(np.float32)); t += dur
    print(f"{t - dur:6.1f}s {dur:4.1f}s {it['mode']:8s} {it['text'][:60]}")

total = t + TAIL
chunks.append(np.zeros(int(TAIL * SR), dtype=np.float32))
track = np.concatenate(chunks)
track *= 0.95 / max(np.abs(track).max(), 1e-6)
sf.write("/tmp/narration.wav", track, SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "/tmp/narration.wav", "-ar", "44100", "-ac", "2", "-b:a", "160k", mp3_path], check=True)
json.dump({"durationSec": round(total, 2), "voiceEndSec": round(t, 2), "sections": sections, "lines": timeline}, open(json_path, "w"), indent=1)
print("total", round(total, 1), "s", sections)
