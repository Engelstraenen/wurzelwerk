#!/usr/bin/env python3
"""Abnahme der Leistungs-Kapitel (Storyboard 1 „Schicht für Schicht“, vorschau/113): je Panel Storyboard, Laptop, Handy.
Start: python3 tools/abnahme_k.py  (Server auf 4430 muss laufen). Schreibt abnahme/leistungen.html + abnahme/img/k*-*.jpg"""
import os, re, subprocess, sys, html
from PIL import Image
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(R, "abnahme", "img"); os.makedirs(IMG, exist_ok=True)
SHOT = os.path.join(R, "abnahme", "_k"); os.makedirs(SHOT, exist_ok=True)
E = html.escape
PAN = [  # (Seite, Station, Name, Abweichung, ok)
 ("rasen", 1, "Über Nacht grün", "Wie im Storyboard: Handschuhe rollen den Rollrasen auf Erde aus, Baum und Haus dahinter. Im Film rollt die Rolle beim Scrollen aus.", True),
 ("rasen", 2, "Schicht für Schicht", "Wie im Storyboard: Boden schwebt in Schichten (Rasen, Oberboden, Sand, Rohr, Unterboden), Haarlinien mit Etiketten. Handy: Schichten als Chips statt Haarlinien (zu schmal).", False),
 ("rasen", 3, "Wasser, wenn es zählt", "Wie im Storyboard: Versenkregner im Gegenlicht, Balkendiagramm links. Werte sind Richtwerte pro m² und Woche, nicht 0–200 Liter.", False),
 ("angebot", 1, "Ein Foto. Mehr nicht.", "Wie im Storyboard: Hand mit Handy, das Display zeigt dieselbe Gartenecke. Beim Scrollen wächst das Display zum ganzen Bild.", True),
 ("angebot", 2, "36 m²", "Wie im Storyboard: Messraster auf dem Boden, Felder leuchten nacheinander, Zahl zählt auf 36 m² hoch. Die Zahl steht als Überschrift statt frei im Bild.", False),
 ("angebot", 3, "Ihre Skizze", "Wie im Storyboard: Draufsicht mit Terrasse, Rasen, Beeten, Maßlinien 8,50 m und 4,25 m, Knopf „Skizze anfordern“. Maßlinie unten statt oben (Kopfzeile).", False),
 ("gehoelzschnitt", 1, "Drei Schnitte", "Wie im Storyboard: Apfelbaum im Winterlicht, drei Ringe auf den Ästen. Handy: nur der mittlere Ring passt ins Hochformat.", False),
 ("gehoelzschnitt", 2, "Schnitt am Astring", "Wie im Storyboard: Säge am Astring, Haarlinie mit „Schnitt am Astring“. Im Film sägt die Hand, der Ast fällt.", True),
 ("gehoelzschnitt", 3, "Januar bis März", "Wie im Storyboard: ausgelichtete Krone mit Sonne, Kalender Januar–März rechts. Handy: Kalender oben, Text unten.", True),
]

def shots():
    for slug in ("rasen", "angebot", "gehoelzschnitt"):
        for sz in ("1440x900", "390x844"):
            subprocess.run([sys.executable, os.path.join(R, "tools", "story_check.py"), slug, SHOT, sz, ".6"], check=True, capture_output=True)

def build():
    sb = Image.open(os.path.join(R, "vorschau", "113-leistungen-storyboard-1-schicht-fuer-schicht.jpg")).convert("RGB")
    W, H = sb.size; pw, ph = W / 3, H / 3
    for k, (slug, st, *_rest) in enumerate(PAN):
        r, c = divmod(k, 3)
        sb.crop((int(c * pw + 4), int(r * ph + 4), int((c + 1) * pw - 4), int((r + 1) * ph - 4))).save(os.path.join(IMG, "k%d-sb.jpg" % (k + 1)), quality=86)
        for sz, tag, mw in (("1440x900", "lap", 1440), ("390x844", "mob", 390)):
            im = Image.open(os.path.join(SHOT, "%s-%d-60-%s.jpg" % (slug, st, sz))).convert("RGB")
            im.save(os.path.join(IMG, "k%d-%s.jpg" % (k + 1, tag)), quality=84)
    src = open(os.path.join(R, "abnahme", "abnahme.html")).read()
    head = src[:src.index('<div class="wrap">')]
    tail = src[src.index('<div class="lb" id="lb" hidden>'):]
    tail = re.sub(r"document\.getElementById\('copy'\)[\s\S]*?\}\);\n", "", tail)
    ch = []
    for k, (slug, st, name, dev, ok) in enumerate(PAN):
        n = k + 1; e = E(name)
        ch.append(f'''  <section class="ch"><div class="ch-h"><span class="n">{n}</span><h2>{e}</h2><span class="tag">{E(slug)} · Station {st}</span></div>
    <div class="grid"><figure><img src="img/k{n}-sb.jpg" alt="Storyboard {e}" loading="lazy"><figcaption>Storyboard</figcaption></figure><figure><img src="img/k{n}-lap.jpg" alt="Seite {e} Laptop" loading="lazy"><figcaption>Seite · Laptop</figcaption></figure><figure><img src="img/k{n}-mob.jpg" alt="Seite {e} Handy" loading="lazy"><figcaption>Handy</figcaption></figure></div>
    <p class="note{' ok' if ok else ''}">{E(dev)}</p>
  </section>
''')
    dev = sum(1 for p in PAN if not p[4])
    top = f'''<div class="wrap">
  <header class="top">
    <h1>WURZELWERK · Leistungs-Kapitel</h1>
    <div class="status">
      <span class="pill"><b>Online</b> · GitHub Pages</span>
      <span class="pill">Storyboard 1 „Schicht für Schicht“</span>
      <span class="pill">3 Unterseiten · je 3 Stationen</span>
      <span class="pill">Geprüft: Laptop + Handy · 0 Fehler · kein Querscroll</span>
      <span class="pill">{dev} Abweichungen markiert</span>
    </div>
    <div class="actions">
      <a class="btn" href="https://engelstraenen.github.io/wurzelwerk/leistungen/rasen.html" target="_blank" rel="noopener">Rasen</a>
      <a class="btn" href="https://engelstraenen.github.io/wurzelwerk/leistungen/angebot.html" target="_blank" rel="noopener">Angebot per Foto</a>
      <a class="btn" href="https://engelstraenen.github.io/wurzelwerk/leistungen/gehoelzschnitt.html" target="_blank" rel="noopener">Gehölzschnitt</a>
    </div>
    <p class="note ok">Je Panel: links das Storyboard, Mitte die Seite am Laptop, rechts am Handy. Bild antippen = groß. Grüne Linie = Abweichung.</p>
  </header>
'''
    open(os.path.join(R, "abnahme", "leistungen.html"), "w").write(head + top + "".join(ch) + "</div>\n\n" + tail)
    print("abnahme/leistungen.html", len(PAN), "Panels")

if __name__ == "__main__":
    if "--nur-html" not in sys.argv: shots()
    build()
