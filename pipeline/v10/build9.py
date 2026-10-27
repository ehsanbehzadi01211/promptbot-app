"""v8 'editorial kinetic' reels for @ehbehzad, modelled on the owner's two reference videos
(cream/ink/accent editorial cards, mono chapter labels, masked headlines, UI mock cards,
karaoke subtitles, progress dots, comment-box CTA).  Renders a SILENT video + an audio bed
(music + SFX); the ElevenLabs voiceover is mixed in afterwards.
Usage: python3 build8.py <key> [ig|yt] [--stills]"""
import json, os, re, subprocess, sys, html, math, wave
import numpy as np
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
LEAD = 0.25          # voice starts this late in the video
TAIL = 1.4           # hold after the last word
SR = 44100
FONT = "file://" + ROOT + "/node_modules/@fontsource"

def esc(s):
    return html.escape(s)

def rich(s, em=True):
    """[[x]] -> accent em; newline -> line spans for the mask reveal."""
    out = []
    for line in s.split("\n"):
        line = esc(line)
        line = re.sub(r"\[\[(.+?)\]\]", r'<em>\1</em>', line)
        out.append(line)
    return out

def plain(s):
    s = re.sub(r"\[[a-z ]+\]", "", s)
    s = re.sub(r"[ً-ْ]", "", s)
    return s.replace("«", "").replace("»", "")

FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")

CSS = """
@font-face{font-family:Vaz;font-weight:500;src:url(FONT/vazirmatn/files/vazirmatn-arabic-500-normal.woff2)}
@font-face{font-family:Vaz;font-weight:700;src:url(FONT/vazirmatn/files/vazirmatn-arabic-700-normal.woff2)}
@font-face{font-family:Vaz;font-weight:800;src:url(FONT/vazirmatn/files/vazirmatn-arabic-800-normal.woff2)}
@font-face{font-family:Vaz;font-weight:900;src:url(FONT/vazirmatn/files/vazirmatn-arabic-900-normal.woff2)}
@font-face{font-family:Vaz;font-weight:900;src:url(FONT/vazirmatn/files/vazirmatn-latin-900-normal.woff2);unicode-range:U+0000-00FF}
@font-face{font-family:Vaz;font-weight:800;src:url(FONT/vazirmatn/files/vazirmatn-latin-800-normal.woff2);unicode-range:U+0000-00FF}
@font-face{font-family:Vaz;font-weight:700;src:url(FONT/vazirmatn/files/vazirmatn-latin-700-normal.woff2);unicode-range:U+0000-00FF}
@font-face{font-family:Vaz;font-weight:500;src:url(FONT/vazirmatn/files/vazirmatn-latin-500-normal.woff2);unicode-range:U+0000-00FF}
@font-face{font-family:Mono;font-weight:500;src:url(FONT/jetbrains-mono/files/jetbrains-mono-latin-500-normal.woff2)}
@font-face{font-family:Mono;font-weight:700;src:url(FONT/jetbrains-mono/files/jetbrains-mono-latin-700-normal.woff2)}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#111}
body{font-family:Vaz,"Inter",sans-serif;-webkit-font-smoothing:antialiased}
.lat{font-family:"Inter Display","Inter",Vaz,sans-serif;direction:ltr;unicode-bidi:isolate}
.mono{font-family:Mono,monospace}
.scene{position:absolute;inset:0;visibility:hidden;overflow:hidden;direction:rtl}
.cream{--bg:#F2F0EB;--fg:#121212;--mut:#8b8984;--line:rgba(0,0,0,.14);--em:var(--a);--card:#fff;--cfg:#121212}
.ink{--bg:#121212;--fg:#F2F0EB;--mut:#8f8d88;--line:rgba(255,255,255,.16);--em:var(--a);--card:#1d1d1d;--cfg:#F2F0EB}
.accent{--bg:var(--a);--fg:#fff;--mut:rgba(255,255,255,.78);--line:rgba(255,255,255,.35);--em:#121212;--card:#fff;--cfg:#121212}
.bgl{position:absolute;inset:0;background:var(--bg)}
.wipe .bgl{animation:wipe .42s cubic-bezier(.7,0,.2,1) var(--s) both}
@keyframes wipe{from{clip-path:circle(0% at 50% 62%)}to{clip-path:circle(140% at 50% 62%)}}
@keyframes vis{from{visibility:visible}to{visibility:visible}}
.stage{position:absolute;inset:0;color:var(--fg)}
.wipe .stage{animation:punch .55s cubic-bezier(.2,.8,.2,1) var(--s) both}
@keyframes punch{from{transform:scale(1.07)}to{transform:none}}
.head{position:absolute;top:96px;left:72px;right:72px;display:flex;justify-content:space-between;direction:ltr;font-family:Mono;font-weight:700;font-size:25px;letter-spacing:.06em;color:var(--fg)}
.head b{font-weight:700;color:var(--mut)}
.content{position:absolute;top:210px;left:72px;right:72px;height:1190px;display:flex;flex-direction:column;align-items:stretch}
.h1{font-weight:900;font-size:132px;line-height:1.16;letter-spacing:-.01em;color:var(--fg)}
.h1 .ln{display:block;overflow:hidden;padding-bottom:6px}
.h1 .ln>span{display:inline-block;white-space:nowrap}
.h1 em{font-style:normal;color:var(--em)}
.dot{display:inline-block;width:.2em;height:.2em;border-radius:50%;background:var(--a);margin-right:.08em;vertical-align:baseline}
.accent .dot{background:#121212}
.sub{margin-top:30px;font-size:50px;font-weight:700;color:var(--mut)}
.pill{align-self:flex-start;display:inline-flex;align-items:center;gap:20px;direction:ltr;background:var(--fg);color:var(--bg);font-family:"Inter Display",Inter,sans-serif;font-weight:800;font-size:46px;padding:20px 44px 22px 30px;border-radius:80px;margin-bottom:56px}
.pill .star{width:46px;height:46px;color:var(--a)}
.lbl{display:none;font-family:Mono;font-weight:700;font-size:28px;color:var(--mut);direction:ltr;text-align:right;margin-bottom:22px;letter-spacing:.05em}
/* motion primitives (absolute delays) */
.up{animation:up .5s cubic-bezier(.2,.9,.2,1) both}
@keyframes up{from{transform:translateY(110%)}to{transform:none}}
.rise{animation:rise .5s cubic-bezier(.2,.9,.2,1) both}
@keyframes rise{from{opacity:0;transform:translateY(70px)}to{opacity:1;transform:none}}
.pop{animation:pop .5s cubic-bezier(.3,1.6,.5,1) both}
@keyframes pop{from{opacity:0;transform:scale(.55)}to{opacity:1;transform:none}}
.slideL{animation:slideL .5s cubic-bezier(.2,.9,.2,1) both}
@keyframes slideL{from{opacity:0;transform:translateX(-140px)}to{opacity:1;transform:none}}
.slideR{animation:slideR .5s cubic-bezier(.2,.9,.2,1) both}
@keyframes slideR{from{opacity:0;transform:translateX(140px)}to{opacity:1;transform:none}}
.fade{animation:fade .4s ease both}
@keyframes fade{from{opacity:0}to{opacity:1}}
.shake{animation:shake .5s ease both}
@keyframes shake{0%,100%{transform:none}20%{transform:rotate(-7deg) scale(1.08)}40%{transform:rotate(6deg)}60%{transform:rotate(-4deg)}80%{transform:rotate(2deg)}}
.blink{animation:blink .9s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
/* hook card */
.tri{margin-top:auto;margin-bottom:40px;display:flex;align-items:stretch;border:4px solid var(--fg);border-radius:34px;height:250px;overflow:hidden;direction:ltr}
.tri .side{flex:1;display:flex;align-items:center;justify-content:center;font-family:Mono;font-weight:700;font-size:34px;color:var(--fg)}
.tri .mid{width:290px;background:var(--fg);display:flex;align-items:center;justify-content:center;position:relative}
.tri .mid svg{width:120px;height:120px;color:var(--a)}
.cursor{position:absolute;width:64px;height:64px}
/* underline sweep on em in hook */
.sweep{position:relative}
.sweep::after{content:"";position:absolute;left:0;right:0;bottom:8px;height:16px;background:var(--a);opacity:.28;transform-origin:right;animation:sw .7s cubic-bezier(.6,0,.2,1) .15s both;border-radius:8px}
@keyframes sw{from{transform:scaleX(0)}to{transform:scaleX(1)}}
/* tool */
.tool{margin-top:60px;display:flex;flex-direction:column;align-items:center;gap:40px}
.logo{width:330px;height:330px;border-radius:84px;background:var(--a);display:flex;align-items:center;justify-content:center;color:#fff;font-family:"Inter Display",Inter;font-weight:900;font-size:170px;box-shadow:0 30px 80px rgba(0,0,0,.25);position:relative}
.accent .logo{background:#121212}
.tname{font-family:"Inter Display",Inter;font-weight:900;font-size:128px;direction:ltr;letter-spacing:-.02em;line-height:1}
.turl{font-family:Mono;font-weight:700;font-size:44px;direction:ltr;color:var(--mut);border:3px solid var(--line);padding:14px 34px;border-radius:60px}
.tag{font-size:50px;font-weight:800;background:var(--fg);color:var(--bg);padding:14px 44px 20px;border-radius:60px}
.ripple{position:absolute;inset:-20px;border-radius:100px;border:6px solid var(--fg);animation:rip .7s ease-out both}
@keyframes rip{from{opacity:1;transform:scale(.8)}to{opacity:0;transform:scale(1.35)}}
/* grid */
.grid{margin-top:60px;display:grid;grid-template-columns:1fr 1fr;gap:26px}
.cell{border:4px solid var(--line);border-radius:30px;padding:26px 30px 30px;background:transparent;height:190px;display:flex;flex-direction:column;justify-content:space-between}
.cell .m{font-family:Mono;font-weight:700;font-size:28px;color:var(--a);direction:ltr;text-align:left}
.accent .cell .m{color:#121212}
.cell .t{font-size:58px;font-weight:900}
.cell.hi{animation-name:pop,hi;animation-duration:.5s,.9s;animation-fill-mode:both,both}
@keyframes hi{0%{background:transparent}30%{background:var(--fg);color:var(--bg)}100%{background:transparent}}
/* counter */
.big{font-family:"Inter Display",Inter;font-weight:900;font-size:270px;line-height:1;direction:ltr;text-align:center;margin-top:110px;letter-spacing:-.03em}
.unit{text-align:center;font-size:72px;font-weight:900;margin-top:20px}
.note{align-self:center;margin-top:44px;font-size:50px;font-weight:800;background:var(--fg);color:var(--bg);padding:16px 46px 22px;border-radius:70px}
.spark{margin-top:auto;margin-bottom:40px;height:260px}
.spark path{fill:none;stroke:var(--fg);stroke-width:10;stroke-linecap:round;stroke-dasharray:1400;animation:draw 1.2s ease both}
@keyframes draw{from{stroke-dashoffset:1400}to{stroke-dashoffset:0}}
/* compare */
.cmp{margin-top:70px;display:flex;gap:26px;direction:rtl}
.cc{flex:1;height:520px;border:4px solid var(--fg);border-radius:36px;display:flex;flex-direction:column;justify-content:space-between;padding:34px 26px}
.cc .n{font-family:"Inter Display",Inter,Vaz;font-weight:900;font-size:118px;direction:ltr;text-align:right;line-height:1}
.cc .l{font-size:44px;font-weight:800;line-height:1.3}
.cc .play{width:70px;height:70px}
.cc.f{background:var(--fg);color:var(--bg)}
.cc.f .n{color:var(--a)}
.accent .cc.f .n{color:var(--a)}
/* prompt */
.chat{margin-top:56px;background:var(--card);color:var(--cfg);border-radius:40px;box-shadow:0 30px 90px rgba(0,0,0,.18);padding:34px 40px 40px;border:3px solid var(--line)}
.chat .bar{display:flex;align-items:center;justify-content:space-between;direction:ltr;font-family:Mono;font-weight:700;font-size:30px;color:#888;margin-bottom:24px}
.chat .bar i{display:inline-block;width:18px;height:18px;border-radius:50%;background:var(--a);margin-right:12px}
.chat .txt{font-size:56px;font-weight:800;line-height:1.5;min-height:420px}
.chat .txt.ltr{direction:ltr;font-family:"Inter Display",Inter;font-weight:700;font-size:60px}
.caret{display:inline-block;width:6px;height:1em;background:var(--a);vertical-align:middle;margin:0 4px}
.send{margin-top:20px;display:flex;justify-content:flex-start;direction:ltr}
.send span{width:110px;height:110px;border-radius:50%;background:var(--a);display:flex;align-items:center;justify-content:center;color:#fff}
.send svg{width:56px;height:56px}
.press{animation:press .35s ease both}
@keyframes press{50%{transform:scale(.82)}}
/* steps */
.steps{margin-top:64px;display:flex;flex-direction:column;gap:30px}
.st{display:flex;align-items:center;gap:34px;border-bottom:3px solid var(--line);padding-bottom:30px}
.st .n{flex:none;width:118px;height:118px;border-radius:50%;background:var(--a);color:#fff;font-weight:900;font-size:64px;display:flex;align-items:center;justify-content:center}
.accent .st .n{background:#121212}
.st .x{font-size:62px;font-weight:900;line-height:1.25}
.st .x .lat{font-weight:800}
/* warn */
.warn{margin-top:40px;width:250px;height:250px;border-radius:50%;background:var(--a);color:#fff;font-family:Inter;font-weight:900;font-size:190px;display:flex;align-items:center;justify-content:center;margin-bottom:70px}
.accent .warn{background:#121212}
/* proof */
.wave{margin-top:auto;margin-bottom:60px;height:360px;display:flex;align-items:center;justify-content:space-between;direction:ltr}
.wave i{display:block;width:16px;border-radius:10px;background:var(--a);animation:wv 1s ease-in-out infinite alternate}
@keyframes wv{from{height:12%}to{height:100%}}
.play2{display:flex;align-items:center;gap:22px;direction:ltr;font-family:Mono;font-weight:700;font-size:40px;margin-bottom:70px}
.play2 span{width:96px;height:96px;border-radius:50%;background:var(--fg);color:var(--bg);display:flex;align-items:center;justify-content:center}
/* image upload */
.art{margin:70px auto 0;width:560px;height:560px;border-radius:44px;background:radial-gradient(circle at 70% 30%,#ffd27a 0 12%,transparent 13%),linear-gradient(180deg,#ff8a5c 0%,#e3477a 45%,#3a2b6b 46%,#2a1f52 100%);position:relative;overflow:hidden;box-shadow:0 30px 90px rgba(0,0,0,.35)}
.art::before{content:"";position:absolute;left:-10%;right:-10%;bottom:0;height:52%;background:linear-gradient(160deg,transparent 30%,#1b1438 31%),linear-gradient(200deg,transparent 40%,#251b49 41%);}
.apps{margin-top:60px;display:flex;gap:22px;justify-content:center;direction:ltr}
.apps span{font-family:"Inter Display",Inter;font-weight:800;font-size:46px;border:4px solid var(--fg);padding:16px 34px;border-radius:60px}
.apps span.on{background:var(--a);border-color:var(--a);color:#fff}
.drop{animation:drop .9s cubic-bezier(.5,0,.3,1) both}
@keyframes drop{0%{transform:translateY(-160px) rotate(-6deg);opacity:0}60%{transform:translateY(16px) rotate(2deg);opacity:1}100%{transform:none}}
/* code */
.term{margin-top:56px;background:#0d1117;border-radius:34px;border:3px solid rgba(255,255,255,.12);overflow:hidden;direction:ltr}
.term .bar{height:74px;display:flex;align-items:center;gap:14px;padding:0 30px;background:#161b22}
.term .bar i{width:22px;height:22px;border-radius:50%;background:#ff5f57}.term .bar i:nth-child(2){background:#febc2e}.term .bar i:nth-child(3){background:#28c840}
.term .bar b{margin-left:auto;font-family:Mono;font-size:28px;color:#8b949e}
.term pre{font-family:Mono;font-weight:500;font-size:37px;line-height:1.75;color:#e6edf3;padding:30px 34px 40px;white-space:pre;min-height:600px}
.term .k{color:#ff7b72}.term .f{color:#d2a8ff}.term .c{color:#8b949e}.term .s{color:#a5d6ff}.term .nm{color:#79c0ff}
/* chart */
.chart{margin-top:50px;background:var(--card);border-radius:36px;padding:20px;border:3px solid var(--line)}
.chart svg{display:block;width:100%;height:720px}
.ma{fill:none;stroke-width:7;stroke-dasharray:3000;animation:draw2 1.8s ease both}
@keyframes draw2{from{stroke-dashoffset:3000}to{stroke-dashoffset:0}}
/* cta */
.cbox{margin-top:70px;background:#fff;color:#121212;border-radius:36px;overflow:hidden;box-shadow:0 30px 90px rgba(0,0,0,.25)}
.cbox .tabs{display:flex;gap:40px;padding:22px 36px;background:#f6f8fa;border-bottom:2px solid #e3e3e3;font-weight:800;font-size:38px;color:#888}
.cbox .tabs b{color:#121212;border-bottom:5px solid var(--a);padding-bottom:6px}
.cbox .in{margin:30px 36px 0;border:4px solid var(--a);border-radius:22px;padding:18px 30px;font-size:110px;font-weight:900;min-height:180px;line-height:1.3}
.cbox .row{display:flex;justify-content:flex-start;padding:26px 36px 30px}
.cbox .btn{background:#1f883d;color:#fff;font-weight:900;font-size:44px;padding:14px 50px 22px;border-radius:20px}
.dm{margin-top:44px;background:#fff;color:#121212;border-radius:36px;padding:30px 34px;box-shadow:0 30px 90px rgba(0,0,0,.25)}
.dm .who{display:flex;align-items:center;gap:20px;direction:ltr;margin-bottom:22px}
.dm .av{width:84px;height:84px;border-radius:50%;background:linear-gradient(135deg,#feda75,#d62976,#4f5bd5);display:flex;align-items:center;justify-content:center;color:#fff;font-family:Inter;font-weight:900;font-size:44px}
.dm .who b{font-family:Inter;font-weight:800;font-size:40px}.dm .who small{font-family:Inter;color:#888;font-size:30px;margin-left:8px}
.dm .bub{display:inline-block;background:#efefef;border-radius:34px;padding:18px 34px 24px;font-size:48px;font-weight:800}
.dm .lk{margin-top:18px;display:flex;align-items:center;justify-content:center;gap:18px;background:var(--a);color:#fff;border-radius:24px;padding:22px 30px 28px;font-size:48px;font-weight:900}
.dm .lk svg{width:52px;height:52px}
.follow{margin-top:34px;align-self:center;display:flex;align-items:center;gap:20px;font-size:44px;font-weight:900;background:#121212;color:#fff;padding:18px 44px 24px;border-radius:70px}
.ytarrow{margin:80px auto 0;width:220px;height:220px;color:var(--a);animation:bob .7s ease-in-out infinite alternate}
@keyframes bob{from{transform:translateY(-20px)}to{transform:translateY(20px)}}
.subbtn{margin:70px auto 0;display:flex;align-items:center;gap:24px;background:#ff0033;color:#fff;font-family:Inter;font-weight:900;font-size:60px;padding:26px 66px;border-radius:80px;direction:ltr}
/* bottom: progress + karaoke */
.prog{position:absolute;left:72px;right:72px;top:1452px;height:40px;direction:ltr}
.prog .tr{position:absolute;left:0;right:0;top:18px;height:3px;background:var(--line)}
.prog .fl{position:absolute;left:0;top:17px;height:5px;background:var(--fg);width:0}
.prog .pd{position:absolute;top:12px;width:16px;height:16px;border-radius:50%;background:var(--line);margin-left:-8px}
.prog .pd.on{background:var(--fg)}
.prog .hd{position:absolute;top:8px;width:24px;height:24px;border-radius:50%;background:var(--fg);margin-left:-12px}
.meta{position:absolute;left:72px;right:72px;top:1500px;display:flex;justify-content:space-between;direction:ltr;font-family:Mono;font-weight:700;font-size:24px;color:var(--mut);letter-spacing:.06em}
.kara{position:absolute;left:110px;right:110px;top:1556px;text-align:center;font-size:54px;font-weight:900;line-height:1.45;color:var(--fg)}
.kara span{opacity:.32;transition:none}
.kara span.p{opacity:1}
.kara span.c{opacity:1;color:var(--em)}

/* ---- v9 energy ---- */
.content{transform-origin:50% 40%}
.kb{animation:kb var(--dur) linear var(--s) both}
@keyframes kb{from{transform:scale(1)}to{transform:scale(1.045)}}
.flash{position:absolute;inset:0;background:var(--a);mix-blend-mode:screen;opacity:0;pointer-events:none;animation:flash .45s ease-out both}
@keyframes flash{0%{opacity:.85}100%{opacity:0}}
.jolt{animation:jolt .5s cubic-bezier(.3,1.5,.4,1) both}
@keyframes jolt{0%{transform:scale(1.6) rotate(-4deg);opacity:0}35%{opacity:1}60%{transform:scale(.94) rotate(1.5deg)}100%{transform:none}}
.glitch{animation:glitch 2.2s steps(1) infinite}
@keyframes glitch{0%,86%,100%{text-shadow:none;transform:none}88%{text-shadow:-8px 0 #00e5ff,8px 0 #ff2a6d;transform:translateX(6px)}91%{text-shadow:6px 0 #00e5ff,-6px 0 #ff2a6d;transform:translateX(-8px)}94%{text-shadow:none;transform:translateX(3px)}}
.t-shock .h1{font-size:170px;line-height:1.08}
.t-shock .h1 em{color:var(--a)}
.tape{margin-top:auto;margin-bottom:30px;margin-left:-140px;margin-right:-140px;transform:rotate(-4deg);background:var(--a);color:#fff;font-weight:900;font-size:50px;white-space:nowrap;overflow:hidden;padding:18px 0 24px;box-shadow:0 20px 60px rgba(0,0,0,.4)}
.tape span{display:inline-block;animation:marq 6s linear infinite}
@keyframes marq{from{transform:translateX(0)}to{transform:translateX(50%)}}
.cond{margin-top:34px;font-size:56px;font-weight:900;color:var(--fg);background:rgba(255,255,255,.08);border-right:12px solid var(--a);padding:18px 30px 24px;border-radius:14px;align-self:flex-start}
.cream .cond{background:rgba(0,0,0,.05)}
/* skill card */
.sk{margin-top:40px;display:flex;flex-direction:column;gap:44px}
.sk .top{display:flex;align-items:center;gap:30px}
.sk .num{flex:none;width:170px;height:170px;border-radius:44px;background:var(--a);color:#fff;font-weight:900;font-size:110px;display:flex;align-items:center;justify-content:center;box-shadow:0 20px 60px rgba(0,0,0,.3)}
.sk .of{font-family:Mono;font-weight:700;font-size:34px;color:var(--mut);direction:ltr}
.sk .nm{font-family:"Inter Display",Inter,Vaz;font-weight:900;font-size:124px;line-height:1.02;direction:ltr;text-align:right;letter-spacing:-.02em}
.sk .star2{align-self:flex-start;display:inline-flex;gap:14px;align-items:center;direction:ltr;font-family:Mono;font-weight:700;font-size:38px;border:3px solid var(--line);padding:12px 30px;border-radius:60px}
.sk .star2 b{color:#f5b301}
.ba{display:flex;align-items:center;gap:28px;border-radius:30px;padding:36px 36px 42px;font-size:62px;font-weight:900;line-height:1.3}
.ba i{flex:none;font-style:normal;width:84px;height:84px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:Inter;font-size:54px;color:#fff}
.ba.bad{background:rgba(229,72,77,.16)}
.accent .ba.bad,.accent .ba.good{background:rgba(0,0,0,.2)}
.ba.bad span{opacity:.75}
.ba.bad i{background:#e5484d}
.ba.bad span{text-decoration:line-through;text-decoration-color:#e5484d;text-decoration-thickness:6px}
.ba.good{background:rgba(22,163,74,.14)}
.ba.good i{background:#16a34a}
.emo{align-self:center;margin-top:50px;font-size:300px;line-height:1;font-family:"Noto Color Emoji"}
.flt{display:inline-block;animation:flt 1.6s ease-in-out infinite alternate}
@keyframes flt{from{transform:translateY(-14px) rotate(-5deg)}to{transform:translateY(14px) rotate(5deg)}}
.cmd{direction:ltr;text-align:left;font-family:Mono;font-weight:700;font-size:34px;line-height:1.5;background:#0d1117;color:#e6edf3;border-radius:22px;padding:22px 28px;word-break:break-all;border:3px solid rgba(255,255,255,.12)}
.cmd b{color:var(--a)}
/* chat bubbles */
.cv{margin-top:60px;display:flex;flex-direction:column;gap:34px}
.bq{max-width:84%;border-radius:40px;padding:30px 40px 38px;font-size:58px;font-weight:800;line-height:1.4}
.bq.me{align-self:flex-start;background:var(--a);color:#fff;border-bottom-right-radius:10px}
.bq.ai{align-self:flex-end;background:var(--card);color:var(--cfg);border:3px solid var(--line);border-bottom-left-radius:10px}
.bq .who{display:block;font-family:Mono;font-size:28px;font-weight:700;opacity:.7;margin-bottom:10px;direction:ltr;text-align:left}
.stamp{align-self:center;margin-top:40px;font-weight:900;font-size:76px;color:#e5484d;border:8px solid #e5484d;padding:6px 40px 16px;border-radius:20px;transform:rotate(-8deg)}
.stampin{animation:stampin .45s cubic-bezier(.3,1.6,.5,1) both}
@keyframes stampin{from{opacity:0;transform:rotate(-8deg) scale(2.4)}to{opacity:1;transform:rotate(-8deg) scale(1)}}
.warn.ok{background:#16a34a}
"""

STAR = '<svg class="star" viewBox="0 0 24 24" fill="currentColor"><path d="M12 1.5l1.6 7.1 6.6-3.2-4.5 5.7 7 1.9-7.2 1.4 3.6 6.4-6-4.3L12 22.5l-1.1-6-6 4.3 3.6-6.4-7.2-1.4 7-1.9-4.5-5.7 6.6 3.2z"/></svg>'
STAR_B = STAR.replace('class="star"', "")
CUR = '<svg class="cursor" viewBox="0 0 24 24"><path d="M4 2l15 10-6.5 1.3L16 21l-3 1.3-3.5-7.6L4 19z" fill="#fff" stroke="#121212" stroke-width="1.6" stroke-linejoin="round"/></svg>'
LINK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"><path d="M10 14a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/><path d="M14 10a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/></svg>'
SEND = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg>'
PLAY = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4l13 8-13 8z"/></svg>'


class Scene:
    def __init__(self, sc, s, e, i, n, spec, words):
        self.sc, self.s, self.e, self.i, self.n, self.spec, self.words = sc, s, e, i, n, spec, words

    def d(self, off):
        return f"animation-delay:{self.s + off:.3f}s"

    def h1(self, text, off=0.08, step=0.09, instant=False):
        lines = rich(text)
        out = []
        for k, ln in enumerate(lines):
            dot = '<i class="dot"></i>' if k == len(lines) - 1 else ""
            if instant:
                out.append(f'<span class="ln"><span>{ln}{dot}</span></span>')
            else:
                out.append(f'<span class="ln"><span class="up" style="{self.d(off + k * step)}">{ln}{dot}</span></span>')
        return f'<div class="h1">{"".join(out)}</div>'

    def body(self):
        sc, t, d = self.sc, self.sc["type"], self.d
        if t == "hook":
            pill = f'<div class="pill">{STAR}<span>{esc(sc["pill"])}</span></div>'
            title = self.h1(sc["title"], instant=True).replace("<em>", '<em class="sweep">')
            sub = f'<div class="sub">{esc(sc["sub"])}</div>'
            kw = esc(self.spec["keyword"])
            card = (f'<div class="tri"><div class="side">/free</div><div class="mid">{STAR_B}'
                    f'<div style="position:absolute;left:150px;top:150px" class="fade" ><div style="{d(0.6)}" class="pop">{CUR}</div></div></div>'
                    f'<div class="side" style="font-family:Vaz;font-weight:900;font-size:46px">«{kw}»</div></div>')
            return pill + title + sub + card
        if t == "shock":
            lines = rich(sc["title"])
            h = "".join(f'<span class="ln"><span class="jolt glitch" style="animation-delay:{self.s + .05 + k * .22:.3f}s,{self.s + 1.2 + k*.3:.3f}s">{ln}</span></span>' for k, ln in enumerate(lines))
            kw = esc(self.spec["keyword"])
            tape = ("کامنت کن «" + kw + "» ✦ ") * 8
            cond = f'<div class="cond rise" style="{d(sc.get("cond_at", 1.4))}">{esc(sc["sub"])}</div>' if sc.get("sub") else ""
            pill = f'<div class="pill pop" style="{d(.0)}">{STAR}<span>{esc(sc["pill"])}</span></div>' if sc.get("pill") else ""
            emo = f'<div class="emo jolt" style="{d(sc.get("emo_at", .6))}"><span class="flt">{sc["emoji"]}</span></div>' if sc.get("emoji") else ""
            return pill + f'<div class="h1">{h}</div>' + cond + emo + f'<div class="tape rise" style="{d(.5)}"><span>{tape}</span></div>'
        if t == "skill":
            return (f'<div class="sk"><div class="top"><div class="num jolt" style="{d(.05)}">{esc(sc["num"])}</div>'
                    f'<div><div class="of rise" style="{d(.2)}">SKILL {esc(sc["of"])}</div></div></div>'
                    f'<div style="overflow:hidden"><div class="nm up" style="{d(.25)}">{esc(sc["name"])}</div></div>'
                    f'<div class="star2 pop" style="{d(.45)}"><b>★</b>{esc(sc["stars"])} GitHub</div>'
                    f'<div class="ba bad slideR" style="{d(sc.get("bad_at", .8))}"><i>✕</i><span>{esc(sc["bad"])}</span></div>'
                    f'<div class="ba good slideR" style="{d(sc.get("good_at", 1.8))}"><i>✓</i><span>{esc(sc["good"])}</span></div>'
                    + (f'<div class="cmd rise" style="{d(.6)}"><b>$</b> <span data-type="{esc(sc["cmd"])}" data-s="{self.s + .8:.3f}" data-d="{min(1.6, .03*len(sc["cmd"])):.2f}"></span><span class="caret"></span></div>' if sc.get("cmd") else "") + '</div>')
        if t == "chat2":
            bub = ""
            for k, (who, txt, at) in enumerate(sc["msgs"]):
                cls = "me" if who == "me" else "ai"
                lab = "YOU" if who == "me" else esc(sc.get("app", "AI"))
                bub += f'<div class="bq {cls} {"slideL" if cls=="me" else "slideR"}" style="{d(at)}"><span class="who">{lab}</span>{esc(txt)}</div>'
            st = f'<div class="stamp stampin" style="{d(sc["stamp_at"])}">{esc(sc["stamp"])}</div>' if sc.get("stamp") else ""
            return self.h1(sc["title"]) + f'<div class="cv">{bub}</div>' + st
        if t == "tool":
            return (f'<div class="lbl rise" style="{d(.05)}">{esc(sc["label"])}</div>'
                    f'<div class="tool"><div class="logo pop" style="{d(.12)}">{esc(sc["mark"])}'
                    f'<div class="ripple" style="{d(.95)}"></div>'
                    f'<div style="position:absolute;left:230px;top:240px"><div class="slideR" style="{d(.55)}">{CUR}</div></div></div>'
                    f'<div style="overflow:hidden"><div class="tname up" style="{d(.3)}">{esc(sc["name"])}<i class="dot" style="margin-left:.08em"></i></div></div>'
                    f'<div class="turl rise" style="{d(.5)}">{esc(sc["url"])}</div>'
                    f'<div class="tag pop" style="{d(.75)}">{esc(sc["tag"])}</div></div>')
        if t == "grid":
            cells = "".join(f'<div class="cell hi pop" style="animation-delay:{self.s + .35 + k * .12:.3f}s,{self.s + 1.1 + k * .35:.3f}s">'
                            f'<div class="m">/{esc(m)}</div><div class="t">{esc(x)}</div></div>' for k, (m, x) in enumerate(sc["items"]))
            return f'<div class="lbl rise" style="{d(.05)}">{esc(sc["label"])}</div>' + self.h1(sc["title"]) + f'<div class="grid">{cells}</div>'
        if t == "counter":
            return (f'<div class="lbl rise" style="{d(.05)}">{esc(sc["label"])}</div>'
                    f'<div class="big" data-count="{sc["value"]}" data-s="{self.s + .15:.3f}" data-d="1.1">0</div>'
                    f'<div class="unit rise" style="{d(.4)}">{esc(sc["unit"])}</div>'
                    f'<div class="note pop" style="{d(.9)}">{esc(sc["note"])}</div>'
                    f'<svg class="spark" viewBox="0 0 936 260" preserveAspectRatio="none"><path style="{d(.3)}" d="M10 240 C 150 230, 210 200, 300 190 S 470 150, 560 120 S 760 60, 926 20"/></svg>')
        if t == "compare":
            cards = ""
            for k, (n, l) in enumerate(sc["items"]):
                cards += (f'<div class="cc pop{" f" if k == 0 else ""}" style="{d(.35 + k * .18)}"><div class="play">{PLAY}</div>'
                          f'<div><div class="n">{esc(n)}</div><div class="l">{esc(l)}</div></div></div>')
            return f'<div class="lbl rise" style="{d(.05)}">{esc(sc["label"])}</div>' + self.h1(sc["title"]) + f'<div class="cmp">{cards}</div>'
        if t == "prompt":
            ltr = "" if sc.get("rtl") else " ltr"
            dur = max(1.2, min(self.e - self.s - 1.4, len(sc["text"]) * 0.035))
            return (f'<div class="lbl rise" style="{d(.05)}">{esc(sc["label"])}</div>' + self.h1(sc["title"]) +
                    f'<div class="chat rise" style="{d(.25)}"><div class="bar"><span><i></i>{esc(sc["app"])}</span><span>NEW CHAT</span></div>'
                    f'<div class="txt{ltr}"><span data-type="{esc(sc["text"])}" data-s="{self.s + .6:.3f}" data-d="{dur:.2f}"></span><span class="caret blink"></span></div>'
                    f'<div class="send"><span class="press" style="{d(.6 + dur + .1)}">{SEND}</span></div></div>')
        if t == "steps":
            rows = ""
            for k, x in enumerate(sc["items"]):
                x = esc(x)
                x = re.sub(r"([A-Za-z][A-Za-z0-9 .\-]*[A-Za-z0-9])", r'<span class="lat">\1</span>', x)
                at_ = sc["items_at"][k] if sc.get("items_at") else .3 + k * .32
                rows += f'<div class="st slideR" style="{d(at_)}"><div class="n">{str(k + 1).translate(FA)}</div><div class="x">{x}</div></div>'
            return f'<div class="lbl rise" style="{d(.05)}">{esc(sc["label"])}</div>' + self.h1(sc["title"]) + f'<div class="steps">{rows}</div>'
        if t == "warn":
            return (f'<div class="lbl rise" style="{d(.05)}">{esc(sc["label"])}</div>'
                    f'<div class="warn pop{" ok" if sc.get("icon") else ""}" style="{d(.1)}"><span class="shake" style="display:block;{d(.45)}">{esc(sc.get("icon","!"))}</span></div>' + self.h1(sc["title"], off=.2) +
                    f'<div class="sub rise" style="{d(.6)}">{esc(sc["sub"])}</div>')
        if t == "proof":
            bars = "".join(f'<i style="animation-duration:{.35 + (k * 37 % 23) / 40:.2f}s;animation-delay:{-(k * 13 % 17) / 10:.2f}s"></i>' for k in range(44))
            return (f'<div class="lbl rise" style="{d(.05)}">{esc(sc["label"])}</div>' + self.h1(sc["title"]) +
                    f'<div class="wave fade" style="{d(.3)}">{bars}</div><div class="play2 rise" style="{d(.5)}"><span>{PLAY}</span>0:31 · voice by ElevenLabs</div>')
        if t == "image":
            apps = "".join(f'<span class="pop{" on" if k == 0 else ""}" style="{d(.9 + k * .15)}">{esc(a)}</span>' for k, a in enumerate(sc["apps"]))
            return (f'<div class="lbl rise" style="{d(.05)}">{esc(sc["label"])}</div>' + self.h1(sc["title"]) +
                    f'<div class="art drop" style="{d(.25)}"></div><div class="apps">{apps}</div>')
        if t == "code":
            js = json.dumps(sc["lines"])
            return (f'<div class="lbl rise" style="{d(.05)}">{esc(sc["label"])}</div>' + self.h1(sc["title"]) +
                    f'<div class="term rise" style="{d(.2)}"><div class="bar"><i></i><i></i><i></i><b>ma_cross.pine</b></div>'
                    f'<pre data-code=\'{esc(js)}\' data-s="{self.s + .5:.3f}" data-d="{max(1.5, self.e - self.s - .9):.2f}"></pre></div>')
        if t == "chart":
            return (f'<div class="lbl rise" style="{d(.05)}">{esc(sc["label"])}</div>' + self.h1(sc["title"]) +
                    f'<div class="chart rise" style="{d(.15)}">{chart_svg(self.s, self.spec["accent"])}</div>')
        if t == "cta":
            kw = self.spec["keyword"]
            return (f'<div class="lbl rise" style="{d(.05)}">{esc(sc["label"])}</div>' + self.h1("کامنت کن") +
                    f'<div class="cbox rise" style="{d(.2)}"><div class="tabs"><b>Comment</b><span>@ehbehzad</span></div>'
                    f'<div class="in"><span data-type="{esc(kw)}" data-s="{self.s + .5:.3f}" data-d="{.18 * len(kw):.2f}"></span><span class="caret blink"></span></div>'
                    f'<div class="row"><span class="btn press" style="{d(.75 + .18 * len(kw))}">ارسال</span></div></div>'
                    f'<div class="dm slideL" style="{d(1.25 + .18 * len(kw))}"><div class="who"><span class="av">e</span><b>ehbehzad</b><small>· Direct</small></div>'
                    f'<div class="bub">اینم لینکش 👇</div><div class="lk">{LINK}<span>{esc(sc["link"])}</span></div></div>'
                    f'<div class="follow pop" style="{d(2.0 + .18 * len(kw))}">+ فالو برای ابزارهای رایگان</div>')
        if t == "ytcta":
            return (f'<div class="lbl rise" style="{d(.05)}">{esc(sc["label"])}</div>' + self.h1("لینک‌ها توی\n[[توضیحات]]") +
                    f'<svg class="ytarrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v16M5 13l7 7 7-7"/></svg>'
                    f'<div class="subbtn pop" style="{d(.6)}">{PLAY.replace("<svg", "<svg width=60 height=60")}Subscribe</div>')
        raise ValueError(t)

    def html(self, total, starts):
        sc = self.sc
        cls = f'scene {sc["bg"]} t-{sc["type"]}' + (" wipe" if self.i else "")
        series = esc(self.spec["series"])
        lab = f'{self.i:02d} / {sc.get("label", "00 / HOOK").split("/")[-1].strip()}' if self.i else "00 / HOOK"
        head = f'<div class="head"><span>@EHBEHZAD · {series}</span><b>{lab}</b></div>'
        dots = "".join(f'<i class="pd" data-at="{s_:.3f}" style="left:{s_ / total * 100:.3f}%"></i>' for s_ in starts)
        prog = f'<div class="prog"><div class="tr"></div><div class="fl"></div>{dots}<i class="hd"></i></div>'
        meta = '<div class="meta"><span class="ts">00s</span><span>INSTAGRAM · YOUTUBE · TELEGRAM @EHBEHZAD</span></div>'
        ws = "".join(f'<span data-t="{a:.3f}" data-g="{k // 6 if len(self.words) > 7 else 0}">{esc(w)} </span>' for k, (w, a) in enumerate(self.words))
        kara = f'<div class="kara">{ws}</div>'
        flash = f'<div class="flash" style="animation-delay:{self.s:.3f}s"></div>' if sc["type"] in ("shock", "skill") else ""
        life = f"animation:vis {self.e - self.s:.3f}s linear {self.s:.3f}s"
        return (f'<section class="{cls}" style="{life};--s:{self.s:.3f}s;--dur:{self.e - self.s:.3f}s"><div class="bgl"></div><div class="stage">{head}'
                f'<div class="content kb">{self.body()}</div>{prog}{meta}{kara}{flash}</div></section>')


def chart_svg(s, acc):
    rng = np.random.default_rng(7)
    n, p, pts = 46, 100.0, []
    for k in range(n):
        drift = -0.5 if k < 22 else 0.9
        o = p; c = p + drift + rng.normal(0, 1.6)
        hi = max(o, c) + abs(rng.normal(0, 1)); lo = min(o, c) - abs(rng.normal(0, 1))
        pts.append((o, hi, lo, c)); p = c
    lo_, hi_ = min(x[2] for x in pts) - 2, max(x[1] for x in pts) + 2
    Y = lambda v: 700 - (v - lo_) / (hi_ - lo_) * 660 - 20
    X = lambda k: 30 + k * (980 - 60) / (n - 1)
    out = []
    for k, (o, h, l, c) in enumerate(pts):
        col = "#16a34a" if c >= o else "#e5484d"
        out.append(f'<g class="fade" style="animation-delay:{s + .3 + k * .02:.3f}s"><line x1="{X(k):.1f}" x2="{X(k):.1f}" y1="{Y(h):.1f}" y2="{Y(l):.1f}" stroke="{col}" stroke-width="3"/>'
                   f'<rect x="{X(k) - 7:.1f}" y="{Y(max(o, c)):.1f}" width="14" height="{max(3, abs(Y(o) - Y(c))):.1f}" fill="{col}"/></g>')
    closes = [x[3] for x in pts]
    def ma(m):
        return [np.mean(closes[max(0, k - m + 1):k + 1]) for k in range(n)]
    f_, s_ = ma(5), ma(14)
    path = lambda arr: "M" + " L".join(f"{X(k):.1f} {Y(v):.1f}" for k, v in enumerate(arr))
    out.append(f'<path class="ma" d="{path(f_)}" stroke="#2f81f7" style="animation-delay:{s + .8:.3f}s"/>')
    out.append(f'<path class="ma" d="{path(s_)}" stroke="#f59e0b" style="animation-delay:{s + .9:.3f}s"/>')
    for k in range(15, n):
        if f_[k - 1] <= s_[k - 1] and f_[k] > s_[k]:
            x, y = X(k), Y(pts[k][2]) + 40
            out.append(f'<g class="pop" style="animation-delay:{s + 1.9:.3f}s;transform-origin:{x:.0f}px {y:.0f}px"><path d="M{x:.0f} {y - 26:.0f} l26 44 h-52z" fill="{acc}"/>'
                       f'<rect x="{x - 70:.0f}" y="{y + 30:.0f}" width="140" height="60" rx="14" fill="{acc}"/><text x="{x:.0f}" y="{y + 72:.0f}" text-anchor="middle" font-family="Inter" font-weight="900" font-size="36" fill="#fff">BUY</text></g>')
            break
    return f'<svg viewBox="0 0 1000 720">{"".join(out)}</svg>'


JS = r"""
const FA='۰۱۲۳۴۵۶۷۸۹';
function fmt(n){return Math.round(n).toLocaleString('en-US')}
function fitAll(){document.querySelectorAll('.h1').forEach(h=>{const W=h.clientWidth;let m=0;h.querySelectorAll('.ln>span').forEach(x=>{m=Math.max(m,x.scrollWidth)});const fs=parseFloat(getComputedStyle(h).fontSize);if(m>W){h.style.fontSize=(fs*W/m*0.98)+'px'}})}
window.fitAll=fitAll;
window.tick=function(t){
 document.querySelectorAll('[data-count]').forEach(e=>{const s=+e.dataset.s,d=+e.dataset.d,v=+e.dataset.count;let p=Math.min(1,Math.max(0,(t-s)/d));p=1-Math.pow(1-p,3);e.textContent=fmt(v*p)});
 document.querySelectorAll('[data-type]').forEach(e=>{const s=+e.dataset.s,d=+e.dataset.d,x=[...e.dataset.type];const n=Math.round(Math.min(1,Math.max(0,(t-s)/d))*x.length);e.textContent=x.slice(0,n).join('')});
 document.querySelectorAll('[data-code]').forEach(e=>{const L=JSON.parse(e.dataset.code),s=+e.dataset.s,d=+e.dataset.d;const all=L.join('\n');const n=Math.round(Math.min(1,Math.max(0,(t-s)/d))*all.length);
   let txt=all.slice(0,n).replace(/&/g,'&amp;').replace(/</g,'&lt;');
   txt=txt.replace(/("[^"\n]*"?)/g,'<span class="s">$1</span>').replace(/^(\/\/.*)$/gm,'<span class="c">$1</span>').replace(/\b(ta|shape)\./g,'<span class="nm">$1</span>.').replace(/\b(indicator|plotshape|alertcondition|sma|crossover)\b/g,'<span class="f">$1</span>').replace(/\b(true|close)\b/g,'<span class="k">$1</span>');
   e.innerHTML=txt+'<span class="caret" style="background:#58a6ff"></span>'});
 document.querySelectorAll('.prog').forEach(p=>{const T=window.TOTAL;p.querySelector('.fl').style.width=(Math.min(1,t/T)*100)+'%';p.querySelector('.hd').style.left=(Math.min(1,t/T)*100)+'%';p.querySelectorAll('.pd').forEach(d=>d.classList.toggle('on',t>=+d.dataset.at))});
 document.querySelectorAll('.ts').forEach(e=>{e.textContent=String(Math.floor(t)).padStart(2,'0')+'s'});
 document.querySelectorAll('.kara').forEach(k=>{const sp=[...k.children];let cur=-1;sp.forEach((s,i)=>{if(t>=+s.dataset.t)cur=i});const c0=Math.max(0,cur);const g=+(sp[c0]&&sp[c0].dataset.g||0);sp.forEach((s,i)=>{s.style.display=(+s.dataset.g==g)?'':'none';s.className=i<cur?'p':(i==cur?'c':'')})});
};
"""


def timeline(spec, words, variant):
    scenes = spec["scenes"]
    toks, owner = [], []
    for i, sc in enumerate(scenes):
        for w in sc["voice"].replace("[excited]", "").split():
            toks.append(plain(w)); owner.append(i)
    ts = [LEAD + x for x in words["t"]]
    assert len(ts) == len(toks), (len(ts), len(toks))
    n = len(scenes)
    starts = [0.0]
    for i in range(1, n):
        k = owner.index(i)
        starts.append(max(starts[-1] + .8, ts[k] - 0.12))
    end_voice = LEAD + words["end"]
    total = end_voice + TAIL + 0.6
    sw = [[] for _ in range(n)]
    for w, a, o in zip(toks, ts, owner):
        sw[o].append((w, a))
    if variant == "yt":
        cta = dict(scenes[-1]); cta["type"] = "ytcta"; cta["bg"] = "ink"
        scenes = scenes[:-1] + [cta]
        total = starts[-1] + 3.4
        sw[-1] = [(w, starts[-1] + 0.2 + k * 0.35) for k, w in enumerate("لینک‌ها توی توضیحات؛ سابسکرایب یادت نره".split())]
    ends = starts[1:] + [total]
    ends = [min(total, e + 0.45) for e in ends]
    return scenes, starts, ends, sw, total


def bed(starts, total, out, spec, scenes, seed=3):
    """Energetic 124 bpm beat + SFX on every scene change."""
    rng = np.random.default_rng(seed)
    N = int(total * SR); t = np.arange(N) / SR
    sig = np.zeros(N)
    bpm = 124; beat = 60 / bpm
    def add(at, x, g=1.0):
        a = int(at * SR)
        if a >= N: return
        x = x[:N - a]; sig[a:a + len(x)] += g * x
    def kick():
        tt = np.arange(int(.35 * SR)) / SR
        return np.sin(2 * np.pi * (45 + 110 * np.exp(-tt * 28)) * tt) * np.exp(-tt * 9)
    def hat(l=.05):
        tt = np.arange(int(l * SR)) / SR
        return rng.normal(0, 1, len(tt)) * np.exp(-tt * 90) * .25
    def clap():
        tt = np.arange(int(.18 * SR)) / SR
        return rng.normal(0, 1, len(tt)) * np.exp(-tt * 26) * .45
    K, Hh, C = kick(), hat(), clap()
    roots = [55.0, 55.0, 65.41, 49.0]
    nb = int(total / beat) + 1
    for b in range(nb):
        at = b * beat
        add(at, K, .9)
        add(at + beat / 2, Hh, .8); add(at + beat / 4 * 3, Hh, .4)
        if b % 2 == 1: add(at, C, .8)
        f = roots[(b // 8) % 4]
        tt = np.arange(int(beat * .9 * SR)) / SR
        bass = np.sign(np.sin(2 * np.pi * f * tt)) * .22 * np.exp(-tt * 3)
        add(at + beat / 2, bass, .55)
        # plucky arp
        notes = [f * 4, f * 5, f * 6, f * 8]
        tt2 = np.arange(int(beat / 2 * SR)) / SR
        for q in range(2):
            fr = notes[(b * 2 + q) % 4]
            add(at + q * beat / 2, np.sin(2 * np.pi * fr * tt2) * np.exp(-tt2 * 14) * .12)
    # SFX
    def whoosh(l=.45):
        tt = np.arange(int(l * SR)) / SR
        nz = rng.normal(0, 1, len(tt))
        env = np.sin(np.pi * tt / l) ** 2
        # crude band sweep via moving average of varying width
        out_ = np.convolve(nz, np.ones(9) / 9, "same") * env
        return out_ * .9
    def pop(f=880):
        tt = np.arange(int(.12 * SR)) / SR
        return np.sin(2 * np.pi * f * tt * (1 + tt * 6)) * np.exp(-tt * 40) * .5
    def ding():
        tt = np.arange(int(.9 * SR)) / SR
        return (np.sin(2 * np.pi * 1320 * tt) + .5 * np.sin(2 * np.pi * 1980 * tt)) * np.exp(-tt * 5) * .35
    def tick():
        tt = np.arange(int(.02 * SR)) / SR
        return rng.normal(0, 1, len(tt)) * np.exp(-tt * 300) * .35
    for i, s in enumerate(starts):
        if i: add(s - .22, whoosh(), .9)
        add(s + .12, pop(700 + 120 * (i % 4)), .8)
    def boom():
        tt = np.arange(int(1.2 * SR)) / SR
        return (np.sin(2 * np.pi * (38 + 60 * np.exp(-tt * 6)) * tt) * np.exp(-tt * 3.2) + rng.normal(0, 1, len(tt)) * np.exp(-tt * 18) * .5) * .9
    for i, sc in enumerate(scenes):
        s = starts[i]
        if sc["type"] == "shock":
            add(s + .05, boom(), 1.0)
            for k, _ in enumerate(sc["title"].split("\n")[1:], 1):
                add(s + .05 + k * .22, boom(), .6)
        if sc["type"] == "skill":
            add(s + .05, boom(), .55)
            add(s + sc.get("bad_at", .8) + .05, pop(300), .9)
            add(s + sc.get("good_at", 1.8) + .05, ding(), .8)
        if sc["type"] == "chat2":
            for (_, _, at) in sc["msgs"]:
                add(s + at + .05, pop(1200), .7)
            if sc.get("stamp"):
                add(s + sc["stamp_at"] + .05, boom(), .7)
        if sc["type"] in ("prompt", "cta", "code"):
            span = 1.6 if sc["type"] != "code" else 2.6
            for k in range(int(span / .07)):
                add(s + .55 + k * .07, tick(), .9)
        if sc["type"] == "cta":
            add(s + 1.3 + .18 * len(spec["keyword"]), ding(), 1)
        if sc["type"] in ("grid", "compare", "steps"):
            for k in range(6):
                add(s + .35 + k * .15, pop(1000 + 90 * k), .5)
    # duck music a bit under voice region: simple fades
    fade = np.minimum(1, np.minimum(t / .3, np.maximum(0, (total - t)) / 1.0))
    sig = sig / (np.max(np.abs(sig)) + 1e-9) * .85 * fade
    st = np.stack([sig, sig], 1)
    with wave.open(out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())


def build(key, variant="ig", stills=False):
    spec = json.load(open(os.path.join(ROOT, os.environ.get("SPEC", "spec.json"))))[key]
    words = json.load(open(os.path.join(ROOT, os.environ.get("WORDS", "words"), key + ".json")))
    scenes, starts, ends, sw, total = timeline(spec, words, variant)
    for i, sc in enumerate(scenes):
        ws_ = sw[i]
        def wat(k):
            k = min(int(k), len(ws_) - 1)
            return max(.15, ws_[k][1] - starts[i] - .05) if ws_ else .5
        for k in list(sc.keys()):
            if k.endswith("_w"):
                v = sc[k]
                sc[k[:-2] + "_at"] = [wat(x) for x in v] if isinstance(v, list) else wat(v)
        if sc.get("msgs"):
            sc["msgs"] = [(a, b, wat(c[2:]) if isinstance(c, str) and c.startswith("w:") else c) for a, b, c in sc["msgs"]]
    objs = [Scene(sc, s, e, i, len(scenes), spec, sw[i]) for i, (sc, s, e) in enumerate(zip(scenes, starts, ends))]
    page = (f'<!doctype html><html lang="fa"><head><meta charset="utf-8"><style>{CSS.replace("FONT", FONT)}</style></head>'
            f'<body style="--a:{spec["accent"]}">{"".join(o.html(total, starts) for o in objs)}'
            f'<script>window.TOTAL={total:.3f};{JS}</script></body></html>')
    out_dir = os.path.join(ROOT, "out"); os.makedirs(out_dir, exist_ok=True)
    hp = os.path.join(out_dir, f"{key}_{variant}.html"); open(hp, "w").write(page)
    seek = "t=>{document.getAnimations().forEach(a=>{a.pause();a.currentTime=t*1000});window.tick(t)}"
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H})
        pg.goto("file://" + hp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500); pg.evaluate("window.fitAll()")
        if stills:
            for s, e in zip(starts, ends):
                for tt in (s + 0.02, min(e - .5, s + 2.2)):
                    pg.evaluate(seek, tt)
                    pg.screenshot(path=os.path.join(out_dir, f"{key}_{variant}_{tt:05.2f}.png"))
            b.close(); return
        silent = os.path.join(out_dir, f"{key}_{variant}_silent.mp4")
        ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                               "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "veryfast", silent], stdin=subprocess.PIPE)
        for f in range(int(total * FPS)):
            pg.evaluate(seek, f / FPS)
            ff.stdin.write(pg.screenshot(type="jpeg", quality=92))
        b.close()
    ff.stdin.close(); ff.wait()
    wav = os.path.join(out_dir, f"{key}_{variant}_bed.wav")
    bed(starts, total, wav, spec, scenes)
    final = os.path.join(out_dir, f"{key}_{variant}_nolvoice.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "volume=0.30", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", final], check=True)
    json.dump({"starts": starts, "total": total, "lead": LEAD}, open(os.path.join(out_dir, f"{key}_{variant}_tl.json"), "w"))
    print(key, variant, f"{total:.2f}s", [round(s, 2) for s in starts])


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "ig", "--stills" in sys.argv)
