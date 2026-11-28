import json,re,sys,time,urllib.request,urllib.parse,os
sys.path.insert(0,os.path.dirname(__file__))
from candidates import PAGES
REPO="/home/user/rsm-engine/seo/keyword-universe"
# 18 Nov live file
live=set()
for l in open(f"{REPO}/source/google-suggestions-2026-11-18.txt"):
    s,r=l.strip().split("|")
    for x in r.split(" / "):
        k=(x[1:] if x.startswith("~") else (s+" "+x)).strip().lower()
        live.add(re.sub(r"\s+"," ",k))
cache_f=os.path.join(os.path.dirname(__file__),"suggest_cache.json")
cache=json.load(open(cache_f)) if os.path.exists(cache_f) else {}
def suggest(q):
    if q in cache: return cache[q]
    url="https://suggestqueries.google.com/complete/search?client=firefox&hl=en&gl=us&q="+urllib.parse.quote(q)
    for attempt in range(3):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
            raw=urllib.request.urlopen(req,timeout=15).read().decode("utf-8","replace")
            j=json.loads(raw); st=(j[3].get("google:suggestsubtypes",[]) if len(j)>3 else []); res=[[s.lower(), (st[i] if i<len(st) else [])] for i,s in enumerate(j[1])]
            cache[q]=res; json.dump(cache,open(cache_f,"w")); time.sleep(0.4); return res
        except Exception as e:
            err=str(e); time.sleep(2)
    cache[q]=[["__ERROR__ "+err,[]]]; return cache[q]
def norm(k): return re.sub(r"[^a-z0-9 ]","",k.lower().replace("-"," ")).strip()
def status(k):
    sug=suggest(k)
    if sug and sug[0][0].startswith("__ERROR__"): return "CHECK FAILED",sug
    n=norm(k)
    pre=" ".join(k.split()[:-1])
    if pre:
        sp=suggest(pre)
        if n in [norm(s) for s,_ in sp]: return "A: suggested from a shorter prefix",sug
    for s,t in sug:
        if norm(s)==n:
            if 512 in t: return "A: known query (strong echo)",sug
            return "B: known query (weak echo)",sug
    if k.lower() in live: return "A: in 18 Nov live file",sug
    if any(norm(s).startswith(n+" ") for s,_ in sug): return "C: stem only (longer forms suggested)",sug
    return "D: not seen live",sug
out=[]
for pid,name,layer,kws,alts in PAGES:
    for role,k in list(zip(["main","supporting","supporting"],kws))+[("alternate",a) for a in alts]:
        st,sug=status(k)
        out.append(dict(page=pid,name=name,layer=layer,role=role,keyword=k,status=st,suggestions=[s for s,_ in sug[:8]]))
json.dump(out,open(os.path.join(os.path.dirname(__file__),"results.json"),"w"),indent=1)
from collections import Counter
print(Counter((r["role"]=="alternate",r["status"]) for r in out))
for r in out:
    print(f'{r["page"]:>2} {r["role"][:4]:4} {r["status"][:36]:36} | {r["keyword"]}')
