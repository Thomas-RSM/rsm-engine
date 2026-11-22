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
            name,count,kind,desc=[x.strip() for x in line[3:].split("|")]
            cur=dict(name=name,expected=int(count),kind=kind,desc=desc,checks=[]); groups.append(cur)
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
md=["# The audit checks, written out","",
f"Version 1 draft, 22 Nov 2026. **{core} existing checks in {sum(g['kind']=='core' for g in groups)} groups, plus {new} proposed new checks in {sum(g['kind']=='new' for g in groups)} groups: {core+new} in all.**","",
"The 313 follow the group names, descriptions and counts in \"Relevant Search Media — Deliverables\" (group C, Day 3).",
"The individual checks were not itemised in any source available when this was written, so each one here is a draft",
"to be confirmed against the team's working checklist. Checks 314 onward are proposed additions.","",
"Scope: **Page** is checked on every page. **Site** is checked once for the whole site. **Beyond** is checked off the site.",
"Every check ends as pass, fail or not testable with the reason.","",
"| Group | Checks | Numbers | Status |","|---|---|---|---|"]
start=1
for g in groups:
    end=start+len(g["checks"])-1
    md.append(f'| {g["name"]} | {len(g["checks"])} | {start} to {end} | {"Existing" if g["kind"]=="core" else "Proposed"} |'); start=end+1
md.append(f"| **Total** | **{core+new}** | | |"); md.append("")
for gi,g in enumerate(groups,1):
    md+= [f'## {gi}. {g["name"]} ({len(g["checks"])})',"",g["desc"]+".","","| # | Scope | Check |","|---|---|---|"]
    for s,t in g["checks"]:
        n+=1; lab={"P":"Page","S":"Site","X":"Beyond"}[s]
        md.append(f"| {n} | {lab} | {t} |"); rows.append([n,gi,g["name"],"existing" if g["kind"]=="core" else "proposed",SCOPE[s],t])
    md.append("")
open("checks-v1.md","w",encoding="utf-8").write("\n".join(md))
with open("checks-v1.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["number","group_number","group","status","scope","check"]); w.writerows(rows)
from collections import Counter
print("OK. existing:",core,"proposed:",new,"total:",core+new,"groups:",len(groups))
print("by scope:",dict(Counter(r[4] for r in rows)))
