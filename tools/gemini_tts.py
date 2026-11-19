# Gemini TTS. gemini_tts.json: [{name, model?, voice? | speakers:[{speaker,voice}], lines:[{speaker?, text, style?}]}]
# -> media/gtts/<name>.wav ; errors -> media/gtts/<name>.err.txt. Never prints the key.
import base64, json, os, re, struct, requests
KEY = os.environ.get('GEMINI_API_KEY', '')
os.makedirs('media/gtts', exist_ok=True)
H = {'x-goog-api-key': KEY, 'content-type': 'application/json'}
def find_audio(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ('data', 'audio', 'inline_data', 'inlineData') and isinstance(v, str) and len(v) > 2000: return v
            r = find_audio(v)
            if r: return r
    elif isinstance(o, list):
        for v in o:
            r = find_audio(v)
            if r: return r
def strip(o):
    if isinstance(o, dict): return {k: (f'<{len(v)} chars>' if isinstance(v, str) and len(v) > 300 else strip(v)) for k, v in o.items()}
    if isinstance(o, list): return [strip(v) for v in o]
    return o
def wav(pcm, sr=24000):
    return b'RIFF' + struct.pack('<I', 36 + len(pcm)) + b'WAVEfmt ' + struct.pack('<IHHIIHH', 16, 1, 1, sr, sr * 2, 2, 16) + b'data' + struct.pack('<I', len(pcm)) + pcm
def interactions(it, model):
    content = [{'type': 'text', 'text': l['text'], 'annotations': [dict({'type': 'speech_metadata'}, **({'speaker': l['speaker']} if 'speaker' in l else {}), **({'style': l['style']} if 'style' in l else {}))]} for l in it['lines']]
    sc = {'speakers': it['speakers']} if 'speakers' in it else [{'voice': it['voice']}]
    body = {'model': model, 'input': [{'type': 'user_input', 'content': content}], 'response_format': {'type': 'audio', 'mime_type': 'audio/wav'}, 'generation_config': {'speech_config': sc}}
    return requests.post('https://generativelanguage.googleapis.com/v1beta/interactions', headers=H, json=body, timeout=300)
def classic(it, model):
    if 'speakers' in it:
        text = '\n'.join(f"{l['speaker']}: {l['text']}" for l in it['lines']); style = it.get('style', '')
        sc = {'multiSpeakerVoiceConfig': {'speakerVoiceConfigs': [{'speaker': s['speaker'], 'voiceConfig': {'prebuiltVoiceConfig': {'voiceName': s['voice']}}} for s in it['speakers']]}}
    else:
        text = ' '.join(l['text'] for l in it['lines']); style = it['lines'][0].get('style', '')
        sc = {'voiceConfig': {'prebuiltVoiceConfig': {'voiceName': it['voice']}}}
    if style: text = style + ':\n' + text
    body = {'contents': [{'parts': [{'text': text}]}], 'generationConfig': {'responseModalities': ['AUDIO'], 'speechConfig': sc}}
    return requests.post(f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent', headers=H, json=body, timeout=300)
for it in json.load(open('gemini_tts.json')):
    out = f"media/gtts/{it['name']}.wav"
    if os.path.exists(out): continue
    log = []
    m = it.get('model', 'gemini-3.8-flash-tts')
    order = [('classic', m), ('interactions', m)] if 'speakers' in it else [('interactions', m), ('classic', m)]
    if not it.get('no_fallback'): order.append(('classic', 'gemini-2.5-flash-preview-tts'))
    for how, model in order:
        r = (interactions if how == 'interactions' else classic)(it, model)
        try: j = r.json()
        except Exception: j = {'raw': r.text[:500]}
        a = find_audio(j)
        if r.ok and a:
            b = base64.b64decode(a)
            open(out, 'wb').write(b if b[:4] == b'RIFF' else wav(b)); print(it['name'], how, model, len(b))
            if log: open(f"media/gtts/{it['name']}.log.txt", 'w').write('\n\n'.join(log))
            break
        log.append(f'{how} {model} HTTP {r.status_code}: ' + json.dumps(strip(j), ensure_ascii=False)[:1500])
    else:
        open(f"media/gtts/{it['name']}.err.txt", 'w').write('\n\n'.join(log)); print(it['name'], 'FAILED')
