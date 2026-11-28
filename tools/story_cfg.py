"""Leistungs-Kapitel (Storyboard 1 „Schicht für Schicht“, Eugen 28.11.2026): je Unterseite 3 Stationen.
Koordinaten in Bild-Einheiten 160×90 (= 16:9-Foto) bzw. Prozent; nach dem Erzeugen der Fotos gegen die Bilder abgeglichen."""
import calendar, html
E = html.escape

def txt(eye, h, p, extra=""):
    return '<div class="sst-t"><p class="eye">%s</p><h2>%s</h2><p>%s</p>%s</div>' % (E(eye), h, E(p), extra)

def hl(x, y, w, t, sub="", at=0, left=False):
    return '<div class="hl%s" data-at="%s" style="--x:%s%%;--y:%s%%;--w:%s%%"><span>%s%s</span></div>' % (
        " l" if left else "", at, x, y, w, E(t), "<small>%s</small>" % E(sub) if sub else "")

def ring(x, y, at, s=5.5):
    return '<div class="ring" data-at="%s" style="--x:%s%%;--y:%s%%;--s:%s%%"></div>' % (at, x, y, s)

def grid(q, cols=12, rows=7, span=".12,.62"):
    """q = [TL, TR, BR, BL] in 160×90; Zellen bilinear, leuchten der Reihe nach von vorn links."""
    def P(u, v):
        (ax, ay), (bx, by), (cx, cy), (dx, dy) = q
        tx, ty = ax + (bx - ax) * u, ay + (by - ay) * u
        bx2, by2 = dx + (cx - dx) * u, dy + (cy - dy) * u
        return tx + (bx2 - tx) * v, ty + (by2 - ty) * v
    cells = []
    for r in range(rows - 1, -1, -1):
        for c in range(cols):
            pts = [P(c / cols, r / rows), P((c + 1) / cols, r / rows), P((c + 1) / cols, (r + 1) / rows), P(c / cols, (r + 1) / rows)]
            cells.append('<polygon class="c" vector-effect="non-scaling-stroke" points="%s"/>' % " ".join("%.2f,%.2f" % p for p in pts))
    return '<svg class="grid" viewBox="0 0 160 90" data-cells data-span="%s" aria-hidden="true">%s</svg>' % (span, "".join(cells))

def dims(x1, y1, x2, y2, ylab, h1, h2):
    """Maßlinien der Skizze: waagerecht unter, senkrecht rechts neben der Fläche (ylab = Höhe der waagerechten Linie)."""
    return ('<svg class="dims" data-at=".15" viewBox="0 0 160 90" aria-hidden="true">'
            '<line x1="%s" y1="%s" x2="%s" y2="%s"/><line x1="%s" y1="%s" x2="%s" y2="%s"/>'
            '<text x="%s" y="%s" text-anchor="middle">%s</text><text x="%s" y="%s">%s</text></svg>') % (
        x1, ylab, x2, ylab, x2 + 4, y1, x2 + 4, y2, (x1 + x2) / 2, ylab + 3.2, E(h1), x2 + 5.5, (y1 + y2) / 2 + .8, E(h2))

def bars(rows, h, src):
    mx = max(v for _, v in rows)
    cols = "".join('<div data-at="%.2f"><b>%s</b><i style="--h:%.0f%%"></i></div>' % (.1 + .1 * i, v, v / mx * 86) for i, (_, v) in enumerate(rows))
    mo = "".join("<span>%s</span>" % E(m) for m, _ in rows)
    return '<div class="sbars"><h3>%s</h3><p class="src">%s</p><div class="cols">%s</div><div class="mo">%s</div></div>' % (E(h), E(src), cols, mo)

def cal(year=2027):
    names = ["Januar", "Februar", "März"]
    out = []
    for i, nm in enumerate(names):
        days = "".join("<span class=h>%s</span>" % d for d in "MDMDFSS")
        first, nd = calendar.monthrange(year, i + 1)
        days += "<span></span>" * first
        for d in range(1, nd + 1):
            wd = (first + d - 1) % 7
            days += '<span%s>%d</span>' % (' class="w"' if wd < 5 else "", d)
        out.append('<div class="mo" data-at="%.2f"><h4>%s</h4><div class="d">%s</div></div>' % (.12 + .14 * i, nm, days))
    return '<div class="cal3">%s<p>Hervorgehoben: Arbeitstage im Winterschnitt-Fenster. Geschnitten wird nur an frostfreien Tagen.</p></div>' % "".join(out)

STORY = {
 "rasen": [
  dict(img="k-1", v="kv1", posm="62% 50%", tr="zoom:40,82", alt="Ein Landschaftsgärtner rollt frischen Rollrasen über den vorbereiteten Boden aus",
       ov=txt("Rollrasen", "Über Nacht<br>grün.", "Eine Rolle ist 2,50 × 0,40 m, also genau 1 m². Geschält wird sie am Morgen, verlegt am selben Tag.", '<span class="rule"></span>')),
  dict(img="k-2", v="kv2", posm="40% 50%", tr="zoom:40,70", alt="Der Boden unter dem Rasen hebt sich in einzelne Schichten auseinander",
       ov='<div class="fit">%s%s%s%s%s</div>' % (
           hl(66, 25, 8, "Rasenschicht", "Rollrasen, 2–3 cm Soden", .08), hl(66, 40, 8, "Oberboden", "10–15 cm Mutterboden", .22),
           hl(66, 54, 8, "Sandschicht", "hält die Poren offen", .36), hl(64, 70, 9, "Bewässerungsrohr", "Versenkregner, im Herbst entleert", .5),
           hl(64, 83, 9, "Unterboden", "20 cm tief gelockert", .64))
          + txt("Schicht für Schicht", "Was darunter<br>liegt.", "Grün bleibt Rasen nur, wenn die 30 Zentimeter darunter stimmen.",
                '<ol class="lg">%s</ol>' % "".join('<li data-at="%s">%s</li>' % (a, E(t)) for a, t in [(.08, "Rasen"), (.22, "Oberboden"), (.36, "Sand"), (.5, "Bewässerung"), (.64, "Unterboden")]))),
  dict(img="k-3", posm="70% 50%", alt="Fertiger Rasen mit zwei Versenkregnern im Gegenlicht",
       ov=bars([("Apr", 8), ("Mai", 12), ("Jun", 18), ("Jul", 25), ("Aug", 22)], "Wasser pro m² und Woche", "Richtwert in Litern für eingewachsenen Rasen ohne Regen")
          + txt("Bewässerung", "Wasser, wenn<br>es zählt.", "Lieber selten und gründlich: ein- bis zweimal pro Woche, früh am Morgen, statt jeden Abend ein bisschen.",
                '<a class="btn p" href="#rechner" style="margin-top:22px">Fläche berechnen →</a>')),
 ],
 "angebot": [
  dict(img="k-4", posm="20% 50%", tr="match:11,7,22,76", alt="Eine Hand fotografiert mit dem Handy die kahle Gartenecke",
       ov=txt("Angebot per Foto", "Ein Foto.<br>Mehr nicht.", "Querformat, ganze Fläche, bei Tageslicht. Alles andere sehen wir auf dem Bild.")),
  dict(img="k-5b", posm="45% 50%", tr="fade", alt="Die kahle Gartenecke, über dem Boden liegt ein Messraster",
       ov='<div class="fit">%s</div>' % grid([(40, 55), (118, 56), (160, 90), (0, 90)])
          + txt("Fläche aus dem Foto", '<span data-count="36" data-span=".12,.62">0</span> m²', "8,50 × 4,25 m, ermittelt aus Foto und Ihren Schritten. Ganz ohne Termin vor Ort.")),
  dict(img="k-6", posm="50% 50%", alt="Draufsicht auf die geplante Gartenecke mit Terrasse, Rasen und Beeten",
       ov='<div class="fit">%s</div>' % dims(29, 12, 130, 73, 77, "8,50 m", "4,25 m")
          + txt("Ihre Skizze", "So könnte es<br>werden.", "Sie bekommen eine Skizze mit Schichten, Ablauf und Dauer. Erst wenn etwas unklar bleibt, kommen wir vorbei.",
                '<a class="btn p" href="#kontakt" style="margin-top:22px">Skizze anfordern →</a>')),
 ],
 "gehoelzschnitt": [
  dict(img="k-7", posm="45% 50%", tr="zoom:54,35", alt="Der alte Apfelbaum im Winterlicht, drei Äste sind markiert",
       ov='<div class="fit">%s%s%s</div>' % (ring(16, 50, .15), ring(54, 35, .3), ring(72, 24, .45))
          + txt("Gehölzschnitt", "Drei Schnitte.<br>Nicht dreißig.", "Ein alter Obstbaum braucht wenige, gezielte Schnitte. Wer zu viel nimmt, erntet Wasserschosse.")),
  dict(img="k-8", v="kv3", posm="55% 50%", tr="fade", alt="Eine Astsäge setzt genau am Astring des Apfelbaums an",
       ov='<div class="fit">%s</div>' % hl(47, 47, 10, "Schnitt am Astring", "die Wunde schließt sich von selbst", .2).replace('class="hl"', 'class="hl solo"')
          + txt("Der richtige Schnitt", "Am Astring,<br>nicht am Stamm.", "Zu nah am Stamm oder ein langer Stummel: Dann zieht Fäulnis ein. Am Astring wächst die Wunde zu.")),
  dict(img="k-9", posm="40% 50%", alt="Die ausgelichtete Krone des Apfelbaums mit Sonne, die durch die Äste fällt",
       ov=cal() + txt("Wann", "Januar<br>bis März.", "Obstbäume schneiden wir im Winter, an frostfreien Tagen. Für starke Rückschnitte von Hecken gilt vom 1. März bis 30. September Schonzeit (§ 39 BNatSchG).")),
 ],
}

def story_html(slug):
    S = STORY.get(slug)
    if not S: return ""
    ms, os_, dots = [], [], []
    for i, b in enumerate(S):
        ms.append('<div class="sst-m" data-i="%d" data-img="%s"%s data-posm="%s" data-tr="%s"><img alt="%s" decoding="async"><video muted playsinline preload="none" aria-hidden="true"></video></div>' % (
            i, b["img"], ' data-v="%s"' % b["v"] if b.get("v") else "", b.get("posm", "50% 50%"), b.get("tr", "fade"), E(b["alt"])))
        os_.append('<div class="sst-o" data-i="%d">%s</div>' % (i, b["ov"]))
        dots.append('<button type="button" aria-label="Station %d"><i></i></button>' % (i + 1))
    return ('<section class="sst" style="--n:%d" aria-label="Scroll-Kapitel">\n<div class="sst-stage">%s%s<div class="sst-dots">%s</div></div>\n</section>\n' % (
        len(S), "".join(ms), "".join(os_), "".join(dots)))
