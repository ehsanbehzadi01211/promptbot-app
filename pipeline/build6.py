"""V6 'studio' series (making images / video with ChatGPT): build5 motion system plus a
viewfinder identity (crop brackets, selection handles, running timecode on video episodes)
and three subject-specific scenes: grid (edit toolbox), sketch (doodle -> finished image),
board (storyboard strip with a playhead).
Usage: python3 build6.py <key> <voice.mp3> [scripts.json]   (FRAMES=1,2 -> debug stills)"""
import sys
import build5 as B5
from build2 import esc

FA = "۰۱۲۳۴۵۶۷۸۹"

B5.CSS = B5.CSS.replace(".steps{", ".slist{") + """
@property --tc{syntax:'<integer>';inherits:false;initial-value:0}
/* viewfinder: the frame every scene sits in */
.vf{position:absolute;left:36px;right:36px;top:196px;bottom:300px;pointer-events:none}
.vf b{position:absolute;width:74px;height:74px;border:5px solid rgba(255,255,255,.85)}
.vf b:nth-child(1){top:0;right:0;border-left:0;border-bottom:0}
.vf b:nth-child(2){top:0;left:0;border-right:0;border-bottom:0}
.vf b:nth-child(3){bottom:0;right:0;border-left:0;border-top:0}
.vf b:nth-child(4){bottom:0;left:0;border-right:0;border-top:0}
.vf i{position:absolute;width:18px;height:18px;background:var(--a);border:3px solid #fff}
.vf i:nth-of-type(1){top:-7px;right:-7px}.vf i:nth-of-type(2){top:-7px;left:-7px}
.vf i:nth-of-type(3){bottom:-7px;right:-7px}.vf i:nth-of-type(4){bottom:-7px;left:-7px}
.rec{position:absolute;left:66px;bottom:330px;display:flex;align-items:center;gap:14px;font-size:34px;font-weight:700;direction:ltr;text-shadow:0 2px 10px rgba(0,0,0,.8);font-variant-numeric:tabular-nums}
.rec u{width:20px;height:20px;border-radius:50%;background:#ff3b30;box-shadow:0 0 14px #ff3b30;animation:blink2 1s steps(1) 0s infinite}
.rec s{text-decoration:none;counter-reset:t var(--tc);animation:tick linear both}
.rec s::after{content:"00:" counter(t,decimal-leading-zero)}
@keyframes tick{from{--tc:0}to{--tc:var(--end)}}
/* hub: Claude wired to apps */
.hubtop{display:flex;align-items:center;gap:22px;align-self:flex-start;margin:10px 0 26px;padding:16px 34px 16px 20px;border-radius:70px;background:var(--a);color:#0b0b0f;font-size:58px;font-weight:900;direction:ltr}
.hubtop svg{width:76px;height:76px;padding:14px;border-radius:50%;background:#0b0b0f;color:var(--a)}
.hub .rail{top:-30px}
.hub .rail::after{content:"";position:absolute;left:-6px;width:18px;height:60px;border-radius:9px;background:#fff;box-shadow:0 0 22px 6px var(--a);animation:pulse2 1.6s linear 0s infinite}
@keyframes pulse2{from{top:-60px}to{top:100%}}
.hub .nd svg{width:66px;height:66px}
.hub .bx b{direction:ltr;text-align:right;font-size:60px}
.hub .bx small{font-size:36px}
/* grid: edit toolbox */
.tgrid{width:100%;display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-top:34px}
.tile{padding:34px 26px 30px;border-radius:30px;display:flex;flex-direction:column;align-items:center;gap:14px}
.tile .ti{width:150px;height:150px;border-radius:26px;display:grid;place-items:center;color:#0b0b0f;background:var(--a);position:relative;overflow:hidden}
.tile .ti svg{width:92px;height:92px;position:relative}
.tile .ti.chk{background:repeating-conic-gradient(#fff 0 25%,#cfd2d8 0 50%) 0 0/38px 38px}
.tile b{font-size:50px;font-weight:900;line-height:1.3}
.tile small{font-size:34px;font-weight:700;opacity:.82;line-height:1.4}
/* sketch: doodle becomes a finished picture */
.stage{position:relative;width:820px;height:640px;margin-top:30px;border-radius:26px;background:#f3efe6;overflow:hidden;box-shadow:0 30px 90px rgba(0,0,0,.5)}
.stage svg{position:absolute;inset:0;width:100%;height:100%}
.stage .dd path,.stage .dd circle{fill:none;stroke:#23252b;stroke-width:7;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1;animation:draw 1s ease-in-out both}
@keyframes draw{to{stroke-dashoffset:0}}
.stage .fin{animation:reveal 1.1s cubic-bezier(.7,0,.2,1) both}
@keyframes reveal{from{clip-path:inset(0 0 0 100%)}to{clip-path:inset(0 0 0 0)}}
.stage .scan{position:absolute;top:0;bottom:0;width:10px;background:#fff;box-shadow:0 0 30px 8px var(--a);right:-20px;animation:scan 1.1s cubic-bezier(.7,0,.2,1) both}
@keyframes scan{0%{right:-20px;opacity:1}99%{opacity:1}100%{right:100%;opacity:0}}
.sw{position:relative}
.sw .h{position:absolute;width:22px;height:22px;background:#fff;border:4px solid var(--a);z-index:2}
.sw .h:nth-child(1){top:20px;right:-11px}.sw .h:nth-child(2){top:20px;left:-11px}
.sw .h:nth-child(3){bottom:-11px;right:-11px}.sw .h:nth-child(4){bottom:-11px;left:-11px}
.caps{position:relative;height:80px;margin-top:34px;width:100%}
.caps span{position:absolute;left:0;right:0;font-size:50px;font-weight:900;text-shadow:0 4px 20px rgba(0,0,0,.7)}
.caps .c1{animation:rise .6s cubic-bezier(.16,1,.3,1) both,capout .4s ease forwards}
@keyframes capout{to{opacity:0;transform:translateY(-30px)}}
.caps .c2{color:var(--a)}
/* board: storyboard strip */
.sboard{width:100%;display:flex;gap:22px;margin-top:40px;direction:rtl}
.pn{flex:1;display:flex;flex-direction:column;align-items:center}
.pn .fr{width:100%;aspect-ratio:9/14;border-radius:22px;position:relative;display:grid;place-items:center;font-size:150px;font-weight:900;color:var(--a)}
.pn .fr::after{content:"";position:absolute;left:18px;right:18px;top:16px;height:16px;background:repeating-linear-gradient(90deg,rgba(255,255,255,.5) 0 18px,transparent 18px 34px);border-radius:4px}
.pn b{margin-top:22px;font-size:46px;font-weight:900}
.pn small{margin-top:6px;font-size:32px;font-weight:700;opacity:.82}
.tl{position:relative;width:100%;height:14px;margin-top:40px;border-radius:8px;background:rgba(255,255,255,.2);direction:rtl}
.tl i{position:absolute;top:-16px;bottom:-16px;width:8px;border-radius:4px;background:#fff;box-shadow:0 0 18px 4px var(--a);right:0;animation:play linear both}
@keyframes play{from{right:0}to{right:calc(100% - 8px)}}
.tl u{position:absolute;inset:0;border-radius:8px;background:var(--a);transform-origin:right;animation:segfill linear both}
"""

TOOL = {
    "bg": ('chk', '<svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4" fill="#0b0b0f"/><path d="M4 22c0-5 3.5-8 8-8s8 3 8 8z" fill="#0b0b0f"/></svg>'),
    "erase": ('', '<svg viewBox="0 0 24 24"><path d="M14.5 4.5l5 5-9 9H6l-2-2a2 2 0 010-2.8z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/><path d="M9.5 9.5l5 5M10 20h10" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>'),
    "resize": ('', '<svg viewBox="0 0 24 24"><path d="M4 9V4h5M20 15v5h-5M4 4l6.5 6.5M20 20l-6.5-6.5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'),
    "comment": ('', '<svg viewBox="0 0 24 24"><path d="M4 5h16v11H10l-5 4v-4H4z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/><path d="M8 9h8M8 12.5h5" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>'),
}

DOODLE = ('<svg class="dd" viewBox="0 0 820 640">'
          '<circle cx="590" cy="190" r="74" pathLength="1" style="{d0}"/>'
          '<path d="M40 500 L250 230 L360 380 L470 260 L780 505" pathLength="1" style="{d1}"/>'
          '<path d="M60 560 C200 530 300 590 430 560 S680 540 770 570" pathLength="1" style="{d2}"/>'
          '<path d="M590 60v34M590 286v34M460 190h34M686 190h34M498 98l24 24M658 258l24 24M682 98l-24 24M522 258l-24 24" pathLength="1" style="{d3}"/></svg>')
FINAL = ('<svg class="fin" viewBox="0 0 820 640" style="{d}"><defs>'
         '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b1b5a"/><stop offset=".45" stop-color="#e8527a"/><stop offset=".8" stop-color="#ffb347"/></linearGradient>'
         '<radialGradient id="sun"><stop offset="0" stop-color="#fff6d6"/><stop offset=".45" stop-color="#ffd15c"/><stop offset="1" stop-color="#ffd15c" stop-opacity="0"/></radialGradient>'
         '<linearGradient id="m1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7a3b7f"/><stop offset="1" stop-color="#3a2060"/></linearGradient>'
         '<linearGradient id="m2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3b2a6b"/><stop offset="1" stop-color="#17123a"/></linearGradient>'
         '<linearGradient id="wt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff9d5c"/><stop offset="1" stop-color="#3a2060"/></linearGradient></defs>'
         '<rect width="820" height="640" fill="url(#sky)"/><circle cx="590" cy="190" r="190" fill="url(#sun)"/><circle cx="590" cy="190" r="66" fill="#fff3c4"/>'
         '<path d="M0 520 L150 330 L250 430 L400 250 L560 440 L680 350 L820 500 V640 H0z" fill="url(#m1)"/>'
         '<path d="M0 560 L250 230 L360 380 L470 260 L820 540 V640 H0z" fill="url(#m2)"/>'
         '<path d="M250 230 L300 300 L262 290 L232 322 L212 280z M470 260 L520 318 L480 306 L452 330 L440 294z" fill="#ffe9d6" opacity=".9"/>'
         '<rect y="548" width="820" height="92" fill="url(#wt)" opacity=".92"/>'
         '<path d="M500 572h180M540 596h110M90 584h150M300 610h120" stroke="#fff3c4" stroke-width="5" stroke-linecap="round" opacity=".6"/></svg>')

PLUG = '<svg viewBox="0 0 24 24"><path d="M9 3v5M15 3v5M6 8h12v4a6 6 0 01-12 0zM12 18v3" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
_base = B5.scene_html

def scene_html(sc, st, dur):
    d = lambda off: f"animation-delay:{st+off:.3f}s"
    t = sc["type"]
    life = f"animation:enter .55s cubic-bezier(.16,1,.3,1) {st:.3f}s both,leave .32s ease-in {st+dur-0.32:.3f}s forwards"
    first = sc.get("first", 0.5)
    if t == "steps":
        n = len(sc["items"]); span = (sc['at'][-1] - sc['at'][0]) if sc.get('at') else max(1.0, (dur - first) * (n - 1) / n - 0.2)
        first = sc['at'][0] if sc.get('at') else first; items = ""
        for i, (lab, txt) in enumerate(sc["items"]):
            at = sc['at'][i] if sc.get('at') else first + span * i / max(1, n - 1)
            items += (f'<div class="st" style="{d(at)}"><div class="nd">{FA[i+1]}</div>'
                      f'<div class="bx gb fromL" style="{d(at + 0.05)}"><small>{esc(lab)}</small><b>{esc(txt)}</b></div></div>')
        body = (f'<div class="steps-k rise" style="{d(0.0)}">{esc(sc["kicker"])}</div>'
                f'<div class="slist"><div class="rail"><i style="{d(first)};animation-duration:{span:.2f}s"></i></div>{items}</div>')
    elif t == "hub":
        n = len(sc["items"]); span = (sc['at'][-1] - sc['at'][0]) if sc.get('at') else max(1.0, (dur - first) * (n - 1) / n - 0.2)
        first = sc['at'][0] if sc.get('at') else first; items = ""
        for i, (role, app) in enumerate(sc["items"]):
            at = sc['at'][i] if sc.get('at') else first + span * i / max(1, n - 1)
            items += (f'<div class="st" style="{d(at)}"><div class="nd">{PLUG}</div>'
                      f'<div class="bx gb fromL" style="{d(at + 0.05)}"><small>{esc(role)}</small><b>{esc(app)}</b></div></div>')
        body = (f'<div class="steps-k rise" style="{d(0.0)}">{esc(sc["kicker"])}</div>'
                f'<div class="hubtop pop" style="{d(0.3)}">{B5.ICON["spark"]}Claude</div>'
                f'<div class="slist"><div class="rail"><i style="{d(first - 0.4)};animation-duration:{span + 0.4:.2f}s"></i></div>{items}</div>')
    elif t == "grid":
        n = len(sc["items"]); span = (sc['at'][-1] - sc['at'][0]) if sc.get('at') else max(1.0, (dur - first) * (n - 1) / n - 0.2)
        first = sc['at'][0] if sc.get('at') else first; tiles = ""
        for i, (ic, title, sub) in enumerate(sc["items"]):
            at = sc['at'][i] if sc.get('at') else first + span * i / max(1, n - 1); cls, svg = TOOL[ic]
            tiles += (f'<div class="tile gb flip" style="{d(at)}"><div class="ti {cls}">{svg}</div>'
                      f'<b>{esc(title)}</b><small>{esc(sub)}</small></div>')
        body = f'<div class="steps-k rise" style="{d(0.0)}">{esc(sc["kicker"])}</div><div class="tgrid">{tiles}</div>'
    elif t == "sketch":
        turn = max(3.2, dur * 0.58)
        dd = DOODLE.format(d0=d(0.7), d1=d(1.4) + ";animation-duration:1.3s", d2=d(2.4), d3=d(2.0))
        body = (f'<div class="kicker rise" style="{d(0.0)}">{esc(sc["kicker"])}</div>'
                f'<div class="sw rise" style="{d(0.2)}"><i class="h"></i><i class="h"></i><i class="h"></i><i class="h"></i>'
                f'<div class="stage">{dd}{FINAL.format(d=d(turn))}<span class="scan" style="{d(turn)}"></span></div></div>'
                f'<div class="caps"><span class="c1" style="animation-delay:{st+0.5:.3f}s,{st+turn:.3f}s">{esc(sc["cap1"])}</span>'
                f'<span class="c2 rise" style="{d(turn + 0.5)}">{esc(sc["cap2"])}</span></div>')
    elif t == "board":
        n = len(sc["items"]); span = (sc['at'][-1] - sc['at'][0]) if sc.get('at') else max(1.0, (dur - first) * (n - 1) / n - 0.2)
        first = sc['at'][0] if sc.get('at') else first; pn = ""
        for i, (title, sub) in enumerate(sc["items"]):
            at = sc['at'][i] if sc.get('at') else first + span * i / max(1, n - 1)
            pn += (f'<div class="pn"><div class="fr gb flip" style="{d(at)}">{FA[i+1]}</div>'
                   f'<b class="rise" style="{d(at + 0.25)}">{esc(title)}</b><small class="rise" style="{d(at + 0.4)}">{esc(sub)}</small></div>')
        body = (f'<div class="steps-k rise" style="{d(0.0)}">{esc(sc["kicker"])}</div><div class="sboard">{pn}</div>'
                f'<div class="tl rise" style="{d(first - 0.2)}"><u style="{d(first)};animation-duration:{span + 0.8:.2f}s"></u>'
                f'<i style="{d(first)};animation-duration:{span + 0.8:.2f}s"></i></div>')
    else:
        return _base(sc, st, dur)
    return f'<section class="scene {t}" style="{life}">{body}</section>'

class _Chrome:
    """the viewfinder is page-level, so it rides in front of the first scene's markup"""
    video = False; total = 40; on = True
    @classmethod
    def html(cls):
        rec = (f'<div class="rec"><u></u><s style="--end:{int(cls.total)};animation-duration:{int(cls.total)}s"></s></div>' if cls.video else "")
        if not cls.on: return ''
        return f'<div class="vf"><b></b><b></b><b></b><b></b><i></i><i></i><i></i><i></i></div>{rec}'

def _wrapped(sc, st, dur):
    out = scene_html(sc, st, dur)
    return (_Chrome.html() + out) if st == 0 else out

B5.scene_html = _wrapped

def run(key, voice, specfile="scripts8.json"):
    import json, os, subprocess
    spec = json.load(open(os.path.join(B5.ROOT, specfile)))[key]
    _Chrome.video = "ویدیو" in spec["tag"]; _Chrome.on = spec.get("chrome", True)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", voice],
                               capture_output=True, text=True).stdout.strip())
    _Chrome.total = dur + 1.4
    if spec.get("cuts"):
        from align import boundaries as _b
        B5.boundaries = lambda path, sents: (list(spec["cuts"]),) + tuple(_b(path, sents)[1:])
    B5.run(key, voice, specfile)

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], *(sys.argv[3:4]))
