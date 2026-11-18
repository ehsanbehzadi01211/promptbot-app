import { chromium } from 'playwright'; import http from 'http'; import fs from 'fs'; import path from 'path';
const [,, page, out, t = '1.3', w = '1920', h = '1080'] = process.argv; const root = process.cwd();
const srv = http.createServer((q, r) => { const f = path.join(root, decodeURIComponent(q.url.split('?')[0])); if (!fs.existsSync(f)) { r.writeHead(404); return r.end(); } const ty = { '.js': 'text/javascript', '.html': 'text/html', '.woff2': 'font/woff2', '.png': 'image/png', '.json': 'application/json' }[path.extname(f)] || 'application/octet-stream'; r.writeHead(200, { 'content-type': ty }); fs.createReadStream(f).pipe(r); }).listen(8765);
const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: +w, height: +h } });
p.on('console', m => { if (m.type() === 'error') console.log('ERR', m.text()); }); p.on('pageerror', e => console.log('PAGEERR', e.message));
await p.goto('http://localhost:8765/' + page); await p.waitForFunction('window.READY === true', null, { timeout: 60000 });
await p.evaluate(t => window.render(+t), t); await p.screenshot({ path: out }); await b.close(); srv.close();
