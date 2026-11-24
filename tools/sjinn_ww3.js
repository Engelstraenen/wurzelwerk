// WURZELWERK: 3 Storyboard-Varianten, max. 2 eigene Aufträge gleichzeitig (sjinn GPT Image 2, Unlimited)
(() => {
const COMMON = `A professional website design storyboard sheet, 16:9, a clean 3x3 grid of nine photorealistic website screenshots with thin gutters, each panel with a small German caption and number 1–9. The website is for a German garden and landscaping company called "WURZELWERK". Core idea: ONE real back garden of a German family house goes through ONE whole year as the visitor scrolls, the garden visibly changes with the seasons and with the work of the landscapers. Modern landscapers in dark workwear with professional tools (mini excavator, plate compactor, string line, pruning shears, pop-up sprinklers, natural stone). Recruiting, reviews and the contact/offer are built INTO the seasons. Photorealistic photography inside realistic, premium web UI, true-to-life colors, not CGI. Avoid: clichés, garden gnomes, straw hats, cartoon, star ratings with numbers, euro prices, cluttered layout, dark navy with orange, misspelled text.`;
const JOBS = [
{ id: 'WWJ3A', p: `WWJ3A ${COMMON}
VARIANT "Jahresuhr". Color world: warm linen background #efe9df, brick red accent #b8432a for pointer and buttons, earth-black ink. Staging: the camera stays FIXED on the same garden in every panel, only the season and the work change. Navigation: a large thin circular year dial with 12 month ticks (JAN … DEZ) at the bottom center, brick-red pointer, it rotates as you scroll. Elegant large serif headlines, frosted linen glass cards.
1 "Start · März": early spring, bare soil beds, mini excavator at the edge, headline "Ein Garten. Ein Jahr.", dial pointer on MÄR.
2 "April · Pflanzung": landscaper kneeling, planting young shrubs along a taut string line, headline "Frühling. Wir pflanzen."
3 "Mai · Angebot": same garden greening, glass card "Foto schicken – Angebot in 48 h" with a phone photo thumbnail and red button "Foto senden".
4 "Juli · Rasen": lush summer lawn, pop-up sprinklers spraying glittering arcs, headline "Sommer. Wir halten ihn grün."
5 "August · Bewertungen": same summer garden at golden hour with people on a new stone terrace, glass strip "Google Bewertungen" with star outlines filling.
6 "Oktober · Ausbildung": autumn leaves, landscaper pruning a tree, young apprentice raking leaves into a wheelbarrow, big kinetic words "Draußen. Team. Sinn." and red button "In 60 Sekunden bewerben".
7 "Januar · Planung": light snow, granite path and dry stone wall, thin white plan lines with m² labels drawn over the photo, card "Winter. Wir planen Ihren Frühling." red button "Planungstermin".
8 "Jahresuhr": close-up of the dial with four season arcs tinted (fresh green, gold, rust, ice blue), center text "Oktober · Gehölzschnitt", a hand cursor dragging it.
9 "Handy": two smartphones in portrait, spring garden with a compact month strip at the bottom, autumn garden with the apprentice card.` },
{ id: 'WWJ3B', p: `WWJ3B ${COMMON}
VARIANT "Rundgang um den Baum". Color world: deep olive green background #2f3a24, soft rosé accent #e8b4b0 for buttons and highlights, cream text. Staging: a single old apple tree stands in the middle of the garden; as you scroll the camera ORBITS slowly around this tree, each season is one quarter turn, so every panel shows the tree from a different side and the garden behind it changes. Navigation: a thin arc of the sun's path across the top of the screen, a small rosé sun dot moves along it (low in winter, high in summer) with the four seasons marked. Clean modern sans-serif headlines, rosé pill buttons.
1 "Start · Frühling Nordseite": apple tree in blossom, behind it raw soil and a mini excavator, headline "Ein Baum. Vier Seiten. Ein Jahr.", sun dot low on the left.
2 "Drehung · Frühling Ostseite": camera has turned, landscapers lay out a new terrace with string lines and a plate compactor, headline "Frühling. Neu anlegen."
3 "Frühling · Angebot": close view under the blossoms, a smartphone in a hand photographing the bare garden corner, rosé card "Foto schicken, wir rechnen den Plan".
4 "Sommer Südseite": camera turned again, tree full of green leaves, lush lawn rolled out, sprinklers, sun dot at the top of the arc, headline "Sommer. Gepflegt, nicht geplagt."
5 "Sommer · Bewertungen": family under the tree on the new terrace, rosé review cards floating like leaves "Google Bewertungen".
6 "Herbst Westseite": tree with red apples, landscaper on a ladder pruning, apprentice with a leaf blower, headline "Herbst. Komm ins Team." rosé button "60-Sekunden-Bewerbung".
7 "Herbst · Karriere": portrait of the young apprentice holding a crate of apples, kinetic words "Führerschein. Feste Crew. Draußen."
8 "Winter Nordseite": full circle, bare tree with snow, granite path and stone wall lit by garden lights, headline "Winter. Wir planen Ihren Frühling." rosé contact card.
9 "Handy": two smartphones in portrait, swipe gesture rotates the tree, sun arc at the top.` },
{ id: 'WWJ3C', p: `WWJ3C ${COMMON}
VARIANT "Abreißkalender". Color world: chalk white paper #f6f5f1, cobalt blue accent #1f4fd1 for print, tabs and buttons, black text. Staging: the whole website is a large photographic wall calendar; each month is a printed calendar sheet with a big garden photo, the date grid below in cobalt print; as you scroll, the current sheet TEARS OFF and curls away (realistic torn paper edge, perforation) revealing the next month with the SAME garden one month later. Navigation: 12 cobalt index tabs (JAN–DEZ) sticking out on the right edge, the current tab pulled out. Bold grotesque headlines printed like calendar typography, cobalt stamps for calls to action.
1 "Start · März-Blatt": calendar sheet with the bare spring garden and a mini excavator, big print "WURZELWERK – Ihr Gartenjahr", tab MÄR pulled out.
2 "Scroll · Blatt reißt": the March sheet is tearing off diagonally, underneath the April photo with landscapers planting shrubs along a string line.
3 "April · Angebot": on the date grid a cobalt hand-stamped note "Foto schicken – Angebot in 48 h" with a phone photo pinned with a clip.
4 "Juli-Blatt": summer garden, lush lawn, sprinklers, headline "Juli: Rasen, Wasser, Pflege".
5 "August · Bewertungen": the date grid filled with small cobalt handwritten notes from customers like a fridge calendar, label "Google Bewertungen" with star outlines.
6 "Oktober-Blatt": autumn, landscaper pruning, apprentice raking leaves, headline "Oktober: Ausbildung startet – bewirb dich".
7 "Oktober · Bewerbung": a cobalt stamped tear-off coupon at the bottom of the sheet "60-Sekunden-Bewerbung" with dotted perforation, a finger tearing it.
8 "Januar-Blatt": snowy garden with granite path and stone wall, the date grid turns into a planning grid with m² sketches, cobalt button "Planungstermin".
9 "Handy": two smartphones in portrait, swipe up tears the sheet, the month tabs as a horizontal strip at the top.` }
];
const W = window.WWQ3 = { jobs: JOBS, sent: {}, got: {}, log: [], limN: 0, runId: Date.now() };
new MutationObserver(ms => { for (const m of ms) for (const n of m.addedNodes) { if (/maximum limit|concurrent task/i.test(n.textContent || '')) W.limN++; } }).observe(document.body, { childList: true, subtree: true });
const sleep = ms => new Promise(r => setTimeout(r, ms));
W.ok = () => { const b = document.body.innerText; return /Unlimited · On/.test(b) && /\b0 credits/.test(b) && /GPT Image 2/.test(b) && /16:9/.test(b); };
W.scan = () => { for (const im of document.querySelectorAll('img')) { const a = im.alt || ''; for (const j of JOBS) if (a.startsWith(j.id) && !W.got[j.id]) W.got[j.id] = im.src; } };
W.running = () => Object.keys(W.sent).filter(k => !W.got[k]).length;
W.send = async (j) => {
  const ta = document.querySelector('textarea'); const set = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
  set.call(ta, ''); ta.dispatchEvent(new Event('input', { bubbles: true })); set.call(ta, j.p); ta.dispatchEvent(new Event('input', { bubbles: true }));
  await sleep(800);
  if (!W.ok()) { W.log.push('NOT-OK ' + j.id); return false; }
  const btn = [...document.querySelectorAll('button')].find(b => b.textContent.trim() === 'Generate');
  if (!btn || btn.disabled) { W.log.push('NOBTN ' + j.id); return false; }
  const l0 = W.limN; btn.click(); await sleep(20000);
  if (W.limN > l0) { W.log.push('LIMIT ' + j.id + ' ' + new Date().toLocaleTimeString()); return false; }
  W.sent[j.id] = Date.now(); W.log.push('SENT ' + j.id + ' ' + new Date().toLocaleTimeString());
  set.call(ta, ''); ta.dispatchEvent(new Event('input', { bubbles: true }));
  return true;
};
W.loop = async () => { const id = W.runId;
  for (let i = 0; i < 200 && W.runId === id; i++) {
    W.scan();
    if (JOBS.every(j => W.got[j.id])) { W.log.push('ALL DONE'); break; }
    const next = JOBS.find(j => !W.sent[j.id]);
    if (next && W.running() < 2) { const ok = await W.send(next); if (!ok) { await sleep(45000); continue; } await sleep(3000); continue; }
    await sleep(30000);
  } };
W.loop();
})();
