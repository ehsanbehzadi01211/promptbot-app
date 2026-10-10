"""V4 cinematic theme: Adobe Stock footage per scene + transparent motion-graphics overlay.
Usage: python3 build4.py <key> <voice.mp3>   (FRAMES=1,2 -> debug stills composited on footage)"""
import json, os, subprocess, sys
from playwright.sync_api import sync_playwright
from align import boundaries
from build import music, W, H, FPS
import build2 as B2
import build3 as B3
from build2 import esc, ICON, HANDLE, LEAD, TAIL, sfx

ROOT = os.path.dirname(os.path.abspath(__file__))
STOCK = "/home/claude/reels-media/stock"

CSS = B2.FONTS + """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:transparent;font-family:V,sans-serif;color:#fff}
.shade{position:absolute;inset:0;background:
 linear-gradient(180deg,rgba(0,0,0,.72) 0%,rgba(0,0,0,.15) 22%,rgba(0,0,0,.25) 55%,rgba(0,0,0,.82) 100%),
 radial-gradient(ellipse at 50% 45%,rgba(0,0,0,.05) 0%,rgba(0,0,0,.45) 100%)}
.flash{position:absolute;inset:0;background:#fff;opacity:0;animation:flash .28s ease-out forwards}
@keyframes flash{0%{opacity:.35}100%{opacity:0}}
.segs{position:absolute;top:66px;left:60px;right:60px;display:flex;gap:10px;direction:rtl}
.seg{flex:1;height:7px;border-radius:6px;background:rgba(255,255,255,.3);overflow:hidden}
.seg i{display:block;height:100%;background:#fff;transform-origin:right;animation:segfill linear both}
@keyframes segfill{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.head{position:absolute;top:104px;left:60px;right:60px;display:flex;justify-content:space-between;align-items:center;direction:rtl}
.tag{font-size:34px;font-weight:900;padding:10px 26px;border-radius:12px;background:var(--a);color:#0b0b0f;letter-spacing:.5px}
.me{display:flex;align-items:center;gap:14px;font-size:34px;font-weight:700;text-shadow:0 2px 14px rgba(0,0,0,.6)}
.me .mini{width:54px;height:54px;border-radius:50%;background:var(--a);display:grid;place-items:center;color:#0b0b0f}
.me .mini svg{width:28px;height:28px}
.scene{position:absolute;left:0;right:0;top:240px;bottom:360px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:0 70px;direction:rtl}
@keyframes life{0%{opacity:0;transform:scale(1.12)}5%{opacity:1;transform:none}94%{opacity:1;transform:none}100%{opacity:0;transform:scale(.96)}}
mark{color:#0b0b0f;background:var(--a);padding:0 18px;border-radius:10px;box-decoration-break:clone;-webkit-box-decoration-break:clone;text-shadow:none}
.w{display:inline-block;animation:wpop .42s cubic-bezier(.2,1.3,.3,1) both}
@keyframes wpop{from{opacity:0;transform:translateY(60px) scale(1.25);filter:blur(12px)}to{opacity:1;transform:none;filter:none}}
.rise{animation:rise .55s cubic-bezier(.2,.9,.2,1) both}
@keyframes rise{from{opacity:0;transform:translateY(50px)}to{opacity:1;transform:none}}
.pop{animation:pop .5s cubic-bezier(.2,1.5,.4,1) both}
@keyframes pop{from{opacity:0;transform:scale(.4)}to{opacity:1;transform:none}}
.tilt,.tilt2{animation:rise .55s cubic-bezier(.2,.9,.2,1) both}
.hook-t{font-size:122px;font-weight:900;line-height:1.36;text-shadow:0 8px 40px rgba(0,0,0,.7)}
.pill{margin-top:56px;font-size:46px;font-weight:700;padding:16px 40px;border-radius:14px;background:rgba(0,0,0,.55);border-right:10px solid var(--a)}
.card{width:100%;padding:70px 56px 64px;border-radius:40px;background:rgba(8,8,12,.62);border:2px solid rgba(255,255,255,.16);display:flex;flex-direction:column;align-items:center;box-shadow:0 40px 100px rgba(0,0,0,.45)}
.badge{width:150px;height:150px;border-radius:50%;display:grid;place-items:center;font-size:88px;font-weight:900;color:#0b0b0f;background:var(--a);margin-bottom:28px;box-shadow:0 0 0 14px rgba(255,255,255,.08)}
.badge svg{width:84px;height:84px}
.badge.bad{background:#ff4d5e;color:#fff}
.badge.good{background:#2ee6a0}
.kicker{font-size:36px;font-weight:700;letter-spacing:1px;color:var(--a);margin-bottom:16px}
.p-t{font-size:90px;font-weight:900;line-height:1.34;text-shadow:0 6px 30px rgba(0,0,0,.5)}
.p-t.sm{font-size:68px;margin-bottom:46px}
.p-s{margin-top:28px;font-size:46px;font-weight:700;line-height:1.5;opacity:.9}
.chips{margin-top:46px;display:flex;flex-wrap:wrap;justify-content:center;gap:20px}
.chip{font-size:44px;font-weight:900;padding:14px 34px;border-radius:14px;background:var(--a);color:#0b0b0f}
.chat{width:100%;text-align:right;border-radius:34px;background:rgba(8,8,12,.75);border:2px solid rgba(255,255,255,.18);overflow:hidden;padding-bottom:34px}
.chat-h{display:flex;align-items:center;gap:16px;padding:24px 40px;font-size:34px;font-weight:700;background:rgba(255,255,255,.08);margin-bottom:22px}
.chat-h .dot{width:18px;height:18px;border-radius:50%;background:var(--a)}
.chat-h .cp{margin-right:auto;width:44px;height:44px}
.ln{font-size:54px;font-weight:700;line-height:1.6;padding:6px 44px}
.ln mark{padding:0 10px}
.type{animation:typer var(--ty) steps(18) both}
@keyframes typer{from{clip-path:inset(0 0 0 100%)}to{clip-path:inset(0 0 0 0)}}
.prof{display:flex;flex-direction:column;align-items:center;gap:16px;margin-bottom:44px}
.av{width:190px;height:190px;border-radius:50%;display:grid;place-items:center;background:rgba(0,0,0,.5);border:8px solid var(--a)}
.av svg{width:92px;height:92px;color:var(--a)}
.hd{font-size:46px;font-weight:900;text-shadow:0 2px 14px rgba(0,0,0,.6)}
.cta-t{font-size:86px;font-weight:900;line-height:1.42;text-shadow:0 6px 30px rgba(0,0,0,.6)}
.follow{margin-top:56px;font-size:58px;font-weight:900;padding:24px 110px;border-radius:20px;color:#0b0b0f;background:var(--a);animation:pop .5s cubic-bezier(.2,1.5,.4,1) both,pulse 1.2s ease-in-out 0s infinite}
@keyframes pulse{50%{transform:scale(1.06)}}
.acts{margin-top:46px;display:flex;gap:56px}
.acts i{width:76px;height:76px;filter:drop-shadow(0 2px 10px rgba(0,0,0,.6))}
.io-in,.io-out{width:100%;display:flex;align-items:center;gap:32px;text-align:right;padding:38px 42px;border-radius:32px;position:relative}
.io-in{background:rgba(8,8,12,.7);border:2px solid rgba(255,255,255,.2)}
.io-out{background:var(--a);color:#0b0b0f}
.io-ic{flex:none;width:124px;height:124px;border-radius:28px;display:grid;place-items:center;background:rgba(255,255,255,.12)}
.io-out .io-ic{background:rgba(0,0,0,.12)}
.io-ic svg{width:78px;height:78px}
.io-in small,.io-out small{display:block;font-size:34px;font-weight:700;opacity:.75;margin-bottom:6px}
.io-in b,.io-out b{display:block;font-size:56px;font-weight:900;line-height:1.35}
.cam{display:none}
.io-ar{width:100px;height:100px;margin:26px 0;padding:16px;border-radius:50%;background:#fff;color:#0b0b0f}
.io .kicker{margin-bottom:46px;font-size:40px}
.cmp{width:100%;display:flex;gap:26px;align-items:center;text-align:right;margin-top:40px;padding:40px 42px;border-radius:30px;font-size:50px;font-weight:700;line-height:1.55}
.cmp .ic{flex:none;width:90px;height:90px;border-radius:50%;display:grid;place-items:center}
.cmp .ic svg{width:52px;height:52px}
.cmp.bad{background:rgba(8,8,12,.7);border:2px solid rgba(255,77,94,.7);color:rgba(255,255,255,.8)}
.cmp.bad .ic{background:#ff4d5e;color:#fff}
.cmp.good{background:#2ee6a0;color:#0b0b0f}
.cmp.good .ic{background:#0b0b0f;color:#2ee6a0}
.compare .kicker{margin-bottom:10px}
.sent{font-size:76px;font-weight:900;padding:36px 48px;border-radius:30px;background:rgba(8,8,12,.7);border:2px solid rgba(255,255,255,.2)}
.guess{display:inline-block;color:var(--a)}
.caret{display:inline-block;width:8px;height:74px;background:#fff;margin-right:10px;vertical-align:-10px;animation:blink 1s steps(1) 0s infinite}
@keyframes blink{50%{opacity:0}}
.opts{width:100%;margin-top:54px;display:flex;flex-direction:column;gap:28px;padding:36px 40px;border-radius:30px;background:rgba(8,8,12,.6)}
.opt{display:flex;align-items:center;gap:28px;font-size:52px;font-weight:700}
.opt .ow{width:170px;text-align:right}
.opt .track{flex:1;height:50px;border-radius:26px;background:rgba(255,255,255,.12);overflow:hidden}
.opt .fill{display:block;height:100%;width:var(--w);border-radius:26px;background:rgba(255,255,255,.45);transform-origin:right;animation:grow .9s cubic-bezier(.2,.8,.2,1) both}
.opt.top .fill{background:var(--a)}
.opt b{width:130px;text-align:left;font-weight:900}
.opt.top b,.opt.top .ow{color:var(--a)}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.note{margin-top:30px;font-size:34px;opacity:.7}
"""

def bg_track(spec, starts, ends, work):
    parts = []
    for i, (sc, st, en) in enumerate(zip(spec["scenes"], starts, ends)):
        src = os.path.join(STOCK, sc["bg"] + ".mp4"); out = os.path.join(work, f"bg{i}.mp4")
        d = en - st
        # gentle push-in + grade per scene
        vf = (f"scale=1188:2112,crop=1080:1920:(iw-1080)/2*(1-t/{d:.3f})+0*(t/{d:.3f}):(ih-1920)/2,"
              f"eq=contrast=1.08:saturation=1.12:brightness=-0.03,fps={FPS}")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-stream_loop", "-1", "-i", src, "-t", f"{d:.3f}", "-vf", vf,
                        "-an", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", out], check=True)
        parts.append(out)
    lst = os.path.join(work, "bg.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    bg = os.path.join(work, "bg.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", bg], check=True)
    return bg

def run(key, voice_mp3, specfile="scripts3.json"):
    spec = json.load(open(os.path.join(ROOT, specfile)))[key]
    bounds, s0, s1, vdur = boundaries(voice_mp3, [sc["voice"] for sc in spec["scenes"]])
    total = LEAD + vdur + TAIL
    starts = [0.0] + [LEAD + b for b in bounds]
    ends = starts[1:] + [total]
    work = os.path.join(ROOT, "out", key + "_v4"); os.makedirs(work, exist_ok=True)
    scenes = "".join(B3.scene_html(sc, st, en - st) for sc, st, en in zip(spec["scenes"], starts, ends))
    flashes = "".join(f'<div class="flash" style="animation-delay:{st:.3f}s"></div>' for st in starts[1:])
    segs = "".join(f'<div class="seg"><i style="animation-duration:{en-st:.3f}s;animation-delay:{st:.3f}s"></i></div>' for st, en in zip(starts, ends))
    page = f"""<!doctype html><html lang="fa"><head><meta charset="utf-8"><style>{CSS}</style></head>
<body style="--a:{spec['accent']};--b:{spec['accent2']}"><div class="shade"></div>{flashes}
<div class="segs">{segs}</div><div class="head"><div class="tag">{esc(spec['tag'])}</div><div class="me" dir="ltr"><span class="mini">{ICON['spark']}</span>{HANDLE}</div></div>
{scenes}</body></html>"""
    hp = os.path.join(ROOT, f"_{key}_v4.html"); open(hp, "w").write(page)
    bg = bg_track(spec, starts, ends, work)
    seek = "ms=>document.getAnimations().forEach(a=>{a.pause();a.currentTime=ms})"
    only = os.environ.get("FRAMES")
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H})
        pg.goto("file://" + hp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
        if only:
            for s in only.split(","):
                pg.evaluate(seek, float(s) * 1000)
                ov = os.path.join(work, f"ov_{s}.png"); pg.screenshot(path=ov, omit_background=True)
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", s, "-i", bg, "-i", ov, "-filter_complex", "[0:v][1:v]overlay", "-frames:v", "1",
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
    music(total, os.path.join(work, "music.wav"), seed=len(key) + 21)
    sfx(total, starts, os.path.join(work, "sfx.wav"))
    out = os.path.join(ROOT, "out", key + ".mp4")
    L = int(LEAD * 1000)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", voice_mp3, "-i", os.path.join(work, "music.wav"), "-i", os.path.join(work, "sfx.wav"),
                    "-filter_complex", f"[1:a]adelay={L}|{L},aresample=44100[v];[2:a]volume=0.09,aresample=44100[m];[3:a]volume=0.12,aresample=44100[s];[v][m][s]amix=inputs=3:duration=longest:normalize=0,loudnorm=I=-14:TP=-1[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(key, f"{total:.1f}s", [round(s, 2) for s in starts], out)

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], *(sys.argv[3:4]))
