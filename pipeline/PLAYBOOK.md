# @ehbehzad content system — one agent, three channels (since 11 Oct 2026, 22:30 Tehran)

> **Owner, 18 Oct 2026 — Instagram publishing goes through the Uplika connector (cloud, no laptop needed).**
> Uplika account `conn_a8ade4f9de0c6bca` (@ehbehzad, Instagram login). Tools: mcp__Uplika__media_from_url (raw GitHub URL,
> media ids expire after ~2 days unless used) → mcp__Uplika__publish with scheduledAt (Tehran +03:30) and
> options.instagram {contentType reel|feed|story, isAiGenerated true, coverMediaId for reels}. Captions = the Metricool
> post text (metricool_uuid); media = override.media / override.cover / story media in the queue item.
> Uplika has no Trial-reel option: reels go out as normal reels. Scheduled items get status `scheduled`, `via uplika`,
> `uplika_post`; the daily Uplika task schedules the next 2 days and marks yesterday's posts `published` with the URL.
> The Chrome publisher only touches `queued` items, so it never duplicates them. YouTube moves to Uplika as soon as a
> YouTube account appears in mcp__Uplika__list_accounts (owner connects it at https://uplika.com/dashboard/connections).
>
> **Owner, 17 Oct 2026 — overrides everything below and in YOUTUBE.md:**
> - **NO NEW VIDEOS of any kind** (owner, 17 Oct 22:55: «هیچ ویدیو جدید تولید نکن، فقط ویدیوهای قبلی آپلود کن»).
>   Do not script, voice, render or re-edit anything; only upload the existing videos already in content/queue.json.
> - **English YouTube Shorts are CANCELLED** — do not build, voice, render or upload any English video. The `en*` queue
>   items are `cancelled`. The daily production and weekly English tasks stay disabled.
> - **YouTube is now Persian**: the same Persian reels as Instagram, same design, Persian title/description/tags.
>   Queue items `platform youtube` with `lang fa` and `key fa_*`: video `youtube/shorts/<key>.mp4`, title/desc/tags in
>   `pipeline/scripts_en.json[<key>]` (kept there so the existing publisher task can read them; source file
>   `content/fa_youtube.py`). Upload them exactly as written (Persian), Education, not for kids, altered content Yes.
> - Instagram stories are in the queue (19:00 daily, media URL in the item). Desktop Instagram has no story upload:
>   if Chrome cannot post it, set it `manual`/`skipped`; the Telegram bot (promo.py) then sends the file to the owner's
>   private chat to post from his phone.
> - Queue restarted on 18 Oct with the same hour rotation (`content/rebuild_1017.py`, `content/patch_1017b.py`).
> - Media for the publisher: every queued reel/carousel has `override.media` (+ `override.cover`) pointing at copies in
>   this repo, because static.metricool.com is blocked from the task's container and the Chrome extension's
>   file_upload accepts at most 10 MB. All `youtube/shorts/fa_*.mp4` are re-encoded below 9.5 MB and are the same files
>   used for the Instagram reels. Captions still come from the Metricool post (`metricool_uuid`).
> - 13 Oct: Instagram web upload of a reel stalled at "processing" three times. If it stalls again, mark the item
>   `failed` with a note and tell the owner, so he can post that reel from his phone.

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
