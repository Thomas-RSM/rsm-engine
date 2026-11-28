# Work log: building the site page by page

Updated 28 Nov 2026. Read this first when picking the work up.

## Where things stand
- Live site: https://relevantsearchmedia.com (WordPress, Elementor Free, theme `rsm-theme`, plugin `rsm-elements`).
- 20 of 67 planned pages are live and pass the gate: home; `/problems/` and its five pages; `/ask/`; `/book/`;
  `/dsouza-equation/` with read, confirm, choose, standard, method, engines, law-of-search, how-search-works,
  seo-vs-aeo-vs-geo; `/elements/`.
- Next, in order: Services (24 service pages, then the `/services/` hub), Guides (5 + hub), Mirrors
  (ai-recommendation-index, open-board, open-log, searches, your-plan), `/industries/` and `/cities/` hubs,
  Identity (about, thomas-dsouza, commitments, results, editorial-policy, corrections, contact), privacy, terms.
  After those: the 113 element pages listed in `plan/04-architecture/elements.csv`.

## Source of truth
`plan/` (brought in from branch `claude/wizardly-bell-fs4zov`). For each page use:
`04-architecture/site-map.csv` (address, parent), `05-keywords/keyword-map-v2.csv` (lead and same-intent keywords),
`05-keywords/woven-keywords-v2.csv` (section keywords and the FAQ questions to use), `08-blueprints/heroes.csv`
(title, H1, subline), `08-blueprints/blueprints.md` (order of sections), `07-messaging/messaging.md`,
`02-facts/fact-register.md` (the only facts allowed), `02-facts/engine-register.md`.

## How a page is made
1. Add a spec to `wordpress/pages.py` (helpers: hero, sec, steps, terms, table, faq, trust, closing) and a row to `GATE`.
2. `python3 -I build.py` then `bash qa/deploy.sh <page-key>` (add `theme` or `plugin` if their files changed).
3. `./qa/run.sh /the/path/` until it prints `GATE PASS`. `bash qa/all.sh` re-checks every live page after a shared change.
4. `python3 -I qa/records.py`, commit, push.

## Rules the gate enforces that are easy to trip over
- Title and H1 come from `heroes.csv`. Title 60 characters or fewer. H1 must carry the lead keyword (singular/plural both count).
- Description: 110 to 155 characters, at least two sentences ending in a full stop, containing the lead keyword.
- The hero answer: 40 to 60 words (90 ceiling), at most three sentences, lead keyword in the first 100 words.
- At least five H2s that end with a question mark; one H2 must contain the lead keyword.
- Each same-intent keyword appears word for word in an H2 or FAQ question.
- Every paragraph is three sentences or fewer. FAQ answers are 40 to 60 words; split them with `\n`.
- No "best", "leading", "#1", "top-rated" in our own prose (allowed inside a question heading).
- A link to `/book/` must read exactly "Book a discovery call". Each section needs one onward link.
- The page needs a table, numbered steps ("Step 1" / "Check 1" / "Day 1"), one concrete example (the `example` string
  in `GATE`) and a dated figure of our own (`original`).
- Lead keyword density at or under 2%; under 12% of wording shared with any other page (the trust block is exempt).
- Step-card titles must not end with "?" (they would be counted as unanswered FAQ questions).

## Facts and quotes
- Nothing invented. Only Thomas's signed line may be quoted; it sits in the trust block. No client names, no prices.
- Do not call the discovery call "free" and do not promise a reply time: the register says neither.
- The engine list is never given as a fixed public count.
- Only "Thomas D'Souza, Founder" is named publicly (owner's instruction in this project).

## Site-wide behaviour worth knowing
- One sitemap at `/sitemap.xml` (core sitemaps off), one JSON-LD block per page, `llms.txt` rebuilt from published pages.
- LiteSpeed Cache combines and minifies CSS and defers JS. `deploy.sh` warms every page after each deploy.
- Enquiry form posts to `/wp-json/rsm/v1/lead`; enquiries appear under "Enquiries" in wp-admin and are emailed to the admin address.
- The Calendly link from the register is on `/book/`.

## Open items for the owner
- Fact register says the site address is `www.`; the live site answers without `www`. Decide and redirect one to the other.
- Engine names should be checked at source before launch (register note).
- FAQ questions on the first twelve inner pages were written before the plan was found; align them to the woven list.
- Paint times are measured from a test machine. Real-visitor Core Web Vitals need Search Console.
