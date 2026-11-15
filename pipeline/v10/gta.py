# GTA VI news reels (owner, 15 Nov 2026): every frame is official Rockstar footage / screenshots,
# with Persian word-by-word subtitles, "mission-title" cards, the GTA-outfit robot host and the follow card.
#   python3 gta.py <key> [--stills]      spec in gta.json, words in words10/<key>.json
# Footage: ../../footage/<name>_NN.mp4 (fetch-yt workflow, Rockstar CDN), stills: ../../media/gta6_*.jpg
import json, os, re, subprocess, sys, html, base64
from playwright.sync_api import sync_playwright
from build9 import bed, final_mix, W, H, FPS, LEAD, FONT, ROOT

TAIL = 3.4
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
E = html.escape
OUT = os.path.join(ROOT, "out")


def seg_cmd(shot, dur, path):
    fx = shot.get("fx", 0.5)
    n = max(1, round(dur * FPS))
    if "v" in shot:
        src = os.path.join(REPO, "footage", shot["v"])
        z = shot.get("z", 1.0)
        vf = (f"scale=-2:{int(1920 * z)},crop=1080:1920:(iw-1080)*{fx}:(ih-1920)/2,setsar=1,fps={FPS},"
              "eq=contrast=1.06:saturation=1.12")
        return ["ffmpeg", "-v", "error", "-y", "-ss", str(shot.get("ss", 0)), "-i", src, "-t", f"{dur:.3f}",
                "-vf", vf, "-frames:v", str(n), "-an", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
                "-pix_fmt", "yuv420p", path]
    src = os.path.join(REPO, "media", shot["i"])
    zin = shot.get("zoom", "in") == "in"
    zexpr = f"1+0.10*on/{n}" if zin else f"1.10-0.10*on/{n}"
    pan = shot.get("pan", 0)  # -1..1 horizontal drift
    vf = (f"scale=-2:2400,crop=1350:2400:(iw-1350)*{fx}:0,"
          f"zoompan=z='{zexpr}':x='(iw-iw/zoom)/2+{pan}*(iw-iw/zoom)/2*(on/{n}*2-1)':y='(ih-ih/zoom)/2':d={n}:s=1080x1920:fps={FPS},"
          "setsar=1,eq=contrast=1.05:saturation=1.1")
    return ["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", src, "-vf", vf, "-frames:v", str(n), "-an",
            "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", path]


CSS = """
@font-face{font-family:Vaz;font-weight:800;src:url(FONT/vazirmatn/files/vazirmatn-arabic-800-normal.woff2)}
@font-face{font-family:Vaz;font-weight:900;src:url(FONT/vazirmatn/files/vazirmatn-arabic-900-normal.woff2)}
@font-face{font-family:Vaz;font-weight:800;src:url(FONT/vazirmatn/files/vazirmatn-latin-800-normal.woff2);unicode-range:U+0000-00FF}
@font-face{font-family:Vaz;font-weight:900;src:url(FONT/vazirmatn/files/vazirmatn-latin-900-normal.woff2);unicode-range:U+0000-00FF}
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:transparent;font-family:Vaz}
#vt{position:absolute;left:0;right:0;top:0;height:420px;background:linear-gradient(180deg,rgba(0,0,0,.62),rgba(0,0,0,0))}
#vb{position:absolute;left:0;right:0;bottom:0;height:760px;background:linear-gradient(0deg,rgba(0,0,0,.78),rgba(0,0,0,0))}
#hdl{position:absolute;right:40px;top:58px;padding:10px 24px;border-radius:30px;font-weight:800;font-size:30px;color:#fff;
  background:rgba(0,0,0,.45);border:2px solid rgba(255,255,255,.25);direction:ltr}
#tag{position:absolute;right:40px;top:132px;padding:8px 22px;border-radius:10px;font-weight:900;font-size:30px;color:#111;
  background:linear-gradient(90deg,#ffd23f,#ff9a3c);transform:skew(-8deg);letter-spacing:1px;direction:ltr}
#subs{position:absolute;left:60px;right:60px;top:1395px;text-align:center;direction:rtl;font-weight:900;font-size:70px;line-height:1.5;color:#fff;
  -webkit-text-stroke:2px #000;paint-order:stroke fill;text-shadow:0 6px 0 #000,0 8px 24px rgba(0,0,0,.8)}
#subs span{display:inline-block;margin:0 9px;transition:none}
#subs span.on{color:#fff;background:linear-gradient(90deg,#ff2d8a,#ff7a2f);border-radius:16px;padding:0 16px;-webkit-text-stroke:0;
  text-shadow:0 4px 0 rgba(0,0,0,.5);box-shadow:0 8px 30px rgba(255,45,138,.55)}
.card{position:absolute;left:0;right:0;top:470px;text-align:center;opacity:0}
.card .t{display:inline-block;font-weight:900;font-size:150px;line-height:1.05;direction:ltr;transform:skew(-7deg);
  background:linear-gradient(180deg,#fff2a8 0%,#ffd23f 35%,#ff7a2f 75%,#ff2d8a 100%);-webkit-background-clip:text;color:transparent;
  -webkit-text-stroke:5px #000;paint-order:stroke fill;filter:drop-shadow(0 10px 0 #000) drop-shadow(0 18px 40px rgba(0,0,0,.6))}
.card .t.fa{direction:rtl;font-size:118px}
.card .s{margin-top:10px;display:inline-block;font-weight:900;font-size:44px;color:#fff;background:rgba(0,0,0,.6);padding:6px 26px;border-radius:12px;
  border:2px solid rgba(255,255,255,.25);direction:rtl}
#fol{position:absolute;inset:0;background:rgba(0,0,0,.7);opacity:0;display:flex;align-items:center;justify-content:center}
#fol .fc{width:720px;padding:60px 40px 56px;border-radius:44px;text-align:center;background:linear-gradient(160deg,#2a1530,#120c18);
  border:3px solid #ff2d8a;box-shadow:0 40px 120px rgba(0,0,0,.7),0 0 60px rgba(255,45,138,.35)}
#fol .av{width:230px;height:230px;margin:0 auto;border-radius:50%;background-size:cover;background-position:50% 18%;border:7px solid #ffd23f}
#fol .hd{margin-top:28px;font-weight:900;font-size:60px;color:#fff;direction:ltr}
#fol .tg{margin-top:6px;font-weight:800;font-size:36px;color:#c9b8d6}
#fol .bt{display:inline-block;margin-top:34px;padding:18px 64px;border-radius:60px;font-weight:900;font-size:48px;color:#fff;
  background:linear-gradient(90deg,#ff2d8a,#ff7a2f);box-shadow:0 14px 40px rgba(255,45,138,.5)}
"""

JS = r"""
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)), eo=x=>1-Math.pow(1-cl(x),3);
const subs=document.getElementById('subs'); let lastG=-1;
window.tick=function(t){
  // subtitles: one group at a time, current word highlighted
  let cur=-1; for(let i=0;i<WORDS.length;i++){ if(t>=WORDS[i][1]) cur=i; }
  const g = cur>=0 ? WORDS[cur][2] : -1;
  if(g!==lastG){ subs.innerHTML = WORDS.map((w,i)=>w[2]===g?`<span data-i="${i}">${w[0]}</span>`:'').join(''); lastG=g; }
  subs.querySelectorAll('span').forEach(s=>{const i=+s.dataset.i; s.classList.toggle('on', i===cur);});
  const sa = cur>=0 ? WORDS.find(w=>w[2]===g)[1] : 0; const q=eo((t-sa)/.18);
  subs.style.opacity = (t<window.FOL? (cur>=0?1:0) : 0); subs.style.transform=`translateY(${(1-q)*24}px) scale(${.96+.04*q})`;
  // cards
  for(const c of CARDS){ const el=document.getElementById(c.id); const a=c.a, b=c.b;
    const kin=eo((t-a)/.28), kout=cl((b-t)/.25); const on=(t>=a&&t<b)?1:0;
    el.style.opacity = on*Math.min(kin,kout);
    el.style.transform = `translateY(${(1-kin)*-60}px) scale(${1.25-.25*kin})`; }
  const fo=document.getElementById('fol'); const fq=cl((t-window.FOL)/.5); fo.style.opacity=fq;
  fo.firstElementChild.style.transform=`translateY(${(1-eo(fq))*70}px) scale(${.93+.07*eo(fq)})`;
};
"""


def build(key):
    spec = json.load(open(os.path.join(ROOT, "gta.json")))[key]
    words = json.load(open(os.path.join(ROOT, "words10", key + ".json")))
    toks = spec["voice"].replace("[excited]", "").split()
    ts = [LEAD + x for x in words["t"]]
    assert len(ts) == len(toks), (len(ts), len(toks))
    T = lambda i: round(ts[min(int(i), len(ts) - 1)], 3)
    total = LEAD + words["end"] + TAIL
    os.makedirs(OUT, exist_ok=True)

    # ---- background: official footage / screenshots, cut on the narration
    shots = spec["shots"]
    starts = [0.0] + [T(s["w"]) - .08 for s in shots[1:]]
    ends = starts[1:] + [total]
    segs = []
    stills = "--stills" in sys.argv
    if not stills:
        lst = os.path.join(OUT, f"{key}_segs.txt")
        with open(lst, "w") as f:
            for k, (s, a, b) in enumerate(zip(shots, starts, ends)):
                p = os.path.join(OUT, f"{key}_seg{k:02d}.mp4")
                subprocess.run(seg_cmd(s, b - a, p), check=True)
                f.write(f"file '{p}'\n"); segs.append(p)
        bgv = os.path.join(OUT, f"{key}_bg.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", bgv], check=True)

    # ---- overlay page (transparent)
    groups, g, cnt = [], 0, 0
    for w in toks:
        groups.append(g); cnt += 1
        if re.search(r"[.!؟?؛،:,]$", w) or cnt >= 4:
            g += 1; cnt = 0
    clean = lambda w: E(re.sub(r"[«»]", "", w))
    WORDS = [[clean(w), round(a, 3), gg] for w, a, gg in zip(toks, ts, groups)]
    cards, CARDS = [], []
    for k, c in enumerate(spec.get("cards", [])):
        a = T(c["w"]) - .05
        b = T(c["until"]) - .1 if "until" in c else a + c.get("dur", 2.4)
        cls = "t fa" if re.search(r"[؀-ۿ]", c["text"]) and not c.get("ltr") else "t"
        sub = f'<br><div class="s">{E(c["sub"])}</div>' if c.get("sub") else ""
        cards.append(f'<div class="card" id="c{k}"><div class="{cls}">{E(c["text"])}</div>{sub}</div>')
        CARDS.append({"id": f"c{k}", "a": round(a, 3), "b": round(b, 3)})
    robot = os.path.join(REPO, "media", "mascot_2_robot_gta.jpg")
    av = base64.b64encode(open(robot, "rb").read()).decode()
    fol = (f'<div id="fol"><div class="fc"><div class="av" style="background-image:url(data:image/jpeg;base64,{av})"></div>'
           f'<div class="hd">@ehbehzad</div><div class="tg">ترفندهای هوش مصنوعی</div><div class="bt">+ فالو</div></div></div>')
    from host import robot_block, words_to_spans
    hb = robot_block("file://" + robot, words_to_spans(ts, total - 1.0), [[0, "corner"]], "#ff2d8a")
    # the GTA robot's screen sits a little lower/right than the original glass robot's
    dx, dy = spec.get("eye_dx", 14), spec.get("eye_dy", 26)
    hb = (hb.replace("top:196px", f"top:{196 + dy}px").replace("[[eL,215],[eR,305]]", f"[[eL,{215 + dx}],[eR,{305 + dx}]]")
            .replace("left:260px;top:292px", f"left:{260 + dx}px;top:{292 + dy}px")
            .replace("m.style.top=(290-o*10)+'px'", f"m.style.top=({290 + dy}-o*10)+'px'")
            .replace("m.style.top='280px'", f"m.style.top='{280 + dy}px'")
            .replace("m.style.marginLeft=(-w/2)+'px'", f"m.style.marginLeft=(-w/2)+'px'")
            .replace("background-size:553px 737px", "background-size:553px 737px;background-position:0 0"))
    hb = hb.replace("#host{", "#host{border-color:#ffd23f!important;", 1)
    host = ('<script>window.HOSTPOS={big:{d:190,x:40,y:56},corner:{d:190,x:40,y:56},off:{d:190,x:40,y:56}}</script>' + hb)
    page = (f'<!doctype html><html lang="fa"><head><meta charset="utf-8"><style>{CSS.replace("FONT", FONT)}</style></head><body>'
            f'<div id="vt"></div><div id="vb"></div><div id="hdl">@ehbehzad</div><div id="tag">GTA VI</div>{"".join(cards)}'
            f'<div id="subs"></div>{fol}'
            f'<script>window.WORDS={json.dumps(WORDS, ensure_ascii=False)};window.CARDS={json.dumps(CARDS)};window.FOL={total - 2.6:.3f};{JS}</script>'
            f'{host}</body></html>')
    hp = os.path.join(OUT, f"{key}_gta.html"); open(hp, "w").write(page)
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={"width": W, "height": H})
        pg.goto("file://" + hp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(600)
        if stills:
            from PIL import Image
            import io
            for k, (s, a, b) in enumerate(zip(shots, starts, ends)):
                tt = min(b - .2, a + 1.0)
                pg.evaluate("t=>window.tick(t)", tt)
                ov = Image.open(io.BytesIO(pg.screenshot(omit_background=True))).convert("RGBA")
                # cheap preview of the background frame
                bgp = os.path.join(OUT, f"{key}_bgstill.png")
                c = seg_cmd(s, 1 / FPS, bgp)
                c = [x for x in c if x not in ("-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p")]
                subprocess.run(c, check=True)
                bgi = Image.open(bgp).convert("RGBA").resize((W, H))
                Image.alpha_composite(bgi, ov).convert("RGB").save(os.path.join(OUT, f"{key}_gta_{k:02d}_{tt:05.2f}.jpg"), quality=85)
            pg.evaluate("t=>window.tick(t)", total - .4)
            pg.screenshot(path=os.path.join(OUT, f"{key}_gta_end.png"))
            br.close(); return
        silent = os.path.join(OUT, f"{key}_silent.mp4")
        ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-i", bgv, "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-",
                               "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]", "-map", "[v]",
                               "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-t", f"{total:.3f}", silent], stdin=subprocess.PIPE)
        for f in range(int(total * FPS)):
            pg.evaluate("t=>window.tick(t)", f / FPS)
            ff.stdin.write(pg.screenshot(type="png", omit_background=True))
        br.close()
    ff.stdin.close(); ff.wait()
    wav = os.path.join(OUT, f"{key}_bed.wav")
    sc_ = [{"type": "grid"}] * len(starts)
    sc_[-1] = {"type": "cta"}
    bed(starts, total, wav, {"keyword": "gta"}, sc_)
    final = os.path.join(OUT, f"{key}_ig_nolvoice.mp4")
    final_mix(silent, wav, final, total)
    for s in segs:
        os.remove(s)
    print(key, f"{total:.2f}s", len(shots), "shots")


if __name__ == "__main__":
    build(sys.argv[1])
