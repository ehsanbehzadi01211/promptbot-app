"""17 Oct 2026 rebuild: English YouTube cancelled; Persian reels go to Instagram AND YouTube; stories scheduled.
Everything restarts on 18 Oct with the same hour rotation (d = days since 11 Oct)."""
import json, datetime as dt
Q = "content/queue.json"
old = json.load(open(Q))
byid = {it["id"]: it for it in old}
ig = lambda i: (byid[i]["metricool_uuid"], byid[i]["metricool_date"], byid[i]["topic"])
REELS = [  # (ig uuid, ig metricool date, topic, override, youtube key)
 ("-661815568252124700", "2026-10-11T10:00", "خبر: Claude در گوگل داکس، شیت و اسلاید", byid["in-2026-10-30-reel"]["override"], "fa_claude_ws"),
 (*ig("in-2026-10-12-reel"), None, "fa_imgprompt"),
 (*ig("in-2026-10-13-reel"), None, "fa_edit"),
 (*ig("in-2026-10-14-reel"), None, "fa_sketch"),
 (*ig("in-2026-10-15-reel"), None, "fa_video"),
 (*ig("in-2026-10-16-reel"), None, "fa_vprompt"),
 ("-415557555638812148", "2026-10-09T10:00", "پیج اینستاگرامت مال تو نیست (طراحی سایت)", None, "fa_insta"),
 (*ig("in-2026-10-17-reel"), None, "fa_img2vid"),
 (*ig("in-2026-10-18-reel"), None, "fa_teacher"),
 (*ig("in-2026-10-19-reel"), None, "fa_photo"),
 (*ig("in-2026-10-20-reel"), None, "fa_tasks"),
 (*ig("in-2026-10-21-reel"), None, "fa_interview"),
 ("-6564507812620778913", "2026-10-10T10:00", "سایت کند یعنی مشتری رفته (طراحی سایت)", None, "fa_speed"),
 (*ig("in-2026-10-22-reel"), None, "fa_english"),
 (*ig("in-2026-10-23-reel"), None, "fa_phrases"),
 (*ig("in-2026-10-24-reel"), None, "fa_dont"),
 (*ig("in-2026-10-25-reel"), None, "fa_caption"),
 (*ig("in-2026-10-26-reel"), None, "fa_decide"),
 (*ig("in-2026-10-27-reel"), None, "fa_resume"),
 (*ig("in-2026-10-28-reel"), None, "fa_skill"),
 (*ig("in-2026-10-29-reel"), None, "fa_no"),
]
YT_EXTRA = [("fa_mistakes", "۳ اشتباه رایج با هوش مصنوعی"), ("fa_rewrite", "پرامپتی که هر متنی رو حرفه‌ای می‌کنه"),
            ("fa_aijob", "هوش مصنوعی شغلت رو می‌گیره؟")]
CAROUSELS = ["in-2026-10-12-carousel", "in-2026-10-14-carousel", "in-2026-10-15-carousel", "in-2026-10-16-carousel",
             "in-2026-10-17-carousel", "in-2026-10-18-carousel", "in-2026-10-19-carousel"]
RAW = "https://raw.githubusercontent.com/ehsanbehzadi01211/promptbot-app/reels-media/stories/"
STORIES = [("tip_1.jpg", "نکته‌ی روز: به جواب اول اعتماد نکن"), ("st_suno.mp4", "ابزار رایگان: Suno"),
           ("tip_2.jpg", "نکته‌ی روز: هر چیز سخت رو ساده بخواه"), ("st_notebook.mp4", "ابزار رایگان: Gemini Notebook"),
           ("tip_3.jpg", "نکته‌ی روز: متن طولانی؟ ۳ خط بخواه"), ("st_perplexity.mp4", "ابزار رایگان: Perplexity"),
           ("tip_4.jpg", "نکته‌ی روز: بین چند گزینه؟ جدول بخواه"), ("st_gamma.mp4", "ابزار رایگان: Gamma"),
           ("tip_5.jpg", "نکته‌ی روز: لحن پیامت رو چک کن"), ("st_napkin.mp4", "ابزار رایگان: Napkin"),
           ("tip_6.jpg", "نکته‌ی روز: کار بزرگ؟ چک‌لیست بخواه"), ("st_turboscribe.mp4", "ابزار رایگان: TurboScribe")]
START, BASE = dt.date(2026, 10, 18), dt.date(2026, 10, 11)
H = {"reel": {0: "10:00", 1: "16:00", 2: "21:00"}, "carousel": {0: "21:00", 1: "10:00", 2: "16:00"},
     "short": {0: "16:00", 1: "21:00", 2: "10:00"}}
def when(kind, i):
    d = START + dt.timedelta(days=i)
    return d, f"{d.isoformat()}T{H[kind][(d - BASE).days % 3]}"
sc = json.load(open("pipeline/scripts_en.json"))
new = []
for i, (u, md, topic, ov, yk) in enumerate(REELS):
    d, w = when("reel", i)
    it = {"platform": "instagram", "kind": "reel", "when": w, "topic": topic, "metricool_uuid": u, "metricool_date": md,
          "status": "queued", "id": f"in-{d}-reel"}
    if ov: it["override"] = ov
    new.append(it)
yks = [(r[4], r[2]) for r in REELS] + YT_EXTRA
for i, (k, topic) in enumerate(yks):
    d, w = when("short", i)
    new.append({"platform": "youtube", "kind": "short", "lang": "fa", "when": w, "topic": sc[k]["title"].replace(" #Shorts", ""),
                "key": k, "media": f"youtube/shorts/{k}.mp4", "metricool_uuid": sc[k]["metricool_uuid"],
                "metricool_date": sc[k]["metricool_date"], "status": "queued", "id": f"yo-{d}-short"})
for i, cid in enumerate(CAROUSELS):
    d, w = when("carousel", i)
    o = byid[cid]
    new.append({"platform": "instagram", "kind": "carousel", "when": w, "topic": o["topic"], "metricool_uuid": o["metricool_uuid"],
                "metricool_date": o["metricool_date"], "status": "queued", "id": f"in-{d}-carousel"})
for i, (f, topic) in enumerate(STORIES):
    d = START + dt.timedelta(days=i)
    new.append({"platform": "instagram", "kind": "story", "when": f"{d}T19:00", "topic": topic, "media": [RAW + f],
                "status": "queued", "id": f"in-{d}-story",
                "note": "Story: media URL above (no Metricool post). Desktop Instagram may not offer stories; if not, set status 'manual' (or 'skipped') and the Telegram bot sends the file to the owner's phone."})
hist = []
for it in old:
    if it["platform"] == "youtube":
        hist.append({**it, "status": "cancelled", "note": "English YouTube Shorts cancelled by the owner on 17 Oct 2026"})
    elif it["id"] == "in-2026-10-13-carousel":
        hist.append({**it, "status": "skipped", "note": "weekly news roundup of 11 Oct is stale; not posted (17 Oct)"})
    elif it["id"] == "in-2026-10-12-story":
        hist.append({**it, "status": "skipped", "note": "replaced by the new story plan of 17 Oct"})
new.sort(key=lambda x: (x["when"], x["platform"]))
json.dump(hist + new, open(Q, "w"), ensure_ascii=False, indent=1)
sched = [{"date": x["when"][:10], "time": x["when"][11:], "platform": x["platform"], "kind": x["kind"], "topic": x["topic"]}
         for x in new]
json.dump(sched, open("content/schedule.json", "w"), ensure_ascii=False, indent=1)
print(len(new), "queued;", len(hist), "history")
for x in new: print(x["when"], x["platform"][:2], x["kind"], x["topic"][:45])
