# The page gate (v1.0)

How a page is built and checked before it goes live. Replaces the plan of 22 Nov, kept in `archive/`.

## What a page is built from

| Input | File |
|---|---|
| Facts | `02-facts/fact-register.md` |
| Its address, parent and menu place | `04-architecture/site-map.md` |
| Its three locked keywords, section keywords and questions | `05-keywords/keyword-map-v2.csv`, `woven-keywords-v2.csv` |
| The message, the hook and the calls to action | `07-messaging/messaging.md` |
| Its order of sections | `08-blueprints/blueprints.md` |
| Its title, heading and subline | `08-blueprints/heroes.csv` |

## What every page must have

| Element | Rule |
|---|---|
| Lead keyword | In the title, address, H1, first 100 words and one H2. Then natural variants. No density target |
| Same-intent keywords | One heading or FAQ question each, plus the body |
| Title | 60 characters or fewer, unique |
| Meta description | 110 to 155 characters, complete sentences, leads with the answer |
| Answer block | The question as the heading, the answer in 40 to 60 words under it, complete on its own |
| Five blocks | Answer, Explain, Check yourself, How RSM solves it, Next step |
| The equation | Named in full on first mention, in the "How RSM solves it" block, linked to its page |
| FAQ | Five to eight real questions from the woven list, 40 to 60 words each, never reused on another page |
| Markup | Organization, WebSite, Breadcrumb, Article or Service, FAQPage, Person. Built only from the fact register |
| Links | Three to five contextual internal links; link text is the target's keyword |
| Author and dates | Thomas D'Souza, published and last-reviewed dates |
| One primary button | Book a discovery call |

## The checks

Every page passes the 193 page-level checks of the D'Souza Standard that apply to it. Each ends as
pass, fail or not testable with the reason. An untested item is never reported as passing.

## How errors are prevented

1. Facts come only from the fact register.
2. A script checks what a script can: lengths, single H1, keyword placement, keyword uniqueness across pages, leftover placeholders, banned phrases, FAQ markup against visible text, markup that parses, links that resolve, overlap against every other page.
3. A second, independent reviewer reads each page as the owner would.
4. A page that fails is not published.
5. After publishing, the live page is fetched and checked again.

Nothing invented is published: no written-up reviews, clients, quotes or results.
