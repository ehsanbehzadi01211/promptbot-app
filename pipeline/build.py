import json, subprocess, sys, wave, os, html
import numpy as np
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
LEAD, PAD, VOICE_OFF = 0.2, 0.35, 0.2
SR = 22050

def wav_dur(p):
    with wave.open(p) as w:
        return w.getnframes() / w.getframerate()

def tts(text, out):
    tmp = out + ".raw.wav"
    subprocess.run(["espeak-ng", "-v", "mb-ir1", "-s", "172", "-p", "45", "-w", tmp, text], check=True)
    # normalise, slight warmth, resample
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af",
                    "highpass=f=70,lowpass=f=7500,loudnorm=I=-16:TP=-1.5,aresample=%d" % SR,
                    "-ac", "1", out], check=True)
    os.remove(tmp)

def music(total, out, seed=0):
    rng = np.random.default_rng(seed)
    t = np.arange(int(total * SR)) / SR
    chords = [[220.0, 261.63, 329.63], [174.61, 220.0, 261.63], [196.0, 246.94, 293.66], [164.81, 196.0, 246.94]]
    sig = np.zeros_like(t)
    bar = 2.4
    for i, ch in enumerate(chords * 20):
        s = i * bar
        if s > total: break
        m = (t >= s) & (t < s + bar + 0.6)
        tt = t[m] - s
        env = np.minimum(tt / 0.5, 1) * np.exp(-np.maximum(tt - bar, 0) * 4)
        for f in ch:
            sig[m] += env * (np.sin(2*np.pi*f*tt) * 0.5 + np.sin(2*np.pi*f*2.003*tt) * 0.12)
        # soft kick on beats
        for b in range(4):
            kt = tt - b * bar / 4
            km = kt >= 0
            sig[m] += km * np.sin(2*np.pi*(50 + 60*np.exp(-kt*30))*kt) * np.exp(-np.maximum(kt,0)*9) * 0.9
    sig += rng.normal(0, 0.004, sig.shape)
    fade = np.minimum(1, np.minimum(t / 1.0, (total - t) / 1.5))
    sig = sig / np.max(np.abs(sig)) * 0.9 * fade
    with wave.open(out, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((sig * 32767).astype(np.int16).tobytes())

def esc(s):
    return html.escape(s).replace("\n", "<br>")

def scene_html(sc, start, dur, accent):
    def d(off):  # absolute delay for an inner element
        return f"animation-delay:{start+off:.3f}s"
    life = f"animation: life {dur:.3f}s linear {start:.3f}s both"
    t = sc["type"]
    inner = ""
    if t in ("hook", "cta"):
        inner = f'<div class="title big in" style="{d(0.05)}">{esc(sc["title"])}</div>'
        if sc.get("sub"):
            inner += f'<div class="sub in" style="{d(0.45)}">{esc(sc["sub"])}</div>'
        if t == "cta":
            inner = f'<div class="ctaicon in" style="{d(0)}"><svg viewBox="0 0 24 24"><path d="M4 4h16v12H7l-3 3z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg></div>' + inner
    elif t == "chips":
        inner = f'<div class="title in" style="{d(0.05)}">{esc(sc["title"])}</div><div class="chips">'
        for i, it in enumerate(sc["items"]):
            inner += f'<span class="chip in" style="{d(0.35+i*0.18)}" dir="ltr">{esc(it)}<i class="strike" style="{d(1.3+i*0.12)}"></i></span>'
        inner += "</div>"
    elif t == "brand":
        inner = (f'<div class="logo in" style="{d(0.0)}" dir="ltr">{esc(sc["title"])}</div>'
                 f'<div class="star in" style="{d(0.5)}"><svg viewBox="0 0 24 24"><path d="M12 2l3 6.5 7 .8-5.2 4.8 1.5 7L12 17.6 5.7 21.1l1.5-7L2 9.3l7-.8z" fill="currentColor"/></svg>{esc(sc["sub"])}</div>')
    elif t == "steps":
        inner = f'<div class="title in" style="{d(0.05)}">{esc(sc["title"])}</div><div class="steps">'
        n = len(sc["items"])
        gap = max(0.5, (dur - 1.2) / n)
        for i, it in enumerate(sc["items"]):
            inner += f'<div class="step in" style="{d(0.4+i*gap)}"><b>{"۱۲۳۴۵۶"[i]}</b>{esc(it)}</div>'
        inner += "</div>"
    elif t == "terminal":
        inner = f'<div class="title in" style="{d(0.05)}">{esc(sc["title"])}</div><div class="term in" style="{d(0.2)}" dir="ltr"><div class="dots"><i></i><i></i><i></i></div>'
        n = len(sc["items"])
        gap = max(0.6, (dur - 1.2) / n)
        for i, it in enumerate(sc["items"]):
            cls = "cl" if it.startswith("claude") else ""
            inner += f'<div class="line in {cls}" style="{d(0.5+i*gap)}">{esc(it)}</div>'
        inner += "</div>"
    elif t == "point":
        inner = (f'<div class="num in" style="{d(0.0)}">{esc(sc["num"])}</div>'
                 f'<div class="title in" style="{d(0.2)}">{esc(sc["title"])}</div>'
                 f'<div class="sub in" style="{d(0.55)}">{esc(sc["sub"])}</div>')
    return f'<section class="scene {t}" style="{life}">{inner}</section>'

CSS = """
@font-face{font-family:V;src:url(node_modules/@fontsource/vazirmatn/files/vazirmatn-arabic-400-normal.woff2);font-weight:400}
@font-face{font-family:V;src:url(node_modules/@fontsource/vazirmatn/files/vazirmatn-arabic-700-normal.woff2);font-weight:700}
@font-face{font-family:V;src:url(node_modules/@fontsource/vazirmatn/files/vazirmatn-arabic-900-normal.woff2);font-weight:900}
@font-face{font-family:V;src:url(node_modules/@fontsource/vazirmatn/files/vazirmatn-latin-400-normal.woff2);font-weight:400;unicode-range:U+0000-00FF}
@font-face{font-family:V;src:url(node_modules/@fontsource/vazirmatn/files/vazirmatn-latin-700-normal.woff2);font-weight:700;unicode-range:U+0000-00FF}
@font-face{font-family:V;src:url(node_modules/@fontsource/vazirmatn/files/vazirmatn-latin-900-normal.woff2);font-weight:900;unicode-range:U+0000-00FF}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#0b0d14;font-family:V,sans-serif;color:#f4f5f8}
.bg{position:absolute;inset:0;overflow:hidden}
.blob{position:absolute;width:1400px;height:1400px;border-radius:50%;opacity:.55;background:radial-gradient(circle,var(--c) 0%,transparent 65%)}
.b1{--c:var(--a);top:-250px;right:-300px;animation:drift1 14s ease-in-out 0s infinite alternate}
.b2{--c:#6a3cff;bottom:-300px;left:-350px;opacity:.35;animation:drift2 17s ease-in-out 0s infinite alternate}
@keyframes drift1{to{transform:translate(-260px,420px) scale(1.2)}}
@keyframes drift2{to{transform:translate(300px,-380px) scale(1.15)}}
.grain{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(255,255,255,.018) 0 2px,transparent 2px 4px)}
.tag{position:absolute;top:150px;right:80px;padding:14px 30px;border-radius:40px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);font-size:36px;font-weight:700}
.tag::before{content:"";display:inline-block;width:16px;height:16px;border-radius:50%;background:var(--a);margin-left:14px;vertical-align:middle}
.bar{position:absolute;left:80px;right:80px;bottom:150px;height:8px;border-radius:8px;background:rgba(255,255,255,.12);overflow:hidden}
.bar i{display:block;height:100%;width:100%;background:var(--a);transform-origin:right;animation:prog var(--T) linear 0s both}
@keyframes prog{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.scene{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:0 90px;direction:rtl}
@keyframes life{0%{opacity:0}4%{opacity:1}94%{opacity:1}100%{opacity:0}}
.in{animation:rise .6s cubic-bezier(.2,.8,.2,1) both}
@keyframes rise{from{opacity:0;transform:translateY(60px)}to{opacity:1;transform:none}}
.title{font-size:84px;font-weight:900;line-height:1.35}
.title.big{font-size:112px;line-height:1.3}
.sub{margin-top:44px;font-size:52px;font-weight:700;color:var(--a);line-height:1.5}
.chips{margin-top:80px;display:flex;flex-wrap:wrap;justify-content:center;gap:28px}
.chip{position:relative;font-size:50px;font-weight:700;padding:22px 40px;border-radius:24px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.15)}
.strike{position:absolute;left:18px;right:18px;top:50%;height:7px;border-radius:4px;background:#ff4d5e;transform-origin:left;animation:strike .35s ease-out both}
@keyframes strike{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.logo{font-size:128px;font-weight:900;letter-spacing:-2px;background:linear-gradient(90deg,#fff,var(--a));-webkit-background-clip:text;color:transparent}
.star{margin-top:50px;display:flex;align-items:center;gap:20px;font-size:52px;font-weight:700;padding:24px 44px;border-radius:30px;border:2px solid #f5c542;color:#f5c542;background:rgba(245,197,66,.08)}
.star svg{width:56px;height:56px}
.steps{margin-top:70px;display:flex;flex-direction:column;gap:30px;width:100%}
.step{display:flex;align-items:center;gap:36px;font-size:62px;font-weight:700;padding:30px 44px;border-radius:30px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14)}
.step b{display:grid;place-items:center;width:92px;height:92px;border-radius:50%;background:var(--a);color:#0b0d14;font-size:54px;flex:none}
.term{margin-top:70px;width:100%;text-align:left;background:#05060a;border:1px solid rgba(255,255,255,.18);border-radius:30px;padding:40px 44px 50px;font-family:"DejaVu Sans Mono",monospace;font-size:38px;line-height:1.9;box-shadow:0 40px 90px rgba(0,0,0,.5)}
.dots{margin-bottom:24px}.dots i{display:inline-block;width:22px;height:22px;border-radius:50%;margin-right:12px;background:#ff5f57}.dots i:nth-child(2){background:#febc2e}.dots i:nth-child(3){background:#28c840}
.line.cl{color:var(--a)}
.num{font-size:260px;font-weight:900;line-height:1;color:var(--a);margin-bottom:30px}
.ctaicon{width:150px;height:150px;border-radius:40px;background:var(--a);color:#0b0d14;display:grid;place-items:center;margin-bottom:60px}
.ctaicon svg{width:84px;height:84px}
.cta .sub{color:#f4f5f8;opacity:.8}
"""

def build(key, spec, outdir):
    os.makedirs(outdir, exist_ok=True)
    work = os.path.join(outdir, key + "_work"); os.makedirs(work, exist_ok=True)
    t = LEAD; parts = []
    for i, sc in enumerate(spec["scenes"]):
        vp = os.path.join(work, f"v{i}.wav"); tts(sc["voice"], vp)
        vd = wav_dur(vp); dur = VOICE_OFF + vd + PAD
        parts.append((sc, t, dur, vp)); t += dur
    total = t + 0.4
    # voice track
    vo = np.zeros(int(total * SR), dtype=np.float32)
    for sc, st, dur, vp in parts:
        with wave.open(vp) as w:
            a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32767
        s = int((st + VOICE_OFF) * SR); vo[s:s+len(a)] += a[:len(vo)-s]
    with wave.open(os.path.join(work, "voice.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(vo, -1, 1) * 32767).astype(np.int16).tobytes())
    music(total, os.path.join(work, "music.wav"), seed=len(key))
    scenes = "".join(scene_html(sc, st, dur, spec["accent"]) for sc, st, dur, _ in parts)
    page = f"""<!doctype html><html lang="fa"><head><meta charset="utf-8"><style>{CSS}</style></head>
<body style="--a:{spec['accent']};--T:{total:.3f}s"><div class="bg"><div class="blob b1"></div><div class="blob b2"></div><div class="grain"></div></div>
<div class="tag">{esc(spec['tag'])}</div>{scenes}<div class="bar"><i></i></div></body></html>"""
    hp = os.path.join(ROOT, f"_{key}.html"); open(hp, "w").write(page)
    silent = os.path.join(work, "silent.mp4")
    nframes = int(total * FPS)
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", silent], stdin=subprocess.PIPE)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.goto("file://" + hp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
        for f in range(nframes):
            ms = f * 1000 / FPS
            pg.evaluate("ms=>document.getAnimations().forEach(a=>{a.pause();a.currentTime=ms})", ms)
            ff.stdin.write(pg.screenshot(type="jpeg", quality=90, animations="allow", caret="initial"))
        b.close()
    ff.stdin.close(); ff.wait()
    out = os.path.join(outdir, key + ".mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", os.path.join(work, "voice.wav"), "-i", os.path.join(work, "music.wav"),
                    "-filter_complex", "[2:a]volume=0.13[m];[1:a][m]amix=inputs=2:duration=first:normalize=0,aresample=44100,loudnorm=I=-14:TP=-1[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    print(key, f"{total:.1f}s", out)

if __name__ == "__main__":
    specs = json.load(open(os.path.join(ROOT, "scripts.json")))
    only = sys.argv[1:] or list(specs)
    for k in only:
        build(k, specs[k], os.path.join(ROOT, "out"))
