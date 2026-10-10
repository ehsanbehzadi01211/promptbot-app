"""Rebuild reels using an external (ElevenLabs) voiceover, timing scenes to its pauses."""
import json, os, subprocess, sys, wave
import numpy as np
from playwright.sync_api import sync_playwright
import build as B
from align import boundaries

ROOT = os.path.dirname(os.path.abspath(__file__))
LEAD, TAIL = 0.25, 0.8

def run(key, voice_mp3):
    spec = json.load(open(os.path.join(ROOT, "scripts.json")))[key]
    bounds, s0, s1, vdur = boundaries(voice_mp3, [sc["voice"] for sc in spec["scenes"]])
    total = LEAD + vdur + TAIL
    starts = [0.0] + [LEAD + b for b in bounds]
    ends = starts[1:] + [total]
    work = os.path.join(ROOT, "out", key + "_el"); os.makedirs(work, exist_ok=True)
    B.music(total, os.path.join(work, "music.wav"), seed=len(key))
    scenes = "".join(B.scene_html(sc, st, en - st, spec["accent"]) for sc, st, en in zip(spec["scenes"], starts, ends))
    page = f"""<!doctype html><html lang="fa"><head><meta charset="utf-8"><style>{B.CSS}</style></head>
<body style="--a:{spec['accent']};--T:{total:.3f}s"><div class="bg"><div class="blob b1"></div><div class="blob b2"></div><div class="grain"></div></div>
<div class="tag">{B.esc(spec['tag'])}</div>{scenes}<div class="bar"><i></i></div></body></html>"""
    hp = os.path.join(ROOT, f"_{key}_el.html"); open(hp, "w").write(page)
    silent = os.path.join(work, "silent.mp4")
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(B.FPS), "-c:v", "mjpeg", "-i", "-",
                           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", silent], stdin=subprocess.PIPE)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": B.W, "height": B.H})
        pg.goto("file://" + hp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
        for f in range(int(total * B.FPS)):
            pg.evaluate("ms=>document.getAnimations().forEach(a=>{a.pause();a.currentTime=ms})", f * 1000 / B.FPS)
            ff.stdin.write(pg.screenshot(type="jpeg", quality=90))
        b.close()
    ff.stdin.close(); ff.wait()
    out = os.path.join(ROOT, "out", key + "_elevenlabs.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", voice_mp3, "-i", os.path.join(work, "music.wav"),
                    "-filter_complex", f"[1:a]adelay={int(LEAD*1000)}|{int(LEAD*1000)},aresample=44100[v];[2:a]volume=0.10,aresample=44100[m];[v][m]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-14:TP=-1[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(key, f"{total:.1f}s", [round(s, 2) for s in starts], out)

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
