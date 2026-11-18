"""Uniform YouTube Shorts covers for @ehbehzad (cream 'ui' style). python3 ytcovers.py -> /mnt/user-data/outputs/yt_covers/<id>.jpg"""
import os, json
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.abspath(__file__))
FONT = "file://" + ROOT + "/node_modules/@fontsource"
ROBOT = "file://" + ROOT + "/out/mascot_2_robot_glass.png"
OUT = "/mnt/user-data/outputs/yt_covers"
# id: (chip, line1, line2 (highlighted), accent)
C = {
 "nyl38WH9vGI": ("ساخت ویدیو", "فرمول", "پرامپت ویدیو", "#e8693c"),
 "MRGrBfqdasQ": ("ElevenLabs", "صدای حرفه‌ای", "رایگان", "#6a5cff"),
 "TksNhHIca_8": ("جواب صادقانه", "ChatGPT", "ویدیو می‌سازه؟", "#ff4f8b"),
 "Dt1EIIXCZbw": ("کسب‌وکار", "پیج اینستاگرام", "کافی نیست!", "#14a989"),
 "d51X5uontGk": ("ChatGPT", "از خط‌خطی", "تا عکس کامل", "#f2a516"),
 "QWm6KKHGdTs": ("ChatGPT", "ادیت عکس", "بدون فتوشاپ", "#2d8cff"),
 "s4_XCxNdh1E": ("ساخت تصویر", "فرمول", "پرامپت عکس", "#e8693c"),
 "eSRzf_zJxMk": ("خبر Claude", "Claude توی", "داکس و شیت", "#6a5cff"),
 "NcL7F9BlXuQ": ("نمونه‌کار", "سایت فروشگاهی", "چرم ELVA", "#14a989"),
 "uZAv2qXWsnM": ("آموزش", "گیت‌هاب", "به زبان ساده", "#17151a"),
 "dg0AftUVapI": ("آموزش Claude", "کانکتور", "چیه؟", "#2d8cff"),
 "8jQc9pYXKrc": ("ترفند", "۵ عادت", "جواب بهتر", "#ff4f8b"),
 "BqUkMir0JTA": ("ابزار رایگان", "ساخت ویدیو", "رایگان و متن‌باز", "#f2a516"),
 "aa5mbMb8fUU": ("آموزش Claude", "اسکیل", "چیه؟", "#e8693c"),
}
HTML = """<!doctype html><html lang=fa><head><meta charset=utf-8><style>
@font-face{font-family:Vaz;font-weight:800;src:url(FONT/vazirmatn/files/vazirmatn-arabic-800-normal.woff2)}
@font-face{font-family:Vaz;font-weight:900;src:url(FONT/vazirmatn/files/vazirmatn-arabic-900-normal.woff2)}
@font-face{font-family:Vaz;font-weight:900;src:url(FONT/vazirmatn/files/vazirmatn-latin-900-normal.woff2);unicode-range:U+0000-00FF}
@font-face{font-family:Vaz;font-weight:800;src:url(FONT/vazirmatn/files/vazirmatn-latin-800-normal.woff2);unicode-range:U+0000-00FF}
*{margin:0;padding:0;box-sizing:border-box}
html{overflow:hidden}body{width:1080px;height:1920px;overflow:hidden;background:#f5f1ea;font-family:Vaz;direction:rtl;color:#17151a;position:relative}
.b{position:absolute;border-radius:50%;filter:blur(120px);opacity:.6}
.g{position:absolute;inset:0;background-image:radial-gradient(rgba(23,21,26,.13) 2px,transparent 2.2px);background-size:40px 40px;
 -webkit-mask:radial-gradient(ellipse 70% 50% at 50% 48%,#000 20%,transparent 75%);opacity:.55}
.card{position:absolute;left:60px;width:960px;top:780px;border-radius:64px;background:rgba(255,255,255,.88);border:2px solid rgba(23,21,26,.07);
 box-shadow:0 50px 120px rgba(60,40,20,.16);padding:80px 50px 90px;text-align:center}
.chip{display:inline-block;font-weight:800;font-size:46px;color:#fff;background:#17151a;border-radius:50px;padding:10px 40px 16px;margin-bottom:46px}
.l1{font-weight:900;font-size:118px;line-height:1.1;letter-spacing:-2px}
.l2{display:inline-block;max-width:100%;margin-top:26px;font-weight:900;font-size:104px;line-height:1.15;color:#fff;background:var(--a);border-radius:40px;padding:4px 44px 24px;
 box-shadow:0 30px 70px color-mix(in srgb,var(--a) 45%,transparent)}
.rb{position:absolute;left:50%;top:420px;width:300px;height:300px;margin-left:-150px;border-radius:50%;overflow:hidden;border:10px solid #fff;
 box-shadow:0 30px 70px rgba(60,40,20,.25);background:#1b1b1d}
.rb i{position:absolute;left:-12px;top:-24px;width:319px;height:425px;background:url(ROBOT) 0 0/319px 425px}
.rb .e{position:absolute;top:113px;width:24px;height:32px;border-radius:50%;background:#eaf8ff;box-shadow:0 0 10px #bfe9ff}
.rb .m{position:absolute;left:128px;top:162px;width:44px;height:16px;border-bottom:6px solid #eaf8ff;border-radius:0 0 50% 50%}
.h{position:absolute;bottom:250px;left:0;right:0;text-align:center;font-weight:800;font-size:50px;color:#8d8794;direction:ltr}
</style></head><body style="--a:ACC">
<div class=b style="left:-220px;top:60px;width:820px;height:820px;background:#ffb38a"></div>
<div class=b style="right:-280px;top:760px;width:880px;height:880px;background:#b7a8ff"></div>
<div class=b style="left:-140px;bottom:-200px;width:820px;height:820px;background:#9ee6c9"></div><div class=g></div>
<div class=rb><i></i><div class=e style="left:113px"></div><div class=e style="left:163px"></div><div class=m></div></div>
<div class=card><div class=chip>CHIP</div><div class=l1>L1</div><div class=l2>L2</div></div>
<div class=h>@ehbehzad</div></body></html>"""
os.makedirs(OUT, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
    for vid, (chip, l1, l2, acc) in C.items():
        h = HTML.replace("FONT", FONT).replace("ROBOT", ROBOT).replace("ACC", acc).replace("CHIP", chip).replace("L1", l1).replace("L2", l2)
        fp = f"/tmp/cov_{vid}.html"; open(fp, "w").write(h)
        pg.goto("file://" + fp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
        pg.screenshot(path=f"{OUT}/{vid}.jpg", type="jpeg", quality=88)
    b.close()
print("ok")
