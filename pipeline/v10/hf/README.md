# HyperFrames: optional tool for SOME segments (owner decision, 7 Nov 2026)

NOT a replacement for the current renderer. The owner said the current designs "smell AI" and the reel
that got ~4K views is the quality bar. Use HyperFrames (Apache-2.0, free, local render) only for
selected parts of selected reels, e.g. a title card, a kinetic-type hook, an animated chart,
a transition, an overlay. Not every reel and not the whole reel.

## Sandbox recipe (verified 7 Nov, renders 1080x1920 in ~17 s per 14 s)
- Node 22 + ffmpeg exist. `npx -y hyperframes init <dir> --skip-skills`
- Its own Chrome download is blocked: `export HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium-1243/chrome-linux64/chrome`
- CDN is blocked: `npm pack gsap@3.15.0`, copy `package/dist/gsap.min.js` to `vendor/`, script src `vendor/gsap.min.js`.
- Persian font: copy Vazirmatn woff2 into `assets/fonts/` and use @font-face (only bundled fonts resolve by name).
- Size comes from root `data-width`/`data-height` (no --width flag). `npx hyperframes render -o out.mp4`.
- Lint: `npx hyperframes check --json` (the runtime error about Chrome only means the env var is not set).
- Keep content in the 168-1330 px band. Latin text needs a Latin font in the same @font-face stack.
- Known fix: handle `@ehbehzad` needs `dir=ltr` or it shows as `ehbehzad@`.

`example_vertical_index.html` is the 14 s test (hook, 3 numbered points, keyword card).
