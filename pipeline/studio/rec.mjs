// frame-accurate recorder: page.render(t) -> jpeg -> ffmpeg
import { chromium } from 'playwright'; import http from 'http'; import fs from 'fs'; import path from 'path'; import { spawn } from 'child_process';
const [,, page, out, w = '1920', h = '1080', fps = '30', from = '0', to = ''] = process.argv; const root = process.cwd();
const srv = http.createServer((q, r) => { const f = path.join(root, decodeURIComponent(q.url.split('?')[0])); if (!fs.existsSync(f)) { r.writeHead(404); return r.end(); } const ty = { '.js': 'text/javascript', '.html': 'text/html', '.woff2': 'font/woff2', '.jpg': 'image/jpeg', '.json': 'application/json' }[path.extname(f)] || 'application/octet-stream'; r.writeHead(200, { 'content-type': ty }); fs.createReadStream(f).pipe(r); }).listen(8766 + Math.floor(Math.random() * 500));
const port = srv.address().port;
const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: +w, height: +h } });
p.on('pageerror', e => console.log('PAGEERR', e.message));
await p.goto(`http://localhost:${port}/${page}${page.includes('?') ? '&' : '?'}w=${w}&h=${h}`); await p.waitForFunction('window.READY === true', null, { timeout: 120000 });
const dur = to ? +to : await p.evaluate('window.DUR'); const N = Math.round((dur - +from) * +fps);
const ff = spawn('/root/ff7/ffmpeg', ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', fps, '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
const t0 = Date.now();
for (let i = 0; i < N; i++) { const t = +from + i / +fps; await p.evaluate(t => window.render(t), t); const buf = await p.screenshot({ type: 'jpeg', quality: 90 }); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); if (i % 300 === 0) console.log(i, '/', N, ((Date.now() - t0) / 1000).toFixed(0) + 's'); }
ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close(); srv.close(); console.log('done', N);
