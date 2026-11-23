# The D'Souza Standard

Version 1.0, 23 Nov 2026. **413 checks in 27 groups.** The list is open: checks are added as search changes, and each addition gets a version and a date.

The standard is the D'Souza Equation written out as checks: **Relevance = Read × Confirm × Choose**, for every question in the customer's search map.

| Part of the equation | What it asks | Checks |
|---|---|---|
| The question | Is every search a customer makes mapped and assigned to a page? | 14 |
| Read | Can every engine read plainly what the business is and what it answers? | 250 |
| Confirm | Do independent sources say the same thing? | 99 |
| Choose | Do real people, and the engines, choose it? | 50 |
| **Total** | | **413** |

RSM's free report runs about 30 of these. Every client's audit runs all of them.

Checks 1 to 313 follow the group names and counts of the audit described in "Relevant Search Media — Deliverables". Their wording was written out on 22 Nov 2026. Checks 314 onward were added on that date.

Scope: **Page** is checked on every page. **Site** is checked once for the whole site. **Beyond** is checked off the site.
Every check ends as pass, fail or not testable with the reason.

| Group | Equation | Checks | Numbers |
|---|---|---|---|
| Technical health | Read | 36 | 1 to 36 |
| Speed and stability | Read | 24 | 37 to 60 |
| Mobile experience | Read | 14 | 61 to 74 |
| Security | Read | 10 | 75 to 84 |
| Site structure | Read | 18 | 85 to 102 |
| Page titles and descriptions | Read | 14 | 103 to 116 |
| Headings and copy | Read | 20 | 117 to 136 |
| Images and media | Read | 12 | 137 to 148 |
| Verified facts | Read | 20 | 149 to 168 |
| AI readiness | Read | 24 | 169 to 192 |
| Local signals | Confirm | 26 | 193 to 218 |
| Google Business Profile | Confirm | 22 | 219 to 240 |
| Reviews and reputation | Confirm | 10 | 241 to 250 |
| Conversion elements | Choose | 22 | 251 to 272 |
| Tracking and measurement | Choose | 12 | 273 to 284 |
| Content inventory | Read | 8 | 285 to 292 |
| Off-site presence | Confirm | 12 | 293 to 304 |
| Social presence | Confirm | 9 | 305 to 313 |
| Search map coverage | Question | 14 | 314 to 327 |
| Uniqueness and information gain | Read | 12 | 328 to 339 |
| Fact integrity | Read | 10 | 340 to 349 |
| Author and entity | Confirm | 12 | 350 to 361 |
| AI answer verification | Choose | 16 | 362 to 377 |
| Accessibility | Read | 12 | 378 to 389 |
| Video and visual search | Confirm | 8 | 390 to 397 |
| Freshness and corrections | Read | 8 | 398 to 405 |
| Publishing readiness | Read | 8 | 406 to 413 |
| **Total** | | **413** | |

## 1. Technical health (36) · Read

Can Google reach and read every page: indexing, sitemaps, redirects, errors, duplicate pages.

| # | Scope | Check |
|---|---|---|
| 1 | Site | robots.txt exists, returns status 200 and blocks no page that is meant to rank |
| 2 | Site | robots.txt names the location of the XML sitemap |
| 3 | Site | An XML sitemap exists, is valid and returns status 200 |
| 4 | Site | The sitemap lists every indexable page and nothing else |
| 5 | Site | The sitemap contains no redirected, broken, noindexed or canonicalised-away URLs |
| 6 | Site | Sitemap last-modified dates are real and change only when the page changes |
| 7 | Site | The sitemap is submitted in Google Search Console and read without errors |
| 8 | Site | The sitemap is submitted in Bing Webmaster Tools and read without errors |
| 9 | Page | The page returns status 200 |
| 10 | Page | The page is indexable: no noindex in the meta robots tag or the X-Robots-Tag header |
| 11 | Page | The page has exactly one canonical tag and it points to itself |
| 12 | Page | The canonical URL is absolute, returns status 200 and is itself indexable |
| 13 | Page | The page is indexed in Google, confirmed by URL inspection in Search Console |
| 14 | Page | The page is indexed in Bing, confirmed in Bing Webmaster Tools |
| 15 | Site | Only one host version is live: http, https, www and non-www all reach it in a single 301 |
| 16 | Site | Trailing-slash and upper/lower-case variants of a URL resolve to one address |
| 17 | Site | No redirect chain is longer than one hop |
| 18 | Site | No redirect loops exist |
| 19 | Site | Permanent moves use a 301 or 308, never a 302 or a meta refresh |
| 20 | Site | No internal link points to a URL that redirects |
| 21 | Site | No internal link returns a 4xx error |
| 22 | Site | No page returns a 5xx error during a full crawl |
| 23 | Site | Missing pages return a true 404 status with a helpful 404 page, and no soft 404s exist |
| 24 | Site | No duplicate pages: the same content is not reachable at more than one indexable URL |
| 25 | Site | URL parameters for tracking, sorting and filtering do not create indexable duplicates |
| 26 | Site | Paginated series are crawlable and each page in the series is self-canonical |
| 27 | Page | The main content is in the HTML Google receives and does not depend on a click or scroll to appear |
| 28 | Site | The CSS and JavaScript needed to render pages are not blocked from crawlers |
| 29 | Site | Search Console shows no unresolved page-indexing errors for pages meant to rank |
| 30 | Site | Search Console shows no manual action and no security issue |
| 31 | Site | Search Console crawl stats show no rise in errors and no host problems |
| 32 | Page | The URL is lowercase, hyphenated, readable and free of session IDs |
| 33 | Site | Language and region tags (hreflang), where used, are valid and reciprocal |
| 34 | Site | Staging and test copies of the site are blocked from indexing |
| 35 | Site | IndexNow is set up so Bing and other engines learn of changes at once |
| 36 | Site | Crawl data or server logs confirm Googlebot reached every key page in the last 30 days |

## 2. Speed and stability (24) · Read

Google's speed scores (Core Web Vitals) on phone and desktop, image weight, scripts, hosting response.

| # | Scope | Check |
|---|---|---|
| 37 | Page | Largest Contentful Paint is 2.5 seconds or less on mobile |
| 38 | Page | Largest Contentful Paint is 2.5 seconds or less on desktop |
| 39 | Page | Interaction to Next Paint is 200 milliseconds or less on mobile |
| 40 | Page | Interaction to Next Paint is 200 milliseconds or less on desktop |
| 41 | Page | Cumulative Layout Shift is 0.1 or less on mobile |
| 42 | Page | Cumulative Layout Shift is 0.1 or less on desktop |
| 43 | Site | The site passes the Core Web Vitals assessment in Search Console on real-user data |
| 44 | Page | Server response time (time to first byte) is 800 milliseconds or less |
| 45 | Page | PageSpeed Insights performance score is 80 or higher on mobile |
| 46 | Page | PageSpeed Insights performance score is 90 or higher on desktop |
| 47 | Page | Total page weight on first load is under 2 MB |
| 48 | Page | The largest above-the-fold element is prioritised and never lazy-loaded |
| 49 | Page | Images below the fold are lazy-loaded |
| 50 | Page | Images are served in a modern format such as WebP or AVIF |
| 51 | Page | No image is delivered larger than the size it is displayed at |
| 52 | Page | Images, videos and embeds reserve their space so nothing shifts while loading |
| 53 | Page | No script in the page head blocks rendering: scripts are deferred or asynchronous |
| 54 | Page | No single third-party script blocks the main thread for more than 250 milliseconds |
| 55 | Site | Text files are compressed with Brotli or gzip |
| 56 | Site | Static files are cached with long cache lifetimes |
| 57 | Site | A content delivery network serves static files |
| 58 | Site | HTTP/2 or HTTP/3 is enabled |
| 59 | Page | Fonts are limited in number, preloaded and show fallback text while loading |
| 60 | Site | Uptime is monitored and was 99.9% or better over the last 30 days |

## 3. Mobile experience (14) · Read

Tap targets, viewport, menus, forms, click-to-call.

| # | Scope | Check |
|---|---|---|
| 61 | Page | The viewport tag is set so the page fits the screen width |
| 62 | Page | No horizontal scrolling at a 390-pixel phone width |
| 63 | Page | The layout holds together at a 768-pixel tablet width |
| 64 | Page | Body text is at least 16 pixels and readable without zooming |
| 65 | Page | Buttons and links are at least 48 pixels tall with space between them |
| 66 | Site | The mobile menu opens, closes and reaches every main section |
| 67 | Page | Phone numbers are tap-to-call links |
| 68 | Page | Forms are usable on a phone: correct keyboard per field, visible labels, working autofill |
| 69 | Page | No pop-up or overlay covers the content on arrival |
| 70 | Page | Mobile and desktop versions carry the same content, headings, links and structured data |
| 71 | Page | The primary call to action is visible on a phone without scrolling |
| 72 | Page | Sticky bars and buttons never cover content or other buttons |
| 73 | Page | Tables and wide content stack or scroll inside their own container |
| 74 | Page | Addresses open in maps and email addresses open a new message |

## 4. Security (10) · Read

Secure connection and certificate, insecure elements, software versions, exposed files.

| # | Scope | Check |
|---|---|---|
| 75 | Site | The security certificate is valid and does not expire within 30 days |
| 76 | Site | Every http request redirects to https |
| 77 | Page | The page loads no insecure (http) images, scripts or styles |
| 78 | Site | The HSTS header is set |
| 79 | Site | Standard security headers are set: content security policy, content-type options, frame protection, referrer policy |
| 80 | Site | The CMS, theme and plugins run current, supported versions |
| 81 | Site | No backup files, repository folders, environment files, debug logs or open directory listings are exposed |
| 82 | Site | The admin login is protected: no default address or user, attempts limited, two-factor on |
| 83 | Site | Google Safe Browsing and blocklist checks show no malware or warnings |
| 84 | Site | Forms are protected against spam and injection, and backups run automatically with a tested restore |

## 5. Site structure (18) · Read

Navigation, depth, links between pages, pages nothing links to, breadcrumbs.

| # | Scope | Check |
|---|---|---|
| 85 | Site | Every page meant to rank is reachable within three clicks of the home page |
| 86 | Site | No orphan pages: every indexable page has at least one internal link pointing to it |
| 87 | Site | The main navigation is made of ordinary HTML links that work without scripts |
| 88 | Site | Navigation labels are descriptive and each link's text matches the topic of its target |
| 89 | Site | The header links only to priority pages |
| 90 | Site | The footer carries a plain list of key pages, legal pages and contact details |
| 91 | Page | Breadcrumbs are visible on every page below the home page |
| 92 | Page | The breadcrumb shows the real hierarchy and matches the breadcrumb markup |
| 93 | Site | URL folders mirror the site hierarchy |
| 94 | Page | The page links up to its parent or hub page |
| 95 | Page | At least three related pages link to this page from within their content |
| 96 | Page | The page links to three to five related pages from within its content |
| 97 | Page | Internal link text is descriptive, never "click here", and varies naturally |
| 98 | Site | Each search is locked to one page, and every other mention of it on the site links to that page |
| 99 | Site | No two pages compete for the same search |
| 100 | Site | Every hub page links to all of its child pages and every child links back |
| 101 | Site | On-site search, where present, works and its result pages are not indexed |
| 102 | Site | The pages with the most internal links are the priority pages |

## 6. Page titles and descriptions (14) · Read

Every page's title and description against its assigned search.

| # | Scope | Check |
|---|---|---|
| 103 | Page | The page has exactly one title tag |
| 104 | Page | The title is 30 to 60 characters and is not cut off in results |
| 105 | Page | The title is unique across the site |
| 106 | Page | The title leads with the page's assigned search |
| 107 | Page | The title matches what the page actually delivers |
| 108 | Page | The brand name sits at the end of the title in one consistent format |
| 109 | Page | The page has exactly one meta description |
| 110 | Page | The meta description is 110 to 155 characters |
| 111 | Page | The meta description is unique across the site |
| 112 | Page | The meta description is made of complete sentences, leads with the answer and gives a reason to click |
| 113 | Page | The meta description contains the assigned search or a close variant, naturally |
| 114 | Page | The title Google displays in results matches the written title |
| 115 | Page | Sharing tags are set: title, description and a 1200 by 630 image |
| 116 | Site | The site name and icon display correctly in search results |

## 7. Headings and copy (20) · Read

Headings, length, readability, service and area coverage, thin pages.

| # | Scope | Check |
|---|---|---|
| 117 | Page | The page has exactly one H1 |
| 118 | Page | The H1 contains the assigned search or a natural paraphrase of it |
| 119 | Page | Headings run in order with no level skipped |
| 120 | Page | At least two or three H2s are phrased as the reader's next questions |
| 121 | Page | Headings describe the content beneath them and are never used only for styling |
| 122 | Page | The assigned search appears in the first 100 words |
| 123 | Page | Each supporting search appears in a heading or FAQ question and in the body |
| 124 | Page | No stuffing: a search term is never used three times in one paragraph and the copy reads naturally aloud |
| 125 | Page | The page opens with the direct answer, not with background |
| 126 | Page | Word count is within the range for its page type and never under 300 words |
| 127 | Page | Reading level is grade 7 to 9 and the average sentence is under 20 words |
| 128 | Page | Paragraphs are one to three sentences |
| 129 | Page | Every service and sub-service the business offers on this topic is covered |
| 130 | Page | Areas served are stated accurately |
| 131 | Page | At least one table or list is used where the content is tabular or step-by-step |
| 132 | Page | No block of copy is shared with sibling pages beyond the agreed overlap limit |
| 133 | Page | No filler phrases and no superlatives without proof |
| 134 | Page | Spelling, grammar, articles and the casing of acronyms and place names are correct |
| 135 | Page | No placeholder text, bracketed notes, outdated years or expired facts remain |
| 136 | Page | The vocabulary is the trade's own: the words customers and practitioners really use |

## 8. Images and media (12) · Read

Image descriptions, file names, size, formats, loading.

| # | Scope | Check |
|---|---|---|
| 137 | Page | Every meaningful image has alt text and decorative images have empty alt text |
| 138 | Page | Alt text describes what is actually in the image and is never a list of search terms |
| 139 | Page | Image file names are descriptive and hyphenated |
| 140 | Page | The page has at least one original image that is not stock |
| 141 | Page | No image file is over 200 KB without a stated reason |
| 142 | Page | Responsive images serve the right size for each screen |
| 143 | Page | Meaningful images are real image elements, not CSS backgrounds |
| 144 | Page | Videos have a title, a description and captions or a transcript |
| 145 | Page | Videos never autoplay with sound and load only when needed, behind a poster image |
| 146 | Site | Key images are included in the sitemap |
| 147 | Page | Photos of people, premises and work are real and belong to the business |
| 148 | Page | The image shown when the page is shared is set and displays correctly |

## 9. Verified facts (20) · Read

The coded business facts Google and AI read (schema markup): business, service, FAQ, review, article, breadcrumb.

| # | Scope | Check |
|---|---|---|
| 149 | Site | Organization or LocalBusiness markup is present on the home page |
| 150 | Site | The organization markup's name, address, logo and contact details match the visible facts exactly |
| 151 | Site | The sameAs list names every official profile and every link in it works |
| 152 | Site | WebSite markup is present with the site name |
| 153 | Page | Breadcrumb markup is present and matches the visible breadcrumb |
| 154 | Page | Service pages carry Service markup with service type, provider and area served |
| 155 | Page | Where an FAQ is shown, FAQPage markup is present and identical to the visible questions and answers |
| 156 | Page | Articles carry Article markup with headline, author, published date and modified date |
| 157 | Page | The author is marked up as a Person with name, page, job title and profiles |
| 158 | Page | Review and rating markup is used only for real, visible reviews and within Google's rules |
| 159 | Site | Where real premises exist, address, coordinates, hours and phone in the markup match the Google profile |
| 160 | Page | All markup parses without errors |
| 161 | Page | The page passes Google's Rich Results Test with no errors |
| 162 | Page | The schema validator shows no missing required properties |
| 163 | Page | Markup describes only what is visible on the page |
| 164 | Site | One phone format, one logo address and one business name are used in all markup |
| 165 | Page | Entities are joined by identifiers: organization, website, page and author reference each other |
| 166 | Page | No duplicate or conflicting markup blocks are output by plugins |
| 167 | Page | Dates in the markup match the dates shown on the page |
| 168 | Page | Specialised types are used where they fit: steps, video, product, event, defined term |

## 10. AI readiness (24) · Read

Answer-first copy, question coverage, a clear identity, the AI guide file (llms.txt), AI crawler access, citation-worthy facts.

| # | Scope | Check |
|---|---|---|
| 169 | Page | The question is the heading and a direct answer of 40 to 60 words sits directly under it |
| 170 | Page | Every section opens with its own answer, so it can be quoted alone |
| 171 | Page | Sections make sense out of context, with no "as mentioned above" |
| 172 | Page | The follow-up questions people ask on this topic are each answered on the page |
| 173 | Page | An FAQ of five to eight questions is present, each answered in 40 to 60 words |
| 174 | Page | Facts are stated as plain sentences an assistant can quote: who, what, where, how much, how long |
| 175 | Page | The page contains at least one original number, data point or finding, with its source |
| 176 | Page | Outside facts name their source and link to it |
| 177 | Page | Where people ask "best" or "versus", the page answers in a comparison or table |
| 178 | Page | The page carries one quotable line from a named expert |
| 179 | Page | The published date and last-reviewed date are visible |
| 180 | Site | An llms.txt file exists at the root, is accurate and lists the key pages |
| 181 | Site | robots.txt allows the AI crawlers the business has chosen to allow, by name |
| 182 | Site | The firewall and content delivery network do not block those AI crawlers |
| 183 | Page | The content is readable with JavaScript turned off |
| 184 | Site | One identity sentence describes the business the same way on the site and on every profile |
| 185 | Site | The About page states in plain facts who the business is, what it does, where, since when and for whom |
| 186 | Site | The brand name cannot be confused with another organisation, or the difference is stated |
| 187 | Site | The business's records on the sources AI draws from, such as LinkedIn, Crunchbase and Wikidata, exist and agree |
| 188 | Site | The business is present on the third-party lists, directories and review sites AI cites for its trade |
| 189 | Page | The business is named when the page's main question is asked in ChatGPT, recorded with the date |
| 190 | Page | The business is cited when the page's main question triggers a Google AI Overview or AI Mode answer, recorded with the date |
| 191 | Page | The business is named when the page's main question is asked in Perplexity and Gemini, recorded with the date |
| 192 | Site | What AI assistants say about the business is checked for wrong facts, and each one is logged |

## 11. Local signals (26) · Confirm

Name, address, phone consistency across site, profile and listings; service-area pages; map embed.

| # | Scope | Check |
|---|---|---|
| 193 | Site | The business name is identical on the site, the Google profile and every listing |
| 194 | Site | The address is identical everywhere, including its format |
| 195 | Site | The phone number is identical everywhere and is a local number where the business is local |
| 196 | Site | Name, address and phone appear on the site as text, not inside an image |
| 197 | Site | A contact page shows name, address, phone, hours and email |
| 198 | Site | Opening hours are identical everywhere |
| 199 | Site | A map is embedded on the contact or location page where real premises exist |
| 200 | Site | The areas served are listed on the site accurately |
| 201 | Site | Each priority service area has its own page |
| 202 | Page | A service-area page is at least 70% unique against its sibling area pages |
| 203 | Page | A local page names real neighbourhoods, landmarks and local conditions |
| 204 | Page | A local page is not a copy of another with the place name swapped |
| 205 | Site | A business with several locations has one page per location, each with its own details |
| 206 | Site | The business is listed on Apple Business Connect and Bing Places |
| 207 | Site | The business is listed on Yelp, Facebook and the main general directories |
| 208 | Site | The business is listed on the directories specific to its trade |
| 209 | Site | The business is listed with its local chamber of commerce and trade associations |
| 210 | Site | No duplicate listings exist on any platform |
| 211 | Site | No listing shows an old name, address or phone number |
| 212 | Site | Listing categories are consistent from platform to platform |
| 213 | Site | The website address on every listing is correct and uses https |
| 214 | Page | Local pages carry the place name in the title, H1 and copy, naturally |
| 215 | Site | Directions, parking or service radius are explained where customers need them |
| 216 | Site | Call tracking uses number swapping on the site only, so listed numbers stay consistent |
| 217 | Site | Local press, sponsorships and partners mention or link to the business |
| 218 | Site | No virtual office or false address is used anywhere |

## 12. Google Business Profile (22) · Confirm

Categories, services, attributes, photos, posts, Q&A, hours, reviews.

| # | Scope | Check |
|---|---|---|
| 219 | Beyond | The profile is claimed and verified |
| 220 | Beyond | The profile is owned by the business's own account, with correct access roles |
| 221 | Beyond | The profile name is the real business name with no added search terms |
| 222 | Beyond | The primary category is the most specific correct one |
| 223 | Beyond | Secondary categories are complete and accurate |
| 224 | Beyond | The address or service-area setting is correct, with the address hidden for service-area businesses |
| 225 | Beyond | Service areas are listed |
| 226 | Beyond | Phone and website are correct, and the website link carries a tracking tag |
| 227 | Beyond | Regular and holiday hours are set |
| 228 | Beyond | The business description is complete and accurate |
| 229 | Beyond | Every service is listed with a description |
| 230 | Beyond | Products or a menu are listed where they apply |
| 231 | Beyond | All relevant attributes are filled in |
| 232 | Beyond | The opening date is set |
| 233 | Beyond | Logo and cover photo are set |
| 234 | Beyond | At least ten real photos are present and new ones are added every month |
| 235 | Beyond | Posts go out at the agreed cadence and the latest is under seven days old |
| 236 | Beyond | A booking or appointment link is set |
| 237 | Beyond | Customer questions on the profile are answered, and common ones are covered in the description and posts |
| 238 | Beyond | No duplicate profile exists and none is suspended |
| 239 | Beyond | Profile facts match the website and its markup |
| 240 | Beyond | Calls, direction requests, website clicks and searches are recorded monthly |

## 13. Reviews and reputation (10) · Confirm

Volume, rating, recency, response rate, platforms.

| # | Scope | Check |
|---|---|---|
| 241 | Beyond | The Google review count is at or above the middle of the top three local competitors |
| 242 | Beyond | The average Google rating is 4.5 or higher |
| 243 | Beyond | At least one new review arrived in the last 30 days |
| 244 | Beyond | Reviews arrive steadily, not in bursts |
| 245 | Beyond | Every review has a reply within two working days, and critical ones are answered professionally |
| 246 | Beyond | Reviews exist on at least two other platforms that matter for the trade |
| 247 | Site | A review request goes out after every job, with no filtering of unhappy customers and no rewards |
| 248 | Beyond | Reviews mention services and places in the customers' own words |
| 249 | Page | Real reviews are shown on the site with their source |
| 250 | Beyond | No fake reviews exist, and a search for the brand shows no unanswered complaint on page one |

## 14. Conversion elements (22) · Choose

Calls to action, forms, phone placement, trust badges, proof, offers, chat.

| # | Scope | Check |
|---|---|---|
| 251 | Page | The page has one primary call to action, the same one throughout |
| 252 | Page | The call to action is visible without scrolling |
| 253 | Page | The call to action repeats after the proof section and at the end of the page |
| 254 | Page | The call-to-action wording says exactly what happens next |
| 255 | Page | The phone number is in the header and tappable |
| 256 | Page | The form asks only for what is needed |
| 257 | Page | A test submission arrives, and the sender sees a confirmation |
| 258 | Page | Form errors are clear and tell the visitor how to fix them |
| 259 | Page | The confirmation says what happens next and when |
| 260 | Site | A person answers each new lead within the agreed time, tested with a real enquiry |
| 261 | Page | Licences, insurance, certifications or guarantees are shown near the call to action |
| 262 | Page | Real reviews or testimonials are on the page |
| 263 | Page | Proof is shown: results, examples or numbers, each with a source |
| 264 | Page | A lighter second step is offered to visitors not ready to talk |
| 265 | Site | The chat widget works, is answered and covers no content |
| 266 | Site | The booking link works from first click to confirmed appointment |
| 267 | Page | Within five seconds a visitor can tell what is offered, for whom and where |
| 268 | Page | Pricing or honest price guidance is present |
| 269 | Page | The page answers the usual objections: cost, time and risk |
| 270 | Page | The page has no dead end: every section leads to a next step |
| 271 | Page | No competing actions or pop-ups pull the visitor from the primary action |
| 272 | Site | The offer or commitment that removes the visitor's risk is stated |

## 15. Tracking and measurement (12) · Choose

GA4, Search Console, call tracking, form tracking, conversions.

| # | Scope | Check |
|---|---|---|
| 273 | Site | Google Analytics 4 is installed once on every page |
| 274 | Site | Key events are set in Analytics: form, call, booking and chat |
| 275 | Site | Search Console is verified for the whole domain, with owner access held by the business |
| 276 | Site | Bing Webmaster Tools is verified |
| 277 | Site | Call tracking is in place and names the source of each call |
| 278 | Site | Every form submission records the page it came from |
| 279 | Site | Every booking records the page it came from |
| 280 | Site | Office traffic and bots are filtered out of the data |
| 281 | Site | The consent banner and consent mode are set so data is lawful and complete |
| 282 | Site | Links from the profile, social posts and email carry a consistent tracking tag |
| 283 | Site | Visits from ChatGPT, Perplexity, Gemini and Copilot are separated out in Analytics |
| 284 | Site | Position and AI-mention tracking is set up for the mapped searches, with a starting baseline |

## 16. Content inventory (8) · Read

Every page listed with its purpose, search, status: keep, fix, merge, remove.

| # | Scope | Check |
|---|---|---|
| 285 | Site | Every URL on the site is listed in one inventory |
| 286 | Site | Each page has a stated purpose and reader |
| 287 | Site | Each page has one assigned search |
| 288 | Site | Each page has a status: keep, fix, merge or remove |
| 289 | Site | Thin, outdated and duplicate pages are identified |
| 290 | Site | Pages that already hold rankings, traffic or links are marked protected before any change |
| 291 | Site | Mapped searches with no page are listed as gaps |
| 292 | Site | Every page to be merged or removed has a redirect target |

## 17. Off-site presence (12) · Confirm

Listings, mentions, profiles, press, inconsistencies, duplicates.

| # | Scope | Check |
|---|---|---|
| 293 | Beyond | A search for the brand shows the business's own properties across page one |
| 294 | Beyond | Relevant industry sites mention the business, counted against competitors |
| 295 | Beyond | Real, relevant sites link to the business, counted against the top three competitors |
| 296 | Beyond | No spam, paid or manipulative link patterns point at the site |
| 297 | Beyond | The wording of links pointing at the site looks natural |
| 298 | Beyond | The business earned press or editorial mentions in the last 12 months |
| 299 | Beyond | Profiles on the platforms that matter for the trade are claimed and complete |
| 300 | Beyond | Facts are identical on every profile |
| 301 | Beyond | No duplicate or abandoned profiles exist |
| 302 | Beyond | Mentions of the brand without a link are identified |
| 303 | Beyond | The business appears on the lists and comparison pages that rank for "best" searches in its trade and area |
| 304 | Beyond | The business is present where customers ask: Reddit, Quora and trade forums |

## 18. Social presence (9) · Confirm

Channels, completeness, cadence, consistency with site.

| # | Scope | Check |
|---|---|---|
| 305 | Beyond | The right channels for the trade are identified and claimed |
| 306 | Beyond | Handles match the brand on every channel |
| 307 | Beyond | Each profile is complete: description, link, contact, category and images |
| 308 | Beyond | Facts on each profile match the site |
| 309 | Beyond | The posting cadence is met and the last post is under 14 days old |
| 310 | Beyond | Posts are original and show real work and real people |
| 311 | Beyond | Comments and messages are answered |
| 312 | Site | The site links to each profile and each profile links to the site |
| 313 | Beyond | Each key page on the site has been shared on the channels |

## 19. Search map coverage (14) · Question

Every kind of search a customer makes is mapped, not a short keyword list.

| # | Scope | Check |
|---|---|---|
| 314 | Site | Every service in every area served is mapped to the searches customers use for it |
| 315 | Site | Hiring searches are mapped: the words used when someone is ready to buy |
| 316 | Site | Outcome searches are mapped: the results customers ask for in their own words |
| 317 | Site | Question searches are mapped |
| 318 | Site | Comparison and "best" searches are mapped |
| 319 | Site | Problem searches are mapped: "why is" and "how do I fix" |
| 320 | Site | Cost searches are mapped |
| 321 | Site | Switching searches are mapped: alternatives to a current provider or platform |
| 322 | Site | AI prompts are mapped: the full sentences people type into assistants |
| 323 | Site | Spoken and "near me" forms are mapped |
| 324 | Site | Searches in other languages are mapped where customers use them |
| 325 | Site | Each mapped search is assigned to exactly one page |
| 326 | Site | Each mapped search carries dated evidence that people really make it |
| 327 | Site | The map is compared with Search Console queries every 30 days and new searches are added |

## 20. Uniqueness and information gain (12) · Read

Whether the page says something no other page says.

| # | Scope | Check |
|---|---|---|
| 328 | Page | The page contains at least one fact or number available nowhere else |
| 329 | Page | The page contains at least one first-hand finding from real work |
| 330 | Page | The named author states a clear position or verdict |
| 331 | Page | A local page carries three facts true only for that place and trade |
| 332 | Page | Overlap with every other page on the site is under 25%, measured by script |
| 333 | Page | The page would be wrong if the place or trade name were swapped |
| 334 | Page | The page says something the three top-ranking pages do not, and the gap is noted |
| 335 | Page | The page has an original chart, table, photo or diagram |
| 336 | Page | The page gives steps the reader can carry out themselves |
| 337 | Page | Examples are specific and real |
| 338 | Page | No text is copied from elsewhere on the web |
| 339 | Page | The FAQ set is not reused on any other page |

## 21. Fact integrity (10) · Read

Whether every claim on the page is true and traceable.

| # | Scope | Check |
|---|---|---|
| 340 | Page | Every number traces to an entry in the fact register with its source |
| 341 | Page | Company facts match the fact register exactly |
| 342 | Page | No invented reviews, awards, clients or team members appear |
| 343 | Page | Results are stated as counts with their definition |
| 344 | Page | No superlative appears without proof |
| 345 | Page | Outside facts were confirmed at the original source, with the date checked |
| 346 | Page | Quotes are real and approved by the person quoted |
| 347 | Page | Prices, timeframes and guarantees match what the business really offers |
| 348 | Page | Regulated claims follow the rules of the field: legal, medical, financial |
| 349 | Page | A named person signed the fact-check sheet before publishing |

## 22. Author and entity (12) · Confirm

Who stands behind the content and whether they can be verified.

| # | Scope | Check |
|---|---|---|
| 350 | Page | A named author is shown on the page |
| 351 | Site | The author has a page with experience, credentials and a photo |
| 352 | Site | The author's outside profiles are consistent and linked |
| 353 | Page | The author's expertise fits the topic |
| 354 | Page | Health, legal and money topics show a qualified reviewer |
| 355 | Site | The site publishes how its content is written and checked |
| 356 | Site | Ownership, leadership and location are stated openly |
| 357 | Site | Phone, email and address are real and answered |
| 358 | Site | Privacy policy, terms and required legal pages are present and current |
| 359 | Site | Licences, memberships and awards shown are current and can be checked with the issuer |
| 360 | Site | Named methods and terms are defined on their own page with defined-term markup |
| 361 | Site | Asking AI assistants about the brand and the author returns an accurate description |

## 23. AI answer verification (16) · Choose

Measured presence in AI answers, engine by engine, over repeated runs.

| # | Scope | Check |
|---|---|---|
| 362 | Site | A prompt set is defined: at least ten real prompts for each service and area |
| 363 | Beyond | Every prompt is run in ChatGPT and the answer recorded |
| 364 | Beyond | Every prompt is run in Gemini and the answer recorded |
| 365 | Beyond | Every prompt is run in Perplexity and the answer recorded |
| 366 | Beyond | Every prompt is checked in Google AI Overviews and AI Mode and the answer recorded |
| 367 | Beyond | Every prompt is run in Microsoft Copilot and the answer recorded |
| 368 | Beyond | Every prompt is run in the sixth engine of the AI Score set and the answer recorded |
| 369 | Beyond | Each prompt is run at least three times per engine and the share of runs naming the business is recorded |
| 370 | Beyond | The position in each answer is recorded: named first, listed or absent |
| 371 | Beyond | The sources each engine cites are recorded, and the business is present on them |
| 372 | Beyond | The competitors each engine names are recorded |
| 373 | Beyond | What each engine says about the business is factually right |
| 374 | Beyond | Each engine's description of the business matches how the business presents itself |
| 375 | Beyond | Citation links point to the right page |
| 376 | Beyond | Raw answers are archived with their date |
| 377 | Beyond | The change from the previous month is reported |

## 24. Accessibility (12) · Read

Whether everyone can use the page (WCAG 2.2 AA).

| # | Scope | Check |
|---|---|---|
| 378 | Page | Text contrast is at least 4.5 to 1 |
| 379 | Page | Every function works from the keyboard alone |
| 380 | Page | Keyboard focus is always visible |
| 381 | Page | A skip-to-content link is present |
| 382 | Page | Every form field has a label and errors are announced |
| 383 | Page | The page language is declared |
| 384 | Page | Page regions use proper landmarks and semantic elements |
| 385 | Page | Link text makes sense out of context |
| 386 | Page | No information is carried by colour alone |
| 387 | Page | Text can be enlarged to 200% without loss of content |
| 388 | Page | Motion and autoplay can be paused and reduced-motion settings are respected |
| 389 | Page | An automated scan shows no critical errors and a screen-reader pass was done on the template |

## 25. Video and visual search (8) · Confirm

Presence where people search by watching and by image.

| # | Scope | Check |
|---|---|---|
| 390 | Beyond | A YouTube channel is claimed, branded and linked to the site |
| 391 | Beyond | A video exists for each priority service or question |
| 392 | Beyond | Video titles and descriptions match mapped searches and use chapters |
| 393 | Beyond | Captions and transcripts are accurate |
| 394 | Page | Each video is embedded on its matching page with video markup |
| 395 | Beyond | Videos have custom thumbnails |
| 396 | Beyond | Short versions are published on the short-video platforms |
| 397 | Page | Original photos of real work carry enough context to appear in image and lens searches |

## 26. Freshness and corrections (8) · Read

Whether the page stays true over time.

| # | Scope | Check |
|---|---|---|
| 398 | Page | The page shows its last review date and reviewer |
| 399 | Site | Each page type has a review cycle and no page is past it |
| 400 | Page | Time-sensitive facts are flagged for re-checking: prices, laws, product names, years |
| 401 | Site | After each search-system update, affected pages are reviewed within 14 days |
| 402 | Site | A public record lists corrections made |
| 403 | Page | Dated predictions are revisited and marked right or wrong |
| 404 | Site | Outdated pages are updated, merged or removed, never left standing |
| 405 | Page | The modified date changes only when the content really changes |

## 27. Publishing readiness (8) · Read

The gate a page passes before and after it goes live.

| # | Scope | Check |
|---|---|---|
| 406 | Page | The page passed every applicable check and the result is recorded |
| 407 | Page | A second, independent reviewer signed it off |
| 408 | Page | The owner approved it where the rules require approval |
| 409 | Page | Its internal links in and out are placed at publish, so it never launches as an orphan |
| 410 | Page | It is added to the sitemap and indexing is requested |
| 411 | Page | The live page is fetched and checked again after publishing |
| 412 | Page | Its distribution pieces are scheduled |
| 413 | Page | It is recorded in the work log with a day-seven indexing check |
