import json, sys, numpy as np, soundfile as sf, soxr
ep = json.load(open(sys.argv[1])); out = sys.argv[2]; SR = 48000; T = ep['t']; D = T['dur']; N = int(D * SR) + SR
rng = np.random.default_rng(7); t = np.arange(N) / SR
def tone(f, d, a=.2, att=.01, rel=.3, kind='saw'):
    n = int(d * SR); x = np.arange(n) / SR
    w = 2 * (x * f % 1) - 1 if kind == 'saw' else np.sin(2 * np.pi * f * x)
    env = np.minimum(1, x / att) * np.exp(-x / rel); return w * env * a
def add(buf, sig, at):
    i = int(at * SR); j = min(len(buf), i + len(sig)); buf[i:j] += sig[:j - i]
bed = np.zeros(N)
# talk-show bed: 100 bpm, chords I-vi-IV-V in C, soft pluck + kick/hat
bpm = 100; beat = 60 / bpm; prog = [[60, 64, 67], [57, 60, 64], [53, 57, 60], [55, 59, 62]]
mid = lambda m: 440 * 2 ** ((m - 69) / 12)
b = 0; tt = 0.0
while tt < D:
    ch = prog[(b // 4) % 4]
    for k, m in enumerate(ch): add(bed, tone(mid(m), .5, .035, .005, .18, 'sine'), tt + k * .02); add(bed, tone(mid(m) * 2, .3, .01, .005, .1), tt + k * .02)
    if b % 4 == 0: add(bed, tone(mid(ch[0] - 24), beat * 2, .08, .01, .5, 'sine'), tt)
    kick = np.sin(2 * np.pi * (55 + 90 * np.exp(-np.arange(int(.25 * SR)) / SR * 30)) * np.arange(int(.25 * SR)) / SR) * np.exp(-np.arange(int(.25 * SR)) / SR * 12) * .22
    if b % 2 == 0: add(bed, kick, tt)
    hat = rng.standard_normal(int(.05 * SR)) * np.exp(-np.arange(int(.05 * SR)) / SR * 80) * .03
    add(bed, np.diff(hat, prepend=0), tt + beat / 2)
    tt += beat; b += 1
vo = np.zeros(N); duck = np.zeros(N)
for l in ep['lines']:
    a, sr = sf.read(l['file']); a = a.mean(1) if a.ndim > 1 else a
    if sr != SR: a = soxr.resample(a, sr, SR)
    a = a / (np.max(np.abs(a)) + 1e-9) * .9; add(vo, a, l['start']); duck[int(l['start'] * SR):int((l['start'] + l['dur']) * SR)] = 1
k = int(.25 * SR); duck = np.convolve(duck, np.ones(k) / k, 'same'); g = 1 - .72 * duck
sfx = np.zeros(N)
# intro sting: rising arpeggio + hit
for i, m in enumerate([60, 64, 67, 72, 76, 79]): add(sfx, tone(mid(m), .5, .09, .005, .25), .1 + i * .09)
hit = rng.standard_normal(int(1.2 * SR)) * np.exp(-np.arange(int(1.2 * SR)) / SR * 4) * .12; add(sfx, hit + tone(mid(48), 1.2, .25, .005, .6, 'sine'), .65)
# applause on guest entrance
e0, e1 = T['enter']; n = int((e1 - e0 + 1.2) * SR); ap = np.zeros(n)
for c in range(int((e1 - e0 + 1.2) * 70)):
    s = int(rng.uniform(0, n - 3000)); cl = rng.standard_normal(1500) * np.exp(-np.arange(1500) / 150) * rng.uniform(.1, .3); ap[s:s + 1500] += cl
env = np.minimum(1, np.arange(n) / (.3 * SR)) * np.minimum(1, (n - np.arange(n)) / (.8 * SR)); add(sfx, ap * env * .5, e0 + .1)
# whoosh into monitor + outro sting
w = rng.standard_normal(int(.7 * SR)); w = np.convolve(w, np.ones(30) / 30, 'same') * np.sin(np.linspace(0, np.pi, len(w))) * .5; add(sfx, w, T['demo'][0] - .75); add(sfx, w[::-1] * .7, T['demo'][1] - .3)
for i, m in enumerate([79, 76, 72, 67, 72]): add(sfx, tone(mid(m), .6, .08, .005, .3), T['outro'] + 1.8 + i * .1)
mix = bed * g * .9 + vo + sfx
fade = np.ones(N); fl = int(1.5 * SR); fade[-fl:] = np.linspace(1, 0, fl); mix = mix[:int(D * SR)] * fade[:int(D * SR)]
mix = mix / (np.max(np.abs(mix)) + 1e-9) * .92
sf.write(out, np.stack([mix, mix], 1), SR)
print('ok', D)
