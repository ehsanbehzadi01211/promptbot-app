"""Announce newly published Instagram/YouTube posts in the Telegram channel.
Reads content/queue.json (items the Chrome publisher marked status "published" with a "url") and posts each once.
  python newsbot/promo.py"""
import html, json, os, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
QUEUE = os.path.join(HERE, "..", "content", "queue.json")
SENT = os.path.join(HERE, "state", "promo_sent.json")
LABEL = {("instagram", "reel"): "📷 ریل جدید اینستاگرام", ("instagram", "carousel"): "📷 پست جدید اینستاگرام",
         ("instagram", "story"): None, ("youtube", "short"): "▶️ ویدیوی جدید یوتیوب (انگلیسی)"}


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


if __name__ == "__main__":
    main()
