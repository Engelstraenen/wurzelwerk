/* WURZELWERK „Rundgang“: Scrollen = einmal um den Apfelbaum, durch ein ganzes Jahr. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
  var seg = function (p, a, b) { return clamp((p - a) / (b - a), 0, 1); };
  var eio = function (t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
  var eout = function (t) { return 1 - Math.pow(1 - t, 3); };
  var root = document.documentElement;
  var mob = function () { return innerWidth < 900; };

  /* Parameter: ?firma=Name  ·  ?farbe=2f3a24,e8b4b0 (Grundton, Akzent) */
  var qs = new URLSearchParams(location.search);
  if (qs.get('firma')) { $('[data-firma]').textContent = qs.get('firma').slice(0, 60); $('.demo .for').hidden = false; }
  if (/^[0-9a-f]{6},[0-9a-f]{6}$/i.test(qs.get('farbe') || '')) {
    var f = qs.get('farbe').split(','), rgb = function (h) { return [0, 2, 4].map(function (i) { return parseInt(h.substr(i, 2), 16); }).join(','); };
    root.style.setProperty('--bg', '#' + f[0]); root.style.setProperty('--bg-rgb', rgb(f[0]));
    root.style.setProperty('--or', '#' + f[1]); root.style.setProperty('--or-rgb', rgb(f[1]));
  }

  /* Bilder: 8 Seiten des Baums. Fehlt eines, springt die Nachbarseite ein (nie Platzhalter). */
  var pics = $$('.pic'), have = [], N = pics.length;
  var SIDES = ['Nordseite · März', 'Ostseite · April', 'Unter der Blüte · Mai', 'Südseite · Juli', 'Unter dem Baum · August', 'Westseite · Oktober', 'Am Stamm · November', 'Nordseite · Januar'];
  var ANG = [0, 90, 125, 180, 205, 270, 305, 360];
  function loadPics() {
    var m = mob() && innerHeight > innerWidth;
    pics.forEach(function (el, i) {
      var src = 'assets/img/rund/p' + (i + 1) + (m ? '-m' : '') + '.webp';
      if (el.dataset.src === src) return;
      el.dataset.src = src;
      var im = new Image();
      im.onload = function () { el.style.backgroundImage = 'url(' + src + ')'; have[i] = true; req(); };
      im.onerror = function () { have[i] = false; req(); };
      im.src = src;
    });
  }
  function use(i) { for (var d = 0; d < N; d++) { if (have[i - d]) return i - d; if (have[i + d]) return i + d; } return -1; }

  /* Haltepunkte: Inhalt in eine klebende Ebene legen */
  var stops = $$('.stop');
  stops.forEach(function (s) { var w = document.createElement('div'); w.className = 'in'; while (s.firstChild) w.appendChild(s.firstChild); s.appendChild(w); });

  var sideTxt = $('.sideTxt'), dot = $('.dot'), arcOn = $('#arcOn'), needle = $('.needle'), sls = $$('.sl');
  arcOn.setAttribute('pathLength', '1');
  var t0 = performance.now(), intro = 1;

  function qOf(s) { var r = s.getBoundingClientRect(), h = s.offsetHeight - innerHeight; return { q: h > 0 ? clamp(-r.top / h, 0, 1) : 0, enter: clamp(1 - r.top / innerHeight, 0, 1), top: r.top }; }
  function show(el, o, dx, dy) { if (!el) return; el.style.opacity = o.toFixed(3); el.style.transform = 'translate(' + ((1 - o) * (dx || 0)).toFixed(1) + 'px,' + ((1 - o) * (dy || 0)).toFixed(1) + 'px)'; }
  function bez(u) { var a = 1 - u; return { x: (a * a * 40 + 2 * a * u * 500 + u * u * 960) / 1000, y: (a * a * 138 + 2 * a * u * -30 + u * u * 138) / 140 }; }

  function frame(now) {
    tick = false;
    var cur = 0, qs2 = stops.map(qOf);
    qs2.forEach(function (o, i) { if (o.top <= 1) cur = i; });
    var q = qs2[cur].q, t = cur < N - 1 ? eio(seg(q, .58, 1)) : 0, s = cur + t;
    intro = eout(clamp((now - t0) / 2200, 0, 1));

    /* Bilder: alte Seite dreht nach links weg, neue kommt von rechts (Kamera kreist um den Baum) */
    var a = use(cur), b = use(cur + 1), mv = mob() ? 6 : 9;
    pics.forEach(function (el, i) {
      var o = 0, tx = 0, sc = 1.05, z = 1;
      if (i === a) { o = 1; tx = -q * 2 - t * mv; sc = 1.05 + (1 - intro) * .1 + t * .03; }
      var wipe = i === b && b !== a && t > 0;
      if (wipe) { o = 1; tx = (1 - t) * mv; sc = 1.08 - t * .03; z = 2; el.style.setProperty('--w', ((1 - t) * 114).toFixed(2) + '%'); }
      el.classList.toggle('in2', wipe);
      if (i === a && t > 0) el.style.filter = 'brightness(' + (1 - t * .35).toFixed(3) + ')'; else el.style.filter = '';
      el.style.opacity = o; el.style.zIndex = z;
      if (o > 0) el.style.transform = 'translate3d(' + tx.toFixed(2) + '%,0,0) scale(' + sc.toFixed(4) + ')';
    });

    /* Sonnenbahn + Kompass */
    var u = (.04 + s / (N - 1) * .92) * intro, pt = bez(u);
    dot.style.left = (pt.x * 100) + '%'; dot.style.top = (pt.y * 100) + '%';
    arcOn.style.strokeDashoffset = (1 - u).toFixed(4);
    var season = s < 2.5 ? 0 : s < 4.5 ? 1 : s < 6.5 ? 2 : 3;
    sls.forEach(function (b, i) { b.classList.toggle('on', i === season); });
    var ang = ANG[cur] + (ANG[Math.min(cur + 1, N - 1)] - ANG[cur]) * t;
    needle.style.setProperty('--rot', ang + 'deg');
    var st = SIDES[t > .5 ? Math.min(cur + 1, N - 1) : cur];
    if (sideTxt.textContent !== st) sideTxt.textContent = st;

    /* Texte je Haltepunkt */
    stops.forEach(function (sec, i) {
      var o = qs2[i], last = i === N - 1;
      var vis = i === 0 ? 1 - seg(o.q, .5, .68) : Math.min(seg(o.enter, .55, 1), last ? 1 : 1 - seg(o.q, .5, .68));
      if (i === 0) vis = Math.min(vis, intro * 1.4);
      var inn = sec.firstChild; inn.style.opacity = vis.toFixed(3); inn.style.visibility = vis < .01 ? 'hidden' : 'visible';
      inn.style.transform = 'translateY(' + ((1 - vis) * 24).toFixed(1) + 'px)';
      var p = i === 0 ? 0 : o.q + (1 - o.enter) * -.2;
      $$('.steps li', sec).forEach(function (li, k) { li.classList.toggle('on', p >= k * .1 - .04); });
      $$('.kin li', sec).forEach(function (li, k) { show(li, eout(seg(p, -.1 + k * .1, k * .1)), -60, 0); });
      $$('.big-kin li', sec).forEach(function (li, k) { show(li, eout(seg(p, -.12 + k * .12, k * .12 + .02)), -140, 0); });
      $$('.stars i', sec).forEach(function (st, k) { st.style.setProperty('--f', seg(p, -.1 + k * .05, -.04 + k * .05).toFixed(3)); });
      var qq = $$('.q', sec);
      if (qq.length) {
        if (mob()) { var k1 = Math.floor(clamp(p, 0, .999) / .14) % qq.length; qq.forEach(function (e, k) { e.classList.toggle('on', k === k1 && vis > .3); }); }
        else qq.forEach(function (e, k) { e.classList.toggle('on', p >= -.08 + k * .08 && vis > .3); });
      }
    });
    root.classList.toggle('past', $('#rund').getBoundingClientRect().bottom < innerHeight * .75);
    if (intro < 1) req();
  }
  var tick = false;
  function req() { if (!tick) { tick = true; requestAnimationFrame(frame); } }
  addEventListener('scroll', req, { passive: true });
  addEventListener('resize', function () { loadPics(); req(); });
  loadPics(); req();

  /* Sprünge: Sonnenbahn, Menü, Knöpfe */
  function go(i) { var s = stops[clamp(i, 0, N - 1)]; scrollTo({ top: s.offsetTop + (i ? innerHeight * .05 : 0), behavior: 'smooth' }); }
  $$('[data-go]').forEach(function (b) { b.addEventListener('click', function (e) { e.preventDefault(); root.classList.remove('menu-open'); go(+b.getAttribute('data-go')); }); });
  var burger = $('.burger');
  burger.addEventListener('click', function () { var o = root.classList.toggle('menu-open'); burger.setAttribute('aria-expanded', o); burger.setAttribute('aria-label', o ? 'Menü schließen' : 'Menü öffnen'); });
  addEventListener('keydown', function (e) { if (e.key === 'Escape') root.classList.remove('menu-open'); });

  /* Handy: seitlich wischen = um den Baum gehen */
  var sx = 0, sy = 0, swipeHint = $('.swipe');
  addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; sy = e.touches[0].clientY; }, { passive: true });
  addEventListener('touchend', function (e) {
    if (e.target.closest('dialog, .menu, input, .card, label')) return;
    var dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy;
    if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) {
      var cur = 0; stops.forEach(function (s, i) { if (s.getBoundingClientRect().top <= 1) cur = i; });
      go(cur + (dx < 0 ? 1 : -1)); swipeHint.style.opacity = 0;
    }
  }, { passive: true });
  addEventListener('scroll', function () { if (scrollY > innerHeight) swipeHint.style.opacity = 0; }, { passive: true });

  /* Dialoge + Demo-Formulare */
  var toastEl = $('.toast'), toastT;
  function toast(t) { toastEl.textContent = t; toastEl.hidden = false; clearTimeout(toastT); toastT = setTimeout(function () { toastEl.hidden = true; }, 3200); }
  $$('[data-open]').forEach(function (b) { b.addEventListener('click', function () { var d = $('#m-' + b.getAttribute('data-open')); if (d && d.showModal) { resetApp(d); d.showModal(); } }); });
  $$('dialog form[data-demo]').forEach(function (f) { f.addEventListener('submit', function (e) { if (e.submitter && e.submitter.value === 'ok') toast(f.getAttribute('data-demo')); }); });
  $$('dialog').forEach(function (d) { d.addEventListener('click', function (e) { if (e.target === d) d.close(); }); });
  var mini = $('.mini');
  mini.addEventListener('submit', function (e) { e.preventDefault(); toast(mini.getAttribute('data-demo')); });
  var fi = $('.file input'), fs = $('.file span');
  fi.addEventListener('change', function () { if (fi.files[0]) { fs.textContent = '✓ ' + fi.files[0].name.slice(0, 28); fi.parentNode.classList.add('has'); } });
  var rg = $('.rng input'), ro = $('.rng output');
  rg.addEventListener('input', function () { ro.textContent = rg.value; });

  /* 60-Sekunden-Bewerbung: Antippen = nächste Karte */
  function resetApp(d) { if (d.id !== 'm-bewerbung') return; setCard(0); }
  var sc = $$('.sc'), barI = $('.bar i');
  function setCard(k) { sc.forEach(function (c, i) { c.classList.toggle('on', i === k); }); barI.style.width = ((k + 1) / sc.length * 100) + '%'; }
  sc.forEach(function (c, i) { $$('input[type=radio]', c).forEach(function (r) { r.addEventListener('change', function () { setTimeout(function () { setCard(i + 1); }, 260); }); }); });
})();
