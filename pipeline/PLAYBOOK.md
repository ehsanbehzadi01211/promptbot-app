# @ehbehzad content system — one agent, three channels (since 11 Oct 2026, 22:30 Tehran)

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
     AI label on. Stories cannot be posted from desktop web: mark them `skipped`.
   - YouTube: studio.youtube.com → Create → Upload; English title/description/tags, not made for kids, category
     Education, altered/synthetic content = Yes, Public.
3. Write status `published` + the post URL (or `failed` + reason) into content/queue.json and push. The push makes the
   Telegram bot announce it in the channel (newsbot/promo.py).
4. If the Chrome tools are missing or a site asks for a login/2FA/captcha, do not improvise: tell the owner exactly which
   items are waiting.

## Telegram channel @ehbehzad_ai (GitHub Actions, newsbot/)
- AI news: every 2 hours, max 3 per run and 16 per day, Persian title + summary + source link.
- Announcement in the channel each time an Instagram post or YouTube Short goes live (promo.py, from queue.json).
- Owner's private chat: 7-day schedule every morning at 08:20 Tehran, plus a note whenever new items are queued.

## Production
- Daily task (05:47 Tehran, cloud): render the next two English Shorts that have no mp4 yet (encuts → stills → render_en.sh),
  push to youtube/shorts/. Instagram videos are paused by the owner ("no new Instagram videos for now").
- Weekly task (Thursday 18:47 Tehran, cloud): plan the following week — Instagram carousels (one per day), new English Shorts
  (specs + Liam voices + transcripts), append them to content/queue.json with times by the rotation, refresh schedule.json.
- Time test until 24 Oct (d = days since 11 Oct): IG reel {0:10,1:16,2:21}, IG carousel {0:21,1:10,2:16}, YT {0:16,1:21,2:10}.
  A one-time task on 24 Oct analyses it and moves later queue items to the winning hours.
