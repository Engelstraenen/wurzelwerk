#!/usr/bin/env python3
"""Leistungs-Kapitel: Layout-Prüfung je Station und Größe (Querscroll, Text außerhalb, Überlappung von Textblöcken, Schrift < 12 px, Tipp-Flächen < 44 px, Kopfzeile rechts im Bild).
Start: python3 tools/story_mobil.py"""
from playwright.sync_api import sync_playwright
JS = r"""()=>{const W=innerWidth,H=innerHeight,o=document.querySelector('.sst-o.on');const r=[];if(!o)return ['keine Station sichtbar'];
const els=[...o.querySelectorAll('h2,p,a,button,.hl .lab,.lg span,.cal3,.sbars,.dims span')].filter(e=>{const s=getComputedStyle(e);return s.display!='none'&&s.visibility!='hidden'&&+s.opacity>.05&&e.getBoundingClientRect().width>0});
const bx=els.map(e=>[e,e.getBoundingClientRect()]);
for(const [e,b] of bx){const n=(e.className||e.tagName)+':'+(e.textContent||'').trim().slice(0,18);
 if(b.left<-1||b.right>W+1||b.top<-1||b.bottom>H+1)r.push('raus '+n+' '+[b.left,b.top,b.right,b.bottom].map(Math.round));
 const fs=parseFloat(getComputedStyle(e).fontSize);if(/^(P|H2|A|BUTTON)$/.test(e.tagName)&&fs<12)r.push('klein '+fs+' '+n);
 if(/^(A|BUTTON)$/.test(e.tagName)&&b.height<44)r.push('tipp '+Math.round(b.height)+' '+n);}
for(let i=0;i<bx.length;i++)for(let j=i+1;j<bx.length;j++){const[a,A]=bx[i],[c,C]=bx[j];if(a.contains(c)||c.contains(a))continue;
 const ix=Math.min(A.right,C.right)-Math.max(A.left,C.left),iy=Math.min(A.bottom,C.bottom)-Math.max(A.top,C.top);if(ix>4&&iy>4)r.push('ueberlapp '+(a.textContent||'').trim().slice(0,14)+' | '+(c.textContent||'').trim().slice(0,14));}
const hd=[...document.querySelectorAll('header *, .top *, nav *')].filter(e=>e.getBoundingClientRect().width>0&&getComputedStyle(e).visibility!='hidden');
const mr=Math.max(0,...hd.map(e=>e.getBoundingClientRect().right));if(mr>W+1)r.push('kopf rechts '+Math.round(mr));
const qs=document.documentElement.scrollWidth-W;if(qs>0)r.push('querscroll '+qs);return r;}"""
SZ = ["390x844", "360x740", "430x932", "844x390", "1081x800", "1280x800", "1440x900", "1600x900"]
bad = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    for sz in SZ:
        w, h = map(int, sz.split("x")); m = w < 900
        for slug in ("rasen", "angebot", "gehoelzschnitt"):
            pg = b.new_page(viewport={"width": w, "height": h}, is_mobile=m, has_touch=m); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto("http://127.0.0.1:4430/leistungen/%s.html" % slug, wait_until="domcontentloaded"); pg.wait_for_timeout(1500)
            pg.add_style_tag(content="html{scroll-behavior:auto!important}")
            n = pg.evaluate("document.querySelectorAll('.sst-m').length")
            for i in range(n):
                pg.evaluate("([i,n])=>{const s=document.querySelector('.sst');scrollTo(0,s.offsetTop+(s.offsetHeight-innerHeight)*(i+.6)/n)}", [i, n])
                pg.wait_for_timeout(700)
                r = pg.evaluate(JS)
                if r: bad += 1; print(sz, slug, i + 1, r[:4])
            if errs: print(sz, slug, "FEHLER", errs[:2]); bad += 1
            pg.close()
    b.close()
print("fertig, Befunde:", bad)
