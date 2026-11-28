#!/usr/bin/env python3
"""Leistungs-Kapitel headless prüfen: Screenshots je Station (Anteil t) + Übergang, Konsolenfehler, Querscroll.
Start: python3 tools/story_check.py <slug> <ordner> [BxH] [t-Liste z. B. .5,.9]"""
import os, sys
from playwright.sync_api import sync_playwright
slug, out = sys.argv[1], sys.argv[2]
w, h = (int(x) for x in (sys.argv[3] if len(sys.argv) > 3 else "1440x900").split("x"))
ts = [float(x) for x in (sys.argv[4] if len(sys.argv) > 4 else ".55").split(",")]
os.makedirs(out, exist_ok=True); errs = []
with sync_playwright() as p:
    b = p.chromium.launch(); m = w < 760
    pg = b.new_page(viewport={"width": w, "height": h}, is_mobile=m, has_touch=m)
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda x: errs.append(x.text) if x.type == "error" else None)
    pg.goto("http://127.0.0.1:4430/leistungen/%s.html" % slug, wait_until="domcontentloaded"); pg.wait_for_timeout(2500)
    pg.add_style_tag(content="html{scroll-behavior:auto!important}")
    n = pg.evaluate("document.querySelectorAll('.sst-m').length")
    for i in range(n):
        for t in ts:
            pg.evaluate("([i,t,n])=>{const s=document.querySelector('.sst');scrollTo(0,s.offsetTop+(s.offsetHeight-innerHeight)*(i+t)/n)}", [i, t, n])
            pg.wait_for_timeout(1300)
            fn = os.path.join(out, "%s-%d-%02d-%dx%d.jpg" % (slug, i + 1, int(t * 100), w, h)); pg.screenshot(path=fn, type="jpeg", quality=72); print(fn)
    print("querscroll", pg.evaluate("document.documentElement.scrollWidth-innerWidth"), "fehler", len(errs), errs[:3])
    b.close()
