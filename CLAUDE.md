# PROJEKT-MASTERFILE – WURZELWERK
Gilt zusätzlich zur globalen Masterfile (~/.claude/CLAUDE.md).

## 1. Ziel und Endprodukt
Interaktive Demo-Website für einen erfundenen Garten- und Landschaftsbaubetrieb (WURZELWERK). Musterbeispiel für Akquise bei GaLaBau-Firmen (nach LICHTBOGEN/Elektro, FARBKANTE/Maler, WARMHERZ).
Probleme, die die Seite löst: Fachkräfte/Azubis (eigenes Kapitel, 60-s-Bewerbung), unnötige Besichtigungen (Angebot per Foto + Flächenrechner ohne Euro), Kunde kann sich Garten nicht vorstellen (Vorher/Nachher, Planer), Preisdruck (Profi-Unterbau sichtbar machen), Winterloch (Pflege-Abo, Winterdienst), Vertrauen (Bewertungen bewegt).

## 2. Qualitätsanspruch & Referenzen
- Aufbau wie FLUTLICHT27 / FARBKANTE: Film-Kapitel (Scrollen spult) ↔ Motion-Design-Kapitel mit Übergängen.
- Filme Vorher → Arbeit → Ergebnis (verwilderter Garten → Minibagger/Aushub → Unterbau/Rüttelplatte → Pflaster/Rollrasen → fertiger Garten am Abend).
- Leitmotiv eindeutig GaLaBau: Minibagger, Rüttelplatte, Schnurgerüst, Plattenverlegezange, Rollrasen, Natursteinmauer.

## 3. Regeln für dieses Projekt
- (Eugen 25.11.2026) Scrollytelling = durchdachte Story: jede Station kurz erklärt mit echten GaLaBau-Daten + Knopf zu einer detaillierten Unterseite mit starken Visuals; Seiten-Fotos aus den bestätigten Storyboard-Panels (Storyboard als Referenz), Kamerafahrt um den Baum als echter Film Clip an Clip.
- Keine echten Firmen, keine Preise/Euro, kein Wort „KI“, Demo-Hinweis, Formulare senden nichts.
- Alle Seiten mobil-optimiert (4 Größen + Kopfzeile 1081–1600 px).
- Bilder (V2.74, 25.11.2026): 4K nur für vollflächige/gezoomte Bilder (Hauptseiten-Szenen, Unterseiten-Hero, Fugen-Makro mit Lupe), Rest 2K (Vergleichskarten T7A/B, Ablauf-Fotos D1–D5); jedes Bild nachschärfen (Unsharp r1.6 p70 t2). Endvideos MiniMax H3 2K nur nach Kosten-OK.

## 4. Skills, Plugins, Agenten, MCP
Keine zusätzlichen nötig.

## 5. Zugänge
gh (Engelstraenen), sjinn in Chrome eingeloggt (Unlimited).

## 6. Workflow & Freigabepunkte
3 Storyboards (Eugen wählt) → First Frames 4K → Video-Drafts gratis → Seite bauen → Storyboard-Abgleich → GitHub Pages.

## 7. Befehle
- Vorschau: `python3 tools/serve.py 4430` → http://127.0.0.1:4430/ (Port 4430, vorher `<title>` per curl prüfen)
- Bilder bauen: `python3 tools/rund_img.py` (Quellen assets-roh/4k/WWR-P*.png, Cache; Handy = Hochformat-Ausschnitt)
- Prüfen: `python3 tools/check.py http://127.0.0.1:4430/ <ordner> 1440x900 s1:0,s3:.2,s7:.3` (+ 390x844, 360x740, 430x932, 844x390)
- Veröffentlichen: `tools/publish.sh` (gh-pages als ein Commit aus main:site, V2.77; in zsh `${C}:refs` schreiben, sonst schneidet `:r` den Hash ab)

## 8. Offene Fragen
- (keine, Bauplan steht 23.11.2026)

## 9. Entschieden
- 23.11.2026: Name WURZELWERK (Annahme), 3 Storyboard-Varianten in Arbeit.
- 23.11.2026 (Eugen): Mix aus 1 Zeitraffer + 3 Rollrasen. Sieht der Mix nicht gut aus → nur 3. Look-Basis = 3 (Tannengrün/Off-White/Limette).
- 23.11.2026: Bewertungen ohne erfundene Note; echte Werte erst bei echtem Kunden.
- 23.11.2026 (Eugen, BAUPLAN): Seite = beste Teile aller drei Storyboards. (1) Start mit Scrollytelling-Zeitraffer aus Storyboard 1 (Panels 1–5: Vorher → Aushub → Unterbau → Pflaster+Rasen → Fertig, gleicher Garten, feste Kamera). (2) Aus Storyboard 2 der Gartenplaner mit Grundriss (Panel 6: Terrasse/Rasen/Hochbeet ziehen, Live-m², „Plan senden“). (3) ALLES aus Storyboard 3 komplett (Rollrasen rollt aus „Über Nacht grün.“, Handschuh drückt Naht + Buttons, Leistungen als Rasenstreifen, Vorher/Nachher-Slider Vorgarten, Angebot per Foto 36 m², Karriere-Duo mit Rollrasen + Kinetik-Typo, Swipe-Bewerbung „Was fährst du?“, Bewertungen + Footer). Look aus 3 (Tannengrün/Off-White/Limette). Mix-Storyboards A/B nur Zwischenstand.

- 24.11.2026: Video-Drafts auf Dreamina Seedance 2.5 Unlimited (Masterfile V2.45). Z1 Zeitraffer (Start F1 + Ende F5, 8 s) und K1 Karriere (8 s) eingebaut; K1b-Variante gegen Rollen-Morph läuft.
- 24.11.2026 (Eugen): Karriere-Film = Version 28 (K1b, Gesichter im Bild, Rolle rollt ohne Sprung aus), eingebaut.
- 24.11.2026 (Hauptsitzung + Eugen): Standard-Schema weg. 3 Storyboards (37 Jahresuhr, 38 Rundgang, 39 Abreißkalender), Eugen wählt **2 Rundgang um den Baum**: Scrollen = Kamera kreist um den alten Apfelbaum, 8 Haltepunkte (N-Frühling, O-Frühling/Neuanlage, Angebot per Foto, S-Sommer, Bewertungen unterm Baum, W-Herbst, Karriere am Stamm, N-Winter/Kontakt). Navigation = Sonnenbahn oben (Punkt wandert, Jahreszeiten anklickbar) + Kompass. Farbwelt Olive #2f3a24 + Rosé #e8b4b0. Alte Seite (Zeitraffer, Rollrasen, Planer …) nur noch in Git-Historie. Dateien: site/index.html, assets/css/rund.css, assets/js/rund.js, Bilder tools/rund_img.py (WWR-P1…P8, GPT Image 2 4K = 3584×2016, Edits mit P1-Referenz).

- 25.11.2026 (Eugen): Übergänge 1 + 2 kombiniert: oben Jahreszeiten-Schalter (Frühling/Sommer/Herbst/Winter, läuft beim Scrollen mit, antippen = springen). Innerhalb einer Jahreszeit Kamera-Schleier (Variante 2: Nebel, Sprühnebel, Herbstnebel, Schnee + Clip 1), zwischen den Szenen Natur-Brücken (Variante 1): Blüte → Handy (Iris), Handy-Display → Sommergarten (Rechteck wächst), Sprühnebel-Tropfen → Abendlicht, fallendes Blatt → Herbst, Apfel → Kiste des Azubis, Atem → Schnee. Brücken = eigene Szenen (.stop.bridge, data-img b1–b5), Einstieg mit Morgennebel b6. Partikel je Jahreszeit (Canvas .fx). Clips 2–7 entfallen (Brücken ersetzen sie). Abnahme tools/walk.py (5-%-Durchlauf).
- 25.11.2026 (Eugen): Beide Versionen zum Vergleich: ?v=natur (Standard, Version 1 Natur-Brücken), ?v=kamera (Version 2 Kamerafahrt), ?v=kombi (1+2); Umschalter in der Demo-Leiste.

## 10. Ablage
Code: Dropbox/CLAUDE/Projekte/WURZELWERK · Storyboards: konzepte/
