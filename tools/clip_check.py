#!/usr/bin/env python3
"""Prüft einen One-Take-Clip, bevor er Eugen gezeigt wird.

Start: python3 tools/clip_check.py <clip.mp4> [--start bild.jpg] [--ende bild.jpg] [--bogen out.jpg]
- erstes Bild gegen das Startbild, letztes Bild gegen das Zielbild (Korrelation, 1 = gleich)
- Schnitt-/Sprung-Suche: Bild-zu-Bild-Differenz, alles über 6× Median wird mit Sekunde gemeldet
- Kontaktbogen (24 Bilder) zum eigenen Ansehen der Nahtstellen
"""
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

a = sys.argv[1:]
opt = {}
for k in ("--start", "--ende", "--bogen"):
    if k in a:
        i = a.index(k); opt[k] = a[i + 1]; del a[i:i + 2]
clip = a[0]


def grau(f):
    return cv2.cvtColor(cv2.resize(f, (320, 180), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY).astype(float)


def korr(x, y):
    return float(np.corrcoef(grau(x).ravel(), grau(y).ravel())[0, 1])


c = cv2.VideoCapture(clip)
fps = c.get(cv2.CAP_PROP_FPS) or 24
fs = []
while True:
    ok, f = c.read()
    if not ok:
        break
    fs.append(f)
n = len(fs)
h, w = fs[0].shape[:2]
print("%s: %dx%d, %d Bilder, %.2f s" % (clip, w, h, n, n / fps))
if "--start" in opt:
    print("erstes Bild vs Start: %.3f" % korr(fs[0], cv2.imread(opt["--start"])))
if "--ende" in opt:
    print("letztes Bild vs Ziel: %.3f" % korr(fs[-1], cv2.imread(opt["--ende"])))
g = [grau(f) for f in fs]
d = np.array([np.abs(g[i] - g[i - 1]).mean() for i in range(1, n)])
med = float(np.median(d)) or 0.1
# Sprung = Ausreißer gegenüber der eigenen Umgebung (schnelle Kamerafahrt zählt nicht, nur plötzlicher Bildwechsel)
spr = []
for i in range(len(d)):
    um = np.concatenate([d[max(0, i - 6):i], d[i + 1:i + 7]])
    ref = max(float(np.median(um)) if len(um) else med, med)
    if d[i] > 3 * ref and d[i] > 8:
        spr.append((i + 1, d[i]))
print("Median-Bewegung %.2f, Sprünge: %s" % (med, ", ".join("%.2f s (%.0f)" % (i / fps, v) for i, v in spr) or "keine"))

if "--bogen" in opt:
    K = 24
    idx = [round(i * (n - 1) / (K - 1)) for i in range(K)]
    TW, TH = 320, int(320 * h / w)
    sheet = Image.new("RGB", (6 * (TW + 6) + 6, 4 * (TH + 26) + 6), (20, 20, 20))
    dr = ImageDraw.Draw(sheet)
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    for k, i in enumerate(idx):
        r, cc = divmod(k, 6)
        x, y = 6 + cc * (TW + 6), 6 + r * (TH + 26)
        dr.text((x, y), "%.1f s" % (i / fps), fill=(255, 220, 80), font=font)
        im = Image.fromarray(cv2.cvtColor(fs[i], cv2.COLOR_BGR2RGB)).resize((TW, TH))
        sheet.paste(im, (x, y + 20))
    sheet.save(opt["--bogen"], quality=82)
    print("Bogen:", opt["--bogen"])
