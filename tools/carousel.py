"""Instagram carousel slides (1080x1350) in the 'desk scene + glass rows' style.
python3 carousel.py [key ...]  -> carousels/<key>/<nn>.jpg"""
import json, os, sys
from playwright.sync_api import sync_playwright
import build2 as B2

ROOT = os.path.dirname(os.path.abspath(__file__))
MEDIA = "/home/claude/reels-media/media"
W, H = 1080, 1350

CSS = B2.FONTS + """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden;background:#07080a;font-family:V,sans-serif;color:#fff}
.bg{position:absolute;inset:0;background-size:cover;background-position:center}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,6,8,.86) 0%,rgba(5,6,8,.35) 34%,rgba(5,6,8,.30) 55%,rgba(5,6,8,.88) 100%)}
.shade.inner{background:linear-gradient(180deg,rgba(5,6,8,.80) 0%,rgba(5,6,8,.55) 30%,rgba(5,6,8,.55) 70%,rgba(5,6,8,.85) 100%)}
.brand{position:absolute;top:58px;left:70px;font-size:22px;letter-spacing:9px;font-weight:700;opacity:.8;direction:ltr}
.page{position:absolute;bottom:62px;left:70px;font-size:26px;font-weight:700;opacity:.8;direction:ltr}
.handle{position:absolute;bottom:52px;left:50%;transform:translateX(-50%);font-size:26px;letter-spacing:4px;padding:10px 34px 12px;border-radius:40px;border:2px solid rgba(255,255,255,.35);background:rgba(0,0,0,.35);direction:ltr;font-weight:700}
.head{position:absolute;top:110px;left:70px;right:70px;text-align:center;direction:rtl}
h1{font-size:92px;font-weight:900;line-height:1.18;text-shadow:0 8px 40px rgba(0,0,0,.6)}
h1 em{font-style:normal;color:var(--a)}
.sub{margin-top:18px;font-size:38px;font-weight:700;color:rgba(255,255,255,.88)}
.cover h1{font-size:104px}
.pill{display:inline-block;margin-top:30px;font-size:42px;font-weight:900;padding:12px 44px 18px;border-radius:26px;background:rgba(255,255,255,.12);border:2px solid var(--a);backdrop-filter:blur(10px)}
.swipe{position:absolute;bottom:150px;left:50%;transform:translateX(-50%);font-size:34px;font-weight:700;padding:16px 46px 20px;border-radius:24px;background:rgba(10,10,12,.55);border:2px solid rgba(255,255,255,.3);direction:rtl;white-space:nowrap}
.swipe b{color:var(--a)}
.rows{position:absolute;left:80px;right:80px;top:400px;bottom:190px;display:flex;flex-direction:column;justify-content:center;gap:30px;direction:rtl}
em{font-style:normal;color:var(--a)}
.row{display:flex;align-items:center;gap:28px;padding:34px 40px;border-radius:26px;background:linear-gradient(135deg,rgba(255,255,255,.13),rgba(255,255,255,.05));border:2px solid color-mix(in srgb,var(--a) 55%,transparent);box-shadow:0 0 30px color-mix(in srgb,var(--a) 22%,transparent),inset 0 1px 0 rgba(255,255,255,.18);backdrop-filter:blur(14px)}
.num{font-size:34px;font-weight:700;color:var(--a);min-width:52px;direction:ltr;text-align:center;border-left:2px solid rgba(255,255,255,.25);padding-left:22px}
.txt{flex:1}
.t{font-size:48px;font-weight:900;line-height:1.3}
.t .en{direction:ltr;unicode-bidi:isolate}
.d{margin-top:10px;font-size:34px;font-weight:400;line-height:1.5;color:rgba(255,255,255,.82)}
.big .t{font-size:52px}
.big .d{font-size:36px}
.note{position:absolute;left:90px;right:90px;bottom:140px;text-align:center;font-size:32px;font-weight:700;direction:rtl;color:rgba(255,255,255,.85)}
.cta h1{font-size:96px}
.cta .num42{font-size:150px;color:var(--a);font-weight:900;line-height:1}
.save{margin-top:28px;font-size:36px;font-weight:700;color:rgba(255,255,255,.85)}
"""


def esc(s):
    return B2.esc(s)


def rich(s):
    """**x** -> accent, `x` -> ltr span"""
    import re
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<em>\1</em>", s)
    s = re.sub(r"`(.+?)`", r'<span class="en">\1</span>', s)
    return s.replace("\n", "<br>")


def slide_html(c, i, s, n):
    a = c["accent"]
    img = c["cover"] if s["type"] in ("cover", "cta") else c["bg"]
    bgpos = (f"background-size:{c['cover_size']};background-position:{c['cover_x']} 40%" if img == c["cover"] and c.get("cover_size") else "")
    shade = "shade" if s["type"] in ("cover", "cta") else "shade inner"
    body = ""
    if s["type"] == "cover":
        body = (f'<div class="head cover"><h1>{rich(s["title"])}</h1>'
                + (f'<div class="pill">{rich(s["pill"])}</div>' if s.get("pill") else "")
                + (f'<div class="sub">{rich(s["sub"])}</div>' if s.get("sub") else "") + "</div>"
                + f'<div class="swipe">ورق بزن <b>←</b> {esc(s.get("swipe", ""))}</div>')
    elif s["type"] == "rows":
        rows = "".join(
            f'<div class="row"><div class="num">{k + 1:02d}</div><div class="txt"><div class="t">{rich(r[0])}</div>'
            + (f'<div class="d">{rich(r[1])}</div>' if len(r) > 1 and r[1] else "") + "</div></div>"
            for k, r in enumerate(s["rows"], start=s.get("start", 0)))
        body = (f'<div class="head"><h1>{rich(s["title"])}</h1>'
                + (f'<div class="sub">{rich(s["sub"])}</div>' if s.get("sub") else "") + "</div>"
                + f'<div class="rows {s.get("cls", "")}" style="--top:{s.get("top", 430)}px">{rows}</div>'
                + (f'<div class="note">{rich(s["note"])}</div>' if s.get("note") else ""))
    elif s["type"] == "cta":
        body = (f'<div class="head cta" style="top:150px"><h1>{rich(s["title"])}</h1></div>'
                f'<div class="head" style="top:auto;bottom:250px"><h1 style="font-size:70px">{rich(s["ask"])}</h1>'
                f'<div class="save">🔖 {esc(s.get("save", "ذخیره کن تا وقتی لازمت شد گمش نکنی"))}</div></div>')
    return (f'<!doctype html><html lang="fa"><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body style="--a:{a}"><div class="bg" style="background-image:url(file://{MEDIA}/{img});{bgpos}"></div>'
            f'<div class="{shade}"></div><div class="brand">EHBEHZAD</div>{body}'
            f'<div class="handle">@ehbehzad</div><div class="page">{i}/{n}</div></body></html>')


def render(keys):
    data = json.load(open(os.path.join(ROOT, "carousels.json")))
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        for key in keys or list(data):
            c = data[key]
            out = os.path.join(ROOT, "carousels", key)
            os.makedirs(out, exist_ok=True)
            n = len(c["slides"])
            for i, s in enumerate(c["slides"], 1):
                hp = os.path.join(ROOT, f"_car.html")
                open(hp, "w").write(slide_html(c, i, s, n))
                pg.goto("file://" + hp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(250)
                pg.screenshot(path=os.path.join(out, f"{i:02d}.jpg"), type="jpeg", quality=92)
            print("ok", key, n)
        b.close()


if __name__ == "__main__":
    render(sys.argv[1:])
