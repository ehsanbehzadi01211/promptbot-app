# Daily reel run (@ehbehzad) — one new reel per day

Reply to the owner in Persian. Every reel: strong hook in the first 2 seconds, narrator voice, word-by-word
subtitles, one short comment keyword with an automatic DM of links. Never invent numbers; check every tool,
price and free quota on the web the same day (if it changed or can't be checked, rewrite or skip the idea).

## 1. Setup (fresh session)

    git clone -b reels-media https://github.com/ehsanbehzadi01211/promptbot-app /tmp/rm
    mkdir -p /home/claude/v8 && cp -r /tmp/rm/pipeline/v10/* /home/claude/v8/ && cd /home/claude/v8
    npm install                                   # Vazirmatn + JetBrains Mono fonts
    pip install --break-system-packages numpy playwright   # Chromium is preinstalled; never run "playwright install"
    mkdir -p out && cp /tmp/rm/media/mascot_2_robot_glass.png /tmp/rm/media/mascot_1_ehsan.png out/   # talking hosts

The shell can only reach GitHub, npm and PyPI. Cloudinary, ElevenLabs and Uplika are reached through their
MCP tools only.

## 2. Pick the idea

`ideas.json`: first item with `"status": "todo"`. Research the topic, write a 30–50 s Persian script
(hook → condition/twist → 2–7 concrete items → "کلمه‌ی «X» رو کامنت کن"). Keep claims honest.

**Format (owner, 31 Oct): make every new reel in the `ui` format (ui.py)** unless the owner asks otherwise; the
idea's old `format` field is only a hint for the content. `ui` = the clean "studio UI" product-explainer look the
owner asked for (reference: farshad_frhni reel DfJ5NyeRHyl, but higher quality): cream canvas with drifting pastel
light, white UI cards, node diagrams whose edges draw and carry packets, counters, bars, chat windows, checklists,
score rings, a chapter pill bar on top, phrase subtitles that darken word by word with the current word in an
accent chip, blur/slide scene transitions, one dark scene for contrast, the glass robot top-left.
`list` (build9.py) and `laptop` (laptop.py) still work but are the old look.

### ui.json schema (see key `agents7` for a full worked example)
Times are word indices of the spoken text (`12`, or `"12+0.3"` / `"12-0.2"` for an offset in seconds).
* spec: `keyword`, `accent` (default #e8693c), `host: "robot"`, `voice`, `tabs` (chapter names, one per item scene),
  `scenes`.
* scene: `w` (start word), optional `tab` (index into tabs), `dark: true`, `head: {kick, h1: [[word, at],...],
  em: [i], hl: [i], top}`, optional `stage_top`, `els: [...]`. Last scene: `{"w": N, "type": "cta", "keyword": "...",
  "dm": "what they get in DM"}`.
* elements (stage = 920×780 px, shown at 1.1×, y 0 ≈ just under the headline):
  `node {x,y,label,icon,at,pal 0-6,sub,cls "c"|"big"|"c big",lit,m "pop"|"up"|"left"|"right"|"drop"}`,
  `edges {items:[{id,d (SVG path),at,hot,pk:[[at,dur,period?]]}]}`, `chip {x,y,text,icon,cls "a"|"g",at}`,
  `chat {x,y,w,h,at,dim,app,msgs:[{who "me"|"ai",text,at,type (end time → typing),dots,out}]}`,
  `meter {y,at,label,from,to,suffix,count_at,count_end,color,badge{text,at,icon}}`, `big {at,end,count:[a,b],text,y}`,
  `h {y,words:[[html,at]],size}`, `tiles {y,at,step,items:[[name,icon]]}` (≤8), `lanes {y,at,fill_at,dur,items:[[name,speed]]}`,
  `checklist {y,at,items:[[text,tick_at]]}`, `score {x,y,at,keys:[[at,value]]}`, `orbit {cx,cy,r,at,speed,items:[[name,icon]]}`,
  `html {html}` (raw, `{w12+0.3}` placeholders).
  Icons: chat brain tool db search doc split user users check bolt crown eye pen loop flag mail headset cart code spark target.
* Every scene must show something within ~0.3 s of its start (first element at `"w+0.3"`), elements must not
  reach the subtitles (stage y ≤ ~760), and each item scene should *show* the idea (a diagram, UI or demo), not just
  text. Vary the layouts between reels.

## 2b. Talking host (every reel)

The owner chose a host character: a small robot in frosted white glass (`out/mascot_2_robot_glass.png`).
Put `"host": "robot"` in every spec unless the owner says otherwise (`"ehsan"` = his own cartoon, only if he
asks). `host.py` draws the robot's eyes (blinking) and mouth (opens on every narrated word) on its blank
screen and bobs the head. build9: first scene big (the hook emoji is hidden), later scenes a circle top-left;
override per scene with `"host": "big" | "corner" | "off"` (use "off" where a scene's content sits top-left).
laptop and ui: always the top-left circle. Always look at the `--stills` frames and fix overlaps before rendering.
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

## 3b. Fresh music under every reel (owner, 29 Oct: the music was too repetitive)

Every reel gets its OWN background track; never reuse one.
* ElevenLabs Music (`eleven_music_v2_5`, through `creative_generate_in_flow` on flow `bu6itCvwoCIwUujfT3Td`):
  instrumental only, `duration_seconds` = reel length + 2, prompt = a different genre/mood each day that fits
  the topic (e.g. lo-fi chill, cinematic tension, synthwave, upbeat electronic pop, afro-house, light phonk,
  ambient tech, funky groove, epic trailer), "no vocals, steady energy, sits under a voice-over".
  Write the prompt into the idea as `"music": "<prompt>"` and check the last 7 ideas so genres don't repeat.
* Get the mp3 into the container through the fetch-media workflow: put `music_<key>.mp3 <content_url>` in
  `/tmp/rm/fetch.txt`, commit, push, wait until `media/music_<key>.mp3` appears (git fetch; ~1 min).
* Render with `MUSIC_FILE=/tmp/rm/media/music_<key>.mp3` set (build9.py and laptop.py then make only the SFX
  and mix the track at low volume with fades, 48 kHz stereo). If music generation fails, render without
  MUSIC_FILE: the built-in synth beat now changes tempo/key/sound per reel. Say which one you used in the report.

## 4. Render

* ui format (default): add the spec under a new key in `ui.json`, words in `words10/<key>.json`, then
  `python3 ui.py <key> --stills` (look at every still: overlaps, empty frames, text over subtitles), then
  `MUSIC_FILE=... python3 ui.py <key>` → `out/<key>_ig_nolvoice.mp4` (~6–8 min for 50 s).
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
* Slot (owner, 29 Oct): at most TWO Instagram reels per day, at 10:00 and 21:00 Tehran (the hours with the
  most views/comments on our page; 17:00 was weak). New reels go at 21:00: take the first day from tomorrow on
  with no reel at 21:00 UTC+03:30 (= 17:30 UTC) and fewer than 2 reels that day; check with
  `list_posts status=scheduled sort=scheduled`. `scheduledAt` like `2026-11-08T21:00:00+03:30`.
  Never schedule a third reel on a day; stories and YouTube don't count.
* Then `create_comment_to_dm` on that post id: keywords (+ spelling variants), `requireFollow: true`,
  same message/button/publicReply wording as the existing v9 automations, deliver text + up to 3 link
  buttons, `enabled: true`. (The `automation` field on `publish` does NOT create it for scheduled posts.)
* YouTube (`conn_0518c6141bae7d86`) is optional: its daily slot 12:30 UTC is already filled until Nov 18 and
  Uplika's shared YouTube quota fails often.

## 6. Finish

Set the idea to `"status": "scheduled", "post": <id>, "date": <day>` in `ideas.json`, commit + push.
Report to the owner in Persian: the hook, the day/time, the keyword, and a link to the final video.
