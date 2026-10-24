"""Story images (1080x1920 JPG) in the v8 design system."""
import os, json
from playwright.sync_api import sync_playwright
import build8 as B

STORIES = [
 ("s01", "#E0306A", "cream", "ریل جدید", "ماهی ۱۰ هزار\nکردیت [[رایگان]]", "برای ساخت صدا با هوش مصنوعی", "kw", "صدا"),
 ("s02", "#1F6FEB", "ink", "امشب ساعت ۹", "روزی ۵ ویدیو\n[[با صدا]]، رایگان", "با هوش مصنوعی گوگل 🎬", "soon", ""),
 ("s03", "#E8622C", "cream", "امشب ساعت ۹", "پرامپتِ [[هر عکسی]]\nرو دربیار", "با ChatGPT، Gemini یا Claude", "soon", ""),
 ("s04", "#E0306A", "ink", "ترفند امروز", "قبل از جواب\n[[ازم سؤال بپرس]]", "این جمله رو اول هر پرامپت بنویس؛ جواب دقیق‌تر می‌گیری", "tip", ""),
 ("s05", "#7C3AED", "cream", "ریل جدید", "۳ سایت [[عکس‌ساز]]\nکه رایگانن", "Krea · Ideogram · Leonardo", "kw", "عکس"),
 ("s06", "#16A34A", "ink", "امشب ساعت ۹", "اندیکاتورِ [[خودت]]\nرو بساز", "با Claude و TradingView 📈", "soon", ""),
 ("s07", "#E0306A", "accent", "طراحی سایت", "کسب‌وکارت\n[[سایت]] نداره؟", "دایرکت بده تا برات طراحی کنم · نمونه‌کار: elvaleather.ir", "dm", ""),
 ("s08", "#1F6FEB", "cream", "تلگرام", "اخبار روز\n[[هوش مصنوعی]]", "هر روز، کوتاه و فارسی · t.me/ehbehzad_ai", "link", "@ehbehzad_ai"),
 ("s09", "#E8622C", "ink", "این هفته", "۵ ابزار رایگان\n[[۵ کلمه]]", "زیر هر ریل کلمه‌ش رو کامنت کن تا لینک بیاد", "chips", "صدا|ویو|پرامپت|عکس|اندیکاتور"),
 ("s10", "#7C3AED", "cream", "ترفند امروز", "نقطه‌ضعفِ\n[[جوابت رو بگو]]", "آخر پرامپت بنویس؛ هوش مصنوعی خودش رو چک می‌کنه", "tip", ""),
 ("s11", "#E0306A", "ink", "یوتیوب", "همه‌ی ویدیوها\n[[توی یوتیوب]]", "youtube.com/@ehbehzad", "link", "@ehbehzad"),
 ("s12", "#16A34A", "cream", "امنیت", "رمز و کارت بانکی\n[[رو به AI نده]]", "هیچ چت‌باتی جای امنی برای اطلاعات بانکی نیست 🔒", "tip", ""),
 ("s13", "#1F6FEB", "accent", "نظرسنجی", "ابزار رایگانِ\n[[بعدی]] چی باشه؟", "اسمش رو برام دایرکت بفرست", "dm", ""),
 ("s14", "#E8622C", "cream", "ترفند ویدیو", "توی هر صحنه\n[[فقط یه حرکت]]", "ویدیوسازها با چند حرکت هم‌زمان قاطی می‌کنن", "tip", ""),
 ("s15", "#E0306A", "ink", "طراحی سایت", "سایتت زیر\n[[۳ ثانیه]] باز میشه؟", "دایرکت بده تا سرعتش رو برات چک کنم", "dm", ""),
]

EXTRA = """
.scene{visibility:visible}
.story .content{top:330px;height:1180px}
.story .h1{font-size:150px}
.kick{align-self:flex-start;font-family:Vaz;font-weight:900;font-size:50px;background:var(--fg);color:var(--bg);padding:14px 40px 20px;border-radius:70px;margin-bottom:60px;display:inline-flex;gap:16px;align-items:center}
.kick i{width:22px;height:22px;border-radius:50%;background:var(--a);display:inline-block}
.box{margin-top:auto;margin-bottom:30px;border:5px solid var(--fg);border-radius:40px;padding:40px;display:flex;flex-direction:column;gap:24px}
.box .q{font-size:46px;font-weight:800;color:var(--mut)}
.box .k{font-size:120px;font-weight:900;color:var(--em);line-height:1.1}
.chips2{display:flex;flex-wrap:wrap;gap:20px}
.chips2 span{font-size:56px;font-weight:900;border:4px solid var(--fg);padding:10px 36px 18px;border-radius:60px}
.big2{font-family:"Inter Display",Inter;font-weight:900;font-size:96px;direction:ltr;text-align:left}
.foot{position:absolute;left:72px;right:72px;bottom:150px;display:flex;justify-content:space-between;direction:ltr;font-family:Mono;font-weight:700;font-size:28px;color:var(--mut)}
"""

def card(kind, val):
    if kind == "kw":
        return f'<div class="box"><div class="q">برو زیر ریل و این کلمه رو کامنت کن 👇</div><div class="k">«{B.esc(val)}»</div></div>'
    if kind == "soon":
        return '<div class="box"><div class="q">ریل جدید</div><div class="k">ساعت ۲۱:۰۰ ⏰</div></div>'
    if kind == "tip":
        return '<div class="box"><div class="q">ذخیره کن 🔖</div><div class="k" style="font-size:80px">ترفند هوش مصنوعی</div></div>'
    if kind == "dm":
        return '<div class="box"><div class="q">دایرکت پیام بده 📩</div><div class="k lat" style="font-size:96px;text-align:right">@ehbehzad</div></div>'
    if kind == "link":
        return f'<div class="box"><div class="q">دنبال کن 👇</div><div class="big2">{B.esc(val)}</div></div>'
    if kind == "chips":
        return '<div class="box"><div class="chips2">' + "".join(f"<span>{B.esc(x)}</span>" for x in val.split("|")) + "</div></div>"

def main():
    out = os.path.join(B.ROOT, "out", "stories"); os.makedirs(out, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        for sid, acc, bg, kick, title, sub, kind, val in STORIES:
            lines = B.rich(title)
            h1 = "".join(f'<span class="ln"><span>{ln}{"<i class=dot></i>" if k == len(lines) - 1 else ""}</span></span>' for k, ln in enumerate(lines))
            page = (f'<!doctype html><html lang="fa"><head><meta charset="utf-8"><style>{B.CSS.replace("FONT", B.FONT)}{EXTRA}</style></head>'
                    f'<body style="--a:{acc}"><section class="scene story {bg}"><div class="bgl"></div><div class="stage">'
                    f'<div class="content"><div class="kick"><i></i>{B.esc(kick)}</div><div class="h1">{h1}</div>'
                    f'<div class="sub">{B.esc(sub)}</div>{card(kind, val)}</div>'
                    f'<div class="foot"><span>@EHBEHZAD</span><span>AI · FREE TOOLS</span></div></div></section>'
                    f'<script>{B.JS}</script></body></html>')
            hp = os.path.join(out, sid + ".html"); open(hp, "w").write(page)
            pg.goto("file://" + hp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300); pg.evaluate("window.fitAll()")
            pg.screenshot(path=os.path.join(out, sid + ".jpg"), type="jpeg", quality=92)
        b.close()

if __name__ == "__main__":
    main()
