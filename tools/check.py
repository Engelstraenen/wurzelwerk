#!/usr/bin/env python3
"""Headless-Prüfung: Konsolenfehler, Querscrollen, Screenshots an Scroll-Stellen.

Start: python3 tools/check.py [url] [ausgabeordner] [breite]x[höhe] [stellen]
  stellen = kommagetrennt "kapitel:anteil", z. B. fassade:0,fassade:.5,leistungen:.6
"""
import sys
from playwright.sync_api import sync_playwright

url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:4430/"
out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/fk-check"
w, h = (int(x) for x in (sys.argv[3] if len(sys.argv) > 3 else "1440x900").split("x"))
spots = (sys.argv[4] if len(sys.argv) > 4 else "fassade:0").split(",")

import os
os.makedirs(out, exist_ok=True)
errs = []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1, is_mobile=w < 600, has_touch=w < 600)
    pg.on("console", lambda m: errs.append(m.type + ": " + m.text) if m.type in ("error", "warning") else None)
    pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
    pg.goto(url, wait_until="networkidle")
    pg.add_style_tag(content="html{scroll-behavior:auto!important}"); pg.wait_for_timeout(600)
    for s in spots:
        ch, f = s.split(":")
        y = pg.evaluate("""([id,f])=>{const s=document.getElementById(id);const t=s.offsetTop+(s.offsetHeight-innerHeight)*f;window.scrollTo(0,t);return t}""", [ch, float(f)])
        pg.wait_for_timeout(450)
        fn = os.path.join(out, "%s-%s-%dx%d.jpg" % (ch, f.replace(".", ""), w, h))
        pg.screenshot(path=fn, type="jpeg", quality=70)
        print("shot", fn, int(y))
    ov = pg.evaluate("document.documentElement.scrollWidth - innerWidth")
    print("querscroll px:", ov)
    b.close()
print("fehler:", len(errs))
for e in errs[:20]:
    print("  ", e)
