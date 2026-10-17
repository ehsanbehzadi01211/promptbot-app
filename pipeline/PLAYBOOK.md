# @ehbehzad content system — one agent, three channels (since 11 Oct 2026, 22:30 Tehran)

> **Owner, 17 Oct 2026 — overrides everything below and in YOUTUBE.md:**
> - **English YouTube Shorts are CANCELLED** — do not build, voice, render or upload any English video. The `en*` queue
>   items are `cancelled`. The daily production and weekly English tasks stay disabled.
> - **YouTube is now Persian**: the same Persian reels as Instagram, same design, Persian title/description/tags.
>   Queue items `platform youtube` with `lang fa` and `key fa_*`: video `youtube/shorts/<key>.mp4`, title/desc/tags in
>   `pipeline/scripts_en.json[<key>]` (kept there so the existing publisher task can read them; source file
>   `content/fa_youtube.py`). Upload them exactly as written (Persian), Education, not for kids, altered content Yes.
> - Instagram stories are in the queue (19:00 daily, media URL in the item). Desktop Instagram has no story upload:
>   if Chrome cannot post it, set it `manual`/`skipped`; the Telegram bot (promo.py) then sends the file to the owner's
>   private chat to post from his phone.
> - Queue restarted on 18 Oct with the same hour rotation (rebuild script `content/rebuild_1017.py`).

The owner cancelled the separate Instagram and YouTube desks. ONE agent plans and runs everything end to end
(Instagram, YouTube, Telegram) and reports to him in Persian, always in three sections: تلگرام، اینستاگرام، یوتیوب.
INSTAGRAM.md and YOUTUBE.md stay as reference for each platform's rules; where they talk about "separate desks",
this file wins.

## Single source of truth: content/queue.json
Every Instagram and YouTube item that will be published, with its Tehran time (`when`), kind, topic, status
(`queued` / `published` / `skipped` / `failed`), and where its content lives:
- Instagram items: caption, media and cover are in Metricool (`metricool_uuid`; find it with getScheduledPosts around
  `metricool_date`). `override.media` / `override.cover` replace the Metricool media when present.
- YouTube items: video `youtube/shorts/<key>.mp4` in this repo (raw URL
  https://raw.githubusercontent.com/ehsanbehzadi01211/promptbot-app/reels-media/youtube/shorts/<key>.mp4);
  title, description and tags from pipeline/scripts_en.json[<key>].
content/schedule.json is derived from the queue (date, time, platform, kind, topic) — rewrite it whenever the queue changes;
the Telegram bot sends it to the owner every morning (08:20 Tehran) and announces new items.

## Publishing: through the owner's Chrome (Claude in Chrome extension), at the queue time
Metricool's free plan is exhausted until 1 Nov 2026 ("You have reached your Metricool account limit"), and the owner wants
uploads done in his own Chrome. Metricool is only a content store now. The scheduled task
"@ehbehzad publisher (Chrome)" runs on the owner's computer a few minutes before each slot (10:00, 16:00, 19:00, 21:00 Tehran):
1. Load the Claude in Chrome tools (ToolSearch "claude-in-chrome"; read the chrome-browser skill), tabs_context first.
2. For each queue item whose `when` is within the next 10 minutes or already passed today with status `queued`:
   set its Metricool post to draft first (so Metricool can never publish a duplicate), check the profile/channel that it
   is not already there, download the media, wait until the exact minute, and upload:
   - Instagram: instagram.com → Create; reel (Trial reel if offered), carousel in slide order, exact Metricool caption,
     AI label on. Stories: try; if desktop has no story option mark `manual` (the bot sends the file to the owner).
   - YouTube: studio.youtube.com → Create → Upload; Persian title/description/tags from scripts_en.json[<key>]
     (since 17 Oct), not made for kids, category Education, altered/synthetic content = Yes, Public.
3. Write status `published` + the post URL (or `failed` + reason) into content/queue.json and push. The push makes the
   Telegram bot announce it in the channel (newsbot/promo.py).
4. If the Chrome tools are missing or a site asks for a login/2FA/captcha, do not improvise: tell the owner exactly which
   items are waiting.

## Telegram channel @ehbehzad_ai (GitHub Actions, newsbot/)
- AI news: every 2 hours, max 3 per run and 16 per day, Persian title + summary + source link, ALWAYS with a picture (owner, 11 Oct): the story's own image (feed media or og:image), otherwise a branded card about the story (newsbot/card.py).
- Announcement in the channel each time an Instagram post or YouTube Short goes live (promo.py, from queue.json).
- Owner's private chat: 7-day schedule every morning at 08:20 Tehran, plus a note whenever new items are queued.

## Production
- English Shorts production is cancelled (17 Oct); the daily production task is disabled. New Instagram videos are
  still paused by the owner ("no new Instagram videos for now"). The weekly planning task is disabled too; ready
  carousels run out on 24 Oct and reels on 7 Nov — ask the owner before making new content.
- Time rotation (d = days since 11 Oct): IG reel {0:10,1:16,2:21}, IG carousel {0:21,1:10,2:16}, YT {0:16,1:21,2:10}, story 19:00.
  A one-time task on 24 Oct analyses it and moves later queue items to the winning hours.
