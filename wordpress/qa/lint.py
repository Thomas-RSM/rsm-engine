"""lint.py [key…] -> checks a built page before it is published: FAQ answers 40 to 60 words, paragraphs of at most three sentences, answer block 40 to 60 words, no superlatives in prose."""
import json, re, sys, os
S = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'rsm-theme', 'import', 'site.json')))
txt = lambda h: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h)).strip()
def walk(e, out):
    for x in e if isinstance(e, list) else [e]:
        if x.get('widgetType') == 'rsm-faq':
            for it in x['settings'].get('items', []): out.append(('faq', it.get('q', ''), txt(it.get('a', ''))))
        if x.get('widgetType') == 'text-editor':
            for para in re.findall(r'<p>(.*?)</p>', x['settings'].get('editor', ''), re.S): out.append(('answer' if x['settings'].get('_element_id') == 'answer' else 'p', '', txt(para)))
        walk(x.get('elements', []), out)
bad = 0
for p in S['pages']:
    if sys.argv[1:] and p['key'] not in sys.argv[1:]: continue
    out = []; walk(p['data'], out)
    for kind, q, t in out:
        n = len(re.findall(r"[A-Za-z0-9'’]+", t));
        sents = len(re.findall(r'[.?!](?=\s|$|”)', re.sub(r'\b(Pvt|Ltd|vs|e\.g|i\.e)\.', r'\1', t)))
        if kind == 'faq' and not 40 <= n <= 60: print(p['key'], 'FAQ %d words:' % n, q); bad += 1
        if kind == 'answer' and not 40 <= n <= 62: print(p['key'], 'answer %d words' % n); bad += 1
        if kind in ('p', 'answer') and sents > 3: print(p['key'], '%d sentences:' % sents, t[:70]); bad += 1
        if kind != 'faq' and re.search(r'\b(best|leading|number one|top-rated)\b', t.lower()) and '“' not in t: print(p['key'], 'superlative:', t[:70]); bad += 1
    d = p['seo']['description']
    if not 110 <= len(d) <= 155: print(p['key'], 'description %d chars' % len(d)); bad += 1
    if not 30 <= len(p['seo']['title']) <= 60: print(p['key'], 'title %d chars' % len(p['seo']['title'])); bad += 1
print('lint:', bad, 'to fix')
