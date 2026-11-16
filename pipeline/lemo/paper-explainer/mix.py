# voice (ElevenLabs take, already in the repo) + synth bed from the reel pipeline + paper foley on every page change
import json, subprocess, sys, numpy as np, soundfile as sf
sys.path.insert(0, '/tmp/claude-0/-home-claude/882fcc5a-7a1f-5257-bf9f-907519f21b27/scratchpad/rm/pipeline/v10'); sys.path.insert(0, '/root/lemo-opuscar/core/audio')
import sfx
from sfx import SR, add, whoosh, thump
P = '/tmp/claude-0/-home-claude/882fcc5a-7a1f-5257-bf9f-907519f21b27/scratchpad/paper-explainer-test'; W = json.load(open(P + '/words.json')); S = json.load(open(P + '/spec.json'))
T = lambda i: W['lead'] + W['t'][i]; dur = W['lead'] + W['end'] + 3.4
starts = [0.0] + [T(s['w']) - .05 for s in S['scenes'][1:]]
from build9 import bed
bed(starts, dur, P + '/out/bed.wav', {"keyword": S['keyword']}, [{"type": "grid"}] * (len(starts) - 1) + [{"type": "cta"}])
b, sr = sf.read(P + '/out/bed.wav', always_2d=True)
if sr != SR:
    import soxr; b = soxr.resample(b, sr, SR)
v = subprocess.run(['/root/ff7/ffmpeg', '-v', 'error', '-i', '/tmp/claude-0/-home-claude/882fcc5a-7a1f-5257-bf9f-907519f21b27/scratchpad/rm/media/' + sys.argv[1] + '.mp3', '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout
v = np.frombuffer(v, np.float32)
n = int(dur * SR); buf = np.zeros((n, 2), np.float32)
L = min(len(b), n); buf[:L] += b[:L] * .55
for a in starts[1:]: add(buf, whoosh(.45, .5), a - .3, .35); add(buf, thump(.6), a + .05, .25)
add(buf, v, W['lead'], 1.0)
buf /= max(1.0, np.abs(buf).max() / .95)
sf.write(P + '/out/mix.wav', buf, SR, subtype='FLOAT'); print('mix', round(dur, 2))
