# RSM keyword universe (v4, 18 Nov 2026)

113,720 unique keywords for relevantsearchmedia.com. Every keyword carries a location (city, suburb/county, state or USA). Zero duplicates across both files.

| File | Contents | Keywords |
|---|---|---|
| `RSM_KU_v4_1_Launch_Cities.xlsx` | 10 launch cities at full depth (New York, Los Angeles, Chicago, Houston, Dallas, Miami, Atlanta, Phoenix, Denver, Fresno), 18 sections each, 14–15 suburbs/counties per city | 77,971 |
| `RSM_KU_v4_2_More_Locations.xlsx` | 40 more cities (lighter depth), all 50 states, USA, the live Google suggestion data, and the "Where Buyers Are" map | 35,749 |

Google Sheets copies (Thomas's Drive):
- Sheet 1: https://docs.google.com/spreadsheets/d/1boGVFbPasi9OHD56boomFgvrRtmbGb55hoKwdNWNGoY/edit
- Sheet 2: https://docs.google.com/spreadsheets/d/1sxj9LqIvGVoUSpkMjNM1_0eg6gxp01Do4b2E0PXiY0o/edit

## Sections (each sheet has a Section Guide tab)
Broad head terms · Primary – Core · Primary – Industry (49 buyer categories) · Primary – Specialty (62 sub-specialties + city-signature industries) · Leads & Outcomes · Switcher · Alternative (lead platforms / agencies) · Owner Research · Spanish · Local Area · Secondary · Question · AEO · AIO · GEO & AI SEO · E-E-A-T · Comparison · AI Prompt.

## Live demand signal
`source/google-suggestions-2026-11-18.txt` holds 995 real US Google suggestions pulled from 197 seeds (49 categories × seo/marketing/leads, 30 agency and AI-search seeds, 10 cities), cleaned of jobs/courses/non-US results. Rows marked "Seen live" match a suggestion exactly; "National form seen live" match after removing the location. No monthly volumes yet: Keyword Planner would not run on the cancelled Ads account and Semrush had no API units.

Findings from the live data: owners search for *leads* (for sale, pay per lead, exclusive) far more than for service names; they say "marketing agency / companies / ideas" and use trade words (plumber, dentist, attorney); ChatGPT "how do I get my business recommended" queries are real; Spanish agency searches exist (Miami); no live demand yet for "[trade] aeo / geo / aio company".

## Rebuilding
`cd builder && python3 build_universe.py` (needs openpyxl). Edit the lists at the top of the script (cities, buyer categories, service lines, suburbs) and regenerate; duplicate and location checks run on every row.

## Keyword Group / Where it lives
One keyword = one group = one home on the site. Only Broad, Tier A category and Switcher groups get dedicated pages; the rest live as sections, question pages or articles until Search Console shows impressions.
