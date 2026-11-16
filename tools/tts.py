# Free Microsoft neural TTS (edge-tts). tts.json: [{name, voice, rate, pitch, text}] -> media/<name>.mp3 (+ .words.json word timings)
import asyncio, json, os, edge_tts
async def one(it):
    out = f"media/{it['name']}.mp3"
    if os.path.exists(out): return
    c = edge_tts.Communicate(it['text'], it.get('voice', 'fa-IR-FaridNeural'), rate=it.get('rate', '+0%'), pitch=it.get('pitch', '+0Hz'), boundary='WordBoundary')
    words = []
    with open(out, 'wb') as f:
        async for ch in c.stream():
            if ch['type'] == 'audio': f.write(ch['data'])
            elif ch['type'] == 'WordBoundary': words.append({'w': ch['text'], 's': ch['offset'] / 1e7, 'e': (ch['offset'] + ch['duration']) / 1e7})
    json.dump(words, open(f"media/{it['name']}.words.json", 'w'), ensure_ascii=False)
    print(it['name'], len(words))
async def main():
    for it in json.load(open('tts.json')): await one(it)
asyncio.run(main())
