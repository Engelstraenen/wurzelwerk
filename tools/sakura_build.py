#!/usr/bin/env python3
"""Baut site/sakura/index.html aus der motionsites-Vorlage „Sakura QR“ (vorlage/sakura/original.html).
Übernommen: Three.js-Szene (3D-Tonbaum baum.glb, Licht, Schatten, Blütenblätter, Ziehen zum Drehen, Wind).
Entfernt: QR-Code (Bibliothek, Link-Feld, Teilen, QR-Draufsicht), Swatches/Knöpfe der Vorlage.
Neu: Scrollen = Kamera kreist einmal um den Baum, Jahreszeiten färben Baum/Boden/Partikel,
Story-Stationen mit Daten + Fotos, Jahreszeiten-Schalter, Olive/Rosé.
Start: python3 tools/sakura_build.py"""
import os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(R, "vorlage", "sakura", "original.html")).read()
importmap = re.search(r'<script type="importmap">.*?</script>', src, re.S).group(0)
js = re.search(r'<script type="module">(.*?)</script>', src, re.S).group(1)

def rep(old, new, count=1):
    global js
    assert old in js, "fehlt: " + old[:60]
    js = js.replace(old, new, count)

rep("const TREE_URL = 'https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20261018_171945_1dc5b1e5-4084-4243-91fa-7685bc18c495.glb';", "const TREE_URL = 'baum.glb';")
rep("const DEFAULT_URL = 'https://yoursite.com';", "")
# Jahreszeiten statt Farb-Swatches
rep(re.search(r"const PALETTES = \[.*?\];", js, re.S).group(0), """const PALETTES = [
  { name:'Frühling', tint:'#f6b3c4', deep:'#b8506c', tile:'#dfe6cf', amt:0 },
  { name:'Sommer',   tint:'#86b25a', deep:'#2f5a22', tile:'#c9dbb0', amt:1 },
  { name:'Herbst',   tint:'#e39a45', deep:'#8a3a12', tile:'#e3d2b4', amt:1 },
  { name:'Winter',   tint:'#f4f3f0', deep:'#6b6560', tile:'#eef1f4', amt:1 },
];""")
# QR-Bibliothek raus, Garten-Plan statt QR-Modulen (Ring aus Beeten, Weg nach vorn, Hochbeete)
rep("qrcode.stringToBytes = qrcode.stringToBytesFuncs['UTF-8'];", """function gardenPlan(){
  const N = 21, c = (N - 1) / 2;
  return { getModuleCount: () => N, isDark: (r, k) => {
    const d = Math.hypot(r - c, k - c);
    const path = Math.abs(k - c) <= 1 && r > c + 2;          // Weg nach vorn
    if (path) return false;
    if (d > 6.2 && d < 7.6) return true;                       // runder Beet-/Heckenring
    if (r < 4 && k > 13 && (r + k) % 2 === 0) return true;     // Hochbeet hinten rechts
    if (r > 15 && k < 5 && (r * k) % 3 === 0) return true;      // Staudengruppe vorn links
    return false; } };
}""")
rep("""  const q = qrcode(0, 'M');
  q.addData(text);
  q.make();""", "  const q = gardenPlan();")
# Tippen auf den Baum: Blütenstoß statt QR
rep("""    if (qrTarget === 1) setQR(false);
    else if (hit === 'tree') setQR(true);""", """    if (hit === 'tree'){ pulse = 1; for (let n = 0; n < 30; n++) spawnPetal(true); }""")
rep("canvas.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' '){ e.preventDefault(); setQR(qrTarget === 0); } });", "")
# Link/Teilen-Block + Swatch-/Knopf-Logik raus, Jahreszeiten-API rein
a = js.index("/* URL + share */"); b = js.index("/* =========================================================\n   Loop")
js = js[:a] + """/* Jahreszeiten: färben Baum, Boden und Partikel */
let season = 0;
function setSeason(i, burst){
  if (i === season && !burst) return;
  season = i;
  const p = PALETTES[i];
  colorState.index = i;
  colorState.tintTarget.set(p.tint);
  colorState.deepTarget.set(p.deep);
  colorState.amtTarget = (p.amt === 0 && treeGroup.children.some(c => c.isMesh && c.material.map)) ? 0 : 1;
  tileTarget.set(p.tile);
  if (burst){ pulse = 1; for (let n = 0; n < 40; n++) spawnPetal(true); }
}
const tileTarget = new THREE.Color(PALETTES[0].tile);
tileMat.color.set(PALETTES[0].tile);
/* Scrollen: Kamera kreist einmal um den Baum (0–360°) */
let scrollP = 0;
function readScroll(){
  const st = document.getElementById('story');
  const h = st.offsetHeight - innerHeight;
  scrollP = h > 0 ? Math.min(1, Math.max(0, -st.getBoundingClientRect().top / h)) : 0;
}
addEventListener('scroll', readScroll, { passive: true });
window.WW3D = { setSeason: (i) => setSeason(i, true), get p(){ return scrollP; }, dbg: () => ({ season, scrollP, amt: colorState.amt, amtT: colorState.amtTarget, tint: colorState.tint.getHexString(), u: treeUniforms.uAmt.value }) };
const breeze = false;
""" + js[b:]
# Loop: Drehung = Scroll + gezogener Versatz, der zurückfedert
rep("""  if (qrTarget === 0 && qrP === 0){
    if (!down){
      yaw += yawVel * dt;
      yawVel *= Math.pow(0.04, dt);
    }
  } else {
    yaw = THREE.MathUtils.lerp(yawFrom, yawTo, qrEase);
    if (qrP === 0) yawVel = 0;
  }
  world.rotation.y = yaw;""", """  if (!down){
    yaw += yawVel * dt;
    yawVel *= Math.pow(0.04, dt);
    yaw *= Math.pow(0.35, dt);            // gezogener Versatz federt sanft zurück
  }
  readScroll();
  scrollEase += (scrollP - scrollEase) * (1 - Math.exp(-dt * 5));
  world.rotation.y = ISO_YAW + scrollEase * Math.PI * 2 + yaw + t * 0.02;
  const si = window.WW_SEASON == null ? 0 : window.WW_SEASON;   // Jahreszeit der sichtbaren Station
  if (si !== season) setSeason(si, true);
  tileMat.color.lerp(tileTarget, 1 - Math.exp(-dt * 2.5));""")
rep("let yaw = ISO_YAW, yawVel = 0, yawFrom = ISO_YAW, yawTo = 0;", "let yaw = 0, yawVel = 0, yawFrom = 0, yawTo = 0, scrollEase = 0;")
rep("""  if (autoBloom){
    autoBloomTimer += dt;
    if (autoBloomTimer > 3.6){ autoBloomTimer = 0; setPalette((colorState.index + 1) % PALETTES.length, true); }
  }""", "")
rep("buildGarden(currentURL(), true);", "buildGarden('', true);")
# Kamera etwas näher und ruhiger, Platz für Text links
rep("camera.setViewOffset(w, h, 0, (uiH - topPad) / 2, w, h);", "camera.setViewOffset(w, h, w > 900 ? w * 0.2 : 0, (uiH - topPad) / 2 + (w <= 900 ? h * 0.14 : 0), w, h);")
rep("frame.isoR = Math.max(4.9 * k / t, 5.0 / (t * aspect));", "frame.isoR = Math.max(4.6 * k / t, 4.7 / (t * aspect)) * (aspect < .8 ? 1.05 : 1);")

html = open(os.path.join(R, "tools", "sakura_page.html")).read()
html = html.replace("<!--IMPORTMAP-->", importmap).replace("/*SCENE*/", js)
os.makedirs(os.path.join(R, "site", "sakura"), exist_ok=True)
open(os.path.join(R, "site", "sakura", "index.html"), "w").write(html)
print("ok", len(html))
