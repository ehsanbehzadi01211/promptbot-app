// Swiss Motion Graphics (Lemo-Opuscar style), vertical 1080x1920, Persian (RTL: flush RIGHT is our "flush left").
// Grid: 6 columns, 72 px margins, 24 px gutters, 24 px baseline. Paper, ink, greys and ONE signal colour.
// Two curves only (precise ease + linear), entrances are clip-reveals/wipes, deletions knife cuts, no bounce.
import { clamp, lerp, seg } from '/core/lib.js';

const W = 1080, H = 1920, M = 72, G = 24, COLS = 6, CW = (W - 2 * M - (COLS - 1) * G) / COLS;
const C = document.getElementById('c'), X = C.getContext('2d');
const WD = await (await fetch('words.json')).json();
const T = i => WD.lead + WD.t[Math.min(i, WD.t.length - 1)];
const DUR = WD.lead + WD.end + 3.3; window.DUR = DUR;
const PAGE = '#f2f0ea', INK = '#141414', G1 = '#d9d6ce', G2 = '#bdb9af', G3 = '#8a867d', SIG = '#ff5a00';
// precise ease cubic-bezier(.7,0,.2,1)
function bez(t) { t = clamp(t); if (t <= 0) return 0; if (t >= 1) return 1; let lo = 0, hi = 1, u = t; for (let i = 0; i < 18; i++) { u = (lo + hi) / 2; const x = 3 * (1 - u) ** 2 * u * .7 + 3 * (1 - u) * u * u * .2 + u ** 3; if (x < t) lo = u; else hi = u; }
  return 3 * (1 - u) * u * u + u ** 3; }
const colR = c => W - M - c * (CW + G);            // right edge of column c (0 = rightmost)
const colL = c => colR(c) - CW;
const span = (c0, n) => [colL(c0 + n - 1), colR(c0)]; // x range covering n columns starting at column c0 from the right
const FONT = w => `${w} ${'px'} Vaz`;

// ---------- type primitives ----------
function setF(size, wt = 900) { X.font = `${wt} ${size}px Vaz`; }
// clip-reveal from below the baseline (enter) and up (leave); text is flush right at xr
function rise(s, xr, base, size, t, tIn, tOut = 1e9, col = INK, wt = 900, dir = 'rtl', align = 'right') {
  const kin = bez(seg(t, tIn, tIn + .32)), kout = bez(seg(t, tOut, tOut + .28)); if (kin <= 0 || kout >= 1) return;
  setF(size, wt); X.direction = dir; X.textAlign = align; X.textBaseline = 'alphabetic';
  const w = X.measureText(s).width, x0 = align === 'right' ? xr - w : align === 'left' ? xr : xr - w / 2;
  X.save(); X.beginPath(); X.rect(x0 - 20, base - size * 1.05, w + 40, size * 1.35); X.clip();
  X.fillStyle = col; X.fillText(s, xr, base + (1 - kin) * size * 1.2 - kout * size * 1.3); X.restore();
  return w;
}
function block(x0, y0, x1, y1, t, tIn, col = SIG, from = 'right', tOut = 1e9) {     // wipe a flat block in
  const k = bez(seg(t, tIn, tIn + .3)), ko = bez(seg(t, tOut, tOut + .25)); if (k <= 0 || ko >= 1) return;
  X.fillStyle = col; const w = (x1 - x0) * k;
  if (ko > 0) { const h = (y1 - y0) * (1 - ko), m = (y0 + y1) / 2; X.fillRect(x0, m - h / 2, x1 - x0, h); return; }   // knife-cut collapse to the midline
  if (from === 'right') X.fillRect(x1 - w, y0, w, y1 - y0); else X.fillRect(x0, y0, w, y1 - y0);
}
function rule(x0, x1, y, t, tIn, col = INK, lw = 2) { const k = seg(t, tIn, tIn + .4); if (k <= 0) return; X.fillStyle = col; X.fillRect(x1 - (x1 - x0) * k, y, (x1 - x0) * k, lw); }
function note(s, xr, y, t, tIn, col = G3, size = 26) { rise(s, xr, y, size, t, tIn, 1e9, col, 700); }
// giant numeral climbing in eased steps (one module at a time)
function numeral(s, xr, base, size, t, tIn, col = INK, steps = 4) {
  const k = seg(t, tIn, tIn + .6); if (k <= 0) return; const q = Math.min(1, Math.ceil(k * steps) / steps), e = bez(q);
  setF(size, 900); X.direction = 'ltr'; X.textAlign = 'right'; X.textBaseline = 'alphabetic';
  const w = X.measureText(s).width; X.save(); X.beginPath(); X.rect(xr - w - 30, base - size * .78, w + 60, size * .8); X.clip();
  X.fillStyle = col; X.fillText(s, xr, base + (1 - e) * size * .8); X.restore();
}

// ---------- the film, scene by scene ----------
const SC = [];   // [startWord, fn(t, t0, t1)]
const at = i => T(i) - .04;

// 1 hook (w0-8): statement rows, then the signal block "رایگان"
SC.push([0, (t, t0, t1) => {
  const xr = colR(0); let y = 520;
  rise('یه تیم کامل', xr, y, 128, t, at(0), t1 - .3); y += 160;
  rise('برای کانال', xr, y, 128, t, at(3), t1 - .3); y += 160;
  rise('یوتیوبت', xr, y, 128, t, at(5), t1 - .3);
  block(colL(3), 900, colR(0), 1070, t, at(6), SIG, 'right', t1 - .3);
  rise('رایگان', colR(0) - 30, 1035, 120, t, at(6) + .12, t1 - .3, INK);
  rise('توی Claude', colR(0), 1210, 64, t, at(7), t1 - .3, G3, 800);
  note('01 / hook', colL(5) + 140, 1290, t, at(0) + .3, G3); rule(M, W - M, 1310, t, at(0));
}]);
// 2 the package (w9-25): title, giant 11, spec rows with rules
SC.push([9, (t, t0, t1) => {
  rise('YouTube Agent Skills', colR(0), 380, 70, t, at(9), t1 - .3, INK, 900, 'ltr', 'right');
  rule(M, W - M, 410, t, at(9) + .2);
  numeral('11', colR(0) + 10, 900, 520, t, at(13), SIG);
  rise('مهارت آماده', colL(4) + CW, 880, 64, t, at(14), t1 - .3, INK, 900, 'rtl', 'right');
  const rows = [[17, 'لایسنس', 'MIT'], [20, 'ثبت‌نام', 'نداره'], [23, 'کلید API', 'نداره']];
  rows.forEach(([wi, a, b], i) => { const y = 1060 + i * 96; rule(M, W - M, y - 62, t, at(wi), G2, 1); rise(a, colR(0), y, 44, t, at(wi), t1 - .3, G3, 700); rise(b, colL(5) + 160, y, 44, t, at(wi) + .08, t1 - .3, INK, 900, /[A-Za-z]/.test(b) ? 'ltr' : 'rtl', 'right'); });
  note('02 / package — 6 col · 24 px', colL(5) + 300, 1400, t, at(9) + .4);
}]);
// 3-7 the five skills: each a page with giant numeral, label, technical note; the camera pans by one page between them
const SK = [[26, '01', 'اسکریپت', '۲۱ فرمول هوک', '۵ پیشنهاد + امتیاز', 33], [43, '02', 'عنوان + تامبنیل', 'چک با هم', 'تکرار · کوتاهی · مبهم', 46],
  [52, '03', 'ادیت', 'سکوت‌ها و تکرارها', 'از روی متن ویدیو', 57], [63, '04', 'ریتنشن', 'دقیقاً کجا رفتن', 'خواندن نمودار', 70], [74, '05', 'شورت', 'شورت‌های قایم‌شده', 'از ویدیوی بلند', 78]];
SK.forEach(([wi, n, a, b, c, w2], k) => SC.push([wi, (t, t0, t1) => {
  numeral(n, colR(0) + 10, 760, 420, t, at(wi), k % 2 ? INK : SIG, 3);
  rise(a, colR(0), 960, 104, t, at(wi + 1), t1 - .3);
  rule(M, W - M, 1010, t, at(wi + 1) + .1);
  rise(b, colR(0), 1110, 58, t, at(w2), t1 - .3, INK, 800);
  rise(c, colR(0), 1190, 40, t, at(w2) + .25, t1 - .3, G3, 700);
  // a bar counter: k+1 of 5 modules filled (the system's progress)
  for (let i = 0; i < 5; i++) { const x1 = colR(0) - i * 64; block(x1 - 52, 1290, x1, 1306, t, at(wi) + .1 + i * .05, i <= k ? INK : G1, 'right', t1 - .3); }
  note(`${n} / 05 skills`, colL(5) + 160, 1360, t, at(wi) + .3);
}]));
// 8 the exception (w83-92): "it doesn't upload" — the signal block leaves the grid, linear and tilted
SC.push([83, (t, t0, t1) => {
  rise('فقط یادت باشه', colR(0), 560, 72, t, at(83), t1 - .3, G3, 800);
  const k = seg(t, at(86), at(88) + .6);   // linear, unsnapped
  X.save(); X.translate(lerp(colR(0) - 380, 560, k), lerp(820, 860, k)); X.rotate(lerp(0, -.07, k));
  block(-400, -110, 400, 110, t, at(86), SIG, 'right', t1 - .3); X.restore();
  X.save(); X.translate(lerp(colR(0) - 380, 560, k), lerp(820, 860, k)); X.rotate(lerp(0, -.07, k));
  rise('خودش آپلود نمی‌کنه', 0, 30, 76, t, at(87), t1 - .3, INK, 900, 'rtl', 'center'); X.restore();
  rise('آپلود با خودته.', colR(0), 1120, 96, t, at(89), t1 - .3);
  note(k < 1 ? 'off grid' : 'off grid ✕', colL(5) + 110, 1220, t, at(86), SIG);
}]);
// 9 CTA (w93-end): the keyword in the signal colour, then the follow block
SC.push([93, (t, t0, t1) => {
  rise('کامنت کن', colR(0), 520, 84, t, at(96), t1, G3, 800);
  block(M, 600, W - M, 900, t, at(94), SIG);
  rise('یوتیوب', W / 2, 840, 230, t, at(94) + .12, 1e9, INK, 900, 'rtl', 'center');
  rise('لینک + روش نصب توی دایرکت', colR(0), 1010, 52, t, at(99), t1, INK, 800);
  const f = DUR - 2.6;
  block(M, 1150, W - M, 1450, t, f, INK); rise('@ehbehzad', W / 2, 1290, 104, t, f + .1, 1e9, PAGE, 900, 'ltr', 'center');
  rise('ترفندهای هوش مصنوعی — فالو کن', W / 2, 1390, 44, t, f + .2, 1e9, G2, 800, 'rtl', 'center');
}]);
SC.forEach((s, i) => { s.t0 = i ? at(s[0]) : 0; s.t1 = i + 1 < SC.length ? at(SC[i + 1][0]) : DUR; });

// ---------- subtitles inside the layout: bottom rows, grey lead-in + bold line, words clip-revealed ----------
const toks = WD.toks.map(s => s.replace(/[«»]/g, ''));
const groups = []; { let g = [], n = 0; toks.forEach((w, i) => { g.push(i); n++; if (/[.!؟?؛،:]$/.test(w) || n >= 5) { groups.push(g); g = []; n = 0; } }); if (g.length) groups.push(g); }
let SUB = null;
function subtitle(t) {
  SUB = null; let cur = -1; for (let i = 0; i < toks.length; i++) if (t >= T(i)) cur = i;
  if (cur < 0 || t > DUR - 2.9) return; const g = groups.find(g => g.includes(cur)), gi = groups.indexOf(g);
  X.fillStyle = INK; X.fillRect(M, 1612, W - 2 * M, 2);
  setF(24, 700); X.fillStyle = G3; X.direction = 'ltr'; X.textAlign = 'left'; X.fillText(String(gi + 1).padStart(2, '0') + ' —', M, 1650);
  setF(50, 800); X.direction = 'rtl'; X.textAlign = 'right'; let xr = colR(0);
  g.forEach(i => { const w = toks[i]; const tw = X.measureText(w).width;
    const k = bez(seg(t, T(i) - .05, T(i) + .2)); X.save(); X.beginPath(); X.rect(xr - tw - 4, 1660, tw + 8, 74); X.clip();
    X.fillStyle = INK; X.fillText(w, xr, 1716 + (1 - k) * 60); X.restore(); setF(50, 800); xr -= tw + 16; });
  SUB = { id: 'sub' + gi, text: g.map(i => toks[i]).join(' '), x0: M, y0: 1612, x1: W - M, y1: 1740, pass: true };
}

function render(t) {
  X.setTransform(1, 0, 0, 1, 0, 0); X.fillStyle = PAGE; X.fillRect(0, 0, W, H);
  // the grid, faint (stronger while a page is being built)
  const s = SC[Math.max(0, SC.findLastIndex(s => t >= s.t0))];
  const build = 1 - seg(t, s.t0, s.t0 + .8);
  X.fillStyle = `rgba(20,20,20,${.05 + .07 * build})`;
  for (let c = 0; c < COLS; c++) { X.fillRect(colL(c), 0, 1, H); X.fillRect(colR(c) - 1, 0, 1, H); }
  for (let y = 0; y < H; y += 24 * 8) X.fillRect(0, y, W, 1);
  // hard pan by one page between scenes (precise ease, lands on the next word)
  const pan = 1 - bez(seg(t, s.t0 - .02, s.t0 + .32));
  X.save(); X.translate(0, pan * 160 * (s === SC[0] ? 0 : 1));
  s[1](t, s.t0, s.t1); X.restore();
  subtitle(t);
  setF(26, 800); X.fillStyle = G3; X.direction = 'ltr'; X.textAlign = 'left'; X.fillText('@ehbehzad', M, 92);
  X.textAlign = 'right'; X.fillText('YT · AGENT · SKILLS', W - M, 92); X.fillStyle = INK; X.fillRect(M, 112, W - 2 * M, 2);
}
window.TEXTS = t => { render(t); return SUB ? [SUB] : []; };
window.EV = SC.map(s => ({ t: s.t0, type: 'snap' }));
for (const w of [700, 800, 900]) await document.fonts.load(`${w} 60px Vaz`);
window.render = render; window.READY = true;
