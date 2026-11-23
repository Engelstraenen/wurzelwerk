#!/usr/bin/env python3
"""Baut die Scroll-Videos für ein Filmkapitel, OHNE Verkleinern (volle 2K-Auflösung).

Start: python3 tools/video.py <roh.mp4> <kapitel> [--t <sekunden>]   (kapitel = fassade | raum | karriere)
Ziel:  site/assets/vid/<kapitel>.mp4    Desktop: volle Quellauflösung (2560x1440), All-Intra
       site/assets/vid/<kapitel>-p.mp4  Handy hochkant: Ausschnitt in voller Quellhöhe (1080x1440),
                                         Lage = object-position des Kapitels, darum gleicher Bildausschnitt
       site/assets/vid/<kapitel>-m.mp4  Handy quer: ganzes Bild 1280 breit
Trägt das Kapitel in tools/geo.json unter "vid" ein und baut img.js neu (Versionsstempel).
All-Intra = jedes Bild ein Keyframe, damit Scrollen vor und zurück ohne Ruckeln springt.
Nie hochskalieren. 20.11.2026: Eugen sah unscharfe Videos, weil die Seite 2K auf 1920/720 verkleinert hat.
"""
import json
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site", "assets", "vid")
RAW = os.path.join(ROOT, "assets-roh", "vid")
# object-position (x) der Kapitel auf dem Handy, siehe style.css @media (max-width:900px)
POS = {"fassade": 0.5, "raum": 0.76, "karriere": 0.6}


def size(src):
    o = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0",
                                 "-show_entries", "stream=width,height", "-of", "csv=p=0", src]).decode()
    w, h = (int(x) for x in o.strip().split(",")[:2])
    return w, h


def enc(src, dst, vf, crf, t=None):
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", src]
    if t:
        cmd += ["-t", str(t)]
    cmd += ["-an", "-vf", vf + ",format=yuv420p",
            "-c:v", "libx264", "-preset", "slow", "-crf", str(crf), "-tune", "film",
            "-g", "1", "-keyint_min", "1", "-sc_threshold", "0",
            "-movflags", "+faststart", dst]
    subprocess.check_call(cmd)
    return os.path.getsize(dst)


def main():
    a = sys.argv[1:]
    t = None
    if "--t" in a:
        i = a.index("--t")
        t = float(a[i + 1])
        del a[i:i + 2]
    src, ch = a[0], a[1]
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(RAW, exist_ok=True)
    keep = os.path.join(RAW, ch + "-roh" + os.path.splitext(src)[1])
    if os.path.abspath(src) != os.path.abspath(keep):
        shutil.copy2(src, keep)
    w, h = size(src)
    # Desktop: volle Auflösung
    s1 = enc(src, os.path.join(OUT, ch + ".mp4"), "null", 20, t)
    # Handy hochkant: 3:4-Ausschnitt in voller Höhe, Lage wie object-position
    cw = min(w, (h * 3 // 4) // 2 * 2)
    x0 = int(round(POS.get(ch, 0.5) * (w - cw))) // 2 * 2
    s2 = enc(src, os.path.join(OUT, ch + "-p.mp4"), "crop=%d:%d:%d:0" % (cw, h, x0), 21, t)
    # Handy quer: ganzes Bild
    s3 = enc(src, os.path.join(OUT, ch + "-m.mp4"), "scale=%d:-2:flags=lanczos" % min(w, 1280), 21, t)
    print("quelle %dx%d -> %s.mp4 %dx%d %.1f MB | -p %dx%d (x0 %d) %.1f MB | -m %.1f MB"
          % (w, h, ch, w, h, s1 / 1e6, cw, h, x0, s2 / 1e6, s3 / 1e6))
    gp = os.path.join(ROOT, "tools", "geo.json")
    geo = json.load(open(gp)) if os.path.exists(gp) else {}
    geo.setdefault("vid", {})[ch] = 1
    json.dump(geo, open(gp, "w"), indent=1, ensure_ascii=False)
    subprocess.check_call([sys.executable, os.path.join(ROOT, "tools", "assets.py")])


if __name__ == "__main__":
    main()
