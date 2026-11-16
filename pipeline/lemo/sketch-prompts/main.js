// Sketchnote (Lemo-Opuscar style, vertical 1080x1920, Persian): one page of visual notes drawn while you watch.
// Fineliner (wobbly double pass), grey marker (multiply hatching), ONE yellow for the thread; camera rides the page,
// ends by pulling back to the whole page. Page contract: READY, DUR, render(t), TEXTS, EV.
import { clamp, lerp, seg, ss, eo, eio, mulberry, TAU } from '/core/lib.js';

const W = 1080, H = 1920, PW = 1080, PH = 3560;           // screen and page (world) size
const C = document.getElementById('c'), X = C.getContext('2d');
const WD = await (await fetch('words.json')).json();
const T = i => WD.lead + WD.t[Math.min(i, WD.t.length - 1)];
const DUR = WD.lead + WD.end + 3.2; window.DUR = DUR;
const INK = '#1e1e22', NOTE = '#5b5852', PAPER = '#fbfaf6', YEL = 'rgba(255,205,40,.80)', YEL2 = '#f5aa00';
const GREY = ['rgba(100,100,110,.16)', 'rgba(80,80,92,.28)', 'rgba(52,52,64,.45)'];

// ---------- paper texture (page space, anchored) ----------
const GR = (() => { const c = document.createElement('canvas'); c.width = c.height = 256; const x = c.getContext('2d'), R = mulberry(5), im = x.createImageData(256, 256);
  for (let i = 0; i < im.data.length; i += 4) { const v = R(); im.data[i] = im.data[i + 1] = im.data[i + 2] = v < .5 ? 120 : 255; im.data[i + 3] = 10 + R() * 10; } x.putImageData(im, 0, 0); return c; })();

// ---------- camera: world -> screen ----------
let CAM = { x: PW / 2, y: 960, z: 1 };
const keys = [];   // [t, x, y, z]
function camAt(t) {
  if (t <= keys[0][0]) return keys[0];
  for (let i = 0; i < keys.length - 1; i++) { const a = keys[i], b = keys[i + 1]; if (t < b[0]) { const k = eio((t - a[0]) / (b[0] - a[0]));
    const z = Math.exp(lerp(Math.log(a[3]), Math.log(b[3]), k)); return [t, lerp(a[1], b[1], k), lerp(a[2], b[2], k), z]; } }
  return keys[keys.length - 1];
}
function applyCam(t) { const c = camAt(t); CAM = { x: c[1], y: c[2], z: c[3] }; X.setTransform(c[3], 0, 0, c[3], W / 2 - c[1] * c[3], H / 2 - c[2] * c[3]); }

// ---------- pen primitives (progress p 0..1 reveals the stroke) ----------
let BOIL = 0;
function wob(pts, seed, amp = 1.4) {           // resample + three sines along the normal (boils on twos)
  const R = mulberry(seed), ph = [R() * TAU + BOIL, R() * TAU - BOIL * .7, R() * TAU + BOIL * 1.3], out = [];
  let L = 0; for (let i = 1; i < pts.length; i++) L += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
  let d = 0;
  for (let i = 0; i < pts.length - 1; i++) {
    const a = pts[i], b = pts[i + 1], l = Math.hypot(b[0] - a[0], b[1] - a[1]) || 1, nx = -(b[1] - a[1]) / l, ny = (b[0] - a[0]) / l, n = Math.max(1, Math.ceil(l / 3));
    for (let j = 0; j < n; j++) { const u = j / n, s = (d + u * l) / 40, o = amp * (Math.sin(s * .9 + ph[0]) * .6 + Math.sin(s * 2.3 + ph[1]) * .3 + Math.sin(s * 7 + ph[2]) * .15);
      out.push([lerp(a[0], b[0], u) + nx * o, lerp(a[1], b[1], u) + ny * o]); }
    d += l;
  }
  out.push(pts[pts.length - 1]); return out;
}
function strokePts(pts, p, lw = 4.2, col = INK, seed = 1) {
  if (p <= 0) return; const q = wob(pts, seed), n = Math.max(2, Math.round(q.length * clamp(p)));
  for (const [w, a, s2] of [[lw, 1, 0], [lw * .6, .5, 7]]) {
    const r = s2 ? wob(pts, seed + s2, 2.2) : q; X.globalAlpha = a; X.strokeStyle = col; X.lineWidth = w; X.lineCap = X.lineJoin = 'round';
    X.beginPath(); X.moveTo(r[0][0], r[0][1]); for (let i = 1; i < Math.min(n, r.length); i++) X.lineTo(r[i][0], r[i][1]); X.stroke();
  }
  X.globalAlpha = 1;
}
const rectPts = (x, y, w, h, r = 22) => { const p = []; const arc = (cx, cy, a0) => { for (let i = 0; i <= 6; i++) { const a = a0 + i / 6 * Math.PI / 2; p.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]); } };
  arc(x + w - r, y + r, -Math.PI / 2); arc(x + w - r, y + h - r, 0); arc(x + r, y + h - r, Math.PI / 2); arc(x + r, y + r, Math.PI); p.push([x + w - r + 4, y - 1]); return p; };
const circPts = (cx, cy, r, n = 40) => Array.from({ length: n + 3 }, (_, i) => [cx + Math.cos(i / n * TAU - 1.2) * r, cy + Math.sin(i / n * TAU - 1.2) * r]);
// marker: bowed translucent strokes at one angle, clipped to a path, multiplied
function marker(pathFn, p, col, ang = -.5, seed = 3, bb = [0, 0, PW, PH]) {
  if (p <= 0) return; const R = mulberry(seed);
  X.save(); pathFn(); X.clip(); X.globalCompositeOperation = 'multiply'; X.strokeStyle = col; X.lineCap = 'round';
  const [x0, y0, x1, y1] = bb, span = (x1 - x0) + (y1 - y0), n = Math.ceil(span / 22), m = Math.ceil(n * clamp(p));
  for (let i = 0; i < m; i++) { const o = -span / 2 + i * 22 + R() * 6, cx = (x0 + x1) / 2 + o * Math.cos(ang + Math.PI / 2), cy = (y0 + y1) / 2 + o * Math.sin(ang + Math.PI / 2);
    X.lineWidth = 26 + R() * 6; X.beginPath(); X.moveTo(cx - Math.cos(ang) * span, cy - Math.sin(ang) * span);
    X.quadraticCurveTo(cx + 6, cy + 6, cx + Math.cos(ang) * span, cy + Math.sin(ang) * span); X.stroke(); }
  X.restore();
}
// hand-lettered text written right-to-left (Persian pen direction) with a little tilt/bob per word
function write(s, x, y, size, p, col = INK, font = 'Hand', align = 'center', seed = 2) {
  if (p <= 0) return; X.save(); X.font = `${font === 'Hand' ? '' : '800 '}${size}px ${font}`; X.fillStyle = col; X.textBaseline = 'middle';
  const rtl = /[؀-ۿ]/.test(s); X.direction = rtl ? 'rtl' : 'ltr'; X.textAlign = align;
  const w = X.measureText(s).width, left = align === 'center' ? x - w / 2 : align === 'right' ? x - w : x;
  const R = mulberry(seed); X.translate(x, y); X.rotate((R() - .5) * .03); X.translate(-x, -y);
  X.beginPath(); const k = clamp(p); if (rtl) X.rect(left + w * (1 - k) - 6, y - size, w * k + 12, size * 2); else X.rect(left - 6, y - size, w * k + 12, size * 2); X.clip();
  X.fillText(s, x, y); X.restore();
}
// fat yellow arrow along a path
function fatArrow(pts, p, seed) {
  if (p <= 0) return; strokePts(pts, p, 22, YEL, seed); strokePts(pts, p, 3.2, INK, seed + 1);
  if (p > .95) { const a = pts[pts.length - 2], b = pts[pts.length - 1], ang = Math.atan2(b[1] - a[1], b[0] - a[0]);
    strokePts([[b[0] - Math.cos(ang - .5) * 30, b[1] - Math.sin(ang - .5) * 30], b, [b[0] - Math.cos(ang + .5) * 30, b[1] - Math.sin(ang + .5) * 30]], seg(p, .95, 1), 4, INK, seed + 2); }
}

// ---------- the page: a list of drawn elements, each timed to a word ----------
const E = [];   // {at, dur, draw(p)}
const add = (wi, dur, draw, off = 0) => E.push({ at: T(wi) + off, dur, draw });
const box = (x, y, w, h, wi, opt = {}) => {
  const pts = rectPts(x, y, w, h, opt.r || 26), path = () => { X.beginPath(); X.roundRect(x, y, w, h, opt.r || 26); };
  add(wi, .45, p => { if (opt.fill) { X.save(); path(); X.fillStyle = PAPER; X.globalAlpha = clamp(p * 3); X.fill(); X.restore(); } strokePts(pts, p, 4.4, INK, x + y); }, opt.off || 0);
  if (opt.marker) add(wi, .5, p => marker(path, p, opt.marker, -.6, x * 3 + y, [x, y, x + w, y + h]), (opt.off || 0) + .35);
  // drop shadow down-right in grey marker
  add(wi, .3, p => marker(() => { X.beginPath(); X.rect(x + w, y + 12, 12, h); X.rect(x + 12, y + h, w, 12); }, p, GREY[1], 0, 9, [x, y, x + w + 12, y + h + 12]), (opt.off || 0) + .3);
};

// block 1 — the empty prompt box, crossed out (w0-4)
box(140, 170, 800, 260, 0, { fill: true });
add(0, .5, p => write('پرامپت از خودت…', 880, 300, 64, p, NOTE, 'Vaz', 'right'), .3);
add(1, .2, p => { if (Math.floor(T(1) * 3 + p) % 2 === 0) strokePts([[230, 260], [230, 340]], p, 6, INK, 11); });
add(3, .45, p => { strokePts([[160, 190], [920, 410]], p, 10, '#d23b2a', 12); strokePts([[920, 190], [160, 410]], seg(p, .3, 1), 10, '#d23b2a', 13); });
add(4, .5, p => write('ننویس!', 540, 520, 110, p, INK), 0);
// block 2 — the library (w5-20)
const B2 = 760;
add(5, .6, p => { marker(() => { X.beginPath(); X.ellipse(540, B2 + 70, 360, 70, -.02, 0, TAU); }, p, YEL, -.3, 21, [180, B2, 900, B2 + 140]); write('prompts.chat', 540, B2 + 70, 112, seg(p, .2, 1), INK, 'Hand'); });
add(6, .8, p => write('بزرگ‌ترین کتابخونه‌ی', 540, B2 + 230, 76, p, INK));
add(8, .8, p => write('پرامپت متن‌باز دنیا', 540, B2 + 330, 76, p, INK));
// star + count
const st = () => { X.beginPath(); for (let i = 0; i < 10; i++) { const r = i % 2 ? 46 : 104, a = -Math.PI / 2 + i * Math.PI / 5; X.lineTo(330 + Math.cos(a) * r, B2 + 540 + Math.sin(a) * r); } X.closePath(); };
add(14, .5, p => { const pts = []; for (let i = 0; i <= 10; i++) { const r = i % 2 ? 46 : 104, a = -Math.PI / 2 + i * Math.PI / 5; pts.push([330 + Math.cos(a) * r, B2 + 540 + Math.sin(a) * r]); } strokePts(pts, p, 4.6, INK, 31); });
add(14, .5, p => marker(st, p, YEL, -.5, 33, [220, B2 + 430, 440, B2 + 650]), .4);
add(16, .7, p => write('+170K', 700, B2 + 515, 110, p, INK, 'Hand'));
add(18, .6, p => write('ستاره توی گیت‌هاب', 700, B2 + 615, 48, p, NOTE, 'Vaz'));
// block 3 — roles (w21-28)
const B3 = 1520;
add(21, .7, p => { marker(() => { X.beginPath(); X.roundRect(250, B3 - 10, 580, 110, 18); }, p, GREY[0], -.2, 41, [250, B3 - 10, 830, B3 + 100]); write('هزاران پرامپت آماده', 540, B3 + 45, 70, seg(p, .1, 1), INK); });
const roles = [[24, 'مشاور', '💬'], [25, 'مترجم', '🌐'], [26, 'معلم', '📚'], [27, 'برنامه‌نویس', '</>'], [28, 'بازاریاب', '📣']];
roles.forEach(([wi, name, ic], i) => {
  const cx = [810, 540, 270, 680, 400][i], cy = B3 + (i < 3 ? 260 : 520), w = 250, h = 210, x = cx - w / 2, y = cy - h / 2;
  box(x, y, w, h, wi, { fill: true, marker: i === 0 ? YEL : null });
  add(wi, .4, p => { if (ic === '</>') write('</>', cx, cy - 30, 64, p, INK, 'Hand'); else { X.save(); X.globalAlpha = clamp(p * 2); X.filter = 'grayscale(1) contrast(1.4)'; X.font = '64px "Noto Color Emoji"'; X.textAlign = 'center'; X.textBaseline = 'middle'; X.fillText(ic, cx, cy - 30); X.restore(); } }, .25);
  add(wi, .45, p => write(name, cx, cy + 55, 46, p, INK, 'Vaz'), .35);
});
// block 4 — works with (w29-35)
const B4 = 2280;
add(29, .4, p => write('با این‌ها کار می‌کنه:', 540, B4, 58, p, NOTE, 'Vaz'));
[[30, 'ChatGPT', 830], [31, 'Claude', 540], [33, 'Gemini', 250]].forEach(([wi, n, cx], i) => {
  box(cx - 135, B4 + 70, 270, 120, wi, { fill: true, r: 60 }); add(wi, .45, p => write(n, cx, B4 + 130, 54, p, INK, 'Hand'), .3);
});
// block 5 — numbered steps with fat arrows (w36-44)
const B5 = 2620;
const banner = (x, y, w, num, label, wi) => {
  add(wi, .5, p => { marker(() => { X.beginPath(); X.moveTo(x, y); X.lineTo(x + w, y); X.lineTo(x + w - 24, y + 55); X.lineTo(x + w, y + 110); X.lineTo(x, y + 110); X.closePath(); }, p, YEL, -.4, wi * 7, [x, y, x + w, y + 110]);
    strokePts([[x, y], [x + w, y], [x + w - 24, y + 55], [x + w, y + 110], [x, y + 110], [x, y]], p, 4.4, INK, wi * 3); });
  add(wi, .4, p => { strokePts(circPts(x + w - 70, y + 55, 38), p, 4, INK, wi); write(num, x + w - 70, y + 58, 52, p, INK, 'Hand'); write(label, x + w - 130, y + 58, 56, seg(p, .2, 1), INK, 'Hand', 'right'); }, .3);
};
banner(560, B5, 400, '۱', 'سرچ', 36); banner(120, B5, 400, '۲', 'کپی', 38); banner(340, B5 + 220, 520, '۳', 'جاهای خالی رو پر کن', 40);
add(38, .4, p => fatArrow([[550, B5 + 55], [530, B5 + 55]], p, 51), -.1);
add(40, .45, p => fatArrow([[300, B5 + 120], [380, B5 + 210]], p, 52), -.15);
// block 6 — CC0 (w45-52)
const B6 = 3040;
box(170, B6, 740, 200, 45, { fill: true, marker: GREY[0] });
add(46, .6, p => write('مال عموم (CC0)', 540, B6 + 70, 76, p, INK));
add(50, .6, p => write('آزادانه استفاده کن', 540, B6 + 150, 50, p, NOTE, 'Vaz'));
add(50, .5, p => { strokePts([[300, B6 + 185], [780, B6 + 185]], p, 6, YEL2, 61); }, .3);
// block 7 — the keyword bubble (w53-)
const B7 = 3320;
add(53, .5, p => { const pts = rectPts(250, B7, 580, 170, 60); pts.push([330, B7 + 168], [290, B7 + 230], [380, B7 + 168]); strokePts(pts, p, 4.6, INK, 71); });
add(54, .55, p => { marker(() => { X.beginPath(); X.roundRect(250, B7, 580, 170, 60); }, p, YEL, -.5, 73, [250, B7, 830, B7 + 170]); write('کتابخونه', 540, B7 + 88, 104, seg(p, .2, 1), INK); });

// camera: ride the blocks, then pull back to the whole page
const fitZ = Math.min(H / (PH + 80), 1);
// blocks: [start word, centre y, zoom]; the camera holds on a block and moves 0.6 s before the next one starts
const BL = [[0, 470, 1.35], [5, B2 + 320, 1.35], [21, B3 + 360, 1.25], [29, B4 + 120, 1.3], [36, B5 + 170, 1.2], [45, B6 + 100, 1.3], [53, B7 + 90, 1.3]];
BL.forEach((b, i) => { const st = i ? T(b[0]) - .35 : 0, en = i + 1 < BL.length ? T(BL[i + 1][0]) - .35 - .6 : DUR - 3.4; keys.push([st, 540, b[1], b[2]], [Math.max(st + .01, en), 540, b[1], b[2]]); });
keys.push([DUR - 2.9, 540, PH / 2, fitZ], [DUR, 540, PH / 2, fitZ]);

// ---------- subtitles: a paper slip with washi tape at the bottom ----------
const toks = WD.toks.map(s => s.replace(/[«»]/g, ''));
const groups = []; { let g = [], n = 0; toks.forEach((w, i) => { g.push(i); n++; if (/[.!؟?؛،:]$/.test(w) || n >= 5) { groups.push(g); g = []; n = 0; } }); if (g.length) groups.push(g); }
let SUB = null;
function subtitle(t) {
  SUB = null; let cur = -1; for (let i = 0; i < toks.length; i++) if (t >= T(i)) cur = i;
  if (cur < 0 || t > DUR - 3) return;
  const g = groups.find(g => g.includes(cur)), line = g.map(i => toks[i]).join(' '), a = seg(t, T(g[0]) - .1, T(g[0]) + .1);
  X.setTransform(1, 0, 0, 1, 0, 0); X.save(); X.globalAlpha = a; X.font = '800 52px Vaz'; X.direction = 'rtl';
  const w = Math.min(980, X.measureText(line).width + 90), x = (W - w) / 2, y = 1690 + (1 - a) * 6;
  X.shadowColor = 'rgba(0,0,0,.18)'; X.shadowBlur = 14; X.shadowOffsetY = 4; X.fillStyle = '#fffdf6'; X.beginPath(); X.rect(x, y, w, 116); X.fill(); X.shadowColor = 'transparent';
  X.fillStyle = 'rgba(160,160,170,.55)'; X.save(); X.translate(x + w - 40, y + 2); X.rotate(.5); X.fillRect(-55, -16, 110, 32); X.restore();
  X.fillStyle = INK; X.textAlign = 'center'; X.textBaseline = 'middle'; X.fillText(line, W / 2, y + 57); X.restore();
  SUB = { id: 'sub' + groups.indexOf(g), text: line, x0: x, y0: y, x1: x + w, y1: y + 110, pass: true };
}

// ---------- follow slip at the very end ----------
const avatar = new Image(); avatar.src = 'robot.png'; await avatar.decode().catch(() => {});
function follow(t) {
  const k = eo(seg(t, DUR - 2.5, DUR - 2.0)); if (k <= 0) return;
  X.setTransform(1, 0, 0, 1, 0, 0); X.save(); X.globalAlpha = k; X.fillStyle = 'rgba(251,250,246,.86)'; X.fillRect(0, 0, W, H);
  X.translate(0, (1 - k) * 40); X.fillStyle = '#fffdf6'; X.shadowColor = 'rgba(0,0,0,.2)'; X.shadowBlur = 20; X.beginPath(); X.roundRect(190, 640, 700, 640, 30); X.fill(); X.shadowColor = 'transparent';
  X.save(); X.beginPath(); X.arc(540, 820, 130, 0, TAU); X.clip(); if (avatar.width) X.drawImage(avatar, 540 - 150, 820 - 130, 300, 400); X.restore();
  X.restore(); X.save(); X.globalAlpha = k; X.translate(0, (1 - k) * 40);
  strokePts(circPts(540, 820, 132), 1, 5, INK, 91); strokePts(rectPts(190, 640, 700, 640, 30), 1, 4.4, INK, 92);
  write('@ehbehzad', 540, 1020, 80, 1, INK, 'Hand'); write('ترفندهای هوش مصنوعی', 540, 1100, 46, 1, NOTE, 'Vaz');
  marker(() => { X.beginPath(); X.roundRect(370, 1150, 340, 96, 48); }, 1, YEL, -.4, 95, [370, 1150, 710, 1246]); strokePts(rectPts(370, 1150, 340, 96, 46), 1, 4.4, INK, 96); write('+ فالو', 540, 1200, 56, 1, INK, 'Hand');
  X.restore();
}

function render(t) {
  BOIL = Math.floor(t * 12) % 3 * .5;                    // fineliner boil on twos, cycle of 3
  X.setTransform(1, 0, 0, 1, 0, 0); X.fillStyle = PAPER; X.fillRect(0, 0, W, H);
  applyCam(t);
  // page: grain + dot grid in world space
  X.save(); X.fillStyle = X.createPattern(GR, 'repeat'); X.fillRect(-200, -200, PW + 400, PH + 400); X.restore();
  const z = CAM.z, x0 = CAM.x - W / 2 / z, y0 = CAM.y - H / 2 / z, x1 = CAM.x + W / 2 / z, y1 = CAM.y + H / 2 / z;
  X.fillStyle = 'rgba(150,140,125,.55)';
  for (let y = Math.floor(y0 / 26) * 26; y < y1; y += 26) for (let x = Math.floor(x0 / 26) * 26; x < x1; x += 26) X.fillRect(x, y, 2.6, 2.6);
  for (const e of E) { const p = (t - e.at) / e.dur; if (p > 0) e.draw(clamp(p)); }
  subtitle(t); follow(t);
  X.save(); X.setTransform(1, 0, 0, 1, 0, 0); X.font = '800 30px Vaz'; X.direction = 'ltr'; X.textAlign = 'right'; X.fillStyle = 'rgba(30,30,34,.55)'; X.fillText('@ehbehzad', W - 44, 70); X.restore();
}
window.TEXTS = t => { render(t); return SUB ? [SUB] : []; };
window.EV = E.map(e => ({ t: e.at, type: 'pen', dur: e.dur }));
await document.fonts.load('80px Hand'); await document.fonts.load('800 40px Vaz'); await document.fonts.load('64px "Noto Color Emoji"');
window.render = render; window.READY = true;
