// WURZELWERK Rundgang: 7 Übergangs-Clips auf Dreamina (Seedance 2.5, First and last frames, 16:9 720P, 5 s, Unlimited).
// Einspielen: <input type=file id=wwjs> + file_upload, dann (0,eval)(await wwjs.files[0].text())
// Ablauf je Clip: Bilder in <input id=wwin> laden (P_n.jpg, P_n+1.jpg) -> DW.prep(n) -> Leiste per zoom prüfen -> DW.safeGen()
(() => {
  const ST = ' Photorealistic, natural light, true-to-life colors, realistic motion, stable geometry, the old apple tree keeps its exact shape (thick gnarled trunk forking into three main limbs), the white modern house and the hornbeam hedge stay consistent. ACTION STARTS IMMEDIATELY IN THE VERY FIRST FRAME, no still moment. One continuous shot, no cuts. Landscapers wear dark olive-green work clothes without logos. No text, no logos, no clichés, no garden gnomes.';
  const P = {
    1: 'WWC1 Smooth continuous camera orbit around the old apple tree in a German back garden: the camera circles about 90 degrees to the right around the blossoming tree at eye level, from the north side to the east side. While the camera moves, the dug-up soil turns into a prepared gravel bed, the mini excavator drives out of frame to the right, two landscapers appear at the new terrace with string lines and a plate compactor. Spring morning light.',
    2: 'WWC2 The camera glides slowly forward under the blossoming branches of the old apple tree towards a bare garden corner, white and pink blossoms pass close in front of the lens, a hand with a smartphone rises into the frame from the left and frames the bare soil corner on its screen. Spring, soft light, shallow depth of field.',
    3: 'WWC3 The hand with the smartphone lowers out of the frame, the camera pulls back and orbits to the south side of the old apple tree. Time-lapse of the season changing from spring to summer during the move: the blossoms fall like snow, the crown fills with dense green leaves, fresh rolled turf covers the garden, pop-up sprinklers start to spray glittering arcs. Bright summer afternoon at the end.',
    4: 'WWC4 The camera moves slowly towards the trunk of the old apple tree and under its green crown while the day turns into a warm summer evening: string lights in the branches switch on one by one, four friends sit down at a long wooden table on the new stone terrace under the tree, food and drinks on the table, golden evening light.',
    5: 'WWC5 Smooth camera orbit about 90 degrees around the old apple tree from the terrace side to the west side. Time-lapse of the season changing from late summer to autumn during the move: the table and people fade away, the leaves turn orange and brown, red apples ripen on the branches, leaves drift onto the lawn, a landscaper sets an aluminium ladder against the crown, an apprentice with a backpack leaf blower appears on the right. Low golden autumn sun.',
    6: 'WWC6 The camera pushes in slowly towards the gnarled trunk of the old apple tree in autumn, the ladder and the leaf blower move out of frame, a young apprentice in dark olive-green work clothes steps into the frame from the right carrying a wooden crate full of red apples, stops next to the trunk and smiles to the side. Warm low afternoon sun, orange leaves.',
    7: 'WWC7 The apprentice walks out of the frame, the camera pulls back and orbits about 90 degrees around the old apple tree to the north side. Time-lapse from autumn to winter during the move: the last leaves fall, the branches become bare, light snow begins to fall and covers the ground and the branches, the day turns into blue hour, warm LED lights in a new dry stone wall along a curved granite path switch on. Calm winter evening at the end.'
  };
  for (const k in P) P[k] += ST;
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const main = el => el.getBoundingClientRect().left > 400;
  const W = window.DW = { P, log: [], lim: 0 };
  if (window.__dwObs) window.__dwObs.disconnect();
  window.__dwObs = new MutationObserver(ms => { for (const m of ms) for (const n of m.addedNodes) if (/up to 1 generation at a time/i.test(n.textContent || '')) { W.lim++; return; } });
  window.__dwObs.observe(document.body, { childList: true, subtree: true });
  const box = t => { const e = [...document.querySelectorAll('*')].find(e => e.children.length === 0 && (e.innerText || '').trim() === t); if (!e) return null; let c = e; for (let k = 0; k < 3; k++) c = c.parentElement; return c; };
  W.clear = async () => { for (let k = 0; k < 4; k++) { const b = document.querySelector('div[aria-label="Remove · Reference"],[aria-label^="Remove"]'); if (!b) break; b.click(); await sleep(500); } };
  const drop = (el, f) => { const dt = new DataTransfer(); dt.items.add(f); for (const ev of ['dragenter', 'dragover', 'drop']) el.dispatchEvent(new DragEvent(ev, { bubbles: true, cancelable: true, dataTransfer: dt })); };
  W.prep = async n => {
    const fs = document.getElementById('wwin').files; if (fs.length < 2) return 'NOFILES';
    await W.clear();
    const a = box('First frame'), b = box('Last frame'); if (!a || !b) return 'NOBOX';
    drop(a, fs[0]); await sleep(4000);
    const b2 = box('Last frame'); if (!b2) return 'NOLAST'; drop(b2, fs[1]); await sleep(4000);
    const ta = document.querySelector('textarea.lv-textarea'); ta.focus();
    Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set.call(ta, P[n]); ta.dispatchEvent(new Event('input', { bubbles: true }));
    await sleep(800);
    return W.state();
  };
  W.state = () => {
    const sw = document.querySelector('[role=switch]');
    const bar = [...document.querySelectorAll('*')].filter(e => e.children.length === 0 && /Unlimited|720P|16:9|\d+s$|Seedance/.test(e.innerText || '')).map(e => e.innerText.trim()).slice(0, 10).join(' | ');
    const imgs = [...document.querySelectorAll('img')].filter(i => { const r = i.getBoundingClientRect(); return r.top > innerHeight - 200 && r.width > 20 && r.width < 120; }).length;
    const ta = document.querySelector('textarea.lv-textarea');
    return { sw: sw && sw.getAttribute('aria-checked'), bar, refImgs: imgs, prompt: ta ? ta.value.slice(0, 6) : '' };
  };
  W.price = () => { let e = document.querySelector('[role=switch]'); if (!e) return null; for (let k = 0; k < 5; k++) e = e.parentElement; const m = (e.innerText || '').match(/Unlimited\s*\n\s*(\d+)/); return m ? +m[1] : null; };
  W.safeGen = async () => {
    const sw = document.querySelector('[role=switch]');
    if (!sw || sw.getAttribute('aria-checked') !== 'true') return 'SWITCH-OFF';
    const g = [...document.querySelectorAll('button[aria-label="Generate"],button')].find(b => (b.getAttribute('aria-label') || '') === 'Generate' && b.getBoundingClientRect().width > 0 && /lv-btn-primary/.test(b.className));
    if (!g || g.disabled) return 'NOBTN';
    if (W.price() !== 0 && W.price() !== null) return 'PRICE ' + W.price();
    const l0 = W.lim; g.click(); await sleep(30000);
    if (W.lim > l0) { const s2 = document.querySelector('[role=switch]'); if (s2 && s2.getAttribute('aria-checked') !== 'true') s2.click(); return 'BUSY'; }
    return 'SENT';
  };
})();
