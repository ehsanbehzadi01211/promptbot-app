"""V3 theme: bright neo-brutalist (cream paper, thick black outlines, hard shadows, sticker colours).
Usage: python3 build3.py <key> <voice.mp3>   (FRAMES=1,2,3 for debug stills)"""
import json, os, subprocess, sys
import numpy as np
from playwright.sync_api import sync_playwright
from align import boundaries
from build import music, W, H, FPS
import build2 as B2
from build2 import esc, ICON, HANDLE, LEAD, TAIL, sfx

ROOT = os.path.dirname(os.path.abspath(__file__))

ICON3 = dict(ICON)
ICON3.update({
    "fridge": '<svg viewBox="0 0 24 24"><rect x="6" y="2.5" width="12" height="19" rx="2.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M6 10h12M9 5.5v2M9 13v3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    "error": '<svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="13" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M9 21h6M12 17v4M12 7.5v4M12 14v.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    "menu": '<svg viewBox="0 0 24 24"><path d="M6 2.5h12v19H6z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M9 7h6M9 11h6M9 15h4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    "camera": '<svg viewBox="0 0 24 24"><path d="M4 7h3l2-3h6l2 3h3v12H4z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><circle cx="12" cy="13" r="3.5" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24"><path d="M12 4v15M6 13l6 6 6-6" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>',
})

def scene_html(sc, st, dur):
    if sc["type"] != "io":
        return B2.scene_html(sc, st, dur)
    d = lambda off: f"animation-delay:{st+off:.3f}s"
    body = (f'<div class="kicker rise" style="{d(0.0)}">{esc(sc["kicker"]) if sc.get("kicker") else "کاربرد " + esc(sc["num"])}</div>'
            f'<div class="io-in tilt" style="{d(0.15)}"><div class="io-ic">{ICON3[sc["icon"]]}</div>'
            f'<div><small>تو می‌فرستی</small><b>{esc(sc["inp"])}</b></div><i class="cam">{ICON3["camera"]}</i></div>'
            f'<div class="io-ar pop" style="{d(max(0.9, dur*0.35))}">{ICON3["arrow"]}</div>'
            f'<div class="io-out tilt2" style="{d(max(1.2, dur*0.45))}"><div class="io-ic">{ICON3["spark"]}</div>'
            f'<div><small>جواب هوش مصنوعی</small><b>{esc(sc["out"])}</b></div></div>')
    return f'<section class="scene io" style="animation:life {dur:.3f}s linear {st:.3f}s both">{body}</section>'

CSS = B2.FONTS + """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#f4efe3;font-family:V,sans-serif;color:#111}
:root{--k:#111;--bd:6px solid #111}
.bg{position:absolute;inset:0;overflow:hidden;background:radial-gradient(#111 2.2px,transparent 2.6px) 0 0/44px 44px;opacity:1}
.bg::after{content:"";position:absolute;inset:0;background:#f4efe3;opacity:.86}
.shape{position:absolute;border:6px solid #111;z-index:1;animation:bob 6s ease-in-out 0s infinite alternate}
.s1{width:230px;height:230px;border-radius:50%;background:var(--a);top:330px;left:-80px}
.s2{width:170px;height:170px;background:var(--b);top:1250px;right:-50px;transform:rotate(14deg);border-radius:28px;animation-duration:7s}
.s3{width:120px;height:120px;background:#fff;top:1500px;left:70px;border-radius:50%;animation-duration:5s}
.s4{width:90px;height:90px;background:var(--a);top:420px;right:40px;transform:rotate(-12deg);border-radius:18px;animation-duration:8s}
@keyframes bob{to{translate:0 -40px;rotate:12deg}}
.tape{position:absolute;left:-60px;right:-60px;top:1640px;height:96px;background:#111;color:#f4efe3;transform:rotate(-4deg);overflow:hidden;z-index:2;border-top:6px solid var(--a);border-bottom:6px solid var(--a)}
.tape div{position:absolute;top:14px;white-space:nowrap;font-size:46px;font-weight:900;animation:marq 14s linear 0s infinite;direction:rtl}
@keyframes marq{from{transform:translateX(-50%)}to{transform:translateX(0)}}
.segs{position:absolute;top:70px;left:70px;right:70px;display:flex;gap:10px;direction:rtl;z-index:5}
.seg{flex:1;height:12px;border-radius:8px;background:#fff;border:3px solid #111;overflow:hidden}
.seg i{display:block;height:100%;background:#111;transform-origin:right;animation:segfill linear both}
@keyframes segfill{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.head{position:absolute;top:118px;left:70px;right:70px;display:flex;justify-content:space-between;align-items:center;direction:rtl;z-index:5}
.tag{font-size:34px;font-weight:900;padding:12px 28px;border-radius:40px;background:var(--a);border:5px solid #111;box-shadow:5px 5px 0 #111}
.me{display:flex;align-items:center;gap:14px;font-size:32px;font-weight:900;padding:8px 22px 8px 10px;background:#fff;border:5px solid #111;border-radius:40px;box-shadow:5px 5px 0 #111}
.me .mini{width:46px;height:46px;border-radius:50%;background:var(--b);border:4px solid #111;display:grid;place-items:center}
.me .mini svg{width:24px;height:24px}
.scene{position:absolute;left:0;right:0;top:250px;bottom:380px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:0 80px;direction:rtl;z-index:4}
@keyframes life{0%{opacity:0;transform:translateX(-140px) rotate(-4deg)}6%{opacity:1;transform:none}92%{opacity:1;transform:none}100%{opacity:0;transform:translateX(160px) rotate(4deg)}}
mark{color:#111;background:var(--a);padding:0 20px;border:6px solid #111;border-radius:22px;box-shadow:8px 8px 0 #111;display:inline-block;transform:rotate(-2deg);margin:8px 0}
.w{display:inline-block;animation:wpop .45s cubic-bezier(.3,1.6,.4,1) both}
@keyframes wpop{from{opacity:0;transform:scale(.2) rotate(-12deg)}to{opacity:1;transform:none}}
.rise{animation:rise .5s cubic-bezier(.3,1.4,.4,1) both}
@keyframes rise{from{opacity:0;transform:translateY(70px)}to{opacity:1;transform:none}}
.pop{animation:pop .5s cubic-bezier(.3,1.7,.4,1) both}
@keyframes pop{from{opacity:0;transform:scale(.3) rotate(10deg)}to{opacity:1;transform:none}}
.tilt{animation:tin .55s cubic-bezier(.3,1.5,.4,1) both;transform:rotate(-2deg)}
.tilt2{animation:tin2 .55s cubic-bezier(.3,1.5,.4,1) both;transform:rotate(2deg)}
@keyframes tin{from{opacity:0;transform:translateX(200px) rotate(-10deg)}to{opacity:1;transform:rotate(-2deg)}}
@keyframes tin2{from{opacity:0;transform:translateX(-200px) rotate(10deg)}to{opacity:1;transform:rotate(2deg)}}
.hook-t{font-size:116px;font-weight:900;line-height:1.42}
.pill{margin-top:64px;font-size:46px;font-weight:900;padding:20px 44px;border-radius:60px;background:#fff;border:6px solid #111;box-shadow:8px 8px 0 #111}
.card{width:100%;padding:76px 60px 70px;border-radius:44px;background:#fff;border:7px solid #111;box-shadow:18px 18px 0 #111;display:flex;flex-direction:column;align-items:center;transform:rotate(-1deg)}
.badge{width:160px;height:160px;border-radius:50%;display:grid;place-items:center;font-size:92px;font-weight:900;color:#111;background:var(--a);border:7px solid #111;box-shadow:8px 8px 0 #111;margin-bottom:30px}
.badge svg{width:90px;height:90px}
.badge.bad{background:#ff5d5d}
.badge.good{background:#3ddc97}
.kicker{display:inline-block;font-size:36px;font-weight:900;padding:6px 26px;margin-bottom:22px;background:#111;color:#f4efe3;border-radius:14px}
.p-t{font-size:90px;font-weight:900;line-height:1.35}
.p-t.sm{font-size:68px;margin-bottom:54px}
.p-s{margin-top:30px;font-size:46px;font-weight:700;line-height:1.5;color:#333}
.chips{margin-top:48px;display:flex;flex-wrap:wrap;justify-content:center;gap:24px}
.chip{font-size:44px;font-weight:900;padding:16px 36px;border-radius:22px;background:var(--b);border:5px solid #111;box-shadow:6px 6px 0 #111}
.chip:nth-child(2n){background:var(--a)}
.chat{width:100%;text-align:right;border-radius:36px;background:#fff;border:7px solid #111;box-shadow:16px 16px 0 #111;overflow:hidden;padding-bottom:36px}
.chat-h{display:flex;align-items:center;gap:18px;padding:26px 40px;font-size:36px;font-weight:900;background:var(--a);border-bottom:6px solid #111;margin-bottom:24px}
.chat-h .dot{width:22px;height:22px;border-radius:50%;background:#111}
.chat-h .cp{margin-right:auto;width:48px;height:48px}
.ln{font-size:54px;font-weight:700;line-height:1.6;padding:6px 44px}
.ln mark{padding:0 12px;border-width:4px;box-shadow:4px 4px 0 #111;border-radius:12px;margin:0;background:var(--b)}
.type{animation:typer var(--ty) steps(18) both}
@keyframes typer{from{clip-path:inset(0 0 0 100%)}to{clip-path:inset(0 0 0 0)}}
.prof{display:flex;flex-direction:column;align-items:center;gap:18px;margin-bottom:46px}
.av{width:190px;height:190px;border-radius:50%;display:grid;place-items:center;background:var(--b);border:7px solid #111;box-shadow:10px 10px 0 #111}
.av svg{width:96px;height:96px}
.hd{font-size:46px;font-weight:900}
.cta-t{font-size:84px;font-weight:900;line-height:1.45}
.follow{margin-top:60px;font-size:58px;font-weight:900;padding:24px 110px;border-radius:28px;color:#f4efe3;background:#111;border:6px solid #111;box-shadow:10px 10px 0 var(--a);animation:pop .5s cubic-bezier(.3,1.7,.4,1) both,wig 1.4s ease-in-out 0s infinite}
@keyframes wig{0%,100%{rotate:0deg}50%{rotate:-3deg}}
.acts{margin-top:50px;display:flex;gap:40px}
.acts i{width:110px;height:110px;padding:20px;background:#fff;border:5px solid #111;border-radius:50%;box-shadow:6px 6px 0 #111}
.cta .p-s{font-size:42px}
.io-in,.io-out{width:100%;display:flex;align-items:center;gap:34px;text-align:right;padding:40px 44px;border-radius:36px;border:7px solid #111;box-shadow:14px 14px 0 #111;position:relative}
.io-in{background:#fff}
.io-out{background:var(--a)}
.io-ic{flex:none;width:130px;height:130px;border-radius:30px;display:grid;place-items:center;background:var(--b);border:6px solid #111}
.io-out .io-ic{background:#fff}
.io-ic svg{width:80px;height:80px}
.io-in small,.io-out small{display:block;font-size:34px;font-weight:700;opacity:.7;margin-bottom:6px}
.io-in b,.io-out b{display:block;font-size:56px;font-weight:900;line-height:1.35}
.cam{position:absolute;top:-34px;left:34px;width:84px;height:84px;padding:14px;border-radius:50%;background:#111;color:#f4efe3}
.io-ar{width:110px;height:110px;margin:30px 0;padding:18px;border-radius:50%;background:#111;color:#f4efe3}
.io .kicker{margin-bottom:56px}
"""

def run(key, voice_mp3, specfile="scripts3.json"):
    spec = json.load(open(os.path.join(ROOT, specfile)))[key]
    bounds, s0, s1, vdur = boundaries(voice_mp3, [sc["voice"] for sc in spec["scenes"]])
    total = LEAD + vdur + TAIL
    starts = [0.0] + [LEAD + b for b in bounds]
    ends = starts[1:] + [total]
    work = os.path.join(ROOT, "out", key + "_v3"); os.makedirs(work, exist_ok=True)
    music(total, os.path.join(work, "music.wav"), seed=len(key) + 11)
    sfx(total, starts, os.path.join(work, "sfx.wav"))
    scenes = "".join(scene_html(sc, st, en - st) for sc, st, en in zip(spec["scenes"], starts, ends))
    segs = "".join(f'<div class="seg"><i style="animation-duration:{en-st:.3f}s;animation-delay:{st:.3f}s"></i></div>' for st, en in zip(starts, ends))
    tape_txt = (" \u2066" + HANDLE + "\u2069 ✦ هوش مصنوعی به زبان ساده ✦ ") * 8
    page = f"""<!doctype html><html lang="fa"><head><meta charset="utf-8"><style>{CSS}</style></head>
<body style="--a:{spec['accent']};--b:{spec['accent2']}"><div class="bg"></div>
<div class="shape s1"></div><div class="shape s2"></div><div class="shape s3"></div><div class="shape s4"></div>
<div class="tape"><div>{esc(tape_txt)}{esc(tape_txt)}</div></div>
<div class="segs">{segs}</div><div class="head"><div class="tag">{esc(spec['tag'])}</div><div class="me" dir="ltr"><span class="mini">{ICON['spark']}</span>{HANDLE}</div></div>
{scenes}</body></html>"""
    hp = os.path.join(ROOT, f"_{key}_v3.html"); open(hp, "w").write(page)
    only = os.environ.get("FRAMES")
    silent = os.path.join(work, "silent.mp4")
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H})
        pg.goto("file://" + hp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
        seek = "ms=>document.getAnimations().forEach(a=>{a.pause();a.currentTime=ms})"
        if only:
            for s in only.split(","):
                pg.evaluate(seek, float(s) * 1000); pg.screenshot(path=os.path.join(work, f"still_{s}.png"))
            b.close(); print("stills", work, [round(x, 2) for x in starts]); return
        ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                               "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", silent], stdin=subprocess.PIPE)
        for f in range(int(total * FPS)):
            pg.evaluate(seek, f * 1000 / FPS)
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
