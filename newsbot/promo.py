"""Announce newly published Instagram/YouTube posts in the Telegram channel.
Reads content/queue.json (items the Chrome publisher marked status "published" with a "url") and posts each once.
  python newsbot/promo.py"""
import datetime as dt, html, json, os, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
QUEUE = os.path.join(HERE, "..", "content", "queue.json")
SENT = os.path.join(HERE, "state", "promo_sent.json")
STORY_SENT = os.path.join(HERE, "state", "stories_sent.json")
TEHRAN = dt.timezone(dt.timedelta(hours=3, minutes=30))
LABEL = {("instagram", "reel"): "📷 ریل جدید اینستاگرام", ("instagram", "carousel"): "📷 پست جدید اینستاگرام",
         ("instagram", "story"): None, ("youtube", "short"): "▶️ ویدیوی جدید یوتیوب"}


def load(p, d):
    try:
        return json.load(open(p))
    except Exception:
        return d


def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    channel = load(os.path.join(HERE, "state", "chats.json"), {}).get("channel")
    if not token or not channel:
        print("promo: no token/channel"); return
    sent = set(load(SENT, []))
    queue = load(QUEUE, [])
    # owner, 15 Nov 2026: only NEW VIDEOS, and ONE message per video. Instagram + YouTube of the same video go out
    # at the same moment (same uplika_post), so both links go into a single message.
    now = dt.datetime.now(TEHRAN).replace(tzinfo=None)
    groups = {}
    for it in queue:
        if (it.get("platform"), it.get("kind")) not in (("instagram", "reel"), ("youtube", "short")):
            continue
        g = it.get("uplika_post") or it["id"]
        groups.setdefault(g, []).append(it)
    for g, items in groups.items():
        pub = [it for it in items if it.get("status") == "published" and it.get("url")]
        if not pub:
            continue
        if any(it["id"] in sent for it in items):  # this video was already announced once
            sent.update(it["id"] for it in pub)
            continue
        try:  # old items (before today) are only marked, never announced late
            old = dt.datetime.fromisoformat(items[0]["when"]) < now - dt.timedelta(days=2)
        except Exception:
            old = False
        if not old:
            links = "\n".join(("📷 اینستاگرام: " if it["platform"] == "instagram" else "▶️ یوتیوب: ") + html.escape(it["url"])
                              for it in sorted(pub, key=lambda x: x["platform"]))
            text = f"🎬 ویدیوی جدید\n\n<b>{html.escape(items[0].get('topic', ''))}</b>\n\n{links}\n\n@ehbehzad_ai"
            body = urllib.parse.urlencode({"chat_id": channel, "text": text, "parse_mode": "HTML"}).encode()
            try:
                urllib.request.urlopen(f"https://api.telegram.org/bot{token}/sendMessage", data=body, timeout=30)
                print("promo sent", g)
            except Exception as ex:
                print("promo fail", g, ex); continue
        for it in pub:
            sent.add(it["id"])
    json.dump(sorted(sent), open(SENT, "w"), indent=1)
    stories(token, load(os.path.join(HERE, "state", "chats.json"), {}).get("owner"))


def stories(token, owner):
    """Instagram stories cannot be posted from desktop Chrome: once a story's time has come and the Chrome publisher
    has not published it, send the file to the owner's private chat so he can post it from his phone in one tap."""
    if not owner:
        return
    done = set(load(STORY_SENT, []))
    now = dt.datetime.now(TEHRAN).replace(tzinfo=None)
    for it in load(QUEUE, []):
        if it.get("kind") != "story" or it["id"] in done or it.get("status") not in ("queued", "manual", "skipped"):
            continue
        if it.get("status") == "skipped" and "replaced" in it.get("note", ""):
            continue
        t = dt.datetime.fromisoformat(it["when"])
        if not (t <= now <= t + dt.timedelta(hours=20)):
            continue
        url = (it.get("media") or [None])[0]
        if not url:
            continue
        cap = (f"📲 <b>استوری امروز اینستاگرام</b> ({it['when'][11:]})\n{html.escape(it['topic'])}\n\n"
               "این فایل رو از گوشی به‌عنوان استوری بذار (برچسب AI رو روشن کن).")
        method, field = ("sendVideo", "video") if url.endswith(".mp4") else ("sendPhoto", "photo")
        body = urllib.parse.urlencode({"chat_id": owner, field: url, "caption": cap, "parse_mode": "HTML"}).encode()
        try:
            urllib.request.urlopen(f"https://api.telegram.org/bot{token}/{method}", data=body, timeout=60)
            print("story sent to owner", it["id"])
            done.add(it["id"])
        except Exception as ex:
            print("story fail", it["id"], ex)
    json.dump(sorted(done), open(STORY_SENT, "w"), indent=1)


if __name__ == "__main__":
    main()
