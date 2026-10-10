"""Story teaser for a reel: the first seconds of the real video, shown as a card on its own blurred
backdrop, with a 'new reel' sticker. Usage: python3 teaser.py <key>:<colour>:<src.mp4> ..."""
import os, sys, subprocess
from playwright.sync_api import sync_playwright
import build2 as B2
ROOT = os.path.dirname(os.path.abspath(__file__))
CSS = B2.FONTS + """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;background:transparent;font-family:V,sans-serif;direction:rtl}
.frame{position:absolute;left:132px;top:262px;width:816px;height:1438px;border:8px solid var(--c);border-radius:40px;box-shadow:0 0 0 2000px rgba(0,0,0,.28)}
.new{position:absolute;top:214px;right:92px;font-size:78px;font-weight:900;color:#0b0b0f;background:var(--c);padding:4px 40px 14px;border-radius:22px;transform:rotate(4deg);box-shadow:0 18px 44px rgba(0,0,0,.5)}
.go{position:absolute;left:0;right:0;top:1640px;text-align:center}
.go span{display:inline-block;font-size:56px;font-weight:900;color:#fff;background:#0b0b0f;border:5px solid var(--c);padding:10px 48px 18px;border-radius:70px}
"""
def main(items):
    os.makedirs(os.path.join(ROOT, "stories"), exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        for it in items:
            key, col, src = it.split(":")
            hp = os.path.join(ROOT, f"_teaser_{key}.html")
            open(hp, "w").write(f'<!doctype html><html lang="fa"><head><meta charset="utf-8"><style>{CSS}</style></head>'
                                f'<body style="--c:#{col}"><div class="frame"></div><div class="new">ریل جدید</div>'
                                f'<div class="go"><span>کاملش توی پیج</span></div></body></html>')
            pg.goto("file://" + hp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
            ov = os.path.join(ROOT, "stories", f"_ov_{key}.png"); pg.screenshot(path=ov, omit_background=True)
            out = os.path.join(ROOT, "stories", f"teaser_{key}.mp4")
            fc = ("[0:v]split[a][b];[a]scale=1080:1920,gblur=sigma=40,eq=brightness=-0.12[bg];"
                  "[b]scale=800:1422[fg];[bg][fg]overlay=140:270[v0];[v0][1:v]overlay=0:0,fade=t=out:st=6.5:d=0.5,format=yuv420p[v];"
                  "[0:a]afade=t=out:st=6.2:d=0.8[a]")
            subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-t", "7", "-i", src, "-i", ov, "-filter_complex", fc,
                            "-map", "[v]", "-map", "[a]", "-t", "7", "-c:v", "libx264", "-crf", "20", "-preset", "veryfast",
                            "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out], check=True)
            print("ok", key)
        b.close()
if __name__ == "__main__":
    main(sys.argv[1:])
