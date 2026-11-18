# Reel / carousel pipeline (@ehbehzad)

Fresh session setup (paths are hard-coded):

    git clone -b reels-media https://github.com/ehsanbehzadi01211/promptbot-app /home/claude/reels-media
    mkdir -p /home/claude/reels && cp -r /home/claude/reels-media/pipeline/* /home/claude/reels/
    cd /home/claude/reels && npm install            # Vazirmatn font (@fontsource/vazirmatn)
    pip install --break-system-packages playwright numpy   # Chromium is preinstalled (PLAYWRIGHT_BROWSERS_PATH)

* Carousels: edit `carousels.json`, put backgrounds in `/home/claude/reels-media/media/` (`cN_cover.jpg`, `cN_bg.jpg`),
  run `python3 carousel.py <key>`, copy `carousels/<key>` into the repo, push, and schedule the raw.githubusercontent
  URLs pinned to the commit SHA as an Instagram POST in Metricool (blogId 7161172, Asia/Tehran).
* Reels without voice: spec with `"silent": seconds, "scuts": [...]`, empty `"voice": ""` per scene,
  `python3 build7.py <key> none <specs.json>` -> `out/<key>.mp4` (~9 min per 20 s on 2 CPUs; run detached).
  Stock clips live in `/home/claude/reels-media/stock/<id>.mp4`.
* HTML templates must be written in /home/claude/reels (relative font URLs).
* Downloads go through the `fetch-media` workflow (`fetch.txt`: "name url" per line) because the container
  can only reach GitHub/PyPI/npm.
