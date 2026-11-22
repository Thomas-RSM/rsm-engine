# Optimization and verification plan for the 36 foundation pages

Written 22 Nov 2026. Companion to `decisions.md` and `seo/foundation/keyword-map-v1.csv`.
Status: **proposed**, for Thomas's approval. Nothing here has been applied to a page yet.

## 1. What was checked to write this, and what could not be

| Source | Read | Result |
|---|---|---|
| Keyword universe (both workbooks, live file of 18 Nov) | Yes | Used for candidates |
| Google autocomplete, live, 22 Nov 2026 | Yes, 177 keywords tested by script | Raw answers saved in `seo/foundation/evidence/` |
| Skills: god-mode-seo, god-content-agent, rsm-audit, rsm-strategy | Yes, in full | Rules carried into section 4 |
| "Relevant Search Media — Deliverables" document, audit section | Yes | The 313 points as 18 groups with counts |
| `rsm-auditor-brain` repository | Yes, the audit and offer files | 16 family names, firm facts |
| **RSM canon** (`Thomas-RSM/rsm-canon`) | **No. Not reachable from this session** | Vocabulary rules, never-do list and the QA tool were not loaded |
| `rsm-standards` skill | **No. Not installed in this session** | Referenced by rsm-audit and rsm-strategy |
| Search volumes | **No.** Semrush has no API units | Demand is graded by live autocomplete only |

Limits of the live check: autocomplete proves a search exists. It does not give volume or difficulty.
Some answers showed non-US results, so the checking machine may not be seen as a US user. Every keyword
must be re-checked with volumes before a page is published.

## 2. Keyword map

File: `seo/foundation/keyword-map-v1.csv`. One main keyword and at most two supporting per page.
90 keywords on 33 pages; 3 pages have no search target by design (Ask, Open Board, Book 20 minutes).

Evidence grades: **A** Google suggests it or knows it as a query (82). **B** weak signal (6).
**D** no live signal (2: the new method term, and Thomas's name, both expected).

Scripted checks passed: no keyword on two pages, no page over 1+2, every keyword has a live check on file.

Changes the checks forced on the earlier page list:
- Cost and time were two intents on one page. Cost moves to the situation page "I'm being quoted", time stays as its own Standard page.
- Six planned main keywords had no live demand and were replaced by proven forms (pages 5, 9, 16, 19, 20, 22).
- No comparison search such as "ecommerce seo vs local seo" exists yet. Page 20 targets ecommerce terms.
- Open Board has no existing search to target. It is reached through internal links only.

Existing terms still without a page in the 36: web design, link building, content marketing,
reputation management. They need a decision: swap into the 36, or first pages of the next wave.

## 3. The 313 points: what exists and what is proposed

What exists today, from the Deliverables document:

| Group | Checks | Group | Checks |
|---|---|---|---|
| Technical health | 36 | AI readiness | 24 |
| Speed and stability | 24 | Local signals | 26 |
| Mobile experience | 14 | Google Business Profile | 22 |
| Security | 10 | Reviews and reputation | 10 |
| Site structure | 18 | Conversion elements | 22 |
| Page titles and descriptions | 14 | Tracking and measurement | 12 |
| Headings and copy | 20 | Content inventory | 8 |
| Images and media | 12 | Off-site presence | 12 |
| Verified facts (schema) | 20 | Social presence | 9 |
| | | **Total** | **313** |

Three findings:
1. **The 313 checks are not written out one by one** in anything this session could read. Only the group names and counts exist. A page cannot be checked against a count.
2. **The same document describes the audit two ways**: 16 families in the summary and the auditor app, 18 groups in the catalogue. The names do not match.
3. The 313 audit a client's site. They do not cover what makes a page unique or true, which is where earlier errors came from.

Proposed upgrade, in this order:
1. Write out every one of the 313 checks as a single numbered list: what is checked, how it is measured, pass or fail. Settle 16 versus 18 groups.
2. Add the families the current audit lacks:
   - **Uniqueness**: overlap against every other page, one client-only fact, one finding, local facts on local pages.
   - **Fact integrity**: every number and claim traced to the fact register; company facts identical everywhere.
   - **AI answer verification**: the page's question asked in each named AI engine, answer and citation recorded with date.
   - **Author and entity**: named author, biography, consistent profiles, definition sentence of the method.
   - **Term policy**: existing term in title, heading and answer; method term in its fixed place.
   - **Freshness and corrections**: review date, dated prediction, correction record.
3. The new total is whatever the written list counts to. No new number is announced before the list exists.
4. Changing "313" touches the auditor app, the mailer, the proposal, the Deliverables document and the canon. They change together in one sweep, or the public number stays 313 for the client audit and the larger list is named separately for RSM's own pages.

## 4. How each page is optimized

Every page is built to one specification, and each line is a check with a pass or fail result.

| Element | Rule |
|---|---|
| Main keyword | In the title, URL, H1, first 100 words and one H2. Then natural variants. No density target. |
| Supporting keywords | One H2 or FAQ question each, plus body mentions. Same intent as the main keyword. |
| Title | 30 to 60 characters, keyword first, brand last. |
| Meta description | 110 to 155 characters, a complete sentence that leads with the answer. |
| URL | Lowercase, hyphenated, five words or fewer, from the main keyword. |
| Answer block | The question as the heading, the answer in 40 to 60 words directly under it. Complete without the method's name. |
| Five blocks | Answer, Explain, Check yourself, How RSM solves it, Next step. In that order. |
| Headings | One H1. H2s are the reader's next questions. No skipped levels. |
| Unique core | Five slots filled: Index data, one finding, local or trade facts, Thomas's stance, live record. |
| Verdict | One of three outcomes stated plainly. |
| FAQ | 5 to 8 questions, answers of 40 to 60 words, never reused on another page, schema identical to the visible text. |
| Schema | Organization, WebSite, Breadcrumb, Article or Service, FAQPage, Person for the author. Built only from the fact register. |
| Images | Real images, descriptive alt text, keyword file names, compressed. |
| Internal links | 3 to 5 contextual links, link text is the target's keyword, at least one inbound link from a live page. |
| Outbound links | 1 to 2 authoritative sources, each named in the text. |
| Author and dates | Thomas named, biography linked, published and reviewed dates shown. |
| Method term | In the "How RSM solves it" block only, full name first, linked to its definition. |
| Technical | Self-canonical, indexable, Core Web Vitals in the green, mobile checked at three widths. |

## 5. How errors are prevented

The rules in the skills were written after earlier mistakes. They show the same pattern each time:
a check done by eye, or a fact taken from memory. So the rule here is that nothing is checked by eye
alone and nothing is taken from memory.

1. **Fact register first.** One file holds every company fact with its source. Copy can only use facts from it. Today the facts disagree across systems: see section 6.
2. **Scripted gate on every page.** Lengths, single H1, keyword placement, keyword uniqueness across pages, leftover placeholders, banned phrases, numbers traced to the register, FAQ schema against visible text, schema parses, links resolve, overlap against every other page.
3. **A second, independent reviewer** reads each page as the owner and as the developer, with no knowledge of the author's reasoning.
4. **Thomas signs off the facts.** Each page ships with a sheet mapping every factual sentence to its source.
5. **Three outcomes only** for any check: pass, fail, or not testable with the reason. An untested item is never reported as passing.
6. **A failing page is not published.** The standard does not bend to the calendar.
7. **After publish:** live page re-fetched and re-checked, indexing confirmed, result logged.

Known error classes carried from the skills: broken sentence templates, placeholders left in live copy,
cut-off meta descriptions, planned URL used where the live URL differed, keyword stuffing, near-duplicate
sibling pages, invented numbers, wrong article before a vowel, lowercase acronyms, agencies listed as
neighbourhoods, state rules on the wrong state's page.

## 6. Conflicts found that must be settled before any copy is written

| # | Conflict | Where |
|---|---|---|
| 1 | Founding year. Thomas confirmed **2020**. The auditor's offer file, read on every audit and every email, says **2006**. The skills' fallback text says 2006. | `rsm-auditor-brain/backend/offering_default.json`, ai-search-audit-email skill |
| 2 | City. Site plan says New Delhi. The Manifest says Gurugram. Google suggests "relevant search media noida". | Public profiles |
| 3 | Vocabulary. The content skill says RSM's own website copy must not use "SEO", "digital marketing", "keywords", "AEO". The keyword plan and this map target exactly those terms. | god-content-agent skill, canon |
| 4 | Plans. The offer file says two plans, Partnership removed from client copy. The business plan lists three. No prices on the site either way. | Offer file, business plan |
| 5 | Booking. Offer file says "Book 30 minutes". The site plan says "Book 20 minutes". | Offer file, business plan |
| 6 | Audit structure: 16 families or 18 groups. | Deliverables document |
| 7 | Keywords per page. The strategy skill defaults to 3 primary, 3 secondary, 3 related. The RSM site decision is 1 main and at most 2 supporting. This map follows the RSM decision. | god-mode-seo skill |

## 7. Order of work from here

1. Thomas settles the seven conflicts and the open questions in `decisions.md`.
2. Canon and rsm-standards made readable to this session.
3. Fact register written and signed.
4. The 313 checks written out; additions agreed; number decided.
5. Volumes added to the keyword map; map locked.
6. Page gate script built and tested on one page.
7. First page drafted, gated, reviewed, signed. Then the rest, in the order set in `decisions.md`.
