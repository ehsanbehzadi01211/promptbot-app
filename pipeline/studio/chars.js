// Studio AI — original voxel ("blocky") characters. Pixel-art textures on boxes, no third-party characters or logos.
import * as THREE from 'three';

const NEAREST = t => { t.magFilter = THREE.NearestFilter; t.minFilter = THREE.NearestFilter; t.colorSpace = THREE.SRGBColorSpace; return t; };
// pixel texture from a painter fn on an N×N grid
export function pix(n, paint) { const c = document.createElement('canvas'); c.width = c.height = n; const x = c.getContext('2d'); paint(x, n); return NEAREST(new THREE.CanvasTexture(c)); }
const noise = (x, n, base, amt = 18, seed = 1) => { let s = seed; const r = () => (s = (s * 16807) % 2147483647) / 2147483647; x.fillStyle = base; x.fillRect(0, 0, n, n);
  for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) { const v = (r() - .5) * amt; x.fillStyle = `rgba(${v > 0 ? '255,255,255' : '0,0,0'},${Math.abs(v) / 100})`; x.fillRect(i, j, 1, 1); } };
export const solid = (col, seed = 3, amt = 16) => pix(16, (x, n) => noise(x, n, col, amt, seed));

// face states: mouth 0 closed, 1 half, 2 open; blink
export function faceTex(spec, mouth = 0, blink = false) {
  return pix(16, (x, n) => {
    noise(x, n, spec.skin, 12, 7);
    if (spec.facePaint) spec.facePaint(x, n);
    const ey = spec.eyeY ?? 7;
    if (blink) { x.fillStyle = spec.eye || '#1a1a1a'; x.fillRect(3, ey + 1, 3, 1); x.fillRect(10, ey + 1, 3, 1); }
    else { x.fillStyle = '#ffffff'; x.fillRect(3, ey, 3, 2); x.fillRect(10, ey, 3, 2); x.fillStyle = spec.eye || '#1a1a1a'; x.fillRect(4, ey, 2, 2); x.fillRect(10, ey, 2, 2); }
    if (spec.brow) { x.fillStyle = spec.brow; x.fillRect(3, ey - 2, 3, 1); x.fillRect(10, ey - 2, 3, 1); }
    const my = spec.mouthY ?? 11; x.fillStyle = spec.mouth || '#5a2a1a';
    if (mouth === 0) x.fillRect(6, my, 4, 1);
    else if (mouth === 1) { x.fillRect(6, my, 4, 2); x.fillStyle = '#2a0a0a'; x.fillRect(7, my, 2, 1); }
    else { x.fillRect(5, my - 1, 6, 3); x.fillStyle = '#2a0a0a'; x.fillRect(6, my, 4, 2); x.fillStyle = '#e05a6a'; x.fillRect(7, my + 1, 2, 1); }
  });
}

const mat = t => new THREE.MeshStandardMaterial({ map: t, roughness: .85, metalness: 0 });
function box(w, h, d, mats) { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), Array.isArray(mats) ? mats : mat(mats)); m.castShadow = true; m.receiveShadow = true; return m; }
// box with a special front face (+z is index 4)
function boxFront(w, h, d, side, front) { const s = mat(side); return box(w, h, d, [s, s, s, s, mat(front), s]); }

// Character: units in "pixels" /16 like the classic blocky proportions (head 8, body 12, arms/legs 4 wide)
export function makeChar(spec) {
  const g = new THREE.Group(); const U = 1 / 16;
  const skin = solid(spec.skin, 5), shirt = spec.shirtTex || solid(spec.shirt, 9), pants = solid(spec.pants, 11), shoe = solid(spec.shoe || '#2a2a2a', 13);
  const faces = [0, 1, 2].map(m => faceTex(spec, m)), blink = faceTex(spec, 0, true);
  // legs
  const legL = new THREE.Group(), legR = new THREE.Group();
  [legL, legR].forEach((L, i) => { const p = box(4 * U, 10 * U, 4 * U, pants); p.position.y = -5 * U; const s = box(4.2 * U, 2 * U, 4.6 * U, shoe); s.position.set(0, -11 * U, .2 * U); L.add(p, s); L.position.set((i ? 2 : -2) * U, 12 * U, 0); g.add(L); });
  // body
  const body = boxFront(8 * U, 12 * U, 4 * U, shirt, spec.chestTex || shirt); body.position.y = 18 * U; g.add(body);
  // arms (pivot at shoulder)
  const arms = [0, 1].map(i => { const A = new THREE.Group(); const sl = box(4 * U, 6 * U, 4 * U, spec.sleeve ? solid(spec.sleeve, 21) : shirt); sl.position.y = -3 * U; const hd = box(4 * U, 6 * U, 4 * U, skin); hd.position.y = -9 * U; A.add(sl, hd); A.position.set((i ? 6 : -6) * U, 23.5 * U, 0); g.add(A); return A; });
  // head
  const head = new THREE.Group(); const sideHead = spec.headSide ? spec.headSide : solid(spec.hair || spec.skin, 17);
  const topHead = spec.headTop || solid(spec.hair || spec.skin, 19);
  const hm = [mat(sideHead), mat(sideHead), mat(topHead), mat(skin), mat(faces[0]), mat(spec.headBack || sideHead)];
  const hb = box(8 * U, 8 * U, 8 * U, hm); hb.position.y = 4 * U; head.add(hb); head.position.y = 24 * U; g.add(head);
  if (spec.hairFringe) { const f = box(8.4 * U, 2 * U, 8.4 * U, solid(spec.hair, 23)); f.position.y = 7.4 * U; head.add(f); }
  // accessories
  (spec.extras || []).forEach(fn => fn({ g, head, body, arms, legs: [legL, legR], U, box, solid, pix, mat, THREE }));
  g.userData = { head, body, arms, legs: [legL, legR], faceMat: hm[4], faces, blink, spec };
  return g;
}

// animate: talk (0..1 loudness), t seconds, gesture
export function pose(ch, t, talk = 0, opt = {}) {
  const u = ch.userData, ph = (opt.phase || 0);
  u.head.rotation.y = Math.sin(t * .7 + ph) * .12 + (opt.look || 0); u.head.rotation.x = Math.sin(t * 1.3 + ph) * .04 - talk * .05; u.head.rotation.z = Math.sin(t * .9 + ph) * .03;
  u.body.rotation.y = Math.sin(t * .5 + ph) * .05;
  const wave = opt.wave ? Math.sin(t * 9) * .35 - 2.6 : 0;
  u.arms[0].rotation.x = opt.wave ? 0 : Math.sin(t * 1.1 + ph) * .06 - talk * .25 * Math.sin(t * 6); u.arms[0].rotation.z = opt.wave ? -wave : -.06;
  u.arms[1].rotation.x = Math.sin(t * 1.2 + ph + 1) * .06 + (opt.hold ? -1.1 : 0); u.arms[1].rotation.z = .06;
  const walk = opt.walk || 0; u.legs[0].rotation.x = Math.sin(t * 8) * .6 * walk; u.legs[1].rotation.x = -Math.sin(t * 8) * .6 * walk; if (walk) { u.arms[0].rotation.x = -Math.sin(t * 8) * .5 * walk; }
  const m = talk > .55 ? 2 : talk > .18 ? 1 : 0, bl = ((t + ph * 3) % 3.7) < .12;
  u.faceMat.map = bl && m === 0 ? u.blink : u.faces[m]; u.faceMat.needsUpdate = true;
  ch.position.y = (opt.y || 0) + Math.abs(Math.sin(t * 8)) * .03 * walk;
}

// ---------- the cast ----------
const chest = (bg, paint) => pix(16, (x, n) => { noise(x, n, bg, 14, 31); paint(x, n); });
export const CAST = {
  claude: { name: 'کلاد', role: 'مجری', skin: '#e8a27c', hair: '#c4572f', hairFringe: true, eye: '#2b1a12', brow: '#8a3418', shirt: '#24324a', sleeve: '#24324a', pants: '#1b2333', shoe: '#3a2a20',
    chestTex: chest('#24324a', (x) => { x.fillStyle = '#f3ead8'; x.fillRect(5, 0, 6, 9); x.fillStyle = '#d9643a'; x.fillRect(6, 1, 4, 2); x.fillRect(7, 3, 2, 1); x.fillStyle = '#e8c35a'; x.fillRect(2, 4, 2, 1); }),
    extras: [({ arms, U, box, solid }) => { const mic = box(1.6 * U, 5 * U, 1.6 * U, solid('#222', 41)); mic.position.set(0, -12.5 * U, 2.2 * U); mic.rotation.x = -.9; const ball = box(2.6 * U, 2.6 * U, 2.6 * U, solid('#9aa3ad', 43)); ball.position.set(0, -11 * U, 4.4 * U); arms[1].add(mic, ball); }] },
  hyperframes: { name: 'فریم', role: 'HyperFrames', skin: '#9fe3d6', eye: '#0d2b2b', shirt: '#127a73', pants: '#0f3a44', mouth: '#0d4a44',
    headSide: pix(16, (x, n) => { noise(x, n, '#1b1f27', 10, 51); x.fillStyle = '#e9edf2'; for (let i = 1; i < 16; i += 4) { x.fillRect(1, i, 2, 2); x.fillRect(13, i, 2, 2); } }),
    facePaint: (x) => { x.fillStyle = '#1b1f27'; x.fillRect(0, 0, 16, 2); x.fillRect(0, 14, 16, 2); x.fillStyle = '#e9edf2'; for (let i = 1; i < 16; i += 4) { x.fillRect(i, 0, 2, 1); x.fillRect(i, 15, 2, 1); } },
    chestTex: chest('#127a73', (x) => { x.fillStyle = '#e9edf2'; x.fillRect(3, 3, 10, 7); x.fillStyle = '#ff5a5f'; x.fillRect(4, 4, 3, 5); x.fillStyle = '#ffd34d'; x.fillRect(7, 4, 3, 5); x.fillStyle = '#4dc3ff'; x.fillRect(10, 4, 2, 5); }),
    extras: [({ arms, U, box, pix }) => { const cl = box(6 * U, 4 * U, 1 * U, pix(16, (x) => { x.fillStyle = '#111'; x.fillRect(0, 0, 16, 16); x.fillStyle = '#fff'; for (let i = 0; i < 16; i += 4) x.fillRect(i, 0, 2, 4); x.fillRect(2, 8, 12, 1); x.fillRect(2, 11, 8, 1); })); cl.position.set(0, -12.5 * U, 2.6 * U); arms[1].add(cl); }] },
  remotion: { name: 'ری‌موشن', role: 'Remotion Skills', skin: '#c9c3ff', eye: '#1c1450', shirt: '#4a3aff', pants: '#22195e', hair: '#2a1f7a', hairFringe: true, mouth: '#3a2a8a',
    chestTex: chest('#4a3aff', (x) => { x.fillStyle = '#fff'; for (let i = 0; i < 7; i++) x.fillRect(5 + Math.floor(i / 2), 3 + i, 7 - i, 1); x.fillStyle = 'rgba(255,255,255,.35)'; x.fillRect(1, 5, 3, 1); x.fillRect(1, 8, 4, 1); }),
    extras: [({ head, U, box, solid }) => { const band = box(9 * U, 1.2 * U, 2 * U, solid('#111', 61)); band.position.set(0, 8.6 * U, 0); const e1 = box(1.6 * U, 3.4 * U, 3.4 * U, solid('#ff4fa3', 63)); e1.position.set(-4.6 * U, 4 * U, 0); const e2 = e1.clone(); e2.position.x = 4.6 * U; head.add(band, e1, e2); }] },
  htmlvideo: { name: 'تگ', role: 'html-video', skin: '#d8f5c8', eye: '#123012', shirt: '#2f9e44', pants: '#1d4d27', mouth: '#1d4d27',
    headTop: pix(16, (x, n) => { noise(x, n, '#2f9e44', 10, 71); }),
    headSide: pix(16, (x, n) => { noise(x, n, '#d8f5c8', 10, 73); x.fillStyle = '#2f9e44'; x.fillRect(0, 0, 16, 3); }),
    facePaint: (x) => { x.fillStyle = '#2f9e44'; x.fillRect(0, 0, 16, 3); x.fillStyle = '#ffffff'; x.fillRect(1, 1, 1, 1); x.fillRect(2, 0, 1, 1); x.fillRect(2, 2, 1, 1); x.fillRect(14, 1, 1, 1); x.fillRect(13, 0, 1, 1); x.fillRect(13, 2, 1, 1); x.fillRect(8, 0, 1, 3); },
    chestTex: chest('#2f9e44', (x) => { x.fillStyle = '#fff'; [[3, 6], [4, 5], [4, 7], [5, 4], [5, 8], [10, 4], [10, 8], [11, 5], [11, 7], [12, 6], [7, 9], [8, 6], [8, 7], [7, 8], [9, 4], [8, 5]].forEach(([a, b]) => x.fillRect(a, b, 1, 1)); }),
    extras: [({ arms, U, box, solid, pix }) => { const lp = box(7 * U, .8 * U, 5 * U, solid('#c9ced6', 81)); lp.position.set(0, -12.5 * U, 3 * U); const sc = box(7 * U, 5 * U, .6 * U, pix(16, (x) => { x.fillStyle = '#14202b'; x.fillRect(0, 0, 16, 16); x.fillStyle = '#7ee787'; x.fillRect(2, 3, 6, 1); x.fillRect(4, 6, 8, 1); x.fillStyle = '#79c0ff'; x.fillRect(4, 9, 5, 1); x.fillRect(2, 12, 4, 1); })); sc.position.set(0, -10 * U, 5.4 * U); sc.rotation.x = -.35; arms[1].add(lp, sc); }] },
  manim: { name: 'مانی', role: 'Manim Skill', skin: '#f1d9b5', eye: '#1b2a4a', brow: '#555', shirt: '#3b4a5a', pants: '#25303b', hair: '#d9d9d9', hairFringe: true,
    shirtTex: pix(16, (x, n) => { noise(x, n, '#3b4a5a', 10, 91); x.fillStyle = 'rgba(255,255,255,.18)'; for (let i = 0; i < 16; i += 4) { x.fillRect(i, 0, 1, 16); x.fillRect(0, i, 16, 1); } }),
    chestTex: chest('#3b4a5a', (x) => { x.fillStyle = 'rgba(255,255,255,.18)'; for (let i = 0; i < 16; i += 4) { x.fillRect(i, 0, 1, 16); x.fillRect(0, i, 16, 1); } x.fillStyle = '#ffd34d'; for (let i = 0; i < 12; i++) x.fillRect(2 + i, 11 - Math.round(Math.sin(i / 2) * 3 + 3), 1, 1); }),
    extras: [({ head, U, box, solid, arms }) => { const cap = box(10 * U, 1 * U, 10 * U, solid('#111', 101)); cap.position.y = 9 * U; cap.rotation.y = .785; const top = box(5 * U, 2 * U, 5 * U, solid('#111', 103)); top.position.y = 8.2 * U; const tas = box(.6 * U, 4 * U, .6 * U, solid('#ffd34d', 105)); tas.position.set(4 * U, 7 * U, 0); head.add(cap, top, tas);
      const ch = box(1 * U, 4 * U, 1 * U, solid('#ffffff', 107)); ch.position.set(0, -12.5 * U, 1.5 * U); ch.rotation.x = -.6; arms[1].add(ch); }] },
  lemo: { name: 'لِمو', role: 'lemo-opuscar', skin: '#ffe27a', eye: '#3a2a00', shirt: '#f3efe6', pants: '#3a4a7a', mouth: '#9a5a00', brow: '#9a6a00',
    shirtTex: pix(16, (x, n) => { noise(x, n, '#f3efe6', 10, 111); [['#ff5a5f', 3, 4], ['#4dc3ff', 10, 9], ['#7ee787', 6, 13], ['#ffd34d', 12, 2]].forEach(([c, a, b]) => { x.fillStyle = c; x.fillRect(a, b, 2, 2); x.fillRect(a + 1, b + 2, 1, 1); }); }),
    extras: [({ head, U, box, solid, arms, pix }) => { const b1 = box(9 * U, 1.6 * U, 9 * U, solid('#c0392b', 121)); b1.position.set(.6 * U, 8.6 * U, 0); b1.rotation.z = -.12; const b2 = box(1.4 * U, 1.4 * U, 1.4 * U, solid('#c0392b', 123)); b2.position.set(1 * U, 10 * U, 0); head.add(b1, b2);
      const pal = box(6 * U, .8 * U, 5 * U, pix(16, (x) => { x.fillStyle = '#c8955a'; x.fillRect(0, 0, 16, 16); [['#ff5a5f', 3, 3], ['#4dc3ff', 9, 3], ['#7ee787', 3, 9], ['#ffd34d', 9, 10], ['#b07cff', 12, 6]].forEach(([c, a, b]) => { x.fillStyle = c; x.fillRect(a, b, 3, 3); }); })); pal.position.set(0, -12.5 * U, 3 * U); pal.rotation.x = .9; arms[1].add(pal);
      const br = box(.7 * U, 7 * U, .7 * U, solid('#7a4a20', 125)); br.position.set(0, -11 * U, 1 * U); br.rotation.x = -.8; arms[0].add(br); }] },
  onetake: { name: 'وان‌تیک', role: 'onetake', skin: '#c99772', eye: '#1a1a1a', brow: '#222', shirt: '#1b1b1f', pants: '#2b2b33', hair: '#2a1d14',
    chestTex: chest('#1b1b1f', (x) => { x.fillStyle = '#ff3b3b'; x.fillRect(3, 3, 3, 3); x.fillStyle = '#fff'; x.fillRect(7, 4, 6, 1); x.fillRect(7, 6, 4, 1); }),
    extras: [({ head, U, box, solid, pix, arms }) => { const cap = box(8.6 * U, 2.4 * U, 8.6 * U, solid('#ff3b3b', 131)); cap.position.y = 8.6 * U; const bill = box(6 * U, .8 * U, 4 * U, solid('#ff3b3b', 133)); bill.position.set(0, 7.6 * U, -5.6 * U); head.add(cap, bill);
      const cam = box(5 * U, 5 * U, 9 * U, solid('#2d2d33', 135)); cam.position.set(-7.6 * U, 6 * U, 1 * U); const lens = box(3.4 * U, 3.4 * U, 3 * U, pix(16, (x) => { x.fillStyle = '#111'; x.fillRect(0, 0, 16, 16); x.fillStyle = '#3a5a8a'; x.fillRect(4, 4, 8, 8); x.fillStyle = '#9ad'; x.fillRect(5, 5, 3, 3); })); lens.position.set(-7.6 * U, 6 * U, 6.6 * U);
      const rec = box(1 * U, 1 * U, 1 * U, solid('#ff2020', 137)); rec.position.set(-7.6 * U, 9 * U, 4 * U); head.add(cam, lens, rec); }] },
};
