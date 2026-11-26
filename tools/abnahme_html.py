#!/usr/bin/env python3
"""Schreibt abnahme/abnahme.html neu (Kapitel aus abnahme/daten.json + Abweichungen unten). Start nach tools/abnahme.py."""
import os, json, html, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, "abnahme", "abnahme.html")
s = open(P).read()
D = json.load(open(os.path.join(R, "abnahme", "daten.json")))
AB = {
 "s1": (True, "Wie im Storyboard: Morgennebel, kahler Baum, Bagger hinten. Der Film startet genau auf diesem Bild."),
 "s2": (False, "Schnurgerüst und Gärtner wie im Storyboard, aber weiter weg und mit Bagger rechts statt unscharf im Vordergrund (One-Take statt Einzelbild)."),
 "s3": (False, "Blüte wie im Storyboard, aber Totale mit neuem Staudenbeet statt Blick durch die Blüten. Karte in Salbei statt Rosé (neue Farbwelt)."),
 "s4": (False, "Sommer mit Versenkregnern statt einem Regner mit Regenbogen. Neu: Wasser-Diagramm und Foto-Karte mit Schritte-Rechner."),
 "s5": (False, "Abend mit Lichterketten wie im Storyboard, Tisch näher am Haus. Bewertungskarten als markierte Beispiele."),
 "s6": (True, "Wie im Storyboard: Herbstnebel, Laubbläser, Leiter am Baum. Krone im Film voller und oranger."),
 "s7": (False, "Bewusst anders: Azubi setzt eine Granit-Baumscheibe statt Apfelkiste (Eugen 26.11.: keine Äpfel). Text oben, Azubi frei."),
 "s8": (False, "Winter zur blauen Stunde wie im Storyboard, das Haus leuchtet; die beleuchtete Natursteinmauer ist im Film kaum zu sehen."),
}
ch = []
for i, d in enumerate(D):
    ok, t = AB.get(d["id"], (True, ""))
    n, e = i + 1, html.escape(d["name"])
    ch.append(f'''  <section class="ch"><div class="ch-h"><span class="n">{n}</span><h2>{e}</h2><span class="tag">Panel {d["panel"]}</span></div>
    <div class="grid"><figure><img src="img/{d["id"]}-sb.jpg" alt="Storyboard {e}" loading="lazy"><figcaption>Storyboard</figcaption></figure><figure><img src="img/{d["id"]}-lap.jpg" alt="Seite {e} Laptop" loading="lazy"><figcaption>Seite · Laptop</figcaption></figure><figure><img src="img/{d["id"]}-mob.jpg" alt="Seite {e} Handy" loading="lazy"><figcaption>Handy</figcaption></figure></div>
    <p class="note{' ok' if ok else ''}">{html.escape(t)}</p>
  </section>
''')
a = s.index('  <section class="ch"><div class="ch-h">'); b = s.index('  <section class="ch box"><h2>Zum Einbetten</h2>')
s = s[:a] + "".join(ch) + "\n" + s[b:]
dev = sum(1 for d in D if not AB.get(d["id"], (True,))[0])
st = f'''    <div class="status">
      <span class="pill"><b>Online</b> · GitHub Pages</span>
      <span class="pill">Ein One-Take (30 s) durch 8 Stationen</span>
      <span class="pill">8 Unterseiten</span>
      <span class="pill">Farbwelt Erdbraun + Salbei</span>
      <span class="pill">Geprüft: Laptop, 3 Handys, quer · 0 Fehler · kein Querscroll</span>
      <span class="pill">{dev} Abweichungen markiert</span>
    </div>'''
s = re.sub(r'    <div class="status">.*?</div>', st, s, count=1, flags=re.S)
s = re.sub(r'  <section class="ch box"><h2>Offen</h2>.*?</section>', '''  <section class="ch box"><h2>Offen</h2>
    <ul>
      <li>Der One-Take ist ein kostenloser 720P-Entwurf. Hochskalieren oder 2K erst nach deinem OK (kostet Credits).</li>
      <li>Geprüft nur headless (Laptop + 4 Handygrößen), nicht auf einem echten Handy.</li>
    </ul>
  </section>''', s, count=1, flags=re.S)
# Farbwelt Erdbraun + Salbei
s = s.replace("Farbwelt der Seite: Olive + Rosé", "Farbwelt der Seite: Erdbraun + Salbei")
s = s.replace("--bg:#f3f1ea; --panel:#e7e9dc; --line:#cfd3bf; --fg:#1f2617; --mut:#5c6452; --acc:#b5605a; --acc-bg:#e8b4b0; --on-acc:#2a2420;",
              "--bg:#f2efe9; --panel:#e6e9df; --line:#cdd3c3; --fg:#1d1915; --mut:#5a5a4c; --acc:#5e7a4c; --acc-bg:#b7c9a4; --on-acc:#1d1915;")
s = s.replace("--bg:#232c1b;--panel:#2f3a24;--line:#45523a;--fg:#f4efe6;--mut:#b9bfae;--acc:#e8b4b0;--acc-bg:#e8b4b0;--on-acc:#2a2420;",
              "--bg:#15120f;--panel:#1d1915;--line:#3a332b;--fg:#efe9df;--mut:#b3ab9e;--acc:#b7c9a4;--acc-bg:#b7c9a4;--on-acc:#1d1915;")
s = s.replace("Rosa Linie = Abweichung vom Storyboard.", "Grüne Linie = Abweichung vom Storyboard.")
s = s.replace('height="800" style="border:0" loading="lazy" title="WURZELWERK Demo"', 'style="width:100%;height:100vh;border:0" loading="lazy" title="WURZELWERK – Garten- und Landschaftsbau (Demo)"')
open(P, "w").write(s)
print("ok", len(D), "Kapitel,", dev, "Abweichungen")
