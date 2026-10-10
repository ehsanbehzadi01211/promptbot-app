"""Find the channel the bot administers and the owner's private chat from getUpdates; store in state/chats.json.
The owner only needs to send /start to the bot once, and the channel is found from any post or the admin event."""
import json, os, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(HERE, "state", "chats.json")
chats = json.load(open(path)) if os.path.exists(path) else {}
token = os.environ["TELEGRAM_BOT_TOKEN"]
data = json.loads(urllib.request.urlopen(f"https://api.telegram.org/bot{token}/getUpdates?allowed_updates=%5B%22message%22%2C%22channel_post%22%2C%22my_chat_member%22%5D", timeout=30).read())
for u in data.get("result", []):
    for key in ("message", "channel_post", "my_chat_member"):
        chat = (u.get(key) or {}).get("chat")
        if not chat:
            continue
        if chat["type"] == "channel" and "channel" not in chats:
            chats["channel"] = chat["id"]; chats["channel_title"] = chat.get("title")
        if chat["type"] == "private" and "owner" not in chats:
            chats["owner"] = chat["id"]
if os.environ.get("CHANNEL") and "channel" not in chats:   # e.g. @mychannel
    chats["channel"] = os.environ["CHANNEL"]
os.makedirs(os.path.dirname(path), exist_ok=True)
json.dump(chats, open(path, "w"), ensure_ascii=False, indent=1)
print({k: ("set" if v else "") for k, v in chats.items()})
