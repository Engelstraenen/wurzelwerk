#!/usr/bin/env python3
"""Baut die Web-Bilder aus den 4K-Originalen (sjinn 5504x3072 bzw. 3072x5504).

Quelle:  assets-roh/4k/<ID>.png|jpg   (ID = WW-F1, WW-R1 ...)
Ziel:    site/assets/img/<name>.webp (lange Kante 3840) und <name>-m.webp (lange Kante 1800)
         r3-rolle: Magenta freistellen -> PNG mit Alpha (1600 / 800)
Schreibt site/assets/js/img.js (window.WW_IMG + Versionsstempel).
Cache (Dropbox lädt große Quellen bei jedem Öffnen neu): unveränderte Quellen werden nicht geöffnet.

Start: python3 tools/assets.py
"""
import json
import os
import time

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "assets-roh", "4k")
OUT = os.path.join(ROOT, "site", "assets", "img")
CACHE = os.path.join(ROOT, "tools", ".assets-cache.json")
os.makedirs(OUT, exist_ok=True)

NAMES = {
    "WW-F1": "f1-vorher", "WW-K1": "k1-karriere", "WW-R1": "r1-erde", "WW-R2": "r2-rasen",
    "WW-R3": "r3-rolle", "WW-R4": "r4-hand", "WW-V1": "v1-nachher", "WW-V0": "v0-vorher",
    "WW-S1": "s1-pflaster", "WW-S2": "s2-rasen", "WW-S3": "s3-mauern", "WW-S4": "s4-bewaesserung",
    "WW-S5": "s5-pflege", "WW-P1": "p1-handyfoto",
}
PNG = {"r3-rolle"}


def fit(im, long):
    s = long / max(im.size)
    return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS) if s < 1 else im


def key_magenta(im):
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mag = np.clip(((r + b) / 2 - g - 60) / 80, 0, 1)
    alpha = (1 - mag) * 255
    spill = np.clip(((r + b) / 2 - g) / 255, 0, 1) * (alpha < 250)
    rgba = np.dstack([np.clip(r - spill * 60, 0, 255), g, np.clip(b - spill * 60, 0, 255), alpha]).astype(np.uint8)
    out = Image.fromarray(rgba, "RGBA")
    bbox = out.getchannel("A").point(lambda v: 255 if v > 20 else 0).getbbox()
    return out.crop(bbox) if bbox else out


def main():
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    info = {}
    for f in sorted(os.listdir(RAW)) if os.path.isdir(RAW) else []:
        rid, ext = os.path.splitext(f)
        name = NAMES.get(rid)
        if not name or ext.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
            continue
        src = os.path.join(RAW, f)
        st = os.stat(src)
        key = "%s|%d|%d" % (f, st.st_size, int(st.st_mtime))
        outs = [os.path.join(OUT, name + s) for s in ((".png", "-m.png") if name in PNG else (".webp", "-m.webp"))]
        if cache.get(name, {}).get("key") == key and all(os.path.exists(o) for o in outs):
            info[name] = cache[name]["info"]
            continue
        im = Image.open(src)
        im.load()
        if name in PNG:
            cut = key_magenta(im)
            fit(cut, 1600).save(outs[0], optimize=True)
            fit(cut, 800).save(outs[1], optimize=True)
            i = {"w": cut.width, "h": cut.height, "png": 1}
        else:
            rgb = im.convert("RGB")
            fit(rgb, 3840).save(outs[0], "WEBP", quality=82, method=6)
            fit(rgb, 1800).save(outs[1], "WEBP", quality=80, method=6)
            i = {"w": im.width, "h": im.height}
        info[name] = i
        cache[name] = {"key": key, "info": i}
        print("gebaut", name, im.size)
    json.dump(cache, open(CACHE, "w"))
    info["_v"] = int(time.time())
    js = os.path.join(ROOT, "site", "assets", "js", "img.js")
    open(js, "w").write("window.WW_IMG=" + json.dumps(info) + ";\n")
    print("img.js:", len(info) - 1, "Bilder")


if __name__ == "__main__":
    main()
