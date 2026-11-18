# generic mix: voice (repo media) at lead + synth bed + whoosh/thump at given cue times
import json, subprocess, sys, numpy as np, soundfile as sf
sys.path.insert(0, '/tmp/claude-0/-home-claude/882fcc5a-7a1f-5257-bf9f-907519f21b27/scratchpad/rm/pipeline/v10'); sys.path.insert(0, '/root/lemo-opuscar/core/audio')
from sfx import SR, add, whoosh, thump, click
from build9 import bed
P, voice, kw = sys.argv[1], sys.argv[2], sys.argv[3]; cues = [float(x) for x in sys.argv[4].split(',')]; style = sys.argv[5] if len(sys.argv) > 5 else 'paper'
W = json.load(open(P + '/words.json')); dur = float(sys.argv[6]) if len(sys.argv) > 6 else W['lead'] + W['end'] + 3.3
starts = [0.0] + cues
bed(starts, dur, P + '/out/bed.wav', {"keyword": kw}, [{"type": "grid"}] * (len(starts) - 1) + [{"type": "cta"}])
b, sr = sf.read(P + '/out/bed.wav', always_2d=True)
if sr != SR:
    import soxr; b = soxr.resample(b, sr, SR)
v = np.frombuffer(subprocess.run(['/root/ff7/ffmpeg', '-v', 'error', '-i', '/tmp/claude-0/-home-claude/882fcc5a-7a1f-5257-bf9f-907519f21b27/scratchpad/rm/media/' + voice + '.mp3', '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout, np.float32)
n = int(dur * SR); buf = np.zeros((n, 2), np.float32); L = min(len(b), n); buf[:L] += b[:L] * .5
for a in cues:
    if style == 'swiss': add(buf, click(.8, .7), a, .35); add(buf, thump(.5, 90), a, .2)
    else: add(buf, whoosh(.4, .45), a - .25, .3)
add(buf, v, W['lead'], 1.0)
buf /= max(1.0, np.abs(buf).max() / .95); sf.write(P + '/out/mix.wav', buf, SR, subtype='FLOAT'); print('mix', round(dur, 2))
