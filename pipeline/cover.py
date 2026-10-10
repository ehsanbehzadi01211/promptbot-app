"""Custom reel covers: one shared template, one colour per row of three (Reels tab grid)."""
import os, html
from playwright.sync_api import sync_playwright
import build2 as B2

ROOT = os.path.dirname(os.path.abspath(__file__))
ROWS = {"red": "#ff4d5e", "yellow": "#ffd23f", "blue": "#4da3ff", "green": "#3ddc97", "purple": "#b07cff", "orange": "#ff8a3d", "pink": "#ff4f9a", "teal": "#22d3ee", "lime": "#c6f432"}
COVERS = [  # key, number, line1, highlighted line, row colour, kicker
    ("reel4_mistakes", "04", "۳ اشتباه", "رایج", "red", "اشتباه رایج"),
    ("reel5_prompt", "05", "پرامپت", "حرفه‌ای", "red", "پرامپت کاربردی"),
    ("reel6_how", "06", "ChatGPT", "فکر می‌کنه؟", "red", "به زبان ساده"),
    ("reel7_teacher", "19", "معلم", "خصوصی", "yellow", "یادگیری"),
    ("reel8_photo", "20", "فقط", "عکس بده", "yellow", "ترفند"),
    ("reel9_tasks", "21", "۵ کار در", "۱ دقیقه", "yellow", "بهره‌وری"),
    ("reel10_interview", "22", "تمرین", "مصاحبه", "blue", "ترفند کاری"),
    ("reel11_english", "23", "انگلیسی", "حرف بزن", "blue", "یادگیری زبان"),
    ("reel12_phrases", "24", "۳ جمله‌ی", "جادویی", "blue", "ترفند"),
    ("reel13_dont", "25", "۳ کار", "ممنوع", "green", "هشدار"),
    ("reel14_caption", "26", "کپشن", "حرفه‌ای", "green", "تولید محتوا"),
    ("reel15_decide", "27", "تصمیم", "سخت؟", "green", "تصمیم‌گیری"),
    ("reel16_resume", "28", "نقد", "رزومه", "purple", "ترفند کاری"),
    ("reel17_skill", "29", "۳۰ روز", "یه مهارت", "purple", "یادگیری"),
    ("reel18_no", "30", "«نه» گفتن", "مؤدبانه", "purple", "ترفند ارتباطی"),
    ("reel19_imgprompt", "13", "فرمول", "پرامپت عکس", "orange", "ساخت تصویر"),
    ("reel20_edit", "14", "ادیت عکس", "بدون فتوشاپ", "orange", "ادیت عکس"),
    ("reel21_sketch", "15", "از خط‌خطی", "تا تصویر", "orange", "ساخت تصویر"),
    ("reel22_video", "16", "ویدیو با", "ChatGPT؟", "pink", "ساخت ویدیو"),
    ("reel23_vprompt", "17", "فرمول", "پرامپت ویدیو", "pink", "ساخت ویدیو"),
    ("reel24_img2vid", "18", "عکس رو", "زنده کن", "pink", "ساخت ویدیو"),
    ("reel25_skill", "07", "اسکیل", "چیه؟", "teal", "ابزارهای Claude"),
    ("reel26_connector", "08", "کانکتور", "چیه؟", "teal", "ابزارهای Claude"),
    ("reel27_github", "09", "گیت‌هاب", "به زبان ساده", "teal", "ابزارهای Claude"),
    ("webdesign_ad", "10", "سایت خودت رو", "سفارش بده", "lime", "طراحی سایت"),
    ("web1_page", "11", "پیجت", "مال تو نیست", "lime", "طراحی سایت"),
    ("web2_speed", "12", "سایت کند؟", "مشتری رفت", "lime", "طراحی سایت"),
]
import sys
ALL_COVERS = list(COVERS)
if __name__ == "__main__" and len(sys.argv) > 1:
    COVERS = [c for c in COVERS if c[0] in sys.argv[1:]]

CSS = B2.FONTS + """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;font-family:V,sans-serif;color:#fff;background:#000}
.bg{position:absolute;inset:0;background-size:cover;background-position:center;filter:saturate(1.05) brightness(.62)}
.tint{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.55) 0%,rgba(0,0,0,.15) 30%,rgba(0,0,0,.2) 62%,rgba(0,0,0,.75) 100%)}
.frame{position:absolute;left:0;right:0;top:240px;bottom:240px;border-top:14px solid var(--c);border-bottom:14px solid var(--c);opacity:.0}
.safe{position:absolute;left:0;right:0;top:240px;height:1440px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;direction:rtl}
.kick{font-size:44px;font-weight:700;padding:10px 30px;border-radius:12px;background:rgba(0,0,0,.55);border-right:12px solid var(--c);margin-bottom:46px}
.t1{font-size:150px;font-weight:900;line-height:1.15;text-shadow:0 8px 40px rgba(0,0,0,.6)}
.t2{margin-top:18px;font-size:150px;font-weight:900;line-height:1.2;color:#0b0b0f;background:var(--c);padding:0 34px 10px;border-radius:22px}
.num{position:absolute;top:300px;left:90px;font-size:120px;font-weight:900;color:transparent;-webkit-text-stroke:5px var(--c);letter-spacing:2px}
.hd{position:absolute;bottom:310px;left:0;right:0;text-align:center;font-size:44px;font-weight:700;opacity:.9}
.bar{position:absolute;left:0;right:0;bottom:0;height:22px;background:var(--c)}
.bar.t{top:0;bottom:auto}
"""

def main():
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        for key, num, l1, l2, row, kick in COVERS:
            bg = os.path.join(ROOT, "covers", f"bg_{key}.jpg")
            page = f"""<!doctype html><html lang="fa"><head><meta charset="utf-8"><style>{CSS}</style></head>
<body style="--c:{ROWS[row]}"><div class="bg" style="background-image:url('file://{bg}')"></div><div class="tint"></div>
<div class="bar t"></div><div class="num" dir="ltr">{num}</div>
<div class="safe"><div class="kick">{html.escape(kick)}</div><div class="t1">{html.escape(l1)}</div><div class="t2">{html.escape(l2)}</div></div>
<div class="hd" dir="ltr">@ehbehzad</div><div class="bar"></div></body></html>"""
            hp = os.path.join(ROOT, "covers", f"_{key}.html"); open(hp, "w").write(page)
            pg.goto("file://" + hp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
            pg.screenshot(path=os.path.join(ROOT, "covers", f"cover_{key}.jpg"), type="jpeg", quality=92)
            print("ok", key)
        b.close()

if __name__ == "__main__":
    main()
