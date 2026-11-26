#!/usr/bin/env python3
"""One-Take (Eugen 26.11.2026): EIN Film (assets-roh/vid/WWONE.mp4, 30 s) wird an den Stationsgrenzen in 8 Abschnitte geteilt
-> assets-roh/vid/WWC41..48.mp4 (s1..s8). Benachbarte Abschnitte sind direkt aufeinanderfolgende Bilder desselben Films,
also keine Naht. Danach tools/rund_vid.py. Start: python3 tools/onetake.py [Schnittzeiten in s, z. B. 4 8 12 16 20 24 27]"""
import os, sys, subprocess
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(R, "assets-roh", "vid", "WWONE.mp4")
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", SRC]).decode())
cuts = [float(x) for x in sys.argv[1:]] or [4, 8, 12, 16, 20, 24, 27]
b = [0] + cuts + [dur]
fps = 30
for i in range(8):
    dst = os.path.join(R, "assets-roh", "vid", "WWC%d.mp4" % (41 + i))
    a, e = b[i], b[i + 1]
    # Bild-genau: Abschnitt i endet mit dem Bild, mit dem Abschnitt i+1 beginnt (gemeinsames Grenzbild, kein Sprung)
    sf, ef = round(a * fps), round(e * fps)
    subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-i", SRC, "-an", "-vf",
                           "fps=%d,trim=start_frame=%d:end_frame=%d,setpts=PTS-STARTPTS" % (fps, sf, min(ef + 1, round(dur * fps))),
                           "-c:v", "libx264", "-preset", "slow", "-crf", "12", "-pix_fmt", "yuv420p", dst])
    print("WWC%d" % (41 + i), "%.2f–%.2f s" % (a, e))
