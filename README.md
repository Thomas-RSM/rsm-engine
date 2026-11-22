# RSM website and SEO

The working repository for Relevant Search Media's new website and the search programme behind it.
Everything a Claude session or a person needs to pick the work up is here or linked from here.

Start with **`docs/context-brief.md`**: the facts, decisions and plan in two pages. Then
`docs/sessions-and-links.md` for where everything else lives.

## Layout

| Folder | What is in it |
|---|---|
| `plan/` | **Start here for the website build.** `ROADMAP.md` (the steps and their status), `decisions.md` (every decision, Fixed or Proposed) and one folder per step |
| `docs/` | Context brief (facts and decisions), the business plan, and the index of sessions and documents |
| `design/canvas/project/` | The home page design as Claude Design canvas files. `Main.dc.html` is the page; `Origin.dc.html` is the hero in use; the other `.dc.html` files are earlier hero versions kept for reference; `canvas.json` is the board index |
| `design/canvas/support.js` | The canvas runtime, needed to open the `.dc.html` files in a browser |
| `design/assets/` | Logo files |
| `design/tools/` | Playwright scripts that test the hero and header (see its README) |
| `reference/old-site/` | The old relevantsearchmedia.com hero (HTML, JS, CSS, icons) and a screenshot, kept as the design reference |
| `seo/` | (to add) keyword plans, the 60-day calendar and the Problem Atlas from the keywords session |

## Company facts to use everywhere

- Relevant Search Media, founded 2020.
- Thomas D'Souza is the one named person; in digital marketing since 2010.
- 900+ businesses served. No prices on the site.

## Viewing the design locally

```bash
cd design/canvas/project
cp ../support.js .
npx http-server -p 8765 -c-1 .
```

Then open http://localhost:8765/Main.dc.html. The logo images are referenced from the published
artifact (`/_blob/...`), so they show only in the live canvas at
https://claude.ai/artifact/XRbUgXLXjPLA7j3e3LVCJN; locally, swap those paths for `design/assets/`.
