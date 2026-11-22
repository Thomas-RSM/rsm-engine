import json,csv,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from candidates import PAGES
res={r["keyword"]:r["status"] for r in json.load(open("results.json"))}
FINAL={ # page: [main, supporting...]; None main = no search target
1:["seo company in usa","seo agency in usa","digital marketing agency usa"],
2:["why is my business not showing up on google","why is my business not showing up on google maps","how to get my business on google"],
3:["how to get more leads for my business","lead generation company","how to get more customers for my business"],
4:["how to get my business recommended by chatgpt","how to rank in chatgpt","chatgpt seo"],
5:["website traffic dropped suddenly","google ranking dropped dramatically"],
6:["how much does seo cost","seo pricing","seo cost for small business"],
7:["universal engine optimization","search everywhere optimization","seo vs aeo vs geo"],
8:["how does google search work","how do ai overviews work","how does chatgpt search work"],
9:["seo services","seo services company","small business seo services"],
10:["local seo services","local seo agency","google maps seo"],
11:["ai seo services","ai seo agency","ai search optimization"],
12:["answer engine optimization","aeo services","voice search optimization"],
13:["generative engine optimization","generative engine optimization agency","geo services"],
14:["ai overview optimization","how to show up in google ai overviews","google ai overview seo"],
15:["google business profile optimization","google my business optimization","google business profile management"],
16:["technical seo","technical seo audit","schema markup services"],
17:["what is e-e-a-t","google e-e-a-t","e-e-a-t seo"],
18:["social media marketing services","social media optimization","social media marketing for small business"],
19:["seo keyword research","how to do keyword research"],
20:["ecommerce seo","ecommerce seo services","b2b seo services"],
21:["how long does seo take","how long does it take to rank on google","is seo worth it"],
22:["how to choose an seo company","how to choose an seo agency","how to find a good seo company"],
23:["seo audit","seo strategy","seo audit checklist"],
24:[],
25:["how does chatgpt recommend businesses"],
26:[],
27:["seo report example","what does an seo report look like","seo progress report"],
28:["plumber seo keywords","plumbing seo keywords"],
29:["seo plan","seo plan template","90 day seo plan"],
30:["seo problems","common seo issues","digital marketing problems"],
31:["relevant search media"],
32:["thomas d'souza seo"],
33:["seo guarantee","guaranteed seo services","pay for performance seo"],
34:["relevant search media reviews","seo case studies","seo results"],
35:[],
36:["seo by industry","industry specific seo","niche seo"],
}
NOTES={5:"'why did my google rankings drop' has no live signal; the two proven forms are used.",
7:"Main is RSM's own new term: no demand expected yet. The two supporting terms carry the traffic.",
19:"'how to choose keywords for seo' has no live signal; Google completes it for research papers and ads, not SEO.",
20:"No comparison phrase (ecommerce vs local, service vs ecommerce) has a live signal. The page targets ecommerce terms and explains the difference.",
24:"The Ask tool. No search target.",
25:"Only one proven term. 'AI Recommendation Index' is RSM's own name for the data.",
26:"No existing search found for exclusivity. Own-name page, reached from every trade and city page.",
28:"Hub page. No generic 'keywords by industry' search is proven; each trade's keyword page carries its own term, plumbing first.",
32:"Name search. No demand yet; grows with the author's public footprint.",
35:"Conversion page. No search target.",
36:"Two of three terms are weak signals only."}
names={p[0]:(p[1],p[2]) for p in PAGES}
# ---- verification
seen={}; errs=[]
for pid,kws in FINAL.items():
    if len(kws)>3: errs.append(f"page {pid} has more than 1+2 keywords")
    for k in kws:
        if k in seen: errs.append(f"DUPLICATE '{k}' on pages {seen[k]} and {pid}")
        seen[k]=pid
        if k not in res: errs.append(f"NO LIVE CHECK for '{k}' (page {pid})")
if sorted(FINAL)!=list(range(1,37)): errs.append("page ids are not 1..36")
print("verification errors:",errs or "none")
rows=[]
for pid in range(1,37):
    kws=FINAL[pid]
    if not kws: rows.append([pid,names[pid][1],names[pid][0],"none","","",NOTES.get(pid,"")]); continue
    for i,k in enumerate(kws):
        rows.append([pid,names[pid][1],names[pid][0],"main" if i==0 else "supporting",k,res[k],NOTES.get(pid,"") if i==0 else ""])
out="/home/user/rsm-engine/plan/05-keywords"; os.makedirs(out,exist_ok=True)
with open(f"{out}/keyword-map-v1.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["page","layer","page_name","role","keyword","live_evidence_22_nov_2026","note"]); w.writerows(rows)
from collections import Counter
g=Counter(r[5][:1] for r in rows if r[4]); print("grades:",dict(g),"keywords:",sum(g.values()))
json.dump(FINAL,open("final.json","w"))
