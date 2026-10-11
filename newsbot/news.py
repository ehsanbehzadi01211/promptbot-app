"""AI news engine.
  python news.py fetch   -> pull feeds, drop old/duplicate items, add Persian title+summary,
                            append to data/YYYY-MM-DD.json and to state/queue.json
  python news.py post    -> send up to N queued items to the Telegram channel
Env: TELEGRAM_BOT_TOKEN, and the channel id in state/chats.json (filled by discover.py)."""
import hashlib, html, json, os, re, sys, time, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

import feedparser

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "state")
DATA = os.path.join(HERE, "data")
UA = "Mozilla/5.0 (compatible; ai-news-bot/1.0)"
CFG = json.load(open(os.path.join(HERE, "sources.json")))
TRUSTED = {s.lower() for s in CFG["trusted_publishers"]}
NOW = datetime.now(timezone.utc)
MAX_AGE = timedelta(hours=36)


def jload(path, default):
    try:
        return json.load(open(path))
    except Exception:
        return default


def jsave(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(obj, open(path, "w"), ensure_ascii=False, indent=1)


def get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def clean(text, n=None):
    text = html.unescape(re.sub(r"<[^>]+>", " ", text or ""))
    text = re.sub(r"\s+", " ", text).strip()
    if n and len(text) > n:
        text = text[:n].rsplit(" ", 1)[0] + "…"
    return text


def words(title):
    return set(w for w in re.findall(r"[a-z0-9]+", title.lower()) if len(w) > 2)


def similar(a, b):
    wa, wb = words(a), words(b)
    if not wa or not wb:
        return False
    return len(wa & wb) / len(wa | wb) > 0.55


def entry_time(e):
    for k in ("published_parsed", "updated_parsed"):
        if e.get(k):
            return datetime.fromtimestamp(time.mktime(e[k]), timezone.utc)
    return None


def from_feed(src):
    out = []
    try:
        feed = feedparser.parse(get(src["url"]))
    except Exception as ex:
        print("feed fail", src["name"], ex)
        return out
    for e in feed.entries[:30]:
        t = entry_time(e)
        if t and NOW - t > MAX_AGE:
            continue
        title = clean(e.get("title"))
        source = src["name"]
        if src.get("gnews"):  # "Headline - Publisher"
            m = re.match(r"(.*) - ([^-]+)$", title)
            if m:
                title, source = m.group(1).strip(), m.group(2).strip()
        out.append({"title": title, "summary": clean(e.get("summary"), 400), "url": e.get("link"),
                    "source": source, "official": src.get("official", False), "tools": src.get("tools", False),
                    "gnews": bool(src.get("gnews")), "time": (t or NOW).isoformat()})
    print(f"{src['name']}: {len(out)} fresh")
    return out


def from_page(src):
    """Sites without RSS (Anthropic): new article links on the news page are 'fresh' the first time we see them."""
    out = []
    try:
        page = get(src["url"]).decode("utf-8", "ignore")
    except Exception as ex:
        print("page fail", src["name"], ex)
        return out
    seen = set()
    for href, inner in re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', page, flags=re.S):
        path = href.replace(src["base"], "")
        if not re.match(src["pattern"], path) or path in seen:
            continue
        seen.add(path)
        title = clean(inner, 160)
        if len(title) < 12:
            title = path.rsplit("/", 1)[-1].replace("-", " ").capitalize()
        out.append({"title": title, "summary": "", "url": src["base"] + path, "source": src["name"],
                    "official": True, "tools": False, "time": NOW.isoformat(), "page": True})
    print(f"{src['name']}: {len(out)} links")
    return out[:15]


def _first_str(x):
    if isinstance(x, str):
        return x
    if isinstance(x, list):
        for y in x:
            s = _first_str(y)
            if s:
                return s
    return ""


def _gtx(text):
    q = urllib.parse.urlencode({"client": "gtx", "sl": "auto", "tl": "fa", "dt": "t", "q": text})
    data = json.loads(get("https://translate.googleapis.com/translate_a/single?" + q))
    return "".join(part[0] for part in data[0] if part[0])


def _clients5(text):
    q = urllib.parse.urlencode({"client": "dict-chrome-ex", "sl": "auto", "tl": "fa", "q": text})
    return _first_str(json.loads(get("https://clients5.google.com/translate_a/t?" + q)))


def _mymemory(text):
    q = urllib.parse.urlencode({"q": text[:480], "langpair": "en|fa"})
    data = json.loads(get("https://api.mymemory.translated.net/get?" + q))
    out = (data.get("responseData") or {}).get("translatedText") or ""
    return "" if "MYMEMORY WARNING" in out.upper() or data.get("responseStatus") not in (200, "200") else out


def translate(text):
    """Free endpoints are rate-limited per IP on shared runners, so try three in turn."""
    if not text:
        return ""
    for name, fn in (("gtx", _gtx), ("clients5", _clients5), ("mymemory", _mymemory)):
        try:
            out = html.unescape(fn(text)).strip()
            if out and re.search(r"[\u0600-\u06FF]", out):
                print("translated via", name)
                return out
            print("translate empty", name)
        except Exception as ex:
            print("translate fail", name, ex)
        time.sleep(2)
    return ""


def item_id(it):
    return hashlib.sha1((it["url"] or it["title"]).encode()).hexdigest()[:16]


def relevant(it):
    """Official sources always pass. Everything else must be about AI, read like a launch/update,
    come from a known publisher (Google News results) and not be finance/PR noise."""
    if it["official"]:
        return True
    t = " " + it["title"].lower() + " "
    if any(w in t for w in CFG["block_words"]):
        return False
    if not any(re.search(r"(?<![a-z0-9])" + re.escape(w) + r"(?![a-z0-9])", t) for w in CFG["ai_words"]):
        return False
    if it.get("gnews") and it["source"].lower() not in TRUSTED:
        return False
    return score(it) > 0


def score(it):
    s = 3 if it["official"] else 0
    t = it["title"].lower()
    s += sum(1 for w in CFG["launch_words"] if w in t)
    return s


def fetch():
    seen = jload(os.path.join(STATE, "seen.json"), {})
    first_run = not seen
    items = []
    for src in CFG["feeds"]:
        items += from_feed(src)
    for src in CFG["pages"]:
        items += from_page(src)
    for q in CFG["google_news"]:
        url = "https://news.google.com/rss/search?" + urllib.parse.urlencode(
            {"q": q + " when:1d", "hl": "en-US", "gl": "US", "ceid": "US:en"})
        items += from_feed({"name": "Google News", "url": url, "gnews": True})

    recent = jload(os.path.join(STATE, "recent_titles.json"), [])
    fresh = []
    for it in sorted(items, key=score, reverse=True):
        iid = item_id(it)
        if iid in seen:
            continue
        seen[iid] = NOW.isoformat()
        if any(similar(it["title"], r) for r in recent + [f["title"] for f in fresh]):
            continue
        if not relevant(it):
            continue
        it["id"] = iid
        fresh.append(it)
    fresh = fresh[:CFG["max_new_per_fetch"]]
    # first run only records what exists, so the channel isn't flooded with old posts
    if first_run:
        fresh = [it for it in fresh if not it.get("page")][:6]
    # Persian text is added in post(), a few items per run, so the translate endpoint is not hammered
    # forget ids older than 10 days
    cutoff = (NOW - timedelta(days=10)).isoformat()
    seen = {k: v for k, v in seen.items() if v > cutoff}
    jsave(os.path.join(STATE, "seen.json"), seen)
    jsave(os.path.join(STATE, "recent_titles.json"), (recent + [f["title"] for f in fresh])[-300:])
    day = os.path.join(DATA, NOW.strftime("%Y-%m-%d") + ".json")
    jsave(day, jload(day, []) + fresh)
    queue = jload(os.path.join(STATE, "queue.json"), [])
    jsave(os.path.join(STATE, "queue.json"), (queue + fresh)[-60:])
    print(f"new items: {len(fresh)}")


TAGS = {"OpenAI": "#OpenAI", "Anthropic": "#Claude", "Google": "#Gemini", "Google DeepMind": "#DeepMind",
        "Microsoft": "#Microsoft", "NVIDIA": "#NVIDIA", "Hugging Face": "#HuggingFace", "Product Hunt": "#ابزار_جدید"}


def tg(method, **params):
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    body = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/{method}", data=body)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def fmt(it):
    title = it.get("title_fa") or it["title"]
    lines = [f"🆕 <b>{html.escape(title)}</b>"]
    if it.get("summary_fa"):
        lines.append(html.escape(clean(it["summary_fa"], 350)))
    lines.append(f"<i>{html.escape(it['title'])}</i>")
    tag = TAGS.get(it["source"], "")
    lines.append(f"🔗 <a href=\"{html.escape(it['url'])}\">منبع: {html.escape(it['source'])}</a>")
    lines.append(" ".join(x for x in ["#هوش_مصنوعی", tag, "#خبر"] if x))
    return "\n\n".join(lines)


def post():
    chats = jload(os.path.join(STATE, "chats.json"), {})
    channel = chats.get("channel")
    if not channel or not os.environ.get("TELEGRAM_BOT_TOKEN"):
        print("no channel or token yet; skipping post")
        return
    queue = jload(os.path.join(STATE, "queue.json"), [])
    stale = (NOW - timedelta(hours=CFG["max_queue_age_hours"])).isoformat()
    queue = [it for it in queue if it["time"] > stale and relevant(it)]
    log = jload(os.path.join(STATE, "posted.json"), {})
    today = NOW.strftime("%Y-%m-%d")
    done_today = log.get(today, 0)
    room = min(CFG["max_posts_per_run"], CFG["max_posts_per_day"] - done_today)
    sent = 0
    while queue and sent < room:
        it = queue[0]
        if not it.get("title_fa"):
            it["title_fa"] = translate(it["title"])
            time.sleep(1.5)
            it["summary_fa"] = translate(it["summary"])
        if not it["title_fa"]:   # the channel is Persian: never post an untranslated headline
            print("no translation; will retry next run")
            break
        queue.pop(0)
        try:
            r = tg("sendMessage", chat_id=channel, text=fmt(it), parse_mode="HTML",
                   disable_web_page_preview="false")
            print("sent", r.get("ok"), it["title"][:60])
            sent += 1
        except Exception as ex:
            print("send fail", ex)
        time.sleep(3)
    log[today] = done_today + sent
    jsave(os.path.join(STATE, "posted.json"), dict(list(log.items())[-14:]))
    jsave(os.path.join(STATE, "queue.json"), queue)


if __name__ == "__main__":
    {"fetch": fetch, "post": post}[sys.argv[1]]()
