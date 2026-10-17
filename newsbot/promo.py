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
    for it in load(QUEUE, []):
        if it.get("status") != "published" or not it.get("url") or it["id"] in sent:
            continue
        label = LABEL.get((it["platform"], it["kind"]), "🆕 پست جدید")
        if label:
            text = f"{label}\n\n<b>{html.escape(it['topic'])}</b>\n\n🔗 {html.escape(it['url'])}\n\n#هوش_مصنوعی @ehbehzad_ai"
            body = urllib.parse.urlencode({"chat_id": channel, "text": text, "parse_mode": "HTML"}).encode()
            try:
                urllib.request.urlopen(f"https://api.telegram.org/bot{token}/sendMessage", data=body, timeout=30)
                print("promo sent", it["id"])
            except Exception as ex:
                print("promo fail", it["id"], ex); continue
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
