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

## 2c-bis. Closing follow card (owner, 2 Nov)

Every ui reel ends with a ~2.6 s follow card (robot avatar, page handle, tagline, «+ فالو») on a blurred backdrop, like the speedy_devv reference.
It is built into ui.py (`TAIL = 3.4`, `#fol`); nothing to do per reel. `python3 ui.py <key> --stills` also writes `<key>_ui_end.png` to check it.
Per-page handle chip + card: default = @ehbehzad, `UI_VARIANT=hooshyar` = @hooshyar__ai.

## 2c. Reach rules (owner asked 2 Nov after the diagnosis; see project doc reach-diagnosis-2026-11-02)

Measured: @ehbehzad reels get ~200 views (3.6K followers) while mgh.mobin (149K) has a median of 62K. Spikes came only from
"free tool + comment keyword" reels (2-4K); generic tip lists and ads for Claude stayed at ~200. So:
* **Pick order**: prefer ideas that name a real FREE tool/limit (verified) or a surprising proof («این رو من نساختم», «X رو کشت»). Skip pure tip lists
  and trading/finance topics unless nothing else is todo.
* **Hook (first 2 s, spoken + on screen)**: one sharp claim or proof, not a title. Examples of the style that works for the references:
  «این ویدیو رو من نساختم 👀», «هنوز توی سطح یکی هستی؟», «پول X نده، این رایگانه». Never start with "۳ تا ..." alone.
* **Length**: the references run 40-75 s (mgh.mobin median 66 s). From now on make every second reel 45-60 s (more concrete steps,
  not filler) to test watch time; keep the others at 30-40 s. Note the length in ideas.json (`len`).
* **Caption**: hook line + 2-4 short lines + the keyword line. Footer is ONE line `📷 @ehbehzad` only (no YouTube/Telegram lines),
  at most 3 hashtags. Telegram/YouTube links go into the DM message instead.
* After 7 days, re-measure with `/api/v1/media/{id}/info/` (Chrome tab) and compare against the previous week; log the numbers in the project doc.

> **UPDATE (8 Nov 2026):** ElevenLabs TTS works again after the owner fixed the account, but only in the NEW flow `bL6QQph8QFSQMkqJ05SL` (the old flow `bu6itCvwoCIwUujfT3Td` is dead: create a new flow if it errors). Music (`eleven_music_v2_5`) was still "busy" / "Insufficient funds": try once per turn, and if it answers busy do not start a second generation; fall back to the built-in synth beat and say so in the report. Never reuse an old track.

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
  footer `📷 @ehbehzad` only (see 2c: no YouTube/Telegram lines in the caption) + at most 3 hashtags.
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


## 2d. Reach rules v2 (owner research request, 7 Nov)
Measured: our reels ~230 views; named free tool + visual proof + keyword spikes (design skills 4K, motion 1.5K). @cookin.code (7K followers) gets 16K-193K with 30-40 s reels, one named free GitHub tool/skill, one-word keyword, caption of ONE line + <=3 hashtags. So: make new reels 30-35 s (max 45), one named free thing, hook = the claim in 2 s, show the real UI/result, one-word keyword, and the creator-style comment replies are handled by the automation. Never promise results. Only @ehbehzad now.

## 2e. HyperFrames for some segments (owner, 7 Nov)
Owner: do NOT replace the renderer, the designs still smell AI and must look more professional, like the reel that got ~4K views.
Use HyperFrames (see pipeline/v10/hf/README.md) for selected segments of SOME new reels only (a title card, kinetic hook, chart, transition, overlay), then composite into the normal render. Never for every reel.

## 5b. Second page @hooshyar__ai — CANCELLED (owner, 7 Nov)
**STOP: do NOT render, schedule or publish anything on @hooshyar__ai any more. Only @ehbehzad. Ignore everything below in this section; kept for history only.** On 7 Nov all 9 scheduled hooshyar posts were deleted and the automations attached to them were disabled; already-published hooshyar posts and their automations were left as they are.

(old text, no longer valid:) 5b. Second page @hooshyar__ai (owner, 1 Nov) 

Uplika now has TWO workspaces, so **every Uplika call needs workspaceId**:
* @ehbehzad (Instagram conn_a8ade4f9de0c6bca, YouTube conn_0518c6141bae7d86): `ws_680c8b2ee3656246`
* @hooshyar__ai (Instagram conn_dbfffe5a1a54753c): `ws_b59367124738a6a7`

hooshyar = «هوشیار | هوش مصنوعی به زبان ساده», same topics, violet look, the glass robot is "هوشیار".
* Render a second version of the same reel (owner, 2 Nov): the ONLY difference is the page handle burned into the video.
  Every ui reel now carries a small handle chip top-right (`@ehbehzad`); `UI_VARIANT=hooshyar MUSIC_FILE=... python3 ui.py <key>`
  swaps it to `@hooshyar__ai` (same colours, same voice, same music) → `out/<key>_hy_ig_nolvoice.mp4`. Push it as `v10/<key>_hy_ig_nolvoice.mp4`,
  upload to Cloudinary as `ehbehzad/v10_<key>_hy_nolvoice`, mix the same voice the same way, save as `ehbehzad/v10_<key>_hy_final`.
* Schedule on hooshyar (owner, 1 Nov: **2 reels/day, 10:00 and 21:00 Tehran**). On 1 Nov the 18 older @ehbehzad reels were copied as-is
  (media_from_url of their Uplika cdn file, same caption with the hooshyar footer, own comment_to_dm automations) and fill every slot until
  11 Nov 10:00. A new reel takes the first free 21:00 slot (check `list_posts status=scheduled sort=scheduled` with workspaceId ws_b59367124738a6a7).
  Every hooshyar post needs its own comment_to_dm. DM auto-reply (ai_reply) is on for both pages (af_ec33805335e450f1 hooshyar, af_d33e3005c804bd63 ehbehzad). It goes out on hooshyar first and later on @ehbehzad, which is fine.
* **Duplicate-content rule (2 Nov, owner)**: each page's reel shows its OWN handle inside the video and its own caption footer. Do not copy
  an @ehbehzad video as-is to hooshyar. Instagram also fingerprints picture/audio, so keep a few days between the two pages when possible
  and reword the hook line in the caption.
* Caption: same text, but the footer is `🤖 هوشیار | هوش مصنوعی به زبان ساده` + `📷 @hooshyar__ai`
  (no @ehbehzad YouTube/Telegram lines). At most 3 hashtags.
* `create_comment_to_dm` with workspaceId ws_b59367124738a6a7, accountId conn_dbfffe5a1a54753c, same keyword,
  deliver and button; notFollowingMessage asks to follow @hooshyar__ai. Example: automation af_56d9170e4662c485 (agents7).
* In ideas.json also set `hy_post`, `hy_date`, `hy_automation`.

## 5c. Put the new reel in the upload queue (owner, 8 Nov: every day one new reel AND it goes into the upload queue)

Every new reel must also be added to `content/queue.json` (list, indent=2, ensure_ascii=False), so the daily
publisher task tracks it and also uploads it to YouTube. Append TWO items (`<day>` = the day you scheduled it):

* Instagram (already scheduled by you in 5):
  `{"platform":"instagram","kind":"reel","when":"<day>T21:00","topic":"<hook>","key":"v10_<key>",
  "media":"<final Cloudinary URL>","status":"scheduled","id":"in-<day>-reel-v10","via":"uplika",
  "uplika_post":"<post id>","automation":"<automation id>"}`
* YouTube Short (the publisher schedules it through Uplika):
  `{"platform":"youtube","kind":"short","lang":"fa","when":"<day>T21:00","topic":"<hook>","key":"fa_v10_<key>",
  "media":"<final Cloudinary URL>","status":"queued","id":"yo-<day>-short-v10"}`
* Add `pipeline/scripts_en.json["fa_v10_<key>"]` = `{"lang":"fa","title":"<Persian title, max 90 chars> #Shorts",
  "desc":"<2-4 Persian lines>\n\n▶️ یوتیوب: https://youtube.com/@ehbehzad\n📷 اینستاگرام: https://instagram.com/ehbehzad\n📢 تلگرام: https://t.me/ehbehzad_ai\n\n#Shorts #هوش_مصنوعی ...",
  "tags":[5-10 Persian/English tags]}` (same shape as the existing fa_* entries; no comment-keyword line, YouTube has no DM automation).
* If an id already exists, do not add a second one. `git pull --rebase` before committing.

## 6. Finish

Set the idea to `"status": "scheduled", "post": <id>, "date": <day>` in `ideas.json`, make sure step 5c is done
(queue.json + scripts_en.json), commit "reel v10_<key> + queue" and push.
Report to the owner in Persian: the hook, the day/time, the keyword, and a link to the final video.
