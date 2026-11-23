"""Builds the numbered check list from the two source files and verifies the counts.
Run: python3 build_checks.py   (from this folder)"""
import csv,re,sys
SCOPE={"P":"Every page","S":"Whole site","X":"Beyond the site"}
groups=[];cur=None
for f in ("checks-source-part1.txt","checks-source-part2.txt"):
    for line in open(f,encoding="utf-8"):
        line=line.rstrip("\n")
        if not line.strip(): continue
        if line.startswith("## "):
            name,count,kind,desc,term=[x.strip() for x in line[3:].split("|")]
            cur=dict(name=name,expected=int(count),kind=kind,desc=desc,term=term,checks=[]); groups.append(cur)
        else:
            s,t=line.split("|",1); assert s in SCOPE,line
            cur["checks"].append((s,t.strip()))
errs=[]
for g in groups:
    if len(g["checks"])!=g["expected"]: errs.append(f'{g["name"]}: {len(g["checks"])} written, {g["expected"]} expected')
texts=[t.lower() for g in groups for _,t in g["checks"]]
dups={t for t in texts if texts.count(t)>1}
if dups: errs.append(f"duplicate checks: {dups}")
core=sum(len(g["checks"]) for g in groups if g["kind"]=="core")
new=sum(len(g["checks"]) for g in groups if g["kind"]=="new")
if core!=313: errs.append(f"core total is {core}, not 313")
if errs: print("FAILED:",*errs,sep="\n  "); sys.exit(1)
rows=[];n=0
TERMS=["Question","Read","Confirm","Choose"]
tcount={t:sum(len(g["checks"]) for g in groups if g["term"]==t) for t in TERMS}
md=["# The D'Souza Standard","",
f"Version 1.0, 23 Nov 2026. **{core+new} checks in {len(groups)} groups.** The list is open: checks are added as search changes, and each addition gets a version and a date.","",
"The standard is the D'Souza Equation written out as checks: **Relevance = Read × Confirm × Choose**, for every question in the customer's search map.","",
"| Part of the equation | What it asks | Checks |","|---|---|---|",
f"| The question | Is every search a customer makes mapped and assigned to a page? | {tcount['Question']} |",
f"| Read | Can every engine read plainly what the business is and what it answers? | {tcount['Read']} |",
f"| Confirm | Do independent sources say the same thing? | {tcount['Confirm']} |",
f"| Choose | Do real people, and the engines, choose it? | {tcount['Choose']} |",
f"| **Total** | | **{core+new}** |","",
"RSM's free report runs about 30 of these. Every client's audit runs all of them.","",
"Checks 1 to 313 follow the group names and counts of the audit described in \"Relevant Search Media — Deliverables\". Their wording was written out on 22 Nov 2026. Checks 314 onward were added on that date.","",
"Scope: **Page** is checked on every page. **Site** is checked once for the whole site. **Beyond** is checked off the site.",
"Every check ends as pass, fail or not testable with the reason.","",
"| Group | Equation | Checks | Numbers |","|---|---|---|---|"]
start=1
for g in groups:
    end=start+len(g["checks"])-1
    md.append(f'| {g["name"]} | {g["term"]} | {len(g["checks"])} | {start} to {end} |'); start=end+1
md.append(f"| **Total** | | **{core+new}** | |"); md.append("")
for gi,g in enumerate(groups,1):
    md+= [f'## {gi}. {g["name"]} ({len(g["checks"])}) · {g["term"]}',"",g["desc"]+".","","| # | Scope | Check |","|---|---|---|"]
    for s,t in g["checks"]:
        n+=1; lab={"P":"Page","S":"Site","X":"Beyond"}[s]
        md.append(f"| {n} | {lab} | {t} |"); rows.append([n,gi,g["name"],g["term"],SCOPE[s],t])
    md.append("")
open("dsouza-standard.md","w",encoding="utf-8").write("\n".join(md))
with open("dsouza-standard.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["number","group_number","group","equation_term","scope","check"]); w.writerows(rows)
from collections import Counter
print("OK. total:",core+new,"groups:",len(groups),"by term:",tcount)
print("by scope:",dict(Counter(r[4] for r in rows)))
