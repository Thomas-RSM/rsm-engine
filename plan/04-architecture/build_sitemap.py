"""Builds the foundation site map and checks it. Run: python3 build_sitemap.py"""
import csv,sys
# layer, page, url, parent url, menu slot, main keyword already mapped in step 5 v1 ("" = to map)
P=[
("Home","Home","/","","Logo","seo company in usa"),
# Situations: menu "What's wrong?"
("Situation","Nobody can find my business online","/problems/not-showing-up-on-google/","/problems/","What's wrong?","why is my business not showing up on google"),
("Situation","People find me but don't pick me","/problems/not-getting-leads/","/problems/","What's wrong?","how to get more leads for my business"),
("Situation","Google shows me, AI doesn't","/problems/not-recommended-by-chatgpt/","/problems/","What's wrong?","how to get my business recommended by chatgpt"),
("Situation","I was ranking and I lost it","/problems/traffic-dropped/","/problems/","What's wrong?","website traffic dropped suddenly"),
("Situation","I'm being quoted and don't know if it's fair","/problems/seo-cost/","/problems/","What's wrong?","how much does seo cost"),
("Hub","Problems: the encyclopedia","/problems/","/","What's wrong?","seo problems"),
# The equation: menu "The Equation"
("Equation","The D'Souza Equation","/dsouza-equation/","/","The Equation",""),
("Equation","D'Souza's Law of Search: engines change, the question does not","/dsouza-equation/law-of-search/","/dsouza-equation/","The Equation",""),
("Equation","Read: can every engine read your business","/dsouza-equation/read/","/dsouza-equation/","The Equation",""),
("Equation","Confirm: do others say the same","/dsouza-equation/confirm/","/dsouza-equation/","The Equation",""),
("Equation","Choose: do people and engines pick you","/dsouza-equation/choose/","/dsouza-equation/","The Equation",""),
("Equation","The D'Souza Standard: all 413 checks","/dsouza-equation/standard/","/dsouza-equation/","The Equation","seo audit"),
("Equation","The D'Souza Method: the first 15 days and every day after","/dsouza-equation/method/","/dsouza-equation/","The Equation","seo plan"),
("Equation","Every engine: the open list","/dsouza-equation/engines/","/dsouza-equation/","The Equation",""),
("Equation","How search works now","/dsouza-equation/how-search-works/","/dsouza-equation/","The Equation","how does google search work"),
("Equation","SEO vs AEO vs GEO vs AIO, and where each fits","/dsouza-equation/seo-vs-aeo-vs-geo/","/dsouza-equation/","The Equation","universal engine optimization"),
# Search services: menu "Services"
("Service","SEO","/services/seo/","/services/","Services","seo services"),
("Service","Local SEO","/services/local-seo/","/services/","Services","local seo services"),
("Service","AI SEO","/services/ai-seo/","/services/","Services","ai seo services"),
("Service","Answer Engine Optimization (AEO)","/services/answer-engine-optimization/","/services/","Services","answer engine optimization"),
("Service","Generative Engine Optimization (GEO)","/services/generative-engine-optimization/","/services/","Services","generative engine optimization"),
("Service","AI Overview Optimization (AIO)","/services/ai-overview-optimization/","/services/","Services","ai overview optimization"),
("Service","ChatGPT and LLM SEO","/services/chatgpt-seo/","/services/","Services",""),
("Service","Google Business Profile","/services/google-business-profile-optimization/","/services/","Services","google business profile optimization"),
("Service","Technical SEO","/services/technical-seo/","/services/","Services","technical seo"),
("Service","Content marketing","/services/content-marketing/","/services/","Services",""),
("Service","Link building and earned mentions","/services/link-building/","/services/","Services",""),
("Service","Social media marketing (SMO)","/services/social-media-marketing/","/services/","Services","social media marketing services"),
("Service","Reputation and reviews","/services/reputation-management/","/services/","Services",""),
("Service","Voice search","/services/voice-search-optimization/","/services/","Services",""),
("Service","Ecommerce SEO","/services/ecommerce-seo/","/services/","Services","ecommerce seo"),
("Service","B2B SEO","/services/b2b-seo/","/services/","Services",""),
("Service","Small business SEO","/services/small-business-seo/","/services/","Services",""),
("Service","Lead generation","/services/lead-generation/","/services/","Services",""),
("Service","Digital marketing","/services/digital-marketing/","/services/","Services",""),
# Build services
("Service","Web design","/services/web-design/","/services/","Services",""),
("Service","Web development","/services/web-development/","/services/","Services",""),
("Service","App development","/services/app-development/","/services/","Services",""),
("Service","Custom CRM","/services/custom-crm/","/services/","Services",""),
("Service","Design services","/services/design/","/services/","Services",""),
("Hub","Services","/services/","/","Services",""),
# Guides: menu "What's wrong?" second column
("Guide","What is E-E-A-T","/guides/what-is-eeat/","/guides/","What's wrong?","what is e-e-a-t"),
("Guide","SEO keyword research: how we choose","/guides/seo-keyword-research/","/guides/","What's wrong?","seo keyword research"),
("Guide","How long SEO takes","/guides/how-long-does-seo-take/","/guides/","What's wrong?","how long does seo take"),
("Guide","How to choose an SEO company","/guides/how-to-choose-an-seo-company/","/guides/","What's wrong?","how to choose an seo company"),
("Guide","Service business vs ecommerce vs B2B","/guides/service-vs-ecommerce-vs-b2b-seo/","/guides/","What's wrong?",""),
("Hub","Guides","/guides/","/","What's wrong?",""),
# Mirrors: menu "Look yourself up"
("Mirror","Ask","/ask/","/","Header field",""),
("Mirror","AI Recommendation Index","/ai-recommendation-index/","/","Look yourself up","how does chatgpt recommend businesses"),
("Mirror","Open Board","/open-board/","/","Look yourself up",""),
("Mirror","Open Log","/open-log/","/","Look yourself up","seo report example"),
("Mirror","Searches by trade and city","/searches/","/","Look yourself up","plumber seo keywords"),
("Mirror","Your Plan","/your-plan/","/","Look yourself up",""),
("Hub","Industries","/industries/","/","Look yourself up","seo by industry"),
("Hub","Cities","/cities/","/","Look yourself up",""),
# Identity: menu "Who's behind this"
("Identity","Origin: how the equation came about","/about/","/","Who's behind this","relevant search media"),
("Identity","Thomas D'Souza","/thomas-dsouza/","/about/","Who's behind this","thomas d'souza seo"),
("Identity","The two commitments","/commitments/","/about/","Who's behind this","seo guarantee"),
("Identity","Results and reviews","/results/","/about/","Who's behind this","relevant search media reviews"),
("Identity","How we write and check","/about/editorial-policy/","/about/","Footer",""),
("Identity","Corrections","/about/corrections/","/about/","Footer",""),
("Identity","Contact","/contact/","/","Footer",""),
("Identity","Book a discovery call","/book/","/","Button",""),
("Legal","Privacy policy","/privacy/","/","Footer",""),
("Legal","Terms","/terms/","/","Footer",""),
]
errs=[]; urls=[p[2] for p in P]
if len(set(urls))!=len(urls): errs.append("duplicate URL")
kws=[p[5] for p in P if p[5]]
if len(set(kws))!=len(kws): errs.append("a keyword sits on two pages: "+str({k for k in kws if kws.count(k)>1}))
for l,n,u,par,m,k in P:
    if u!="/" and par not in urls: errs.append(f"{u}: parent {par} is not a page")
    if not (u.startswith("/") and u.endswith("/") and u==u.lower() and " " not in u): errs.append(f"bad url {u}")
if errs: print("FAILED",*errs,sep="\n  "); sys.exit(1)
from collections import Counter
lc=Counter(p[0] for p in P); mc=Counter(p[4] for p in P)
with open("site-map.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["number","layer","page","url","parent","menu","main_keyword_v1"])
    for i,p in enumerate(P,1): w.writerow([i,*p])
md=["# Site map: the foundation (draft v1, for approval)","",
f"Step 4 of the roadmap. 23 Nov 2026. **{len(P)} foundation pages.** Built and checked by `build_sitemap.py`: no duplicate address, every page has a parent, no keyword on two pages.","",
"## What changed from the 36","",
"- The D'Souza Equation has its own section of ten pages. It replaces the earlier \"Standard\" section.",
"- Every service RSM sells has a page: 19 search services and 5 build services (web design, web development, app development, custom CRM, design).",
"- The four keyword gaps are closed: web design, link building, content marketing and reputation each have a page.",
"- Trust pages added: how we write and check, corrections, contact, privacy, terms.","",
"## Pages by layer","","| Layer | Pages |","|---|---|"]+[f"| {k} | {v} |" for k,v in lc.items()]+[f"| **Total** | **{len(P)}** |","",
"## The header","",
"A live strip on top: the Standard's version and date, the Open Log's day count, and the open-or-taken check.",
"Then five menus, the Ask field and one button.","",
"| Menu | What the owner hears | Pages |","|---|---|---|",
f"| What's wrong? | Why am I not getting found | {mc['What\\'s wrong?']} |",
f"| The Equation | How this really works | {mc['The Equation']} |",
f"| Services | What you do, by its common name | {mc['Services']} |",
f"| Look yourself up | Show me my own business | {mc['Look yourself up']} |",
f"| Who's behind this | Can I trust you | {mc[chr(87)+'ho'+chr(39)+'s behind this']} |","",
"The Cities menu item opens the main 10 to 15 cities. Every other city is reached from the Cities hub; none is dropped.",
"Link text in every menu is the plain search term. Footer pages are linked from every page.","",
"## After the foundation","",
"Built on these pages, each one passing the page gate before it goes live:","",
"- **Industries**: one page per trade, 49 in the keyword universe.",
"- **Cities**: one page per city, 50 in the keyword universe, with the 10 launch cities first.",
"- **Trade in city**: one page per trade per city, following the pattern `/new-york/plumbers/seo/`.",
"- **Encyclopedia entries** under `/problems/`, from the Problem Atlas.",
"- **Question pages and articles**, daily.","",
"## All pages","","| # | Layer | Page | Address | Menu | Main keyword (v1) |","|---|---|---|---|---|---|"]
for i,(l,n,u,par,m,k) in enumerate(P,1): md.append(f"| {i} | {l} | {n} | `{u}` | {m} | {k or 'to map in Step 5'} |")
md+=["","## To settle in Step 5","",
f"- {sum(1 for p in P if not p[5] and p[0] in ('Service','Guide','Equation','Mirror','Hub'))} pages have no keyword yet. Each gets a locked set, checked against live demand.",
"- Page 17 carried the old method name as its keyword. It is re-mapped to the comparison searches.",
"- The keyword map moves from 36 pages to this list."]
open("site-map.md","w").write("\n".join(md))
print("OK pages:",len(P),dict(lc)); print(dict(mc))
