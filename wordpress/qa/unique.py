"""unique.py -> for every recorded page: the page it shares most 8-word runs with, and how much. Also flags any lead keyword, title, description or H1 used twice.
Shared service blocks marked rs-boiler (trust block, closing, hero form) are left out by the gate before the runs are recorded."""
import json, os, csv, collections
D = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(D, 'pages.json')))
S = {k: set(v.get('shingles', [])) for k, v in R.items()}
rows = []
for k in R:
    best = ('', 0.0)
    for j in R:
        if j == k or not S[k]: continue
        o = len(S[k] & S[j]) / len(S[k]) * 100
        if o > best[1]: best = (j, o)
    rows.append((k, best[0], round(best[1], 1)))
rows.sort(key=lambda r: -r[2])
dup = {}
for f in ('lead', 'title', 'description', 'h1'):
    c = collections.Counter(v.get(f, '').strip().lower() for v in R.values() if v.get(f, '').strip()); dup[f] = [x for x, n in c.items() if n > 1]
with open(os.path.join(D, 'uniqueness.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['page', 'closest other page', 'shared 8-word runs %']); w.writerows(rows)
print(len(rows), 'pages · highest overlap', rows[0], '· median', sorted(r[2] for r in rows)[len(rows) // 2])
print('over 12%:', [r for r in rows if r[2] >= 12])
print('repeated:', {k: v for k, v in dup.items()})
