"""Live-demand checks against Google autocomplete, with a cache of raw answers."""
import json,re,time,urllib.request,urllib.parse,os
HERE=os.path.dirname(os.path.abspath(__file__))
CACHE_F=os.path.join(HERE,"evidence","google-suggest-raw.json")
OLD=os.path.join(HERE,"evidence","google-suggest-raw-2026-11-22.json")
cache=json.load(open(CACHE_F)) if os.path.exists(CACHE_F) else (json.load(open(OLD)) if os.path.exists(OLD) else {})
LIVE=set()
src=os.path.join(HERE,"..","..","seo","keyword-universe","source","google-suggestions-2026-11-18.txt")
for l in open(src):
    s,r=l.strip().split("|")
    for x in r.split(" / "):
        LIVE.add(re.sub(r"\s+"," ",(x[1:] if x.startswith("~") else (s+" "+x)).strip().lower()))
def save(): json.dump(cache,open(CACHE_F,"w"))
def suggest(q):
    if q in cache: return cache[q]
    url="https://suggestqueries.google.com/complete/search?client=firefox&hl=en&gl=us&q="+urllib.parse.quote(q)
    err=""
    for _ in range(3):
        try:
            raw=urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"}),timeout=15).read().decode("utf-8","replace")
            j=json.loads(raw); st=(j[3].get("google:suggestsubtypes",[]) if len(j)>3 else [])
            cache[q]=[[s.lower(),(st[i] if i<len(st) else [])] for i,s in enumerate(j[1])]; time.sleep(0.35); return cache[q]
        except Exception as e: err=str(e); time.sleep(2)
    return [["__ERROR__ "+err,[]]]
def norm(k): return re.sub(r"[^a-z0-9 ]","",k.lower().replace("-"," ")).strip()
def grade(k):
    sug=suggest(k)
    if sug and sug[0][0].startswith("__ERROR__"): return "X"
    n=norm(k); pre=" ".join(k.split()[:-1])
    if pre and n in [norm(s) for s,_ in suggest(pre)]: return "A"
    for s,t in sug:
        if norm(s)==n: return "A" if 512 in t else "B"
    if k.lower() in LIVE: return "A"
    if any(norm(s).startswith(n+" ") for s,_ in sug): return "C"
    return "D"
