"""Animated 'host' character overlay (the owner's cartoon portrait) for build9.py / laptop.py pages.

The portrait is one flat image (media/mascot_1_ehsan.png, 1280x720, face centre ~(585,230)).
It is animated like a cut-out puppet: the lower lip + goatee are a second copy of the image clipped to
that region and moved down while a dark mouth shape opens behind them; the whole head bobs/tilts gently.
Mouth timing comes from the narration's word start times (no audio analysis needed).

host_block(img_url, words, modes, accent) -> HTML+CSS+JS string to append to <body> AFTER the page's
own script (it wraps window.tick).
  words: [[start_s, end_s], ...] absolute times on the video timeline
  modes: [[from_s, mode], ...] sorted; mode = "big" | "corner" | "off"
"""
import json

FACE = dict(ox=325, oy=-20)      # image offset so the face centre lands at (260, 250) in a 520 box

CSS = """
#host{position:absolute;z-index:50;border-radius:50%;overflow:hidden;opacity:0;
  box-shadow:0 18px 50px rgba(0,0,0,.45);border:7px solid var(--hostc);background:#e8761a}
.t-shock .emo{opacity:0!important}
#host .hin{position:absolute;left:0;top:0;width:520px;height:520px;transform-origin:0 0}
#host .head{position:absolute;inset:0;transform-origin:260px 330px}
#host .im{position:absolute;left:-325px;top:20px;width:1280px;height:720px;background-size:1280px 720px}
#host .hole{position:absolute;left:226px;top:232px;width:68px;height:4px;border-radius:50%;
  background:radial-gradient(ellipse at 50% 35%,#5a1d1d 0,#2a0b0b 70%);transform:rotate(-9deg);transform-origin:50% 0}
#host .hole:before{content:"";position:absolute;left:12%;right:12%;top:0;height:30%;background:#f4efe6;border-radius:0 0 40% 40%;opacity:.85}
#host .jaw{position:absolute;inset:0;
  clip-path:polygon(223px 240px,300px 228px,309px 252px,296px 280px,262px 292px,230px 284px,214px 262px)}
"""

JS = r"""
(function(){
const HW=window.HOSTWORDS, HM=window.HOSTMODES, H=document.getElementById('host');
const jaw=H.querySelector('.jaw'), hole=H.querySelector('.hole'), head=H.querySelector('.head'), hin=H.querySelector('.hin');
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)), eo=x=>1-Math.pow(1-cl(x),3);
const POS=window.HOSTPOS||{big:{d:500,x:290,y:790},corner:{d:260,x:36,y:150},off:{d:260,x:36,y:150}};
function modeAt(t){let m='off',s=0,pm='off';for(const [a,mm] of HM){if(t>=a){pm=m;m=mm;s=a}}return [m,pm,s]}
function openAt(t){for(const [a,b] of HW){if(t>=a-.02&&t<b){const k=t-a;return cl(0.35+0.65*Math.abs(Math.sin(Math.PI*k*6.5)))*cl((b-t)/.06)*cl((t-a+.02)/.05)}}return 0}
const _t=window.tick;
window.tick=function(t){ if(_t)_t(t);
  const [m,pm,s]=modeAt(t), k=eo((t-s)/.35), A=POS[pm], B=POS[m];
  const op=(pm==='off'?0:1)*(1-k)+(m==='off'?0:1)*k;
  const d=A.d+(B.d-A.d)*k, x=A.x+(B.x-A.x)*k, y=A.y+(B.y-A.y)*k;
  H.style.opacity=op; H.style.width=H.style.height=d+'px'; H.style.left=x+'px'; H.style.top=y+'px';
  hin.style.transform=`scale(${(d-14)/520})`;
  const o=openAt(t);
  jaw.style.transform=`translateY(${o*11}px)`; hole.style.height=(o*18)+'px'; hole.style.opacity=o>0.03?1:0;
  const talk=o>0?1:0;
  head.style.transform=`rotate(${Math.sin(t*1.7)*1.6+talk*Math.sin(t*9)*0.6}deg) translateY(${Math.sin(t*2.3)*3-o*2}px)`;
};
})();
"""


def host_block(img_url, words, modes, accent="#F97316"):
    img = f'<div class="im" style="background-image:url({img_url})"></div>'
    return (f'<style>{CSS}</style>'
            f'<div id="host" style="--hostc:{accent}"><div class="hin"><div class="head">{img}'
            f'<div class="hole"></div><div class="jaw">{img}</div></div></div></div>'
            f'<script>window.HOSTWORDS={json.dumps(words)};window.HOSTMODES={json.dumps(modes)};{JS}</script>')


def words_to_spans(times, end, gap=0.42):
    """word start times -> [start, end] spans (a word ends at the next start, max `gap` s)."""
    out = []
    for i, a in enumerate(times):
        b = times[i + 1] if i + 1 < len(times) else end
        out.append([round(a, 3), round(min(b - 0.03, a + gap), 3)])
    return out


# ---------------------------------------------------------------------------------------------
# Robot host: frosted white glass robot (media/mascot_2_robot_glass.png, 768x1024) with a BLANK
# black screen face; eyes and mouth are drawn here as glowing shapes, so lip-sync is clean.
ROBOT_CSS = """
#host{position:absolute;z-index:50;border-radius:50%;overflow:hidden;opacity:0;
  box-shadow:0 18px 50px rgba(0,0,0,.45);border:7px solid var(--hostc);background:#1b1b1d}
.t-shock .emo{opacity:0!important}
#host .hin{position:absolute;left:0;top:0;width:520px;height:520px;transform-origin:0 0}
#host .head{position:absolute;inset:0;transform-origin:260px 330px}
#host .im{position:absolute;left:-21px;top:-42px;width:553px;height:737px;background-size:553px 737px}
#host .eye{position:absolute;top:196px;width:40px;height:56px;margin-left:-20px;border-radius:50%;
  background:#eaf8ff;box-shadow:0 0 14px #bfe9ff,0 0 30px rgba(150,220,255,.7)}
#host .mouth{position:absolute;left:260px;top:292px;width:74px;height:10px;margin-left:-37px;box-sizing:border-box;
  filter:drop-shadow(0 0 6px #bfe9ff) drop-shadow(0 0 14px rgba(150,220,255,.7))}
"""

ROBOT_JS = r"""
(function(){
const HW=window.HOSTWORDS, HM=window.HOSTMODES, H=document.getElementById('host');
const head=H.querySelector('.head'), hin=H.querySelector('.hin'), m=H.querySelector('.mouth');
const eL=H.querySelector('.eL'), eR=H.querySelector('.eR');
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)), eo=x=>1-Math.pow(1-cl(x),3);
const POS=window.HOSTPOS||{big:{d:500,x:290,y:790},corner:{d:260,x:36,y:150},off:{d:260,x:36,y:150}};
function modeAt(t){let m='off',s=0,pm='off';for(const [a,mm] of HM){if(t>=a){pm=m;m=mm;s=a}}return [m,pm,s]}
function openAt(t){for(const [a,b] of HW){if(t>=a-.02&&t<b){const k=t-a;return cl(0.3+0.7*Math.abs(Math.sin(Math.PI*k*6.5)))*cl((b-t)/.06)*cl((t-a+.02)/.05)}}return 0}
const BL=[1.2,4.1,6.6,9.8,12.4,15.9,18.3,21.7,24.2,27.8,30.1,33.6,36.2,39.5,42.8,45.3,48.9,52.1,55.4,58.8];
const _t=window.tick;
window.tick=function(t){ if(_t)_t(t);
  const [md,pm,s]=modeAt(t), k=eo((t-s)/.35), A=POS[pm], B=POS[md];
  const op=(pm==='off'?0:1)*(1-k)+(md==='off'?0:1)*k;
  const d=A.d+(B.d-A.d)*k, x=A.x+(B.x-A.x)*k, y=A.y+(B.y-A.y)*k;
  H.style.opacity=op; H.style.width=H.style.height=d+'px'; H.style.left=x+'px'; H.style.top=y+'px';
  hin.style.transform=`scale(${(d-14)/520})`;
  const o=openAt(t);
  // mouth: smile curve when quiet, rounded opening while talking
  if(o>0.05){const w=70-o*20, h=12+o*32;
    m.style.width=w+'px'; m.style.marginLeft=(-w/2)+'px'; m.style.height=h+'px'; m.style.top=(290-o*10)+'px';
    m.style.background='#eaf8ff'; m.style.border='none'; m.style.borderRadius='45% 45% 50% 50%';
  } else {
    m.style.width='76px'; m.style.marginLeft='-38px'; m.style.height='24px'; m.style.top='280px';
    m.style.background='transparent'; m.style.border='none'; m.style.borderBottom='9px solid #eaf8ff'; m.style.borderRadius='0 0 50% 50%';
  }
  // eyes: blink + look around a little, squash slightly while talking
  let bl=1; for(const b of BL){const q=t-b; if(q>=0&&q<.16) bl=Math.abs(q-.08)/.08}
  const lx=Math.sin(t*.7)*5, sy=bl*(1-o*.12);
  for(const [e,cx] of [[eL,215],[eR,305]]){e.style.left=(cx+lx)+'px'; e.style.transform=`scaleY(${Math.max(.08,sy)})`}
  head.style.transform=`rotate(${Math.sin(t*1.7)*2+(o>0?Math.sin(t*9)*0.8:0)}deg) translateY(${Math.sin(t*2.3)*4-o*3}px)`;
};
})();
"""


def robot_block(img_url, words, modes, accent="#F97316"):
    return (f'<style>{ROBOT_CSS}</style>'
            f'<div id="host" style="--hostc:{accent}"><div class="hin"><div class="head">'
            f'<div class="im" style="background-image:url({img_url})"></div>'
            f'<div class="eye eL"></div><div class="eye eR"></div><div class="mouth"></div></div></div></div>'
            f'<script>window.HOSTWORDS={json.dumps(words)};window.HOSTMODES={json.dumps(modes)};{ROBOT_JS}</script>')


def host_any(kind, root, words, modes, accent):
    """kind: True/"robot" -> glass robot (default), "ehsan" -> owner's cartoon."""
    import os
    if kind == "ehsan":
        return host_block("file://" + os.path.join(root, "out", "mascot_1_ehsan.png"), words, modes, accent)
    return robot_block("file://" + os.path.join(root, "out", "mascot_2_robot_glass.png"), words, modes, accent)
