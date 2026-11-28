"""Collects section keywords and real questions for every page from Google autocomplete.
Run after map_v2.py: python3 woven.py"""
import csv,re,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from kwlib import suggest,save,norm
BAD=re.compile(r"\b(jobs?|salary|course|courses|certification|certificate|internship|career|careers|remote|india|delhi|noida|gurgaon|gurugram|kolkata|bangalore|bengaluru|mumbai|pune|chennai|hyderabad|ahmedabad|jaipur|lahore|karachi|islamabad|dhaka|bangladesh|nepal|sri lanka|uk|london|manchester|dubai|uae|abu dhabi|saudi|qatar|australia|melbourne|sydney|brisbane|perth|toronto|vancouver|canada|pakistan|nigeria|lagos|kenya|nairobi|philippines|singapore|malaysia|south africa|ireland|new zealand|hindi|urdu|tamil|reddit|pdf|ppt|login|meaning in|free download|template free|near me|coalition|manager|specialist|interview)\b")
QW=("how","what","why","is","are","can","does","do","should","when","which","who","will")
rows=list(csv.DictReader(open("keyword-map-v2.csv")))
locked={norm(r["keyword"]) for r in rows if r["keyword"]}
pages={}
for r in rows:
    pages.setdefault(r["url"],{"name":r["page_name"],"kws":[]})
    if r["keyword"] and r["live_grade"]!="own term": pages[r["url"]]["kws"].append(r["keyword"])
used=set(locked); out=[]
for url,p in pages.items():
    if not p["kws"]: continue
    lead=p["kws"][0]
    core=re.sub(r"^(how to|how do|how does|what is|why is|why did|is)\s+","",lead)
    sect=[];qs=[]
    def take(lst,bucket,limit,isq):
        for s,_ in lst:
            n=norm(s)
            if n in used or BAD.search(s) or len(s.split())<2: continue
            q=s.split()[0] in QW
            if q!=isq: continue
            if len(bucket)>=limit: return
            bucket.append(s); used.add(n)
    for k in p["kws"]: take(suggest(k),sect,3,False)
    for pre in ("how ","what is ","why ","is ","does ","can ","how much ","how long "):
        take(suggest(pre+core),qs,8,True)
    for k in p["kws"]: take(suggest(k),qs,8,True)
    for s in sect: out.append([url,p["name"],"section keyword",s])
    for s in qs: out.append([url,p["name"],"question",s])
save()
with open("woven-keywords-v2.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["url","page_name","role","keyword"]); w.writerows(out)
from collections import Counter
c=Counter(r[2] for r in out); pc=Counter(r[0] for r in out if r[2]=="question")
print(dict(c),"pages with questions:",len(pc),"pages with under 5 questions:",sum(1 for u,p in pages.items() if p["kws"] and pc.get(u,0)<5))
for u in list(pages)[:3]+["/services/local-seo/","/dsouza-equation/read/"]:
    print(u,[r[3] for r in out if r[0]==u][:9])
