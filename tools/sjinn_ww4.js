// WURZELWERK Rundgang: 8 Seitenbilder, GPT Image 2, 16:9, 4K, Unlimited, max. 2 eigene Aufträge.
// Status: WW4.s / WW4.log / WW4.got · Stop: WW4.runId = 0
(() => {
const TREE = 'a large old apple tree with a thick gnarled trunk that forks into three main limbs at about 1.5 m height and a wide rounded crown, standing in the middle of the back garden of a modern white German family house with large floor-to-ceiling windows and a flat roof, the garden enclosed by a tall clipped hornbeam hedge';
const ST = ' Photorealistic professional photograph, full-frame camera, 24mm, eye level, natural light, realistic textures, true-to-life colors, subtle film grain, ultra sharp, 16:9. Modern landscapers wear modern dark olive-green work clothes with no logos. No text, no letters, no logos, no watermark, no clichés, no garden gnomes, no straw hats, not CGI, no plastic look.';
const REFTXT = ' Use the reference image only for the exact look of the apple tree (trunk shape, fork into three limbs, crown), the white house and the hedge; the camera now stands on a different side of the tree as described.';
const J = [
 { id: 'WWR-P1', p: `Spring morning, view from the north side of the garden: ${TREE}. The tree is in full white and pale pink blossom and stands in the center of the frame. Around it the old lawn has been dug up into raw brown soil, a small red and white tracked mini excavator on the right digs with its bucket, a landscaper with a spade works on the left, neighbouring houses and a cloudy bright sky behind the hedge. The left third of the image is calm for a headline.` },
 { id: 'WWR-P3', p: `Close-up under the white and pale pink blossoms of an old apple tree in a German garden in spring: a hand holds a modern smartphone horizontally on the left half of the frame and photographs a bare garden corner with raw soil, the phone screen clearly shows that photo of the bare soil corner and the hedge. Shallow depth of field, blossoms soft in the foreground, the right third of the frame is calm blurred garden for a card.` },
 { id: 'WWR-P7', p: `Autumn portrait of a confident young landscaping apprentice, about 18 years old, in modern dark olive-green work clothes and work gloves, holding a wooden crate full of red apples, standing slightly right of center next to the gnarled trunk of an old apple tree with red apples and orange leaves, warm low afternoon sun, he looks to the side and smiles, the left 40 percent of the frame is calm soft background for a headline.` },
 { id: 'WWR-P2', ref: 1, p: `Spring, the camera has moved to the east side of the same garden: ${TREE}. The blossoming tree stands left of center, the white house with its large windows is on the right. Two landscapers build a new terrace in front of the house: taut white string lines on wooden stakes mark the edges, one landscaper compacts a gravel bed with a yellow plate compactor, the other kneels and lays large grey porcelain pavers on the finished part. Soft morning light, the left third calm for a headline.` },
 { id: 'WWR-P4', ref: 1, p: `High summer, the camera has moved to the south side of the same garden: ${TREE}. The tree is full of dense green leaves and stands left of center, a freshly laid lush green lawn covers the garden, three pop-up sprinklers spray glittering arcs of water in the sunlight, the white house with a stone terrace and two loungers on the right in the background. Sunny warm afternoon, crisp, the left third calm for a headline.` },
 { id: 'WWR-P5', ref: 1, p: `Summer evening in the same garden: ${TREE}, green leaves. Under the tree on the new grey stone terrace four adults sit at a long wooden table with food and drinks, laughing, warm golden evening light through the leaves, string lights in the tree. Symmetrical composition, the tree trunk in the center, calm space on the left and right sides for cards.` },
 { id: 'WWR-P6', ref: 1, p: `Autumn, the camera has moved to the west side of the same garden: ${TREE}. The tree carries red apples and orange-brown leaves and stands in the center, one landscaper stands on an aluminium ladder against the crown and prunes branches with professional pruning shears, a young apprentice on the right clears the lawn with a backpack leaf blower, colourful leaves on the lawn, low golden sunlight. The left third calm for a headline.` },
 { id: 'WWR-P8', ref: 1, p: `Winter blue hour, the camera is back on the north side of the same garden, a full circle: ${TREE}. The tree is bare with a light layer of snow on its branches and stands in the center. A new curved granite paving path leads past it, a dry stone wall with built-in warm LED lights runs along the right side, a modern wooden garden house with a warmly lit window in the background, light snow on the ground. The left third calm for a headline.` }
];
for (const j of J) j.p = j.id + ' ' + j.p + (j.ref ? REFTXT : '') + ST;
const W = window.WW4 = { jobs: J, sent: JSON.parse(localStorage.WW4_SENT || '{}'), REFURL: localStorage.WW4_REF || '', got: JSON.parse(localStorage.WW4_GOT || '{}'), log: [], limN: 0, runId: Date.now(), s: 'init' };
const wk = new Worker(URL.createObjectURL(new Blob(['onmessage=e=>setTimeout(()=>postMessage(e.data.id),e.data.ms)'])));
let n = 0; const cb = {}; wk.onmessage = e => { cb[e.data](); delete cb[e.data]; };
const sleep = ms => new Promise(r => { const id = ++n; cb[id] = r; wk.postMessage({ id, ms }); });
if (window.__ww4Obs) window.__ww4Obs.disconnect();
window.__ww4Obs = new MutationObserver(ms => { for (const m of ms) for (const nd of m.addedNodes) if (/maximum limit|concurrent task/i.test(nd.textContent || '')) { W.limN++; return; } });
window.__ww4Obs.observe(document.body, { childList: true, subtree: true });
const bar = () => [...document.querySelectorAll('button')].map(b => b.innerText.trim()).filter(t => /GPT Image|16:9|4K|2K|1K|Unlimited/.test(t)).join(' | ') + ' | ' + (document.body.innerText.match(/\b\d+ credits/) || [''])[0];
W.bar = bar;
const ok = () => { const b = bar(); return /GPT Image 2/.test(b) && /Unlimited · On/.test(b) && /\b0 credits/.test(b) && /16:9/.test(b) && /4K/.test(b); };
const scan = () => { for (const im of document.querySelectorAll('img')) { const m = (im.alt || '').match(/^(WWR-P\d)/); if (m && im.src.includes('/result/') && !W.got[m[1]]) W.got[m[1]] = im.src.split('?')[0]; } localStorage.WW4_GOT = JSON.stringify(W.got); };
const btn = t => [...document.querySelectorAll('button,[role=button]')].find(b => ((b.getAttribute('aria-label') || '') + '|' + b.innerText).toLowerCase().includes(t.toLowerCase()));
const clearRefs = async () => { for (let k = 0; k < 6; k++) { const b = [...document.querySelectorAll('button')].find(b => /^Remove Image/.test(b.getAttribute('aria-label') || '')); if (!b) break; b.click(); await sleep(500); } };
const setRef = async src => {
  if (!document.querySelector('[role=dialog]')) { const b = btn('Add reference'); if (!b) return 'NOADD'; b.click(); await sleep(2000); }
  const dlg = document.querySelector('[role=dialog]'); if (!dlg) return 'NODLG';
  const clr = [...dlg.querySelectorAll('button')].find(b => /Clear selection/i.test(b.innerText)); if (clr) { clr.click(); await sleep(600); }
  const key = src.split('/').pop().split('.')[0];
  let img = [...dlg.querySelectorAll('img')].find(i => i.src.includes(key));
  for (let k = 0; !img && k < 8; k++) { const lm = [...dlg.querySelectorAll('button')].find(b => /Load more/i.test(b.innerText)); if (!lm) break; lm.click(); await sleep(2500); img = [...dlg.querySelectorAll('img')].find(i => i.src.includes(key)); }
  if (img) { let c = img; for (let k = 0; k < 7; k++) { c = c.parentElement; const sb = c && c.querySelector('button[aria-label^="Select image"]'); if (sb) { sb.click(); break; } } await sleep(600); }
  const use = [...dlg.querySelectorAll('button')].find(b => /^Use \d+ image|Apply selection/i.test(b.innerText.trim()));
  if (img && use && !use.disabled) { use.click(); await sleep(1200); return 'ok'; }
  const x = [...dlg.querySelectorAll('button')].find(b => b.innerText.trim() === 'Cancel' || b.getAttribute('aria-label') === 'Close'); x && x.click(); await sleep(600); return img ? 'NOUSE' : 'NOIMG';
};
W.setRef = setRef;
const send = async j => {
  await clearRefs();
  if (j.ref) { const r = await setRef(W.REFURL); if (r !== 'ok') { W.log.push('REF ' + r + ' ' + j.id); return false; } }
  const ta = document.querySelector('textarea'); const set = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
  set.call(ta, ''); ta.dispatchEvent(new Event('input', { bubbles: true })); set.call(ta, j.p); ta.dispatchEvent(new Event('input', { bubbles: true }));
  await sleep(1000);
  if (!ok()) { W.log.push('NOT-OK ' + bar()); return false; }
  const g = [...document.querySelectorAll('button')].find(b => b.textContent.trim() === 'Generate');
  if (!g || g.disabled) { W.log.push('NOBTN'); return false; }
  const l0 = W.limN; g.click(); await sleep(20000);
  if (W.limN > l0) { W.log.push('LIMIT ' + j.id + ' ' + new Date().toLocaleTimeString()); return false; }
  W.sent[j.id] = Date.now(); localStorage.WW4_SENT = JSON.stringify(W.sent); W.log.push('SENT ' + j.id + ' ' + new Date().toLocaleTimeString());
  set.call(ta, ''); ta.dispatchEvent(new Event('input', { bubbles: true }));
  return true;
};
W.loop = async () => { const id = W.runId;
  while (W.runId === id) {
    scan();
    for (const k of Object.keys(W.sent)) if (!W.got[k] && Date.now() - W.sent[k] > 20 * 60000) { W.log.push('TIMEOUT ' + k); delete W.sent[k]; }
    if (J.every(j => W.got[j.id])) { W.s = 'ALL DONE ' + new Date().toLocaleTimeString(); break; }
    const running = Object.keys(W.sent).filter(k => !W.got[k]).length;
    const next = J.find(j => !W.got[j.id] && !W.sent[j.id] && (!j.ref || W.REFURL));
    W.s = 'running ' + running + ' next ' + (next ? next.id : '-') + ' ' + new Date().toLocaleTimeString();
    if (next && running < 2) { const okk = await send(next); await sleep(okk ? 3000 : 45000); continue; }
    await sleep(30000);
  } };
W.loop();
})();
