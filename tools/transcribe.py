"""Transcribe the voiceovers listed in transcribe.txt with Whisper so pronunciation can be checked as text."""
import os, sys
from faster_whisper import WhisperModel
m = WhisperModel("large-v3", device="cpu", compute_type="int8")
os.makedirs("transcripts", exist_ok=True)
for name in open("transcribe.txt").read().split():
    segs, _ = m.transcribe(os.path.join("media", name), language="fa", beam_size=5, word_timestamps=True, vad_filter=False,
                           condition_on_previous_text=False)
    out = []
    for s in segs:
        out.append(f"[{s.start:.2f}-{s.end:.2f}] {s.text.strip()}")
        out.append("   " + " ".join(f"{w.word.strip()}({w.probability:.2f})" for w in s.words))
    open(os.path.join("transcripts", name + ".txt"), "w").write("\n".join(out) + "\n")
    print(name, "ok", flush=True)
