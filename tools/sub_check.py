#!/usr/bin/env python3
"""Headless-Prüfung der Unterseiten: Konsolenfehler, Querscroll, zu kleine Tipp-Flächen, Screenshots je Abschnitt.
Start: python3 tools/sub_check.py [ordner] [seiten…]"""
import sys, os
from playwright.sync_api import sync_playwright
BASE = "http://127.0.0.1:4430/leistungen/"
out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/ww-sub"
pages = sys.argv[2:] or ["neuanlage", "angebot", "rasen", "pflege", "gehoelzschnitt"]
SIZES = [(1440, 900), (1280, 800), (390, 844), (360, 740), (430, 932), (844, 390)]
os.makedirs(out, exist_ok=True)
JS_SPOTS = """() => { const r = []; const L = document.querySelector('.layers'); const n = JSON.parse(document.getElementById('layers-data').textContent).length;
 r.push(['hero', 0]); for (let i = 0; i < n; i++) r.push(['l' + (i + 1), L.offsetTop + (L.offsetHeight - innerHeight) * (i + .5) / n]);
 for (const s of ['.macro', '.why', '.chart', '.calc', '.flow', '.faq', '.cta']) { const e = document.querySelector(s); if (e && !e.hidden && e.offsetHeight) r.push([s.slice(1), e.getBoundingClientRect().top + scrollY - 40]); }
 return r; }"""
JS_TAPS = """() => [...document.querySelectorAll('a,button,summary,input')].filter(e => e.offsetParent && !e.closest('[hidden]')).map(e => { const b = e.getBoundingClientRect(); return [e.tagName + ' ' + (e.textContent || e.id).trim().slice(0, 24), Math.round(b.width), Math.round(b.height)]; }).filter(x => x[2] < 44 || x[1] < 44)"""
bad = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    for slug in pages:
        for w, h in SIZES:
            errs = []
            pg = b.new_page(viewport={"width": w, "height": h}, is_mobile=w < 600, has_touch=w < 600)
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(BASE + slug + ".html", wait_until="load"); pg.wait_for_timeout(800)
            pg.add_style_tag(content="html{scroll-behavior:auto!important}")
            spots = pg.evaluate(JS_SPOTS)
            for name, y in spots:
                pg.evaluate("y => scrollTo(0, y)", y); pg.wait_for_timeout(900 if name in ("chart", "flow", "macro") else 350)
                if w in (1440, 390):
                    pg.screenshot(path=os.path.join(out, "%s-%dx%d-%s.jpg" % (slug, w, h, name)), type="jpeg", quality=70)
            ox = pg.evaluate("document.documentElement.scrollWidth - innerWidth")
            hdr = pg.evaluate("Math.max(...[...document.querySelectorAll('.top *')].map(e => e.getBoundingClientRect().right)) - innerWidth")
            small = pg.evaluate(JS_TAPS) if w < 900 else []
            small = [s for s in small if not s[0].startswith("INPUT")]
            ok = not errs and ox <= 0 and hdr <= 0
            bad += not ok
            print("%-15s %4dx%-4d %s querscroll=%d kopf=%d fehler=%s klein=%s" % (slug, w, h, "OK " if ok else "BAD", ox, hdr, errs[:2], small[:4]))
            pg.close()
    b.close()
print("FEHLER" if bad else "alles ok")
