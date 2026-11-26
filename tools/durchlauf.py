#!/usr/bin/env python3
"""Durchlauf-Video der Startseite (headless): scrollt gleichmäßig von oben bis unten und nimmt auf.
Start: python3 tools/durchlauf.py <ziel.mp4> [breite x höhe] [sekunden]"""
import sys, os, glob, subprocess, tempfile
from playwright.sync_api import sync_playwright
out = sys.argv[1]; w, h = (int(x) for x in (sys.argv[2] if len(sys.argv) > 2 else "1280x720").split("x")); dur = float(sys.argv[3]) if len(sys.argv) > 3 else 45
tmp = tempfile.mkdtemp()
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": w, "height": h}, record_video_dir=tmp, record_video_size={"width": w, "height": h}, is_mobile=w < 600, has_touch=w < 600)
    pg = ctx.new_page(); pg.goto("http://127.0.0.1:4430/", wait_until="load"); pg.wait_for_timeout(3000)
    H = pg.evaluate("document.documentElement.scrollHeight - innerHeight")
    steps = int(dur * 20)
    for i in range(steps + 1):
        pg.evaluate("y => scrollTo(0, y)", H * i / steps); pg.wait_for_timeout(50)
        if i % 40 == 0: pg.wait_for_function("() => [...document.querySelectorAll('video.clip')].every(v => v.readyState >= 2 || !v.src)", timeout=15000)
    pg.wait_for_timeout(1500); ctx.close(); b.close()
v = glob.glob(os.path.join(tmp, "*.webm"))[0]
subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-i", v, "-c:v", "libx264", "-crf", "22", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out])
print(out)
