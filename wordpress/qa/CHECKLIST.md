# The page gate

No page is called finished until `gate.py` prints `GATE PASS` for it on the live site. It checks the page three ways.

## 1. The D'Souza Standard (413 checks)
`site/tools/check_page.py`, run on the page exactly as the live server sends it. Every check ends PASS, FAIL or N/T.
N/T means "cannot be judged from the page alone": it needs Search Console data, a second human reviewer, an outside
profile, or time to pass (for example the day-seven indexing check). A page passes with **0 FAIL**. N/T items are
listed in the page's report so they can be closed when the data exists; they are never counted as passes.

## 2. Extra gates (measured on the live page)
| Gate | Rule |
|---|---|
| Lead keyword | present in copy, in the title, in the one H1 |
| Keyword density | lead keyword at or under 2% of the copy; no single content word over 3% |
| Cannibalisation | no other page has the same lead keyword |
| Duplication | title and description unique site-wide; under 12% of 8-word runs shared with any other page |
| Title / description | 30 to 60 characters / 110 to 160 characters |
| Canonical, indexing | canonical points to itself; page is indexable |
| Copy | at least 300 words and inside the range for its page type |
| Images | every image under 200 KB, with alt text, width and height; none missing |
| Weight and speed | HTML under 250 KB; cached response under 0.8 s |
| Links | no broken internal link (links to pages still on the build list are reported, not failed) |

## 3. Browser run at four sizes (desktop 1440, laptop 1280, tablet 820, phone 390)
No sideways scroll · no script errors · no failed files · no broken images · layout shift under 0.1 ·
largest paint under 2.5 s on desktop and phone · no copy under 12px on the phone.

## Order of work
One page at a time. Build → publish → run the gate → fix → run again → record in `pages.json` and the keyword map.
The next page starts only after the current one prints `GATE PASS`.

## Honest limits
- Paint times are measured from a test machine, not from real visitors. Real-user Core Web Vitals come from Search Console after launch.
- Keyword density is a ceiling, not a target. Repeating a phrase to reach a percentage reads badly and is not a ranking factor.
- Checks that need a person (a second reviewer's sign-off, the owner's approval) stay N/T until that person signs.
