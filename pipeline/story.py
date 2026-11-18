"""Instagram story announcing a new reel: the reel's own cover as a tilted card, so followers
recognise it in the grid. Usage: python3 story.py <key> [<key> ...]  ->  stories/story_<key>.jpg"""
import os, sys
from playwright.sync_api import sync_playwright
import build2 as B2
import cover as C

ROOT = os.path.dirname(os.path.abspath(__file__))
CSS = B2.FONTS + """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;font-family:V,sans-serif;color:#fff;background:#07070a}
.bg{position:absolute;inset:-80px;background-size:cover;background-position:center;filter:blur(46px) brightness(.34) saturate(1.2)}
.top{position:absolute;top:270px;left:0;right:0;text-align:center;direction:rtl}
.new{display:inline-block;font-size:124px;font-weight:900;line-height:1.25;color:#0b0b0f;background:var(--c);padding:0 46px 12px;border-radius:26px;transform:rotate(-3deg)}
.card{position:absolute;left:50%;top:560px;width:560px;height:996px;margin-left:-280px;border-radius:44px;overflow:hidden;transform:rotate(4deg);
 box-shadow:0 60px 120px rgba(0,0,0,.65),0 0 0 8px var(--c)}
.card img{width:100%;height:100%;object-fit:cover;display:block}
.play{position:absolute;left:50%;top:1345px;width:120px;height:120px;margin-left:-90px;border-radius:50%;background:rgba(8,8,12,.72);border:6px solid #fff;display:grid;place-items:center;transform:rotate(4deg)}
.play::after{content:"";border-left:40px solid #fff;border-top:25px solid transparent;border-bottom:25px solid transparent;margin-left:11px}
.foot{position:absolute;left:0;right:0;top:1600px;text-align:center;direction:rtl;font-size:58px;font-weight:900;line-height:1.5}
.foot small{display:block;font-size:42px;font-weight:700;opacity:.85;direction:ltr}
"""

def main(keys):
    os.makedirs(os.path.join(ROOT, "stories"), exist_ok=True)
    rows = {c[0]: c[4] for c in C.COVERS}
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        for key in keys:
            cov = "file://" + os.path.join(ROOT, "covers", f"cover_{key}.jpg")
            page = f"""<!doctype html><html lang="fa"><head><meta charset="utf-8"><style>{CSS}</style></head>
<body style="--c:{C.ROWS[rows[key]]}"><div class="bg" style="background-image:url('{cov}')"></div>
<div class="top"><span class="new">ریل جدید</span></div>
<div class="card"><img src="{cov}"></div><div class="play"></div>
<div class="foot">همین الان توی پیج ببین<small>@ehbehzad</small></div></body></html>"""
            hp = os.path.join(ROOT, "stories", f"_{key}.html"); open(hp, "w").write(page)
            pg.goto("file://" + hp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
            pg.screenshot(path=os.path.join(ROOT, "stories", f"story_{key}.jpg"), type="jpeg", quality=92)
            print("ok", key)
        b.close()

if __name__ == "__main__":
    main(sys.argv[1:])
