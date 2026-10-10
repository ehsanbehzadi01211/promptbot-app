"""Content schedule -> owner's private chat.
  python schedule.py daily -> list of the next 7 days
  python schedule.py new   -> only items not announced before
content/schedule.json: [{"date":"2026-10-12","time":"10:00","platform":"instagram|youtube","kind":"reel|carousel|short|story","topic":"..."}]"""
import html, json, os, sys, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
TEHRAN = timezone(timedelta(hours=3, minutes=30))
ICON = {"instagram": "📷", "youtube": "▶️"}
KIND = {"reel": "ریل", "carousel": "پست اسلایدی", "short": "شورتس", "story": "استوری"}
DAYS = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه", "یکشنبه"]


def load(p, d):
    try:
        return json.load(open(p))
    except Exception:
        return d


def send(chat, text):
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    body = urllib.parse.urlencode({"chat_id": chat, "text": text, "parse_mode": "HTML",
                                   "disable_web_page_preview": "true"}).encode()
    urllib.request.urlopen(f"https://api.telegram.org/bot{token}/sendMessage", data=body, timeout=30)


def line(it):
    return f"{ICON.get(it['platform'], '•')} {it['time']} · {KIND.get(it['kind'], it['kind'])} · {html.escape(it['topic'])}"


def main(mode):
    chats = load(os.path.join(HERE, "state", "chats.json"), {})
    if not chats.get("owner"):
        print("owner chat unknown; send /start to the bot"); return
    items = sorted(load(os.path.join(HERE, "..", "content", "schedule.json"), []), key=lambda x: (x["date"], x["time"]))
    sent_path = os.path.join(HERE, "state", "sched_sent.json")
    sent = set(load(sent_path, []))
    key = lambda it: f"{it['date']} {it['time']} {it['platform']} {it['topic']}"
    now = datetime.now(TEHRAN)
    if mode == "daily":
        end = (now + timedelta(days=7)).strftime("%Y-%m-%d")
        today = now.strftime("%Y-%m-%d")
        upcoming = [it for it in items if today <= it["date"] <= end]
        out, last = ["🗓 <b>برنامه‌ی انتشار ۷ روز آینده</b>"], None
        for it in upcoming:
            if it["date"] != last:
                d = datetime.strptime(it["date"], "%Y-%m-%d")
                out.append(f"\n<b>{DAYS[d.weekday()]} {it['date']}</b>")
                last = it["date"]
            out.append(line(it))
        if not upcoming:
            out.append("هنوز چیزی برای این هفته زمان‌بندی نشده.")
        send(chats["owner"], "\n".join(out))
    new = [it for it in items if key(it) not in sent and it["date"] >= now.strftime("%Y-%m-%d")]
    if mode == "new" and new:
        send(chats["owner"], "🆕 <b>محتوای جدید زمان‌بندی شد</b>\n\n" + "\n".join(f"{it['date']} · {line(it)}" for it in new))
    sent |= {key(it) for it in items}
    json.dump(sorted(sent), open(sent_path, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
