"""V5 'motion' theme: Adobe Stock footage with ffmpeg xfade transitions + a new kinetic overlay
(masked word reveals, highlight sweeps, 3D card flips, animated gradient borders, ring-draw badges,
light sweeps, zoom-through exits, a 'steps' timeline scene).
Usage: python3 build5.py <key> <voice.mp3> [scripts.json]   (FRAMES=1,2 -> debug stills)"""
import json, os, re, subprocess, sys
from playwright.sync_api import sync_playwright
from align import boundaries
from build import music, W, H, FPS
import build2 as B2
import build3 as B3
from build2 import esc, ICON, HANDLE, LEAD, TAIL, sfx

ROOT = os.path.dirname(os.path.abspath(__file__))
STOCK = "/home/claude/reels-media/stock"
XF = 0.45  # background crossfade length
XFADES = ["smoothleft", "circleopen", "slideup", "zoomin", "radial", "smoothright", "diagtl"]

CSS = B2.FONTS + """
@property --ang{syntax:'<angle>';inherits:false;initial-value:0deg}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:transparent;font-family:V,sans-serif;color:#fff}
.shade{position:absolute;inset:0;background:
 linear-gradient(180deg,rgba(0,0,0,.74) 0%,rgba(0,0,0,.12) 20%,rgba(0,0,0,.22) 55%,rgba(0,0,0,.85) 100%),
 radial-gradient(ellipse at 50% 46%,rgba(0,0,0,0) 0%,rgba(0,0,0,.5) 100%)}
/* drifting accent light leaks */
.leak{position:absolute;width:900px;height:900px;border-radius:50%;filter:blur(120px);opacity:.22;mix-blend-mode:screen}
.l1{background:var(--a);top:-260px;right:-380px;animation:drift1 9s ease-in-out 0s infinite alternate}
.l2{background:var(--b);bottom:-320px;left:-420px;opacity:.16;animation:drift2 11s ease-in-out 0s infinite alternate}
@keyframes drift1{to{transform:translate(-260px,320px) scale(1.2)}}
@keyframes drift2{to{transform:translate(300px,-260px) scale(1.15)}}
/* cut transition: skewed accent panel sweeping across */
.wipe{position:absolute;top:-200px;bottom:-200px;width:700px;left:-1700px;background:linear-gradient(90deg,transparent,var(--a) 35%,rgba(255,255,255,.9) 50%,var(--a) 65%,transparent);transform:skewX(-18deg);opacity:.0;animation:wipe .5s cubic-bezier(.6,0,.3,1) forwards}
@keyframes wipe{0%{left:-900px;opacity:.38}100%{left:1300px;opacity:.38}}
.segs{position:absolute;top:66px;left:60px;right:60px;display:flex;gap:10px;direction:rtl}
.seg{flex:1;height:7px;border-radius:6px;background:rgba(255,255,255,.28);overflow:hidden}
.seg i{display:block;height:100%;background:linear-gradient(270deg,#fff,var(--a));transform-origin:right;animation:segfill linear both}
@keyframes segfill{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.head{position:absolute;top:104px;left:60px;right:60px;display:flex;justify-content:space-between;align-items:center;direction:rtl}
.tag{font-size:34px;font-weight:900;padding:10px 26px;border-radius:40px;background:rgba(0,0,0,.45);color:#fff;border:2px solid var(--a);display:flex;gap:12px;align-items:center}
.tag::before{content:"";width:14px;height:14px;border-radius:50%;background:var(--a);box-shadow:0 0 14px var(--a);animation:blink2 1.6s ease-in-out 0s infinite}
@keyframes blink2{50%{opacity:.25}}
.me{display:flex;align-items:center;gap:14px;font-size:34px;font-weight:700;text-shadow:0 2px 14px rgba(0,0,0,.6)}
.me .mini{width:54px;height:54px;border-radius:50%;background:var(--a);display:grid;place-items:center;color:#0b0b0f}
.me .mini svg{width:28px;height:28px}
.scene::before{content:'';position:absolute;inset:-80px -40px;background:radial-gradient(ellipse at 50% 50%,rgba(0,0,0,.45),rgba(0,0,0,0) 70%);z-index:-1}
.scene{position:absolute;z-index:0;left:0;right:0;top:240px;bottom:360px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:0 70px;direction:rtl;perspective:1800px}
@keyframes enter{from{opacity:0;transform:scale(1.1);filter:blur(18px)}to{opacity:1;transform:none;filter:none}}
@keyframes leave{from{opacity:1;transform:none;filter:none}to{opacity:0;transform:scale(1.18);filter:blur(16px)}}
/* masked word reveal */
.wm{display:inline-block;overflow:hidden;vertical-align:top;padding:0 4px;margin:-6px 0}
.wm>.w{display:inline-block;animation:wup .55s cubic-bezier(.16,1,.3,1) both}
@keyframes wup{from{transform:translateY(105%) rotate(4deg);opacity:0}to{transform:none;opacity:1}}
.slam .wm{overflow:visible}
.slam .wm>.w{animation:slam .5s cubic-bezier(.2,1.2,.3,1) both}
@keyframes slam{0%{opacity:0;transform:scale(2.4);filter:blur(14px)}60%{opacity:1;filter:none}100%{transform:none}}
/* highlight sweep */
mark{color:#fff;background:linear-gradient(var(--a),var(--a)) no-repeat right/0% 100%;padding:0 18px;border-radius:12px;box-decoration-break:clone;-webkit-box-decoration-break:clone;animation:hl .6s cubic-bezier(.7,0,.2,1) both;animation-delay:inherit}
@keyframes hl{0%,30%{background-size:0% 100%;color:#fff}100%{background-size:100% 100%;color:#0b0b0f}}
.rise{animation:rise .6s cubic-bezier(.16,1,.3,1) both}
@keyframes rise{from{opacity:0;transform:translateY(60px);filter:blur(8px)}to{opacity:1;transform:none;filter:none}}
.pop{animation:pop .6s cubic-bezier(.2,1.6,.4,1) both}
@keyframes pop{from{opacity:0;transform:scale(.3) rotate(-14deg)}to{opacity:1;transform:none}}
.flip{animation:flip .8s cubic-bezier(.16,1,.3,1) both;transform-origin:50% 100%}
@keyframes flip{from{opacity:0;transform:rotateX(-75deg) translateY(140px)}to{opacity:1;transform:none}}
.fromR{animation:fromR .7s cubic-bezier(.16,1,.3,1) both}
@keyframes fromR{from{opacity:0;transform:translateX(260px) rotateY(-35deg)}to{opacity:1;transform:none}}
.fromL{animation:fromL .7s cubic-bezier(.16,1,.3,1) both}
@keyframes fromL{from{opacity:0;transform:translateX(-260px) rotateY(35deg)}to{opacity:1;transform:none}}
/* glass card with rotating gradient border + sheen */
.gb{position:relative;border-radius:40px;background:rgba(8,8,14,.66);box-shadow:0 40px 110px rgba(0,0,0,.5);overflow:hidden}
.gb::before{content:"";position:absolute;inset:0;border-radius:inherit;padding:3px;background:conic-gradient(from var(--ang),rgba(255,255,255,.12),var(--a),rgba(255,255,255,.12) 35%,var(--b),rgba(255,255,255,.12) 75%);
 -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;animation:spin 4s linear 0s infinite;pointer-events:none}
@keyframes spin{to{--ang:360deg}}
.gb::after{content:"";position:absolute;top:0;bottom:0;width:240px;left:-320px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.22),transparent);transform:skewX(-20deg);animation:sheen 1.1s ease-in-out both;animation-delay:inherit}
@keyframes sheen{0%,40%{left:-320px}100%{left:1100px}}
.hook-t{font-size:122px;font-weight:900;line-height:1.38;text-shadow:0 8px 40px rgba(0,0,0,.7)}
.pill{margin-top:56px;font-size:46px;font-weight:700;padding:16px 40px;border-radius:60px;background:rgba(0,0,0,.5);border:2px solid rgba(255,255,255,.25);display:flex;align-items:center;gap:16px}
.pill::before{content:"";width:16px;height:16px;border-radius:50%;background:var(--a);box-shadow:0 0 16px var(--a)}
.card{width:100%;padding:70px 56px 64px;display:flex;flex-direction:column;align-items:center}
.bw{position:relative;width:170px;height:170px;margin-bottom:26px;display:grid;place-items:center}
.bw svg.ring{position:absolute;inset:0;transform:rotate(-90deg)}
.bw svg.ring circle{fill:none;stroke:var(--a);stroke-width:6;stroke-linecap:round;stroke-dasharray:500;stroke-dashoffset:500;animation:ring 1s cubic-bezier(.6,0,.2,1) both;animation-delay:inherit}
.bw.bad svg.ring circle{stroke:#ff4d5e}.bw.good svg.ring circle{stroke:#2ee6a0}
@keyframes ring{to{stroke-dashoffset:0}}
.badge{width:128px;height:128px;border-radius:50%;display:grid;place-items:center;font-size:76px;font-weight:900;color:#0b0b0f;background:var(--a)}
.badge svg{width:72px;height:72px}
.bad .badge{background:#ff4d5e;color:#fff}.good .badge{background:#2ee6a0}
.kicker{display:flex;align-items:center;gap:18px;font-size:38px;font-weight:900;letter-spacing:1px;color:var(--a);margin-bottom:16px;text-shadow:0 2px 12px rgba(0,0,0,.9),0 0 2px rgba(0,0,0,.9)}
.kicker::before,.kicker::after{content:"";height:3px;width:70px;background:var(--a);transform-origin:center;animation:line .7s cubic-bezier(.16,1,.3,1) both;animation-delay:inherit}
@keyframes line{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.p-t{font-size:90px;font-weight:900;line-height:1.36;text-shadow:0 6px 30px rgba(0,0,0,.5)}
.p-t.sm{font-size:68px;margin-bottom:46px}
.p-s{margin-top:28px;font-size:46px;font-weight:700;line-height:1.5;opacity:.9}
.chips{margin-top:46px;display:flex;flex-wrap:wrap;justify-content:center;gap:20px}
.chip{font-size:44px;font-weight:900;padding:14px 34px;border-radius:40px;background:var(--a);color:#0b0b0f;box-shadow:0 10px 30px rgba(0,0,0,.35)}
.chat{width:100%;text-align:right;padding-bottom:34px}
.chat-h{display:flex;align-items:center;gap:16px;padding:24px 40px;font-size:34px;font-weight:700;background:rgba(255,255,255,.07);margin-bottom:22px}
.chat-h .dot{width:18px;height:18px;border-radius:50%;background:var(--a);box-shadow:0 0 12px var(--a)}
.chat-h .cp{margin-right:auto;width:44px;height:44px}
.ln{font-size:54px;font-weight:700;line-height:1.6;padding:6px 44px;position:relative}
.ln mark{padding:0 10px}
.type{animation:typer var(--ty) steps(22) both}
@keyframes typer{from{clip-path:inset(0 0 0 100%)}to{clip-path:inset(0 0 0 0)}}
.send{display:flex;justify-content:flex-start;padding:16px 40px 0}
.send b{display:flex;gap:12px;align-items:center;font-size:36px;font-weight:900;color:#0b0b0f;background:var(--a);padding:12px 30px;border-radius:40px}
.send svg{width:36px;height:36px}
.prof{display:flex;flex-direction:column;align-items:center;gap:16px;margin-bottom:44px}
.av{position:relative;width:200px;height:200px;border-radius:50%;display:grid;place-items:center;background:rgba(0,0,0,.55)}
.av::before{content:"";position:absolute;inset:-8px;border-radius:50%;padding:8px;background:conic-gradient(from var(--ang),var(--a),var(--b),var(--a));-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;animation:spin 2.5s linear 0s infinite}
.av svg{width:92px;height:92px;color:var(--a)}
.hd{font-size:46px;font-weight:900;text-shadow:0 2px 14px rgba(0,0,0,.6)}
.cta-t{font-size:86px;font-weight:900;line-height:1.42;text-shadow:0 6px 30px rgba(0,0,0,.6)}
.fw{position:relative;margin-top:56px}
.follow{position:relative;z-index:1;font-size:58px;font-weight:900;padding:24px 110px;border-radius:60px;color:#0b0b0f;background:var(--a)}
.rip{position:absolute;inset:0;border-radius:60px;border:4px solid var(--a);animation:rip 1.6s ease-out 0s infinite}
.rip.r2{animation-delay:-.8s}
@keyframes rip{from{transform:scale(1);opacity:.9}to{transform:scale(1.45,1.9);opacity:0}}
.acts{margin-top:46px;display:flex;gap:56px}
.acts i{width:76px;height:76px;filter:drop-shadow(0 2px 10px rgba(0,0,0,.6))}
.acts i:nth-child(1){animation:beat 1s ease-in-out 0s infinite;color:#ff4d6d}
@keyframes beat{0%,100%{transform:scale(1)}15%{transform:scale(1.25)}30%{transform:scale(1)}}
.io-in,.io-out{width:100%;display:flex;align-items:center;gap:32px;text-align:right;padding:38px 42px;border-radius:32px;position:relative}
.io-in{background:rgba(8,8,12,.7);border:2px solid rgba(255,255,255,.2)}
.io-out{background:var(--a);color:#0b0b0f}
.io-ic{flex:none;width:124px;height:124px;border-radius:28px;display:grid;place-items:center;background:rgba(255,255,255,.12)}
.io-out .io-ic{background:rgba(0,0,0,.12)}
.io-ic svg{width:78px;height:78px}
.io-in small,.io-out small{display:block;font-size:34px;font-weight:700;opacity:.75;margin-bottom:6px}
.io-in b,.io-out b{display:block;font-size:56px;font-weight:900;line-height:1.35}
.io-ar{width:100px;height:100px;margin:26px 0;padding:16px;border-radius:50%;background:#fff;color:#0b0b0f}
/* compare */
.cmp{width:100%;display:flex;gap:26px;align-items:center;text-align:right;margin-top:40px;padding:40px 42px;border-radius:30px;font-size:50px;font-weight:700;line-height:1.55;position:relative}
.cmp .ic{flex:none;width:90px;height:90px;border-radius:50%;display:grid;place-items:center}
.cmp .ic svg{width:52px;height:52px}
.cmp.bad{background:rgba(8,8,12,.72);border:2px solid rgba(255,77,94,.7);color:rgba(255,255,255,.85)}
.cmp.bad .ic{background:#ff4d5e;color:#fff}
.cmp.bad .strike{position:absolute;right:150px;left:42px;top:50%;height:6px;border-radius:4px;background:#ff4d5e;transform-origin:right;animation:line .5s cubic-bezier(.7,0,.2,1) both}
.cmp.bad .txt{animation:dim .4s ease both}
@keyframes dim{to{opacity:.45}}
.cmp.good{background:#2ee6a0;color:#0b0b0f;box-shadow:0 0 0 0 rgba(46,230,160,.6);animation:fromL .7s cubic-bezier(.16,1,.3,1) both,glow 1.6s ease-out both}
@keyframes glow{0%{box-shadow:0 0 0 0 rgba(46,230,160,.7)}100%{box-shadow:0 0 0 40px rgba(46,230,160,0)}}
.cmp.good .ic{background:#0b0b0f;color:#2ee6a0}
.shake{animation:shake .45s ease both}
@keyframes shake{0%,100%{transform:none}20%{transform:translateX(-14px)}40%{transform:translateX(12px)}60%{transform:translateX(-8px)}80%{transform:translateX(5px)}}
/* steps timeline */
.steps{position:relative;width:100%;padding:20px 0 20px 0;display:flex;flex-direction:column;gap:34px}
.rail{position:absolute;right:62px;top:60px;bottom:60px;width:6px;border-radius:4px;background:rgba(255,255,255,.18);overflow:hidden}
.rail i{display:block;width:100%;height:100%;background:linear-gradient(180deg,var(--a),var(--b));transform-origin:top;animation:railgrow linear both}
@keyframes railgrow{from{transform:scaleY(0)}to{transform:scaleY(1)}}
.st{position:relative;display:flex;align-items:center;gap:34px;text-align:right}
.st .nd{flex:none;width:130px;height:130px;border-radius:50%;display:grid;place-items:center;font-size:56px;font-weight:900;background:rgba(8,8,12,.85);border:5px solid var(--a);color:var(--a);z-index:1;animation:pop .6s cubic-bezier(.2,1.6,.4,1) both,ndfill .5s ease both;animation-delay:inherit}
@keyframes ndfill{0%,60%{background:rgba(8,8,12,.85);color:var(--a)}100%{background:var(--a);color:#0b0b0f}}
.st .bx{flex:1;padding:26px 36px;border-radius:28px}
.st small{display:block;font-size:34px;font-weight:700;color:var(--a);margin-bottom:4px}
.st b{display:block;font-size:56px;font-weight:900;line-height:1.3}
.steps-k{font-size:46px;font-weight:900;margin-bottom:40px;text-shadow:0 4px 20px rgba(0,0,0,.6)}
"""

ICON["arrowL"] = '<svg viewBox="0 0 24 24"><path d="M19 12H5M11 6l-6 6 6 6" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
FA = "۰۱۲۳۴۵۶۷۸۹"

def kwords(s, start, step=0.1, slam=False):
    """masked word reveal; [[x]] -> highlight sweep (inherits the word's delay)"""
    lines, i = [], 0
    for line in s.split("\n"):
        spans = []
        for p in re.findall(r"\[\[.+?\]\]|\S+", line):
            hl = p.startswith("[[")
            txt = esc(p[2:-2] if hl else p)
            dl = start + i * step
            inner = f'<mark style="animation-delay:{dl + 0.25:.3f}s">{txt}</mark>' if hl else txt
            spans.append(f'<span class="wm"><span class="w" style="animation-delay:{dl:.3f}s">{inner}</span></span>')
            i += 1
        lines.append(" ".join(spans))
    return "<br>".join(lines), i

def scene_html(sc, st, dur):
    d = lambda off: f"animation-delay:{st+off:.3f}s"
    t = sc["type"]
    if t == "hook":
        w, n = kwords(sc["title"], st + 0.1, 0.13, slam=True)
        body = f'<div class="hook-t slam">{w}</div>'
        if sc.get("sub"):
            body += f'<div class="pill rise" style="{d(0.3 + n*0.13)}">{esc(sc["sub"])}</div>'
    elif t == "point":
        mark = sc.get("mark") or ""
        badge = ICON[mark] if mark in ("bad", "good") else esc(sc["num"])
        kick = esc(sc["kicker"]) if sc.get("kicker") else ("اشتباه" if mark == "bad" else "قدم") + " " + esc(sc["num"])
        tw, n = kwords(sc["title"], st + 0.45, 0.09)
        body = (f'<div class="card gb flip" style="{d(0.0)}">'
                f'<div class="bw {mark} pop" style="{d(0.2)}"><svg class="ring" viewBox="0 0 170 170"><circle cx="85" cy="85" r="79" style="{d(0.25)}"/></svg>'
                f'<div class="badge">{badge}</div></div>'
                f'<div class="kicker rise" style="{d(0.3)}">{kick}</div>'
                f'<div class="p-t">{tw}</div>'
                f'<div class="p-s rise" style="{d(0.55 + n*0.09)}">{esc(sc["sub"])}</div>')
        if sc.get("chips"):
            body += '<div class="chips">' + "".join(
                f'<span class="chip pop" style="{d(1.0 + n*0.09 + i*0.2)}">{esc(c)}</span>' for i, c in enumerate(sc["chips"])) + "</div>"
        body += "</div>"
    elif t == "prompt":
        gap = min(1.25, max(0.6, (dur - 1.6) / max(1, len(sc["lines"]))))
        lines = "".join(f'<div class="ln type" style="{d(0.75 + i*gap)};--ty:{gap*0.85:.2f}s">{B2.rich(l)}</div>' for i, l in enumerate(sc["lines"]))
        body = (f'<div class="p-t sm rise" style="{d(0.0)}">{esc(sc["title"])}</div>'
                f'<div class="chat gb flip" style="{d(0.2)}"><div class="chat-h"><span class="dot"></span>'
                f'<span>پیام تو به هوش مصنوعی</span><i class="cp">{ICON["copy"]}</i></div>{lines}'
                f'<div class="send pop" style="{d(0.75 + len(sc["lines"])*gap)}"><b>{ICON["send"]} ارسال</b></div></div>')
    elif t == "compare":
        good_at = max(1.5, dur * 0.42)
        body = (f'<div class="kicker rise" style="{d(0.0)}">{esc(sc.get("kicker") or "مقایسه")}</div>'
                f'<div class="p-t">{kwords(sc["title"], st + 0.1, 0.1)[0]}</div>'
                f'<div class="fromR" style="{d(0.55)};width:100%"><div class="cmp bad shake" style="{d(good_at - 0.5)}"><i class="ic">{ICON["bad"]}</i>'
                f'<div class="txt" style="{d(good_at - 0.4)}">{esc(sc["bad"])}</div><span class="strike" style="{d(good_at - 0.45)}"></span></div></div>'
                f'<div class="cmp good" style="{d(good_at)}"><i class="ic">{ICON["good"]}</i><div>{esc(sc["good"])}</div></div>')
    elif t == "io":
        body = (f'<div class="kicker rise" style="{d(0.0)}">{esc(sc.get("kicker") or "مثال")}</div>'
                f'<div class="io-in fromR" style="{d(0.15)}"><div class="io-ic">{B3.ICON3[sc["icon"]]}</div>'
                f'<div><small>تو می‌فرستی</small><b>{esc(sc["inp"])}</b></div></div>'
                f'<div class="io-ar pop" style="{d(max(0.9, dur*0.35))}">{B3.ICON3["arrow"]}</div>'
                f'<div class="io-out fromL" style="{d(max(1.2, dur*0.45))}"><div class="io-ic">{B3.ICON3["spark"]}</div>'
                f'<div><small>جواب هوش مصنوعی</small><b>{esc(sc["out"])}</b></div></div>')
    elif t == "steps":
        n = len(sc["items"]); first = 0.5; span = max(1.0, dur - 1.4 - first)
        items = ""
        for i, (lab, txt) in enumerate(sc["items"]):
            at = first + span * i / max(1, n - 1)
            items += (f'<div class="st" style="{d(at)}"><div class="nd">{FA[i+1]}</div>'
                      f'<div class="bx gb fromL" style="{d(at + 0.05)}"><small>{esc(lab)}</small><b>{esc(txt)}</b></div></div>')
        body = (f'<div class="steps-k rise" style="{d(0.0)}">{esc(sc["kicker"])}</div>'
                f'<div class="steps"><div class="rail"><i style="{d(first)};animation-duration:{span:.2f}s"></i></div>{items}</div>')
    elif t == "cta":
        w, n = kwords(sc["title"], st + 0.35, 0.1)
        body = (f'<div class="prof pop" style="{d(0.0)}"><div class="av">{ICON["spark"]}</div><div class="hd" dir="ltr">{HANDLE}</div></div>'
                f'<div class="cta-t">{w}</div>'
                f'<div class="fw pop" style="{d(0.6 + n*0.1)}"><span class="rip"></span><span class="rip r2"></span><div class="follow">+ فالو</div></div>'
                f'<div class="acts rise" style="{d(0.85 + n*0.1)}"><i>{ICON["heart"]}</i><i>{ICON["send"]}</i><i>{ICON["save"]}</i></div>'
                f'<div class="p-s rise" style="{d(0.95 + n*0.1)}">{esc(sc["sub"])}</div>')
    else:
        raise ValueError(t)
    life = f"animation:enter .55s cubic-bezier(.16,1,.3,1) {st:.3f}s both,leave .32s ease-in {st+dur-0.32:.3f}s forwards"
    return f'<section class="scene {t}" style="{life}">{body}</section>'

def grade(src, d, out, i):
    N = max(1, int(d * FPS))
    z = f"1+0.09*on/{N}" if i % 2 == 0 else f"1.09-0.09*on/{N}"   # alternate push-in / pull-out
    vf = (f"fps={FPS},scale=1620:2880,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps={FPS},"
          f"eq=contrast=1.08:saturation=1.12:brightness=-0.03,format=yuv420p")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-stream_loop", "-1", "-i", src, "-t", f"{d:.3f}", "-vf", vf,
                    "-an", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", out], check=True)

def bg_track(spec, starts, ends, work):
    n = len(starts); total = ends[-1]; h = XF / 2
    ins, lens = [], []
    for i, sc in enumerate(spec["scenes"]):
        a = max(0.0, starts[i] - (h if i else 0)); b = min(total, ends[i] + (h if i < n - 1 else 0))
        out = os.path.join(work, f"bg{i}.mp4"); grade(os.path.join(STOCK, sc["bg"] + ".mp4"), b - a, out, i)
        ins += ["-i", out]; lens.append(b - a)
    fc, prev = [], "0:v"
    for k in range(1, n):
        lab = f"x{k}"
        fc.append(f"[{prev}][{k}:v]xfade=transition={XFADES[(k-1) % len(XFADES)]}:duration={XF}:offset={starts[k]-h:.3f}[{lab}]")
        prev = lab
    bg = os.path.join(work, "bg.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", f"[{prev}]",
                    "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", bg], check=True)
    return bg

def run(key, voice_mp3, specfile="scripts7.json"):
    spec = json.load(open(os.path.join(ROOT, specfile)))[key]
    bounds, s0, s1, vdur = boundaries(voice_mp3, [sc["voice"] for sc in spec["scenes"]])
    total = LEAD + vdur + TAIL
    starts = [0.0] + [LEAD + b for b in bounds]
    ends = starts[1:] + [total]
    work = os.path.join(ROOT, "out", key + "_v5"); os.makedirs(work, exist_ok=True)
    scenes = "".join(scene_html(sc, st, en - st) for sc, st, en in zip(spec["scenes"], starts, ends))
    wipes = "".join(f'<div class="wipe" style="animation-delay:{st-0.25:.3f}s"></div>' for st in starts[1:])
    segs = "".join(f'<div class="seg"><i style="animation-duration:{en-st:.3f}s;animation-delay:{st:.3f}s"></i></div>' for st, en in zip(starts, ends))
    page = f"""<!doctype html><html lang="fa"><head><meta charset="utf-8"><style>{CSS}</style></head>
<body style="--a:{spec['accent']};--b:{spec['accent2']}"><div class="shade"></div><div class="leak l1"></div><div class="leak l2"></div>
<div class="segs">{segs}</div><div class="head"><div class="tag">{esc(spec['tag'])}</div><div class="me" dir="ltr"><span class="mini">{ICON['spark']}</span>{HANDLE}</div></div>
{scenes}{wipes}</body></html>"""
    hp = os.path.join(ROOT, f"_{key}_v5.html"); open(hp, "w").write(page)
    only = os.environ.get("FRAMES")
    bg = os.path.join(work, "bg.mp4")
    if not (only and os.path.exists(bg) and os.environ.get("KEEPBG")):
        bg = bg_track(spec, starts, ends, work)
    seek = "ms=>document.getAnimations().forEach(a=>{a.pause();a.currentTime=ms})"
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H})
        pg.goto("file://" + hp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
        if only:
            for s in only.split(","):
                pg.evaluate(seek, float(s) * 1000)
                ov = os.path.join(work, f"ov_{s}.png"); pg.screenshot(path=ov, omit_background=True)
                subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", s, "-i", bg, "-i", ov, "-filter_complex", "[0:v][1:v]overlay", "-frames:v", "1",
                                os.path.join(work, f"still_{s}.jpg")], check=True)
            b.close(); print("stills", work, [round(x, 2) for x in starts]); return
        silent = os.path.join(work, "silent.mp4")
        ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-i", bg, "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-",
                               "-filter_complex", "[0:v][1:v]overlay=shortest=1,format=yuv420p", "-c:v", "libx264", "-crf", "18", "-preset", "medium", silent],
                              stdin=subprocess.PIPE)
        for f in range(int(total * FPS)):
            pg.evaluate(seek, f * 1000 / FPS)
            ff.stdin.write(pg.screenshot(type="png", omit_background=True))
        b.close()
    ff.stdin.close(); ff.wait()
    music(total, os.path.join(work, "music.wav"), seed=len(key) + 31)
    sfx(total, starts, os.path.join(work, "sfx.wav"))
    out = os.path.join(ROOT, "out", key + ".mp4")
    L = int(LEAD * 1000)
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", silent, "-i", voice_mp3, "-i", os.path.join(work, "music.wav"), "-i", os.path.join(work, "sfx.wav"),
                    "-filter_complex", f"[1:a]adelay={L}|{L},aresample=44100[v];[2:a]volume=0.09,aresample=44100[m];[3:a]volume=0.12,aresample=44100[s];[v][m][s]amix=inputs=3:duration=longest:normalize=0,loudnorm=I=-14:TP=-1[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(key, f"{total:.1f}s", [round(s, 2) for s in starts], out)

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], *(sys.argv[3:4]))
