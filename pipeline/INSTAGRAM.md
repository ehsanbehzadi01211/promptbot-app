# Instagram desk (@ehbehzad) — handoff

Owner: Ehsan Behzadi. Reply to him in Persian only. Instagram content is in natural colloquial Persian.
He wants everything produced and published automatically (no approval step), and a report about
Instagram only. YouTube is handled by a separate chat (see YOUTUBE.md); never post Persian videos to YouTube.

Setup for a fresh session: see SETUP.md (clone branch `reels-media` of ehsanbehzadi01211/promptbot-app,
copy `pipeline/*` to /home/claude/reels, npm install, pip install playwright numpy). Commit as
"Ehsan Behzadi <ehsanbehzadi01211.eb@gmail.com>".

## Owner instructions, 11 Oct 2026
- **No new Instagram videos for now** ("ویدیو جدید دیگه نساز برای اینستاگرام فعلا"). Do not render or schedule new reels
  until he says otherwise; already-scheduled reels stay. Carousels and stories are not affected.
- reel28s/reel29s were rendered on 11 Oct but NOT pushed or scheduled (render was stopped on his request);
  reel30s is still unrendered. In reel29s the step labels should read "Settings → Capabilities" / "Customize → Skills"
  (LTR run, the arrow currently points the wrong way) before any future render.

## Standing rules
- Daily: exactly **one carousel post + one reel**. All reels go out as **TRIAL_REEL** (isAiGenerated true).
- Stories are welcome too (free-tool / AI-tip stories, `story.py`, `scripts_story.json`).
- Caption footer on every post: `▶️ یوتیوب: youtube.com/@ehbehzad` / `📷 اینستاگرام: @ehbehzad`, then max 5 hashtags.
- Some content should be website-design promos ending with a DM offer
  ("دایرکت پیام بده، برات طراحی می‌کنم", sample work elvaleather.ir).
- No comment-keyword → DM-link automation (he dropped it).
- Persian voiceovers (ElevenLabs, model eleven_v4, voice Kaveh `xKk80LgyXTAl6McCiFke`, generations_count 1):
  add diacritics on ambiguous words and verify with the transcribe workflow before using the voice.
- Carousels: reference style = the MOBIKAA "۴۲ چنل یوتیوب" carousel (3D desk scene, one colour per topic,
  glass list rows, save/comment CTA). Renderer `carousel.py`, data `carousels.json`, backgrounds `media/cN_cover.jpg`,
  `media/cN_bg.jpg`. Cloudinary generate-image (flux standard) for new backgrounds, max 3 per week.
- He asked for trending music on carousels; the Metricool API only supports audio on reels, so carousels go without.
- 2D animated video (`out/demo_gpt6.mp4`, spec `scripts11.json` demo_gpt6): NOT to be posted until he finalises it with you.

## Posting-time test (until 24 Oct 2026), Tehran time, d = days since 11 Oct 2026
| d % 3 | reel | carousel |
|---|---|---|
| 0 | 10:00 | 21:00 |
| 1 | 16:00 | 10:00 |
| 2 | 21:00 | 16:00 |
A scheduled task on 24 Oct analyses the results and moves later posts to the winning hours.

## Metricool
blogId 7161172, timezone Asia/Tehran. Updating a post needs the full info JSON; the id changes, uuid stays.
**Account limit:** every post from 9 Oct 2026 onward failed with "You have reached your Metricool account limit."
The owner has to check/upgrade the Metricool plan. Metricool's help centre says the free plan publishes at most
20 posts per calendar month (resets on the 1st), which matches these errors; still failing on 10 Oct 22:15.
Scheduling is accepted, the refusal happens at publish time, so PENDING does not mean it will go out. Failed posts to re-schedule once fixed:
reel "پیج اینستاگرامت مال تو نیست", reel "سایت کند یعنی مشتری رفته", carousel GPT-6 (c1_gpt6), 4 stories.

## Scheduled (as of 11 Oct 2026)
Trial reels daily 11–29 Oct (reel19…reel18 topics + Claude-in-Google-Docs news), carousels 11–17 Oct
(c2 tools, c3 prompts, c4 news, c5 channels, c6 mistakes, c7 jobs, c8 website). Carousels from 18 Oct onward are
made by the weekly scheduled task (Thursdays 18:47 Tehran). Ready but unscheduled: out/reel28s, reel29s
(silent reels about Claude skills/connectors); reel30s needs a re-render.

## Telegram AI-news bot (lives with this desk)
Code in `newsbot/` (news.py fetch/post, discover.py, schedule.py, newsbot.workflow.yml). The bot token must never be
committed (repo is public): it has to go in a GitHub secret `TELEGRAM_BOT_TOKEN`, ideally in a new private repo.
11 Oct: owner said the public repo is fine, the bot is started and is admin of the channel. Workflow installed as
`.github/workflows/newsbot.yml` on main (cron) and reels-media (push); it checks out reels-media, writes
`newsbot/run_log.txt` and commits state. A push whose message contains "[news]" and touches `newsbot/run.txt` runs a
fetch+post immediately. Still needed from the owner: the repository secret `TELEGRAM_BOT_TOKEN` (cannot be set from
a Claude session). If the channel is not discovered (Telegram keeps updates only 24 h), set repo variable
`TELEGRAM_CHANNEL` or put the id in `newsbot/state/chats.json`.
News → public channel; daily content schedule → owner's private chat with the bot.
