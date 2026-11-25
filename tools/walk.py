#!/usr/bin/env python3
"""Abnahme-Durchlauf: Seite in 5-%-Schritten durchscrollen, Screenshots + Kontaktbogen.
Start: python3 tools/walk.py <url> <ordner> <breite>x<höhe>"""
import sys, os
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
url, out, vp = sys.argv[1], sys.argv[2], sys.argv[3]
w, h = (int(x) for x in vp.split("x")); os.makedirs(out, exist_ok=True)
errs = []; shots = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": w, "height": h}, is_mobile=w < 600, has_touch=w < 600)
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(url, wait_until="networkidle", timeout=90000); pg.wait_for_timeout(3600)
    pg.add_style_tag(content="html{scroll-behavior:auto!important}")
    H = pg.evaluate("document.documentElement.scrollHeight - innerHeight")
    for k in range(21):
        pg.evaluate("y=>scrollTo(0,y)", int(H * k / 20)); pg.wait_for_timeout(500)
        fn = os.path.join(out, "w%02d.jpg" % (k * 5)); pg.screenshot(path=fn, type="jpeg", quality=60); shots.append(fn)
    ov = pg.evaluate("document.documentElement.scrollWidth - innerWidth"); b.close()
tw = 320 if w > h else 160; th = int(tw * h / w); cols = 7 if w > h else 11
sheet = Image.new("RGB", (cols * tw, ((len(shots) + cols - 1) // cols) * th), (0, 0, 0)); d = ImageDraw.Draw(sheet)
for i, f in enumerate(shots):
    im = Image.open(f).resize((tw, th)); x, y = (i % cols) * tw, (i // cols) * th; sheet.paste(im, (x, y)); d.text((x + 4, y + 4), "%d%%" % (i * 5), fill=(255, 255, 0))
sheet.save(os.path.join(out, "bogen.jpg"), quality=70)
print("querscroll", ov, "fehler", len(errs), errs[:3])
