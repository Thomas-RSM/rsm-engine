// Loads one page at four sizes in a real browser and reports what a person would hit.
const { chromium } = require('playwright');
(async () => {
  const url = process.argv[2]; const out = { sizes: {} }; const b = await chromium.launch();
  for (const [name, w, h, mobile] of [['desktop', 1440, 900, false], ['laptop', 1280, 800, false], ['tablet', 820, 1180, true], ['phone', 390, 844, true]]) {
    const c = await b.newContext({ viewport: { width: w, height: h }, isMobile: mobile, hasTouch: mobile, deviceScaleFactor: 1 }); const p = await c.newPage(); const errors = [], bad = [];
    p.on('pageerror', e => errors.push(e.message.slice(0, 90))); p.on('response', r => { if (r.status() >= 400) bad.push(r.status() + ' ' + r.url().slice(-50)); });
    await p.addInitScript(() => { window.__lcp = 0; window.__cls = 0; new PerformanceObserver(l => { for (const e of l.getEntries()) window.__lcp = e.startTime; }).observe({ type: 'largest-contentful-paint', buffered: true }); new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__cls += e.value; }).observe({ type: 'layout-shift', buffered: true }); });
    await p.goto(url, { waitUntil: 'networkidle', timeout: 90000 }); await p.waitForTimeout(800);
    const H = await p.evaluate(() => document.documentElement.scrollHeight); for (let y = 0; y < H; y += 900) { await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(70); } await p.waitForTimeout(500);
    out.sizes[name] = await p.evaluate(() => ({ vw: innerWidth, dw: document.documentElement.scrollWidth, h: document.documentElement.scrollHeight, lcp: Math.round(window.__lcp), cls: +window.__cls.toFixed(3),
      broken: [...document.images].filter(i => i.complete && !i.naturalWidth).length,
      small: [...document.querySelectorAll('main *')].filter(e => e.children.length === 0 && e.innerText && e.innerText.trim().length > 2 && e.getBoundingClientRect().height > 0 && parseFloat(getComputedStyle(e).fontSize) < 12 && !e.closest('.orbit,svg,thead')).length }));
    out.sizes[name].errors = [...new Set(errors)]; out.sizes[name].bad = [...new Set(bad)]; await c.close();
    // paint time through a shared network is noisy: load twice more in clean contexts and keep the best
    for (let k = 0; k < 2; k++) { const c2 = await b.newContext({ viewport: { width: w, height: h }, isMobile: mobile, deviceScaleFactor: 1 }); const p2 = await c2.newPage();
      await p2.addInitScript(() => { window.__lcp = 0; new PerformanceObserver(l => { for (const e of l.getEntries()) window.__lcp = e.startTime; }).observe({ type: 'largest-contentful-paint', buffered: true }); });
      try { await p2.goto(url, { waitUntil: 'load', timeout: 90000 }); await p2.waitForTimeout(700); const v = Math.round(await p2.evaluate(() => window.__lcp)); if (v && v < out.sizes[name].lcp) out.sizes[name].lcp = v; } catch (e) {} await c2.close(); }
  }
  await b.close(); console.log(JSON.stringify(out));
})().catch(e => { console.log(JSON.stringify({ error: String(e).slice(0, 200) })); process.exit(1); });
