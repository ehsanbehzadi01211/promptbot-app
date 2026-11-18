"""Transcribe the voiceovers listed in transcribe.txt with Whisper so pronunciation can be checked as text.
Files starting with "en" are transcribed as English, everything else as Persian. Word timings go to <name>.json."""
import json, os
from faster_whisper import WhisperModel
m = WhisperModel("large-v3", device="cpu", compute_type="int8")
os.makedirs("transcripts", exist_ok=True)
for name in open("transcribe.txt").read().split():
    lang = "en" if name.startswith("en") else "fa"
    segs, _ = m.transcribe(os.path.join("media", name), language=lang, beam_size=5, word_timestamps=True, vad_filter=False,
                           condition_on_previous_text=False)
    out, words = [], []
    for s in segs:
        out.append(f"[{s.start:.2f}-{s.end:.2f}] {s.text.strip()}")
        out.append("   " + " ".join(f"{w.word.strip()}({w.probability:.2f})" for w in s.words))
        words += [[w.word.strip(), round(w.start, 2), round(w.end, 2), round(w.probability, 2)] for w in s.words]
    open(os.path.join("transcripts", name + ".txt"), "w").write("\n".join(out) + "\n")
    json.dump(words, open(os.path.join("transcripts", name + ".json"), "w"))
    print(name, "ok", flush=True)
