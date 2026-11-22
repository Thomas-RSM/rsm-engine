# Roadmap: the RSM website, one step at a time

One step is finished and approved by Thomas before the next begins. Every step has one folder,
one deliverable and one definition of done. Nothing lives only in a chat.

Status words: **Not started** · **In progress** · **Awaiting approval** · **Done**.

| # | Step | What it settles | Deliverable | Done when | Status |
|---|---|---|---|---|---|
| 1 | Method | What RSM does that no one else does, stated so a stranger can follow and test it | `01-method/method.md` | Thomas approves the definition, the five parts and the name | **Awaiting approval** (draft v2) |
| 2 | Facts | Every company fact, with its source, identical everywhere | `02-facts/fact-register.md` | Thomas signs each fact; outside systems that disagree are listed for correction | Not started |
| 3 | Standard | The full check list and its public number | `03-standard/checks-v1.md` | Compared with the team's working checklist; number approved | In progress (413 drafted) |
| 4 | Architecture | The page list (36 to 50), URLs, menu, internal links | `04-architecture/site-map.md` | Every page has a purpose, a URL, a parent and a place in the menu | Not started |
| 5 | Keywords | Locked and woven keywords per page, with volumes | `05-keywords/keyword-map.csv` | Every page has its keywords, each with evidence; no keyword on two pages | In progress (v1, no volumes) |
| 6 | Proof | Findings, result statements, first Index run | `06-proof/` | 100 findings banked; result statements approved; Index run for the first trade | Not started |
| 7 | Messaging | Positioning, hooks, reasons to call, calls to action, voice | `07-messaging/messaging.md` | One approved hook, reason to call and call to action per page type | Not started |
| 8 | Blueprints | For each page type: section order, what goes where, hero specification | `08-blueprints/` | One blueprint per page type; hero written for every page | Not started |
| 9 | Design | Design system, header, heroes and page templates on the canvas | `09-design/` | Every blueprint has an approved design at phone, tablet and desktop width | Not started |
| 10 | Content | The pages, drafted one by one through the gate | `10-content/` | Each page passes every page check, the second review and Thomas's fact sign-off | Not started |
| 11 | Build | WordPress, the data engine, markup, tracking | `11-build/` | Staging site matches design and content; tracking verified | Not started |
| 12 | Launch | The whole standard run on RSM's own site, then publish | `12-launch/` | Every site and page check passes or is listed as not testable with its reason | Not started |

After launch the daily engine starts: one trade, one city, a day.

## Rules of the road

1. One step at a time. Work on a later step only where it cannot change (for example, checks already drafted).
2. Every decision goes in `decisions.md`, marked Fixed or Proposed, with the date.
3. Every deliverable is versioned: v1, v2. Old versions stay in git history, not in file names.
4. Every claim in a deliverable has evidence beside it or is marked "not verified".
5. Scripts that check a deliverable live in the same folder as the deliverable.

## Where things are

| Folder | Contents |
|---|---|
| `plan/` | This roadmap, the decisions log and one folder per step |
| `docs/` | Context brief, business plan, index of sessions and documents |
| `design/` | The home page canvas, logos and test scripts from the design session |
| `reference/` | The old site, kept for reference |
| `seo/keyword-universe/` | The 113,720-keyword universe and its builder |
