"""17 Oct (b): facts from the 12–13 Oct publisher runs + repo media copies the Chrome publisher can upload
(static.metricool.com is blocked from its container; Chrome file_upload limit 10 MB)."""
import json, datetime as dt
RAW = "https://raw.githubusercontent.com/ehsanbehzadi01211/promptbot-app/reels-media/"
q = json.load(open("content/queue.json"))
COVER = {"fa_claude_ws": "reels11/news_claude_ws_cover.jpg", "fa_insta": "covers2/cover_web1_page.jpg",
         "fa_speed": "covers2/cover_web2_speed.jpg"}
for k, r in {"imgprompt": 19, "edit": 20, "sketch": 21, "video": 22, "vprompt": 23, "img2vid": 24, "teacher": 7,
             "photo": 8, "tasks": 9, "interview": 10, "english": 11, "phrases": 12, "dont": 13, "caption": 14,
             "decide": 15, "resume": 16, "skill": 17, "no": 18}.items():
    COVER["fa_" + k] = f"covers2/cover_reel{r}_{k}.jpg"
CAR = {"۶ کانال یوتیوب آموزش AI": ("c5_channels", 5), "۵ اشتباه با هوش مصنوعی": ("c6_mistakes", 4),
       "پرامپت مخصوص هر شغل": ("c7_jobs", 5), "چک‌لیست ۶ مورد سایت (طراحی سایت)": ("c8_website", 4),
       "GPT-6 برای همه + ۶ پرامپت": ("c1_gpt6", 6), "۶ ابزار رایگان هوش مصنوعی": ("c2_tools", 5)}
hist = [x for x in q if x["status"] != "queued"]
live = [x for x in q if x["status"] == "queued"]
# facts reported by the 13 Oct publisher run (project doc claude/pending-queue-updates.md)
for x in hist:
    if x["id"] == "yo-2026-10-12-short":
        x.update(status="published", url="https://youtube.com/shorts/PpXLYBofJUM", note="English; went live 11 Oct")
    if x["id"] == "yo-2026-10-13-short":
        x.update(status="published", url="https://youtube.com/shorts/enrBVCh3tYQ", note="English; went live 12 Oct")
eight = [x for x in live if x["kind"] == "carousel" and x["topic"].startswith("۸ پرامپت")][0]
live.remove(eight)
hist.append({**eight, "when": "2026-10-12T19:00", "status": "published", "url": "https://www.instagram.com/p/DeZj43iiOTh/",
             "id": "in-2026-10-12-carousel", "note": "published by the Chrome publisher on 12 Oct"})
# carousels move up one day each (same hour rotation)
BASE = dt.date(2026, 10, 11); HC = {0: "21:00", 1: "10:00", 2: "16:00"}
cars = sorted([x for x in live if x["kind"] == "carousel"], key=lambda x: x["when"])
for i, x in enumerate(cars):
    d = dt.date(2026, 10, 18) + dt.timedelta(days=i)
    x["when"] = f"{d}T{HC[(d - BASE).days % 3]}"; x["id"] = f"in-{d}-carousel"
    c, n = CAR[x["topic"]]
    x["override"] = {"media": [f"{RAW}carousels/{c}/{j:02d}.jpg" for j in range(1, n + 1)]}
# reels: same order as the Persian YouTube keys
yks = [x["key"] for x in sorted([x for x in live if x["platform"] == "youtube"], key=lambda x: x["when"])]
reels = sorted([x for x in live if x["kind"] == "reel"], key=lambda x: x["when"])
for x, k in zip(reels, yks):
    x["yt_key"] = k
    x["override"] = {"media": [f"{RAW}youtube/shorts/{k}.mp4"], "cover": RAW + COVER[k]}
live.sort(key=lambda x: (x["when"], x["platform"]))
json.dump(hist + live, open("content/queue.json", "w"), ensure_ascii=False, indent=1)
json.dump([{"date": x["when"][:10], "time": x["when"][11:], "platform": x["platform"], "kind": x["kind"], "topic": x["topic"]}
           for x in live], open("content/schedule.json", "w"), ensure_ascii=False, indent=1)
ps = "newsbot/state/promo_sent.json"
s = set(json.load(open(ps))) | {"yo-2026-10-12-short", "yo-2026-10-13-short", "in-2026-10-12-carousel"}
json.dump(sorted(s), open(ps, "w"), indent=1)
print(len(live), "queued")
for x in live:
    if x["kind"] in ("reel", "carousel"): print(x["when"], x["kind"], x.get("yt_key", ""), x["topic"][:30])
