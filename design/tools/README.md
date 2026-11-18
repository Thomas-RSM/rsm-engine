# Design tools

Playwright scripts used to check the home page and the hero animation. They expect a local
server at http://localhost:8765 serving `design/canvas/project/` (copy `support.js` beside the
`.dc.html` files, and rewrite the Google Fonts link to a local stylesheet if you are offline).

| Script | What it checks |
|---|---|
| `verify.js <outdir>` | Hero at 8 widths: console errors, failed requests, icons loaded, motion never stalls, no tile/label overlap, nothing clipped, hover works |
| `perf.js <file> <secs> <w> <h>` | Frame rate, slow frames, script time, main-thread load, DOM writes, memory over a timed run |
| `pause.js` | Animation stops when scrolled away and resumes on return |
| `nav.js`, `nav2.js` | Header menus open, stay open, don't spill; phone drawer opens/closes |
| `ovl.py '<json config>'` | Pure-maths overlap search for the hero's orbit spacing (no browser) |
| `shot2.js`, `shot3.js`, `sec.js`, `full.js`, `mob.js` | Screenshots: single, software-GL, per-section, full page, phone strips |
| `test_orbit.js` | Older solar-system hero: click/sync test |

Run with the Playwright that ships with Chromium: `node design/tools/verify.js ./out`.
