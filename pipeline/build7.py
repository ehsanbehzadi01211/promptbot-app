"""V7 'hook-first' reels: build6 plus three changes aimed at 3-second retention.
1. The opening claim is fully on screen at frame 0 (no entrance animation); the only motion in the
   first second is the highlight sweep. Voice starts 0.12 s in instead of 0.35 s.
2. `ask`  - closing scene that asks for a one-word comment (options shown as chips).
3. `offer`- closing scene that invites a DM (used on the web-design reels).
Usage: python3 build7.py <key> <voice.mp3> [scripts.json]   (FRAMES=0,1 -> debug stills)"""
import re, sys
import build6 as B6
from build2 import esc, HANDLE, ICON

B5 = B6.B5
B5.LEAD = 0.12

BUBBLE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">'
          '<path d="M21 11.5a8.4 8.4 0 0 1-12.3 7.4L3 20.5l1.7-5.2A8.4 8.4 0 1 1 21 11.5z"/></svg>')
PLANE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">'
         '<path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4z"/></svg>')

B5.CSS += """
.cmt{display:flex;align-items:center;gap:20px;font-size:56px;font-weight:900;padding:18px 46px;border-radius:70px;background:var(--a);color:#0b0b0f;margin-bottom:50px;box-shadow:0 18px 50px rgba(0,0,0,.45)}
.cmt svg{width:68px;height:68px}
.ask .cta-t{font-size:92px}
.ask .chips{margin-top:54px;gap:24px}
.ask .chip{font-size:56px;padding:18px 44px;background:rgba(8,8,14,.72);color:#fff;border:4px solid var(--a)}
.offer .follow{display:flex;align-items:center;gap:22px;padding:26px 64px;font-size:60px}
.offer .follow svg{width:62px;height:62px}
.offer .cta-t{font-size:96px}
"""

# story mode: Instagram covers the top ~200px with its own header, so the reel header goes and a sticker takes its place
STORY_CSS = """
.head,.segs{display:none}
.stk{position:absolute;top:250px;right:70px;z-index:5;font-size:54px;font-weight:900;color:#0b0b0f;background:var(--a);padding:8px 38px 14px;border-radius:20px;transform:rotate(3deg);box-shadow:0 18px 44px rgba(0,0,0,.5);direction:rtl}
.scene{top:330px;bottom:330px}
.hook-t{font-size:136px}
.tname{font-size:92px;font-weight:900;direction:ltr;margin-bottom:38px;text-shadow:0 6px 30px rgba(0,0,0,.7)}
.tname small{display:block;font-size:40px;font-weight:700;opacity:.85;direction:rtl}
.tnote{margin-top:40px;font-size:48px;font-weight:900;padding:16px 40px;border-radius:60px;background:rgba(8,8,12,.75);border:3px solid var(--a);direction:rtl}
"""
STICKER = ""

_prev = B5.scene_html   # build6's wrapped renderer

def scene_html(sc, st, dur):
    d = lambda off: f"animation-delay:{st+off:.3f}s"
    t = sc["type"]
    leave = f"leave .32s ease-in {st+dur-0.32:.3f}s forwards"
    if t == "hook" and st == 0:
        w, n = B5.kwords(sc["title"], -2.0, 0.0, slam=True)          # words already landed at frame 0
        w = re.sub(r'(<mark style="animation-delay:)-?[\d.]+s', r'\g<1>0.200s', w)   # the one early motion
        body = f'<div class="hook-t slam">{w}</div>'
        if sc.get("sub"):
            body += f'<div class="pill rise" style="{d(0.5)}">{esc(sc["sub"])}</div>'
        return STICKER + B6._Chrome.html() + f'<section class="scene hook" style="animation:{leave}">{body}</section>'
    if t == "ask":
        w, n = B5.kwords(sc["title"], st + 0.2, 0.09)
        chips = "".join(f'<span class="chip pop" style="{d(sc.get("chips_at", 0.8 + n * 0.09) + i * 0.22)}">{esc(c)}</span>'
                        for i, c in enumerate(sc.get("chips", [])))
        body = (f'<div class="cmt pop" style="{d(0.0)}">{BUBBLE}<b>کامنت کن</b></div>'
                f'<div class="cta-t">{w}</div>'
                + (f'<div class="chips">{chips}</div>' if chips else "")
                + (f'<div class="p-s rise" style="{d(1.0 + n * 0.09)}">{esc(sc["sub"])}</div>' if sc.get("sub") else ""))
    elif t == "tool":
        import build3 as B3
        body = (f'<div class="tname rise" style="{d(0.0)}">{esc(sc["name"])}'
                + (f'<small>{esc(sc["aka"])}</small>' if sc.get("aka") else "") + '</div>'
                f'<div class="io-in fromR" style="{d(0.35)}"><div class="io-ic">{B3.ICON3["menu"]}</div>'
                f'<div><small>تو می‌دی</small><b>{esc(sc["inp"])}</b></div></div>'
                f'<div class="io-ar pop" style="{d(1.5)}">{B3.ICON3["arrow"]}</div>'
                f'<div class="io-out fromL" style="{d(2.0)}"><div class="io-ic">{B3.ICON3["spark"]}</div>'
                f'<div><small>تحویل می‌گیری</small><b>{esc(sc["out"])}</b></div></div>'
                f'<div class="tnote pop" style="{d(3.4)}">{esc(sc["note"])}</div>')
    elif t == "offer":
        w, n = B5.kwords(sc["title"], st + 0.3, 0.1)
        body = (f'<div class="prof pop" style="{d(0.0)}"><div class="av">{ICON["spark"]}</div><div class="hd" dir="ltr">{HANDLE}</div></div>'
                f'<div class="cta-t">{w}</div>'
                f'<div class="fw pop" style="{d(0.6 + n * 0.1)}"><span class="rip"></span><span class="rip r2"></span>'
                f'<div class="follow">{PLANE}<span>دایرکت پیام بده</span></div></div>'
                + (f'<div class="p-s rise" style="{d(0.9 + n * 0.1)}">{esc(sc["sub"])}</div>' if sc.get("sub") else ""))
    else:
        return _prev(sc, st, dur)
    return f'<section class="scene {t}" style="animation:enter .55s cubic-bezier(.16,1,.3,1) {st:.3f}s both,{leave}">{body}</section>'

B5.scene_html = scene_html

def run(key, voice, specfile="scripts10.json"):
    """`silent: <seconds>` + `scuts` in the spec -> music-and-text reel with no voiceover"""
    import json, os, subprocess
    spec = json.load(open(os.path.join(B5.ROOT, specfile)))[key]
    if spec.get("story"):
        global STICKER
        B5.CSS += STORY_CSS; STICKER = f'<div class="stk">{esc(spec["story"])}</div>'
    if spec.get("silent"):
        D = float(spec["silent"]); voice = os.path.join(B5.ROOT, "out", key + "_silence.mp3")
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", str(D), voice], check=True)
        B5.boundaries = lambda p, sents: (list(spec["scuts"]), 0.0, D, D)
    B6.run(key, voice, specfile)

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], *(sys.argv[3:4]))
