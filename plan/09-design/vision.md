# Design plan v2: the instrument that converts

Step 9 of the roadmap. 23 Nov 2026. Replaces v1 of today. Built on Steps 1 to 8 as they stand tonight
(`07-messaging`, `08-blueprints/heroes.md`, `04-architecture/elements.md`) and on the goal Thomas set:
**show how extraordinary RSM is, hook the visitor, and turn pages into booked calls.**

## 1. What "extraordinary" is, and how a page shows it without saying it

RSM's advantage is not a claim. It is a set of things that exist and can be opened:

| The thing | How a page shows it | What the visitor feels |
|---|---|---|
| The D'Souza Equation | The formula, named after a real person, applied to the visitor's own trade | "There is a theory here, and it is about me" |
| The Standard, 413 checks, versioned and public | The live strip on every page; every service and element page links to its own checks by number | "They show their work" |
| 113,720 searches mapped; 113 elements; ~3,100 problems | The Console counts them for the visitor's trade and city; the Library lets them read any one | "They have already done the work for my trade" |
| The Index, the Board, the Log | Live panels with honest states | "This is real and it is moving" |
| One fact register, one author | The same sentence, name and dates everywhere; a corrections page | "Nothing here is made up" |
| Two commitments | Signed, on every page, above the fold on the commitments page | "They can lose if they are wrong" |

Rule: depth is shown by letting the visitor open it, never by adjectives. The messaging file bans the
hype words; the design bans the hype shapes (stock photos, stat counters that count up, fake chat
widgets, badge walls).

## 2. The conversion path, the same on every page

Messaging §7 says what the owner leaves the call with: who AI names for them, which searches they are
missing, whether their trade is open. The site gives a **taste of all three before the call**, so the
call is the obvious next step, not a leap.

```
Hook (their question, answered in two lines)
  → Taste (their trade and city: one real number from the map, one Index line, open or taken)
    → Proof (the equation, the Standard, the commitments, the record)
      → Call (Book a discovery call · 20 to 30 minutes with Thomas · the three things they get)
        → Lighter step (ask a question · check if open · see the 413 · get told when this changes)
```

Every page ends with the closing block from the blueprints. Every page has the **Taste** somewhere
above the first closing block: on mirror pages it is the whole page; on situation, service, guide and
element pages it is one panel, "For your trade and city", fed by the same data as the Console.

## 3. The Console: the hook on the home page and the taste on every other

A picker: **trade** (49) and **city** (50, the 10 launch cities first). Nothing else to fill in. On
submit, three panels fill, one per term of the equation, from data the plan already holds:

| Panel | Source | Shown now | Shown at launch |
|---|---|---|---|
| **Read** — "What your customers search" | Keyword universe v4, by trade and city | Count of mapped searches and the first three, by kind | Same, with the page for each kind |
| **Confirm** — "Who gets named" | AI Recommendation Index | "First run: plumbing, launch cities" until run | The month's names for that pair, and whether the visitor's business is among them (they type their name) |
| **Choose** — "Is your trade open" | Open Board | Open or taken, from the client map | Same, live |

Under the panels, one line and the button: *"This is the D'Souza Equation applied to you. The call
shows all 413."* The visitor has now seen RSM know their trade and city before anyone sold them anything.

The orbit animation is the Console's backdrop: the engines the console reads. It stays as built
(verified, lightweight, pauses off-screen). Nothing else on the site moves on its own.

The Console is a static-data build at Step 11: one JSON per trade-and-city pair generated from the
universe, the Index results and the Board, no server needed. Until the Index has run, the Confirm panel
says so in words. No number is ever invented.

## 4. The home page, section by section (follows the Home blueprint)

| # | Section | What it does for conversion |
|---|---|---|
| 0 | Live strip + header | Standard v1.0 and date · Open Log day · "Is your trade open?" · five menus · Ask · Book |
| 1 | **Hero = the Console** | H1 "The SEO company in the USA that makes you the answer". Subline: "Engines change. Your customer's question does not…". Trade and city picker. Trust line. Button + "Ask a question" |
| 2 | The two commitments | Two cards, signed. The risk is theirs, not yours |
| 3 | The equation | Formula, one line each for Read, Confirm, Choose, link |
| 4 | What's wrong? | The five doors, each with its ten-minute check |
| 5 | Look yourself up | Index, Board, Searches, Your Plan, with honest states |
| 6 | The record | 900+ businesses · about 400 projects, 90% successful · 100+ specialists · since 2010 |
| 7 | How it starts | Day 1 to 5, then the 15-day report and the Relevance Rate |
| 8 | Services by common name | Being found · being built. Plain links |
| 9 | Results by trade | Category-level, no names (from the findings bank when it exists; until then, the commitments stand in and the section is omitted, not faked) |
| 10 | Thomas | Photo, one paragraph, link. Real assets only |
| 11 | Closing block | The reason to book, the button, "Ask a question" |

Plus one section the blueprint does not list and this plan asks to add, after §3: **The machine
behind this site**, a six-cell record: 413 checks · 113 elements · 113,720 searches mapped · ~3,100
problems · every engine, open list · one fact register. Each cell links to the thing. This is the
"see how advanced we are" section, and it converts because every number is a door.

## 5. The design system

- **Two papers.** Navy `#0B1123` for the Console, the Studio and the closing block; warm ivory
  `#F6F1E6` (the logo disc) for everything the visitor reads. Gold `#F8B10F` only on the one live or
  signed thing per screen. Current cloud grey is retired.
- **Type.** Inter Tight 800 for headings; Inter for body at 17–19px; Instrument Serif italic for the
  owner's words and Thomas's; JetBrains Mono for data, the strip and labels only.
- **Panels.** Console panels are instrument-like: hairline borders, mono numbers, a state chip (live /
  first run / at launch). Library pages have no panels at all: text, tables, one diagram.
- **Motion.** Moves only when data moved or the reader acted. Page loads fade in once. The orbit is
  the single ambient exception.
- **Film.** One film per page where a film helps (see §6), muted autoplay never; a play button, a
  transcript under it, Thomas credited on the title card.
- **Speed.** No framework. Static pages, system fonts fallback, films served as MP4 with a poster.
  Core Web Vitals are checks in the Standard; the site must pass its own checks on launch day.

## 6. HeyGen Hyperframes: the films, and the rules

The HeyGen connector is attached to this account. Its `signal` preset is navy, cream and one antique
gold with serif, sans and mono: RSM's palette. Films are 60 to 90 seconds, composed from a brief,
rendered as MP4 in HeyGen's cloud, and billed to the HeyGen account.

| Film | Plays on | What it says in 75 seconds |
|---|---|---|
| **The D'Souza Equation** | Home §3, `/dsouza-equation/` | Engines change, the question does not; Read × Confirm × Choose; miss one and it is zero; why a new engine is one more reader |
| **Why is my business not showing up on Google?** | `/problems/not-showing-up-on-google/` | The three causes, the ten-minute check, what RSM does first |
| **Google shows me, AI doesn't** | `/problems/not-recommended-by-chatgpt/` | Why AI fails the Confirm test for most businesses |
| **How the Index is run** | `/ai-recommendation-index/` | The prompts, the engines, the cadence, what counts as named |
| **The first fifteen days** | `/dsouza-equation/method/`, `/your-plan/` | Day 1 to 5, the log, the 15-day report |
| 30-second cuts of each | LinkedIn, Shorts, Reels, the daily posting run | One idea each, the equation named, Thomas credited |

Rules: every film has a transcript on the page (Read) and Thomas's name on the title card (Confirm).
No avatar and no synthetic Thomas; his appearance is real footage or nothing (fact B7). The first film
is the equation; it is approved before the others are made, so one render proves the style.

The design canvas can be sent to Hyperframes directly, so the orbit plate becomes the opening of the
equation film without being redrawn.

## 7. How conversion is measured

From the business plan: booked calls per 100 visits, by source page. Each page's button carries its
page as the Calendly source. The Console logs trade-and-city submissions (no personal data) so the
most-asked pairs are known, and those pairs get their trade-in-city pages first.

## 8. Order of work

1. Rebuild the home page to §4 on the canvas, with the Console in its honest pre-launch state. Commit.
2. Compose the equation film in `signal`; embed it in home §3 with its transcript.
3. Build the five situation pages and one mirror page (the Board) as canvas boards, from the blueprints
   and heroes, so the page gate and the design meet before Step 10 writes 66 pages.
4. Step 11 wires the Console to the data.

## 9. Decisions asked of Thomas

1. Approve this plan as Step 9.
2. Approve composing the first film (uses HeyGen credits).
3. Confirm "The machine behind this site" may be added to the Home blueprint.
