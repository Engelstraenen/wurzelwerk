#!/usr/bin/env python3
"""Abnahme Hauptseite (Masterfile V2.67): je Kapitel Storyboard-Panel neben Laptop- und Handy-Screenshot.
Ausgabe: abnahme/img/*.jpg (+ abnahme/daten.json). Start: python3 tools/abnahme.py [url]"""
import os, sys, json
from PIL import Image
from playwright.sync_api import sync_playwright
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:4430/"
OUT = os.path.join(R, "abnahme", "img"); os.makedirs(OUT, exist_ok=True)
SHEETS = {"B": "vorschau/43-uebergang-B-kamerafahrt.jpg", "A": "vorschau/42-uebergang-A-naturbruecken.jpg"}
# Reihenfolge = Scroll-Reihenfolge der Seite
CH = [("s1", "B", 1, "Nordseite · März"), ("s2", "B", 2, "Ostseite · April · Schnurgerüst"), ("s3", "B", 3, "Blüte · Mai · Garten neu gestalten"),
      ("s4", "B", 4, "Sommer · Juli · Angebot per Foto"), ("s5", "B", 5, "Abendlicht · August · Bewertungen"), ("s6", "B", 6, "Herbstnebel · Oktober"),
      ("s7", "B", 7, "Am Stamm · November · Ausbildung"), ("s8", "B", 8, "Winter · Januar · Kontakt")]


def panel(sheet, n):
    im = Image.open(os.path.join(R, SHEETS[sheet])).convert("RGB")
    w, h = im.size; c, r = (n - 1) % 3, (n - 1) // 3
    pw, ph = w / 3, h / 3; ins = .012 * w
    return im.crop((int(c * pw + ins), int(r * ph + ins), int((c + 1) * pw - ins), int((r + 1) * ph - ins)))


data = []
for cid, sh, n, name in CH:
    p = panel(sh, n); p.thumbnail((1200, 1200)); p.save(os.path.join(OUT, "%s-sb.jpg" % cid), quality=82)
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for (w, h, tag) in ((1440, 900, "lap"), (390, 844, "mob")):
        pg = b.new_page(viewport={"width": w, "height": h}, is_mobile=w < 600, has_touch=w < 600)
        pg.goto(URL, wait_until="load"); pg.wait_for_timeout(2500)
        pg.add_style_tag(content="html{scroll-behavior:auto!important}")
        for cid, sh, n, name in CH:
            pg.evaluate("""id => { const s = document.getElementById(id); scrollTo(0, s.offsetTop + (s.offsetHeight - innerHeight) * .3); }""", cid)
            pg.wait_for_timeout(3500)
            fn = os.path.join(OUT, "%s-%s.jpg" % (cid, tag))
            pg.screenshot(path=fn, type="jpeg", quality=80)
        pg.close()
    b.close()
for cid, sh, n, name in CH:
    data.append(dict(id=cid, panel="%s%d" % (sh, n), name=name))
json.dump(data, open(os.path.join(R, "abnahme", "daten.json"), "w"), ensure_ascii=False, indent=1)
print(len(data), "Kapitel")
