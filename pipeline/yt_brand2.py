"""YouTube channel art, second pass: three directions, each a banner (2560x1440, content inside the
1546x423 centre) and a matching avatar (800x800, circle-safe).
A 'studio'  - the look of the web-design ad: dark grid, lime glow, phones showing the real reel covers
B 'signal'  - light-fibre footage frame, glowing type
C 'aurora'  - vivid mesh gradient with glass topic pills"""
import os
from playwright.sync_api import sync_playwright
import build2 as B2

ROOT = os.path.dirname(os.path.abspath(__file__))
F = "file://" + ROOT
SPARK = '<svg viewBox="0 0 24 24"><path d="M12 2l2.2 6.3L20.5 10l-6.3 2.2L12 18.5l-2.2-6.3L3.5 10l6.3-1.7z" fill="currentColor"/></svg>'
BASE = B2.FONTS + "*{margin:0;padding:0;box-sizing:border-box}html,body{font-family:V,sans-serif;color:#fff;overflow:hidden}"
SAFE = ".safe{position:absolute;left:507px;top:508px;width:1546px;height:423px}"

def phone(key, x, y, h, rot, dim=1.0):
    w = h * 9 / 16
    return (f'<div class="ph" style="left:{x}px;top:{y}px;width:{w:.0f}px;height:{h}px;transform:rotate({rot}deg);opacity:{dim}">'
            f'<img src="{F}/covers/cover_{key}.jpg"></div>')

# ---------- A: studio ----------
A_PH = ".ph{position:absolute;border-radius:30px;overflow:hidden;border:6px solid #1c2126;box-shadow:0 30px 80px rgba(0,0,0,.7),0 0 0 2px rgba(255,255,255,.08)}.ph img{width:100%;height:100%;object-fit:cover;display:block}"
banner_a = f"""<style>{BASE}{SAFE}{A_PH}
html,body{{width:2560px;height:1440px;background:#06080a}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.045) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.045) 2px,transparent 2px);background-size:96px 96px}}
.glow{{position:absolute;border-radius:50%;filter:blur(120px)}}
.g1{{left:820px;top:260px;width:900px;height:900px;background:rgba(198,244,50,.20)}}
.g2{{left:-200px;top:300px;width:800px;height:800px;background:rgba(34,211,238,.13)}}
.g3{{right:-200px;top:300px;width:800px;height:800px;background:rgba(176,124,255,.14)}}
.vig{{position:absolute;inset:0;background:radial-gradient(1500px 800px at 50% 50%,transparent 40%,rgba(4,5,7,.85) 100%)}}
.txt{{position:absolute;right:30px;top:0;bottom:0;width:980px;direction:rtl;display:flex;flex-direction:column;justify-content:center;align-items:flex-start}}
.tag{{display:flex;align-items:center;gap:14px;font-size:38px;font-weight:900;color:#0a0c0e;background:#c6f432;padding:6px 28px 12px;border-radius:40px;margin-bottom:20px}}
.tag svg{{width:36px;height:36px}}
h1{{font-size:112px;font-weight:900;line-height:1.16;white-space:nowrap}}
h1 em{{font-style:normal;color:#c6f432}}
p{{margin-top:18px;font-size:42px;font-weight:700;color:#aeb6bd;white-space:nowrap}}
p b{{color:#fff;direction:ltr;display:inline-block}}
</style><div class="grid"></div><div class="glow g1"></div><div class="glow g2"></div><div class="glow g3"></div><div class="vig"></div>
{phone("reel13_dont", 90, 470, 500, -8, .55)}{phone("reel10_interview", 330, 500, 440, 6, .5)}
{phone("reel16_resume", 2110, 500, 440, -6, .5)}{phone("reel7_teacher", 2330, 470, 500, 8, .55)}
<div class="safe">{phone("reel19_imgprompt", 20, 30, 370, -9)}{phone("web1_page", 330, 18, 390, 7)}{phone("reel25_skill", 168, 4, 415, -1)}
<div class="txt"><div class="tag">{SPARK}<span>هر روز یک ویدیوی کوتاه</span></div>
<h1>هوش مصنوعی<br><em>ساده و کاربردی</em></h1><p>ابزار رایگان، پرامپت آماده، طراحی سایت &nbsp; <b>@ehbehzad</b></p></div></div>"""
avatar_a = f"""<style>{BASE}html,body{{width:800px;height:800px;background:#06080a}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.06) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.06) 2px,transparent 2px);background-size:80px 80px}}
.glow{{position:absolute;inset:120px;border-radius:50%;background:rgba(198,244,50,.42);filter:blur(90px)}}
.disc{{position:absolute;left:190px;top:190px;width:420px;height:420px;border-radius:50%;background:#c6f432;display:grid;place-items:center;box-shadow:0 0 0 14px rgba(198,244,50,.18),0 30px 80px rgba(0,0,0,.6)}}
.disc svg{{width:360px;height:360px;color:#06080a;margin-top:26px}}
</style><div class="grid"></div><div class="glow"></div><div class="disc">{SPARK}</div>"""

# ---------- B: signal ----------
banner_b = f"""<style>{BASE}{SAFE}
html,body{{width:2560px;height:1440px;background:#020611}}
.bg{{position:absolute;inset:0;background:url({F}/youtube/bg_fibres.jpg) center/cover;transform:rotate(90deg) scale(1.78);filter:saturate(1.3) brightness(.95)}}
.sh{{position:absolute;inset:0;background:radial-gradient(1300px 520px at 50% 50%,rgba(2,6,17,.86),rgba(2,6,17,.25) 75%,rgba(2,6,17,.55))}}
.safe{{direction:rtl;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}}
h1{{font-size:102px;font-weight:900;line-height:1.2;white-space:nowrap;text-shadow:0 0 60px rgba(77,163,255,.9),0 0 14px rgba(77,163,255,.7)}}
h1 em{{font-style:normal;color:#7fd4ff}}
p{{margin-top:22px;font-size:46px;font-weight:700;white-space:nowrap;color:#d6e6ff}}
.h{{margin-top:22px;font-size:42px;font-weight:900;direction:ltr;padding:6px 34px 12px;border-radius:40px;border:3px solid #7fd4ff;color:#7fd4ff;background:rgba(2,6,17,.5)}}
</style><div class="bg"></div><div class="sh"></div>
<div class="safe"><h1>هوش مصنوعی رو <em>ساده</em> یاد بگیر</h1><p>هر روز یک ویدیوی کوتاه از ابزارها و ترفندها</p><div class="h">@ehbehzad</div></div>"""
avatar_b = f"""<style>{BASE}html,body{{width:800px;height:800px;background:#020611}}
.bg{{position:absolute;inset:-60px;background:url({F}/youtube/bg_fibres.jpg) center/cover;filter:saturate(1.4) brightness(.8)}}
.sh{{position:absolute;inset:0;background:radial-gradient(circle at 50% 50%,rgba(2,6,17,.2),rgba(2,6,17,.75))}}
.m{{position:absolute;inset:0;display:grid;place-items:center}}
.m svg{{width:430px;height:430px;color:#fff;filter:drop-shadow(0 0 50px rgba(77,163,255,1)) drop-shadow(0 0 14px rgba(127,212,255,.9));margin-top:32px}}
</style><div class="bg"></div><div class="sh"></div><div class="m">{SPARK}</div>"""

# ---------- C: aurora ----------
MESH = ("background:radial-gradient(1300px 900px at 10% 30%,#7c3aed,transparent 70%),radial-gradient(1300px 900px at 90% 35%,#ec4899,transparent 68%),"
        "radial-gradient(1400px 900px at 68% 80%,#2563eb,transparent 66%),radial-gradient(1200px 800px at 25% 78%,#06b6d4,transparent 64%),#2a0f5c")
banner_c = f"""<style>{BASE}{SAFE}
html,body{{width:2560px;height:1440px;{MESH}}}
.noise{{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.10) 1.5px,transparent 1.5px);background-size:26px 26px;opacity:.5}}
.safe{{direction:rtl;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}}
h1{{font-size:104px;font-weight:900;line-height:1.2;white-space:nowrap;text-shadow:0 10px 40px rgba(18,6,43,.55)}}
.pills{{margin-top:30px;display:flex;gap:14px}}
.pills span{{font-size:36px;font-weight:900;padding:6px 26px 12px;border-radius:50px;background:rgba(255,255,255,.16);border:3px solid rgba(255,255,255,.55);backdrop-filter:blur(8px);white-space:nowrap}}
.pills span.h{{background:#fff;color:#3b1d8f;direction:ltr}}
</style><div class="noise"></div>
<div class="safe"><h1>هوش مصنوعی، ساده و کاربردی</h1>
<div class="pills"><span>ابزار رایگان</span><span>پرامپت آماده</span><span>ساخت عکس و ویدیو</span><span>طراحی سایت</span><span class="h">@ehbehzad</span></div></div>"""
avatar_c = f"""<style>{BASE}html,body{{width:800px;height:800px;background:radial-gradient(520px 420px at 20% 20%,#7c3aed,transparent 65%),radial-gradient(520px 460px at 85% 25%,#ec4899,transparent 62%),radial-gradient(560px 460px at 70% 95%,#2563eb,transparent 60%),radial-gradient(480px 420px at 20% 95%,#06b6d4,transparent 60%),#12062b}}
.m{{position:absolute;inset:0;display:grid;place-items:center}}
.m svg{{width:440px;height:440px;color:#fff;filter:drop-shadow(0 16px 40px rgba(18,6,43,.6));margin-top:32px}}
</style><div class="m">{SPARK}</div>"""

def main():
    os.makedirs(os.path.join(ROOT, "youtube"), exist_ok=True)
    jobs = [("banner_A", banner_a, 2560, 1440), ("banner_B", banner_b, 2560, 1440), ("banner_C", banner_c, 2560, 1440),
            ("profile_A", avatar_a, 800, 800), ("profile_B", avatar_b, 800, 800), ("profile_C", avatar_c, 800, 800)]
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, body, w, h in jobs:
            pg = b.new_page(viewport={"width": w, "height": h})
            hp = os.path.join(ROOT, f"_yt_{name}.html")
            open(hp, "w").write(f'<!doctype html><html lang="fa"><head><meta charset="utf-8"></head><body>{body}</body></html>')
            pg.goto("file://" + hp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(600)
            pg.screenshot(path=os.path.join(ROOT, "youtube", f"{name}.png")); pg.close(); print("ok", name)
        b.close()

if __name__ == "__main__":
    main()
