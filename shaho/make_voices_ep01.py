# -*- coding: utf-8 -*-
"""
ساخت صدای دیالوگ‌های قسمت ۱ «شاهو، روباه شجاع» با Gemini TTS
طراح و تهیه‌کننده: ehbehzad

نصب (یک بار):
    pip install -U google-genai

اجرا در ویندوز (PowerShell):
    $env:GEMINI_API_KEY="کلید-API-خودت"
    python make_voices_ep01.py --test     # فقط ۴ جملهٔ تستی
    python make_voices_ep01.py            # کل قسمت ۱

خروجی: پوشهٔ voices_ep01 با یک فایل WAV برای هر دیالوگ، به ترتیب صحنه
(مثلاً 03_07_shaho.wav یعنی صحنهٔ ۳، دیالوگ ۷، شاهو) + فایل lines.csv
فایل‌هایی که قبلاً ساخته شده‌اند دوباره ساخته نمی‌شوند؛ برای ساخت دوباره، پاکشان کن.
"""
import argparse, csv, os, sys, time, wave

MODELS = ["gemini-2.5-flash-preview-tts", "gemini-2.5-flash-tts", "gemini-2.5-pro-preview-tts"]
OUT = os.environ.get("VOICES_OUT", "voices_ep01")

# صدای پایه و توصیف هر شخصیت. صداها را می‌توانی عوض کنی.
# فهرست صداها: Zephyr, Puck, Charon, Kore, Fenrir, Leda, Orus, Aoede, Callirrhoe, Autonoe,
# Enceladus, Iapetus, Umbriel, Algieba, Despina, Erinome, Algenib, Rasalgethi, Laomedeia,
# Achernar, Alnilam, Schedar, Gacrux, Pulcherrima, Achird, Zubenelgenubi, Sadachbia,
# Sadaltager, Sulafat, Vindemiatrix
CAST = {
    "shaho":   ("Puck",      "a brave, energetic 10-year-old boy fox, fast and a bit cocky, native Persian (Tehrani) accent"),
    "sanjar":  ("Charon",    "a big strong father, deep, calm and warm, speaks slowly with few words, native Persian accent"),
    "nasim":   ("Sulafat",   "a kind, playful mother, warm and smiling voice, native Persian accent"),
    "nokhodi": ("Leda",      "a cute 5-year-old little girl, high and giggly, native Persian accent"),
    "parpari": ("Zephyr",    "a chatty excited parrot, very fast, high-pitched, dramatic, native Persian accent"),
    "laki":    ("Enceladus", "a wise old-soul turtle, slow, calm, thoughtful, slightly drawn-out words, native Persian accent"),
    "vezvez":  ("Autonoe",   "a tiny timid bee, thin shaky voice, nervous, native Persian accent"),
    "abi":     ("Aoede",     "a playful mischievous axolotl, bubbly and laughing, native Persian accent"),
    "zangar":  ("Algenib",   "a greedy badger miner, low, slow, gravelly and a little menacing, native Persian accent"),
}

# (صحنه، شخصیت، حالت این جمله، متن)
LINES = [
 (0,"shaho","heroic, shouting like a movie hero","سبزدره آروم باش! شاهوی شجاع اینجاست! از هیچی نمی‌ترسه، نه از تاریکی، نه از هیولا، نه از…"),
 (0,"nokhodi","laughing, calling out","مامان! شاهوی شجاع بازم از یه پروانه شکست خورد!"),
 (0,"shaho","embarrassed, defensive","شکست نخوردم! داشتم… تمرین افتادن می‌کردم!"),
 (1,"nasim","smiling, teasing gently","صبح بخیر قهرمان. تمرینت چطور بود؟"),
 (1,"shaho","proud and eager","عالی! مامان، من دیگه بزرگ شدم. یه کار مهم بهم بدین."),
 (1,"nokhodi","excited, mouth full","فردا تولد منه! من کیک عسلی می‌خوام!"),
 (1,"nasim","warm","چشم خانم کوچولو. فقط عسلمون تموم شده. باید از تپهٔ زنبورها بیاریم."),
 (1,"shaho","jumping up, excited","من می‌رم! من می‌رم می‌آرم!"),
 (1,"sanjar","calm, not looking up","تپهٔ زنبورها اون طرف روده، شاهو. پل قدیمی رو بارون بهاری برد."),
 (1,"shaho","stubborn","خب… یه جوری می‌پرم اون طرف!"),
 (1,"sanjar","calm but firm","امروز آب تنده. من فردا صبح پل تازه رو می‌سازم، بعد با هم می‌ریم عسل می‌آریم. قبول؟"),
 (1,"shaho","frustrated, whiny","فردا؟! ولی کیک باید امشب پخته بشه! بابا، من دیگه بچه نیستم!"),
 (1,"sanjar","gentle, loving","می‌دونم پسرم. ولی پل خوب رو یه‌شبه نمی‌سازن. قول بده تنهایی نزدیک رود نمی‌ری."),
 (1,"shaho","mumbling, reluctant","باشه…"),
 (2,"parpari","very excited, shouting news","خبر داغ! خبر داغ! رود امروز مثل اژدها غرش می‌کنه! خودم دیدم یه کدوی به این گندگی رو یه لقمه کرد!"),
 (2,"laki","calm, correcting","کدو نبود، پرپری. یه برگ بود. ولی راست می‌گه، بعد از بارون آب دو برابر شده."),
 (2,"vezvez","scared, trembling","من که اصلاً از اینجا تکون نمی‌خورم…"),
 (2,"shaho","excited, like a leader","بچه‌ها، یه ماموریت مهم داریم! باید بریم تپهٔ زنبورها عسل بیاریم، برای کیک نخودی."),
 (2,"vezvez","worried, rambling","ولی… تپهٔ ما اون طرف روده! من هم که از آب می‌ترسم، تازه سه روزه هم اومدم این طرف مهمونی و برگشتم گیر افتاده…"),
 (2,"laki","suspicious","بابات چی گفت؟"),
 (2,"shaho","avoiding, then clever","گفت… گفت تنهایی نرم. خب ما که تنها نیستیم! چهار نفریم!"),
 (2,"parpari","cheerful","من میام! ولی از بالا نگاه می‌کنم، پرهام نباید خیس بشه!"),
 (2,"laki","sighing","کسی باید مراقب شماها باشه. من هم میام."),
 (3,"abi","playful, laughing","سلام خشکی‌نشین‌ها! شنا می‌کنین؟"),
 (3,"vezvez","squeaking","آییی! خیس شدم! بالم خیس شد!"),
 (3,"shaho","determined","آبی، می‌خوایم بریم اون طرف رود. از روی این سنگ‌ها و تنه‌ها."),
 (3,"abi","laugh stops, serious","از روی اونا؟ شاهو، اون تنه‌ها امروز هیچ‌کدومشون سر جاش بند نیست. زیر آب هم انگار یه غول داره هلشون می‌ده."),
 (3,"laki","calm, persuading","بیا برگردیم. فردا با بابات میایم."),
 (3,"shaho","brave, cocky","ترس؟ ترس دیگه چیه! شما همین‌جا بمونین، من می‌رم عسل می‌آرم."),
 (3,"shaho","proud, showing off","دیدین؟ راحته! من دیگه بزرگ…"),
 (3,"shaho","scared, voice trembling, almost whispering","چوب‌دستیم…"),
 (4,"laki","loud but calm","شاهو! تکون نخور! هرچی شد، از روی سنگ تکون نخور!"),
 (4,"parpari","panicking, very fast","چیکار کنیم؟ چیکار کنیم؟ آب داره بالا میاد!"),
 (4,"laki","firm, clear","پرپری، تو از همهٔ ما تندتری. پرواز کن برو بابا سنجر رو بیار. این دفعه همونی که دیدی رو بگو، نه ده برابرش رو!"),
 (4,"parpari","serious, focused","همونی که دیدم. فهمیدم!"),
 (4,"abi","soft, reassuring, not joking","من همین‌جام، باشه؟ نگاه آب نکن. نگاه من کن."),
 (4,"shaho","sad, quiet","آبی… من فقط می‌خواستم نشون بدم بزرگ شدم."),
 (4,"abi","kind, then a small smile","می‌دونم. ولی بزرگ‌ترها از روی تنهٔ لق نمی‌پرن. حتی من، که ماهی‌ام!"),
 (4,"shaho","small laugh through fear","تو که ماهی نیستی."),
 (4,"abi","whispering, playful","هیسس! به کسی نگو."),
 (4,"vezvez","trembling but trying to be brave","شاهو! من… من هم همین‌جام! خیلی هم نمی‌ترسم! فقط… یه کمی!"),
 (5,"sanjar","calm, steady, reassuring","شاهو، همون‌جا بمون. دارم میام."),
 (5,"shaho","quiet, ashamed","ببخشید بابا… قولم رو شکستم."),
 (5,"sanjar","after a pause, soft","ترسیدی؟"),
 (5,"shaho","quiet, honest","اوهوم."),
 (5,"sanjar","warm, approving","خوبه. یعنی عقلت کار می‌کنه."),
 (5,"shaho","surprised","خوبه؟"),
 (5,"sanjar","warm, inviting","حالا که پل هست، بریم عسل بیاریم؟ این دفعه تو جلو برو."),
 (6,"vezvez","proud and happy","بهترین عسل تپه، برای تولد نخودی! مامانم گفت این جایزهٔ منه، چون امروز نزدیک آب رفتم!"),
 (6,"shaho","sincere","وزوز، تو امروز از من شجاع‌تر بودی."),
 (6,"vezvez","shy, flustered","من؟ من که همه‌ش لرزیدم!"),
 (6,"sanjar","wise, gentle","همین که با لرزیدن هم اومدی، یعنی شجاعی."),
 (7,"nokhodi","teasing, giggling","شاهو، تو همون شاهوی شجاعی که از پروانه می‌ترسه؟"),
 (7,"nasim","warm, proud","بابات تعریف می‌کرد امروز چقدر شجاع بودی."),
 (7,"shaho","surprised","من؟ من که گیر افتادم!"),
 (7,"sanjar","slow, wise, warm","گیر افتادن شجاعت نمی‌خواد. اون لحظه‌ای شجاع بودی که به حرف لاکی گوش دادی، تکون نخوردی و منتظر کمک موندی. شجاعت یعنی بدونی کی بپری، و کی کمک بخوای."),
 (7,"shaho","thinking, then smiling","پس ترس… ترس یه چیزیه."),
 (7,"laki","calm, mouth full of cake","این بهترین جمله‌ای بود که تا حالا گفتی."),
 (7,"shaho","cheerful, all together","تولدت مبارک نخودی!"),
 (7,"zangar","low, slow, menacing, from the darkness","همم… سبزدره. زیر این همه چمن، چقدر الماس خوابیده؟"),
]

MODEL_USED = [None]

API = "https://generativelanguage.googleapis.com/v1beta"

def _keys():
    names = sorted(k for k, v in os.environ.items() if k.startswith("GEMINI_API_KEY") and v.strip())
    seen, out = set(), []
    for n in names:
        v = os.environ[n].strip()
        if v not in seen:
            seen.add(v); out.append((n, v))
    return out

KEYS = []
KEY_IDX = [0]

def _key():
    return KEYS[KEY_IDX[0]][1]

def _post(model, body):
    import json, urllib.request, urllib.error
    req = urllib.request.Request(f"{API}/models/{model}:generateContent",
        data=json.dumps(body).encode(), method="POST",
        headers={"Content-Type": "application/json", "x-goog-api-key": _key()})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{e.code} {e.read().decode()[:400]}")

def list_tts_models():
    import json, urllib.request
    req = urllib.request.Request(f"{API}/models?pageSize=200", headers={"x-goog-api-key": _key()})
    with urllib.request.urlopen(req, timeout=60) as r:
        ms = json.loads(r.read()).get("models", [])
    return [m["name"].split("/")[-1] for m in ms if "tts" in m["name"]]

def synth(client, voice, style, text):
    import base64
    prompt = f"Read the following Persian (Farsi) line aloud. Voice and acting: {style}\n\n{text}"
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    models = [MODEL_USED[0]] if MODEL_USED[0] else MODELS
    last = None
    for m in models:
        try:
            r = _post(m, body)
            part = r["candidates"][0]["content"]["parts"][0]["inlineData"]
            MODEL_USED[0] = m
            return base64.b64decode(part["data"]), part.get("mimeType", "")
        except Exception as e:
            last = e
            if MODEL_USED[0] or not any(k in str(e) for k in ("404", "NOT_FOUND", "not found", "not supported")):
                raise
    raise last

def save(path, data, mime):
    if data[:4] == b"RIFF":
        open(path, "wb").write(data); return
    rate = 24000
    if "rate=" in mime:
        try: rate = int(mime.split("rate=")[1].split(";")[0])
        except ValueError: pass
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(data)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true", help="فقط چند جملهٔ تستی")
    a = ap.parse_args()
    KEYS.extend(_keys())
    if not KEYS:
        sys.exit("کلید API را تنظیم کن:  $env:GEMINI_API_KEY=\"...\"")
    print("تعداد کلیدها:", len(KEYS), [n for n, _ in KEYS])
    client = None
    try:
        found = list_tts_models()
        print("مدل‌های TTS در دسترس:", found)
        global MODELS
        MODELS = [m for m in MODELS if m in found] + [m for m in found if m not in MODELS] or MODELS
    except Exception as e:
        print("فهرست مدل‌ها گرفته نشد:", e)
    os.makedirs(OUT, exist_ok=True)
    counter, rows = {}, []
    for scene, who, mood, text in LINES:
        counter[scene] = counter.get(scene, 0) + 1
        rows.append((f"{scene:02d}_{counter[scene]:02d}_{who}.wav", scene, who, mood, text))
    todo = [rows[i] for i in (0, 12, 16, 59)] if a.test else rows
    made, hits429, quota_done = 0, 0, False
    for i, (fname, scene, who, mood, text) in enumerate(todo, 1):
        path = os.path.join(OUT, fname)
        if os.path.exists(path):
            print(f"[{i}/{len(todo)}] {fname} قبلاً ساخته شده"); continue
        voice, base = CAST[who]
        style = f"{base}. Delivery: {mood}. Speak in natural spoken Persian (Farsi)."
        for attempt in range(4 + 2 * len(KEYS)):
            try:
                data, mime = synth(client, voice, style, text)
                save(path, data, mime)
                made += 1
                print(f"[{i}/{len(todo)}] {fname} ساخته شد ({MODEL_USED[0]})")
                break
            except Exception as e:
                if "429" in str(e):
                    hits429 += 1
                    if hits429 >= 2:
                        if KEY_IDX[0] + 1 < len(KEYS):
                            KEY_IDX[0] += 1
                            hits429 = 0
                            print(f"   سهمیهٔ این کلید تمام شد؛ رفتن به کلید بعدی ({KEYS[KEY_IDX[0]][0]})")
                            continue
                        print(f"   سهمیهٔ امروز همهٔ کلیدها تمام شد. {made} فایل ساخته شد؛ بقیه در اجرای بعدی.")
                        quota_done = True
                        break
                    print("   محدودیت سرعت؛ ۶۵ ثانیه صبر...")
                    time.sleep(65)
                    continue
                wait = 8 * (attempt + 1)
                print(f"   خطا در {fname}: {str(e)[:300]}  (تلاش دوباره تا {wait} ثانیه دیگر)")
                time.sleep(wait)
        else:
            print(f"   {fname} ساخته نشد، بعداً دوباره اجرا کن")
        if quota_done:
            break
        hits429 = 0
        time.sleep(7)
    with open(os.path.join(OUT, "lines.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["file", "scene", "character", "delivery", "text"]); w.writerows(rows)
    print(f"\nتمام. فایل‌ها در پوشهٔ {OUT}")

if __name__ == "__main__":
    main()
