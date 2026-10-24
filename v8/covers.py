import os
from playwright.sync_api import sync_playwright
ROOT=os.path.dirname(os.path.abspath(__file__))
keys=["eleven","veo","revprompt","imagetools","indicator"]
seek="t=>{document.getAnimations().forEach(a=>{a.pause();a.currentTime=t*1000});window.tick(t)}"
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1080,"height":1920})
    for k in keys:
        pg.goto("file://"+os.path.join(ROOT,"out",f"{k}_ig.html")); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400); pg.evaluate("window.fitAll()")
        pg.evaluate(seek,1.5)
        pg.add_style_tag(content=".kara,.prog,.meta{display:none!important}")
        pg.screenshot(path=os.path.join(ROOT,"out",f"{k}_cover.jpg"),type="jpeg",quality=90)
    b.close()
