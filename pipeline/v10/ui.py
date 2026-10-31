"""'Studio UI' reel format (format 3): a clean product-explainer look modelled on farshad_frhni's reels,
pushed further. Warm cream canvas with drifting pastel light, glassy white UI cards, node diagrams whose
edges draw themselves and carry moving packets, counters, progress bars, chat bubbles, a chapter
pill bar on top, phrase subtitles that darken word by word, and soft blur/slide scene transitions.
The frosted glass robot host sits in the top-left circle.

Usage: python3 ui.py <key> [--stills]   (reads ui.json[key] and words10/<key>.json)
Scene times and element times are word indices: {wN} or {wN+0.2} inside templates.
"""
import json, os, re, subprocess, sys, html
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build9 import bed, final_mix, W, H, FPS, LEAD, FONT, ROOT

TAIL = 1.6
E = html.escape

# ----------------------------------------------------------------------------------------------- icons
def ic(name, size=56, color="currentColor", sw=2.2):
    P = {
        "chat": '<path d="M4 5h16v11H9l-5 4z"/>',
        "brain": '<path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 2 5 3 3 0 0 0 6 1V5a3 3 0 0 0-3-1zM15 4a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-2 5 3 3 0 0 1-6 1"/>',
        "tool": '<path d="M14.5 5.5a4 4 0 0 0 4.9 4.9L21 12l-9 9-3-3 9-9-1.6-1.6a4 4 0 0 0-4.9-4.9l2.8 2.8-2 2-2.8-2.8"/>',
        "db": '<ellipse cx="12" cy="5.5" rx="7" ry="2.8"/><path d="M5 5.5v13c0 1.5 3 2.8 7 2.8s7-1.3 7-2.8v-13M5 12c0 1.5 3 2.8 7 2.8s7-1.3 7-2.8"/>',
        "search": '<circle cx="10.5" cy="10.5" r="6"/><path d="M15 15l5 5"/>',
        "doc": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
        "split": '<path d="M12 3v6M12 9L5 16M12 9l7 7M12 9v12"/>',
        "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6"/>',
        "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2 20c.8-3.5 3.5-5.5 7-5.5s6.2 2 7 5.5"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8M18 14.8c2 .8 3.4 2.6 4 5.2"/>',
        "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
        "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
        "crown": '<path d="M3 8l4.5 4L12 5l4.5 7L21 8l-2 11H5z"/>',
        "eye": '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
        "pen": '<path d="M4 20l4-1 11-11-3-3L5 16z"/><path d="M14 6l3 3"/>',
        "loop": '<path d="M20 12a8 8 0 0 1-14 5.3M4 12a8 8 0 0 1 14-5.3"/><path d="M18 3v4h-4M6 21v-4h4"/>',
        "flag": '<path d="M5 21V4h11l-2 4 2 4H5"/>',
        "mail": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M3.5 6.5L12 13l8.5-6.5"/>',
        "headset": '<path d="M4 14v-2a8 8 0 0 1 16 0v2"/><rect x="3" y="13" width="4" height="6" rx="1.5"/><rect x="17" y="13" width="4" height="6" rx="1.5"/>',
        "cart": '<circle cx="9" cy="20" r="1.5"/><circle cx="17" cy="20" r="1.5"/><path d="M3 4h2.5l2.2 11h11l2-8H6.3"/>',
        "code": '<path d="M8 7l-5 5 5 5M16 7l5 5-5 5"/>',
        "spark": '<path d="M12 3l1.8 5.4L19 10l-5.2 1.6L12 17l-1.8-5.4L5 10l5.2-1.6z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/>',
        "target": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r=".6"/>',
    }
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{P[name]}</svg>')


FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")

CSS = """
@font-face{font-family:Vaz;font-weight:500;src:url(FONT/vazirmatn/files/vazirmatn-arabic-500-normal.woff2)}
@font-face{font-family:Vaz;font-weight:700;src:url(FONT/vazirmatn/files/vazirmatn-arabic-700-normal.woff2)}
@font-face{font-family:Vaz;font-weight:800;src:url(FONT/vazirmatn/files/vazirmatn-arabic-800-normal.woff2)}
@font-face{font-family:Vaz;font-weight:900;src:url(FONT/vazirmatn/files/vazirmatn-arabic-900-normal.woff2)}
@font-face{font-family:Vaz;font-weight:500;src:url(FONT/vazirmatn/files/vazirmatn-latin-500-normal.woff2);unicode-range:U+0000-00FF}
@font-face{font-family:Vaz;font-weight:700;src:url(FONT/vazirmatn/files/vazirmatn-latin-700-normal.woff2);unicode-range:U+0000-00FF}
@font-face{font-family:Vaz;font-weight:800;src:url(FONT/vazirmatn/files/vazirmatn-latin-800-normal.woff2);unicode-range:U+0000-00FF}
@font-face{font-family:Vaz;font-weight:900;src:url(FONT/vazirmatn/files/vazirmatn-latin-900-normal.woff2);unicode-range:U+0000-00FF}
@font-face{font-family:Mono;font-weight:700;src:url(FONT/jetbrains-mono/files/jetbrains-mono-latin-700-normal.woff2)}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden}
body{font-family:Vaz,sans-serif;direction:rtl;color:var(--ink);-webkit-font-smoothing:antialiased;
  --ink:#17151a;--mut:#8d8794;--bg:#f5f1ea;--card:#ffffff;--line:rgba(23,21,26,.08);background:var(--bg)}
#bg{position:absolute;inset:0;background:var(--bg);overflow:hidden}
#bg .blob{position:absolute;border-radius:50%;filter:blur(110px);opacity:.55}
#bg .grid{position:absolute;inset:0;background-image:radial-gradient(rgba(23,21,26,.13) 1.6px,transparent 1.7px);background-size:36px 36px;
  -webkit-mask:radial-gradient(ellipse 70% 55% at 50% 45%,#000 20%,transparent 75%);opacity:.6}
#dark{position:absolute;inset:0;background:radial-gradient(ellipse 90% 60% at 50% 40%,#1d1a24,#0b0a0e 70%);opacity:0}
#dark .grid{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.10) 1.6px,transparent 1.7px);background-size:36px 36px;
  -webkit-mask:radial-gradient(ellipse 70% 55% at 50% 45%,#000 20%,transparent 75%)}
#cam{position:absolute;inset:0;transform-origin:50% 45%}
.sc{position:absolute;inset:0;opacity:0;will-change:transform,opacity,filter}
.sc.dk{color:#fff}
/* top chapter bar */
#tabs{position:absolute;top:92px;left:250px;right:60px;height:74px;display:flex;gap:10px;justify-content:center;align-items:center;opacity:0}
#tabs .tb{height:62px;min-width:62px;border-radius:40px;background:rgba(255,255,255,.75);border:1.5px solid var(--line);
  display:flex;align-items:center;justify-content:center;font-weight:800;font-size:28px;color:var(--mut);padding:0 18px;
  box-shadow:0 6px 20px rgba(40,30,20,.06);white-space:nowrap;overflow:hidden;transition:none}
#tabs .tb.on{background:var(--ink);color:#fff;border-color:var(--ink)}
#tabs .tb.done{color:var(--a)}
/* headline */
.head{position:absolute;top:300px;left:70px;right:70px;text-align:center}
.kick{display:inline-flex;gap:12px;align-items:center;font-weight:800;font-size:34px;color:var(--mut);background:rgba(255,255,255,.8);
  border:1.5px solid var(--line);border-radius:40px;padding:10px 26px;margin-bottom:26px}
.kick b{color:var(--a)}
.dk .kick{background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.12);color:#b9b3c4}
h1{font-weight:900;font-size:100px;line-height:1.16;letter-spacing:-.5px}
h1 .w{display:inline-block;opacity:0}
h1 em,.em{font-style:normal;color:var(--a)}
.hl{background:linear-gradient(transparent 58%,var(--a2) 58%,var(--a2) 90%,transparent 90%);padding:0 6px}
/* stage */
.stage{position:absolute;left:80px;top:575px;width:920px;height:780px;transform:scale(1.1);transform-origin:50% 0}
.node{position:absolute;display:flex;align-items:center;gap:20px;padding:22px 30px 22px 26px;border-radius:30px;background:var(--card);
  border:1.5px solid var(--line);box-shadow:0 24px 60px rgba(60,40,20,.10),0 2px 6px rgba(60,40,20,.05);font-weight:800;font-size:42px;opacity:0;white-space:nowrap}
.node .i{width:84px;height:84px;border-radius:22px;display:flex;align-items:center;justify-content:center;color:#fff;flex:none;
  background:linear-gradient(145deg,var(--c1,var(--a)),var(--c2,#ff9d6b));box-shadow:inset 0 1px 0 rgba(255,255,255,.4),0 8px 20px var(--glow,rgba(232,105,60,.35))}
.node small{display:block;font-weight:700;font-size:25px;color:var(--mut);margin-top:2px}
.node.c{flex-direction:column;gap:14px;padding:30px 34px;text-align:center}
.node.big{font-size:44px}.node.big .i{width:110px;height:110px;border-radius:30px}
.node .ring{position:absolute;inset:-10px;border-radius:38px;border:4px solid var(--a);opacity:0}
.dk .node{background:rgba(255,255,255,.07);border-color:rgba(255,255,255,.14);color:#fff;box-shadow:0 30px 70px rgba(0,0,0,.45)}
svg.edges{position:absolute;inset:0;overflow:visible}
svg.edges path.e{fill:none;stroke:#cfc6bb;stroke-width:5;stroke-linecap:round}
svg.edges path.e.a{stroke:var(--a)}
.dk svg.edges path.e{stroke:rgba(255,255,255,.22)}
svg.edges circle.pk{fill:var(--a);filter:drop-shadow(0 0 8px var(--a))}
.chipr{position:absolute;display:flex;gap:10px;align-items:center;font-weight:800;font-size:28px;padding:10px 20px;border-radius:30px;
  background:var(--ink);color:#fff;opacity:0}
.chipr.a{background:var(--a)}
.chipr.g{background:#21b26b}
/* cards & bars */
.card{position:absolute;border-radius:34px;background:var(--card);border:1.5px solid var(--line);box-shadow:0 30px 70px rgba(60,40,20,.12);opacity:0;overflow:hidden}
.win{display:flex;gap:9px;padding:20px 26px;border-bottom:1.5px solid var(--line);direction:ltr;align-items:center}
.win i{width:15px;height:15px;border-radius:50%;background:#e8e2da}.win i:nth-child(1){background:#ff6b5f}.win i:nth-child(2){background:#ffbd2e}.win i:nth-child(3){background:#29c840}
.win span{margin-left:auto;font-family:Mono;font-size:22px;color:var(--mut)}
.bub{max-width:640px;padding:20px 28px;border-radius:30px;font-weight:700;font-size:36px;line-height:1.45;opacity:0}
.bub.me{background:var(--ink);color:#fff;border-bottom-left-radius:8px;margin-right:auto}
.bub.ai{background:#f3eee7;border-bottom-right-radius:8px}
.dots{display:inline-flex;gap:8px}.dots i{width:13px;height:13px;border-radius:50%;background:var(--mut)}
.bar{height:26px;border-radius:20px;background:#ece6de;overflow:hidden;position:relative}
.bar i{position:absolute;top:0;bottom:0;right:0;width:0;border-radius:20px;background:linear-gradient(90deg,var(--a),#ff9d6b)}
.dk .bar{background:rgba(255,255,255,.1)}
.big7{font-weight:900;font-size:430px;line-height:.9;color:var(--a);text-align:center;letter-spacing:-8px;
  text-shadow:0 30px 80px rgba(232,105,60,.35)}
.tile{position:absolute;width:196px;height:196px;border-radius:40px;background:var(--card);border:1.5px solid var(--line);
  box-shadow:0 20px 50px rgba(60,40,20,.10);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;opacity:0;
  font-weight:800;font-size:27px}
.tile .i{width:74px;height:74px;border-radius:22px;display:flex;align-items:center;justify-content:center;color:#fff;
  background:linear-gradient(145deg,var(--c1),var(--c2))}
.tick{width:58px;height:58px;border-radius:50%;background:#ddd6cd;color:#fff;display:flex;align-items:center;justify-content:center;opacity:0;flex:none}
.li{display:flex;align-items:center;gap:22px;font-weight:800;font-size:40px;padding:22px 30px;border-radius:26px;background:rgba(255,255,255,.07);
  border:1.5px solid rgba(255,255,255,.12);opacity:0}
.li .tick{background:rgba(255,255,255,.12)}
.li.lt{background:#fff;border-color:var(--line);color:var(--ink);box-shadow:0 14px 34px rgba(60,40,20,.08)}.li.lt .tick{background:#ddd6cd}
.score{position:absolute;width:250px;height:250px}
.score svg{position:absolute;inset:0;transform:rotate(-90deg)}
.score b{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:84px}
/* subtitles */
#subs{position:absolute;left:70px;right:70px;top:1445px;text-align:center;font-weight:900;font-size:60px;line-height:1.4;min-height:100px}
#subs span{display:inline-block;margin:0 7px;color:#cbc4bb}
#subs span.s{color:var(--ink)}
#subs span.on{color:#fff;background:var(--a);border-radius:18px;padding:0 16px;box-shadow:0 10px 30px rgba(232,105,60,.35)}
body.dkm #subs span{color:#5b5664}body.dkm #subs span.s{color:#fff}
/* CTA */
.cta-box{position:absolute;left:110px;right:110px;top:690px;border-radius:50px;background:var(--card);padding:56px 50px 60px;text-align:center;
  box-shadow:0 40px 90px rgba(60,40,20,.16);border:1.5px solid var(--line);opacity:0}
.cta-box .t{font-weight:900;font-size:76px}
.kw{display:inline-block;margin-top:30px;font-weight:900;font-size:120px;color:#fff;background:var(--a);border-radius:40px;padding:6px 56px 16px;
  box-shadow:0 26px 60px rgba(232,105,60,.45)}
.kw u{text-decoration:none;display:inline-block;width:8px;height:110px;background:#fff;vertical-align:middle;margin-right:10px;border-radius:4px}
.cbox{margin-top:46px;border-radius:40px;border:2px solid var(--line);background:#f7f3ee;padding:26px 34px;display:flex;align-items:center;gap:22px;
  font-weight:800;font-size:40px;color:var(--mut);text-align:right}
.cbox .av{width:66px;height:66px;border-radius:50%;background:linear-gradient(145deg,var(--a),#ffb38a);flex:none}
.dm{position:absolute;left:150px;right:150px;top:1340px;display:flex;align-items:center;gap:22px;border-radius:34px;background:var(--ink);color:#fff;
  padding:26px 32px;font-weight:800;font-size:38px;opacity:0;box-shadow:0 30px 60px rgba(0,0,0,.25)}
.dm .ico{width:76px;height:76px;border-radius:24px;background:var(--a);display:flex;align-items:center;justify-content:center;flex:none}
#flash{position:absolute;inset:0;background:#fff;opacity:0;pointer-events:none}
"""

JS = r"""
const $=s=>[...document.querySelectorAll(s)];
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const ex=x=>{x=cl(x);return x===1?1:1-Math.pow(2,-10*x)};               // expo out
const eio=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};        // cubic in-out
const back=x=>{x=cl(x);const c=1.6;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
const FAN=n=>String(n).replace(/[0-9]/g,d=>'۰۱۲۳۴۵۶۷۸۹'[d]);
const S=window.SCN;
// path lengths
$('path.e').forEach(p=>{const L=p.getTotalLength();p.dataset.len=L;p.style.strokeDasharray=L;p.style.strokeDashoffset=L});
window.tick=function(t){
  // background light drift
  $('#bg .blob').forEach((b,i)=>{const k=i*1.7;b.style.transform=`translate(${Math.sin(t*.23+k)*90}px,${Math.cos(t*.19+k)*70}px) scale(${1+Math.sin(t*.3+k)*.08})`});
  // dark mode amount
  let dk=0; for(const s of S){ if(s.dark){ dk=Math.max(dk,cl((t-s.a+.2)/.5)*cl((s.e-t+.2)/.5)); } }
  document.getElementById('dark').style.opacity=dk; document.body.classList.toggle('dkm',dk>.5);
  // camera: slow push + tiny drift, kick on scene start
  let kick=0; for(const s of S){const d=t-s.a; if(d>=0&&d<.6) kick=Math.max(kick,(1-ex(d/.6))*.025)}
  document.getElementById('cam').style.transform=`scale(${1.0+.02*Math.sin(t*.15)+kick}) translate(${Math.sin(t*.4)*6}px,${Math.cos(t*.33)*5}px)`;
  // scenes in/out
  S.forEach((s,i)=>{const el=document.getElementById('s'+i);const di=t-(s.a-.14),de=(s.e+.14)-t;   // overlapping cross-transition
    let o=cl(di/.28), y=(1-ex(di/.7))*90, sc=.965+.035*ex(di/.7), bl=(1-ex(di/.4))*14;
    if(de<.34){const k=1-cl(de/.34);y=-60*eio(k);sc=1+.03*eio(k);bl=12*k;o=Math.min(o,1-k)}
    if(di<0){o=0}
    el.style.opacity=o; el.style.transform=`translateY(${y}px) scale(${sc})`; el.style.filter=bl>.3?`blur(${bl}px)`:'none';
    el.style.visibility=o<=0.001?'hidden':'visible'});
  // headline words
  $('h1 .w').forEach(w=>{const a=+w.dataset.in,d=t-a;w.style.opacity=cl(d/.22);
    w.style.transform=`translateY(${(1-ex(d/.55))*46}px)`;w.style.filter=d<.3?`blur(${(1-cl(d/.3))*10}px)`:'none'});
  // generic entrances
  $('[data-in]:not(.w)').forEach(el=>{const a=+el.dataset.in,d=t-a,m=el.dataset.m||'pop';
    let o=cl(d/.2),tr='';
    if(m==='pop'){tr=`scale(${d<0?.7:.7+.3*back(d/.5)})`}
    else if(m==='up'){tr=`translateY(${(1-ex(d/.6))*60}px)`}
    else if(m==='right'){tr=`translateX(${(1-ex(d/.6))*120}px)`}
    else if(m==='left'){tr=`translateX(${-(1-ex(d/.6))*120}px)`}
    else if(m==='drop'){tr=`translateY(${-(1-ex(d/.6))*80}px) scale(${.9+.1*ex(d/.6)})`}
    if(el.dataset.out){const q=t-(+el.dataset.out);if(q>0){o*=1-cl(q/.3);tr+=` scale(${1-.1*ex(q/.3)})`}}
    if(el.dataset.dim){const q=t-(+el.dataset.dim);if(q>0){o*=1-.6*cl(q/.4)}}
    if(d>.6&&(el.classList.contains('node')||el.classList.contains('tile'))){const ph=(+el.dataset.in)*3.1;tr+=` translateY(${Math.sin(t*1.6+ph)*5}px)`}
    el.style.opacity=o; el.style.transform=(el.dataset.base||'')+' '+tr;
    if(el.dataset.mv){const [a2,dx,dy,s2]=el.dataset.mv.split(',').map(Number);const k=eio((t-a2)/.7);
      el.style.transform=(el.dataset.base||'')+' '+tr+` translate(${dx*k}px,${dy*k}px) scale(${1+(s2-1)*k})`}});
  // edges draw
  $('path.e').forEach(p=>{const a=+p.dataset.draw,L=+p.dataset.len,k=ex((t-a)/.6);p.style.strokeDashoffset=L*(1-k);
    if(p.dataset.hot){p.classList.toggle('a',t>=+p.dataset.hot)}});
  // packets: data-p="pathId,a,dur[,period]"
  $('circle.pk').forEach(c=>{const [pid,a,dur,per]=c.dataset.p.split(',');const p=document.getElementById(pid);const L=+p.dataset.len;
    let d=t-(+a); if(per&&d>0) d=d%(+per); const k=d/(+dur);
    if(d<0||k>1||!L){c.style.opacity=0;return}
    const pt=p.getPointAtLength(L*eio(k));c.setAttribute('cx',pt.x);c.setAttribute('cy',pt.y);c.style.opacity=Math.min(1,k*6,(1-k)*6)});
  // glow rings: data-lit="t"
  $('[data-lit]').forEach(el=>{const d=t-(+el.dataset.lit);const r=el.querySelector('.ring');if(!r)return;
    r.style.opacity=d<0?0:cl(d/.2)*(.65+.35*Math.sin(d*6)); r.style.transform=`scale(${1+(d>=0&&d<.5?(1-d/.5)*.08:0)})`});
  // bars: data-fill="a,e,pct"
  $('[data-fill]').forEach(el=>{const [a,e,p]=el.dataset.fill.split(',').map(Number);el.style.width=(eio((t-a)/(e-a))*p)+'%'});
  // counters: data-count="a,e,from,to[,suffix]"
  $('[data-count]').forEach(el=>{const f=el.dataset.count.split(',');const [a,e,x0,x1]=f.slice(0,4).map(Number);
    el.textContent=FAN(Math.round(x0+(x1-x0)*ex((t-a)/(e-a))))+(f[4]||'')});
  // score ring: data-ring="t:v;t:v"
  $('[data-ring]').forEach(el=>{const ks=el.dataset.ring.split(';').map(s=>s.split(':').map(Number));let v=ks[0][1];
    for(let i=1;i<ks.length;i++){const [ta,va]=ks[i-1],[tb,vb]=ks[i];if(t>=ta) v=va+(vb-va)*eio((t-ta)/(tb-ta))}
    const C=+el.dataset.c;el.querySelector('circle.v').style.strokeDashoffset=C*(1-v/100);el.querySelector('b').textContent=FAN(Math.round(v));
    el.querySelector('circle.v').style.stroke=v>=85?'#21b26b':'var(--a)'});
  // typing: data-type, data-a, data-e
  $('[data-type]').forEach(el=>{const a=+el.dataset.a,e=+el.dataset.e,s=el.dataset.type;const n=Math.round(cl((t-a)/(e-a))*s.length);
    el.textContent=s.slice(0,n)});
  // typing dots
  $('.dots').forEach(d=>[...d.children].forEach((i,k)=>i.style.transform=`translateY(${Math.sin(t*9-k*.9)*5}px)`));
  // orbit: data-orbit="cx,cy,r,phase,speed"
  $('[data-orbit]').forEach(el=>{const [cx,cy,r,ph,sp]=el.dataset.orbit.split(',').map(Number);const an=ph+t*sp;
    el.style.left=(cx+Math.cos(an)*r)+'px';el.style.top=(cy+Math.sin(an)*r*.55)+'px';el.style.zIndex=Math.sin(an)>0?3:1});
  // ticks
  $('[data-tk]').forEach(el=>{const d=t-(+el.dataset.tk);const tk=el.querySelector('.tick');if(!tk)return;
    tk.style.opacity=d<0?.35:1; tk.style.background=d<0?'':'#21b26b'; tk.style.transform=`scale(${d<0?1:.7+.3*back(d/.4)})`;
    tk.querySelector('svg').style.opacity=d<0?0:1});
  // tabs
  const tb=document.getElementById('tabs'); let ti=-1, show=0;
  S.forEach(s=>{if(s.tab!=null&&t>=s.a-.1){ti=s.tab}});
  show=window.TABS_ON?cl((t-window.TABS_ON)/.4)*cl((window.CTA-t)/.3):0; tb.style.opacity=show; tb.style.transform=`translateY(${(1-ex((t-window.TABS_ON)/.6))*-40}px)`;
  [...tb.children].forEach((c,i)=>{c.className='tb'+(i===ti?' on':'')+(i<ti?' done':'');c.textContent=i===ti?c.dataset.n:FAN(i+1)});
  // subtitles: phrase groups, spoken words dark, current word in accent chip
  const WS=window.WORDS; let cur=-1; for(let i=0;i<WS.length;i++) if(t>=WS[i][1]) cur=i;
  const sub=document.getElementById('subs');
  if(cur<0||t>window.CTA-.05){sub.innerHTML=''}else{const g=WS[cur][2];const ids=[];WS.forEach((w,i)=>{if(w[2]===g)ids.push(i)});
    const age=t-WS[ids[0]][1];
    sub.style.opacity=cl(age/.15);
    sub.innerHTML=ids.map(i=>`<span class="${i===cur?'on':(i<cur?'s':'')}">${WS[i][0]}</span>`).join('')}
  // flash
  let fl=0; for(const s of window.FLASH){const q=t-s; if(q>=0&&q<.2) fl=Math.max(fl,.45*(1-q/.2))} document.getElementById('flash').style.opacity=fl;
};
"""

# ----------------------------------------------------------------------------------------------- builders
PAL = [("#e8693c", "#ff9d6b", "rgba(232,105,60,.35)"), ("#6a5cff", "#a493ff", "rgba(106,92,255,.35)"),
       ("#14a989", "#5fd9b6", "rgba(20,169,137,.35)"), ("#2d8cff", "#7cc1ff", "rgba(45,140,255,.35)"),
       ("#ff4f8b", "#ff9ab9", "rgba(255,79,139,.35)"), ("#f2a516", "#ffd065", "rgba(242,165,22,.35)"),
       ("#17151a", "#4a4552", "rgba(23,21,26,.3)")]


def node(x, y, label, icon, t, pal=0, sub="", cls="", lit=None, m="pop", w=None, extra=""):
    c1, c2, g = PAL[pal % len(PAL)]
    st = f"left:{x}px;top:{y}px;--c1:{c1};--c2:{c2};--glow:{g};" + (f"width:{w}px;" if w else "")
    li = f' data-lit="{lit}"' if lit is not None else ""
    s = f"<small>{sub}</small>" if sub else ""
    return (f'<div class="node {cls}" style="{st}" data-in="{t}" data-m="{m}"{li} {extra}><div class="ring"></div>'
            f'<div class="i">{ic(icon, 46 if "big" not in cls else 62, "#fff", 2.4)}</div><div>{label}{s}</div></div>')


def edges(paths):
    """paths: list of (id, d, draw_t, hot_t|None, packets[(a,dur,period|None)])"""
    out = ['<svg class="edges" viewBox="0 0 920 780" width="920" height="780">']
    for pid, d, a, hot, pk in paths:
        h = f' data-hot="{hot}"' if hot is not None else ""
        out.append(f'<path class="e" id="{pid}" d="{d}" data-draw="{a}"{h}/>')
        for p in pk:
            out.append(f'<circle class="pk" r="11" data-p="{pid},{p[0]},{p[1]}{"," + str(p[2]) if len(p) > 2 and p[2] else ""}"/>')
    out.append("</svg>")
    return "".join(out)


def head(kick, h1_words, k_in):
    """h1_words: list of (html, t) ; kick: html or ''"""
    kk = f'<div class="kick" data-in="{k_in}" data-m="drop">{kick}</div><br>' if kick else ""
    ws = " ".join(f'<span class="w" data-in="{t}">{h}</span>' for h, t in h1_words)
    return f'<div class="head">{kk}<h1>{ws}</h1></div>'


def tm(v, T):
    """time spec -> seconds. int = word index; "12+0.3" / "12-0.2" = word index + offset; float string "s:3.5" = absolute."""
    if isinstance(v, (int,)):
        return T(v)
    if isinstance(v, float):
        return T(int(v)) + (v - int(v))
    m = re.fullmatch(r"\s*(\d+)\s*([+-]\s*[\d.]+)?\s*", str(v))
    if not m:
        raise ValueError(f"bad time {v!r}")
    return round(T(int(m.group(1))) + float((m.group(2) or "0").replace(" ", "")), 3)


def el_html(e, T, dark=False):
    """One stage element (stage is 920x780, scaled 1.1). See DAILY.md / ui.json for the schema."""
    k = e["el"]
    t = lambda key, d=None: tm(e[key], T) if key in e else d
    if k == "node":
        return node(e["x"], e["y"], e["label"], e.get("icon", "spark"), t("at"), e.get("pal", 0), e.get("sub", ""),
                    e.get("cls", ""), t("lit"), e.get("m", "pop"), e.get("w"))
    if k == "edges":
        return edges([(x["id"], x["d"], tm(x["at"], T), tm(x["hot"], T) if x.get("hot") is not None else None,
                       [[tm(p[0], T)] + list(p[1:]) for p in x.get("pk", [])]) for x in e["items"]])
    if k == "chip":
        cls = e.get("cls", "")
        icon = ic(e["icon"], 30, "#fff", 2.6) + " " if e.get("icon") else ""
        return f'<div class="chipr {cls}" style="left:{e["x"]}px;top:{e["y"]}px" data-in="{t("at")}">{icon}{e["text"]}</div>'
    if k == "chat":
        msgs = []
        for m_ in e["msgs"]:
            who = m_.get("who", "ai")
            mv = "left" if who == "me" else "right"
            if m_.get("dots"):
                inner = '<span class="dots"><i></i><i></i><i></i></span>'
            elif m_.get("type"):
                inner = f'<span data-type="{E(m_["text"])}" data-a="{tm(m_["at"], T)}" data-e="{tm(m_["type"], T)}"></span>'
            else:
                inner = m_["text"]
            out = f' data-out="{tm(m_["out"], T)}"' if m_.get("out") is not None else ""
            msgs.append(f'<div class="bub {who}" data-in="{tm(m_["at"], T)}" data-m="{mv}"{out}>{inner}</div>')
        dim = f' data-dim="{t("dim")}"' if "dim" in e else ""
        return (f'<div class="card" style="left:{e.get("x", 70)}px;top:{e.get("y", 0)}px;width:{e.get("w", 780)}px;height:{e.get("h", 420)}px" '
                f'data-in="{t("at")}" data-m="up"{dim}><div class="win"><i></i><i></i><i></i><span>{e.get("app", "claude.ai")}</span></div>'
                f'<div style="padding:34px;display:flex;flex-direction:column;gap:22px">{"".join(msgs)}</div></div>')
    if k == "meter":
        # label, value counts from->to (suffix), bar fills to the same value
        a, b = t("count_at", t("at")), t("count_end", t("at") + .8)
        col = e.get("color", "")
        bg = f' style="background:linear-gradient(90deg,{col},#ff9d6b)"' if col else ""
        badge = ""
        if e.get("badge"):
            badge = (f'<div class="chipr" style="position:relative;display:inline-flex;margin-top:28px;{"background:" + col if col else ""}" '
                     f'data-in="{tm(e["badge"]["at"], T)}">{ic(e["badge"].get("icon", "bolt"), 30, "#fff")} {e["badge"]["text"]}</div>')
        return (f'<div class="card" style="left:{e.get("x", 110)}px;top:{e["y"]}px;width:{e.get("w", 700)}px;padding:34px 44px 36px" data-in="{t("at")}" data-m="up">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;font-weight:800;font-size:38px;margin-bottom:24px">'
                f'<span>{e["label"]}</span><span class="em" style="font-size:54px;font-weight:900" data-count="{a},{b},{e["from"]},{e["to"]},{e.get("suffix", "")}"></span></div>'
                f'<div class="bar"><i data-fill="{a},{b},{e["to"]}"{bg}></i></div>{badge}</div>')
    if k == "big":   # huge number / word
        cnt = f' data-count="{t("at")},{t("end", t("at") + .5)},{e["count"][0]},{e["count"][1]}"' if e.get("count") else ""
        return (f'<div class="big7" style="position:absolute;left:0;right:0;top:{e.get("y", -10)}px;{e.get("style", "")}" data-in="{t("at")}" data-m="pop"{cnt}>'
                f'{e.get("text", "")}</div>')
    if k == "h":     # extra headline inside the stage: words [[text, at], ...]
        ws = " ".join(f'<span class="w" data-in="{tm(a_, T)}">{h}</span>' for h, a_ in e["words"])
        return f'<div style="position:absolute;left:0;right:0;top:{e["y"]}px;text-align:center"><h1 style="font-size:{e.get("size", 84)}px">{ws}</h1></div>'
    if k == "tiles":  # up to 8 tiles, rows of 4 (second row centred)
        out = []
        items = e["items"]
        for i, (nm, icon) in enumerate(items):
            r, c = divmod(i, 4)
            row_n = min(4, len(items) - r * 4)
            x = (920 - (row_n * 196 + (row_n - 1) * 22)) / 2 + c * 218
            c1, c2, _ = PAL[i % len(PAL)]
            out.append(f'<div class="tile" style="left:{x:.0f}px;top:{e["y"] + r * 218}px;--c1:{c1};--c2:{c2}" data-in="{t("at") + i * e.get("step", .11):.3f}">'
                       f'<div class="i">{ic(icon, 40, "#fff", 2.4)}</div>{nm}</div>')
        return "".join(out)
    if k == "lanes":  # parallel progress lanes [[name, speed], ...]
        out = []
        for i, (nm, sp) in enumerate(e["items"]):
            y = e["y"] + i * 135
            end = t("fill_at") + e.get("dur", 1.1) * sp
            out.append(f'<div class="card" style="left:60px;top:{y}px;width:800px;padding:26px 34px;display:flex;align-items:center;gap:26px" data-in="{t("at") + i * .12:.3f}" data-m="right">'
                       f'<b style="font-size:36px;width:130px">{nm}</b><div class="bar" style="flex:1"><i data-fill="{t("fill_at"):.3f},{end:.3f},100"></i></div>'
                       f'<div data-tk="{end:.3f}"><div class="tick">{ic("check", 34, "#fff", 3)}</div></div></div>')
        return "".join(out)
    if k == "checklist":  # [[text, tick_at], ...]
        lis = []
        for i, (txt, tk) in enumerate(e["items"]):
            lis.append(f'<div class="li{"" if dark else " lt"}" data-in="{t("at") + i * .15:.3f}" data-m="up" data-tk="{tm(tk, T):.3f}">'
                       f'<div class="tick">{ic("check", 34, "#fff", 3)}</div>{txt}</div>')
        return f'<div style="position:absolute;left:120px;right:120px;top:{e["y"]}px;display:flex;flex-direction:column;gap:18px">{"".join(lis)}</div>'
    if k == "score":  # ring that animates through [[at, value], ...]
        ks = ";".join(f"{tm(a_, T)}:{v}" for a_, v in e["keys"])
        return (f'<div class="score" style="left:{e.get("x", 335)}px;top:{e["y"]}px" data-in="{t("at")}" data-ring="{ks}" data-c="691">'
                f'<svg viewBox="0 0 250 250"><circle cx="125" cy="125" r="110" fill="#fff" stroke="#ece6de" stroke-width="18"/>'
                f'<circle class="v" cx="125" cy="125" r="110" fill="none" stroke-width="18" stroke-linecap="round" stroke-dasharray="691" stroke-dashoffset="691"/></svg><b>0</b></div>')
    if k == "orbit":  # chips circling a centre point
        out = []
        n = len(e["items"])
        for i, (nm, icon) in enumerate(e["items"]):
            out.append(f'<div class="chipr" style="background:rgba(255,255,255,.12);border:1.5px solid rgba(255,255,255,.18);margin:-28px 0 0 -90px;width:180px;justify-content:center" '
                       f'data-in="{t("at") + i * .15:.3f}" data-orbit="{e["cx"]},{e["cy"]},{e.get("r", 310)},{i * 6.283 / n:.3f},{e.get("speed", .9)}">{ic(icon, 30, "#fff")} {nm}</div>')
        return "".join(out)
    if k == "html":   # raw HTML; {wN} / {wN+0.3} become times
        return re.sub(r"\{w(\d+)([+-][\d.]+)?\}", lambda m: f"{T(int(m.group(1))) + float(m.group(2) or 0):.3f}", e["html"])
    raise ValueError(f"unknown element {k}")


def scene_html(sc, T, n_tabs):
    if sc.get("type") == "cta":
        kw = sc["keyword"]
        w = sc["w"]
        a = T(w)
        return f"""
<div class="head" style="top:330px"><h1 style="font-size:92px"><span class="w" data-in="{a}">فقط</span> <span class="w" data-in="{T(w + 1)}">یه</span> <span class="w" data-in="{T(w + 1) + .12}"><em>کلمه</em></span></h1></div>
<div class="cta-box" data-in="{a + .1}" data-m="up">
 <div class="t">کامنت کن</div>
 <div class="kw" data-in="{T(w + 1)}" data-m="pop">{kw}</div>
 <div class="cbox"><div class="av"></div><span data-type="{kw}" data-a="{T(w + 3)}" data-e="{T(w + 4)}" style="color:var(--ink)"></span><span style="margin-right:auto;color:var(--a)">{ic("mail", 44, "currentColor")}</span></div>
</div>
<div class="dm" data-in="{T(w + 6)}" data-m="up"><div class="ico">{ic("mail", 44, "#fff")}</div><div>{sc['dm']}<small style="display:block;font-size:28px;color:#aaa;font-weight:700">توی دایرکتت</small></div></div>"""
    hd = ""
    h = sc.get("head")
    if h:
        kick = h.get("kick", "")
        if sc.get("tab") is not None and not kick:
            kick = f'<b>{str(sc["tab"] + 1).translate(FA)}</b> / {str(n_tabs).translate(FA)}'
        em = set(h.get("em", []))
        hl = set(h.get("hl", []))
        words = []
        for i, (txt, at) in enumerate(h["h1"]):
            if i in hl:
                txt = f'<em class="hl">{txt}</em>'
            elif i in em:
                txt = f"<em>{txt}</em>"
            at_s = tm(at, T)
            if h.get("early", sc.get("tab") is not None):   # chapter titles show as the scene opens
                at_s = min(at_s, T(sc["w"]) + .1 + .12 * i)
            words.append((txt, at_s))
        hd = head(kick, words, tm(h.get("kick_at", sc["w"]), T) - .1)
        if h.get("top"):
            hd = hd.replace('<div class="head">', f'<div class="head" style="top:{h["top"]}px">', 1)
    st = f' style="top:{sc["stage_top"]}px"' if sc.get("stage_top") else ""
    return hd + f'<div class="stage"{st}>{"".join(el_html(e, T, sc.get("dark")) for e in sc.get("els", []))}</div>'


def build(key):
    spec = json.load(open(os.path.join(ROOT, "ui.json")))[key]
    words = json.load(open(os.path.join(ROOT, "words10", key + ".json")))
    toks = spec["voice"].replace("[excited]", "").split()
    ts = [LEAD + x for x in words["t"]]
    assert len(ts) == len(toks), (len(ts), len(toks))
    T = lambda i: round(ts[min(int(i), len(ts) - 1)], 3)
    total = LEAD + words["end"] + TAIL
    scenes = spec["scenes"]
    starts = [T(s["w"]) - .15 for s in scenes]
    ends = starts[1:] + [total + 1]
    cta_at = starts[-1]
    n_tabs = len(spec["tabs"])
    parts, S = [], []
    for i, (sc, a, e) in enumerate(zip(scenes, starts, ends)):
        dk = " dk" if sc.get("dark") else ""
        parts.append(f'<div class="sc{dk}" id="s{i}">{scene_html(sc, T, n_tabs)}</div>')
        S.append({"a": round(a, 3), "e": round(e, 3), "dark": bool(sc.get("dark")), "tab": sc.get("tab")})
    # subtitle groups: break after punctuation or every 5 words
    groups, g, cnt = [], 0, 0
    for w in toks:
        groups.append(g); cnt += 1
        if re.search(r"[.!؟?؛،:,]$", w) or cnt >= 5:
            g += 1; cnt = 0
    clean = lambda w: E(re.sub(r"[«»]", "", w))
    WORDS = [[clean(w), round(a, 3), gg] for w, a, gg in zip(toks, ts, groups)]
    tabs_on = min(s["a"] for s in S if s["tab"] is not None)
    tabs = "".join(f'<div class="tb" data-n="{E(n)}"></div>' for n in spec["tabs"])
    blobs = ('<div class="blob" style="left:-200px;top:80px;width:760px;height:760px;background:#ffb38a"></div>'
             '<div class="blob" style="right:-260px;top:620px;width:820px;height:820px;background:#b7a8ff"></div>'
             '<div class="blob" style="left:-120px;bottom:-160px;width:760px;height:760px;background:#9ee6c9"></div>')
    host_html = ""
    if spec.get("host"):
        from host import host_any, words_to_spans
        host_html = ('<script>window.HOSTPOS={big:{d:190,x:40,y:84},corner:{d:190,x:40,y:84},off:{d:190,x:40,y:84}}</script>' +
                     host_any(spec["host"], ROOT, words_to_spans(ts, total - 1.0), [[0, "corner"]], spec.get("accent", "#e8693c")))
        host_html = host_html.replace("#host{", "#host{border-color:#fff!important;box-shadow:0 14px 40px rgba(60,40,20,.25)!important;", 1)
    page = (f'<!doctype html><html lang="fa"><head><meta charset="utf-8"><style>{CSS.replace("FONT", FONT)}</style></head>'
            f'<body style="--a:{spec.get("accent", "#e8693c")};--a2:{spec.get("accent2", "rgba(232,105,60,.22)")}">'
            f'<div id="bg">{blobs}<div class="grid"></div></div><div id="dark"><div class="grid"></div></div>'
            f'<div id="cam">{"".join(parts)}</div><div id="tabs">{tabs}</div><div id="subs"></div><div id="flash"></div>'
            f'<script>window.SCN={json.dumps(S)};window.TOTAL={total:.3f};window.CTA={cta_at:.3f};window.TABS_ON={tabs_on};'
            f'window.WORDS={json.dumps(WORDS, ensure_ascii=False)};window.FLASH={json.dumps([round(cta_at + .1, 3)])};{JS}</script>'
            f'{host_html}</body></html>')
    out_dir = os.path.join(ROOT, "out"); os.makedirs(out_dir, exist_ok=True)
    hp = os.path.join(out_dir, f"{key}_ui.html"); open(hp, "w").write(page)
    seek = "t=>window.tick(t)"
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={"width": W, "height": H})
        pg.goto("file://" + hp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(700)
        if "--stills" in sys.argv:
            for k_, (a, e) in enumerate(zip(starts, ends)):
                for tt in (a + .5, min(e - .4, a + 3.2)):
                    pg.evaluate(seek, tt); pg.screenshot(path=os.path.join(out_dir, f"{key}_ui_{k_}_{tt:05.2f}.png"))
            br.close(); return
        silent = os.path.join(out_dir, f"{key}_silent.mp4")
        ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                               "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", "-preset", "veryfast", silent], stdin=subprocess.PIPE)
        for f in range(int(total * FPS)):
            pg.evaluate(seek, f / FPS)
            ff.stdin.write(pg.screenshot(type="jpeg", quality=93))
        br.close()
    ff.stdin.close(); ff.wait()
    wav = os.path.join(out_dir, f"{key}_bed.wav")
    sc_ = [{"type": "grid"}] * len(starts)
    sc_[-1] = {"type": "cta"}
    bed(starts, total, wav, {"keyword": spec["keyword"]}, sc_)
    final = os.path.join(out_dir, f"{key}_ig_nolvoice.mp4")
    final_mix(silent, wav, final, total)
    print(key, f"{total:.2f}s", [round(s, 2) for s in starts])


if __name__ == "__main__":
    build(sys.argv[1])
