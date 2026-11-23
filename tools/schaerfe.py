#!/usr/bin/env python3
"""Echte Schärfe eines Videos messen (Pflicht vor jeder Final-Lieferung, Masterfile: MiniMax-2K-Regel).

Vergleicht die Kanten-Schärfe (Laplace-Varianz) jedes Video-Abschnitts mit dem 4K-Startbild,
das auf die Videogröße und auf 1920 / 1280 / 854 Breite heruntergerechnet und wieder hochgezogen wird.
So sieht man, welcher echten Auflösung das Detail im Video entspricht.

Start: python3 tools/schaerfe.py <video.mp4> <startbild-4k.jpg>
"""
import subprocess
import sys

import cv2
import numpy as np


def lapvar(img):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if img.ndim == 3 else img
    return float(cv2.Laplacian(g, cv2.CV_64F).var())


def main():
    vid, ref = sys.argv[1], sys.argv[2]
    cap = cv2.VideoCapture(vid)
    W, H = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 24
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    im = cv2.imread(ref)
    base = cv2.resize(im, (W, H), interpolation=cv2.INTER_AREA)
    refs = {"%dp-voll" % H: lapvar(base)}
    for w in (1920, 1280, 854):
        if w >= W:
            continue
        h = round(w * H / W)
        small = cv2.resize(im, (w, h), interpolation=cv2.INTER_AREA)
        refs["%dp" % h] = lapvar(cv2.resize(small, (W, H), interpolation=cv2.INTER_CUBIC))
    print("Video %dx%d, %.1f s" % (W, H, n / fps))
    print("Startbild als Maßstab:", ", ".join("%s=%.0f" % kv for kv in refs.items()))
    step = int(round(fps))
    for i in range(0, n, step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ok, fr = cap.read()
        if not ok:
            break
        v = lapvar(fr)
        near = min(refs.items(), key=lambda kv: abs(kv[1] - v))[0]
        print("t=%4.1f s  Schärfe %6.0f  ≈ %s" % (i / fps, v, near))


if __name__ == "__main__":
    main()
