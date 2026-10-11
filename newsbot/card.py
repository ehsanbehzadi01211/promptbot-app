"""Branded 1280x720 news card for Telegram when a story has no usable image of its own.
  card(title_fa, source, out_path) -> out_path"""
import hashlib, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BOLD = os.path.join(HERE, "assets", "Vazirmatn-900.ttf")
MED = os.path.join(HERE, "assets", "Vazirmatn-500.ttf")
W, H = 1280, 720
ACCENTS = {"OpenAI": "#10a37f", "Anthropic": "#d97757", "Google": "#4285f4", "Google DeepMind": "#4285f4",
           "Microsoft": "#00a4ef", "NVIDIA": "#76b900", "Hugging Face": "#ffb000", "Meta": "#0866ff"}
PALETTE = ["#7c5cff", "#2fb8ff", "#ff4f9a", "#3ddc97", "#ffb347", "#c9a7ff"]


def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


from PIL import features
RAQM = features.check("raqm")


def _font(path, size):
    return ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM if RAQM else ImageFont.Layout.BASIC)


def _shape(text):
    """Without libraqm, shape + reorder Persian ourselves (arabic_reshaper + python-bidi)."""
    if RAQM:
        return text
    import arabic_reshaper
    from bidi.algorithm import get_display
    return get_display(arabic_reshaper.reshape(text))


def _rtl(d, xy_right, y, text, font, fill):
    if RAQM:
        w = d.textlength(text, font=font, direction="rtl", language="fa")
        d.text((xy_right - w, y), text, font=font, fill=fill, direction="rtl", language="fa")
    else:
        t = _shape(text)
        d.text((xy_right - d.textlength(t, font=font), y), t, font=font, fill=fill)


def _wrap(draw, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        tl = draw.textlength(trial, font=font, direction="rtl", language="fa") if RAQM else draw.textlength(_shape(trial), font=font)
        if tl <= width or not cur:
            cur = trial
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def card(title, source, out):
    accent = ACCENTS.get(source) or PALETTE[int(hashlib.md5(source.encode()).hexdigest(), 16) % len(PALETTE)]
    a = _rgb(accent)
    img = Image.new("RGB", (W, H), (8, 9, 14))
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    g = ImageDraw.Draw(glow)
    g.ellipse((W - 620, -380, W + 260, 420), fill=a)
    g.ellipse((-360, H - 300, 420, H + 380), fill=tuple(int(c * 0.55) for c in a))
    glow = glow.filter(ImageFilter.GaussianBlur(170))
    img = Image.blend(img, glow, 0.55)
    d = ImageDraw.Draw(img)
    grid = img.copy(); gd = ImageDraw.Draw(grid)
    for x in range(0, W, 64):                      # faint grid
        gd.line([(x, 0), (x, H)], fill=(255, 255, 255), width=1)
    for y in range(0, H, 64):
        gd.line([(0, y), (W, y)], fill=(255, 255, 255), width=1)
    img = Image.blend(img, grid, 0.05)
    d = ImageDraw.Draw(img)

    brand = _font(BOLD, 26)
    d.text((64, 52), "EHBEHZAD  ·  AI NEWS", font=brand, fill=(255, 255, 255))
    pill_f = _font(BOLD, 30)
    tw = d.textlength(source, font=pill_f)
    x1 = W - 64; x0 = x1 - tw - 56
    d.rounded_rectangle((x0, 44, x1, 100), radius=28, fill=a)
    d.text((x0 + 28, 50), source, font=pill_f, fill=(10, 10, 14))

    size = 74
    while size > 40:
        f = _font(BOLD, size)
        lines = _wrap(d, title, f, W - 160)
        if len(lines) <= 4:
            break
        size -= 6
    lh = int(size * 1.45)
    y = (H - lh * len(lines)) // 2 + 20
    for ln in lines:
        _rtl(d, W - 80, y, ln, f, (255, 255, 255))
        y += lh
    d.rectangle((W - 80 - 140, y + 6, W - 80, y + 14), fill=a)

    foot = _font(MED, 28)
    d.text((64, H - 84), "@ehbehzad_ai", font=_font(BOLD, 30), fill=a)
    note = "خبرهای روز هوش مصنوعی به فارسی"
    _rtl(d, W - 64, H - 82, note, foot, (210, 212, 220))
    img.save(out, "JPEG", quality=90)
    return out


if __name__ == "__main__":
    import sys
    print(card(sys.argv[1], sys.argv[2], sys.argv[3]))
