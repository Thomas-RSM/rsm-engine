# Off-site profile and posting system — site catalogue (draft v1)

Written 19 Nov 2026. This is the thinking behind the "make the accounts for our clients" system:
which sites, what each one is worth, how an account gets made there, who can reach it, and how
the engine should pick and grow the list per client. It is a draft for discussion, not a plan yet.

## 1. What this system is

For every RSM client (a US local business: plumber, HVAC, roofer, law firm, dentist, and so on)
RSM creates one real profile on each site that matters, in the business's own name, using an
email address made for that client, then hands the client the logins. RSM keeps posting to those
profiles as part of the daily "12 pieces off site".

Two rules that keep this from being read as spam (the business plan already names this risk):

1. **One real account per site per real business.** Real name, real address, real phone, real
   owner. Never a second alias, never a "network" of accounts RSM controls under made-up names.
2. **Native content on each profile.** The 12 off-site pieces are rewrites, not copies, and
   Reddit and Quora get full answers with links only where the community allows them.

What the links are worth, honestly:

- Facebook, Instagram, X, Reddit, Quora, Pinterest, Tumblr, Medium, YouTube, LinkedIn all mark
  outbound links `nofollow` or `ugc`. They pass little or no "link juice".
- Their value is different and still large: a consistent business entity across the web (name,
  address, phone, the same everywhere), presence in the sources AI engines cite most (Reddit,
  Quora, Yelp, BBB, Healthgrades, Avvo, YouTube), referral traffic, and a place to publish the
  daily pieces.
- The directories and vertical sites (Yelp, BBB, Angi, Avvo, Healthgrades, chamber sites,
  manufacturer dealer locators) are the ones that move local rankings. They are the "citations".
- Dofollow links come mostly from Blogger, WordPress.com, Weebly/Strikingly-style site builders,
  some directories, press release sites and guest posts, and from the RSM site's own pages.

So the system is really three things with one account layer underneath: **citations** (directories),
**presence** (social and Q&A), and **publishing** (blogs, video, documents, press).

## 2. The account layer: email, phone, password vault

**Email.** Best option is a mailbox on the client's own domain, for example `listings@clientdomain.com`,
made in whatever the client already uses (Google Workspace or Microsoft 365). Directories and
Google trust a domain email more, domain-ownership checks work, and handover is clean. If the client
has no domain mail, second choice is a free Zoho Mail mailbox on their domain; last choice a Gmail
(needs a phone and a real browser to create).

Proposal for verification codes: forward that mailbox to one RSM operations Gmail during setup.
This session has a Gmail connector, so Claude can read the verification emails itself and finish
signups without a person copying codes. Forwarding is switched off at handover.

**Phone.** This is the real gate. Almost every site that matters (Google, Facebook, Instagram, X,
LinkedIn, Reddit sometimes, Yelp, Nextdoor, Angi) wants a text code, and most reject VoIP numbers
(Google Voice, Twilio). Options:

- the client's own business phone, with the client relaying codes (slow, but the account is
  theirs from day one, and for Google Business Profile, Yelp and Angi it has to be the owner anyway);
- a small pool of real US SIM numbers at RSM used only for the signup step, then the number is
  changed to the client's at handover (fast, but some platforms flag a number reused across accounts).

Recommendation: client phone for the owner-verified sites (group C below); RSM SIM for the social
signups, swapped at handover. This is the one decision to settle first.

**Passwords.** A password manager with one shared collection per client (Bitwarden or 1Password),
not a spreadsheet. Handover is "we share the collection with you", and RSM keeps access while it
posts. Enable two-factor on every account with the authenticator held in the vault.

## 3. How far Claude can reach, by itself

| Reach | Meaning | What falls here |
|---|---|---|
| **A. Cloud, no help** | Signup needs only email verification; posting has an API or a plain form. Claude does it from this session. | WordPress.com, Tumblr, PRLog, openPR, Issuu, Scribd/SlideShare, About.me, Gravatar, Hotfrog, Brownbook, Cylex, Manta, niche forums, most small directories |
| **B. Chrome on your computer** | Signup needs a phone code, a CAPTCHA, or a residential IP and a real browser. You attach a computer, Claude drives Chrome, you (or a SIM) supply the code. Posting afterwards is often API-able from the cloud. | Google account (so Blogger, Sites, YouTube, Business Profile), Facebook and Instagram, X, LinkedIn, Reddit, Quora, Pinterest, Nextdoor, Bing Places, Apple Business Connect, Alignable |
| **C. The client themselves** | The site verifies the business owner: a postcard or video to the premises, a licence number, a background check, a bar or dental registration, or a fee. RSM prepares everything; the owner presses the button. | Google Business Profile, Yelp claim, BBB, Angi / HomeAdvisor, Thumbtack, Houzz Pro, state bar directories, ADA Find-a-Dentist, manufacturer dealer programmes (Carrier, Trane, Lennox, GAF, Owens Corning) |
| **D. Paid** | Works, costs money. | X API for posting, EIN Presswire / PRWeb, Yext or BrightLocal citation builder (which pushes to the data aggregators for about $2–3 per citation), sponsored Clutch / Angi leads |

Datacenter IPs are the reason group B exists: Google, Meta, X and Reddit treat signups from a cloud
IP as bots. Trying from here would get the account, and sometimes the whole client, flagged.

## 4. The core set: every client gets these (about 30)

Posting column: **API** = Claude can post from the cloud after the account exists; **form** =
Claude can post by driving the site; **manual** = a person posts.

### 4a. Citations and maps (the ones that move local rankings)

| Site | Why | Account | Posting | Link |
|---|---|---|---|---|
| Google Business Profile | The map box and the AI answer's first source. The single most important profile. | C (owner verification) | API needs Google approval; otherwise form | nofollow, but ranking signal |
| Bing Places | Bing, Copilot, DuckDuckGo maps; imports from GBP | B | form | nofollow |
| Apple Business Connect | Apple Maps, Siri | B (Apple ID) then C | form | nofollow |
| Yelp | Cited by ChatGPT and Perplexity for local; reviews | C (claim by phone) | form | nofollow |
| Better Business Bureau | Trust; AI engines cite it; accreditation is paid, the listing is free | C | manual | nofollow (dofollow for accredited in some cases) |
| Facebook Page | Citation, reviews, place in Meta search | B | API (Graph, after app review) or form | nofollow |
| Nextdoor Business | Neighbourhood recommendations, strong for home services | B (address check) | form | nofollow |
| Yellow Pages (yp.com) | Legacy citation aggregator | A/B | form | nofollow |
| Foursquare | Feeds Apple, Uber, many apps; a data source | A | form | nofollow |
| Data Axle, Neustar/Localeze, Foursquare (aggregators) | Feed hundreds of smaller directories | D (via Yext / BrightLocal / direct) | once | n/a |
| Chamber of Commerce (local) and ChamberofCommerce.com | Local trust; the local chamber's link is often dofollow | C (membership) / A | manual | often dofollow |
| Alignable | Local business network | B | form | nofollow |
| MapQuest, Superpages, Citysearch, Merchant Circle, Manta, Hotfrog, Brownbook, Cylex, eLocal, Local.com | Second-tier citations; consistency, not authority | A | form | mixed |

### 4b. Presence: social and Q&A

| Site | Why | Account | Posting | Link |
|---|---|---|---|---|
| LinkedIn (company page + owner profile) | B2B trust, author identity for the owner | B | API (Share on LinkedIn) for personal; company page needs Marketing API approval | nofollow |
| Instagram (business) | Visual proof of work; linked to the Facebook page | B | API (Content Publishing, via the Facebook page) | nofollow |
| X | Fast presence; low value for trades | B | API free tier allows posting; reading is paid | nofollow |
| Pinterest (business) | Long-lived visual search; good for roofing, dental, home | B | API v5 | nofollow |
| Reddit | The source ChatGPT and Google cite most. Value is in real answers in local and trade subreddits, not in links. New accounts need age and karma before anyone listens. | B (signup) | API for posting; moderators remove self-promotion | nofollow |
| Quora | Second most-cited Q&A; full answers only | B | manual (no posting API) | nofollow |
| YouTube | Second search engine; AI engines cite transcripts | B (Google account) | API | nofollow |
| TikTok (business) | Reach; weak for SEO | B | API (Content Posting, approval) | nofollow |
| Threads | Comes with Instagram | B | API | nofollow |

### 4c. Publishing: blogs, documents, video, press

| Site | Why | Account | Posting | Link |
|---|---|---|---|---|
| Blogger | Google-owned, indexes fast, links are dofollow | B (Google account) | API (Blogger v3) | dofollow |
| WordPress.com | Strongest free blog host; dofollow | A | API (REST) | dofollow |
| Google Sites | One-page "about" site under the Google account | B | manual (no content API) | dofollow |
| Tumblr | Easy, API, fast indexing | A | API | nofollow |
| Medium | Reach and AI citation; links nofollow; posting API closed, manual | A/B | manual | nofollow |
| Substack | Newsletter and archive; owner's voice | A | manual | nofollow |
| Weebly / Strikingly / Site123 (one of them) | A second dofollow host | A | form | dofollow |
| Issuu, Scribd (SlideShare), Calaméo, Yumpu | Documents: guides, checklists, price-range sheets | A | form / API (Issuu) | mixed |
| Vimeo, Dailymotion | Second and third video hosts for the same clips | A | API | nofollow |
| Spotify for Creators, Apple Podcasts | If the owner records audio | B | form | nofollow |
| PRLog, openPR, PR.com (free); EIN Presswire (paid) | Press releases for real news: new service, new area, award | A / D | form | dofollow on some |
| Qwoted, Featured.com, SourceBottle, Help a B2B Writer | Journalist requests (what HARO used to be); earns real editorial links | A | manual answers | dofollow |

## 5. Trade packs: added by niche

These are the vertical directories and communities where the client's customers actually look,
and where AI engines look for "best plumber in Houston". Most are group C (owner verifies).

**Home services (plumbing, HVAC, roofing, electrical, landscaping)**
Angi (Angi + HomeAdvisor), Thumbtack, Houzz, Porch, BuildZoom, Networx, Bark, HomeGuide,
Yelp (again, central here), Nextdoor, BBB, state licence board public lookup (make sure it is
correct), and the community sites: r/Plumbing, r/HVAC, r/Roofing, r/homeowners, r/HomeImprovement,
DIY Stack Exchange, ContractorTalk, HVAC-Talk, Terry Love plumbing forum.

- Plumbing: PHCC member directory, Plumbing-HVAC.com? (verify), Rheem / Navien / Moen Pro
  installer locators, Rooter? (verify).
- HVAC: ACCA directory, Carrier / Trane / Lennox / Daikin dealer locators (dealer status needed),
  NATE-certified technician listing, Energy Star partner.
- Roofing: GAF certified contractor, Owens Corning preferred contractor, CertainTeed, IKO, NRCA
  member directory, RoofingContractor? (verify).

**Law firms (personal injury and others)**
Avvo, Justia, FindLaw, Lawyers.com / Martindale, Nolo, Super Lawyers, LegalMatch, HG.org,
Lawyerland, the state bar's public directory, county bar association, Expertise.com, Best Lawyers
(invitation), Lawyer Legion; communities: r/legaladvice (answers only, strict rules), Avvo Q&A,
Justia Ask a Lawyer.

**Dental**
Healthgrades, Zocdoc, Vitals, WebMD Care, ADA Find-a-Dentist, Dentistry.com, Opencare,
1-800-Dentist, Smile Generation (if applicable), state dental board lookup, insurer provider
directories (Delta Dental, Cigna, Aetna), DentalTown (professional), r/askdentists (answers).

**Any B2B or agency client (and RSM itself)**
Clutch, GoodFirms, DesignRush, Crunchbase, G2 (software), UpCity, Expertise.com, Sortlist,
Agency Spotter, TrustRadius.

**Restaurants / retail / healthcare / real estate**: separate packs when the first client of that
kind arrives (TripAdvisor, OpenTable, Zomato; Healthgrades, Zocdoc, NPI registry; Zillow, Realtor.com).

## 6. City packs

Per launch city: the local chamber of commerce, the city or county business directory, the local
newspaper's business listings, Patch.com (local news with business profiles and posts), the
regional BBB, Nextdoor neighbourhoods, local subreddit (r/houston, r/nyc), local Facebook groups
(the owner's personal profile posts there), local trade associations (Houston PHCC chapter,
Texas Roofing Contractors Association), and the city's "Best of" awards sites.

## 7. How the engine stays intelligent: picking and growing the list

The catalogue above becomes **data**, one row per site, with these fields:

`site, url, category (citation / presence / publishing / vertical / local), trades[], cities[],
reach (A/B/C/D), signup_needs (email / phone / captcha / owner / licence / fee), posting_method
(api / form / manual), link_type (dofollow / nofollow / ugc / none), authority (DR or a rank),
ai_cited (how often ChatGPT, Gemini, Perplexity cite it for local queries, from the AI
Recommendation Index), cost, risk_notes, status (active / dead / changed), last_verified`.

For a new client the engine builds the list in four layers:

1. **Core set** (section 4): everyone.
2. **Trade pack + city pack** (sections 5 and 6): matched on `trades[]` and `cities[]`.
3. **Competitor gap** (the intelligent part): take the top five businesses in the client's trade
   and city from Google and from the AI Recommendation Index, pull their backlink and citation
   sources (Semrush backlinks research once API units exist; Ahrefs or a crawl otherwise), and
   suggest every domain that lists two or more of them but not the client. A person approves
   before anything is created.
4. **SERP discovery**: for "{trade} {city}" and "best {trade} in {city}", every non-business
   result in the top 30 that is a directory, list, forum or local news site is a candidate.
   Same for the AI engines' cited sources on those questions.

Growth after that: a monthly job re-runs layers 3 and 4 for every client and queues new
suggestions with the reason ("lists 4 of your 5 competitors", "cited by Perplexity for 'emergency
plumber Houston'"). The engine also marks what works: which profiles get indexed, which send
visits or calls (every lead records its source), which AI engines start citing the profile. Sites
that produce nothing after 90 days drop down the list for the next client of that trade.

Each client × site pair has a status: not started → email made → account made → verified →
profile complete (NAP, categories, hours, service area, description, logo, photos) → first post
→ handed over → live URL recorded → last checked. The "profile pack" (NAP in one agreed format,
50/150/500-word descriptions, logo in the four common sizes, 10 photos, categories, owner bio)
is made once per client and reused on every site, which is what makes 30 signups a day's work
rather than a week's.

## 8. Things to verify before this becomes a plan

- Whether the clients already have domain email (decides the email path).
- The phone decision (section 2).
- Which of the group B signups a US residential IP plus a real browser actually gets through today;
  Meta and Google change this often. One afternoon with a test business would tell us.
- X API free-tier posting limits and whether a trade client wants X at all.
- Whether to buy BrightLocal or Yext for the aggregators or submit to each by hand.
- Semrush has no API units at the moment, so layer 3 needs Ahrefs, a crawl, or units.
- Rows marked "(verify)" above are from memory and need checking.

## 9. Working files

- `sites.csv`: the complete list, one row per site, with signup link, group, who does it, what it
  needs, how posting works afterwards and the link type. This is the data file the engine grows.
- `client-intake-template.md`: what RSM collects from a client once, so every signup is a copy job.
