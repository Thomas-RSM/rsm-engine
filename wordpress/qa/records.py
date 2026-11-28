#!/usr/bin/env python3
"""Refresh keyword-map.csv from pages.json (what the gate last measured on each live page)."""
import csv, json, os
H = os.path.dirname(os.path.abspath(__file__)); rec = json.load(open(os.path.join(H, 'pages.json'))); f = os.path.join(H, 'keyword-map.csv')
rows = list(csv.reader(open(f))); head, body = rows[0], rows[1:]; ix = {k: i for i, k in enumerate(head)}
for r in body:
    o = rec.get(r[ix['URL']]);
    if not o: continue
    st = o.get('standard', {}); r[ix['Status']] = 'Live, gate passed' if o.get('gate') == 'PASS' else 'Live, gate failing'
    r[ix['Standard: pass']] = st.get('pass', ''); r[ix['Standard: fail']] = st.get('fail', ''); r[ix['Standard: not testable yet']] = st.get('nt', ''); r[ix['Extra gates']] = o.get('gate', '')
    r[ix['Live title']] = o.get('title', ''); r[ix['Live description']] = o.get('description', ''); r[ix['Words']] = o.get('words', ''); r[ix['Last checked']] = o.get('checked', '')
    if r[ix['Lead keyword (one page only)']] and o.get('lead') != r[ix['Lead keyword (one page only)']].lower(): r[ix['Status']] = 'Live, to realign with the plan'
csv.writer(open(f, 'w', newline='')).writerows([head] + body)
print(sum(1 for r in body if r[ix['Status']] == 'Live, gate passed'), 'of', len(body), 'pages live and passing')
