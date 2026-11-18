"""V2 reel design: kinetic typography, glass cards, story-style progress, SFX.
Usage: python3 build2.py <key> <voice.mp3>   (scenes timed to the voiceover's pauses)"""
import json, os, re, subprocess, sys, wave, html
import numpy as np
from playwright.sync_api import sync_playwright
from align import boundaries
from build import music, W, H, FPS, SR

ROOT = os.path.dirname(os.path.abspath(__file__))
LEAD, TAIL = 0.35, 1.0
HANDLE = "@ehbehzad"

def esc(s):
    return html.escape(s)

def rich(s):
    """escape, newline -> <br>, [[x]] -> highlight marker"""
    out = []
    for line in s.split("\n"):
        e = esc(line)
        e = re.sub(r"\[\[(.+?)\]\]", r'<mark>\1</mark>', e)
        out.append(e)
    return "<br>".join(out)

def words(s, start, step=0.11, cls="w"):
    """word-by-word reveal; keeps [[..]] highlight spans intact"""
    html_lines, i = [], 0
    for line in s.split("\n"):
        parts = re.findall(r"\[\[.+?\]\]|\S+", line)
        spans = []
        for p in parts:
            hl = p.startswith("[[")
            txt = esc(p[2:-2] if hl else p)
            inner = f"<mark>{txt}</mark>" if hl else txt
            spans.append(f'<span class="{cls}" style="animation-delay:{start + i*step:.3f}s">{inner}</span>')
            i += 1
        html_lines.append(" ".join(spans))
    return "<br>".join(html_lines), i

ICON = {
    "bad": '<svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>',
    "good": '<svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "copy": '<svg viewBox="0 0 24 24"><rect x="8" y="8" width="12" height="12" rx="3" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16 8V6a2 2 0 00-2-2H6a2 2 0 00-2 2v8a2 2 0 002 2h2" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
    "spark": '<svg viewBox="0 0 24 24"><path d="M12 2l2.2 6.3L20.5 10l-6.3 2.2L12 18.5l-2.2-6.3L3.5 10l6.3-1.7z" fill="currentColor"/></svg>',
    "heart": '<svg viewBox="0 0 24 24"><path d="M12 20s-7-4.4-7-10a4 4 0 017-2.6A4 4 0 0119 10c0 5.6-7 10-7 10z" fill="currentColor"/></svg>',
    "send": '<svg viewBox="0 0 24 24"><path d="M21 3L3 10.5l7 2.5 2.5 7z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
    "save": '<svg viewBox="0 0 24 24"><path d="M6 3h12v18l-6-4.5L6 21z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
}

def scene_html(sc, st, dur):
    d = lambda off: f"animation-delay:{st+off:.3f}s"
    t = sc["type"]
    body = ""
    if t == "hook":
        w, n = words(sc["title"], st + 0.1, 0.12)
        body = f'<div class="hook-t">{w}</div>'
        if sc.get("sub"):
            body += f'<div class="pill pop" style="{d(0.25 + n*0.12)}">{esc(sc["sub"])}</div>'
    elif t == "point":
        mark = sc.get("mark")
        badge = ICON[mark] if mark else esc(sc["num"])
        body = (f'<div class="card rise" style="{d(0.0)}">'
                f'<div class="badge {mark or ""} pop" style="{d(0.15)}">{badge}</div>'
                f'<div class="kicker rise" style="{d(0.25)}">{esc(sc["kicker"]) if sc.get("kicker") else ("اشتباه" if mark=="bad" else "قدم") + " " + esc(sc["num"])}</div>'
                f'<div class="p-t rise" style="{d(0.35)}">{rich(sc["title"])}</div>'
                f'<div class="p-s rise" style="{d(0.7)}">{esc(sc["sub"])}</div>')
        if sc.get("chips"):
            body += '<div class="chips">' + "".join(
                f'<span class="chip pop" style="{d(1.1 + i*0.22)}">{esc(c)}</span>' for i, c in enumerate(sc["chips"])) + "</div>"
        body += "</div>"
    elif t == "compare":
        body = (f'<div class="kicker rise" style="{d(0.0)}">{esc(sc["kicker"]) if sc.get("kicker") else "اشتباه " + esc(sc["num"])}</div>'
                f'<div class="p-t rise" style="{d(0.1)}">{esc(sc["title"])}</div>'
                f'<div class="cmp bad rise" style="{d(0.6)}"><i class="ic">{ICON["bad"]}</i><div>{esc(sc["bad"])}</div></div>'
                f'<div class="cmp good rise" style="{d(max(1.4, dur*0.45))}"><i class="ic">{ICON["good"]}</i><div>{esc(sc["good"])}</div></div>')
    elif t == "prompt":
        n = len(sc["lines"]); gap = max(0.45, (dur - 1.6) / n)
        lines = "".join(
            f'<div class="ln type" style="{d(0.7 + i*gap)};--ty:{gap*0.8:.2f}s">{rich(l)}</div>' for i, l in enumerate(sc["lines"]))
        body = (f'<div class="p-t sm rise" style="{d(0.0)}">{esc(sc["title"])}</div>'
                f'<div class="chat rise" style="{d(0.25)}"><div class="chat-h"><span class="dot"></span>'
                f'<span>پیام تو به هوش مصنوعی</span><i class="cp">{ICON["copy"]}</i></div>{lines}</div>')
    elif t == "predict":
        opts = ""
        for i, (wd, pc) in enumerate(sc["options"]):
            opts += (f'<div class="opt {"top" if i==0 else ""} rise" style="{d(1.0 + i*0.25)}"><span class="ow">{esc(wd)}</span>'
                     f'<span class="track"><i class="fill" style="{d(1.3 + i*0.25)};--w:{pc}%"></i></span><b>{pc}٪</b></div>')
        body = (f'<div class="p-t sm rise" style="{d(0.0)}">{esc(sc["title"])}</div>'
                f'<div class="sent rise" style="{d(0.3)}">{esc(sc["sentence"])} <span class="guess pop" style="{d(max(2.4, dur*0.72))}">{esc(sc["options"][0][0])}</span><span class="caret"></span></div>'
                f'<div class="opts">{opts}</div><div class="note rise" style="{d(1.8)}">{esc(sc["note"])}</div>')
    elif t == "cta":
        w, n = words(sc["title"], st + 0.35, 0.1)
        body = (f'<div class="prof pop" style="{d(0.0)}"><div class="av">{ICON["spark"]}</div><div class="hd" dir="ltr">{HANDLE}</div></div>'
                f'<div class="cta-t">{w}</div>'
                f'<div class="follow pop" style="{d(0.5 + n*0.1)}">+ فالو</div>'
                f'<div class="acts rise" style="{d(0.8 + n*0.1)}"><i>{ICON["heart"]}</i><i>{ICON["send"]}</i><i>{ICON["save"]}</i></div>'
                f'<div class="p-s rise" style="{d(0.9 + n*0.1)}">{esc(sc["sub"])}</div>')
    life = f"animation:life {dur:.3f}s linear {st:.3f}s both"
    return f'<section class="scene {t}" style="{life}">{body}</section>'

FONTS = open(os.path.join(ROOT, "build.py")).read().split('CSS = """')[1].split("*{margin")[0]

CSS = FONTS + """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#06070c;font-family:V,sans-serif;color:#f5f6fa}
.bg{position:absolute;inset:0;overflow:hidden}
.glow{position:absolute;border-radius:50%;filter:blur(40px)}
.g1{width:1100px;height:1100px;top:-300px;right:-350px;background:radial-gradient(circle,var(--a) 0%,transparent 62%);opacity:.55;animation:d1 11s ease-in-out 0s infinite alternate}
.g2{width:1000px;height:1000px;bottom:-200px;left:-380px;background:radial-gradient(circle,var(--b) 0%,transparent 62%);opacity:.38;animation:d2 13s ease-in-out 0s infinite alternate}
@keyframes d1{to{transform:translate(-300px,380px) scale(1.15)}}
@keyframes d2{to{transform:translate(330px,-420px) scale(1.2)}}
.grid{position:absolute;left:-50%;right:-50%;bottom:-120px;height:900px;transform:perspective(700px) rotateX(62deg);transform-origin:bottom;
 background-image:linear-gradient(rgba(255,255,255,.07) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.07) 2px,transparent 2px);
 background-size:90px 90px;animation:gridmv 4s linear 0s infinite;mask-image:linear-gradient(to top,#000 10%,transparent 85%);-webkit-mask-image:linear-gradient(to top,#000 10%,transparent 85%)}
@keyframes gridmv{to{background-position:0 90px}}
.pt{position:absolute;width:6px;height:6px;border-radius:50%;background:#fff;opacity:.0;animation:fly linear 0s infinite}
@keyframes fly{0%{opacity:0;transform:translateY(0)}15%{opacity:.5}100%{opacity:0;transform:translateY(-900px)}}
.vig{position:absolute;inset:0;background:radial-gradient(ellipse at center,transparent 45%,rgba(0,0,0,.6) 100%)}
.noise{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(255,255,255,.015) 0 2px,transparent 2px 4px)}
/* header */
.segs{position:absolute;top:70px;left:70px;right:70px;display:flex;gap:10px;direction:rtl}
.seg{flex:1;height:7px;border-radius:6px;background:rgba(255,255,255,.18);overflow:hidden}
.seg i{display:block;height:100%;background:#fff;transform-origin:right;animation:segfill linear both}
@keyframes segfill{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.head{position:absolute;top:110px;left:70px;right:70px;display:flex;justify-content:space-between;align-items:center;direction:rtl}
.tag{display:flex;align-items:center;gap:14px;font-size:34px;font-weight:700;padding:12px 28px;border-radius:40px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14)}
.tag::before{content:"";width:14px;height:14px;border-radius:50%;background:var(--a);box-shadow:0 0 18px var(--a)}
.me{display:flex;align-items:center;gap:14px;font-size:32px;font-weight:700;opacity:.85}
.me .mini{width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,var(--a),var(--b));display:grid;place-items:center;color:#06070c}
.me .mini svg{width:28px;height:28px}
/* scenes */
.scene{position:absolute;left:0;right:0;top:230px;bottom:330px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:0 80px;direction:rtl}
@keyframes life{0%{opacity:0;transform:scale(.94);filter:blur(18px)}5%{opacity:1;transform:none;filter:none}93%{opacity:1;transform:none;filter:none}100%{opacity:0;transform:scale(1.05);filter:blur(14px)}}
mark{color:#06070c;background:linear-gradient(90deg,var(--a),var(--b));padding:0 18px;border-radius:18px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.w{display:inline-block;animation:wpop .5s cubic-bezier(.2,1.2,.3,1) both}
@keyframes wpop{from{opacity:0;transform:translateY(40px) scale(.8);filter:blur(10px)}to{opacity:1;transform:none;filter:none}}
.rise{animation:rise .6s cubic-bezier(.2,.8,.2,1) both}
@keyframes rise{from{opacity:0;transform:translateY(50px);filter:blur(8px)}to{opacity:1;transform:none;filter:none}}
.pop{animation:pop .55s cubic-bezier(.2,1.4,.4,1) both}
@keyframes pop{from{opacity:0;transform:scale(.5)}to{opacity:1;transform:none}}
.hook-t{font-size:118px;font-weight:900;line-height:1.38;text-shadow:0 10px 50px rgba(0,0,0,.5)}
.pill{margin-top:60px;font-size:48px;font-weight:700;padding:20px 46px;border-radius:60px;border:2px solid var(--a);color:var(--a);background:rgba(0,0,0,.25)}
.card{width:100%;padding:80px 64px 70px;border-radius:56px;background:linear-gradient(160deg,rgba(255,255,255,.10),rgba(255,255,255,.03));border:1.5px solid rgba(255,255,255,.16);box-shadow:0 50px 120px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.2);display:flex;flex-direction:column;align-items:center}
.badge{width:170px;height:170px;border-radius:50%;display:grid;place-items:center;font-size:96px;font-weight:900;color:#06070c;background:linear-gradient(135deg,var(--a),var(--b));box-shadow:0 0 70px color-mix(in srgb,var(--a) 60%,transparent);margin-bottom:34px}
.badge svg{width:96px;height:96px}
.badge.bad{background:linear-gradient(135deg,#ff4d5e,#ff8a3c);color:#fff;box-shadow:0 0 70px rgba(255,77,94,.55)}
.badge.good{background:linear-gradient(135deg,#2ee6a0,#29b6ff);color:#06070c}
.kicker{font-size:38px;font-weight:700;letter-spacing:1px;opacity:.6;margin-bottom:18px}
.p-t{font-size:92px;font-weight:900;line-height:1.35}
.p-t.sm{font-size:70px;margin-bottom:50px}
.p-s{margin-top:34px;font-size:48px;font-weight:700;color:var(--a);line-height:1.5}
.chips{margin-top:54px;display:flex;flex-wrap:wrap;justify-content:center;gap:22px}
.chip{font-size:44px;font-weight:700;padding:18px 36px;border-radius:26px;background:rgba(255,255,255,.08);border:1.5px solid rgba(255,255,255,.2)}
.cmp{width:100%;display:flex;gap:28px;align-items:center;text-align:right;margin-top:44px;padding:44px 46px;border-radius:40px;font-size:50px;font-weight:700;line-height:1.55}
.cmp .ic{flex:none;width:92px;height:92px;border-radius:50%;display:grid;place-items:center}
.cmp .ic svg{width:54px;height:54px}
.cmp.bad{background:rgba(255,77,94,.08);border:2px solid rgba(255,77,94,.5);color:rgba(255,255,255,.7)}
.cmp.bad .ic{background:#ff4d5e;color:#fff}
.cmp.good{background:rgba(46,230,160,.09);border:2px solid rgba(46,230,160,.7);box-shadow:0 0 80px rgba(46,230,160,.2)}
.cmp.good .ic{background:#2ee6a0;color:#06070c}
.chat{width:100%;text-align:right;border-radius:44px;background:#0d0f17;border:1.5px solid rgba(255,255,255,.16);box-shadow:0 50px 120px rgba(0,0,0,.5);padding:0 0 40px;overflow:hidden}
.chat-h{display:flex;align-items:center;gap:18px;padding:30px 44px;font-size:36px;font-weight:700;background:rgba(255,255,255,.05);border-bottom:1px solid rgba(255,255,255,.1);margin-bottom:26px;opacity:.85}
.chat-h .dot{width:18px;height:18px;border-radius:50%;background:var(--a);box-shadow:0 0 14px var(--a)}
.chat-h .cp{margin-right:auto;width:46px;height:46px;opacity:.7}
.ln{font-size:54px;font-weight:700;line-height:1.6;padding:6px 48px}
.ln mark{padding:0 12px;border-radius:12px}
.type{animation:typer var(--ty) steps(18) both}
@keyframes typer{from{clip-path:inset(0 0 0 100%)}to{clip-path:inset(0 0 0 0)}}
.sent{font-size:76px;font-weight:900;padding:40px 50px;border-radius:36px;background:rgba(255,255,255,.06);border:1.5px solid rgba(255,255,255,.15)}
.guess{display:inline-block;color:var(--a)}
.caret{display:inline-block;width:8px;height:74px;background:#fff;margin-right:10px;vertical-align:-10px;animation:blink 1s steps(1) 0s infinite}
@keyframes blink{50%{opacity:0}}
.opts{width:100%;margin-top:60px;display:flex;flex-direction:column;gap:30px}
.opt{display:flex;align-items:center;gap:30px;font-size:52px;font-weight:700}
.opt .ow{width:170px;text-align:right}
.opt .track{flex:1;height:54px;border-radius:30px;background:rgba(255,255,255,.08);overflow:hidden}
.opt .fill{display:block;height:100%;width:var(--w);border-radius:30px;background:rgba(255,255,255,.35);transform-origin:right;animation:grow .9s cubic-bezier(.2,.8,.2,1) both}
.opt.top .fill{background:linear-gradient(90deg,var(--b),var(--a))}
.opt b{width:130px;text-align:left;font-weight:900}
.opt.top b,.opt.top .ow{color:var(--a)}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.note{margin-top:40px;font-size:34px;opacity:.5}
.prof{display:flex;flex-direction:column;align-items:center;gap:20px;margin-bottom:50px}
.av{width:200px;height:200px;border-radius:50%;display:grid;place-items:center;color:#fff;background:#11131c;border:8px solid transparent;
 background-image:linear-gradient(#11131c,#11131c),linear-gradient(135deg,var(--a),var(--b));background-origin:border-box;background-clip:padding-box,border-box;box-shadow:0 0 80px color-mix(in srgb,var(--a) 50%,transparent)}
.av svg{width:100px;height:100px;color:var(--a)}
.hd{font-size:46px;font-weight:700}
.cta-t{font-size:80px;font-weight:900;line-height:1.4}
.follow{margin-top:56px;font-size:56px;font-weight:900;padding:26px 110px;border-radius:30px;color:#06070c;background:linear-gradient(90deg,var(--a),var(--b));box-shadow:0 20px 70px color-mix(in srgb,var(--a) 50%,transparent);animation:pop .55s cubic-bezier(.2,1.4,.4,1) both,pulse 1.2s ease-in-out 0s infinite}
@keyframes pulse{50%{box-shadow:0 20px 110px color-mix(in srgb,var(--a) 80%,transparent)}}
.acts{margin-top:46px;display:flex;gap:60px}
.acts i{width:74px;height:74px;opacity:.85}
.cta .p-s{font-size:42px;color:#f5f6fa;opacity:.7}
"""

def particles(n=26, seed=3):
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        x, y = rng.uniform(0, 1080), rng.uniform(700, 1900)
        dur, delay, sz = rng.uniform(6, 12), -rng.uniform(0, 12), rng.uniform(3, 8)
        out.append(f'<i class="pt" style="left:{x:.0f}px;top:{y:.0f}px;width:{sz:.1f}px;height:{sz:.1f}px;animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s"></i>')
    return "".join(out)

def sfx(total, starts, out):
    t = np.arange(int(total * SR)) / SR
    sig = np.zeros_like(t)
    rng = np.random.default_rng(7)
    for i, s in enumerate(starts):
        n = int(0.45 * SR); a = int(max(0, s - 0.22) * SR)
        if a + n > len(sig): continue
        noise = rng.normal(0, 1, n)
        # crude swept band-pass via moving-average difference
        k = np.linspace(1, 0, n)
        env = np.sin(np.pi * np.linspace(0, 1, n)) ** 2
        lp1 = np.convolve(noise, np.ones(6) / 6, "same"); lp2 = np.convolve(noise, np.ones(40) / 40, "same")
        band = lp1 * (1 - k) + (lp1 - lp2) * k
        sig[a:a + n] += band * env * (0.5 if i else 0.8)
    sig = sig / (np.max(np.abs(sig)) + 1e-9) * 0.6
    with wave.open(out, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((sig * 32767).astype(np.int16).tobytes())

def run(key, voice_mp3, specfile="scripts2.json"):
    spec = json.load(open(os.path.join(ROOT, specfile)))[key]
    bounds, s0, s1, vdur = boundaries(voice_mp3, [sc["voice"] for sc in spec["scenes"]])
    total = LEAD + vdur + TAIL
    starts = [0.0] + [LEAD + b for b in bounds]
    ends = starts[1:] + [total]
    work = os.path.join(ROOT, "out", key + "_v2"); os.makedirs(work, exist_ok=True)
    music(total, os.path.join(work, "music.wav"), seed=len(key) + 3)
    sfx(total, starts, os.path.join(work, "sfx.wav"))
    scenes = "".join(scene_html(sc, st, en - st) for sc, st, en in zip(spec["scenes"], starts, ends))
    segs = "".join(f'<div class="seg"><i style="animation-duration:{en-st:.3f}s;animation-delay:{st:.3f}s"></i></div>' for st, en in zip(starts, ends))
    page = f"""<!doctype html><html lang="fa"><head><meta charset="utf-8"><style>{CSS}</style></head>
<body style="--a:{spec['accent']};--b:{spec['accent2']}"><div class="bg"><div class="glow g1"></div><div class="glow g2"></div><div class="grid"></div>{particles()}<div class="vig"></div><div class="noise"></div></div>
<div class="segs">{segs}</div><div class="head"><div class="tag">{esc(spec['tag'])}</div><div class="me" dir="ltr"><span class="mini">{ICON['spark']}</span>{HANDLE}</div></div>
{scenes}</body></html>"""
    hp = os.path.join(ROOT, f"_{key}_v2.html"); open(hp, "w").write(page)
    silent = os.path.join(work, "silent.mp4")
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", silent], stdin=subprocess.PIPE)
    only = os.environ.get("FRAMES")  # debug: comma list of seconds -> png stills
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H})
        pg.goto("file://" + hp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
        if only:
            for s in only.split(","):
                pg.evaluate("ms=>document.getAnimations().forEach(a=>{a.pause();a.currentTime=ms})", float(s) * 1000)
                pg.screenshot(path=os.path.join(work, f"still_{s}.png"))
            b.close(); ff.stdin.close(); ff.wait(); print("stills", work); return
        for f in range(int(total * FPS)):
            pg.evaluate("ms=>document.getAnimations().forEach(a=>{a.pause();a.currentTime=ms})", f * 1000 / FPS)
            ff.stdin.write(pg.screenshot(type="jpeg", quality=90))
        b.close()
    ff.stdin.close(); ff.wait()
    out = os.path.join(ROOT, "out", key + ".mp4")
    L = int(LEAD * 1000)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", voice_mp3, "-i", os.path.join(work, "music.wav"), "-i", os.path.join(work, "sfx.wav"),
                    "-filter_complex", f"[1:a]adelay={L}|{L},aresample=44100[v];[2:a]volume=0.09,aresample=44100[m];[3:a]volume=0.10,aresample=44100[s];[v][m][s]amix=inputs=3:duration=longest:normalize=0,loudnorm=I=-14:TP=-1[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(key, f"{total:.1f}s", [round(s, 2) for s in starts], out)

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
