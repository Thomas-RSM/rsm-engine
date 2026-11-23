"""Keyword map v2 for the foundation site map. Run: python3 map_v2.py"""
import csv,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from kwlib import grade,save
OWN="own term"  # RSM's own names: no demand expected
M={ # url: [lead, same-intent 1, same-intent 2]
"/":["seo company in usa","seo agency in usa","seo company"],
"/problems/not-showing-up-on-google/":["why is my business not showing up on google","why is my business not showing up on google maps","how to get my business on google"],
"/problems/not-getting-leads/":["how to get more leads for my business","how to get more customers for my business","how to get more leads"],
"/problems/not-recommended-by-chatgpt/":["how to get my business recommended by chatgpt","how to get my business on chatgpt","how to show up in chatgpt"],
"/problems/traffic-dropped/":["website traffic dropped suddenly","google ranking dropped dramatically","why has my website traffic dropped"],
"/problems/seo-cost/":["how much does seo cost","seo pricing","seo cost for small business"],
"/problems/":["seo problems","common seo issues","seo issues"],
"/dsouza-equation/":["d'souza equation","how do search engines rank websites","how does google rank websites"],
"/dsouza-equation/law-of-search/":["d'souza's law of search","is seo dead","future of seo"],
"/dsouza-equation/read/":["on page seo","what is on page seo","on page seo checklist"],
"/dsouza-equation/confirm/":["off page seo","what is off page seo","off page seo techniques"],
"/dsouza-equation/choose/":["conversion rate optimization","what is conversion rate optimization","conversion rate optimization examples"],
"/dsouza-equation/standard/":["seo audit","seo audit checklist","website seo audit"],
"/dsouza-equation/method/":["seo strategy","seo process","how does seo work"],
"/dsouza-equation/engines/":["ai search engines","best ai search engines","list of ai search engines"],
"/dsouza-equation/how-search-works/":["how does google search work","how do ai overviews work","how does chatgpt search work"],
"/dsouza-equation/seo-vs-aeo-vs-geo/":["seo vs geo","seo vs aeo","seo vs aeo vs geo"],
"/services/seo/":["seo services","seo services company","affordable seo services for small businesses"],
"/services/local-seo/":["local seo services","local seo agency","google maps seo"],
"/services/ai-seo/":["ai seo services","ai seo agency","ai search optimization"],
"/services/answer-engine-optimization/":["answer engine optimization","aeo services","answer engine optimization services"],
"/services/generative-engine-optimization/":["generative engine optimization","generative engine optimization agency","geo services"],
"/services/ai-overview-optimization/":["ai overview optimization","how to show up in google ai overviews","google ai overview seo"],
"/services/chatgpt-seo/":["chatgpt seo","llm seo","how to rank in chatgpt"],
"/services/google-business-profile-optimization/":["google business profile optimization","google my business optimization","google business profile management"],
"/services/technical-seo/":["technical seo","technical seo audit","schema markup services"],
"/services/content-marketing/":["content marketing agency","content marketing","seo content writing"],
"/services/link-building/":["link building services","link building agency","backlinks for seo"],
"/services/social-media-marketing/":["social media marketing services","social media optimization","social media marketing for small business"],
"/services/reputation-management/":["reputation management company","online reputation management","review management services"],
"/services/voice-search-optimization/":["voice search optimization","voice search optimization services"],
"/services/ecommerce-seo/":["ecommerce seo","ecommerce seo services","shopify seo"],
"/services/b2b-seo/":["b2b seo services","b2b seo agency","b2b seo strategy"],
"/services/small-business-seo/":["small business seo services","seo for small business","seo services for small businesses"],
"/services/lead-generation/":["lead generation services","lead generation company","lead generation for small business"],
"/services/digital-marketing/":["digital marketing services","digital marketing agency","digital marketing agency usa"],
"/services/web-design/":["web design services","web design company","website design services"],
"/services/web-development/":["web development services","web development company","custom web development"],
"/services/app-development/":["app development services","mobile app development company","app development company"],
"/services/custom-crm/":["custom crm development","custom crm software","custom crm"],
"/services/design/":["graphic design services","branding services","logo design services"],
"/services/":[],
"/guides/what-is-eeat/":["what is e-e-a-t","google e-e-a-t","e-e-a-t seo"],
"/guides/seo-keyword-research/":["seo keyword research","how to do keyword research","keyword research"],
"/guides/how-long-does-seo-take/":["how long does seo take","how long does it take to rank on google","is seo worth it"],
"/guides/how-to-choose-an-seo-company/":["how to choose an seo company","how to choose an seo agency","how to find a good seo company"],
"/guides/service-vs-ecommerce-vs-b2b-seo/":["types of seo","local seo vs seo","types of seo in digital marketing"],
"/guides/":["seo guide","seo for beginners","how to do seo"],
"/ask/":[],
"/ai-recommendation-index/":["how does chatgpt recommend businesses","how does chatgpt recommend products","how can chatgpt recommend my business"],
"/open-board/":[],
"/open-log/":["seo report example","what does an seo report look like","seo progress report"],
"/searches/":["plumber seo keywords","plumbing seo keywords"],
"/your-plan/":["seo plan","seo plan template","90 day seo plan"],
"/industries/":["seo by industry","industry specific seo","niche seo"],
"/cities/":["seo company near me","seo agency near me","seo services near me"],
"/about/":["relevant search media"],
"/thomas-dsouza/":["thomas d'souza seo"],
"/commitments/":["seo guarantee","guaranteed seo services","pay for performance seo"],
"/results/":["relevant search media reviews","seo case studies","seo results"],
"/about/editorial-policy/":[],"/about/corrections/":[],"/contact/":[],"/book/":[],"/privacy/":[],"/terms/":[],
}
OWNSET={"d'souza equation","d'souza's law of search","thomas d'souza seo"}
pages=list(csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","04-architecture","site-map.csv"))))
errs=[]; seen={}
urls={p["url"] for p in pages}
for u in M:
    if u not in urls: errs.append("not in site map: "+u)
for p in pages:
    if p["url"] not in M: errs.append("no entry for "+p["url"])
rows=[]
for p in pages:
    kws=M.get(p["url"],[])
    if len(kws)>3: errs.append("over 3 locked: "+p["url"])
    for i,k in enumerate(kws):
        if k in seen: errs.append(f"DUPLICATE '{k}': {seen[k]} and {p['url']}")
        seen[k]=p["url"]
        g=OWN if k in OWNSET else grade(k)
        rows.append([p["number"],p["layer"],p["page"],p["url"],"lead" if i==0 else "same intent",k,g])
    if not kws: rows.append([p["number"],p["layer"],p["page"],p["url"],"none","",""])
save()
if errs: print("FAILED",*errs,sep="\n  "); sys.exit(1)
with open("keyword-map-v2.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["page","layer","page_name","url","role","keyword","live_grade"]); w.writerows(rows)
from collections import Counter
print("locked keywords:",sum(1 for r in rows if r[5]),"grades:",dict(Counter(r[6] for r in rows if r[5])))
for r in rows:
    if r[6] in ("C","D","X","B"): print(" ",r[6],r[3],"|",r[5])
