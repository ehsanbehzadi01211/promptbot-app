"""Find scene boundaries in a single voiceover file: pick N-1 pauses that best match
character-proportional sentence positions, favouring longer pauses."""
import subprocess, sys, json, itertools
import numpy as np

def pauses(path, step=0.05, thr=250, minlen=0.15):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "8000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(raw, dtype=np.int16).astype(float)
    w = int(8000 * step)
    rms = np.array([np.sqrt((a[i:i + w] ** 2).mean()) for i in range(0, len(a) - w, w)])
    quiet = rms < thr
    dur = len(a) / 8000
    voiced = np.where(~quiet)[0]
    s0, s1 = voiced[0] * step, (voiced[-1] + 1) * step
    out, i = [], 0
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]:
                j += 1
            st, en = i * step, j * step
            if en - st >= minlen and st > s0 and en < s1:
                out.append(((st + en) / 2, en - st))
            i = j
        else:
            i += 1
    return out, s0, s1, dur

def boundaries(path, sentences):
    ps, s0, s1, dur = pauses(path)
    lens = np.array([len(s) for s in sentences], float)
    exp = s0 + (s1 - s0) * np.cumsum(lens)[:-1] / lens.sum()
    n = len(exp)
    # DP over ordered pauses
    best = {}
    INF = 1e9
    m = len(ps)
    cost = [[abs(ps[j][0] - exp[k]) - 1.5 * ps[j][1] for j in range(m)] for k in range(n)]
    dp = np.full((n, m), INF); bk = np.zeros((n, m), int)
    for j in range(m):
        dp[0][j] = cost[0][j]
    for k in range(1, n):
        for j in range(m):
            prev = dp[k - 1][:j]
            if len(prev) and prev.min() < INF:
                p = int(prev.argmin()); dp[k][j] = prev[p] + cost[k][j]; bk[k][j] = p
    j = int(dp[n - 1].argmin()); sel = [j]
    for k in range(n - 1, 0, -1):
        j = bk[k][j]; sel.append(j)
    sel = sel[::-1]
    return [ps[j][0] for j in sel], s0, s1, dur

if __name__ == "__main__":
    path, key = sys.argv[1], sys.argv[2]
    spec = json.load(open("/home/claude/reels/scripts.json"))[key]
    b, s0, s1, dur = boundaries(path, [sc["voice"] for sc in spec["scenes"]])
    print(json.dumps({"bounds": [round(x, 2) for x in b], "speech": [round(s0, 2), round(s1, 2)], "dur": round(dur, 2)}))
