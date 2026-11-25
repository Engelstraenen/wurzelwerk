#!/usr/bin/env python3
"""Rundgang-Clips (nachgeschärft unsharp=5:5:0.7, Masterfile V2.65): assets-roh/vid/WWC<n>.mp4 (Dreamina 720P) -> site/assets/vid/rund/c<n>.mp4 (quer, volle Breite)
und c<n>-p.mp4 (Handy hochkant, Ausschnitt in voller Höhe). Kurze GOP (6) für ruckelfreies Scroll-Spulen.
Nie hochskalieren. Start: python3 tools/rund_vid.py"""
import os, subprocess

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(R, "assets-roh", "vid")
OUT = os.path.join(R, "site", "assets", "vid", "rund")
# Handy-Ausschnitt: Mitte zwischen Start- und Endbild (siehe CX in rund_img.py)
CX = {1: .46, 2: .39, 3: .40, 4: .47, 5: .50, 6: .54, 7: .54}
os.makedirs(OUT, exist_ok=True)


def run(src, dst, vf):
    subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-i", src, "-an", "-vf", vf + ",unsharp=5:5:0.7,fps=30,format=yuv420p",
                           "-c:v", "libx264", "-preset", "slow", "-crf", "21", "-g", "6", "-keyint_min", "6",
                           "-sc_threshold", "0", "-movflags", "+faststart", dst])


for n in range(1, 10):
    src = os.path.join(SRC, "WWC%d.mp4" % n)
    if not os.path.exists(src):
        continue
    d, p = os.path.join(OUT, "c%d.mp4" % n), os.path.join(OUT, "c%d-p.mp4" % n)
    if os.path.exists(d) and os.path.getmtime(d) > os.path.getmtime(src):
        continue
    w, h = (int(x) for x in subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                                    "stream=width,height", "-of", "csv=p=0", src]).decode().split(",")[:2])
    run(src, d, "scale=trunc(iw/2)*2:trunc(ih/2)*2")
    cw = int(h * .62) // 2 * 2
    x = int(min(max(CX.get(n, .5) * w - cw / 2, 0), w - cw))
    run(src, p, "crop=%d:%d:%d:0" % (cw, h - h % 2, x))
    print("c%d" % n, w, "x", h, os.path.getsize(d) // 1024, "KB | p", cw, "x", h, os.path.getsize(p) // 1024, "KB")

# Liste der vorhandenen Clips für die Seite (keine 404-Anfragen auf fehlende Clips)
have = [n for n in range(1, 10) if os.path.exists(os.path.join(OUT, "c%d.mp4" % n))]
open(os.path.join(R, "site", "assets", "js", "clips.js"), "w").write("window.WW_CLIPS=%s;\n" % have)
print("clips.js", have)
