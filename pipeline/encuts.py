"""Scene cut times for an English voiceover from Whisper word timings.
python3 encuts.py key [key...]  -> writes "cuts" into scripts_en.json"""
import difflib, json, re, sys

T = "/home/claude/reels-media/transcripts/{}.mp3.json"
NUM = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "10": "ten", "15": "fifteen", "30": "thirty"}

def toks(s):
    out = []
    for w in re.findall(r"[a-z0-9']+", s.lower().replace("-", " ")):
        out.append(NUM.get(w, w))
    return out

def cuts(spec, words):
    script, starts = [], []
    for sc in spec["scenes"]:
        starts.append(len(script)); script += toks(sc["voice"])
    flat, owner = [], []
    for i, (w, a, b, p) in enumerate(words):
        for t in toks(w):
            flat.append(t); owner.append(i)
    sm = difflib.SequenceMatcher(None, script, flat, autojunk=False)
    m = {}
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            m[blk.a + k] = blk.b + k
    res = []
    for si in starts[1:]:
        j = next((m[k] for k in range(si, si + 6) if k in m), None)
        if j is None:
            raise SystemExit(f"no match near script word {si}: {script[si:si+5]}")
        wi = owner[j]
        prev_end = words[wi - 1][2] if wi else words[wi][1]
        res.append(round((prev_end + words[wi][1]) / 2, 2))
    return res

if __name__ == "__main__":
    d = json.load(open("/home/claude/reels/scripts_en.json"))
    for k in sys.argv[1:]:
        w = json.load(open(T.format(k)))
        d[k]["cuts"] = cuts(d[k], w)
        low = [x for x in w if x[3] < 0.6]
        print(k, d[k]["cuts"], "low-confidence:", [(x[0], x[3]) for x in low][:8])
    json.dump(d, open("/home/claude/reels/scripts_en.json", "w"), ensure_ascii=False, indent=1)
