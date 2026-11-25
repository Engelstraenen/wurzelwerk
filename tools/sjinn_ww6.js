// WURZELWERK Brücken-Fotos (Variante 1 + 2 kombiniert): sjinn GPT Image 2, 16:9, 4K, Unlimited, max. 2 eigene Aufträge.
(() => {
const ST = ' Photorealistic professional photograph, full-frame camera, macro or 50mm lens, natural light, realistic textures, true-to-life colors, subtle film grain, ultra sharp, 16:9. Same old apple tree garden of a modern white German house. No text, no letters, no logos, no watermark, no clichés, not CGI, no plastic look.';
const JOBS = [
 { id: 'WWB-1', p: 'Extreme macro photograph of a single fresh white apple blossom with soft pink edges, five petals, yellow stamens, the flower center exactly in the middle of the frame, a few more blossoms and young green leaves softly blurred around it, deep olive green soft background, gentle spring morning light, dew drops on the petals.' },
 { id: 'WWB-2', p: 'Backlit macro photograph of glittering water droplets from a garden sprinkler suspended in the warm evening air in front of a lush lawn, each droplet sparkling like a tiny light, round warm bokeh balls, some droplets glowing golden like string light bulbs, the old apple tree trunk softly blurred in the background, golden hour.' },
 { id: 'WWB-3', p: 'Macro photograph of a single apple leaf falling through the air in the center of the frame, the leaf half green and half turning orange-red from its edge, tiny water drops on it, the autumn garden with the old apple tree, red apples and orange leaves softly blurred behind, low warm sunlight, slight motion blur at the leaf edge.' },
 { id: 'WWB-4', p: 'Photograph of a ripe red apple falling in motion blur, caught at the moment just above a wooden crate full of red apples held by the gloved hands of a young landscaping apprentice in dark olive-green work clothes, autumn orange leaves and the gnarled apple tree trunk blurred behind, warm afternoon light, the crate in the lower center of the frame.' },
 { id: 'WWB-5', p: 'Close photograph of a young landscaping apprentice in a dark olive-green work jacket standing next to the bare old apple tree at the beginning of winter, exhaling a visible cloud of warm breath into the cold air, the breath dissolving into the first falling snowflakes, blue hour light, a warmly lit dry stone wall with LED lights blurred in the background, face partly turned away.' },
 { id: 'WWB-6', p: 'Wide photograph of soft morning mist drifting low across a freshly prepared spring garden around the old blossoming apple tree, backlit by the rising sun, light rays through the mist, the white modern house faint in the haze, very atmospheric, the mist covering the lower half of the frame, calm and quiet.' }
];
for (const j of JOBS) j.p = j.id + ' ' + j.p + ST;
const W = window.WWQ6 = { sent: {}, got: {}, log: [], limN: 0, runId: Date.now() };
new MutationObserver(ms => { for (const m of ms) for (const n of m.addedNodes) if (/maximum limit|concurrent task/i.test(n.textContent || '')) W.limN++; }).observe(document.body, { childList: true, subtree: true });
const sleep = ms => new Promise(r => setTimeout(r, ms));
const bar = () => [...document.querySelectorAll('button')].map(b => b.innerText.trim()).filter(t => /GPT Image|16:9|4K|2K|1K|Unlimited/.test(t)).join(' | ') + ' | ' + (document.body.innerText.match(/\b\d+ credits/) || [''])[0];
W.bar = bar;
const ok = () => { const b = bar(); return /GPT Image 2/.test(b) && /Unlimited · On/.test(b) && /\b0 credits/.test(b) && /16:9/.test(b) && /4K/.test(b); };
const scan = () => { for (const im of document.querySelectorAll('img')) { const a = im.alt || ''; for (const j of JOBS) if (a.startsWith(j.id + ' ') && !W.got[j.id] && im.src.includes('/result/')) W.got[j.id] = im.src.split('?')[0]; } };
W.loop = async () => { const id = W.runId;
  for (let i = 0; i < 200 && W.runId === id; i++) {
    scan(); if (JOBS.every(j => W.got[j.id])) { W.log.push('ALL DONE ' + new Date().toLocaleTimeString()); break; }
    for (const k of Object.keys(W.sent)) if (!W.got[k] && Date.now() - W.sent[k] > 25 * 60000) { W.log.push('TIMEOUT ' + k); delete W.sent[k]; }
    const running = Object.keys(W.sent).filter(k => !W.got[k]).length;
    const next = JOBS.find(j => !W.sent[j.id] && !W.got[j.id]);
    if (next && running < 2) {
      const ta = document.querySelector('textarea'); const set = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
      set.call(ta, ''); ta.dispatchEvent(new Event('input', { bubbles: true })); set.call(ta, next.p); ta.dispatchEvent(new Event('input', { bubbles: true }));
      await sleep(900);
      if (!ok()) { W.log.push('NOT-OK ' + bar()); await sleep(60000); continue; }
      const g = [...document.querySelectorAll('button')].find(b => b.textContent.trim() === 'Generate'); if (!g || g.disabled) { await sleep(60000); continue; }
      const l0 = W.limN; g.click(); await sleep(20000);
      if (W.limN > l0) { W.log.push('LIMIT ' + next.id); await sleep(90000); continue; }
      W.sent[next.id] = Date.now(); W.log.push('SENT ' + next.id + ' ' + new Date().toLocaleTimeString());
      set.call(ta, ''); ta.dispatchEvent(new Event('input', { bubbles: true })); await sleep(3000); continue;
    }
    await sleep(30000);
  } };
W.loop();
})();
