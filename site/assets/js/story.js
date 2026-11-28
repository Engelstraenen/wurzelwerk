/* WURZELWERK Leistungs-Kapitel (Storyboard 1 „Schicht für Schicht“, vorschau/113):
   Scrollen spult je Station einen Film oder bewegt ein Foto, Übergang in die nächste Station per Zoom, Fenster (match) oder Blende.
   Overlays (Haarlinien, Raster, Diagramm, Kalender) liegen in .fit = exakt die sichtbare Bildfläche, damit sie auf dem Foto sitzen. */
(function () {
  var S = document.querySelector('.sst'); if (!S) return;
  var H = window.WW_IMGS || [], mob = matchMedia('(max-width: 760px)').matches, port = mob && innerHeight > innerWidth;
  var M = [].slice.call(S.querySelectorAll('.sst-m')), O = [].slice.call(S.querySelectorAll('.sst-o')), dots = [].slice.call(S.querySelectorAll('.sst-dots i'));
  var n = M.length, V = window.WW_VIDS || [];
  function cl(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function ez(x) { return x < .5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2; }

  // Medien: Foto sofort, Film nur wenn vorhanden (nie Platzhalter, fehlt beides: Station bleibt dunkel und Text trägt)
  M.forEach(function (m) {
    var k = m.dataset.img, im = m.querySelector('img'), v = m.querySelector('video');
    if (k && H.indexOf(k) >= 0) im.src = '../assets/img/rund/' + k + '.webp';  /* immer das ganze 16:9-Foto, Ausschnitt per object-position, damit Overlays exakt sitzen */ else im.hidden = true;
    if (m.dataset.posm) { im.style.objectPosition = m.dataset.posm; v.style.objectPosition = m.dataset.posm; }
    var vid = m.dataset.v;
    if (vid && V.indexOf(vid) >= 0) {
      v.preload = 'auto'; v.muted = true; v.playsInline = true;
      v.addEventListener('loadeddata', function () { m.classList.add('vok'); tick(); });
      var u = '../assets/vid/sub/' + vid + (port ? '-p' : '') + '.mp4?v=' + (window.WW_VER || 1);
      /* 4K all-intra als Blob laden: Spulen springt sonst beim Nachladen einzelner Bereiche (Masterfile V2.88) */
      fetch(u).then(function (r) { if (!r.ok) throw 0; return r.blob(); }).then(function (b) { v.src = URL.createObjectURL(b); }).catch(function () { v.src = u; });
    } else v.remove();
  });

  function geo(m) { /* sichtbare 16:9-Bildfläche eines Mediums in px (object-fit: cover + object-position) */
    var w = innerWidth, h = innerHeight, r = 16 / 9, fw, fh, px = parseFloat((m.dataset.posm || '50% 50%').split(' ')[0]) / 100;
    if (w / h > r) { fw = w; fh = w / r; } else { fh = h; fw = h * r; }
    return { fw: fw, fh: fh, l: (w - fw) * px, t: (h - fh) / 2 };
  }
  // .fit: sichtbare 16:9-Bildfläche bei object-fit: cover (Hochformat: Ausschnitt laut data-posm)
  function fit() {
    var w = innerWidth, h = innerHeight, r = 16 / 9, fw, fh;
    if (w / h > r) { fw = w; fh = w / r; } else { fh = h; fw = h * r; }
    O.concat(M).forEach(function (el) {
      var f = el.querySelector('.fit'); if (!f) return;
      var m = M[+el.dataset.i], px = parseFloat((m.dataset.posm || '50% 50%').split(' ')[0]) / 100;
      f.style.width = fw + 'px'; f.style.height = fh + 'px';
      f.style.left = (w - fw) * px + 'px'; f.style.top = (h - fh) / 2 + 'px';
    });
  }

  var last = -1, lastT = -1;
  function tick() {
    var r = S.getBoundingClientRect(), span = S.offsetHeight - innerHeight;
    var p = cl(-r.top / Math.max(1, span), 0, .9999), f = p * n, i = Math.floor(f), t = f - i;
    if (Math.abs(t - lastT) < .0005 && i === last) return; lastT = t;
    var TZ = .78, k = t > TZ && i < n - 1 ? ez((t - TZ) / (1 - TZ)) : 0;  /* letztes Fünftel = Übergang in die nächste Station */
    M.forEach(function (m, j) {
      var st = m.style, tr = (M[i].dataset.tr || 'fade').split(':'), a = (tr[1] || '50,50').split(',').map(Number);
      st.clipPath = ''; st.transform = ''; st.transformOrigin = '';
      if (j === i) {
        st.opacity = 1; st.zIndex = 1;
        var v = m.querySelector('video');
        if (v && m.classList.contains('vok') && v.duration) { var tt = cl(t / TZ, 0, 1) * (v.duration - .05); if (Math.abs(v.currentTime - tt) > .02 && !v.seeking) v.currentTime = tt; }
        else st.transform = 'scale(' + (1.02 + .05 * cl(t / TZ, 0, 1)) + ')';  /* Foto atmet: leichter Zoom */
        if (k && tr[0] === 'fade') st.opacity = 1 - cl(k / .5, 0, 1);
        if (k && tr[0] === 'zoom') { st.transformOrigin = a[0] + '% ' + a[1] + '%'; st.transform = 'scale(' + (1.07 + 2.6 * k) + ')'; st.opacity = 1 - cl((k - .5) / .28, 0, 1); }  /* Zoom ins Objekt, dann kurz dunkel (nie zwei versetzte Bilder übereinander) */
      } else if (j === i + 1 && k) {
        st.zIndex = 2;
        if (tr[0] === 'match') { /* Fenster: Bild im Handy-Display wächst zum ganzen Bild */
          var q = 1 - k, g = geo(M[i]), x0 = g.l + g.fw * a[0] / 100, y0 = g.t + g.fh * a[1] / 100, x1 = x0 + g.fw * a[2] / 100, y1 = y0 + g.fh * a[3] / 100; st.opacity = 1;
          st.clipPath = 'inset(' + y0 * q + 'px ' + (innerWidth - x1) * q + 'px ' + (innerHeight - y1) * q + 'px ' + x0 * q + 'px round ' + 22 * q + 'px)';
        } else if (tr[0] === 'zoom') { st.opacity = cl((k - .8) / .2, 0, 1); st.transform = 'scale(' + (1.12 - .1 * k) + ')'; }
        else st.opacity = cl((k - .5) / .5, 0, 1);  /* Blende über kurzes Dunkel statt Doppelbild */
      } else { st.opacity = 0; st.zIndex = 0; }
    });
    O.forEach(function (o, j) {
      var on = j === i && !(k > .35);
      o.classList.toggle('on', on);
      if (j !== i) return;
      o.style.setProperty('--t', t.toFixed(3));
      [].forEach.call(o.querySelectorAll('[data-at]'), function (e) { e.classList.toggle('on', t >= +e.dataset.at); });
      [].forEach.call(o.querySelectorAll('[data-count]'), function (e) {
        var a = (e.dataset.span || '.1,.6').split(',').map(Number), x = cl((t - a[0]) / (a[1] - a[0]), 0, 1);
        e.textContent = Math.round(+e.dataset.count * ez(x)).toLocaleString('de-DE');
      });
      [].forEach.call(o.querySelectorAll('[data-cells]'), function (g) {
        var a = (g.dataset.span || '.1,.6').split(',').map(Number), x = cl((t - a[0]) / (a[1] - a[0]), 0, 1), c = g.querySelectorAll('.c'), lit = Math.round(c.length * x);
        for (var q = 0; q < c.length; q++) c[q].classList.toggle('lit', q < lit);
      });
    });
    dots.forEach(function (d, j) { d.classList.toggle('on', j === i); });
    last = i;
  }
  var raf = 0;
  addEventListener('scroll', function () { if (!raf) raf = requestAnimationFrame(function () { raf = 0; tick(); }); }, { passive: true });
  addEventListener('resize', function () { fit(); lastT = -1; tick(); });
  dots.forEach(function (d, j) { d.addEventListener('click', function () { scrollTo({ top: S.offsetTop + (S.offsetHeight - innerHeight) * (j + .3) / n, behavior: 'smooth' }); }); });
  fit(); tick();
})();
