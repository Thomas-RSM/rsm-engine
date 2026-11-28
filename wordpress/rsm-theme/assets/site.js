/* Relevant Search Media — page script. The page reads and works without it; it adds the living pictures. */
window.RSMInit = function () {
  'use strict';
  var BASE = window.RSM_BASE || '/assets/';
  var REDUCE = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  document.documentElement.classList.remove('no-js'); if (document.body.classList.contains('elementor-editor-active')) { [].forEach.call(document.querySelectorAll('.rv'), function (e) { e.classList.add('in'); }); }
  function onScreen(el, cb, margin) { if (!window.IntersectionObserver) { cb(true); return; } new IntersectionObserver(function (es) { cb(es[0].isIntersecting); }, { rootMargin: margin || '120px' }).observe(el); }

  /* ---------- reveal on scroll ---------- */
  (function () {
    var els = document.querySelectorAll('.rv');
    if (!window.IntersectionObserver || REDUCE) { els.forEach(function (e) { e.classList.add('in'); }); return; }
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px' });
    els.forEach(function (e) { io.observe(e); });
  })();

  /* ---------- 1 · the orbit: twenty platforms round one business ---------- */
  (function () {
    var root = document.getElementById('orbit'); if (!root) return;
    if (root.__rsm) return; root.__rsm = 1;
    var dataEl = root.querySelector('.orbit-data'), I = []; try { I = JSON.parse(dataEl.textContent); } catch (e) {} if (!I.length) return;
    if (window.innerWidth < 480) { var KEEP = ['Google', 'Maps', 'ChatGPT', 'Gemini', 'Perplexity', 'Copilot', 'SEO', 'Local SEO', 'AEO', 'AIO', 'GBP', 'Reddit'], few = I.filter(function (i) { return KEEP.indexOf(i.name) >= 0; }); if (few.length >= 8) I = few; }
    var NT = I.length;
    I.forEach(function (i) { i.src = 'url("data:image/svg+xml;utf8,' + encodeURIComponent(i.svg).replace(/'/g, '%27').replace(/\(/g, '%28').replace(/\)/g, '%29') + '")'; });
    var n1 = Math.max(1, Math.round(NT * 0.2)), n2 = Math.max(1, Math.round(NT * 0.3)), seq = function (a, b) { var r = []; for (var i = a; i < b; i++) r.push(i); return r; };
    var RINGS = [{ ids: seq(0, Math.min(n1, NT)), spd: 8 }, { ids: seq(Math.min(n1, NT), Math.min(n1 + n2, NT)), spd: 5 }, { ids: seq(Math.min(n1 + n2, NT), NT), spd: 3 }].filter(function (r) { return r.ids.length; });
    var META = new Array(NT); RINGS.forEach(function (r, ri) { r.ids.forEach(function (id, i) { META[id] = { ri: ri, i: i, n: r.ids.length }; }); });
    var RGB = I.map(function (ic) { return [parseInt(ic.c.slice(1, 3), 16), parseInt(ic.c.slice(3, 5), 16), parseInt(ic.c.slice(5, 7), 16)]; });
    var mk = function (tag, cls) { var e = document.createElement(tag); if (cls) e.className = cls; e.setAttribute('aria-hidden', 'true'); return e; };
    var light = mk('div', 'o-light'), rayA = mk('canvas'), rayB = mk('canvas'), cv = mk('canvas'), core = root.querySelector('.o-core');
    root.insertBefore(cv, core); root.insertBefore(rayB, cv); root.insertBefore(rayA, rayB); root.insertBefore(light, rayA);
    var els = [], gls = [], boxes = [], ics = [], names = [];
    var hover = -1, boost = new Float32Array(NT), hov = new Float32Array(NT), lastG = new Float32Array(NT).fill(-1), lastZ = new Int16Array(NT).fill(-1);
    I.forEach(function (ic, id) {
      var el = document.createElement('div'); el.className = 'o-tile';
      var gl = mk('span', 'o-glow'), box = document.createElement('span'), icn = mk('span', 'o-ic'), nm = document.createElement('span');
      box.className = 'o-box'; nm.className = 'o-name'; nm.textContent = ic.name; icn.style.backgroundImage = ic.src;
      box.addEventListener('mouseenter', function () { hover = id; }); box.addEventListener('mouseleave', function () { if (hover === id) hover = -1; });
      box.appendChild(icn); el.appendChild(gl); el.appendChild(box); el.appendChild(nm); root.appendChild(el);
      els.push(el); gls.push(gl); boxes.push(box); ics.push(icn); names.push(nm);
    });
    var W = 0, G = null, sprites = null, ctx = null, t = REDUCE ? 20 : 0, prev = 0, raf = 0, visible = true, order = null, buf = null, P = null;
    function geo(w) {
      if (w < 480) { var kk = w / 390; return { w: w, h: 500, cx: w / 2, cy: 246, rx: [64, 112, 156].map(function (v) { return v * kk; }), ry: [84, 150, 212], tile: 46, icon: 24, lf: 9.5, ls: 0.4, gap: 5, logo: Math.min(70, w * 0.17) }; }
      if (w < 820) { var k = Math.min(1.6, w / 390), h = 800, sm = w < 480;
        return { w: w, h: h, cx: w / 2, cy: h / 2 - 8, rx: (sm ? [58, 108, 160] : [62, 110, 158]).map(function (v) { return v * k; }), ry: [126, 232, 330], tile: sm ? 36 : 40, icon: sm ? 19 : 21, lf: sm ? 6.5 : 7, ls: sm ? 0.6 : 1, gap: 5, logo: sm ? Math.min(72, w * 0.17) : Math.min(78, w * 0.18) }; }
      var tab = w < 1100, X = Math.min(560, w / 2 - (tab ? 52 : 34)), tile = tab ? 48 : 52, f = tab ? [0.5, 0.77, 1] : [0.46, 0.76, 1.04];
      var ry = tab ? [130, 216, 302] : [150, 252, 352], hh = tab ? 720 : 840;
      return { w: w, h: hh, cx: w / 2, cy: hh / 2 - 8, rx: f.map(function (v) { return v * X; }), ry: ry, tile: tile, icon: tab ? 24 : 28, lf: tab ? 8 : 10, ls: tab ? 1.5 : 2.5, gap: 6, logo: tab ? 128 : 150 };
    }
    function RL(g) { return Math.min(g.rx[0] * 1.02, g.ry[1]) * 1.25; }
    function RA(g) { return Math.min(g.rx[2] * 1.05, g.h * 0.62); }
    function layout() {
      var w = root.getBoundingClientRect().width; if (!w || Math.abs(w - W) < 1) return; W = w; G = geo(w); sprites = null; ctx = null;
      var g = G, s = g.tile, L = g.logo / 2, ra = RA(g), rl = RL(g);
      root.style.height = g.h + 'px';
      cv.style.cssText = 'left:0;top:0;width:100%;height:100%';
      light.style.cssText = 'left:' + (g.cx - ra) + 'px;top:' + (g.cy - ra) + 'px;width:' + ra * 2 + 'px;height:' + ra * 2 + 'px;opacity:.9;background:radial-gradient(circle, rgba(255,200,100,0.46) ' + (L * 0.9).toFixed(0) + 'px, rgba(248,184,70,0.17) ' + (L * 1.55).toFixed(0) + 'px, rgba(248,177,15,0) ' + (L * 2.6).toFixed(0) + 'px), radial-gradient(circle, rgba(111,140,240,0.29) 0%, rgba(72,99,181,0.15) 35%, rgba(48,70,150,0.05) 70%, rgba(48,70,150,0) 100%)';
      [rayA, rayB].forEach(function (r) { r.style.cssText = 'left:' + (g.cx - rl) + 'px;top:' + (g.cy - rl) + 'px;width:' + rl * 2 + 'px;height:' + rl * 2 + 'px;will-change:transform,opacity'; });
      core.style.left = g.cx + 'px'; core.style.top = g.cy + 'px'; core.style.width = core.style.height = g.logo + 'px';
      I.forEach(function (ic, id) {
        var c = RGB[id], rgba = function (a) { return 'rgba(' + c[0] + ',' + c[1] + ',' + c[2] + ',' + a + ')'; };
        els[id].style.width = s + 'px'; els[id].style.gap = g.gap + 'px';
        var gs = Math.round(s * 2.8), gh = Math.round(s * 1.4);
        gls[id].style.cssText = 'top:' + s / 2 + 'px;width:' + gs + 'px;height:' + gs + 'px;margin:-' + gh + 'px 0 0 -' + gh + 'px;background:radial-gradient(circle, ' + rgba(0.62) + ' 0%, ' + rgba(0.26) + ' 30%, ' + rgba(0.08) + ' 52%, ' + rgba(0) + ' 70%)';
        boxes[id].style.cssText = 'width:' + s + 'px;height:' + s + 'px;border-radius:' + Math.round(s * 0.3) + 'px;background:linear-gradient(150deg, ' + rgba(0.22) + ' 0%, rgba(30,42,86,0.66) 34%, rgba(10,16,36,0.9) 100%);border:1px solid rgba(' + Math.round(c[0] * 0.5 + 127) + ',' + Math.round(c[1] * 0.5 + 127) + ',' + Math.round(c[2] * 0.5 + 127) + ',0.42);box-shadow:0 8px 18px rgba(4,8,22,0.5), inset 0 1px 0 rgba(255,255,255,0.28), inset 0 -' + Math.round(s * 0.2) + 'px ' + Math.round(s * 0.3) + 'px ' + rgba(0.12);
        ics[id].style.width = ics[id].style.height = g.icon + 'px';
        names[id].style.cssText = 'font-size:' + g.lf + 'px;letter-spacing:' + g.ls + 'px;margin-right:-' + g.ls + 'px';
      });
      lastG.fill(-1); lastZ.fill(-1); kick();
    }
    function place(tt) { var g = G, out = new Array(NT);
      RINGS.forEach(function (ring, ri) { var n = ring.ids.length; ring.ids.forEach(function (id, i) { var a = (i / n) * 6.2832 - 1.5708 + tt * 0.011 * ring.spd;
        out[id] = { x: g.cx + Math.cos(a) * g.rx[ri] + Math.sin(tt * 0.18 + id * 1.7) * 4, y: g.cy + Math.sin(a) * g.ry[ri] + Math.cos(tt * 0.18 + id * 2.1) * 3, a: a, d: (Math.sin(a) + 1) / 2 }; }); });
      return out; }
    function wave(u, id, tt) { return Math.sin(u * 5 + tt * 0.18 + id * 2) * 22 * (1 - Math.abs(u - 0.5) * 1.8) + Math.sin(u * 9 + tt * 0.3 + id * 3) * 8 * u; }
    function onPath(x1, y1, x2, y2, u, id, tt, amp) { var dx = x2 - x1, dy = y2 - y1, d = Math.hypot(dx, dy) || 1, w = wave(u, id, tt) * amp; return [x1 + dx * u - dy / d * w, y1 + dy * u + dx / d * w]; }
    function pulseU(tt, id) { var m = META[id], tp = tt % 6.4, p = (tp - (0.5 + m.ri * 0.5 + m.i * 0.07)) / 1.5; return p > 0 && p < 1 ? p : -1; }
    function buildSprites(g, dpr) {
      var L = g.logo / 2, mkc = function (size) { var c = document.createElement('canvas'); c.width = c.height = Math.max(2, Math.round(size * dpr)); var x = c.getContext('2d'); x.scale(dpr, dpr); return [c, x]; }, gr;
      var rl = RL(g), small = g.w < 820 ? 0.8 : 1, sd = 17, r = function () { sd = (sd * 9301 + 49297) % 233280; return sd / 233280; };
      var rays = []; for (var i = 0; i < 34; i++) rays.push({ a: i / 34 * 6.2832 + (r() - 0.5) * 0.16, w: 0.022 + r() * 0.07, l: 1.9 + r() * 2.6, o: 0.5 + r() * 0.5 });
      var mkRays = function (pick, c) { c.width = c.height = Math.round(rl * 2 * dpr); var x = c.getContext('2d'); x.setTransform(dpr, 0, 0, dpr, 0, 0); x.clearRect(0, 0, rl * 2, rl * 2); x.globalCompositeOperation = 'lighter';
        rays.forEach(function (ry, i) { if (i % 2 !== pick) return; var len = Math.min(rl, L * ry.l * small), r0 = L * 0.7, rg = x.createRadialGradient(rl, rl, r0, rl, rl, len);
          rg.addColorStop(0, 'rgba(255,206,110,' + (0.17 * ry.o).toFixed(3) + ')'); rg.addColorStop(0.35, 'rgba(248,184,70,' + (0.085 * ry.o).toFixed(3) + ')'); rg.addColorStop(1, 'rgba(248,177,15,0)'); x.fillStyle = rg; x.beginPath();
          x.moveTo(rl + Math.cos(ry.a - ry.w * 0.35) * r0, rl + Math.sin(ry.a - ry.w * 0.35) * r0); x.lineTo(rl + Math.cos(ry.a - ry.w) * len, rl + Math.sin(ry.a - ry.w) * len); x.arc(rl, rl, len, ry.a - ry.w, ry.a + ry.w); x.lineTo(rl + Math.cos(ry.a + ry.w * 0.35) * r0, rl + Math.sin(ry.a + ry.w * 0.35) * r0); x.closePath(); x.fill(); }); };
      mkRays(0, rayA); mkRays(1, rayB);
      var a = mkc(32), sc = a[0], sx = a[1]; gr = sx.createRadialGradient(16, 16, 0, 16, 16, 16); gr.addColorStop(0, 'rgba(255,246,214,1)'); gr.addColorStop(0.16, 'rgba(255,214,130,0.7)'); gr.addColorStop(1, 'rgba(248,177,15,0)'); sx.fillStyle = gr; sx.fillRect(0, 0, 32, 32);
      var b = mkc(16), bc = b[0], bx = b[1]; gr = bx.createRadialGradient(8, 8, 0, 8, 8, 8); gr.addColorStop(0, 'rgba(214,226,255,0.6)'); gr.addColorStop(1, 'rgba(143,166,240,0)'); bx.fillStyle = gr; bx.fillRect(0, 0, 16, 16);
      return { key: g.w + 'x' + dpr, spark: sc, blue: bc };
    }
    var _lo, _ao, _bo;
    function step(tt, dt) {
      var g = G; if (!g) return; var cx = g.cx, cy = g.cy, L = g.logo / 2;
      var dpr = Math.max(1, Math.min(window.devicePixelRatio || 1, 2, Math.sqrt(2.2e6 / (g.w * g.h))));
      if (cv.width !== Math.round(g.w * dpr) || cv.height !== Math.round(g.h * dpr)) { cv.width = Math.round(g.w * dpr); cv.height = Math.round(g.h * dpr); ctx = null; }
      if (!sprites || sprites.key !== g.w + 'x' + dpr) sprites = buildSprites(g, dpr);
      var S = sprites; P = place(tt);
      var x = ctx || (ctx = cv.getContext('2d')); x.setTransform(dpr, 0, 0, dpr, 0, 0); x.clearRect(0, 0, g.w, g.h);
      var amp = g.w < 820 ? 0.55 : 1, N = 28, tp = tt % 6.4, br = 0.5 + 0.5 * Math.sin(tt * 0.8), kk = tp < 1.4 ? Math.sin(tp / 1.4 * Math.PI) : 0, i, id;
      for (i = 0; i < NT; i++) { boost[i] = Math.max(0, boost[i] - dt * 1.4); hov[i] += ((hover === i ? 1 : 0) - hov[i]) * Math.min(1, dt * 9); }
      x.globalCompositeOperation = 'lighter'; x.lineCap = 'round'; x.lineJoin = 'round';
      var v = Math.min(1, 0.84 + 0.12 * br + 0.1 * kk).toFixed(2); if (v !== _lo) { light.style.opacity = v; _lo = v; }
      rayA.style.transform = 'rotate(' + (tt * 0.69).toFixed(3) + 'deg)'; v = Math.min(1, 0.78 + 0.22 * Math.sin(tt * 0.27) + 0.15 * kk).toFixed(2); if (v !== _ao) { rayA.style.opacity = v; _ao = v; }
      rayB.style.transform = 'rotate(' + (-tt * 0.52).toFixed(3) + 'deg)'; v = Math.min(1, 0.74 + 0.26 * Math.sin(tt * 0.33 + 2.1) + 0.15 * kk).toFixed(2); if (v !== _bo) { rayB.style.opacity = v; _bo = v; }
      for (id = 0; id < NT; id++) { var m = META[id], c = RGB[id], q = P[id], n = 7, span = 0.34 * (m.ri === 0 ? 1.3 : m.ri === 1 ? 1 : 0.8), rx = g.rx[Math.min(m.ri, 2)], ry = g.ry[Math.min(m.ri, 2)];
        var px = cx + Math.cos(q.a) * rx, py = cy + Math.sin(q.a) * ry;
        for (var j = 1; j <= n; j++) { var a1 = q.a - span * j / n, f = 1 - (j - 1) / n, nx = cx + Math.cos(a1) * rx, ny = cy + Math.sin(a1) * ry; x.strokeStyle = 'rgba(' + c[0] + ',' + c[1] + ',' + c[2] + ',' + (f * f * (0.16 + 0.34 * q.d)).toFixed(3) + ')'; x.lineWidth = 1 + 1.4 * f; x.beginPath(); x.moveTo(px, py); x.lineTo(nx, ny); x.stroke(); px = nx; py = ny; } }
      RINGS.forEach(function (ring) { var n = ring.ids.length; x.beginPath(); for (var i = 0; i < n; i++) { var A = P[ring.ids[i]], B = P[ring.ids[(i + 1) % n]]; x.moveTo(A.x, A.y); for (var k = 1; k <= 12; k++) { var p = onPath(A.x, A.y, B.x, B.y, k / 12, ring.ids[i] + 20, tt, amp * 0.8); x.lineTo(p[0], p[1]); } } x.strokeStyle = 'rgba(163,181,242,0.085)'; x.lineWidth = 0.8; x.stroke(); });
      order = order || Array.from({ length: NT }, function (_, i) { return i; }); order.sort(function (a, b) { return P[a].d - P[b].d; });
      buf = buf || new Float32Array((N + 1) * 2);
      order.forEach(function (id) {
        var q = P[id], c = RGB[id], m = META[id], dx = q.x - cx, dy = q.y - cy, dist = Math.hypot(dx, dy) || 1, nx = -dy / dist, ny = dx / dist, hi = Math.min(1, boost[id] + hov[id]);
        var u0 = L / dist, i0 = Math.min(N - 2, Math.ceil(u0 * N)), al = 0.26 + 0.34 * q.d + 0.4 * hi, i, u, w, X, Y;
        var body = new Path2D(), echo = new Path2D();
        for (i = i0; i <= N; i++) { u = i / N; w = wave(u, id, tt) * amp; X = cx + dx * u + nx * w; Y = cy + dy * u + ny * w; i === i0 ? body.moveTo(X, Y) : body.lineTo(X, Y); }
        for (i = 0; i <= 14; i++) { u = u0 + (1 - u0) * i / 14; w = wave(u, id + 50, tt * 0.8) * amp * 1.5; X = cx + dx * u + nx * w; Y = cy + dy * u + ny * w; i ? echo.lineTo(X, Y) : echo.moveTo(X, Y); }
        x.strokeStyle = 'rgba(143,166,240,' + (0.05 + 0.07 * q.d).toFixed(3) + ')'; x.lineWidth = 0.8; x.stroke(echo);
        x.strokeStyle = 'rgba(111,140,240,' + (0.045 + 0.06 * q.d + 0.1 * hi).toFixed(3) + ')'; x.lineWidth = 6; x.stroke(body);
        var gr = x.createLinearGradient(cx, cy, q.x, q.y);
        gr.addColorStop(0, 'rgba(255,214,140,' + Math.min(1, al * 1.15).toFixed(3) + ')'); gr.addColorStop(0.3, 'rgba(190,205,250,' + (al * 0.85).toFixed(3) + ')'); gr.addColorStop(1, 'rgba(' + c[0] + ',' + c[1] + ',' + c[2] + ',' + (al * 0.75).toFixed(3) + ')');
        x.strokeStyle = gr; x.lineWidth = 1.3 + 1.1 * q.d + 0.8 * hi; x.stroke(body);
        x.strokeStyle = 'rgba(255,255,255,' + (0.10 + 0.14 * q.d + 0.3 * hi).toFixed(3) + ')'; x.lineWidth = 0.6; x.stroke(body);
        var per = 5.2 + m.ri * 1.3, h = ((tt / per + m.i / m.n + m.ri * 0.33) % 1), pv, cur, f, j;
        if (h > u0 + 0.02) { var edge = Math.min(1, (h - u0) / 0.08) * Math.min(1, (1 - h) / 0.1), T = 6, du = 0.024; pv = onPath(cx, cy, q.x, q.y, h, id, tt, amp); var hp = pv;
          for (j = 1; j <= T; j++) { var uu = h - j * du; if (uu < u0) break; cur = onPath(cx, cy, q.x, q.y, uu, id, tt, amp); f = 1 - (j - 1) / T; x.strokeStyle = 'rgba(214,226,255,' + (f * f * (0.34 + 0.26 * q.d) * edge).toFixed(3) + ')'; x.lineWidth = 0.8 + 1.5 * f; x.beginPath(); x.moveTo(pv[0], pv[1]); x.lineTo(cur[0], cur[1]); x.stroke(); pv = cur; }
          x.globalAlpha = edge; x.drawImage(S.blue, hp[0] - 7, hp[1] - 7, 14, 14); x.globalAlpha = 1; }
        var pu = pulseU(tt, id);
        if (pu > 0) { var u2 = Math.max(u0, pu), sp = onPath(cx, cy, q.x, q.y, u2, id, tt, amp), fade = pu < 0.1 ? pu / 0.1 : pu > 0.86 ? (1 - pu) / 0.14 : 1; pv = sp;
          for (j = 1; j <= 5; j++) { var ut = u2 - j * 0.022; if (ut < u0) break; cur = onPath(cx, cy, q.x, q.y, ut, id, tt, amp); f = 1 - (j - 1) / 5; x.strokeStyle = 'rgba(255,206,120,' + (f * 0.6 * fade).toFixed(3) + ')'; x.lineWidth = 0.6 + 2.4 * f; x.beginPath(); x.moveTo(pv[0], pv[1]); x.lineTo(cur[0], cur[1]); x.stroke(); pv = cur; }
          x.globalAlpha = fade; x.drawImage(S.spark, sp[0] - 15, sp[1] - 15, 30, 30); x.globalAlpha = 1;
          if (pu > 0.86) boost[id] = Math.max(boost[id], Math.min(1, (pu - 0.86) / 0.06)); }
      });
      var sweep = function (r, a0, len, col, al, w) { var n = 10; for (var j = 0; j < n; j++) { var f = 1 - j / n, b0 = a0 - len * j / n, b1 = a0 - len * (j + 1) / n; x.strokeStyle = 'rgba(' + col + ',' + (al * f * f).toFixed(3) + ')'; x.lineWidth = w * (0.4 + 0.6 * f); x.beginPath(); x.arc(cx, cy, r, b1, b0); x.stroke(); } };
      x.strokeStyle = 'rgba(190,205,250,0.10)'; x.lineWidth = 1; x.beginPath(); x.arc(cx, cy, L + 13, 0, 6.283); x.stroke();
      sweep(L + 13, tt * 0.42, 1.9, '255,206,120', 0.85, 2.2); sweep(L + 13, tt * 0.42 + Math.PI, 1.2, '255,206,120', 0.45, 1.6);
      sweep(L + 24, -tt * 0.27 + 1.2, 1.5, '120,214,196', 0.5, 1.5); sweep(L + 24, -tt * 0.27 + 1.2 + Math.PI, 1.0, '143,166,240', 0.5, 1.5);
      if (tp < 2.2) { var k2 = tp / 2.2, r2 = L + 6 + (g.ry[0] * 0.95 - L) * (1 - Math.pow(1 - k2, 2)); x.strokeStyle = 'rgba(255,214,140,' + (0.42 * (1 - k2) * (1 - k2)).toFixed(3) + ')'; x.lineWidth = 1.6; x.beginPath(); x.ellipse(cx, cy, r2 * (g.rx[0] / g.ry[0]) * 0.72 + r2 * 0.28, r2, 0, 0, 6.283); x.stroke(); }
      x.globalCompositeOperation = 'source-over';
      var s = g.tile;
      for (id = 0; id < NT; id++) { var q2 = P[id], m2 = META[id], hv = hov[id], e = Math.min(1, boost[id] + hv), k3 = 0.9 + 0.1 * q2.d + 0.1 * hv;
        els[id].style.transform = 'translate3d(' + (q2.x - s / 2).toFixed(2) + 'px,' + (q2.y - s / 2).toFixed(2) + 'px,0) scale(' + k3.toFixed(3) + ')';
        var breath = 0.5 + 0.5 * Math.sin(tt * 0.9 - m2.i / m2.n * 6.283 - m2.ri * 1.1), gl = Math.min(1, 0.26 + 0.2 * q2.d + 0.16 * breath + 0.5 * e);
        if (Math.abs(gl - lastG[id]) > 0.008) { gls[id].style.opacity = gl.toFixed(3); lastG[id] = gl; }
        var z = 5 + Math.round(q2.d * 8) + (hv > 0.05 ? 20 : 0); if (z !== lastZ[id]) { els[id].style.zIndex = z; lastZ[id] = z; } }
    }
    function frame(now) { raf = 0; if (!visible || document.hidden) return;
      var dt = prev ? Math.min(0.05, Math.max(0, (now - prev) / 1000)) : 0.016; prev = now; t += dt;
      try { step(t, dt); } catch (err) { if (!frame.warned) { frame.warned = true; console.error('orbit', err); } }
      if (!REDUCE) raf = requestAnimationFrame(frame); }
    function kick() { if (!raf) { prev = 0; raf = requestAnimationFrame(frame); } }
    onScreen(root, function (v) { visible = v; kick(); });
    document.addEventListener('visibilitychange', kick);
    if (window.ResizeObserver) new ResizeObserver(layout).observe(root); else window.addEventListener('resize', layout);
    layout();
  })();

  /* ---------- 2 · the console and its sky: a real map, one light per search ---------- */
  (function () {
    var trade = document.getElementById('trade'), city = document.getElementById('city'), sky = document.getElementById('sky');
    if (!trade || !city || !window.fetch) return; if (trade.__rsm) return; trade.__rsm = 1;
    var form = trade.closest('form'), CT = {}; try { CT = JSON.parse(form.getAttribute('data-c')) || {}; } catch (e) {} var FIRST = (form && form.getAttribute('data-first')) || 'plumbers';
    var counts = null, maps = {}, cv = sky && sky.querySelector('canvas'), tip = sky && sky.querySelector('.sky-tip'), kindsEl = document.getElementById('kinds');
    var HUES = ['248,177,15', '163,181,242', '76,192,168', '111,140,240', '246,241,230', '30,167,232'];
    var dots = [], labels = [], born = 0, t = 0, prev = 0, raf = 0, visible = false, mouse = null, pick = -1, pickAt = 0, ctx = null, CW = 0, CH = 0;
    function set(sel, text) { document.querySelectorAll(sel).forEach(function (el) { el.textContent = text; }); }
    function fill() {
      var tv = trade.value, cvv = city.value, cityName = city.options[city.selectedIndex].text, tradeName = trade.options[trade.selectedIndex].text;
      set('[data-trade-name]', tradeName.toLowerCase()); set('[data-city-name]', cityName);
      var d = counts && counts[tv] && counts[tv].c && counts[tv].c[cvv];
      if (d) { set('[data-count]', d.n.toLocaleString('en-US')); set('[data-ex1]', d.ex[0] || ''); set('[data-ex2]', d.ex[1] || ''); set('[data-kinds]', String(d.k)); }
      var isFirst = tv === FIRST, fillT = function (s) { return (s || '').replace('{trade}', tradeName).replace('{city}', cityName); };
      set('[data-confirm-status]', isFirst ? CT.note : CT.noteOther); set('[data-confirm-big]', isFirst ? CT.big : CT.bigOther); set('[data-confirm-line]', isFirst ? CT.line : fillT(CT.lineOther));
      if (!cv) return;
      if (maps[tv]) build(maps[tv], cvv); else fetch(BASE + 'map/' + tv + '.json').then(function (r) { return r.json(); }).then(function (j) { maps[tv] = j; if (trade.value === tv) build(j, city.value); }).catch(function () {});
    }
    function build(m, cvv) {
      var rows = (m.c && m.c[cvv]) || [], by = {}, order = [];
      rows.forEach(function (r) { if (!by[r[1]]) { by[r[1]] = []; order.push(r[1]); } by[r[1]].push(r[0]); });
      order.sort(function (a, b) { return a - b; });
      var total = rows.length || 1, a0 = -Math.PI / 2, sd = 7, rnd = function () { sd = (sd * 9301 + 49297) % 233280; return sd / 233280; };
      dots = []; labels = [];
      var minSpan = 0.16, spans = order.map(function (k) { return Math.max(minSpan, by[k].length / total * 6.2832); }), sum = spans.reduce(function (a, b) { return a + b; }, 0);
      order.forEach(function (k, oi) {
        var span = spans[oi] / sum * 6.2832, list = by[k], hue = HUES[oi % HUES.length], pad = Math.min(0.05, span * 0.12);
        list.forEach(function (kw, i) {
          var lanes = Math.max(1, Math.ceil(list.length / Math.max(3, Math.floor((span - pad * 2) / 0.085)))), lane = i % lanes, col = Math.floor(i / lanes), cols = Math.ceil(list.length / lanes);
          var a = a0 + pad + (span - pad * 2) * ((col + 0.5) / cols) + (rnd() - 0.5) * 0.02, r = 0.40 + 0.52 * ((lane + 0.5) / lanes) + (rnd() - 0.5) * 0.035;
          dots.push({ a: a, r: r, kw: kw, kind: m.kinds[k], hue: hue, s: 1.3 + rnd() * 1.5, ph: rnd() * 6.28, dl: rnd() * 0.5 });
        });
        labels.push({ a: a0 + span / 2, text: m.kinds[k], n: list.length, hue: hue, span: span });
        a0 += span;
      });
      if (kindsEl) kindsEl.innerHTML = labels.map(function (l) { return '<li><i style="background:rgb(' + l.hue + ')"></i>' + l.text + ' · ' + l.n + '</li>'; }).join('');
      born = t; pick = -1; pickAt = t + 1.4; kick();
    }
    function draw(now) {
      raf = 0; if (!visible || document.hidden || !cv) return;
      var dt = prev ? Math.min(0.05, (now - prev) / 1000) : 0.016; prev = now; t += dt;
      var rect = sky.getBoundingClientRect(), w = rect.width, h = rect.height, dpr = Math.min(window.devicePixelRatio || 1, 2);
      if (CW !== Math.round(w * dpr) || CH !== Math.round(h * dpr)) { CW = cv.width = Math.round(w * dpr); CH = cv.height = Math.round(h * dpr); ctx = null; }
      var x = ctx || (ctx = cv.getContext('2d')); x.setTransform(dpr, 0, 0, dpr, 0, 0); x.clearRect(0, 0, w, h);
      var cx = w / 2, cy = h / 2, R = Math.min(w, h) / 2 - (w < 520 ? 12 : 58), rot = REDUCE ? 0 : t * 0.012, age = t - born, i, d;
      x.lineWidth = 1;
      [0.34, 0.66, 0.96].forEach(function (f, i) { x.strokeStyle = 'rgba(163,181,242,' + (0.16 - i * 0.03) + ')'; x.setLineDash(i === 1 ? [2, 6] : []); x.beginPath(); x.arc(cx, cy, R * f, 0, 6.2832); x.stroke(); });
      x.setLineDash([]);
      var a = 0; labels.forEach(function (l) { var b = l.a - l.span / 2 + rot; x.strokeStyle = 'rgba(163,181,242,0.10)'; x.beginPath(); x.moveTo(cx + Math.cos(b) * R * 0.34, cy + Math.sin(b) * R * 0.34); x.lineTo(cx + Math.cos(b) * R * 0.98, cy + Math.sin(b) * R * 0.98); x.stroke(); });
      var best = -1, bd = 18 * 18;
      x.globalCompositeOperation = 'lighter';
      for (i = 0; i < dots.length; i++) { d = dots[i];
        var k = REDUCE ? 1 : Math.max(0, Math.min(1, (age - d.dl) / 0.9)), e = 1 - Math.pow(1 - k, 3), rr = R * d.r * e, an = d.a + rot + (1 - e) * 1.2;
        d.x = cx + Math.cos(an) * rr; d.y = cy + Math.sin(an) * rr;
        var tw = 0.62 + 0.38 * Math.sin(t * 1.3 + d.ph), on = i === pick ? 1 : 0;
        x.fillStyle = 'rgba(' + d.hue + ',' + (0.10 * tw * e + 0.25 * on).toFixed(3) + ')'; x.beginPath(); x.arc(d.x, d.y, d.s * 3.4 + on * 6, 0, 6.2832); x.fill();
        x.fillStyle = 'rgba(' + d.hue + ',' + ((0.55 + 0.45 * tw) * e).toFixed(3) + ')'; x.beginPath(); x.arc(d.x, d.y, d.s + on * 1.6, 0, 6.2832); x.fill();
        if (mouse) { var q = (d.x - mouse.x) * (d.x - mouse.x) + (d.y - mouse.y) * (d.y - mouse.y); if (q < bd) { bd = q; best = i; } }
      }
      if (mouse && best >= 0) { pick = best; pickAt = t + 3; }
      else if (!mouse && t > pickAt && dots.length) { pick = Math.floor(Math.random() * dots.length); pickAt = t + 2.6; }
      if (pick >= 0 && dots[pick]) { d = dots[pick]; var gr = x.createLinearGradient(cx, cy, d.x, d.y); gr.addColorStop(0, 'rgba(255,214,140,0.0)'); gr.addColorStop(0.25, 'rgba(255,214,140,0.5)'); gr.addColorStop(1, 'rgba(' + d.hue + ',0.9)'); x.strokeStyle = gr; x.lineWidth = 1.2; x.beginPath(); x.moveTo(cx, cy); x.lineTo(d.x, d.y); x.stroke();
        if (tip) { tip.innerHTML = '<i>' + d.kind + '</i>' + d.kw.replace(/</g, '&lt;'); var tx = Math.max(8, Math.min(w - 288, d.x + 14)), ty = Math.max(8, Math.min(h - 70, d.y + 14)); tip.style.transform = 'translate(' + tx.toFixed(0) + 'px,' + ty.toFixed(0) + 'px)'; tip.style.opacity = age > 1 ? 1 : 0; } }
      x.globalCompositeOperation = 'source-over';
      if (w >= 520) { x.font = '600 11.5px "Plus Jakarta Sans", sans-serif'; x.textBaseline = 'middle';
        labels.forEach(function (l) { if (l.span < 0.2) return; var an = l.a + rot, lx = cx + Math.cos(an) * (R + 12), ly = cy + Math.sin(an) * (R + 12), right = Math.cos(an) >= 0; x.textAlign = Math.abs(Math.cos(an)) < 0.25 ? 'center' : right ? 'left' : 'right'; x.fillStyle = 'rgba(' + l.hue + ',0.95)'; var nm = l.text + ' \u00B7 ' + l.n, tw = x.measureText(nm).width, fits = x.textAlign === 'center' ? (lx - tw / 2 > 6 && lx + tw / 2 < w - 6) : right ? lx + tw < w - 6 : lx - tw > 6; x.fillText(fits ? nm : l.n + '', lx, ly); }); }
      if (!REDUCE) raf = requestAnimationFrame(draw);
    }
    function kick() { if (!raf && cv) { prev = 0; raf = requestAnimationFrame(draw); } }
    if (sky) {
      sky.addEventListener('mousemove', function (e) { var r = sky.getBoundingClientRect(); mouse = { x: e.clientX - r.left, y: e.clientY - r.top }; });
      sky.addEventListener('mouseleave', function () { mouse = null; });
      onScreen(sky, function (v) { visible = v; kick(); });
    }
    fetch(BASE + 'console-data.json').then(function (r) { return r.json(); }).then(function (j) { counts = j; fill(); }).catch(function () { fill(); });
    trade.addEventListener('change', fill); city.addEventListener('change', fill);
  })();

  /* ---------- 3 · the equation lab: three lenses, each lets through its share of the light ---------- */
  (function () {
    var lab = document.getElementById('lab'); if (!lab) return; if (lab.__rsm) return; lab.__rsm = 1;
    var cv = lab.querySelector('canvas'), ins = [].slice.call(lab.querySelectorAll('input[type=range]')), outs = [].slice.call(lab.querySelectorAll('.dial output')), big = lab.querySelector('[data-rel]'), say = lab.querySelector('[data-say]');
    var cols = [].slice.call(lab.querySelectorAll('.lt')), live = [lab.querySelector('[data-v0]'), lab.querySelector('[data-v1]'), lab.querySelector('[data-v2]')], live2 = lab.querySelector('[data-rel2]');
    var COL = ['248,177,15', '76,192,168', '163,181,242'], cur = [0.8, 0.7, 0.75], tgt = cur.slice(), t = 0, prev = 0, raf = 0, visible = false, ctx = null, CW = 0, CH = 0;
    var logo = new Image(); logo.onload = function () { kick(); }; logo.src = lab.getAttribute('data-logo') || (BASE + 'rsm-logo-512.png');
    var ASKW = null; try { ASKW = JSON.parse(lab.getAttribute('data-ask')); } catch (e) {}
    var sd = 11, rnd = function () { sd = (sd * 9301 + 49297) % 233280; return sd / 233280; };
    var NP = 80, strat = function () { var a = []; for (var i = 0; i < NP; i++) a.push((i + 0.5) / NP); for (var i = NP - 1; i > 0; i--) { var q = Math.floor(rnd() * (i + 1)), tmp = a[i]; a[i] = a[q]; a[q] = tmp; } return a; }, T0 = strat(), T1 = strat(), T2 = strat();
    var parts = []; for (var i = 0; i < NP; i++) parts.push({ u: (i + rnd()) / NP, y: rnd() - 0.5, s: 0.85 + rnd() * 0.3, th: [T0[i], T1[i], T2[i]], r: 1.6 + rnd() * 1.2 });
    function read() {
      ins.forEach(function (el, i) { tgt[i] = el.value / 100; outs[i].textContent = el.value; if (live[i]) live[i].textContent = el.value; });
      var p = Math.round(tgt[0] * tgt[1] * tgt[2] * 100); big.textContent = p; if (live2) live2.textContent = p;
      var W = function (v) { return v >= 0.75 ? 'yes' : v >= 0.45 ? 'partly' : v >= 0.15 ? 'hardly' : 'no'; };
      say.textContent = 'Can engines read you: ' + W(tgt[0]) + '. Do others back you up: ' + W(tgt[1]) + '. Do people pick you: ' + W(tgt[2]) + '. ' + (p < 5 ? 'Almost every customer is sent to someone else.' : p < 30 ? 'Most customers are sent to someone else.' : p < 60 ? 'Some reach you. Fix the weakest check first.' : 'Most customers who ask are sent to you.');
      var lo = 0; for (var i = 1; i < 3; i++) if (tgt[i] < tgt[lo]) lo = i;
      cols.forEach(function (c, i) { var w = c.querySelector('.weak'); var on = i === lo && p < 60; c.classList.toggle('is-weak', on); if (w) { w.hidden = !on; if (w.getAttribute('data-label')) w.textContent = w.getAttribute('data-label'); } });
      try { document.dispatchEvent(new CustomEvent('rsm:relevance', { detail: p })); } catch (e) {}
      kick(); }
    function draw(now) { raf = 0; if (!visible || document.hidden) return;
      var dt = prev ? Math.min(0.05, (now - prev) / 1000) : 0.016; prev = now; t += dt;
      var moving = false, i, k; for (i = 0; i < 3; i++) { var dv = tgt[i] - cur[i]; if (Math.abs(dv) > 0.002) moving = true; cur[i] += dv * Math.min(1, dt * 7); }
      var r = cv.getBoundingClientRect(), w = r.width, h = r.height, dpr = Math.min(window.devicePixelRatio || 1, 2);
      if (CW !== Math.round(w * dpr) || CH !== Math.round(h * dpr)) { CW = cv.width = Math.round(w * dpr); CH = cv.height = Math.round(h * dpr); ctx = null; }
      var x = ctx || (ctx = cv.getContext('2d')); x.setTransform(dpr, 0, 0, dpr, 0, 0); x.clearRect(0, 0, w, h);
      var small = w < 620, cy = h * (small ? 0.44 : 0.45), R = small ? Math.min(h * 0.15, w * 0.1) : Math.min(h * 0.2, w * 0.07, 76), LX = [1 / 8, 3 / 8, 5 / 8].map(function (f) { return w * f; });
      var RD = R * 0.95, xs = small ? 4 : w * 0.015, xe = w * 7 / 8, railY = h - (small ? 16 : 30), out = cur[0] * cur[1] * cur[2];
      var ASK = (ASKW && ASKW.length === 3) ? ASKW : ['Can it read you?', 'Do others back you up?', 'Do people pick you?'], word = function (v) { return v >= 0.75 ? 'Yes' : v >= 0.45 ? 'Partly' : v >= 0.15 ? 'Hardly' : 'No'; };
      var mono = function (px) { return '700 ' + px + 'px "JetBrains Mono", monospace'; }, sora = function (px, wt) { return (wt || 700) + ' ' + px + 'px "Sora", sans-serif'; };
      // ---- the lane the questions travel, narrowing as fewer get through
      x.globalCompositeOperation = 'lighter'; var v = 1, P = [xs].concat(LX, [xe]);
      for (i = 0; i < 4; i++) { if (i > 0) v *= cur[i - 1]; var bh = 3 + R * 0.5 * v, bg = x.createLinearGradient(0, cy - bh, 0, cy + bh); bg.addColorStop(0, 'rgba(248,177,15,0)'); bg.addColorStop(0.5, 'rgba(255,214,140,' + (0.04 + 0.2 * v).toFixed(3) + ')'); bg.addColorStop(1, 'rgba(248,177,15,0)'); x.fillStyle = bg; x.fillRect(P[i], cy - bh, P[i + 1] - P[i], bh * 2); }
      // rays and glow behind "you"
      var rays = 18, rl = RD * (1.2 + 1.4 * out);
      for (i = 0; i < rays; i++) { var an = i / rays * 6.2832 + t * 0.12 * (i % 2 ? 1 : -1), wd = 0.05 + 0.05 * ((i * 7) % 5) / 5, rg = x.createRadialGradient(xe, cy, RD * 0.7, xe, cy, rl); rg.addColorStop(0, 'rgba(255,206,110,' + (0.03 + 0.2 * out).toFixed(3) + ')'); rg.addColorStop(1, 'rgba(248,177,15,0)'); x.fillStyle = rg; x.beginPath(); x.moveTo(xe + Math.cos(an - wd * 0.3) * RD * 0.7, cy + Math.sin(an - wd * 0.3) * RD * 0.7); x.arc(xe, cy, rl, an - wd, an + wd); x.closePath(); x.fill(); }
      for (i = 0; i < 3; i++) { var gg = x.createRadialGradient(LX[i], cy, R * 0.6, LX[i], cy, R * 1.9); gg.addColorStop(0, 'rgba(' + COL[i] + ',' + (0.04 + 0.26 * cur[i]).toFixed(3) + ')'); gg.addColorStop(1, 'rgba(' + COL[i] + ',0)'); x.fillStyle = gg; x.beginPath(); x.arc(LX[i], cy, R * 1.9, 0, 6.2832); x.fill(); }
      x.globalCompositeOperation = 'source-over';
      // ---- the rail underneath: where the lost questions go
      x.strokeStyle = 'rgba(150,170,255,.28)'; x.lineWidth = 1.5; x.setLineDash([3, 6]); x.beginPath(); x.moveTo(LX[0], railY); x.lineTo(w - (small ? 6 : 20), railY); x.stroke(); x.setLineDash([]);
      x.beginPath(); x.moveTo(w - (small ? 6 : 20), railY); x.lineTo(w - (small ? 12 : 28), railY - 5); x.lineTo(w - (small ? 12 : 28), railY + 5); x.closePath(); x.fillStyle = 'rgba(150,170,255,.5)'; x.fill();
      // ---- every light is one customer asking
      for (i = 0; i < parts.length; i++) { var p = parts[i], u = REDUCE ? p.u : (p.u + t * 0.075 * p.s) % 1, px = xs + (xe - xs) * u, stop = -1;
        for (k = 0; k < 3; k++) if (p.th[k] >= cur[k]) { stop = k; break; }
        var sv = 1; for (k = 0; k < 3; k++) if (px > LX[k]) sv *= cur[k];
        var py = cy + p.y * (8 + R * 0.8 * (0.2 + 0.8 * sv)), fade = Math.min(1, u / 0.04);
        if (stop >= 0 && px > LX[stop]) { var d = (px - LX[stop]) / (w * 0.13), e = Math.min(1, d), ee = e * e * (3 - 2 * e); py = py + (railY - py) * ee; var al = d < 1 ? 0.95 : Math.max(0, 0.95 - (d - 1) * 0.9); if (al <= 0) continue;
          x.fillStyle = 'rgba(150,165,215,' + (al * fade).toFixed(3) + ')'; x.beginPath(); x.arc(px, py, p.r + 0.6, 0, 6.2832); x.fill(); }
        else { var gold = px > LX[2] && stop < 0; if (gold && px > xe - RD) continue; x.fillStyle = gold ? 'rgba(255,205,96,' + fade + ')' : 'rgba(236,241,255,' + (0.95 * fade).toFixed(3) + ')'; if (gold) { x.shadowColor = 'rgba(248,177,15,.9)'; x.shadowBlur = 10; } x.beginPath(); x.arc(px, py, p.r + (gold ? 1.6 : 0.8), 0, 6.2832); x.fill(); x.shadowBlur = 0; } }
      // ---- the person asking
      var bx = xs + (small ? 2 : 6), bw = small ? 0 : Math.min(150, LX[0] - R - bx - 14);
      if (bw > 90) { x.fillStyle = 'rgba(30,42,100,.95)'; x.strokeStyle = 'rgba(150,170,255,.5)'; x.lineWidth = 1.2; var by = cy - R - 54; x.beginPath(); x.roundRect(bx, by, bw, 40, 12); x.fill(); x.stroke(); x.fillStyle = '#fff'; x.font = sora(12.5, 600); x.textAlign = 'left'; x.textBaseline = 'middle'; x.fillText('“Who should', bx + 10, by + 13); x.fillText('I call?”', bx + 10, by + 28); }
      // ---- three checks
      for (i = 0; i < 3; i++) { var c = COL[i], val = cur[i], X = LX[i];
        var mg = x.createLinearGradient(X - R, cy - R, X + R, cy + R); mg.addColorStop(0, 'rgba(58,78,170,1)'); mg.addColorStop(0.45, 'rgba(24,32,84,1)'); mg.addColorStop(1, 'rgba(9,13,40,1)');
        x.fillStyle = mg; x.beginPath(); x.arc(X, cy, R * 0.9, 0, 6.2832); x.fill();
        var tint = x.createRadialGradient(X, cy + R * 0.5, 0, X, cy + R * 0.5, R * 1.1); tint.addColorStop(0, 'rgba(' + c + ',' + (0.06 + 0.26 * val).toFixed(3) + ')'); tint.addColorStop(1, 'rgba(' + c + ',0)'); x.fillStyle = tint; x.beginPath(); x.arc(X, cy, R * 0.9, 0, 6.2832); x.fill();
        x.strokeStyle = 'rgba(150,170,255,.22)'; x.lineWidth = Math.max(4, R * 0.09); x.beginPath(); x.arc(X, cy, R, 0, 6.2832); x.stroke();
        x.strokeStyle = 'rgb(' + c + ')'; x.shadowColor = 'rgba(' + c + ',.95)'; x.shadowBlur = 16; x.lineCap = 'round'; x.beginPath(); x.arc(X, cy, R, -Math.PI / 2, -Math.PI / 2 + 6.2832 * Math.max(0.006, val)); x.stroke(); x.shadowBlur = 0;
        var s = R * 0.27, iy = cy - R * 0.36; x.strokeStyle = 'rgb(' + c + ')'; x.lineWidth = Math.max(1.6, R * 0.035); x.lineJoin = 'round'; x.beginPath();
        if (i === 0) { x.rect(X - s * 0.62, iy - s * 0.8, s * 1.24, s * 1.6); x.moveTo(X - s * 0.32, iy - s * 0.36); x.lineTo(X + s * 0.32, iy - s * 0.36); x.moveTo(X - s * 0.32, iy); x.lineTo(X + s * 0.32, iy); x.moveTo(X - s * 0.32, iy + s * 0.36); x.lineTo(X + s * 0.1, iy + s * 0.36); }
        else if (i === 1) { x.moveTo(X, iy - s * 0.9); x.lineTo(X + s * 0.75, iy - s * 0.55); x.lineTo(X + s * 0.75, iy + s * 0.05); x.quadraticCurveTo(X + s * 0.7, iy + s * 0.65, X, iy + s * 0.92); x.quadraticCurveTo(X - s * 0.7, iy + s * 0.65, X - s * 0.75, iy + s * 0.05); x.lineTo(X - s * 0.75, iy - s * 0.55); x.closePath(); x.moveTo(X - s * 0.32, iy); x.lineTo(X - s * 0.06, iy + s * 0.28); x.lineTo(X + s * 0.36, iy - s * 0.26); }
        else { x.moveTo(X - s * 0.5, iy - s * 0.85); x.lineTo(X - s * 0.5, iy + s * 0.55); x.lineTo(X - s * 0.1, iy + s * 0.2); x.lineTo(X + s * 0.2, iy + s * 0.85); x.lineTo(X + s * 0.45, iy + s * 0.72); x.lineTo(X + s * 0.16, iy + s * 0.1); x.lineTo(X + s * 0.68, iy + s * 0.1); x.closePath(); }
        x.stroke();
        x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = '#fff'; x.font = sora(Math.round(R * (small ? 0.36 : 0.38))); x.fillText(word(val), X, cy + R * 0.3);
        x.textBaseline = 'alphabetic'; x.fillStyle = '#fff'; x.font = sora(small ? 9.5 : 14.5, 600); if (!small) x.fillText(ASK[i], X, cy - R - 20); else x.fillText(['Read?', 'Backed up?', 'Picked?'][i], X, cy - R - 10);
        var n10 = Math.round(val * 10), lost = 10 - n10; x.font = mono(small ? 8 : 10.5); x.fillStyle = 'rgb(' + c + ')'; x.fillText(n10 + ' IN 10 GO ON', X, cy + R + (small ? 14 : 22));
        if (lost > 0 && !small) { x.fillStyle = 'rgba(160,175,225,.85)'; x.fillText(lost + ' TURNED AWAY ↓', X, cy + R + 38); } }
      // ---- you
      var dR = RD * (0.8 + 0.2 * out); x.globalAlpha = 0.35 + 0.65 * out; var dg = x.createRadialGradient(xe - dR * 0.2, cy - dR * 0.3, 0, xe, cy, dR); dg.addColorStop(0, '#FBF7EC'); dg.addColorStop(0.6, '#F1E8D4'); dg.addColorStop(1, '#DDD1B6'); x.fillStyle = dg; x.beginPath(); x.arc(xe, cy, dR, 0, 6.2832); x.fill();
      if (logo.complete && logo.naturalWidth) { var lw = dR * 1.3, lh = lw * logo.naturalHeight / logo.naturalWidth; x.drawImage(logo, xe - lw / 2 + dR * 0.03, cy - lh / 2, lw, lh); }
      x.globalAlpha = 1; x.strokeStyle = 'rgba(226,174,69,' + (0.4 + 0.6 * out).toFixed(2) + ')'; x.lineWidth = 2; x.beginPath(); x.arc(xe, cy, dR, 0, 6.2832); x.stroke();
      x.textAlign = 'center'; x.fillStyle = '#fff'; x.font = sora(small ? 9.5 : 14.5, 600); x.fillText(small ? 'You' : 'Sent to you', xe, cy - R - (small ? 10 : 20));
      x.font = mono(small ? 8 : 10.5); x.fillStyle = '#FFD98A'; x.fillText(Math.round(out * 100) + ' IN 100', xe, cy + R + (small ? 14 : 22));
      x.textAlign = 'right'; x.fillStyle = 'rgba(160,175,225,.9)'; x.font = mono(small ? 8 : 10.5); x.fillText('SENT TO SOMEONE ELSE', w - (small ? 16 : 34), railY - 8);
      if (!small) { x.textAlign = 'left'; x.fillStyle = 'rgba(190,200,234,.8)'; x.fillText('● EACH LIGHT IS ONE CUSTOMER ASKING', xs + 6, 22); }
      if (!REDUCE || moving) raf = requestAnimationFrame(draw); }
    function kick() { if (!raf) { prev = 0; raf = requestAnimationFrame(draw); } }
    ins.forEach(function (el) { el.addEventListener('input', read); });
    lab.querySelectorAll('.presets button').forEach(function (b) { b.addEventListener('click', function () { b.getAttribute('data-v').split(',').forEach(function (v, i) { ins[i].value = v; }); read(); }); });
    onScreen(lab, function (v) { visible = v; kick(); });
    read();
  })();

  /* ---------- 4 · five engines: change the question, tap an engine, the answer follows the dials ---------- */
  (function () {
    var q1 = document.getElementById('eg-q1'); if (!q1) return; if (q1.__rsm) return; q1.__rsm = 1;
    var all = function (c) { return [].slice.call(document.querySelectorAll('.' + c)); };
    var Q1 = all('eg-q1'), Q2 = all('eg-q2'), ANS = all('eg-ans'), ANSR = all('eg-ansr'), ANSL = all('eg-ansl'), GLOW = all('eg-glowc'), cap = document.getElementById('eg-cap');
    var outs = all('eg-o'), btns = [].slice.call(document.querySelectorAll('.eg-controls button')), input = document.getElementById('eg-input'), base = cap ? cap.textContent : '';
    function setQ(text) { text = (text || '').trim() || 'Who should I call?'; var w = text.split(' '), a = '', b = ''; w.forEach(function (x) { if (!b && (a + ' ' + x).trim().length <= 14) a = (a + ' ' + x).trim(); else b = (b + ' ' + x).trim(); }); Q1.forEach(function (e) { e.textContent = '\u201C' + a + (b ? '' : '\u201D'); }); Q2.forEach(function (e) { e.textContent = b ? b + '\u201D' : ''; }); }
    btns.forEach(function (b) { b.addEventListener('click', function () { btns.forEach(function (o) { o.classList.toggle('on', o === b); }); if (input) input.value = ''; setQ(b.getAttribute('data-q')); }); });
    if (input) input.addEventListener('input', function () { btns.forEach(function (o) { o.classList.remove('on'); }); setQ(input.value); });
    all('eg-tile').forEach(function (g) { var show = function () { if (cap) cap.textContent = g.getAttribute('data-info'); }, hide = function () { if (cap) cap.textContent = base; };
      g.addEventListener('mouseenter', show); g.addEventListener('focus', show); g.addEventListener('click', show); g.addEventListener('mouseleave', hide); g.addEventListener('blur', hide); });
    document.addEventListener('rsm:relevance', function (e) { var p = e.detail, you = p >= 30, k = Math.max(0.12, Math.min(1, p / 60));
      ANS.forEach(function (ans) { ans.textContent = you ? (ans.getAttribute('data-yes') || 'You.') : (ans.getAttribute('data-no') || 'Someone else.'); ans.setAttribute('font-size', you ? (ans.id ? 23 : 22) : 18); ans.setAttribute('fill', you ? '#fff' : '#B9C4EA'); });
      ANSR.forEach(function (r) { r.setAttribute('stroke', you ? 'rgba(248,177,15,.8)' : 'rgba(150,170,255,.35)'); }); ANSL.forEach(function (l) { l.setAttribute('fill', you ? '#FFD98A' : '#8A97C4'); }); GLOW.forEach(function (g) { g.setAttribute('opacity', you ? k : 0.05); });
      outs.forEach(function (o) { o.setAttribute('opacity', k); }); });
  })();

  /* ---- the film: rolls muted when on screen, chapters jump, one button for sound ---- */
  (function () {
    var v = document.querySelector('.film video'); if (!v) return; if (v.__rsm) return; v.__rsm = 1; var ROLL = v.hasAttribute('data-roll');
    var btn = document.getElementById('film-sound'), chaps = [].slice.call(document.querySelectorAll('.beats button'));
    var play = function () { var p = v.play(); if (p && p.catch) p.catch(function () {}); };
    if (ROLL && !REDUCE && window.IntersectionObserver) new IntersectionObserver(function (es) { var on = es[0].isIntersecting && es[0].intersectionRatio > 0.45; if (on) play(); else if (!v.paused) v.pause(); }, { threshold: [0, 0.45, 0.8] }).observe(v);
    chaps.forEach(function (b) { b.addEventListener('click', function () { v.currentTime = parseFloat(b.getAttribute('data-t')) + 0.05; play(); }); });
    v.addEventListener('timeupdate', function () { var cur = 0; chaps.forEach(function (b, i) { if (v.currentTime >= parseFloat(b.getAttribute('data-t'))) cur = i; }); chaps.forEach(function (b, i) { b.classList.toggle('on', i === cur); }); });
    if (btn) { var sync = function () { var on = !v.muted; btn.setAttribute('aria-pressed', on ? 'true' : 'false'); btn.textContent = on ? (btn.getAttribute('data-on') || 'Sound on') : (btn.getAttribute('data-off') || 'Play with sound'); };
      btn.addEventListener('click', function () { if (v.muted) { v.muted = false; v.currentTime = 0; play(); } else v.muted = true; sync(); }); v.addEventListener('volumechange', sync); }
  })();
  /* ---- header menus: Escape closes, and a click outside closes the small-screen menu ---- */
  (function () {
    if (window.__rsmMenus) return; window.__rsmMenus = 1;
    document.addEventListener('keydown', function (e) { if (e.key !== 'Escape') return; if (document.activeElement && document.activeElement.blur) document.activeElement.blur(); var m = document.querySelector('details.menu[open]'); if (m) m.open = false; });
    document.addEventListener('click', function (e) { var m = document.querySelector('details.menu[open]'); if (m && !m.contains(e.target)) m.open = false; });
  })();
};
window.RSMInit();
(function () { var T; function again() { clearTimeout(T); T = setTimeout(window.RSMInit, 180); }
  if (window.jQuery) window.jQuery(window).on('elementor/frontend/init', function () { if (window.elementorFrontend && elementorFrontend.hooks) elementorFrontend.hooks.addAction('frontend/element_ready/widget', again); });
})();

/* ---- phones: dots under swipe rows, and the bottom bar appears once the first screen is passed ---- */
(function () {
  function dots() {
    if (!window.matchMedia('(max-width:760px)').matches) return;
    document.querySelectorAll('.e-grid').forEach(function (g) {
      if (g.__rsmDots || !g.querySelector(':scope > .elementor-widget-rsm-card .problems, :scope > .elementor-widget-rsm-card .days, :scope > .elementor-widget-rsm-card .status')) return;
      var kids = g.querySelectorAll(':scope > .elementor-widget'); if (kids.length < 2) return; g.__rsmDots = 1;
      var d = document.createElement('div'); d.className = 'rs-dots'; d.setAttribute('aria-hidden', 'true');
      for (var i = 0; i < kids.length; i++) d.appendChild(document.createElement('i'));
      g.parentNode.insertBefore(d, g.nextSibling);
      function mark() { var best = 0, bd = 1e9, x = g.scrollLeft; for (var i = 0; i < kids.length; i++) { var dx = Math.abs(kids[i].offsetLeft - g.offsetLeft - x - 16 + 16); if (dx < bd) { bd = dx; best = i; } } if (g.scrollLeft + g.clientWidth >= g.scrollWidth - 4) best = kids.length - 1; for (var j = 0; j < d.children.length; j++) d.children[j].className = j === best ? 'on' : ''; }
      g.addEventListener('scroll', function () { window.requestAnimationFrame(mark); }, { passive: true }); mark();
    });
  }
  function bar() { var b = document.querySelector('.rs-mobilebar'); if (!b || b.__rsm) return; b.__rsm = 1;
    function on() { b.classList.toggle('show', window.scrollY > 420); } window.addEventListener('scroll', on, { passive: true }); on(); }
  function go() { dots(); bar(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go); else go();
  window.addEventListener('load', go);
})();

/* ---- desktop: the problem picker shows one answer at a time ---- */
(function () {
  function pick() {
    document.querySelectorAll('.rs-pick').forEach(function (g) { if (g.__rsmPick) return; var cards = [].slice.call(g.querySelectorAll('a.card, div.card')); if (!cards.length) return; g.__rsmPick = 1;
      function on(c) { cards.forEach(function (o) { o.classList.toggle('on', o === c); }); }
      cards.forEach(function (c) { var h = c.querySelector('.c-head'); if (!h) return; h.addEventListener('mouseenter', function () { on(c); }); c.addEventListener('focus', function () { on(c); }); });
      on(cards[0]); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', pick); else pick();
  window.addEventListener('load', pick);
})();

/* ---- 07: the traveller crosses each milestone slowly, rests on it, and leaves it lit ---- */
(function () {
  function go() { var fig = document.querySelector('.rs-path-sync'); if (!fig || fig.__rsmJ) return; var svg = fig.querySelector('svg'), path = svg && svg.querySelector('path.base'), trav = svg && svg.querySelector('.trav'); if (!path || !trav) return; fig.__rsmJ = 1;
    var trail = svg.querySelector('.trail'), glow = svg.querySelector('.trail-glow'), ms = [].slice.call(svg.querySelectorAll('.ms')), ticks = [].slice.call(svg.querySelectorAll('.tick'));
    var days = [].slice.call(document.querySelectorAll('.rs-journey .rs-day')), cad = [].slice.call(document.querySelectorAll('.rs-cadence .rs-cad'));
    var L = path.getTotalLength(), lenAt = function (x) { var lo = 0, hi = L; for (var k = 0; k < 24; k++) { var m = (lo + hi) / 2; if (path.getPointAtLength(m).x < x) lo = m; else hi = m; } return lo; };
    var stops = ms.map(function (g) { return lenAt(parseFloat(g.getAttribute('data-x'))); }), tl = ticks.map(function (g) { return lenAt(parseFloat(g.getAttribute('data-x'))); });
    if (stops.length < 2) return;
    [trail, glow].forEach(function (p) { if (p) { p.style.strokeDasharray = L + ' ' + L; p.style.strokeDashoffset = L; } });
    fig.classList.add('is-live');
    if (window.matchMedia('(prefers-reduced-motion:reduce)').matches) { fig.classList.add('is-still'); ms.forEach(function (g) { g.classList.add('on'); }); ticks.forEach(function (g) { g.classList.add('on'); }); return; }
    /* timeline: rest on a milestone, glide to the next */
    var REST = 1.5, GLIDE = 2.1, LONG = 6.5, END = 3.2, FADE = 1.0, segs = [], T = 0;
    for (var i = 0; i < stops.length; i++) { segs.push({ k: 'rest', i: i, t0: T, d: i === stops.length - 1 ? END : REST }); T += segs[segs.length - 1].d;
      if (i < stops.length - 1) { var d = i === stops.length - 2 ? LONG : GLIDE; segs.push({ k: 'move', i: i, t0: T, d: d }); T += d; } }
    segs.push({ k: 'fade', t0: T, d: FADE }); T += FADE;
    var ease = function (u) { return u < 0.5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2; }, start = 0, raf = 0, vis = false, lastKey = '';
    function set(len, op) { var p = path.getPointAtLength(len); trav.setAttribute('transform', 'translate(' + p.x.toFixed(1) + ',' + p.y.toFixed(1) + ')'); trav.setAttribute('opacity', op); [trail, glow].forEach(function (q, n) { if (q) { q.style.strokeDashoffset = (L - len).toFixed(1); q.setAttribute('opacity', (op * (n ? 0.5 : 0.95)).toFixed(2)); } }); }
    function frame(now) { raf = 0; if (!vis) return; if (!start) start = now; var t = ((now - start) / 1000) % T, sg = segs[0]; for (var i = 0; i < segs.length; i++) if (t >= segs[i].t0) sg = segs[i];
      var u = Math.min(1, (t - sg.t0) / sg.d), len, op = 1, at = -1, reached = -1, wide = window.innerWidth >= 761;
      if (sg.k === 'rest') { len = stops[sg.i]; at = sg.i; reached = sg.i; if (sg.i === 0) op = Math.min(1, u * 3); }
      else if (sg.k === 'move') { var last = sg.i === stops.length - 2; len = stops[sg.i] + (stops[sg.i + 1] - stops[sg.i]) * (last ? u : ease(u)); reached = sg.i; }
      else { len = stops[stops.length - 1]; op = 1 - u; reached = u < 0.6 ? stops.length - 1 : -1; }
      set(len, op);
      var nt = 0; for (var k = 0; k < tl.length; k++) if (len >= tl[k] - 2 && reached >= 0) nt = k + 1;
      var daily = sg.k === 'move' && sg.i === stops.length - 2, report = (sg.k === 'rest' && sg.i === stops.length - 1), key = [sg.k, at, reached, nt, wide].join('|');
      if (key !== lastKey) { lastKey = key;
        ms.forEach(function (g, k) { g.classList.toggle('on', k <= reached); g.classList.toggle('at', k === at); });
        ticks.forEach(function (g, k) { g.classList.toggle('on', k < nt); });
        days.forEach(function (c, k) { c.classList.toggle('lit', wide && k === at && k < 5); c.classList.toggle('done', wide && k <= reached && k !== at); });
        cad.forEach(function (c, k) { c.classList.toggle('lit', wide && ((k === 0 && daily) || (k === 1 && report))); }); }
      raf = requestAnimationFrame(frame); }
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { vis = es[0].isIntersecting; if (vis && !raf) raf = requestAnimationFrame(frame); }, { threshold: 0.15 }).observe(fig); else { vis = true; raf = requestAnimationFrame(frame); }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go); else go();
  window.addEventListener('load', go);
})();

/* ---- ask: narrow the questions as you type; enquiry form: send without leaving the page ---- */
(function () {
  function go() {
    document.querySelectorAll('.ask').forEach(function (box) { if (box.__rsm) return; box.__rsm = 1; var inp = box.querySelector('.ask-input'), none = box.querySelector('.ask-none'), groups = [].slice.call(box.querySelectorAll('.ask-group')), stop = /^(the|a|an|and|or|of|to|in|on|for|my|is|are|do|does|i|how|what|why|can|it|me|with|not)$/;
      inp.addEventListener('input', function () { var ws = inp.value.toLowerCase().split(/[^a-z0-9]+/).filter(function (w) { return w.length > 1 && !stop.test(w); }), shown = 0;
        groups.forEach(function (g) { var items = [].slice.call(g.querySelectorAll('li')), head = (g.querySelector('.ask-title').textContent + ' ' + ((g.querySelector('.ask-desc') || {}).textContent || '')).toLowerCase(), any = 0;
          var hm = !ws.length || ws.some(function (w) { return head.indexOf(w) >= 0; });
          items.forEach(function (li) { var t = li.textContent.toLowerCase(), m = !ws.length || ws.every(function (w) { return t.indexOf(w) >= 0; }) || (ws.length > 1 && ws.filter(function (w) { return t.indexOf(w) >= 0; }).length >= Math.ceil(ws.length * 0.6)); li.hidden = !m; if (m) any++; });
          var show = any > 0 || hm; if (!any && hm) items.forEach(function (li) { li.hidden = false; }); g.hidden = !show; if (show) shown++; });
        none.hidden = shown > 0; }); });
    document.querySelectorAll('.std').forEach(function (box) { if (box.__rsm) return; box.__rsm = 1; var inp = box.querySelector('.std-input'), groups = [].slice.call(box.querySelectorAll('.std-group')), first = groups.map(function (g) { return g.open; });
      inp.addEventListener('input', function () { var q = inp.value.toLowerCase().trim();
        groups.forEach(function (g, gi) { var any = 0; [].slice.call(g.querySelectorAll('li')).forEach(function (li) { var m = !q || li.textContent.toLowerCase().indexOf(q) >= 0; li.hidden = !m; if (m) any++; }); g.hidden = !any; g.open = q ? any > 0 : first[gi]; }); }); });
    document.querySelectorAll('form.lead-form').forEach(function (f) { if (f.__rsm) return; f.__rsm = 1; var st = f.querySelector('.lf-status'), btn = f.querySelector('.lf-send');
      f.addEventListener('submit', function (e) { e.preventDefault(); var d = {}, bad = null; [].slice.call(f.elements).forEach(function (el) { if (el.name) d[el.name] = el.value.trim(); if (!bad && el.required && !el.value.trim()) bad = el; }); d.kind = f.getAttribute('data-kind') || ''; d.page = f.getAttribute('data-page') || location.href;
        if (!bad && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.email || '')) bad = f.elements.email;
        if (bad) { bad.focus(); st.textContent = 'Please fill in your name and a valid email.'; st.className = 'lf-status is-bad'; return; }
        btn.disabled = true; st.textContent = 'Sending…'; st.className = 'lf-status';
        fetch(f.action, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(d) }).then(function (r) { return r.json().then(function (j) { return { ok: r.ok && j && j.ok, j: j }; }); })
          .then(function (r) { if (!r.ok) throw new Error(); f.classList.add('is-done'); st.textContent = f.getAttribute('data-done'); st.className = 'lf-status is-ok'; f.reset(); })
          .catch(function () { st.textContent = f.getAttribute('data-fail'); st.className = 'lf-status is-bad'; btn.disabled = false; }); }); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go); else go();
  window.addEventListener('load', go);
})();
