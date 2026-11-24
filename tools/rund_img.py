#!/usr/bin/env python3
"""Rundgang-Bilder: assets-roh/4k/WWR-P#.png -> site/assets/img/rund/p#.webp (volle Breite)
und p#-m.webp (Hochformat-Ausschnitt fürs Handy, volle Höhe). Cache: nur Geändertes neu.
Start: python3 tools/rund_img.py"""
import json, os
from PIL import Image

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(R, "assets-roh", "4k")
OUT = os.path.join(R, "site", "assets", "img", "rund")
CACHE = os.path.join(R, "assets-roh", "rund_cache.json")
# Mittelpunkt des Handy-Ausschnitts (Anteil der Bildbreite)
CX = {1: .50, 2: .42, 3: .36, 4: .44, 5: .50, 6: .50, 7: .58, 8: .50}
os.makedirs(OUT, exist_ok=True)
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
for n in range(1, 9):
    src = os.path.join(SRC, "WWR-P%d.png" % n)
    if not os.path.exists(src):
        print("fehlt", n); continue
    key = "%d|%d|%s" % (os.path.getmtime(src), os.path.getsize(src), CX[n])
    d, m = os.path.join(OUT, "p%d.webp" % n), os.path.join(OUT, "p%d-m.webp" % n)
    if cache.get(str(n)) == key and os.path.exists(d) and os.path.exists(m):
        continue
    im = Image.open(src).convert("RGB")
    w, h = im.size
    im.save(d, "WEBP", quality=80, method=5)
    cw = int(h * .62); x = int(min(max(CX[n] * w - cw / 2, 0), w - cw))
    im.crop((x, 0, x + cw, h)).save(m, "WEBP", quality=80, method=5)
    cache[str(n)] = key
    print("p%d" % n, w, "x", h, "->", os.path.getsize(d) // 1024, "KB,", "m", cw, "x", h, os.path.getsize(m) // 1024, "KB")
json.dump(cache, open(CACHE, "w"))
