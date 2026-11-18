// Paper Craft Explainer (@ehbehzad) — vertical 1080x1920 reels in torn-paper / hanging-card papercraft.
// Engine: Lemo-Opuscar page contract (render(t), READY, DUR, EV, TEXTS) + paper.js cut-paper helpers.
import { clamp, lerp, seg, ss, eo, back, spring, mulberry, hash, vnoise, TAU } from '/core/lib.js';
import { cv, paperFill, finishCut, GRAIN, rr, blob, sh, crescent, INK } from './paper.js';

const W = 1080, H = 1920;
const C = document.getElementById('c'), X = C.getContext('2d');
const SPEC = await (await fetch('spec.json')).json();
const WD = await (await fetch('words.json')).json();
const LEAD = WD.lead, T = i => LEAD + WD.t[Math.min(i, WD.t.length - 1)];
const DUR = LEAD + WD.end + 3.4;
window.DUR = DUR;

// ---------- palette (reference: warm terracotta / orange / cream / tan) ----------
const PAL = { cream: '#f3e3c8', cream2: '#ead2ae', tan: '#d9a877', orange: '#e2763a', terra: '#c4572a', deep: '#8f3a1c',
  card: '#f6ead6', ink: '#3a2a24', sub: 'rgba(52,34,26,.93)', hl: '#ff9a52', gold: '#f2b632' };

// ---------- torn paper ----------
// a sheet whose top edge is a torn line (y0 + noise), filled below; white fibrous rim on the edge
function tornSheet(col, y0, amp, seed, opt = {}) {
  const c = cv(W + 120, H + 200), x = c.getContext('2d'), R = mulberry(seed);
  const pts = [], n = 90, f1 = 1 + R() * 2, f2 = 4 + R() * 4, ph = R() * 9;
  for (let i = 0; i <= n; i++) {
    const px = i / n * (W + 120);
    const py = y0 + amp * (Math.sin(i / n * TAU * f1 + ph) * .6 + Math.sin(i / n * TAU * f2 + ph * 2) * .25) + (R() - .5) * 9;
    pts.push([px, py]);
  }
  const path = () => { x.beginPath(); x.moveTo(0, H + 200); for (const p of pts) x.lineTo(p[0], p[1]); x.lineTo(W + 120, H + 200); x.closePath(); };
  // fibrous white rim (torn edge shows the paper core)
  x.save(); x.translate(0, -7); path(); x.fillStyle = opt.rim || '#fbf3e6'; x.fill(); x.restore();
  for (let i = 0; i < 260; i++) { const k = Math.floor(R() * pts.length), p = pts[k]; x.strokeStyle = 'rgba(251,243,230,.9)'; x.lineWidth = .8 + R(); x.beginPath(); x.moveTo(p[0], p[1] - 3); x.lineTo(p[0] + (R() - .5) * 10, p[1] - 6 - R() * 9); x.stroke(); }
  const body = cv(W + 120, H + 200), y = body.getContext('2d');
  paperFill(y, W + 120, H + 200, col, seed + 3, .08);
  y.globalCompositeOperation = 'destination-in'; y.fillStyle = '#000'; y.beginPath(); y.moveTo(0, H + 200); for (const p of pts) y.lineTo(p[0], p[1]); y.lineTo(W + 120, H + 200); y.closePath(); y.fill();
  x.drawImage(body, 0, 0);
  return c;
}
function drawSheet(sheet, dx, dy, shadow = 22) {
  X.save(); X.shadowColor = 'rgba(70,35,15,.42)'; X.shadowBlur = shadow; X.shadowOffsetY = 6;
  X.drawImage(sheet, -60 + dx, dy); X.restore();
}

// backdrop sets: a list of torn sheets (back to front) per scene "spread"
const SETS = {};
function makeSet(name, base, layers) {
  const bg = cv(W, H), x = bg.getContext('2d'); paperFill(x, W, H, base, name.length * 7, .07);
  SETS[name] = { bg, sheets: layers.map((l, i) => ({ c: tornSheet(l[0], l[1], l[2], 100 + i * 17 + name.length), par: l[3] ?? (.2 + i * .15) })) };
}
makeSet('warm', PAL.cream, [[PAL.tan, 1180, 40], [PAL.orange, 1380, 55], [PAL.terra, 1560, 45]]);
makeSet('cream', '#f1e2c9', [[PAL.cream2, 1300, 30], [PAL.tan, 1500, 40]]);
makeSet('sun', PAL.orange, [[PAL.tan, 1250, 60], ['#d8b48a', 1420, 50], [PAL.cream2, 1580, 40]]);
// top torn strips (hanging from the top edge, like the reference's upper layers)
function topStrip(col, y0, amp, seed) { const f = cv(W + 120, y0 + 80), x = f.getContext('2d'); x.save(); x.translate(0, y0 + 80); x.scale(1, -1); x.drawImage(tornSheet(col, 80, amp, seed), 0, 0); x.restore(); return f; }
const TOPS = { warm: topStrip(PAL.terra, 150, 28, 41), cream: topStrip(PAL.tan, 120, 22, 43), sun: topStrip('#d0642f', 90, 18, 47) };

function backdrop(name, t, t0) {
  const s = SETS[name]; X.drawImage(s.bg, 0, 0);
  const k = eo(seg(t, t0, t0 + .9));
  s.sheets.forEach((sh2, i) => {
    const rise = (1 - eo(seg(t, t0 + i * .12, t0 + .7 + i * .12))) * 500;
    const drift = Math.sin(t * .35 + i) * 6 * sh2.par;
    drawSheet(sh2.c, drift, rise);
  });
  const top = TOPS[name]; X.save(); X.shadowColor = 'rgba(70,35,15,.4)'; X.shadowBlur = 18; X.shadowOffsetY = 6;
  X.drawImage(top, -60 + Math.sin(t * .3) * 5, -(1 - k) * 200 - 20); X.restore();
}

// ---------- hanging card on strings ----------
const CARDS = {};
function cardCanvas(key, w, h, drawFn, col = PAL.card) {
  if (CARDS[key]) return CARDS[key];
  const art = cv(w + 60, h + 60), x = art.getContext('2d');
  x.translate(30, 30); rr(x, 0, 0, w, h, 34); x.save(); x.clip(); paperFill(x, w, h, col, key.length * 3, .05); x.restore();
  rr(x, 0, 0, w, h, 34); x.lineWidth = 3; x.strokeStyle = 'rgba(120,80,50,.25)'; x.stroke();
  drawFn(x, w, h);
  const out = finishCut(art, 10, { paper: '#fbf5ea', edge: '#b48a62' });
  CARDS[key] = out; return out;
}
// card hung from a nail at (nx, ny) by two strings to its top corners; swings in with a spring
function hang(card, cx, top, t, t0, opt = {}) {
  const p = clamp((t - t0) / .9), drop = (1 - spring(t - t0, 6, .32)) * (opt.drop ?? 380);
  if (t < t0) return;
  const sw = Math.sin((t - t0) * 2.6) * Math.exp(-(t - t0) * 1.6) * .06 + Math.sin(t * .9 + cx) * .006;
  const w = card.width, h = card.height, ny = top - (opt.string ?? 110);
  X.save(); X.globalAlpha = clamp(p * 3);
  X.translate(cx, ny); X.rotate(sw);
  // strings + nail
  X.strokeStyle = '#7a5a3e'; X.lineWidth = 3;
  X.beginPath(); X.moveTo(0, 0); X.lineTo(-w * .32, (opt.string ?? 110) + 34 - drop); X.moveTo(0, 0); X.lineTo(w * .32, (opt.string ?? 110) + 34 - drop); X.stroke();
  X.fillStyle = PAL.terra; X.beginPath(); X.arc(0, 0, 13, 0, TAU); X.fill(); X.fillStyle = 'rgba(255,255,255,.45)'; X.beginPath(); X.arc(-4, -4, 4, 0, TAU); X.fill();
  X.shadowColor = 'rgba(60,30,10,.45)'; X.shadowBlur = 26; X.shadowOffsetY = 12;
  X.drawImage(card, -w / 2, (opt.string ?? 110) - drop);
  X.restore();
}
// a card that pops up from below (pop-up book move)
function pop(card, cx, cy, t, t0, rot = 0) {
  if (t < t0) return;
  const k = back(seg(t, t0, t0 + .45), 2.2), w = card.width, h = card.height;
  X.save(); X.translate(cx, cy + h / 2); X.rotate(rot + (1 - k) * .3); X.scale(1, k);
  X.shadowColor = 'rgba(60,30,10,.42)'; X.shadowBlur = 18; X.shadowOffsetY = 8;
  X.drawImage(card, -w / 2, -h); X.restore();
}
// text helpers
function txt(x, s, px, py, size, col, weight = 900, align = 'center', dir = 'rtl') {
  x.font = `${weight} ${size}px Vaz, 'Noto Color Emoji'`; x.fillStyle = col; x.textAlign = align; x.direction = dir; x.textBaseline = 'middle'; x.fillText(s, px, py);
}
function chip(key, label, col = '#fff6e8', fg = PAL.ink, w = 230) {
  return cardCanvas('chip:' + key + label, w, 96, (x, ww, hh) => txt(x, label, ww / 2, hh / 2 + 2, 40, fg, 900), col);
}
function iconCard(key, emoji, label, w = 230, h = 250) {
  return cardCanvas('ic:' + key, w, h, (x, ww, hh) => { txt(x, emoji, ww / 2, hh * .42, 110, '#000', 900); txt(x, label, ww / 2, hh * .82, 34, PAL.ink, 900, 'center', /[a-z]/i.test(label) ? 'ltr' : 'rtl'); });
}

// ---------- robot host as a paper cut-out ----------
let ROBOT = null;
async function loadRobot() {
  const im = new Image(); im.src = 'assets/robot.png'; await im.decode();
  // round paper badge: robot face crop on a cream disc
  const art = cv(320, 320), x = art.getContext('2d');
  x.beginPath(); x.arc(160, 160, 140, 0, TAU); x.fillStyle = '#f2b98a'; x.fill(); x.save(); x.clip();
  x.drawImage(im, 160 - 150, 160 - 120, 300, 400); x.restore();
  x.beginPath(); x.arc(160, 160, 140, 0, TAU); x.lineWidth = 6; x.strokeStyle = '#3a2a24'; x.stroke();
  ROBOT = finishCut(art, 12, { paper: '#fffaf0', edge: '#b48a62' });
}

// ---------- subtitles (reference: dark-brown rounded box, cream text, keywords in orange) ----------
const HL = new Set(SPEC.hl || []);
const toks = WD.toks.map(s => s.replace(/[«»]/g, ''));
const groups = []; { let g = [], n = 0; toks.forEach((w, i) => { g.push(i); n++; if (/[.!؟?؛،:]$/.test(w) || n >= 5) { groups.push(g); g = []; n = 0; } }); if (g.length) groups.push(g); }
function subs(t) {
  let cur = -1; for (let i = 0; i < toks.length; i++) if (t >= T(i)) cur = i;
  if (cur < 0 || t > DUR - 2.8) return null;
  const g = groups.find(g => g.includes(cur));
  const words = g.map(i => toks[i]);
  X.save(); X.font = '800 50px Vaz'; X.direction = 'rtl';
  const space = 16, ws = words.map(w => X.measureText(w).width), tw = ws.reduce((a, b) => a + b, 0) + space * (words.length - 1);
  const bw = Math.max(520, Math.min(980, tw + 90)), bh = 128, bx = (W - bw) / 2, by = 1600;
  X.shadowColor = 'rgba(0,0,0,.35)'; X.shadowBlur = 20; X.shadowOffsetY = 6;
  rr(X, bx, by, bw, bh, 30); X.fillStyle = PAL.sub; X.fill(); X.shadowColor = 'transparent';
  let px = W / 2 + tw / 2; X.textBaseline = 'middle'; X.textAlign = 'right';
  g.forEach((i, k) => {
    const said = t >= T(i), key = HL.has(toks[i].replace(/[.!؟?؛،:]/g, ''));
    X.fillStyle = key ? PAL.hl : (said ? '#fff6ea' : 'rgba(255,246,234,.45)');
    X.fillText(words[k], px, by + bh / 2 + 3); px -= ws[k] + space;
  });
  X.restore();
  return { id: 'sub' + groups.indexOf(g), text: words.join(' '), x0: bx, y0: by, x1: bx + bw, y1: by + bh, pass: true };
}

// ---------- torn-paper wipe between scenes ----------
const WIPE = tornSheet(PAL.terra, 60, 40, 999);
function wipe(t, at) {
  const k = seg(t, at - .35, at + .35); if (k <= 0 || k >= 1) return;
  const y = lerp(H + 60, -H - 300, ss(k));
  X.save(); X.shadowColor = 'rgba(60,30,10,.5)'; X.shadowBlur = 30; X.drawImage(WIPE, -60, y); X.restore();
}

// ---------- scenes ----------
const S = SPEC.scenes.map(s => ({ ...s, t0: s.w === 0 ? 0 : T(s.w) - .05 }));
S.forEach((s, i) => s.t1 = i + 1 < S.length ? S[i + 1].t0 : DUR);
const DRAW = await import('./scenes.js');

function render(t) {
  X.setTransform(1, 0, 0, 1, 0, 0); X.clearRect(0, 0, W, H);
  const i = Math.max(0, S.findLastIndex(s => t >= s.t0)), s = S[i];
  const API = { X, W, H, PAL, T, t0: s.t0, t1: s.t1, hang, pop, cardCanvas, txt, chip, iconCard, backdrop, ROBOT, spring, back, eo, ss, seg, clamp, lerp, TAU, finishCut, cv, paperFill, blob, sh, crescent, rr, mulberry };
  DRAW[s.type](t, s, API);
  // robot host: small paper cut-out bottom-left, bobs while the voice talks
  if (ROBOT && t < DUR - 2.8 && s.type !== 'cta') {
    const talk = WD.t.some((w, k) => Math.abs(t - T(k) - .1) < .12) ? 1 : 0;
    X.save(); X.translate(30, 1330 + Math.sin(t * 2.2) * 6 - talk * 6); X.rotate(Math.sin(t * 1.3) * .03);
    X.shadowColor = 'rgba(60,30,10,.4)'; X.shadowBlur = 16; X.shadowOffsetY = 8; X.drawImage(ROBOT, 0, 0, 230, 230); X.restore();
  }
  const sb = subs(t);
  S.forEach((s2, k) => k > 0 && wipe(t, s2.t0));
  // handle tag
  X.save(); X.font = '800 30px Vaz'; X.direction = 'ltr'; X.textAlign = 'right'; X.fillStyle = 'rgba(58,42,36,.75)'; X.fillText('@ehbehzad', W - 44, 70); X.restore();
  window.__subs = sb;
}
window.TEXTS = t => { render(t); return window.__subs ? [window.__subs] : []; };
window.EV = S.map(s => ({ t: s.t0, type: 'swish' }));
await document.fonts.load('900 40px Vaz'); await document.fonts.load('800 40px Vaz'); await document.fonts.load('700 40px Vaz');
await loadRobot();
window.render = render; window.READY = true;
