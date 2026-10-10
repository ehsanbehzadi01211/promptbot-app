"""'Tip of the day' Instagram stories: one AI tip + a prompt to screenshot. -> stories/tip_<n>.jpg"""
import os, html
from playwright.sync_api import sync_playwright
import build2 as B2

ROOT = os.path.dirname(os.path.abspath(__file__))
TIPS = [  # colour, headline line 1, highlighted line 2, what it's for, the prompt
    ("#22d3ee", "به جواب اول", "اعتماد نکن", "تا خودش اشتباه‌هاش رو پیدا کنه", "جوابت رو دوباره بررسی کن. کجاش ممکنه غلط باشه؟"),
    ("#ffd23f", "هر چیز سخت رو", "ساده بخواه", "برای وقتی که یه موضوع رو نمی‌فهمی", "این رو طوری توضیح بده که یه بچه‌ی ۱۰ ساله هم بفهمه. با یه مثال."),
    ("#ff8a3d", "متن طولانی داری؟", "۳ خط بخواه", "برای مقاله، ایمیل یا گزارش بلند", "این متن رو توی ۳ خط خلاصه کن. فقط مهم‌ترین نکته‌ها."),
    ("#3ddc97", "بین چند گزینه‌ای؟", "جدول بخواه", "برای مقایسه‌ی گوشی، دوره یا شغل", "این گزینه‌ها رو توی یه جدول مقایسه کن: مزایا، معایب، هزینه."),
    ("#b07cff", "قبل از فرستادن پیام", "لحنش رو چک کن", "برای ایمیل و پیام‌های کاری", "این پیام رو مؤدبانه‌تر و کوتاه‌تر کن. معنی‌ش عوض نشه."),
    ("#ff4f9a", "کار بزرگ داری؟", "چک‌لیست بخواه", "برای سفر، اسباب‌کشی یا یه پروژه", "برای این کار یه چک‌لیست قدم‌به‌قدم بنویس. از اول تا آخر."),
]
CSS = B2.FONTS + """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;font-family:V,sans-serif;color:#fff;direction:rtl;
 background:radial-gradient(900px 700px at 85% 12%,color-mix(in srgb,var(--c) 30%,transparent),transparent 70%),#08080c}
.tag{position:absolute;top:270px;right:80px;font-size:50px;font-weight:900;color:#0b0b0f;background:var(--c);padding:6px 34px 12px;border-radius:18px;transform:rotate(2deg)}
.h{position:absolute;top:430px;right:80px;left:80px;font-size:104px;font-weight:900;line-height:1.3}
.h b{display:inline-block;margin-top:14px;color:#0b0b0f;background:var(--c);padding:0 28px 10px;border-radius:20px}
.for{position:absolute;top:800px;right:80px;left:80px;font-size:48px;font-weight:700;opacity:.82;line-height:1.5}
.card{position:absolute;top:950px;right:80px;left:80px;border-radius:44px 44px 44px 10px;background:#16161d;border:4px solid var(--c);padding:44px 52px 54px;box-shadow:0 40px 100px rgba(0,0,0,.55)}
.card small{display:block;font-size:38px;font-weight:900;color:var(--c);margin-bottom:22px}
.card p{font-size:62px;font-weight:700;line-height:1.6}
.foot{position:absolute;left:80px;right:80px;top:1560px;display:flex;justify-content:space-between;align-items:center;font-size:44px;font-weight:900}
.foot span{direction:ltr;opacity:.85}
.foot i{font-style:normal;padding:10px 30px 14px;border-radius:40px;border:3px solid rgba(255,255,255,.5)}
"""

def main():
    os.makedirs(os.path.join(ROOT, "stories"), exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        for n, (c, l1, l2, why, prompt) in enumerate(TIPS, 1):
            e = html.escape
            page = f"""<!doctype html><html lang="fa"><head><meta charset="utf-8"><style>{CSS}</style></head>
<body style="--c:{c}"><div class="tag">ترفند امروز</div>
<div class="h">{e(l1)}<br><b>{e(l2)}</b></div><div class="for">{e(why)}</div>
<div class="card"><small>این رو بهش بگو</small><p>{e(prompt)}</p></div>
<div class="foot"><i>اسکرین‌شات بگیر</i><span>@ehbehzad</span></div></body></html>"""
            hp = os.path.join(ROOT, f"_tip{n}.html"); open(hp, "w").write(page)
            pg.goto("file://" + hp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
            pg.screenshot(path=os.path.join(ROOT, "stories", f"tip_{n}.jpg"), type="jpeg", quality=92)
        b.close()

if __name__ == "__main__":
    main()
