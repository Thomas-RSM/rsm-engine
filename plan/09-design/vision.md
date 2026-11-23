# Design vision: the site is the instrument, not the brochure

Step 9 of the roadmap. Draft v1, 23 Nov 2026, from the website session. For Thomas's approval before
the canvas is rebuilt a third time.

## 1. Who RSM is, read from everything built so far

Not an agency with a blog. A company that has built, in the open:

| What exists | Size | Where |
|---|---|---|
| A theory of search: the D'Souza Equation, Relevance = Read × Confirm × Choose | 1 equation, 3 terms, 5 parts | `plan/01-method` |
| A written, versioned standard | 413 checks, v1.0, dated | `plan/03-standard` |
| A map of every search a US local business can be found for | 113,720 keywords, 49 trades, 50 cities | `seo/keyword-universe` |
| An encyclopedia of every problem in the field | 1,822 entries drafted, ~3,100 planned | Problem Atlas |
| A monthly measurement no one else publishes | the AI Recommendation Index | Step 6 |
| A public ledger of its own work | the Open Log | at launch |
| A scarcity rule made visible | the Open Board, one business per trade per city | at launch |
| A network of agents that research, write, fact-check, gate, design and build | run from `plan/` | Step 10 |
| One signed fact register every page is built from | 60 facts | `plan/02-facts` |

That is an **instrument**: it reads a business, confirms it and measures whether it is chosen, for every
engine, every day. The current home page describes the instrument. The new site should **be** it.

## 2. The idea in one line

> Type your trade and your city. The site reads your business, confirms it and shows who gets chosen —
> live, on every engine — and then shows you the plan.

Every visitor's first act is to look themselves up. Nothing on the site is about RSM until the owner
has seen their own situation. That is the user-centric centre the page has been missing.

## 3. Three surfaces, one site

| Surface | What it is | Feel | Pages |
|---|---|---|---|
| **The Console** | The live part: Ask, the Index, the Open Board, the Open Log, Searches, Your Plan. Data about the reader's trade and city. | Deep navy, instrument light, numbers that move only because data moved | Mirror pages, home hero |
| **The Library** | The knowledge: the five situations, the equation pages, the guides, the encyclopedia. | Warm ivory paper, editorial type, long reading, no decoration | Situation, Equation, Guide, Problem pages |
| **The Studio** | Thomas: the origin, the biography, recorded sessions, the commitments. | Real photographs and film, his voice, his signature | Identity pages |

The orbit animation stays, but moves from "the hero" to the **backdrop of the Console**: the engines
are what the console reads. The yantra idea stays private, as the plan says.

## 4. The home page, section by section

1. **Console hero.** One line: "Who gets named when your customer asks?" Two fields: *your trade*,
   *your city* (autocomplete from the 49 trades and 50 cities). On submit the three gauges fill in
   front of the orbit backdrop:
   - **Read** — how many of the searches in the map for that trade and city exist (from the universe), and
     the first three.
   - **Confirm** — what the public listings for that trade in that city agree on (from the Index run
     where it exists; otherwise "first run: plumbing, launch cities").
   - **Choose** — who ChatGPT, Gemini and Perplexity named this month (the Index), and whether the
     trade is **open or taken** in that city (the Board).
   Below the gauges: "This is the D'Souza Equation applied to you. Book a discovery call to see the
   full 413." Until the data exists for a pair, the gauge says so plainly; nothing is invented.
2. **What's wrong?** The five situations, in the owner's words, each with its ten-minute first check.
   (Already built; keep.)
3. **The equation, as a 75-second film.** The Hyperframes video embedded: engines change, the question
   does not; Read × Confirm × Choose; why a new engine is one more reader. Thomas's voice if he records
   it; otherwise a narrator and his name on the title card.
4. **The machine behind this site.** A plain table of what RSM has built: 113,720 searches mapped, 413
   checks, the Index, the Log, the encyclopedia, the agent network, one fact register. Stated as a
   record, not as a boast. This is the "see how advanced we are" section the owner has asked for, and
   it works because every number links to the thing itself.
5. **The Open Log, live.** Today's entries from RSM's own site: published, searches gained, AI
   mentions, calls booked. Small numbers at first, shown anyway.
6. **The method and the two commitments.** (Already built; keep.)
7. **Thomas.** Photo, film, the 50-word biography, the signature. Nothing until the real assets arrive.
8. **Services by common name, FAQ, final call.** (Already built; keep.)

## 5. Design language

- **Two papers.** Navy (`#0B1123`) for the Console and the Studio; ivory (`#F6F1E6`, the colour of the
  logo disc) for the Library. The current cloud-grey pages become warm paper. Gold is used only for
  the one thing on a screen that is live or signed.
- **Type.** Inter Tight for headlines, Inter for reading, Instrument Serif italic for the owner's own
  words and Thomas's, JetBrains Mono only for data and labels. No decorative capitals outside the
  Console.
- **Motion rule.** Something moves only when data moved or the reader asked. The orbit backdrop is the
  one ambient exception.
- **Honesty rule.** Every live panel has a state: live, first run, starts at launch. No placeholder
  numbers, ever.
- **Voice.** Short sentences, the owner's words quoted back, Thomas's verdict in first person where he
  has given it.

## 6. Where Hyperframes fits

HeyGen's Hyperframes composes programmable HTML video from a brief, in a house style; its `signal`
preset (editorial navy, cream, one antique-gold accent, serif + sans + mono) is already RSM's palette.
Proposed films, each 60–90 seconds, each with a transcript on the page (for Read) and Thomas credited
(for Confirm):

| Film | Where it plays | Brief |
|---|---|---|
| The D'Souza Equation | Home §3, `/dsouza-equation/` | The idea, the three terms, why it does not go stale |
| One situation each (5) | The five situation pages | The owner's sentence, the first check, how RSM solves it |
| How the Index is run | `/ai-recommendation-index/` | The prompts, the engines, the monthly cadence, what counts |
| The first fifteen days | `/dsouza-equation/method/` | Day 1 to 5, then the log |
| 30-second cuts | LinkedIn, Shorts, Reels | From each of the above, for the daily posting run |

The Claude Design canvas can be sent to Hyperframes directly (its "Send to" button), so the orbit
plate can become the opening of the equation film without being redrawn.

What Hyperframes must not do: stand in for Thomas. No avatar, no synthetic Thomas. His appearance is
real footage or nothing (fact B7).

## 7. What this costs and needs

- The Console hero needs the keyword universe and the Index as data behind the page: a small API or
  static JSON per trade and city at build time (Step 11).
- The films are rendered in HeyGen's cloud and billed to the HeyGen account; the first one proves the
  style before the rest are made.
- Thomas's photo, film and voice remain the one thing no system here can supply.

## 8. Decision asked of Thomas

1. Approve the idea: the Console hero, the three surfaces, the two papers.
2. Approve making the first film, the equation, in the `signal` style.
3. Say whether the orbit animation stays as the Console backdrop or goes.
