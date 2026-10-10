"""YouTube channel art: avatar (800x800, survives the circular crop) and banner (2560x1440,
everything that matters inside the 1546x423 centre that phones show)."""
import os
from playwright.sync_api import sync_playwright
import build2 as B2
ROOT = os.path.dirname(os.path.abspath(__file__))
COLS = ["#ff4d5e", "#ff8a3d", "#ffd23f", "#c6f432", "#3ddc97", "#22d3ee", "#4da3ff", "#b07cff", "#ff4f9a"]
seg = 360 / len(COLS)
ring = ",".join(f"{c} {i*seg:.1f}deg {(i+1)*seg-3:.1f}deg,#07070a {(i+1)*seg-3:.1f}deg {(i+1)*seg:.1f}deg" for i, c in enumerate(COLS))
AVATAR = f"""<!doctype html><html><head><meta charset="utf-8"><style>{B2.FONTS}
*{{margin:0;box-sizing:border-box}}html,body{{width:800px;height:800px;background:#07070a;font-family:V,sans-serif}}
.ring{{position:absolute;inset:70px;border-radius:50%;background:conic-gradient(from -90deg,{ring})}}
.disc{{position:absolute;inset:118px;border-radius:50%;background:#07070a;display:grid;place-items:center}}
.m{{font-size:300px;font-weight:900;color:#fff;letter-spacing:-14px;line-height:1;margin-top:-34px;margin-left:-14px}}
.m b{{color:#c6f432;font-weight:900}}
</style></head><body><div class="ring"></div><div class="disc"><div class="m">e<b>b</b></div></div></body></html>"""
bars = "".join(f'<i style="background:{c}"></i>' for c in COLS)
BANNER = f"""<!doctype html><html lang="fa"><head><meta charset="utf-8"><style>{B2.FONTS}
*{{margin:0;box-sizing:border-box}}html,body{{width:2560px;height:1440px;background:#07070a;font-family:V,sans-serif;color:#fff;overflow:hidden}}
.bars{{position:absolute;top:0;bottom:0;display:flex;gap:14px}}
.bars i{{width:34px;height:100%;display:block;transform:skewX(-12deg)}}
.bars.l{{left:60px}}.bars.r{{right:60px;flex-direction:row-reverse}}
.fade{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(7,7,10,0) 0,rgba(7,7,10,0) 320px,#07070a 520px,#07070a 2040px,rgba(7,7,10,0) 2240px)}}
.safe{{position:absolute;left:507px;top:508px;width:1546px;height:423px;direction:rtl;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}}
h1{{font-size:104px;font-weight:900;line-height:1.25;white-space:nowrap}}
h1 b{{color:#07070a;background:#c6f432;padding:0 30px 10px;border-radius:22px;font-weight:900}}
p{{margin-top:34px;font-size:50px;font-weight:700;opacity:.86;white-space:nowrap}}
.h{{margin-top:26px;font-size:46px;font-weight:900;direction:ltr;color:#c6f432}}
</style></head><body><div class="bars l">{bars}</div><div class="bars r">{bars}</div><div class="fade"></div>
<div class="safe"><h1>هوش مصنوعی، <b>ساده و کاربردی</b></h1>
<p>هر روز یک ویدیوی کوتاه از ابزارها و ترفندها، به‌علاوه‌ی طراحی سایت</p><div class="h">@ehbehzad</div></div></body></html>"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, page, w, h in (("avatar", AVATAR, 800, 800), ("banner", BANNER, 2560, 1440)):
        pg = b.new_page(viewport={"width": w, "height": h})
        hp = os.path.join(ROOT, f"_yt_{name}.html"); open(hp, "w").write(page)
        pg.goto("file://" + hp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
        pg.screenshot(path=os.path.join(ROOT, "youtube", f"{name}.png")); pg.close()
    b.close()
