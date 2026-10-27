# Daily reel run (@ehbehzad) — one new reel per day

Reply to the owner in Persian. Every reel: strong hook in the first 2 seconds, narrator voice, word-by-word
subtitles, one short comment keyword with an automatic DM of links. Never invent numbers; check every tool,
price and free quota on the web the same day (if it changed or can't be checked, rewrite or skip the idea).

## 1. Setup (fresh session)

    git clone -b reels-media https://github.com/ehsanbehzadi01211/promptbot-app /tmp/rm
    mkdir -p /home/claude/v8 && cp -r /tmp/rm/pipeline/v10/* /home/claude/v8/ && cd /home/claude/v8
    npm install                                   # Vazirmatn + JetBrains Mono fonts
    pip install --break-system-packages numpy playwright   # Chromium is preinstalled; never run "playwright install"
    mkdir -p out && cp /tmp/rm/media/mascot_1_ehsan.png out/   # the owner's cartoon (talking host)

The shell can only reach GitHub, npm and PyPI. Cloudinary, ElevenLabs and Uplika are reached through their
MCP tools only.

## 2. Pick the idea

`ideas.json`: first item with `"status": "todo"`. `format` = `list` (build9.py, scenes like spec9.json) or
`laptop` (laptop.py, like laptop.json key `motion`). Research the topic, write a 25–40 s Persian script
(hook → condition/twist → 2–5 concrete items → "کلمه‌ی «X» رو کامنت کن"). Keep claims honest.

## 2b. Talking host (owner's cartoon)

If the idea has `"host": true` (or the owner asked for it), add `"host": true` to the spec. `host.py` animates
`out/mascot_1_ehsan.png` as a cut-out puppet: the mouth opens on every narrated word, the head bobs.
build9: first scene shows it big (the hook emoji is hidden), later scenes in a circle top-left; override per
scene with `"host": "big" | "corner" | "off"` (use "off" where a scene's content sits top-left).
laptop: always the top-left circle. Always look at the `--stills` frames and fix overlaps before rendering.
(ElevenLabs video/lip-sync models need a paid plan on this account, so the host is animated in code.)

## 3. Voice + word times (ElevenLabs MCP)

* `creative_generate_speech`: model `eleven_v4`, voice Aran Parsi `PEdcOLzbXYhL8IKOswXB`,
  flow `bu6itCvwoCIwUujfT3Td`, `generations_count: 1`, prompt starts with `[excited]`.
* 429 = rate limit, nothing was started: wait ~2 min and call again (never resend after a success).
* `creative_transcribe_audio` with `connect_from: [<tts node id>]`, same flow → `words[].start`.
  Drop the `[excited]` token; save `{"t":[starts...], "end": last_end}` to `words10/<key>.json` (or `words9/`
  for list format). The count must equal the number of whitespace tokens of the spoken text.
* Upload the mp3 to Cloudinary (`upload-asset`, `upload_request: {file: <content_url>, public_id:
  "v10_voice_<key>", folder: "ehbehzad", resource_type: "video"}`).

## 4. Render

* list format: add the spec under a new key in `spec9.json`, then
  `SPEC=spec9.json WORDS=words9 python3 build9.py <key> ig` → `out/<key>_ig_nolvoice.mp4`
* laptop format: add to `laptop.json`, then `python3 laptop.py <key>` → `out/<key>_ig_nolvoice.mp4`
  (`--stills` renders one frame per beat to check the layout first; look at them).
* Render takes several minutes: run it with nohup and poll the log.

## 5. Mix voice + publish

* `cp out/<key>_ig_nolvoice.mp4 /tmp/rm/v10/` → commit (author "Ehsan Behzadi
  <ehsanbehzadi01211.eb@gmail.com>") → `git push origin reels-media`.
* Cloudinary `upload-asset` from
  `https://raw.githubusercontent.com/ehsanbehzadi01211/promptbot-app/reels-media/v10/<key>_ig_nolvoice.mp4`
  as `ehbehzad/v10_<key>_nolvoice` (resource_type video).
* Final URL (voice starts 0.25 s in; keep the version number to avoid stale cache):
  `https://res.cloudinary.com/qecsawrr/video/upload/l_audio:ehbehzad:v10_voice_<key>/fl_layer_apply,so_0.25/ac_aac,af_48000/q_auto:best/v<version>/ehbehzad/v10_<key>_nolvoice.mp4`
  (Instagram drops 96 kHz audio; the audio must be 48 kHz.) Upload that URL to Cloudinary as
  `ehbehzad/v10_<key>_final` so the file is fixed.
* Uplika `media_from_url` (final URL, aiGenerated true) → `publish` to Instagram `conn_a8ade4f9de0c6bca`,
  `options.instagram.contentType: "reel"`, `isAiGenerated: true`, caption = hook line + body + keyword line +
  footer (▶️ یوتیوب: youtube.com/@ehbehzad / 📷 اینستاگرام: @ehbehzad / 📢 تلگرام: @ehbehzad_ai) + 5 hashtags.
* Slot: the first day from tomorrow on with no reel at 13:30 UTC (17:00 Tehran); check with
  `list_posts status=scheduled sort=scheduled`. `scheduledAt` like `2026-11-03T17:00:00+03:30`.
* Then `create_comment_to_dm` on that post id: keywords (+ spelling variants), `requireFollow: true`,
  same message/button/publicReply wording as the existing v9 automations, deliver text + up to 3 link
  buttons, `enabled: true`. (The `automation` field on `publish` does NOT create it for scheduled posts.)
* YouTube (`conn_0518c6141bae7d86`) is optional: its daily slot 12:30 UTC is already filled until Nov 18 and
  Uplika's shared YouTube quota fails often.

## 6. Finish

Set the idea to `"status": "scheduled", "post": <id>, "date": <day>` in `ideas.json`, commit + push.
Report to the owner in Persian: the hook, the day/time, the keyword, and a link to the final video.
