"""Writes keyword-map-v2.md from the two CSV files. Run after map_v2.py and woven.py."""
import csv
from collections import Counter,defaultdict
km=list(csv.DictReader(open("keyword-map-v2.csv"))); wv=list(csv.DictReader(open("woven-keywords-v2.csv")))
g=Counter(r["live_grade"] for r in km if r["keyword"]); q=defaultdict(list)
for r in wv:
    if r["role"]=="question": q[r["url"]].append(r["keyword"])
md=["# Keyword map v2","","Step 5 of the roadmap. Built by `map_v2.py`, `woven.py` and `summary.py`; raw Google answers are in `evidence/`.","",
"## How each page is keyed","",
"- **Locked, up to three per page.** One lead keyword that sets the address, title and heading, and up to two with the same intent. No other page may target them.",
"- **Woven, not locked.** Up to three section keywords and up to eight real questions, taken from Google's own suggestions. The writer uses the ones that fit; a question is answered on only one page.","",
"## Result","",
f"- {len({r['url'] for r in km})} foundation pages. {sum(1 for r in km if r['keyword'])} locked keywords. No keyword sits on two pages.",
f"- Live evidence: {g['A']} confirmed real searches, {g['B']} weak signals, {g.get('C',0)+g.get('D',0)} without a signal, {g['own term']} RSM's own terms.",
f"- {len(wv)} woven keywords: {sum(1 for r in wv if r['role']=='section keyword')} section keywords and {sum(1 for r in wv if r['role']=='question')} questions.",
f"- {sum(1 for r in km if r['role']=='none')} pages have no search target by design: tools, trust and legal pages.",
"- The 113 element pages carry one lead keyword each, listed in `04-architecture/elements.md`.","",
"## The equation pages carry existing demand","","| Page | Lead keyword |","|---|---|",
"| Read | on page seo |","| Confirm | off page seo |","| Choose | conversion rate optimization |",
"| D'Souza's Law of Search | supported by \"is seo dead\" and \"future of seo\" |","| The Standard | seo audit |","| The Method | seo strategy |","| Every engine | ai search engines |","",
"## Limits","",
"- No search volumes. Autocomplete proves a search exists, not how often it is made. Volumes come from Search Console after launch.",
"- The checking machine is not always treated as a US user. Suggestions naming other countries are filtered out by script.",
"- The woven list is a pool. A few suggestions have the wrong intent and are dropped by the writer.","",
"## All pages","","| # | Page | Lead | Same intent | Questions found |","|---|---|---|---|---|"]
by=defaultdict(list)
for r in km: by[(r["page"],r["page_name"],r["url"])].append(r)
for (n,name,url),rs in by.items():
    k=[r["keyword"] for r in rs if r["keyword"]]
    md.append(f"| {n} | {name} | {k[0] if k else 'none'} | {' · '.join(k[1:])} | {len(q[url])} |")
open("keyword-map-v2.md","w").write("\n".join(md)); print("summary written:",len(by),"pages")
