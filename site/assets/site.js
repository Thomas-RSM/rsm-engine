/* Relevant Search Media — page script. The page reads and works without it; it adds the living pictures. */
(function () {
  'use strict';
  var BASE = (function () { try { return new URL('.', document.currentScript.src).href; } catch (e) { return '/assets/'; } })();
  var REDUCE = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  document.documentElement.classList.remove('no-js');
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
    var I = [{"name": "Google", "c": "#6F8CF0", "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 48 48\"> <path d=\"M44 24.5c0-1.57-.14-3.09-.4-4.55H24v8.51h11.26c-.49 2.63-1.97 4.85-4.2 6.34v5.27h6.8c3.97-3.66 6.14-9.04 6.14-15.57z\" fill=\"#4285F4\" /> <path d=\"M24 46c5.7 0 10.49-1.89 13.99-5.13l-6.83-5.27c-1.89 1.27-4.31 2.01-7.16 2.01-5.5 0-10.16-3.71-11.83-8.7H5.14v5.44C8.7 41.35 15.84 46 24 46z\" fill=\"#34A853\" /> <path d=\"M12.17 28.91c-.88-2.55-.88-5.27 0-7.82V15.65H5.14C2.38 19.88 1 24.88 1 26s1.38 6.12 4.14 10.35l7.03-5.44z\" fill=\"#FBBC05\" /> <path d=\"M24 10.28c3.1 0 5.88 1.07 8.07 3.16l6.04-6.04C34.46 4.04 29.67 2 24 2 15.84 2 8.7 6.65 5.14 13.65l7.03 5.44c1.67-4.99 6.33-8.81 11.83-8.81z\" fill=\"#EA4335\" /> </svg>"}, {"name": "SEO", "c": "#6F8CF0", "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 48 48\" fill=\"none\"> <circle cx=\"19\" cy=\"19\" r=\"13\" stroke=\"#6F8CF0\" stroke-width=\"3.5\" /> <line x1=\"28.5\" y1=\"28.5\" x2=\"43\" y2=\"43\" stroke=\"#6F8CF0\" stroke-width=\"4\" stroke-linecap=\"round\" /> </svg>"}, {"name": "AEO", "c": "#4CC0A8", "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 48 48\" fill=\"none\"> <rect x=\"5\" y=\"7\" width=\"38\" height=\"34\" rx=\"5\" stroke=\"#4CC0A8\" stroke-width=\"2.5\" /> <circle cx=\"37\" cy=\"13\" r=\"6\" fill=\"#4CC0A8\" /> </svg>"}, {"name": "AIO", "c": "#A3B5F2", "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 48 48\" fill=\"none\"> <path d=\"M24 3L5 13.5v21L24 45l19-10.5v-21L24 3z\" stroke=\"#A3B5F2\" stroke-width=\"2.5\" /> <circle cx=\"24\" cy=\"24\" r=\"6\" fill=\"#A3B5F2\" opacity=\".85\" /> </svg>"}, {"name": "E-E-A-T", "c": "#A3B5F2", "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 48 48\" fill=\"none\"> <path d=\"M24 3l6 12.2L43 17.2l-9.5 9.3L35.7 40 24 33.8 12.3 40l2.2-13.5L5 17.2l13-2L24 3z\" fill=\"#A3B5F2\" opacity=\".85\" /> </svg>"}, {"name": "ChatGPT", "c": "#4CC0A8", "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 48 48\"> <circle cx=\"24\" cy=\"24\" r=\"20\" fill=\"#10a37f\" /> <path d=\"M16 20c0-4.4 3.6-8 8-8s8 3.6 8 8\" stroke=\"#fff\" stroke-width=\"2.5\" fill=\"none\" stroke-linecap=\"round\" opacity=\".7\" /> <rect x=\"16\" y=\"23\" width=\"16\" height=\"10\" rx=\"2\" fill=\"#fff\" opacity=\".7\" /> </svg>"}, {"name": "Maps", "c": "#F8B10F", "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 48 48\"> <path d=\"M24 2C14.6 2 7 9.4 7 18.5 7 31 24 46 24 46s17-15 17-27.5C41 9.4 33.4 2 24 2z\" fill=\"#EA4335\" /> <circle cx=\"24\" cy=\"18\" r=\"4.5\" fill=\"#fff\" /> </svg>"}, {"name": "Schema", "c": "#4CC0A8", "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 48 48\" fill=\"none\"> <path d=\"M16 7L3 24l13 17\" stroke=\"#4CC0A8\" stroke-width=\"3.5\" stroke-linecap=\"round\" /> <path d=\"M32 7l13 17-13 17\" stroke=\"#4CC0A8\" stroke-width=\"3.5\" stroke-linecap=\"round\" /> </svg>"}, {"name": "Perplexity", "c": "#4CC0A8", "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 48 48\" fill=\"none\"> <circle cx=\"24\" cy=\"24\" r=\"19\" stroke=\"#1a7f64\" stroke-width=\"2.5\" /> <path d=\"M12 24h10l4-8 4 16 4-8h10\" stroke=\"#1a7f64\" stroke-width=\"2.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\" /> </svg>"}, {"name": "Copilot", "c": "#1EA7E8", "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 48 48\"> <path d=\"M9 5v31l11 7 19-11.5v-8L22 17l-5 2.5V5H9z\" fill=\"#00a4ef\" /> </svg>"}, {"name": "Reddit", "c": "#F8B10F", "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 48 48\"> <circle cx=\"24\" cy=\"24\" r=\"19\" fill=\"#FF4500\" /> <ellipse cx=\"24\" cy=\"28.5\" rx=\"11\" ry=\"7.5\" fill=\"#fff\" /> <circle cx=\"19.5\" cy=\"26.5\" r=\"2.5\" fill=\"#FF4500\" /> <circle cx=\"28.5\" cy=\"26.5\" r=\"2.5\" fill=\"#FF4500\" /> </svg>"}, {"name": "Gemini", "c": "#6F8CF0", "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 48 48\" fill=\"none\"> <path d=\"M24 2C17 14 9 18 2 26c7 6 15 12 22 20 7-8 15-14 22-20C39 18 31 14 24 2z\" fill=\"url(#gem)\" /> <defs> <linearGradient id=\"gem\" x1=\"2\" y1=\"2\" x2=\"46\" y2=\"46\"> <stop stop-color=\"#4285F4\" /> <stop offset=\".33\" stop-color=\"#34A853\" /> <stop offset=\".66\" stop-color=\"#FBBC05\" /> <stop offset=\"1\" stop-color=\"#EA4335\" /> </linearGradient> </defs> </svg>"}, {"name": "Local SEO", "c": "#F8B10F", "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 48 48\" fill=\"none\"> <circle cx=\"24\" cy=\"19\" r=\"15\" stroke=\"#F8B10F\" stroke-width=\"2.5\" /> <path d=\"M17 42l7-7 7 7\" stroke=\"#F8B10F\" stroke-width=\"3\" stroke-linecap=\"round\" /> </svg>"}, {"name": "GBP", "c": "#4CC0A8", "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 48 48\" fill=\"none\"> <rect x=\"7\" y=\"9\" width=\"34\" height=\"30\" rx=\"4\" stroke=\"#34A853\" stroke-width=\"2.5\" /> <circle cx=\"24\" cy=\"21\" r=\"7\" stroke=\"#34A853\" stroke-width=\"2.5\" /> </svg>"}, {"name": "Citations", "c": "#A3B5F2", "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 48 48\" fill=\"none\"> <path d=\"M9 11h30v32H9z\" stroke=\"#A3B5F2\" stroke-width=\"2.5\" /> <path d=\"M15 20h18M15 26.5h14\" stroke=\"#A3B5F2\" stroke-width=\"2.5\" stroke-linecap=\"round\" opacity=\".55\" /> </svg>"}, {"name": "Tech SEO", "c": "#F8B10F", "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 48 48\" fill=\"none\"> <circle cx=\"24\" cy=\"24\" r=\"9\" stroke=\"#F8B10F\" stroke-width=\"3\" /> <path d=\"M24 3v7M24 38v7M3 24h7M38 24h7\" stroke=\"#F8B10F\" stroke-width=\"3\" stroke-linecap=\"round\" /> </svg>"}, {"name": "Links", "c": "#6F8CF0", "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 48 48\" fill=\"none\"> <path d=\"M19 29l-5 5a6.4 6.4 0 010-9l9-9a6.4 6.4 0 019 0 6.4 6.4 0 010 9\" stroke=\"#6F8CF0\" stroke-width=\"3.5\" stroke-linecap=\"round\" /> <path d=\"M29 19l5-5a6.4 6.4 0 010 9l-9 9a6.4 6.4 0 01-9 0 6.4 6.4 0 010-9\" stroke=\"#6F8CF0\" stroke-width=\"3.5\" stroke-linecap=\"round\" /> </svg>"}, {"name": "Content", "c": "#A3B5F2", "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 48 48\" fill=\"none\"> <path d=\"M7 5h26l8 8v30a2 2 0 01-2 2H9a2 2 0 01-2-2V7a2 2 0 012-2z\" stroke=\"#A3B5F2\" stroke-width=\"2.5\" /> </svg>"}, {"name": "Voice", "c": "#1EA7E8", "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 48 48\" fill=\"none\"> <rect x=\"17\" y=\"5\" width=\"14\" height=\"24\" rx=\"7\" stroke=\"#1EA7E8\" stroke-width=\"2.5\" /> <path d=\"M11 24c0 7.2 5.8 13 13 13s13-5.8 13-13\" stroke=\"#1EA7E8\" stroke-width=\"2.5\" stroke-linecap=\"round\" /> </svg>"}, {"name": "Snippets", "c": "#F8B10F", "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 48 48\" fill=\"none\"> <rect x=\"5\" y=\"7\" width=\"38\" height=\"14\" rx=\"4\" stroke=\"#F8B10F\" stroke-width=\"2.5\" /> </svg>"}];
    I.forEach(function (i) { i.src = 'url("data:image/svg+xml;utf8,' + encodeURIComponent(i.svg).replace(/'/g, '%27').replace(/\(/g, '%28').replace(/\)/g, '%29') + '")'; });
    var RINGS = [{ ids: [0, 1, 2, 3, 4], spd: 8 }, { ids: [5, 6, 7, 8, 9, 10, 11], spd: 5 }, { ids: [12, 13, 14, 15, 16, 17, 18, 19], spd: 3 }];
    var META = new Array(20); RINGS.forEach(function (r, ri) { r.ids.forEach(function (id, i) { META[id] = { ri: ri, i: i, n: r.ids.length }; }); });
    var RGB = I.map(function (ic) { return [parseInt(ic.c.slice(1, 3), 16), parseInt(ic.c.slice(3, 5), 16), parseInt(ic.c.slice(5, 7), 16)]; });
    var mk = function (tag, cls) { var e = document.createElement(tag); if (cls) e.className = cls; e.setAttribute('aria-hidden', 'true'); return e; };
    var light = mk('div', 'o-light'), rayA = mk('canvas'), rayB = mk('canvas'), cv = mk('canvas'), core = root.querySelector('.o-core');
    root.insertBefore(cv, core); root.insertBefore(rayB, cv); root.insertBefore(rayA, rayB); root.insertBefore(light, rayA);
    var els = [], gls = [], boxes = [], ics = [], names = [];
    var hover = -1, boost = new Float32Array(20), hov = new Float32Array(20), lastG = new Float32Array(20).fill(-1), lastZ = new Int16Array(20).fill(-1);
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
      if (w < 820) { var k = Math.min(1.6, w / 390), h = 800, sm = w < 480;
        return { w: w, h: h, cx: w / 2, cy: h / 2 - 8, rx: (sm ? [58, 108, 160] : [62, 110, 158]).map(function (v) { return v * k; }), ry: [126, 232, 330], tile: sm ? 36 : 40, icon: sm ? 19 : 21, lf: sm ? 6.5 : 7, ls: sm ? 0.6 : 1, gap: 5, logo: sm ? Math.min(72, w * 0.17) : Math.min(78, w * 0.18) }; }
      var tab = w < 1100, X = Math.min(540, w / 2 - 52), tile = tab ? 48 : 56, f = tab ? [0.5, 0.77, 1] : [0.52, 0.78, 1];
      var ry = tab ? [130, 216, 302] : [144, 238, 336], hh = tab ? 720 : 804;
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
    function place(tt) { var g = G, out = new Array(20);
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
      for (i = 0; i < 20; i++) { boost[i] = Math.max(0, boost[i] - dt * 1.4); hov[i] += ((hover === i ? 1 : 0) - hov[i]) * Math.min(1, dt * 9); }
      x.globalCompositeOperation = 'lighter'; x.lineCap = 'round'; x.lineJoin = 'round';
      var v = Math.min(1, 0.84 + 0.12 * br + 0.1 * kk).toFixed(2); if (v !== _lo) { light.style.opacity = v; _lo = v; }
      rayA.style.transform = 'rotate(' + (tt * 0.69).toFixed(3) + 'deg)'; v = Math.min(1, 0.78 + 0.22 * Math.sin(tt * 0.27) + 0.15 * kk).toFixed(2); if (v !== _ao) { rayA.style.opacity = v; _ao = v; }
      rayB.style.transform = 'rotate(' + (-tt * 0.52).toFixed(3) + 'deg)'; v = Math.min(1, 0.74 + 0.26 * Math.sin(tt * 0.33 + 2.1) + 0.15 * kk).toFixed(2); if (v !== _bo) { rayB.style.opacity = v; _bo = v; }
      for (id = 0; id < 20; id++) { var m = META[id], c = RGB[id], q = P[id], n = 7, span = 0.34 * (m.ri === 0 ? 1.3 : m.ri === 1 ? 1 : 0.8), rx = g.rx[m.ri], ry = g.ry[m.ri];
        var px = cx + Math.cos(q.a) * rx, py = cy + Math.sin(q.a) * ry;
        for (var j = 1; j <= n; j++) { var a1 = q.a - span * j / n, f = 1 - (j - 1) / n, nx = cx + Math.cos(a1) * rx, ny = cy + Math.sin(a1) * ry; x.strokeStyle = 'rgba(' + c[0] + ',' + c[1] + ',' + c[2] + ',' + (f * f * (0.16 + 0.34 * q.d)).toFixed(3) + ')'; x.lineWidth = 1 + 1.4 * f; x.beginPath(); x.moveTo(px, py); x.lineTo(nx, ny); x.stroke(); px = nx; py = ny; } }
      RINGS.forEach(function (ring) { var n = ring.ids.length; x.beginPath(); for (var i = 0; i < n; i++) { var A = P[ring.ids[i]], B = P[ring.ids[(i + 1) % n]]; x.moveTo(A.x, A.y); for (var k = 1; k <= 12; k++) { var p = onPath(A.x, A.y, B.x, B.y, k / 12, ring.ids[i] + 20, tt, amp * 0.8); x.lineTo(p[0], p[1]); } } x.strokeStyle = 'rgba(163,181,242,0.085)'; x.lineWidth = 0.8; x.stroke(); });
      order = order || Array.from({ length: 20 }, function (_, i) { return i; }); order.sort(function (a, b) { return P[a].d - P[b].d; });
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
      for (id = 0; id < 20; id++) { var q2 = P[id], m2 = META[id], hv = hov[id], e = Math.min(1, boost[id] + hv), k3 = 0.9 + 0.1 * q2.d + 0.1 * hv;
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
    if (!trade || !city || !window.fetch) return;
    var counts = null, maps = {}, cv = sky && sky.querySelector('canvas'), tip = sky && sky.querySelector('.sky-tip'), kindsEl = document.getElementById('kinds');
    var HUES = ['248,177,15', '163,181,242', '76,192,168', '111,140,240', '246,241,230', '30,167,232'];
    var dots = [], labels = [], born = 0, t = 0, prev = 0, raf = 0, visible = false, mouse = null, pick = -1, pickAt = 0, ctx = null, CW = 0, CH = 0;
    function set(sel, text) { document.querySelectorAll(sel).forEach(function (el) { el.textContent = text; }); }
    function fill() {
      var tv = trade.value, cvv = city.value, cityName = city.options[city.selectedIndex].text, tradeName = trade.options[trade.selectedIndex].text;
      set('[data-trade-name]', tradeName.toLowerCase()); set('[data-city-name]', cityName);
      var d = counts && counts[tv] && counts[tv].c && counts[tv].c[cvv];
      if (d) { set('[data-count]', d.n.toLocaleString('en-US')); set('[data-ex1]', d.ex[0] || ''); set('[data-ex2]', d.ex[1] || ''); set('[data-kinds]', String(d.k)); }
      var isPlumb = tv === 'plumbers';
      set('[data-confirm-status]', isPlumb ? 'first run' : 'not run yet'); set('[data-confirm-big]', isPlumb ? 'In progress' : 'Coming');
      set('[data-confirm-line]', isPlumb ? 'The AI Recommendation Index is being run for plumbers in the launch cities this month. Published when it is done.' : 'The Index runs trade by trade. ' + tradeName + ' in ' + cityName + ' is not published yet; ask to be told when it is.');
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
      if (w >= 520) { x.font = '600 10.5px "JetBrains Mono", monospace'; x.textBaseline = 'middle';
        labels.forEach(function (l) { if (l.span < 0.2) return; var an = l.a + rot, lx = cx + Math.cos(an) * (R + 12), ly = cy + Math.sin(an) * (R + 12), right = Math.cos(an) >= 0; x.textAlign = Math.abs(Math.cos(an)) < 0.25 ? 'center' : right ? 'left' : 'right'; x.fillStyle = 'rgba(' + l.hue + ',0.95)'; x.fillText(l.n + '', lx, ly); }); }
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
    var lab = document.getElementById('lab'); if (!lab) return;
    var cv = lab.querySelector('canvas'), ins = [].slice.call(lab.querySelectorAll('input[type=range]')), outs = [].slice.call(lab.querySelectorAll('.dial output')), big = lab.querySelector('[data-rel]'), say = lab.querySelector('[data-say]');
    var cols = [].slice.call(lab.querySelectorAll('.lt')), live = [lab.querySelector('[data-v0]'), lab.querySelector('[data-v1]'), lab.querySelector('[data-v2]')], live2 = lab.querySelector('[data-rel2]');
    var COL = ['248,177,15', '76,192,168', '163,181,242'], cur = [0.8, 0.7, 0.75], tgt = cur.slice(), t = 0, prev = 0, raf = 0, visible = false, ctx = null, CW = 0, CH = 0;
    var sd = 11, rnd = function () { sd = (sd * 9301 + 49297) % 233280; return sd / 233280; };
    var parts = []; for (var i = 0; i < 90; i++) parts.push({ u: rnd(), y: rnd() - 0.5, s: 0.7 + rnd() * 0.6, th: [rnd(), rnd(), rnd()], r: 1 + rnd() * 1.4 });
    function read() {
      ins.forEach(function (el, i) { tgt[i] = el.value / 100; outs[i].textContent = el.value; if (live[i]) live[i].textContent = el.value; });
      var p = Math.round(tgt[0] * tgt[1] * tgt[2] * 100); big.textContent = p; if (live2) live2.textContent = p;
      say.textContent = p < 5 ? 'Engines pass you by. One term near zero cancels the other two.' : p < 30 ? 'Named now and then. The weakest term is holding the other two down.' : p < 60 ? 'Named often. Raise the lowest term first; that is where the gain is.' : 'The answer. All three are strong, so every engine has a reason to name you.';
      var lo = 0; for (var i = 1; i < 3; i++) if (tgt[i] < tgt[lo]) lo = i;
      cols.forEach(function (c, i) { var w = c.querySelector('.weak'); var on = i === lo && p < 60; c.classList.toggle('is-weak', on); if (w) w.hidden = !on; });
      try { document.dispatchEvent(new CustomEvent('rsm:relevance', { detail: p })); } catch (e) {}
      kick(); }
    function draw(now) { raf = 0; if (!visible || document.hidden) return;
      var dt = prev ? Math.min(0.05, (now - prev) / 1000) : 0.016; prev = now; t += dt;
      var moving = false, i; for (i = 0; i < 3; i++) { var dv = tgt[i] - cur[i]; if (Math.abs(dv) > 0.002) moving = true; cur[i] += dv * Math.min(1, dt * 7); }
      var r = cv.getBoundingClientRect(), w = r.width, h = r.height, dpr = Math.min(window.devicePixelRatio || 1, 2);
      if (CW !== Math.round(w * dpr) || CH !== Math.round(h * dpr)) { CW = cv.width = Math.round(w * dpr); CH = cv.height = Math.round(h * dpr); ctx = null; }
      var x = ctx || (ctx = cv.getContext('2d')); x.setTransform(dpr, 0, 0, dpr, 0, 0); x.clearRect(0, 0, w, h);
      var cy = h * 0.5, x0 = w * 0.015, x1 = w * 0.955, LX = [1 / 6, 0.5, 5 / 6].map(function (f) { return w * f; }), lr = Math.min(h * 0.38, 104), lw = lr * 0.36, span = x1 - x0;
      // the path, faint
      x.strokeStyle = 'rgba(163,181,242,0.16)'; x.lineWidth = 1; x.setLineDash([2, 7]); x.beginPath(); x.moveTo(x0, cy); x.lineTo(x1, cy); x.stroke(); x.setLineDash([]);
      // beam: brighter where more light survives
      var seg = [x0].concat(LX, [x1]), v = 1;
      x.globalCompositeOperation = 'lighter'; x.lineCap = 'round';
      for (i = 0; i < 4; i++) { if (i > 0) v *= cur[i - 1]; var bh = 3 + lr * 0.34 * v, bg = x.createLinearGradient(0, cy - bh, 0, cy + bh); bg.addColorStop(0, 'rgba(248,177,15,0)'); bg.addColorStop(0.5, 'rgba(255,214,140,' + (0.05 + 0.3 * v).toFixed(3) + ')'); bg.addColorStop(1, 'rgba(248,177,15,0)'); x.fillStyle = bg; x.fillRect(seg[i], cy - bh, seg[i + 1] - seg[i], bh * 2); x.strokeStyle = 'rgba(255,236,190,' + (0.1 + 0.75 * v).toFixed(3) + ')'; x.lineWidth = 1.4; x.beginPath(); x.moveTo(seg[i], cy); x.lineTo(seg[i + 1], cy); x.stroke(); }
      // the lights: each one must get through every lens
      var arrived = 0;
      for (i = 0; i < parts.length; i++) { var p = parts[i], u = REDUCE ? p.u : (p.u + t * 0.11 * p.s) % 1, px = x0 + span * u, stop = -1, k;
        for (k = 0; k < 3; k++) if (p.th[k] >= cur[k]) { stop = k; break; }
        var sv = 1; for (k = 0; k < 3; k++) if (px > LX[k]) sv *= cur[k];
        var py = cy + p.y * (10 + lr * 0.9 * (0.25 + 0.75 * sv)), al = 0.95;
        if (stop >= 0 && px > LX[stop]) { var d = px - LX[stop]; al = Math.max(0, 0.8 - d / (w * 0.07)); py += (p.y >= 0 ? 1 : -1) * d * 0.9; if (al <= 0) continue; x.fillStyle = 'rgba(' + COL[stop] + ',' + al.toFixed(3) + ')'; }
        else { if (stop < 0 && u > 0.9) arrived++; x.fillStyle = 'rgba(255,232,176,' + al + ')'; }
        x.beginPath(); x.arc(px, py, p.r, 0, 6.2832); x.fill(); }
      x.globalCompositeOperation = 'source-over';
      // lenses: a gauge ring that fills with the term
      for (i = 0; i < 3; i++) { var c = COL[i], val = cur[i];
        var g = x.createRadialGradient(LX[i], cy, 0, LX[i], cy, lr); g.addColorStop(0, 'rgba(' + c + ',' + (0.05 + 0.2 * val).toFixed(3) + ')'); g.addColorStop(1, 'rgba(' + c + ',0.02)');
        x.fillStyle = g; x.beginPath(); x.ellipse(LX[i], cy, lw, lr, 0, 0, 6.2832); x.fill();
        x.strokeStyle = 'rgba(' + c + ',0.28)'; x.lineWidth = 1.5; x.beginPath(); x.ellipse(LX[i], cy, lw, lr, 0, 0, 6.2832); x.stroke();
        x.strokeStyle = 'rgb(' + c + ')'; x.lineWidth = 4; x.lineCap = 'round'; x.shadowColor = 'rgba(' + c + ',0.9)'; x.shadowBlur = 12; x.beginPath(); x.ellipse(LX[i], cy, lw, lr, 0, -Math.PI / 2, -Math.PI / 2 + 6.2832 * Math.max(0.004, val)); x.stroke(); x.shadowBlur = 0;
        x.font = '700 ' + Math.round(Math.max(13, lr * 0.2)) + 'px "Sora", sans-serif'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillStyle = '#fff'; x.fillText(Math.round(val * 100), LX[i], cy - lr - 16);
        if (i < 2) { x.fillStyle = 'rgba(248,177,15,0.95)'; x.font = '700 22px "Sora", sans-serif'; x.fillText('×', (LX[i] + LX[i + 1]) / 2, cy - lr - 16); } }
      x.textBaseline = 'alphabetic'; x.font = '600 10.5px "JetBrains Mono", monospace'; x.fillStyle = 'rgba(190,200,234,0.9)'; x.textAlign = 'left'; x.fillText('THE QUESTION', x0 + 4, cy + lr + 4); x.textAlign = 'right'; x.fillText('THE ANSWER', w - 8, cy + lr + 4);
      // the answer
      var out = cur[0] * cur[1] * cur[2], ox = w * 0.955, orad = 9 + lr * 0.3 * out, gl = x.createRadialGradient(ox, cy, 0, ox, cy, orad * 3.4); gl.addColorStop(0, 'rgba(255,214,140,' + (0.12 + 0.78 * out).toFixed(3) + ')'); gl.addColorStop(1, 'rgba(248,177,15,0)'); x.fillStyle = gl; x.beginPath(); x.arc(ox, cy, orad * 3.4, 0, 6.2832); x.fill();
      x.fillStyle = 'rgba(246,241,230,' + (0.22 + 0.78 * out).toFixed(3) + ')'; x.beginPath(); x.arc(ox, cy, orad, 0, 6.2832); x.fill(); x.strokeStyle = 'rgba(226,174,69,0.95)'; x.lineWidth = 1.5; x.stroke();
      if (!REDUCE || moving) raf = requestAnimationFrame(draw); }
    function kick() { if (!raf) { prev = 0; raf = requestAnimationFrame(draw); } }
    ins.forEach(function (el) { el.addEventListener('input', read); });
    lab.querySelectorAll('.presets button').forEach(function (b) { b.addEventListener('click', function () { b.getAttribute('data-v').split(',').forEach(function (v, i) { ins[i].value = v; }); read(); }); });
    onScreen(lab, function (v) { visible = v; kick(); });
    read();
  })();

  /* ---------- 4 · five engines: change the question, tap an engine, the answer follows the dials ---------- */
  (function () {
    var q1 = document.getElementById('eg-q1'); if (!q1) return;
    var q2 = document.getElementById('eg-q2'), ans = document.getElementById('eg-ans'), ansr = document.getElementById('eg-ansr'), ansl = document.getElementById('eg-ansl'), glow = document.getElementById('eg-glowc'), cap = document.getElementById('eg-cap');
    var outs = [].slice.call(document.querySelectorAll('.eg-o')), btns = [].slice.call(document.querySelectorAll('.eg-controls button')), input = document.getElementById('eg-input'), base = cap ? cap.textContent : '';
    function setQ(text) { text = (text || '').trim() || 'Who should I call?'; var w = text.split(' '), a = '', b = ''; w.forEach(function (x) { if (!b && (a + ' ' + x).trim().length <= 14) a = (a + ' ' + x).trim(); else b = (b + ' ' + x).trim(); }); q1.textContent = '“' + a + (b ? '' : '”'); q2.textContent = b ? b + '”' : ''; }
    btns.forEach(function (b) { b.addEventListener('click', function () { btns.forEach(function (o) { o.classList.toggle('on', o === b); }); if (input) input.value = ''; setQ(b.getAttribute('data-q')); }); });
    if (input) input.addEventListener('input', function () { btns.forEach(function (o) { o.classList.remove('on'); }); setQ(input.value); });
    [].slice.call(document.querySelectorAll('.eg-tile')).forEach(function (g) { var show = function () { if (cap) cap.textContent = g.getAttribute('data-info'); }, hide = function () { if (cap) cap.textContent = base; };
      g.addEventListener('mouseenter', show); g.addEventListener('focus', show); g.addEventListener('click', show); g.addEventListener('mouseleave', hide); g.addEventListener('blur', hide); });
    document.addEventListener('rsm:relevance', function (e) { var p = e.detail, you = p >= 30, k = Math.max(0.12, Math.min(1, p / 60));
      ans.textContent = you ? 'You.' : 'Someone else.'; ans.setAttribute('font-size', you ? 23 : 19); ans.setAttribute('fill', you ? '#fff' : '#B9C4EA');
      ansr.setAttribute('stroke', you ? 'rgba(248,177,15,.8)' : 'rgba(150,170,255,.35)'); ansl.setAttribute('fill', you ? '#FFD98A' : '#8A97C4'); glow.setAttribute('opacity', you ? k : 0.05);
      outs.forEach(function (o) { o.setAttribute('opacity', k); }); });
  })();

  /* ---- the film: rolls muted when on screen, chapters jump, one button for sound ---- */
  (function () {
    var v = document.querySelector('video[data-roll]'); if (!v) return;
    var btn = document.getElementById('film-sound'), chaps = [].slice.call(document.querySelectorAll('.beats button'));
    var play = function () { var p = v.play(); if (p && p.catch) p.catch(function () {}); };
    if (!REDUCE && window.IntersectionObserver) new IntersectionObserver(function (es) { var on = es[0].isIntersecting && es[0].intersectionRatio > 0.45; if (on) play(); else if (!v.paused) v.pause(); }, { threshold: [0, 0.45, 0.8] }).observe(v);
    chaps.forEach(function (b) { b.addEventListener('click', function () { v.currentTime = parseFloat(b.getAttribute('data-t')) + 0.05; play(); }); });
    v.addEventListener('timeupdate', function () { var cur = 0; chaps.forEach(function (b, i) { if (v.currentTime >= parseFloat(b.getAttribute('data-t'))) cur = i; }); chaps.forEach(function (b, i) { b.classList.toggle('on', i === cur); }); });
    if (btn) { var sync = function () { var on = !v.muted; btn.setAttribute('aria-pressed', on ? 'true' : 'false'); btn.textContent = on ? 'Sound on' : 'Play with sound'; };
      btn.addEventListener('click', function () { if (v.muted) { v.muted = false; v.currentTime = 0; play(); } else v.muted = true; sync(); }); v.addEventListener('volumechange', sync); }
  })();
  /* ---- header menus: Escape closes, and a click outside closes the small-screen menu ---- */
  (function () {
    document.addEventListener('keydown', function (e) { if (e.key !== 'Escape') return; if (document.activeElement && document.activeElement.blur) document.activeElement.blur(); var m = document.querySelector('details.menu[open]'); if (m) m.open = false; });
    document.addEventListener('click', function (e) { var m = document.querySelector('details.menu[open]'); if (m && !m.contains(e.target)) m.open = false; });
  })();
})();
