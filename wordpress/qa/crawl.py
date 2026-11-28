"""crawl.py -> site-wide audit of the live site, as an outside auditor would run it: every sitemap URL and every internal link.
Writes crawl.json and prints the findings."""
import re, json, sys, urllib.request, urllib.parse, collections, html
B = 'https://relevantsearchmedia.com'
def get(u, method='GET'):
    try:
        r = urllib.request.Request(u, method=method, headers={'User-Agent': 'Mozilla/5.0 (site audit)'})
        class NoRedir(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *a, **k): return None
        o = urllib.request.build_opener(NoRedir)
        with o.open(r, timeout=40) as x: return x.status, dict(x.headers), x.read().decode('utf-8', 'replace') if method == 'GET' else ''
    except urllib.error.HTTPError as e: return e.code, dict(e.headers), ''
    except Exception as e: return 0, {}, str(e)
sm = get(B + '/sitemap.xml')[2]; urls = re.findall(r'<loc>([^<]+)</loc>', sm)
pages = {}; out = collections.defaultdict(set); F = []
for u in urls:
    st, hd, body = get(u); p = urllib.parse.urlparse(u).path
    t = re.search(r'<title>(.*?)</title>', body, re.S); d = re.search(r'<meta name="description" content="([^"]*)"', body)
    can = re.search(r'<link rel="canonical" href="([^"]*)"', body); h1 = re.findall(r'<h1[^>]*>(.*?)</h1>', body, re.S)
    heads = re.findall(r'<h([1-6])[\s>]', body); imgs = re.findall(r'<img\b[^>]*>', body)
    main = re.search(r'<main.*?</main>', body, re.S); mainb = main.group(0) if main else body
    mimgs = re.findall(r'<img\b[^>]*>', mainb)
    lds = re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', body, re.S); types = []
    for l in lds:
        try:
            j = json.loads(l); types += [n.get('@type') for n in j.get('@graph', [j])]
        except Exception as e: F.append((p, 'JSON-LD does not parse: %s' % e))
    links = set(urllib.parse.urljoin(u, html.unescape(h)).split('#')[0] for h in re.findall(r'<a\b[^>]*href="([^"]+)"', body))
    inl = {l for l in links if l.startswith(B)}; out[p] = {urllib.parse.urlparse(l).path for l in inl}
    mlinks = set(urllib.parse.urlparse(urllib.parse.urljoin(u, html.unescape(h)).split('#')[0]).path for h in re.findall(r'<a\b[^>]*href="([^"]+)"', mainb) if urllib.parse.urljoin(u, h).startswith(B))
    pages[p] = dict(status=st, title=html.unescape(t.group(1).strip()) if t else '', desc=html.unescape(d.group(1)) if d else '', canonical=can.group(1) if can else '', h1=len(h1), imgs=len(imgs), main_imgs=len(mimgs),
                    noalt=sum(1 for i in imgs if 'alt=' not in i), nodim=sum(1 for i in imgs if 'width=' not in i), types=sorted(set(str(x) for x in types)), kb=round(len(body) / 1024), main_links=sorted(mlinks),
                    lang=bool(re.search(r'<html[^>]*lang="en', body)), viewport='name="viewport"' in body, noindex='noindex' in (re.search(r'<meta name="robots" content="([^"]*)"', body) or [0, ''])[1] if re.search(r'<meta name="robots"', body) else False,
                    og=all(x in body for x in ('og:title', 'og:description', 'og:image')), order_ok=all(int(b) - int(a) <= 1 for a, b in zip(heads, heads[1:])), ext=sorted(l for l in links if l.startswith('http') and not l.startswith(B)))
    if st != 200: F.append((p, 'status %s' % st))
    if can and can.group(1) != u: F.append((p, 'canonical is %s' % can.group(1)))
    if not can: F.append((p, 'no canonical'))
    if len(h1) != 1: F.append((p, '%d H1s' % len(h1)))
    if not pages[p]['order_ok']: F.append((p, 'a heading level is skipped'))
    if pages[p]['noalt']: F.append((p, '%d images without alt' % pages[p]['noalt']))
    if pages[p]['nodim']: F.append((p, '%d images without width/height' % pages[p]['nodim']))
    if not pages[p]['og']: F.append((p, 'Open Graph tags incomplete'))
    if pages[p]['noindex']: F.append((p, 'noindex'))
    for need in ('WebPage', 'BreadcrumbList'):
        if need not in pages[p]['types'] and p != '/': F.append((p, 'no %s markup' % need))
allp = set(pages); target = set().union(*out.values())
for l in sorted(target - allp):
    st, hd, _ = get(B + l)
    if st != 200: F.append((l, 'linked from %s but returns %s%s' % (sorted(k for k, v in out.items() if l in v)[:3], st, ' -> ' + hd.get('Location', '') if st in (301, 302, 308) else '')))
inb = collections.Counter(); 
for k, v in pages.items():
    for l in v['main_links']:
        if l != k: inb[l] += 1
for p in sorted(allp):
    if p != '/' and inb[p] == 0: F.append((p, 'orphan: no link from any page body'))
    elif p != '/' and inb[p] < 3: F.append((p, 'only %d body links point here' % inb[p]))
ext = collections.Counter(e for v in pages.values() for e in v['ext'])
for e in ext:
    st = get(e, 'HEAD')[0]
    if st not in (200, 301, 302, 403, 405, 999): F.append((e, 'external link returns %s' % st))
for name, want in (('/robots.txt', 'Sitemap:'), ('/llms.txt', 'Relevant Search Media'), ('/this-page-does-not-exist-xyz/', None)):
    st, hd, b = get(B + name)
    if want is None:
        if st != 404: F.append((name, 'a missing page returns %s, not 404' % st))
    elif st != 200 or want not in b: F.append((name, 'status %s or missing "%s"' % (st, want)))
for v, label in (('http://relevantsearchmedia.com/', 'http'), ('https://www.relevantsearchmedia.com/', 'www')):
    st, hd, _ = get(v)
    if st not in (301, 308) or not hd.get('Location', '').startswith(B): F.append((label, 'does not redirect in one step to %s (status %s, to %s)' % (B, st, hd.get('Location'))))
for f in ('title', 'desc'):
    c = collections.Counter(v[f] for v in pages.values())
    for x, n in c.items():
        if n > 1: F.append(('site', 'duplicate %s: %s' % (f, x[:70])))
json.dump({'pages': pages, 'findings': F, 'inbound': dict(inb)}, open('crawl.json', 'w'), indent=1)
print(len(pages), 'pages in sitemap ·', sum(v['imgs'] for v in pages.values()), 'images ·', sum(1 for v in pages.values() if v['main_imgs'] == 0), 'pages with no image in the body ·', len(F), 'findings')
for f in F: print(' -', f[0], ':', f[1])
