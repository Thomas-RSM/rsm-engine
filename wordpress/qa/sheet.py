"""sheet.py -> qa/site-records.csv : one row per live page with what it targets and how it scored. This is the file uploaded as the Google Sheet."""
import json, csv, os
D = os.path.dirname(os.path.abspath(__file__)); J = lambda f: json.load(open(os.path.join(D, f)))
R = J('pages.json'); G = J('gate-pages.json'); C = J('crawl.json') if os.path.exists(os.path.join(D, 'crawl.json')) else {'pages': {}, 'inbound': {}}
S = {k: set(v.get('shingles', [])) for k, v in R.items()}
def closest(k):
    b = ('', 0.0)
    for j in R:
        if j != k and S[k]:
            o = len(S[k] & S[j]) / len(S[k]) * 100
            if o > b[1]: b = (j, o)
    return b
sec = lambda u: 'Home' if u == '/' else {'problems': "What's wrong?", 'dsouza-equation': 'The Equation', 'elements': 'The Equation', 'services': 'Services', 'guides': 'Guides', 'industries': 'Industries', 'cities': 'Cities', 'about': "Who's behind this", 'thomas-dsouza': "Who's behind this", 'commitments': "Who's behind this", 'results': "Who's behind this", 'contact': "Who's behind this", 'privacy': 'Legal', 'terms': 'Legal'}.get(u.strip('/').split('/')[0], 'Look yourself up')
rows = []
for u in sorted(R, key=lambda x: (sec(x), x)):
    v = R[u]; st = v.get('standard', {}); cp = C['pages'].get(u, {}); cl = closest(u)
    rows.append([u, sec(u), G.get(u, {}).get('type', 'home' if u == '/' else ''), v.get('lead', ''), '; '.join(v.get('supporting', [])), v.get('title', ''), len(v.get('title', '')), v.get('description', ''), len(v.get('description', '')), v.get('h1', ''), v.get('words', ''),
                 v.get('gate', ''), st.get('pass', ''), st.get('fail', ''), st.get('nt', ''), cl[0], round(cl[1], 1), cp.get('main_imgs', ''), C['inbound'].get(u, ''), ', '.join(t for t in cp.get('types', []) if t not in ('None',)), v.get('checked', '')])
with open(os.path.join(D, 'site-records.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['Page', 'Section', 'Page type', 'Lead keyword (one page only)', 'Supporting keywords', 'Title', 'Title length', 'Meta description', 'Description length', 'H1', 'Words', 'Page gate', 'Standard checks passed', 'Standard checks failed', 'Not testable by machine', 'Closest other page', 'Shared 8-word runs %', 'Images on page', 'Body links pointing here', 'Structured data types', 'Last checked'])
    w.writerows(rows)
leads = [r[3] for r in rows if r[3]]
print(len(rows), 'rows ·', sum(1 for r in rows if r[11] == 'PASS'), 'pass ·', len(leads) - len(set(leads)), 'lead keywords used twice · highest overlap', max(r[16] for r in rows))
