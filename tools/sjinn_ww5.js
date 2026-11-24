// WURZELWERK Übergänge: 2 Storyboard-Varianten (sjinn GPT Image 2, 16:9, 2K, Unlimited), max. 2 eigene Aufträge.
(() => {
const BASE = `Photorealistic website scrollytelling storyboard sheet, 16:9, a clean 3x3 grid of nine photorealistic panels with thin gutters on deep olive green (#2f3a24), each panel numbered 1-9 with a short German caption. Website of a German garden and landscaping company "WURZELWERK": the camera walks once around ONE old apple tree (thick gnarled trunk forking into three limbs) in the back garden of a modern white house through one whole year. Rosé (#e8b4b0) accent for buttons and a thin sun-path arc navigation at the top of every panel. KEY IDEA: ONE continuous story with NO hard cuts — every panel shows the MOMENT OF TRANSITION where one season visibly turns into the next. Landscapers in dark olive-green workwear without logos. Photoreal, true-to-life colors, cinematic, not CGI. No clichés, no garden gnomes, no straw hats, no prices, no misspelled text.`;
const JOBS = [
 { id: 'WWU-A', p: `WWU-A ${BASE}
VARIANT "Natur-Brücken": each transition is carried by one real object that travels from one scene into the next, with motion trails.
1 "Start": bare dug-up spring garden with mini excavator, white blossom petals blowing across the screen over the headline "Ein Baum. Vier Seiten. Ein Jahr.".
2 "Blüte wird Bildschirm": extreme close-up of a single apple blossom filling the frame, its center turning into a smartphone screen.
3 "Foto wird Garten": a hand holds a phone showing a photo of a bare corner; the photo on the screen expands beyond the phone edges and becomes the real summer lawn behind it.
4 "Tropfen werden Lichter": glittering water drops from a pop-up sprinkler hang in the air and turn into the warm bulbs of a string light at dusk.
5 "Abendtafel": friends at a table under the tree, rosé review cards falling slowly like leaves.
6 "Blatt färbt sich": macro of one green apple leaf turning orange from the edge while it falls, autumn garden blurred behind.
7 "Apfel fällt in die Kiste": a red apple falling from the branch in motion blur, landing in the wooden crate of a young apprentice, headline "Führerschein. Feste Crew. Draußen.".
8 "Atem wird Schnee": the apprentice's breath in cold air dissolves into falling snowflakes over the winter garden with lit stone wall, headline "Winter. Wir planen Ihren Frühling." and rosé contact card.
9 "Handy": two smartphones in portrait showing the same transitions vertically, a finger swiping.` },
 { id: 'WWU-B', p: `WWU-B ${BASE}
VARIANT "Eine Kamerafahrt": the whole page is ONE unbroken camera move orbiting the tree, scenes are sewn together by soft natural veils (morning mist, sprinkler spray, autumn fog, snowfall) the camera passes through, like a single long film take.
1 "Start": low camera at the north side, spring morning mist lifting off the dug-up soil, headline "Ein Baum. Vier Seiten. Ein Jahr.".
2 "Kamera kreist": motion-blurred orbit to the east side, the mini excavator leaving the frame, landscapers with string lines appearing.
3 "Durch die Blüten": the camera pushes through a curtain of blossoming branches, blossoms soft in front of the lens, an offer card in rosé sliding in on the right.
4 "Durch den Sprühnebel": the camera moves through the backlit spray of a sprinkler, rainbow in the mist, summer lawn appearing behind.
5 "Abendlicht": the same camera move continues into golden evening under the tree, string lights, review cards floating.
6 "Herbstnebel": autumn fog drifting across the frame, the tree with red apples emerging, ladder and leaf blower.
7 "Push-in zum Stamm": the camera glides close to the trunk where a young apprentice holds a crate of apples, big kinetic words "Führerschein. Feste Crew. Draußen.".
8 "Schneetreiben": snowfall sweeps across the lens and the full circle closes at the north side in blue hour, lit stone wall, rosé contact card.
9 "Handy": two smartphones in portrait showing the same continuous film, a thin sun-path arc at the top, a finger swiping.` }
];
const W = window.WWQ5 = { sent: {}, got: {}, log: [], limN: 0, runId: Date.now() };
new MutationObserver(ms => { for (const m of ms) for (const n of m.addedNodes) if (/maximum limit|concurrent task/i.test(n.textContent || '')) W.limN++; }).observe(document.body, { childList: true, subtree: true });
const sleep = ms => new Promise(r => setTimeout(r, ms));
const ok = () => { const b = document.body.innerText; return /Unlimited · On/.test(b) && /\b0 credits/.test(b); };
const scan = () => { for (const im of document.querySelectorAll('img')) { const a = im.alt || ''; for (const j of JOBS) if (a.startsWith(j.id) && !W.got[j.id] && im.src.includes('/result/')) W.got[j.id] = im.src.split('?')[0]; } };
W.loop = async () => { const id = W.runId;
  for (let i = 0; i < 120 && W.runId === id; i++) {
    scan(); if (JOBS.every(j => W.got[j.id])) { W.log.push('ALL DONE'); break; }
    const next = JOBS.find(j => !W.sent[j.id]);
    if (next) {
      const ta = document.querySelector('textarea'); const set = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
      set.call(ta, ''); ta.dispatchEvent(new Event('input', { bubbles: true })); set.call(ta, next.p); ta.dispatchEvent(new Event('input', { bubbles: true }));
      await sleep(900);
      if (!ok()) { W.log.push('NOT-OK'); await sleep(45000); continue; }
      const g = [...document.querySelectorAll('button')].find(b => b.textContent.trim() === 'Generate'); if (!g || g.disabled) { await sleep(45000); continue; }
      const l0 = W.limN; g.click(); await sleep(20000);
      if (W.limN > l0) { W.log.push('LIMIT ' + next.id); await sleep(45000); continue; }
      W.sent[next.id] = Date.now(); W.log.push('SENT ' + next.id + ' ' + new Date().toLocaleTimeString());
      set.call(ta, ''); ta.dispatchEvent(new Event('input', { bubbles: true })); await sleep(3000); continue;
    }
    await sleep(30000);
  } };
W.loop();
})();
