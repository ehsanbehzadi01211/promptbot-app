// Scene types for Paper Craft Explainer. Each: (t, scene, API) draws one full frame (backdrop + paper pieces).

// hook: big hanging title card + pop-up icon cards + chips
export function hero(t, s, A) {
  const { X, W, T, hang, pop, cardCanvas, txt, chip, iconCard, backdrop, PAL } = A;
  backdrop(s.set || 'warm', t, s.t0);
  const card = cardCanvas('hero:' + s.title, 860, 470, (x, w, h) => {
    if (s.kicker) txt(x, s.kicker, w / 2, 80, 44, PAL.terra, 900, 'center', 'ltr');
    txt(x, s.title, w / 2, 210, 120, PAL.ink, 900, 'center', /^[A-Za-z]/.test(s.title) ? 'ltr' : 'rtl');
    if (s.sub) txt(x, s.sub, w / 2, 360, 76, PAL.terra, 900);
  });
  hang(card, W / 2, 270, t, s.t0 + .1);
  (s.icons || []).forEach((ic, i) => pop(iconCard(ic[1] + ic[2], ic[1], ic[2]), 200 + i * 340, 960, t, T(ic[0]), (i - 1) * .05));
  (s.chips || []).forEach((c, i) => pop(chip('h', c[1], '#fff6e8', PAL.ink, 300), 220 + (i % 3) * 320, 1300 + Math.floor(i / 3) * 120, t, T(c[0]), (i % 2 ? -.04 : .04)));
}

// one tool: a big hanging repo card with stats and a command strip, chips below
export function tool(t, s, A) {
  const { X, W, T, hang, pop, cardCanvas, txt, chip, backdrop, PAL, rr } = A;
  backdrop(s.set || 'cream', t, s.t0);
  const card = cardCanvas('tool:' + s.name, 880, 640, (x, w, h) => {
    txt(x, s.icon || '🛠️', w / 2, 140, 150, '#000');
    txt(x, s.name, w / 2, 300, 104, PAL.ink, 900, 'center', 'ltr');
    if (s.line) txt(x, s.line, w / 2, 410, 50, PAL.terra, 900);
    if (s.cmd) { rr(x, 60, 480, w - 120, 100, 22); x.fillStyle = '#2f2420'; x.fill(); txt(x, s.cmd, w / 2, 532, 44, '#f6ead6', 700, 'center', 'ltr'); }
  });
  hang(card, W / 2, 250, t, s.t0 + .1);
  (s.chips || []).forEach((c, i) => pop(chip('t', c[1], i === 0 ? '#ffe2c4' : '#fff6e8', PAL.ink, 280), 190 + i * 350, 1080, t, T(c[0]), (i - 1) * .05));
}

// a flow: hub card, strings down to child cards (the reference's "tree on strings")
export function flow(t, s, A) {
  const { X, W, T, hang, pop, cardCanvas, iconCard, backdrop, PAL, seg, eo } = A;
  backdrop(s.set || 'cream', t, s.t0);
  const hub = iconCard('hub' + s.hub[2], s.hub[1], s.hub[2], 330, 330);
  hang(hub, W / 2, 230, t, T(s.hub[0]));
  const kids = s.kids, n = kids.length, y = 900;
  kids.forEach((k, i) => {
    const cx = W / 2 + (i - (n - 1) / 2) * 270, ta = T(k[0]);
    const p = eo(seg(t, ta - .2, ta + .25));
    if (p > 0) { X.save(); X.strokeStyle = '#7a5a3e'; X.lineWidth = 4; X.beginPath(); X.moveTo(W / 2, 640); X.lineTo(lerpN(W / 2, cx, p), lerpN(640, y, p)); X.stroke(); X.fillStyle = PAL.terra; X.beginPath(); X.arc(cx, y, 10 * p, 0, 7); X.fill(); X.restore(); }
    pop(iconCard('kid' + k[2], k[1], k[2], 240, 270), cx, y + 20, t, ta);
  });
  if (s.foot) pop(cardCanvas('foot' + s.foot[1], 760, 120, (x, w, h) => A.txt(x, s.foot[1], w / 2, h / 2 + 3, 50, PAL.ink, 900)), W / 2, 1290, t, T(s.foot[0]));
}
const lerpN = (a, b, t) => a + (b - a) * t;

// numbered steps: note cards pinned one under another
export function steps(t, s, A) {
  const { X, W, T, cardCanvas, txt, backdrop, PAL, back, seg, rr } = A;
  backdrop(s.set || 'warm', t, s.t0);
  if (s.title) { const tc = cardCanvas('st:' + s.title, 620, 130, (x, w, h) => txt(x, s.title, w / 2, h / 2 + 3, 62, PAL.ink, 900)); pin(A, tc, W / 2, 210, t, s.t0 + .1, 0); }
  s.items.forEach((it, i) => {
    const c = cardCanvas('step' + i + it[2], 900, 250, (x, w, h) => {
      x.fillStyle = PAL.orange; x.beginPath(); x.arc(w - 110, h / 2, 70, 0, 7); x.fill();
      txt(x, it[1], w - 110, h / 2 + 4, 76, '#fff', 900);
      txt(x, it[2], w - 210, h / 2 - (it[3] ? 34 : 0), 50, PAL.ink, 900, 'right');
      if (it[3]) txt(x, it[3], w - 210, h / 2 + 48, 38, PAL.terra, 700, 'right', /^[$A-Za-z]/.test(it[3]) ? 'ltr' : 'rtl');
    });
    pin(A, c, W / 2, 380 + i * 300, t, T(it[0]), (i % 2 ? .025 : -.02));
  });
}
function pin(A, card, cx, cy, t, t0, rot) {
  const { X, PAL, back, seg, TAU } = A; if (t < t0) return;
  const k = back(seg(t, t0, t0 + .4), 2.4), w = card.width, h = card.height;
  X.save(); X.translate(cx, cy + h / 2); X.rotate(rot); X.scale(k, k);
  X.shadowColor = 'rgba(60,30,10,.42)'; X.shadowBlur = 20; X.shadowOffsetY = 10; X.drawImage(card, -w / 2, -h / 2);
  X.shadowColor = 'transparent'; X.fillStyle = PAL.terra; X.beginPath(); X.arc(0, -h / 2 + 26, 14, 0, TAU); X.fill(); X.restore();
}

// a terminal card + a paper phone that lights up
export function run(t, s, A) {
  const { X, W, T, hang, pop, cardCanvas, txt, backdrop, PAL, rr, seg, eo } = A;
  backdrop(s.set || 'cream', t, s.t0);
  const term = cardCanvas('term' + s.cmd, 880, 300, (x, w, h) => { rr(x, 40, 40, w - 80, h - 80, 26); x.fillStyle = '#2f2420'; x.fill(); txt(x, s.cmd, w - 90, 120, 58, '#f6ead6', 700, 'right', 'ltr'); });
  hang(term, W / 2, 230, t, s.t0 + .1);
  const ok = seg(t, T(s.ok), T(s.ok) + .4);
  const phone = cardCanvas('phone' + s.app, 400, 700, (x, w, h) => {
    rr(x, 30, 30, w - 60, h - 60, 60); x.fillStyle = '#2f2420'; x.fill(); rr(x, 55, 75, w - 110, h - 150, 30); x.fillStyle = '#fbe9d2'; x.fill();
  });
  pop(phone, W / 2, 820, t, T(s.phone));
  if (ok > 0) { const k = A.back(ok, 2.6); X.save(); X.translate(W / 2, 1110); X.scale(k, k); rr(X, -110, -110, 220, 220, 50); X.fillStyle = PAL.orange; X.fill(); txt(X, s.app, 0, 6, 120, '#000'); X.restore();
    X.save(); X.globalAlpha = ok; txt(X, s.done, W / 2, 1300, 52, PAL.ink, 900); X.restore(); }
}

// call to action: sun rays, paper star, speech bubble with the keyword, then the follow card
export function cta(t, s, A) {
  const { X, W, H, T, backdrop, PAL, cardCanvas, txt, back, seg, eo, TAU, ROBOT, rr, crescent } = A;
  backdrop('sun', t, s.t0);
  X.save(); X.translate(W / 2, 900); X.rotate(t * .05); const rk = eo(seg(t, s.t0, s.t0 + .8));
  for (let i = 0; i < 18; i++) { X.rotate(TAU / 18); X.fillStyle = i % 2 ? 'rgba(255,214,150,.55)' : 'rgba(255,240,210,.35)'; X.beginPath(); X.moveTo(0, 0); X.lineTo(-60 * rk, -1100 * rk); X.lineTo(60 * rk, -1100 * rk); X.closePath(); X.fill(); }
  X.restore();
  // paper star
  const sk = back(seg(t, s.t0 + .2, s.t0 + .8), 2.2);
  if (sk > 0) { X.save(); X.translate(W / 2, 980); X.scale(sk, sk); X.rotate(Math.sin(t * 1.4) * .04);
    const star = () => { X.beginPath(); for (let i = 0; i < 10; i++) { const r = i % 2 ? 150 : 330, a = -Math.PI / 2 + i * Math.PI / 5; X.lineTo(Math.cos(a) * r, Math.sin(a) * r); } X.closePath(); };
    X.shadowColor = 'rgba(80,35,10,.5)'; X.shadowBlur = 30; X.shadowOffsetY = 14; star(); X.fillStyle = PAL.gold; X.fill(); X.shadowColor = 'transparent';
    crescent(X, star, '#d99a1e', 26, 22, PAL.gold); X.lineWidth = 6; X.strokeStyle = '#fbf3e6'; star(); X.stroke(); X.restore(); }
  // speech bubble with the keyword
  const bk = back(seg(t, T(s.w + 1), T(s.w + 1) + .45), 2.4);
  if (bk > 0) { const b = cardCanvas('bubble' + s.keyword, 560, 300, (x, w, h) => txt(x, s.keyword, w / 2, h / 2 + 6, 150, PAL.ink, 900), '#fbf3e6');
    X.save(); X.translate(W - 330, 470); X.scale(bk, bk); X.rotate(.05); X.shadowColor = 'rgba(60,30,10,.45)'; X.shadowBlur = 24; X.shadowOffsetY = 10;
    X.drawImage(b, -b.width / 2, -b.height / 2); X.fillStyle = '#fbf3e6'; X.beginPath(); X.moveTo(-120, 120); X.lineTo(-220, 230); X.lineTo(-30, 135); X.fill(); X.restore(); }
  // follow card (last 2.6 s)
  const fk = eo(seg(t, A.t1 - 2.6, A.t1 - 2.1));
  if (fk > 0) { X.save(); X.fillStyle = `rgba(60,30,15,${.55 * fk})`; X.fillRect(0, 0, W, H);
    const f = cardCanvas('follow', 760, 760, (x, w, h) => { if (ROBOT) x.drawImage(ROBOT, w / 2 - 170, 50, 340, 340); txt(x, '@ehbehzad', w / 2, 500, 74, PAL.ink, 900, 'center', 'ltr'); txt(x, 'ترفندهای هوش مصنوعی', w / 2, 585, 42, PAL.terra, 800);
      rr(x, w / 2 - 190, 630, 380, 100, 50); x.fillStyle = PAL.orange; x.fill(); txt(x, '+ فالو', w / 2, 682, 52, '#fff', 900); });
    X.translate(W / 2, 900 + (1 - fk) * 120); X.drawImage(f, -f.width / 2, -f.height / 2); X.restore(); }
}
