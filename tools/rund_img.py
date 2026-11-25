#!/usr/bin/env python3
"""Rundgang-Bilder: assets-roh/4k/WWR-P#.png -> site/assets/img/rund/p#.webp (volle Breite)
und p#-m.webp (Hochformat-Ausschnitt fürs Handy, volle Höhe). Cache: nur Geändertes neu.
Start: python3 tools/rund_img.py"""
import json, os
from PIL import Image, ImageFilter
# Masterfile V2.65: lokal nachschärfen vor dem WebP-Export (Originale bleiben unverändert)
USM = dict(radius=1.6, percent=70, threshold=2)

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(R, "assets-roh", "4k")
OUT = os.path.join(R, "site", "assets", "img", "rund")
CACHE = os.path.join(R, "assets-roh", "rund_cache.json")
# Mittelpunkt des Handy-Ausschnitts (Anteil der Bildbreite)
CX = {1: .50, 2: .42, 3: .36, 4: .44, 5: .50, 6: .50, 7: .58, 8: .50}
os.makedirs(OUT, exist_ok=True)
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
JOBS = [(n, "WWR-P%d" % n, "p%d" % n, CX[n]) for n in range(1, 9)] + [(10 + n, "WWB-%d" % n, "b%d" % n, .5) for n in range(1, 7)] + [(20 + n, "WWS-B%d" % n, "sb%d" % n, .5) for n in range(1, 9)] + [(30 + n, "WWS-A%d" % n, "sa%d" % n, {6: .72}.get(n, .5)) for n in range(2, 9)] + [(40 + i, "WWX-" + k, "x-" + k.lower(), .5) for i, k in enumerate(["T1", "T7A", "T7B", "T6", "D1", "D2", "D3", "D4", "D5", "R1", "G1", "P1"])]
for n, raw, out, cxx in JOBS:
    src = os.path.join(SRC, raw + ".png")
    if not os.path.exists(src):
        print("fehlt", raw); continue
    key = "%d|%d|%s|%s" % (os.path.getmtime(src), os.path.getsize(src), cxx, USM)
    d, m = os.path.join(OUT, out + ".webp"), os.path.join(OUT, out + "-m.webp")
    if cache.get(str(n)) == key and os.path.exists(d) and os.path.exists(m):
        continue
    im = Image.open(src).convert("RGB").filter(ImageFilter.UnsharpMask(**USM))
    w, h = im.size
    im.save(d, "WEBP", quality=80, method=5)
    cw = int(h * .62); x = int(min(max(cxx * w - cw / 2, 0), w - cw))
    im.crop((x, 0, x + cw, h)).save(m, "WEBP", quality=80, method=5)
    cache[str(n)] = key
    print(out, w, "x", h, "->", os.path.getsize(d) // 1024, "KB,", "m", cw, "x", h, os.path.getsize(m) // 1024, "KB")
json.dump(cache, open(CACHE, "w"))

# Liste der vorhandenen Bilder für die Seiten (keine 404-Anfragen auf noch fehlende Storyboard-Fotos)
have = sorted(f[:-5] for f in os.listdir(OUT) if f.endswith(".webp") and not f.endswith("-m.webp"))
open(os.path.join(R, "site", "assets", "js", "imgs.js"), "w").write("window.WW_IMGS=%s;\n" % json.dumps(have))
