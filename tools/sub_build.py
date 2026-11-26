#!/usr/bin/env python3
"""Unterseiten im Stil Storyboard U2 „Schnitt durch den Boden“ (vorschau/62) -> site/leistungen/<slug>.html
Aufbau 1:1 nach U2: 1 Hero-Schnitt · 2–5 Ebenen mit Leuchtlinie + Callout · 6 Makro mit Lupe ·
7 Warum das zählt · 8 Ablauf in 5 Tagen · (9 Handy = mobile Fassung). Dazu V2.69: Diagramm, Rechner/Auswahl, FAQ.
Daten = übliche GaLaBau-Richtwerte, keine Firmenzahlen, keine Preise."""
import json, os, html
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(R, "site", "leistungen")
os.makedirs(OUT, exist_ok=True)
E = html.escape

PAGES = [
 dict(slug="neuanlage", back="s3", eye="Terrasse & Pflaster", title="Was unter Ihrer<br>Terrasse liegt.",
  lead="Eine Terrasse sieht man nur von oben. Ob sie in zehn Jahren noch gerade liegt, entscheidet sich darunter: fünf Schichten, rund 40 Zentimeter tief.",
  hero="x-t1", hero_alt="p3", hero_desc="Schnitt durch eine fertige Terrasse am alten Apfelbaum: alle Schichten von der Platte bis zum gewachsenen Boden",
  layers=[
   dict(y=88, h=22, t="Ebene 1 · Boden: <em>tragfähiger Untergrund</em>", c="tragfähiger Untergrund, geprüft",
        p="Bevor Material kommt, prüfen wir den gewachsenen Boden. Lehm und Ton halten Wasser und frieren auf. Gibt der Boden nach, heben wir tiefer aus oder legen ein Trennvlies ein. Das Planum bekommt schon hier das Gefälle."),
   dict(y=66, h=22, t="Ebene 2 · Frostschutz: <em>30–40 cm Kies</em>", c="30–40 cm · 0/32 · lagenweise verdichtet",
        p="Die dickste Schicht: Mineralgemisch 0/32, in Lagen von etwa 15 cm eingebaut, jede Lage mit der Rüttelplatte verdichtet. Wasser sickert hindurch, statt unter der Terrasse zu gefrieren und sie anzuheben."),
   dict(y=50, h=9, t="Ebene 3 · Tragschicht: <em>Schotter 0/45 · 15 cm</em>", c="Schotter 0/45 · 15 cm",
        p="Grober Schotter verzahnt sich beim Verdichten und verteilt das Gewicht von Tisch, Grill und Gästen in die Fläche. Wir messen die Höhe mit dem Laser, nicht nach Augenmaß."),
   dict(y=43.5, h=3, t="Ebene 4 · Bettung: <em>Splitt 2/5 · 3–5 cm</em>", c="Splitt 2/5 · 3–5 cm",
        p="Das Bett aus Edelsplitt wird über Lehren exakt abgezogen. Nicht dicker als nötig: Eine zu dicke Bettung gibt unter Last nach, dann kippeln Platten."),
   dict(y=38.5, h=7, t="Ebene 5 · Belag: <em>Fuge 3–5 mm · 2 % Gefälle</em>", c="Fuge 3–5 mm · 2 % Gefälle",
        p="Gleichmäßige Fugen und 2 % Gefälle vom Haus weg. Auf 4 m Terrassentiefe sind das 8 cm. Regen läuft ab, statt in Pfützen stehen zu bleiben oder an die Hauswand zu laufen."),
  ],
  macro=dict(k="x-t6", c="Fuge 3–5 mm · 2 % Gefälle", h="Ebene 5 · Belag im Detail",
             p="Die Fuge ist kein Schönheitsfehler, sie ist Technik: Sie nimmt Bewegung auf und lässt die Platten arbeiten, ohne dass Kanten abplatzen."),
  why=dict(bad="x-t7a", good="x-t7b", badt="Setzungen, Staunässe, Frostschäden.", goodt="Stabil, dauerhaft, schön – für Jahrzehnte.",
           badl=["Frostschutz zu dünn oder gar nicht verdichtet", "kein Gefälle, Wasser steht", "Bettung zu dick, Platten kippeln"],
           goodl=["Aufbau nach Nutzung bemessen", "jede Lage verdichtet und gemessen", "2 % Gefälle vom Haus weg"]),
  chart=dict(h="Wie tief es nach unten geht", src="Richtwerte für den Gesamtaufbau nach gängiger GaLaBau-Praxis (ZTV-Wegebau). Die genaue Dicke hängt von Boden, Nutzung und Frostzone ab.",
             max=60, rows=[("Gartenweg, begehbar", 30, [6, 9, 15]), ("Terrasse", 40, [7, 15, 18]), ("Stellplatz, PKW", 50, [12, 18, 20])],
             legend=[("#9a9a96", "Belag + Bettung"), ("#c9b79a", "Tragschicht"), ("#6f6a5f", "Frostschutz")], unit="cm"),
  calc=dict(h="Was in Ihre Terrasse hineingeht", lead="Länge und Breite einstellen, Belag wählen. Sie sehen, wie viel Material bewegt wird, ganz ohne Preise.",
            ins=[("Länge", 2, 12, 5), ("Breite", 2, 8, 4)], unit="m",
            mats=[("Feinsteinzeug 60×60", dict(per=1 / .36, txt="<b>Feinsteinzeug:</b> 2 cm stark, nimmt kaum Wasser auf (≤ 0,5 %), fleckunempfindlich. Fuge mindestens 3 mm.")),
                  ("Naturstein 60×40", dict(per=1 / .24, txt="<b>Naturstein:</b> frostfest und hart, jede Platte ein Unikat. Unterschiedliche Stärken werden in der Bettung ausgeglichen.")),
                  ("Betonplatte 40×40", dict(per=1 / .16, txt="<b>Betonplatte:</b> robust, einzelne Platten lassen sich später leicht tauschen. Fuge 3–5 mm."))],
            res=[("platten", "Platten inkl. 5 % Verschnitt", dict(m2=1.05, mat="per", d=0, ceil=1)),
                 ("aushub", "m³ Aushub (ca. 45 cm tief)", dict(m2=.45, d=1)),
                 ("lkw", "Lkw-Fahrten Erde (ca. 10 m³ lose)", dict(m2=.45 * 1.3 / 10, d=0, ceil=1)),
                 ("frost", "t Frostschutz 0/32", dict(m2=.6, d=1)),
                 ("splitt", "t Splitt 2/5", dict(m2=.064, d=1))],
            note="Richtwerte für die Planung: Aushub aufgelockert um ca. 30 %, Frostschutz ca. 30 cm bei rund 2 t/m³ verdichtet."),
  days=[("Tag 1", "Ausheben & Vorbereitung", "x-d1"), ("Tag 2", "Frostschutz einbauen", "x-d2"), ("Tag 3", "Tragschicht herstellen", "x-d3"),
        ("Tag 4", "Bettung & Belag verlegen", "x-d4"), ("Tag 5", "Fugen & Abschluss", "x-d5")],
  days_note="Richtwert für ca. 30 m² bei trockenem Wetter und guter Zufahrt.",
  faq=[("Wie tief wird ausgehoben?", "Für eine Terrasse meist 40–50 cm unter der späteren Oberfläche, bei lehmigem Boden auch mehr. Das zeigt sich beim ersten Spatenstich."),
       ("Warum braucht eine Terrasse Gefälle?", "Damit Regen abläuft. 2 % vom Haus weg sind üblich, also 2 cm pro Meter. Das sieht man nicht, aber man merkt es nach jedem Regen."),
       ("Kann man neue Platten auf die alten legen?", "Selten sinnvoll. Liegen die alten Platten schief oder ist der Unterbau zu dünn, wandert der Fehler mit nach oben."),
       ("Wann kann ich die Terrasse benutzen?", "Bei ungebundener Fuge direkt nach dem Abrütteln und Einkehren. Bei Fugenmörtel nach Herstellerangabe, oft nach etwa einem Tag begehbar."),
       ("Brauche ich eine Genehmigung?", "Ebenerdige Terrassen sind in den meisten Bundesländern verfahrensfrei. Bebauungsplan und Abstandsflächen prüfen wir trotzdem mit Ihnen.")]),

 dict(slug="angebot", back="s4", eye="Angebot per Foto", title="Ein Foto statt<br>drei Termine.",
  lead="Vieles sehen wir schon auf einem guten Foto: Fläche, Gefälle, Zufahrt, alter Belag. So kommen wir nur noch, wenn es wirklich nötig ist.",
  hero="sa3", hero_alt="p3", hero_desc="Hand hält ein Handy mit dem Foto einer Gartenecke vor der echten Gartenecke",
  layers=[
   dict(y=50, h=100, t="Schritt 1 · Foto: <em>die ganze Fläche im Querformat</em>", c="Querformat, ganze Fläche, bei Tageslicht",
        p="Stellen Sie sich an den Rand und fotografieren Sie die Fläche einmal komplett, dazu ein Foto aus der Gegenrichtung. Tageslicht reicht, Blitz eher nicht."),
   dict(y=50, h=100, t="Schritt 2 · Maße: <em>Schritte zählen genügt</em>", c="1 Schritt ≈ 0,75 m",
        p="Ein Maßband ist schön, Schritte reichen für den Anfang: ein normaler Schritt sind etwa 75 cm. Den Rechner unten können Sie direkt mit Schritten füttern."),
   dict(y=50, h=100, t="Schritt 3 · Wunsch: <em>was soll hin?</em>", c="Terrasse, Rasen, Beet, Mauer …",
        p="Ein Satz reicht: „Terrasse für 6 Personen, Rest Rasen.“ Gern mit einem Bild aus einer Zeitschrift oder von Pinterest."),
   dict(y=50, h=100, t="Schritt 4 · Zufahrt: <em>passt ein Minibagger durch?</em>", c="Durchgang ab ca. 1 m Breite",
        p="Kleine Bagger und Raddumper kommen durch Gartentore ab etwa einem Meter. Ein Foto vom Weg in den Garten spart uns die Frage."),
   dict(y=50, h=100, t="Schritt 5 · Antwort: <em>Skizze und Ablauf</em>", c="Rückmeldung mit Skizze",
        p="Sie bekommen eine einfache Skizze, die Schichten, den Ablauf und die Dauer. Erst wenn etwas unklar bleibt, schauen wir es uns vor Ort an."),
  ],
  why=dict(badt="Drei Termine, bevor überhaupt geplant wird.", goodt="Ein Foto, eine Skizze, ein Termin zum Start.",
           badl=["Besichtigung, Aufmaß, Angebotsbesprechung", "Wochen bis zur ersten Zahl", "Urlaubstag für jeden Termin"],
           goodl=["Foto und Schritte schicken", "Skizze mit Schichten und Ablauf", "vor Ort nur, wenn nötig"]),
  calc=dict(h="Schritte rein, Fläche raus", lead="Zählen Sie Länge und Breite in Schritten. Wir rechnen um, ganz ohne Maßband.",
            ins=[("Länge in Schritten", 2, 30, 8), ("Breite in Schritten", 2, 20, 6)], unit="Schritte",
            mats=[("normaler Schritt", dict(per=.75 ** 2, txt="<b>Normaler Schritt:</b> etwa 75 cm. Für eine erste Einschätzung genau genug.")),
                  ("großer Schritt", dict(per=.9 ** 2, txt="<b>Großer Schritt:</b> etwa 90 cm, wenn Sie bewusst weit ausschreiten."))],
            res=[("m2", "m² ungefähr", dict(m2=1, mat="per", d=1)),
                 ("rolle", "Rollen Rollrasen (je 1 m²)", dict(m2=1.05, mat="per", d=0, ceil=1)),
                 ("std", "Stauden für ein Beet dieser Größe", dict(m2=7, mat="per", d=0, ceil=1))],
            note="Rollrasen kommt meist in Rollen zu 1 m² (2,5 m × 0,4 m). Stauden: rund 5–9 Pflanzen pro m², hier 7 gerechnet.", area_mat="per"),
  faq=[("Welche Fotos helfen am meisten?", "Die ganze Fläche im Querformat, einmal aus jeder Richtung, dazu der Weg in den Garten und alles, was bleiben soll (Baum, Mauer, Leitungen)."),
       ("Reicht das wirklich ohne Termin?", "Für eine erste Planung meistens ja. Bei Hanglage, unklarem Boden oder Leitungen kommen wir vorbei."),
       ("Was passiert mit meinen Fotos?", "Sie dienen nur der Planung Ihres Gartens. In dieser Demo wird nichts gesendet.")]),

 dict(slug="rasen", back="s4", eye="Rasen & Bewässerung", title="Was unter Ihrem<br>Rasen liegt.",
  lead="Rollrasen ist über Nacht grün. Ob er grün bleibt, entscheiden die 30 Zentimeter darunter: Boden, Wasser und eine Leitung, die man nie sieht.",
  hero="x-r1", hero_alt="p4", hero_desc="Schnitt durch einen frisch verlegten Rollrasen mit Oberboden, Sandschicht und Regner",
  layers=[
   dict(y=85, h=28, t="Ebene 1 · Unterboden: <em>gelockert, nicht verdichtet</em>", c="ca. 20 cm tief gelockert",
        p="Baufahrzeuge verdichten den Boden. Wir brechen ihn auf, sammeln Steine und Bauschutt ab. Sonst steht Wasser und die Wurzeln bleiben flach."),
   dict(y=61, h=7, t="Ebene 2 · Sand: <em>Wasser darf ablaufen</em>", c="Sand gegen Staunässe",
        p="Auf schweren Böden arbeiten wir Sand ein. Er hält die Poren offen, damit Regen versickert, statt den Rasen zu ersticken."),
   dict(y=67, h=4, t="Ebene 3 · Bewässerung: <em>Leitung und Versenkregner</em>", c="Leitung, Versenkregner, im Herbst entleert",
        p="Die Leitung liegt unsichtbar im Boden, die Regner fahren nur zum Wässern hoch. Vor dem ersten Frost wird die Anlage entleert, damit nichts platzt."),
   dict(y=51, h=13, t="Ebene 4 · Oberboden: <em>10–15 cm Mutterboden</em>", c="10–15 cm · Feinplanum · Startdünger",
        p="Humoser Oberboden, fein planiert und angewalzt. Hier wurzelt der Rasen. Jede Senke im Feinplanum wäre später eine Pfütze."),
   dict(y=40, h=6, t="Ebene 5 · Rollrasen: <em>verlegt am Tag der Lieferung</em>", c="innerhalb von 24 h verlegt",
        p="Rollrasen wird frühmorgens geschält und am selben Tag verlegt, Fugen versetzt wie bei einer Mauer, danach angewalzt und kräftig gewässert."),
  ],
  why=dict(bad=None, good=None, badt="Grün für einen Sommer.", goodt="Grün für viele Jahre.",
           badl=["Rolle auf verdichteten Boden gelegt", "Senken im Planum, Wasser steht", "nach der Verlegung zu wenig gewässert"],
           goodl=["Unterboden gelockert, Sand eingearbeitet", "Feinplanum angewalzt", "Bewässerung von Anfang an mitgeplant"]),
  chart=dict(h="Wie viel Wasser ein Rasen braucht", src="Richtwerte für einen eingewachsenen Rasen bei wenig Regen, Liter pro m² und Woche. Sandboden braucht mehr, Lehmboden weniger.",
             max=30, rows=[("April", 10, [10]), ("Mai", 15, [15]), ("Juni", 20, [20]), ("Juli", 25, [25]), ("August", 20, [20]), ("September", 10, [10])],
             legend=[], unit="l/m²", one=True),
  calc=dict(h="Was Ihr Rasen braucht", lead="Fläche einstellen und Rasentyp wählen.",
            ins=[("Länge", 2, 30, 10), ("Breite", 2, 20, 6)], unit="m",
            mats=[("Spielrasen", dict(per=1, txt="<b>Spielrasen:</b> robuste Mischung mit viel Deutschem Weidelgras, hält Fußball und Gartenpartys aus.")),
                  ("Zierrasen", dict(per=1, txt="<b>Zierrasen:</b> feinblättrig und dicht, braucht häufiger Mähen und mehr Pflege.")),
                  ("Schattenrasen", dict(per=1, txt="<b>Schattenrasen:</b> mit Lägerrispe und Rotschwingel für Flächen unter Bäumen, wie unter dem Apfelbaum."))],
            res=[("rolle", "Rollen Rollrasen (je 1 m², +5 %)", dict(m2=1.05, d=0, ceil=1)),
                 ("boden", "m³ Oberboden (10 cm)", dict(m2=.1, d=1)),
                 ("wasser", "Liter Wasser in den ersten 14 Tagen", dict(m2=10 * 14, d=0)),
                 ("woche", "Liter pro Woche im Juli", dict(m2=25, d=0))],
            note="Anwachsphase: etwa 10 l/m² täglich in den ersten zwei Wochen, je nach Wetter. Erster Schnitt meist nach 10–14 Tagen."),
  days=[("Tag 1", "Altrasen fräsen, Boden lockern", None), ("Tag 2", "Bewässerung verlegen", None), ("Tag 3", "Oberboden & Feinplanum", None),
        ("Tag 4", "Rollrasen verlegen & walzen", None), ("Tag 5", "Wässern & Einweisung", None)],
  days_note="Richtwert für ca. 150 m².",
  faq=[("Wann darf man auf den neuen Rasen?", "Vorsichtig betreten nach etwa zwei Wochen, voll belastbar nach drei bis vier Wochen, wenn die Wurzeln angewachsen sind."),
       ("Wann ist die beste Zeit für Rollrasen?", "Frühjahr und Spätsommer bis Herbst. Im Hochsommer geht es auch, braucht aber konsequentes Wässern."),
       ("Was passiert mit der Bewässerung im Winter?", "Leitungen werden vor dem Frost entleert oder ausgeblasen. Das erledigen wir im Herbst mit der Pflege.")]),

 dict(slug="pflege", back="s5", eye="Beete & Pflege", title="Was ein Beet<br>wachsen lässt.",
  lead="Ein Beet, das wenig Arbeit macht, ist kein Zufall: guter Boden, Wasser an der Wurzel, eine Decke aus Mulch und die richtige Pflanze am richtigen Ort.",
  hero="x-p1", hero_alt="p5", hero_desc="Schnitt durch ein Staudenbeet mit Mulch, humosem Oberboden und Tropfschlauch",
  layers=[
   dict(y=85, h=28, t="Ebene 1 · Unterboden: <em>durchwurzelbar</em>", c="gelockert, ohne Bauschutt",
        p="Wurzeln gehen tiefer, als man denkt. Unter einem guten Beet liegt gelockerter Boden ohne Schutt und Folie."),
   dict(y=57, h=20, t="Ebene 2 · Oberboden: <em>ca. 30 cm, mit Kompost</em>", c="ca. 30 cm humos · Kompost",
        p="Humoser Oberboden mit eingearbeitetem Kompost speichert Wasser und Nährstoffe. Hier sitzt der größte Teil der Wurzeln."),
   dict(y=59, h=3, t="Ebene 3 · Tropfschlauch: <em>Wasser an die Wurzel</em>", c="Wasser direkt an die Wurzel",
        p="Ein Tropfschlauch unter dem Mulch gibt das Wasser langsam ab, genau dort, wo es gebraucht wird. Blätter bleiben trocken, weniger verdunstet."),
   dict(y=45, h=4, t="Ebene 4 · Mulch: <em>5–7 cm Decke</em>", c="5–7 cm Mulch",
        p="Die Mulchschicht hält Feuchtigkeit im Boden und lässt kaum Unkraut durch. Einmal im Jahr wird nachgelegt."),
   dict(y=33, h=18, t="Ebene 5 · Pflanzung: <em>5–9 Stauden pro m²</em>", c="5–9 Stauden pro m²",
        p="Stauden in Gruppen, Gräser als Gerüst, nach Standort gewählt. So schließt sich das Beet nach ein bis zwei Jahren und braucht nur noch wenig Hilfe."),
  ],
  why=dict(badt="Jedes Wochenende Unkraut zupfen.", goodt="Ein Beet, das sich selbst trägt.",
           badl=["nackte Erde, Unkraut keimt sofort", "Pflanzen nach Optik statt Standort", "Wässern mit dem Schlauch von oben"],
           goodl=["Mulchdecke gegen Unkraut", "Pflanzen nach Sonne und Boden", "Tropfschlauch an der Wurzel"]),
  chart=dict(h="Das Pflegejahr", src="Übliche Zeitfenster im Hausgarten. Starke Rückschnitte an Hecken sind vom 1. März bis 30. September nach § 39 Bundesnaturschutzgesetz verboten, schonende Formschnitte sind erlaubt.",
             max=12, rows=[("Stauden zurückschneiden", 0, [1, 2]), ("Mulch nachlegen", 0, [3, 2]), ("Rasen mähen", 0, [3, 7]),
                           ("Hecke Formschnitt", 0, [5, 3]), ("Laub & Winterschutz", 0, [9, 2]), ("Gehölze auslichten", 0, [0, 2, 8, 2])],
             legend=[], unit="", gantt=True),
  calc=dict(h="Ihr Beet in Zahlen", lead="Beetgröße einstellen und Standort wählen.",
            ins=[("Länge", 1, 15, 6), ("Breite", .5, 4, 1.5)], unit="m",
            mats=[("Sonne", dict(per=1, txt="<b>Sonne:</b> Salbei, Katzenminze, Lavendel, Fetthenne und Gräser wie Lampenputzergras.")),
                  ("Halbschatten", dict(per=1, txt="<b>Halbschatten:</b> Storchschnabel, Frauenmantel, Funkien und Astilben.")),
                  ("Schatten", dict(per=1, txt="<b>Schatten:</b> Farne, Elfenblume, Waldmarbel und Golderdbeere, ideal unter dem Apfelbaum."))],
            res=[("std", "Stauden (7 pro m²)", dict(m2=7, d=0, ceil=1)), ("mulch", "m³ Mulch (6 cm)", dict(m2=.06, d=2)),
                 ("kompost", "Liter Kompost pro Jahr", dict(m2=3, d=0))],
            note="Richtwerte: 5–9 Stauden pro m² je nach Wuchsgröße, Kompost 2–3 l/m² im Frühjahr."),
  faq=[("Wie viel Pflege braucht ein neues Beet?", "Im ersten Jahr regelmäßig wässern und Unkraut ziehen. Wenn die Stauden geschlossen sind, reichen wenige Pflegegänge im Jahr."),
       ("Rindenmulch oder Kies?", "Rindenmulch für Waldrand- und Schattenpflanzen, mineralischer Mulch für Steppen- und Präriestauden in der Sonne."),
       ("Gibt es Pflege als Abo?", "Ja, mit festen Terminen übers Jahr: Rückschnitt, Mulch, Rasen, Hecke, Laub. In dieser Demo nur als Beispiel.")]),

 dict(slug="gehoelzschnitt", back="s6", eye="Baum & Gehölzschnitt", title="Was ein Baum<br>unter der Erde hat.",
  lead="Ein alter Apfelbaum ist unter der Erde so breit wie über der Erde. Wer schneidet, gräbt oder pflastert, muss beides kennen.",
  hero="x-g1", hero_alt="p6", hero_desc="Schnitt durch den alten Apfelbaum im Herbst mit dem ganzen Wurzelwerk unter der Erde",
  layers=[
   dict(y=75, h=50, t="Ebene 1 · Wurzelraum: <em>so weit wie die Krone</em>", c="Kronentraufe + 1,5 m schützen",
        p="Die meisten Feinwurzeln liegen in den oberen 60 cm, oft weit über die Krone hinaus. Bei Bauarbeiten schützen wir nach DIN 18920 den Bereich unter der Krone plus 1,5 m."),
   dict(y=45, h=4, t="Ebene 2 · Baumscheibe: <em>frei halten</em>", c="nicht verdichten, nicht pflastern",
        p="Kein Rasen bis an den Stamm, keine Platten auf die Wurzeln. Eine gemulchte Baumscheibe lässt Wasser und Luft an die Wurzeln."),
   dict(y=35, h=18, t="Ebene 3 · Stamm: <em>saubere Schnitte</em>", c="Schnitt am Astring",
        p="Äste werden am Astring abgenommen, nicht bündig am Stamm und nicht als Stummel. So kann der Baum die Wunde selbst überwallen."),
   dict(y=17, h=14, t="Ebene 4 · Leitäste: <em>das Gerüst der Krone</em>", c="3–4 Leitäste",
        p="Ein Obstbaum trägt mit einer Mitte und drei bis vier Leitästen. Konkurrenztriebe und nach innen wachsende Äste kommen heraus, damit Licht in die Krone fällt."),
   dict(y=6, h=10, t="Ebene 5 · Fruchtholz: <em>Ernte im nächsten Jahr</em>", c="Winterschnitt Jan–März",
        p="Der Winterschnitt regt das Wachstum an, ein leichter Sommerschnitt nach der Ernte beruhigt. Wasserschosse werden im Sommer gerissen statt geschnitten."),
  ],
  why=dict(badt="Ein Schnitt, und der Baum treibt nur noch Wasserschosse.", goodt="Ein Schnitt, und der Baum trägt jahrelang.",
           badl=["Kappen statt Auslichten", "Stummel oder Schnitt in den Stamm", "Pflaster bis an den Stamm"],
           goodl=["Auslichten mit Plan", "Schnitt am Astring", "Wurzelraum geschützt"]),
  chart=dict(h="Wann was geschnitten wird", src="Übliche Schnittzeiten. Vom 1. März bis 30. September sind starke Rückschnitte und das Roden von Hecken nach § 39 Bundesnaturschutzgesetz verboten, schonende Form- und Pflegeschnitte sind erlaubt.",
             max=12, rows=[("Obstbaum Winterschnitt", 0, [0, 3]), ("Obstbaum Sommerschnitt", 0, [6, 2]), ("Frühblüher nach der Blüte", 0, [3, 2]),
                           ("Hecke Formschnitt", 0, [5, 3]), ("Hecke starker Rückschnitt", 0, [0, 2, 7, 3])],
             legend=[], unit="", gantt=True),
  calc=dict(h="Ihre Hecke in Zahlen", lead="Länge und Höhe einstellen, Heckenart wählen.",
            ins=[("Länge", 2, 60, 15), ("Höhe", .8, 3, 1.8)], unit="m",
            mats=[("Hainbuche", dict(per=1, cuts=2, txt="<b>Hainbuche:</b> heimisch, gut für Vögel, verträgt starken Schnitt. Meist zweimal im Jahr in Form geschnitten.")),
                  ("Liguster", dict(per=1, cuts=2, txt="<b>Liguster:</b> wächst dicht und schnell, wintergrün bis halbimmergrün. Zwei Schnitte im Jahr.")),
                  ("Eibe", dict(per=1, cuts=1, txt="<b>Eibe:</b> wächst langsam, sehr schnittverträglich, auch im Schatten. Ein Schnitt im Jahr reicht meist."))],
            res=[("flaeche", "m² Schnittfläche (2 Seiten + oben)", dict(m2=None, d=0)), ("cuts", "Schnitte pro Jahr", dict(fix="cuts", d=0))],
            note="Schnittfläche = Länge × (2 × Höhe + 0,6 m Heckenbreite).", hedge=True),
  faq=[("Darf ich meine Hecke im Sommer schneiden?", "Schonende Form- und Pflegeschnitte ja. Starke Rückschnitte und Roden nur vom 1. Oktober bis Ende Februar, und nie, wenn Vögel darin brüten."),
       ("Wann schneidet man Apfelbäume?", "Hauptschnitt im Winter an frostfreien Tagen, ein leichter Sommerschnitt nach der Ernte."),
       ("Kann man unter einem alten Baum pflastern?", "Nur mit Vorsicht: wurzelschonende Bauweise, kein tiefer Aushub im Wurzelraum. Oft ist eine Holzterrasse auf Punktfundamenten die bessere Wahl.")]),
]

def img(k, alt, desc, cls="", hide=True, wide=False, lens=None):
    a = ' data-alt="%s"' % alt if alt else ""
    return '<img data-k="%s"%s%s%s alt="%s"%s loading="lazy" decoding="async">' % (
        k, a, ' data-wide="1"' if wide else "", ' data-lens="%s"' % lens if lens else "", E(desc), ' class="%s"' % cls if cls else "")

def chart(c):
    rows = []
    for name, val, segs in c["rows"]:
        if c.get("gantt"):
            parts, pos, on = [], 0, False
            for s in segs:
                parts.append('<i style="--f:%s"%s></i>' % (s, ' class="c"' if on else ' class="x"')); on = not on
            parts.append('<i style="--f:%s" class="x"></i>' % max(0, 12 - sum(segs)))
            rows.append('<div class="bar"><span>%s</span><div class="tr g"><div class="fl" style="--w:100%%">%s</div></div></div>' % (E(name), "".join(parts)))
        else:
            fl = "".join('<i style="--f:%s"%s></i>' % (s, ' class="c"' if c.get("one") else "") for s in segs)
            rows.append('<div class="bar"><span>%s</span><div class="tr"><div class="fl" style="--w:%.1f%%">%s</div><b>%s %s</b></div></div>' % (E(name), val / c["max"] * 100, fl, val, c["unit"]))
    months = ""
    if c.get("gantt"):
        months = '<div class="bar mo"><span></span><div class="ms">%s</div></div>' % "".join("<i>%s</i>" % m for m in "J F M A M J J A S O N D".split())
    leg = "".join('<span><i style="background:%s"></i>%s</span>' % (col, E(t)) for col, t in c["legend"])
    return '<div class="chart rv"><h3>%s</h3><p class="src">%s</p>%s%s%s</div>' % (E(c["h"]), E(c["src"]), "".join(rows), months, '<div class="legend">%s</div>' % leg if leg else "")

def calc(c):
    k = dict(mat=[m for _, m in c["mats"]], res={}, unit=c["unit"])
    for rid, _, f in c["res"]:
        k["res"][rid] = f
    if c.get("hedge"): k["hedge"] = 1
    if c.get("area_mat"): k["area_mat"] = c["area_mat"]
    ins = "".join('<label for="in%d">%s</label><input type="range" id="in%d" min="%s" max="%s" step="%s" value="%s"><output for="in%d"></output>' % (
        i, E(n), i, lo, hi, .1 if hi <= 5 else (.5 if c["unit"] == "m" else 1), v, i) for i, (n, lo, hi, v) in enumerate(c["ins"]))
    chips = "".join('<button type="button" aria-pressed="%s"%s>%s</button>' % ("true" if i == 0 else "false", ' class="on"' if i == 0 else "", E(n)) for i, (n, _) in enumerate(c["mats"]))
    res = "".join('<div><b data-r="%s">0</b><small>%s</small></div>' % (rid, E(lab)) for rid, lab, _ in c["res"])
    return ('<section class="calc" data-calc=\'%s\'><div class="wrap"><div><p class="eye">Rechner · ohne Preise</p><h2>%s</h2><p class="lead">%s</p>%s'
            '<label>Auswahl</label><div class="chips">%s</div></div><div><p class="eye" style="margin-bottom:10px">Fläche <b data-area>0</b> m²</p><div class="res">%s</div><div class="mat"></div><p class="note">%s</p></div></div></section>') % (
        E(json.dumps(k)), E(c["h"]), E(c["lead"]), ins, chips, res, E(c["note"]))

def page(p):
    L = p["layers"]
    rail = "".join('<button type="button" aria-label="Ebene %d"><i>%d</i></button>' % (i + 1, i + 1) for i in range(len(L)))
    steps = '<div class="step"></div>' * len(L)
    out = []
    out.append('''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%(eye)s · WURZELWERK</title>
<meta name="description" content="%(lead)s">
<meta name="theme-color" content="#2f3a24">
<link rel="preload" href="../assets/fonts/serif.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="../assets/css/sub.css">
</head>
<body>
<div class="demo">Demo-Webseite · erfundener Betrieb · Formulare senden nichts</div>
<header class="top">
  <a class="logo" href="../index.html#s1">WURZELWERK<small>Garten &amp; Landschaft</small></a>
  <a class="back" href="../index.html#%(back)s">← <span>Zurück zum Rundgang</span></a>
</header>
<main>
<section class="hero">
  %(heroimg)s
  <div class="in">
    <a class="back" href="../index.html#%(back)s">← Zurück zur Übersicht</a>
    <p class="eye">%(eye)s</p>
    <h1>%(title)s</h1>
    <p class="lead">%(lead)s</p>
  </div>
  <span class="hint">Scrollen · Ebene für Ebene</span>
</section>
<section class="layers" aria-label="Die Ebenen im Schnitt">
  <script type="application/json" id="layers-data">%(ldata)s</script>
  <div class="stage">
    <div class="cut">%(cutimg)s<div class="dim"></div><div class="glow"></div><div class="call"><span></span></div><div class="rail">%(rail)s</div></div>
    <div class="capbar" aria-live="polite"></div>
  </div>
  <div class="steps">%(steps)s</div>
</section>
''' % dict(eye=E(p["eye"]), lead=E(p["lead"]), back=p["back"], title=p["title"],
           heroimg=img(p["hero"], p["hero_alt"], p["hero_desc"], hide=False).replace(' loading="lazy"', ' fetchpriority="high"'),
           cutimg=img(p["hero"], p["hero_alt"], p["hero_desc"]), rail=rail, steps=steps,
           ldata=json.dumps([dict(y=l["y"], h=l["h"], t=l["t"], c=E(l["c"]), p=E(l["p"])) for l in L], ensure_ascii=False)))
    m = p.get("macro")
    if m:
        out.append('<section class="macro" data-hide><div class="cut">%s<div class="lens" id="lens"></div><div class="call"><span>%s</span></div></div>'
                   '<div class="capbar" style="margin-top:18px"><span class="n">%d</span><b>%s</b><p>%s</p></div></section>\n' % (
                       img(m["k"], None, "Makro der Fuge zwischen zwei Terrassenplatten", lens="#lens"), E(m["c"]), len(L), E(m["h"]), E(m["p"])))
    w = p["why"]
    def side(ok):
        k = w.get("good" if ok else "bad")
        fig = '<figure data-hide>%s</figure>' % img(k, None, w["goodt" if ok else "badt"]) if k else ""
        lst = "".join("<li>%s</li>" % E(x) for x in w["goodl" if ok else "badl"])
        return '<div class="rv"><div class="lab"><i>%s</i>%s</div>%s<p>%s</p><ul>%s</ul></div>' % (
            "✓" if ok else "✕", "Mit WURZELWERK-Aufbau" if ok else "Ohne fachgerechten Aufbau", fig, E(w["goodt" if ok else "badt"]), lst)
    out.append('<section class="why"><h2 class="up">Warum das zählt</h2><div class="vs">%s%s</div>%s</section>\n' % (side(False), side(True), chart(p["chart"]) if p.get("chart") else ""))
    out.append(calc(p["calc"]) + "\n")
    if p.get("days"):
        ds = "".join('<div class="day" style="--i:%d"><div class="t">%s</div><p>%s</p>%s<div class="dot"></div></div>' % (
            i, E(t), E(d), '<figure data-hide>%s</figure>' % img(k, None, d) if k else "") for i, (t, d, k) in enumerate(p["days"]))
        out.append('<section class="flow"><h2 class="up">Ablauf in %d Tagen</h2><div class="days" style="--n:%d">%s</div><p class="note" style="text-align:center;margin-top:26px">%s</p></section>\n' % (
            len(p["days"]), len(p["days"]), ds, E(p["days_note"])))
    fq = "".join("<details><summary>%s</summary><p>%s</p></details>" % (E(q), E(a)) for q, a in p["faq"])
    others = "".join('<a href="%s.html">%s</a>' % (o["slug"], E(o["eye"])) for o in PAGES if o["slug"] != p["slug"])
    out.append('''<section class="faq"><h2 class="up">Häufige Fragen</h2>%s</section>
<section class="cta"><p class="eye">Winter ist Planungszeit</p><h2>Lassen Sie uns<br>über Ihren Garten sprechen.</h2>
<div class="btns"><a class="btn p" href="../index.html#s8">Projekt anfragen →</a><a class="btn" href="../index.html#%s">Zurück zum Rundgang</a></div>
<nav class="more" aria-label="Weitere Leistungen">%s</nav></section>
</main>
<footer>WURZELWERK ist ein erfundener Betrieb. Demo-Webseite, Formulare senden nichts. Alle Angaben sind übliche Richtwerte.</footer>
<script src="../assets/js/imgs.js"></script>
<script src="../assets/js/sub.js"></script>
</body>
</html>
''' % (fq, p["back"], others))
    return "".join(out)

for p in PAGES:
    open(os.path.join(OUT, p["slug"] + ".html"), "w").write(page(p))
    print("leistungen/%s.html" % p["slug"])
