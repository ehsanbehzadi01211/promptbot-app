"""'Laptop on a desk' reel (format 2 of the content plan, modelled on ai.akshu's KATANA reel):
a dark warm room, a laptop whose screen plays neon kinetic typography beat by beat,
a label above, karaoke subtitles below, full-screen comment CTA at the end.
Usage: python3 laptop.py <key>    (reads laptop.json[key] and words10/<key>.json)"""
import json, os, subprocess, sys, html
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build9 import bed, final_mix, W, H, FPS, LEAD, FONT, ROOT

TAIL = 1.6
E = html.escape

CSS = """
@font-face{font-family:Vaz;font-weight:500;src:url(FONT/vazirmatn/files/vazirmatn-arabic-500-normal.woff2)}
@font-face{font-family:Vaz;font-weight:800;src:url(FONT/vazirmatn/files/vazirmatn-arabic-800-normal.woff2)}
@font-face{font-family:Vaz;font-weight:900;src:url(FONT/vazirmatn/files/vazirmatn-arabic-900-normal.woff2)}
@font-face{font-family:Vaz;font-weight:900;src:url(FONT/vazirmatn/files/vazirmatn-latin-900-normal.woff2);unicode-range:U+0000-00FF}
@font-face{font-family:Vaz;font-weight:800;src:url(FONT/vazirmatn/files/vazirmatn-latin-800-normal.woff2);unicode-range:U+0000-00FF}
@font-face{font-family:Mono;font-weight:700;src:url(FONT/jetbrains-mono/files/jetbrains-mono-latin-700-normal.woff2)}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:clip;background:#0b0806}
body{font-family:Vaz,sans-serif;direction:rtl;color:#fff;-webkit-font-smoothing:antialiased;--L:#c8ff3e}
#world{position:absolute;inset:0;transform-origin:50% 45%}
.room{position:absolute;inset:0;background:
  radial-gradient(ellipse 700px 600px at 50% 42%,rgba(255,170,80,.55),rgba(255,140,60,.18) 55%,transparent 75%),
  radial-gradient(ellipse 900px 700px at 50% 38%,rgba(120,60,20,.5),transparent 70%),#0b0806}
.desk{position:absolute;left:0;right:0;top:1300px;bottom:0;background:
  linear-gradient(180deg,#2a1a10 0%,#1a100a 30%,#0c0705 100%);}
.desk:before{content:"";position:absolute;inset:0;opacity:.35;background:repeating-linear-gradient(91deg,rgba(255,200,150,.05) 0 3px,transparent 3px 17px)}
.spill{position:absolute;left:100px;right:100px;top:1300px;height:260px;background:radial-gradient(ellipse at 50% 0,rgba(200,255,62,.20),transparent 70%);mix-blend-mode:screen}
.label{position:absolute;top:470px;left:0;right:0;text-align:center;font-weight:800;font-size:54px;text-shadow:0 4px 18px rgba(0,0,0,.6)}
.lid{position:absolute;left:50px;top:620px;width:980px;height:630px;border-radius:30px;background:linear-gradient(#232323,#121212);box-shadow:0 30px 80px rgba(0,0,0,.7),0 0 0 2px #2c2c2c}
.cam{position:absolute;left:50%;top:10px;width:9px;height:9px;margin-left:-4px;border-radius:50%;background:#333}
.scr{position:absolute;left:22px;top:26px;width:936px;height:580px;border-radius:10px;overflow:hidden;background:#050505;
  background-image:radial-gradient(rgba(255,255,255,.09) 1.3px,transparent 1.4px);background-size:22px 22px}
.scr:after{content:"";position:absolute;inset:0;background:linear-gradient(125deg,rgba(255,255,255,.07),transparent 40%);pointer-events:none}
.bar{position:absolute;top:0;left:0;right:0;height:22px;background:rgba(255,255,255,.06);display:flex;gap:7px;padding:6px 10px;direction:ltr}
.bar i{width:10px;height:10px;border-radius:50%;background:#444}
.base{position:absolute;left:-10px;top:1250px;width:1100px;height:170px;
  clip-path:polygon(4% 0,96% 0,100% 100%,0 100%);background:linear-gradient(#3a3a3a,#1b1b1b)}
.keys{position:absolute;left:12%;right:12%;top:18px;height:84px;opacity:.55;
  background:repeating-linear-gradient(90deg,#0d0d0d 0 46px,transparent 46px 52px),repeating-linear-gradient(0deg,transparent 0 3px,#2a2a2a 3px 6px)}
.keys{background:linear-gradient(#111,#111);mask:repeating-linear-gradient(90deg,#000 0 44px,transparent 44px 52px),repeating-linear-gradient(0deg,#000 0 24px,transparent 24px 30px);-webkit-mask-composite:source-in;mask-composite:intersect}
.pad{position:absolute;left:41%;right:41%;bottom:10px;height:28px;border-radius:6px;background:#2b2b2b}
.beat{position:absolute;inset:22px 0 0 0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;opacity:0}
.big{font-weight:900;font-size:170px;line-height:1.05;text-align:center}
.mid{font-weight:900;font-size:96px;line-height:1.15;text-align:center}
.sm{font-weight:800;font-size:40px;color:#bbb}
.neon{color:var(--L);text-shadow:0 0 18px rgba(200,255,62,.85),0 0 46px rgba(200,255,62,.45)}
.strike{position:relative;display:inline-block}
.strike b{position:absolute;right:-12px;top:52%;height:12px;width:0;background:var(--L);box-shadow:0 0 16px var(--L);border-radius:6px}
.chips{display:flex;gap:18px;flex-wrap:wrap;justify-content:center;max-width:760px}
.chip{font-weight:800;font-size:44px;padding:12px 30px;border-radius:60px;border:3px solid #555;color:#ddd;position:relative;opacity:0}
.chip.x:after{content:"";position:absolute;left:10px;right:10px;top:50%;height:6px;background:#ff4d4d;transform:scaleX(var(--k,0));transform-origin:right;box-shadow:0 0 10px #ff4d4d}
.chip.g{border-color:var(--L);color:#071;background:var(--L);box-shadow:0 0 24px rgba(200,255,62,.6)}
.arrow{font-weight:900;font-size:44px;color:var(--L);opacity:0}
.term{width:820px;border:3px solid #333;border-radius:18px;background:#0c0c0c;padding:22px 28px;text-align:right}
.term .p{font-weight:800;font-size:40px;line-height:1.5;color:#eee;min-height:120px}
.term .p u{text-decoration:none;color:var(--L)}
.prog{height:14px;border-radius:8px;background:#222;margin-top:16px;overflow:hidden}
.prog i{display:block;height:100%;width:0;background:var(--L);box-shadow:0 0 14px var(--L)}
.code{font-family:Mono;font-weight:700;font-size:27px;line-height:1.45;color:#8fdc5a;direction:ltr;text-align:left;white-space:pre;opacity:0;width:740px}
.cap{font-family:Mono;font-weight:700;font-size:26px;color:#888;direction:ltr;letter-spacing:.12em}
.chk{display:flex;flex-direction:column;gap:10px;align-items:flex-start}
.chk div{font-weight:900;font-size:58px;opacity:0}
.chk div span{color:var(--L);margin-left:16px}
.stamp{font-weight:900;font-size:120px;color:var(--L);text-shadow:0 0 30px var(--L);opacity:0;transform:rotate(-8deg)}
.burst{position:absolute;left:50%;top:50%;width:0;height:0}
.burst i{position:absolute;left:0;top:0;width:90px;height:8px;border-radius:4px;background:var(--L);box-shadow:0 0 12px var(--L);opacity:0;transform-origin:0 50%}
.subs{position:absolute;left:60px;right:60px;top:1540px;text-align:center;font-weight:900;font-size:66px;line-height:1.35;text-shadow:0 5px 20px rgba(0,0,0,.9)}
.subs span{opacity:.92}.subs span.on{color:var(--L)}
.cta{position:absolute;inset:0;background:#050505;opacity:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:40px;
  background-image:radial-gradient(rgba(255,255,255,.08) 1.6px,transparent 1.7px);background-size:30px 30px}
.cta .k{font-weight:900;font-size:250px;line-height:1.05}
.cta .t{font-weight:900;font-size:96px}
.cbox{width:860px;border-radius:70px;border:4px solid #444;padding:28px 46px;font-weight:800;font-size:56px;color:#ddd;display:flex;justify-content:space-between;align-items:center;background:#111}
.cbox em{font-style:normal;color:var(--L)}
.cbox s{text-decoration:none;font-size:46px;color:var(--L)}
.cta .h{font-weight:800;font-size:46px;color:#aaa}
.flash{position:absolute;inset:0;background:#fff;opacity:0;pointer-events:none}
"""

JS = r"""
const $=s=>[...document.querySelectorAll(s)];
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const eo=x=>1-Math.pow(1-cl(x),3);
const back=x=>{x=cl(x);const c=1.9;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
window.tick=function(t){
  // world: slow push-in + punch on beats
  let z=1+0.035*(t/window.TOTAL), punch=0;
  for(const s of window.PUNCH){const d=t-s; if(d>=0&&d<.35) punch=Math.max(punch,(1-d/.35)*.035)}
  const shake=punch>0?Math.sin(t*90)*punch*90:0;
  document.getElementById('world').style.transform=`scale(${z+punch}) translate(${shake}px,${shake*.4}px)`;
  // beats
  $('.beat').forEach(b=>{const a=+b.dataset.a,e=+b.dataset.e;
    let o=cl((t-a)/.12)*cl((e-t)/.12); b.style.opacity=o;
    const k=t<a+.25?.9+.1*eo((t-a)/.25):1; b.style.transform=`scale(${k})`; b.style.filter=t<a+.12?`blur(${(1-(t-a)/.12)*8}px)`:'none'});
  $('[data-in]').forEach(el=>{const a=+el.dataset.in,d=t-a;
    if(el.classList.contains('code')){el.style.opacity=cl(d/.2);el.style.transform=`translateY(${(1-eo(d/.5))*40}px)`;return}
    el.style.opacity=cl(d/.15); el.style.transform=`scale(${d<0?.6:.6+.4*back(d/.3)})${el.classList.contains('stamp')?' rotate(-8deg)':''}`});
  $('[data-x]').forEach(el=>el.style.setProperty('--k',eo((t-(+el.dataset.x))/.25)));
  $('.strike b').forEach(el=>el.style.width=`calc(${eo((t-(+el.dataset.d))/.35)*100}% + 24px)`);
  $('.prog i').forEach(el=>{const a=+el.dataset.a,e=+el.dataset.e;el.style.width=cl((t-a)/(e-a))*100+'%'});
  $('[data-type]').forEach(el=>{const a=+el.dataset.a,e=+el.dataset.e,s=el.dataset.type;const n=Math.round(cl((t-a)/(e-a))*s.length);
    el.innerHTML=s.slice(0,n).replace(/«(.*?)»/g,'«<u>$1</u>»')+(n<s.length&&Math.floor(t*3)%2?'▌':'')});
  $('.burst').forEach(bu=>{const a=+bu.dataset.a;[...bu.children].forEach((i,k)=>{const d=t-a,ang=k*360/12;
    i.style.opacity=d<0?0:cl(1-d/.6); i.style.transform=`rotate(${ang}deg) translateX(${170+eo(d/.6)*200}px) scaleX(${cl(1-d/.6)})`})});
  // subtitles
  const W_=window.WORDS; let cur=-1; for(let i=0;i<W_.length;i++) if(t>=W_[i][1]) cur=i;
  const sub=document.querySelector('.subs');
  if(cur<0||t>window.CTA-.05){sub.innerHTML='';}else{const g=Math.floor(cur/4)*4;
    sub.innerHTML=W_.slice(g,g+4).map((w,i)=>`<span class="${g+i==cur?'on':''}">${w[0]}</span>`).join(' ')}
  // CTA takeover
  const c=document.querySelector('.cta'), d=t-window.CTA; c.style.opacity=cl(d/.2);
  c.style.transform=d<0?'none':`scale(${1.2-.2*eo(d/.35)})`;
  const f=document.querySelector('.flash'); let fl=0; for(const s of window.FLASH){const q=t-s; if(q>=0&&q<.18) fl=Math.max(fl,.55*(1-q/.18))} f.style.opacity=fl;
};
"""


def build(key):
    spec = json.load(open(os.path.join(ROOT, "laptop.json")))[key]
    words = json.load(open(os.path.join(ROOT, "words10", key + ".json")))
    toks = spec["voice"].replace("[excited]", "").split()
    ts = [LEAD + x for x in words["t"]]
    assert len(ts) == len(toks), (len(ts), len(toks))
    T = lambda i: ts[min(i, len(ts) - 1)]
    total = LEAD + words["end"] + TAIL
    cta_at = T(spec["cta_w"]) - .1
    beats = spec["beats"]
    starts = [T(b["w"]) - .12 for b in beats]
    ends = starts[1:] + [cta_at]
    parts = []
    for b, a, e in zip(beats, starts, ends):
        body = b["html"]
        # {wN} -> absolute time of word N (seconds)
        import re
        body = re.sub(r"\{w(\d+)([+-][\d.]+)?\}", lambda m: f"{T(int(m.group(1))) + float(m.group(2) or 0):.3f}", body)
        parts.append(f'<div class="beat" data-a="{a:.3f}" data-e="{e + .1:.3f}">{body}</div>')
    cta = spec["cta_html"]
    host_html = ""
    if spec.get("host"):   # owner's talking cartoon in the top-left corner (see host.py)
        from host import host_any, words_to_spans
        host_html = host_any(spec["host"], ROOT, words_to_spans(ts, total - 1.0), [[0, "corner"]], "#c8ff3e")
    page = (f'<!doctype html><html lang="fa"><head><meta charset="utf-8"><style>{CSS.replace("FONT", FONT)}</style></head><body>'
            f'<div id="world"><div class="room"></div><div class="desk"></div><div class="spill"></div>'
            f'<div class="label">{spec["label"]}</div>'
            f'<div class="lid"><div class="cam"></div><div class="scr"><div class="bar"><i></i><i></i><i></i></div>{"".join(parts)}</div></div>'
            f'<div class="base"><div class="keys"></div><div class="pad"></div></div></div>'
            f'<div class="subs"></div><div class="cta">{cta}</div><div class="flash"></div>'
            f'<script>window.TOTAL={total:.3f};window.CTA={cta_at:.3f};'
            f'window.WORDS={json.dumps([[E(w.replace("«","").replace("»","")), round(a, 3)] for w, a in zip(toks, ts)], ensure_ascii=False)};'
            f'window.PUNCH={json.dumps([round(s + .12, 3) for s in starts] + [round(cta_at, 3)])};'
            f'window.FLASH={json.dumps([round(starts[0] + .1, 3), round(cta_at, 3)] + [round(T(w), 3) for w in spec.get("flash_w", [])])};{JS}</script>{host_html}</body></html>')
    out_dir = os.path.join(ROOT, "out"); os.makedirs(out_dir, exist_ok=True)
    hp = os.path.join(out_dir, f"{key}_lap.html"); open(hp, "w").write(page)
    seek = "t=>window.tick(t)"
    stills = "--stills" in sys.argv
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={"width": W, "height": H})
        pg.goto("file://" + hp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(600)
        if stills:
            for k, tt in enumerate([s + .6 for s in starts] + [cta_at + .8]):
                pg.evaluate(seek, tt); pg.screenshot(path=os.path.join(out_dir, f"{key}_s{k}.png"))
            br.close(); return
        silent = os.path.join(out_dir, f"{key}_silent.mp4")
        ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                               "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "veryfast", silent], stdin=subprocess.PIPE)
        for f in range(int(total * FPS)):
            pg.evaluate(seek, f / FPS)
            ff.stdin.write(pg.screenshot(type="jpeg", quality=92))
        br.close()
    ff.stdin.close(); ff.wait()
    wav = os.path.join(out_dir, f"{key}_bed.wav")
    sc = [{"type": "shock", "title": "x"}] + [{"type": "x"}] * (len(starts) - 1) + [{"type": "cta"}]
    bed(starts + [cta_at], total, wav, {"keyword": spec["keyword"]}, sc)
    final = os.path.join(out_dir, f"{key}_ig_nolvoice.mp4")
    final_mix(silent, wav, final, total)
    print(key, f"{total:.2f}s", [round(s, 2) for s in starts], round(cta_at, 2))


if __name__ == "__main__":
    build(sys.argv[1])
