#!/usr/bin/env python3
"""The page gate. One live page in, a verdict out.

  gate.py <path such as /problems/> --keywords "lead;support 1;support 2" [--base https://relevantsearchmedia.com]

Part 1 runs the 413-check D'Souza Standard (site/tools/check_page.py) on the page as served.
Part 2 runs the extra gates the Standard does not measure from HTML alone: keyword density,
cannibalisation and duplication against every other published page, image weight, page weight,
response time, titles and descriptions unique site-wide, broken internal links.
Part 3 (gate_render.js) loads the page in a browser at desktop, laptop, tablet and phone sizes.
Exit code 0 only when nothing fails.
"""
import sys, os, re, json, subprocess, time, urllib.request, urllib.error, tempfile, hashlib
from html.parser import HTMLParser
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
CHECKER = os.path.join(REPO, 'site', 'tools', 'check_page.py')
RECORDS = os.path.join(HERE, 'pages.json')
UA = {'User-Agent': 'Mozilla/5.0 (rsm-gate)', 'Accept-Encoding': 'identity'}

def get(url, method='GET'):
    t = time.time()
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=UA, method=method), timeout=40); body = r.read() if method == 'GET' else b''
        return r.status, body, dict(r.headers), time.time() - t
    except urllib.error.HTTPError as e: return e.code, b'', dict(e.headers), time.time() - t
    except Exception as e: return 0, str(e).encode(), {}, time.time() - t

class Text(HTMLParser):
    def __init__(s): super().__init__(); s.main = 0; s.skip = 0; s.out = []; s.boil = 0; s.uniq = []; s.title = ''; s._t = 0; s.h = []; s._h = None; s.imgs = []; s.links = []; s.desc = ''; s.canon = ''; s.robots = ''
    def handle_starttag(s, tag, a):
        a = dict(a)
        if tag == 'main': s.main = 1
        if s.boil and tag == 'div': s.boil += 1
        if not s.boil and tag == 'div' and 'rs-boiler' in (a.get('class') or ''): s.boil = 1
        if tag in ('script', 'style', 'svg', 'noscript', 'template', 'select'): s.skip += 1
        if tag == 'ol' and 'std-list' in (a.get('class') or ''): s.skip += 1; s.std = 1
        if tag == 'ul' and 'el-list' in (a.get('class') or ''): s.skip += 1; s.ell = 1
        if tag == 'title' and not s.skip and not s.title: s._t = 1
        if tag in ('h1', 'h2', 'h3'): s._h = [tag, '']
        if tag == 'img': s.imgs.append(a)
        if tag == 'a' and a.get('href'): s.links.append(a['href'])
        if tag == 'meta' and a.get('name') == 'description': s.desc = a.get('content', '')
        if tag == 'meta' and a.get('name') == 'robots': s.robots = a.get('content', '')
        if tag == 'link' and a.get('rel') == 'canonical': s.canon = a.get('href', '')
    def handle_endtag(s, tag):
        if tag in ('script', 'style', 'svg', 'noscript', 'template', 'select'): s.skip = max(0, s.skip - 1)
        if tag == 'ol' and getattr(s, 'std', 0): s.skip = max(0, s.skip - 1); s.std = 0
        if tag == 'ul' and getattr(s, 'ell', 0): s.skip = max(0, s.skip - 1); s.ell = 0
        if tag == 'title': s._t = 0
        if tag in ('h1', 'h2', 'h3') and s._h: s.h.append((s._h[0], ' '.join(s._h[1].split()))); s._h = None
        if tag == 'main': s.main = 0
        if s.boil and tag == 'div': s.boil -= 1
    def handle_data(s, d):
        if s._t: s.title += d
        if s.skip: return
        if s._h: s._h[1] += d
        if s.main: s.out.append(d)
        if s.main and not s.boil: s.uniq.append(d)

def parse(html):
    p = Text(); p.feed(html); p.text = ' '.join(' '.join(p.out).split()); p.own = ' '.join(' '.join(p.uniq).split()); return p

def words(t): return re.findall(r"[a-z0-9']+", t.lower().replace('’', "'"))
def shingles(t, n=8):
    w = words(t); return {' '.join(w[i:i + n]) for i in range(0, max(0, len(w) - n + 1))}

def main():
    a = sys.argv[1:]; path = a[0]; base = 'https://relevantsearchmedia.com'; kws = []
    if '--base' in a: base = a[a.index('--base') + 1].rstrip('/')
    if '--keywords' in a: kws = [k.strip() for k in a[a.index('--keywords') + 1].split(';') if k.strip()]
    lead = kws[0].lower() if kws else ''; fails = []; notes = []
    def gate(name, ok, detail=''):
        (notes if ok else fails).append(f"{'PASS' if ok else 'FAIL'} · {name}" + (f" · {detail}" if detail else ''))
    url = base + path
    st, body, hd, dt = get(url + ('&' if '?' in url else '?') + 'gate=' + str(int(time.time())))
    gate('page answers 200', st == 200, f'{st}')
    if st != 200: print('\n'.join(fails)); return 1
    html = body.decode('utf-8', 'replace'); p = parse(html)
    # ---------- part 1: the Standard ----------
    d = tempfile.mkdtemp(prefix='gate-')
    local = re.sub(r'(<a\b[^>]*?\shref=["\'])' + re.escape(base) + r'/', r'\1/', html)   # links as paths; canonical, og and schema stay absolute
    local = re.sub(r'<style\b[^>]*>.*?</style>', '', local, flags=re.S)
    local = re.sub(r'<script\b(?![^>]*ld\+json)([^>]*)>.*?</script>', r'<script\1></script>', local, flags=re.S)
    fp = os.path.join(d, path.strip('/'), 'index.html') if path != '/' else os.path.join(d, 'index.html'); os.makedirs(os.path.dirname(fp), exist_ok=True); open(fp, 'w', encoding='utf-8').write(local)
    for src, dst in (('/robots.txt', 'robots.txt'), ('/llms.txt', 'llms.txt'), ('/sitemap.xml', 'sitemap.xml')):
        s2, b2, _, _ = get(base + src); open(os.path.join(d, dst), 'wb').write(b2 if s2 == 200 else b'')
    os.makedirs(os.path.join(d, 'assets'), exist_ok=True)
    for f in ('site.css', 'site.js'):
        src = os.path.join(REPO, 'wordpress', 'rsm-theme', 'assets', f)
        if os.path.exists(src): open(os.path.join(d, 'assets', f), 'w', encoding='utf-8').write(open(src, encoding='utf-8').read() + (open(os.path.join(REPO, 'wordpress', 'rsm-theme', 'assets', 'wp.css'), encoding='utf-8').read() if f == 'site.css' else ''))
    out = os.path.join(d, 'result.json')
    arg = lambda k, dflt=None: a[a.index(k) + 1] if k in a else dflt
    mt = re.search(r'Last reviewed\s+(\d{1,2})\s(\w{3})\w*\s(\d{4})', p.text); mon = dict(Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6, Jul=7, Aug=8, Sep=9, Oct=10, Nov=11, Dec=12)
    cfg = {'host': base, 'cwv_lab': False, 'lead': lead, 'no_lead': not lead}
    if arg('--trade'): cfg['trade_words'] = [x for x in arg('--trade').split(';') if x]
    if mt: cfg['modified'] = '%s-%02d-%02d' % (mt.group(3), mon.get(mt.group(2), 0), int(mt.group(1))); cfg['modified_text'] = '%d %s %s' % (int(mt.group(1)), mt.group(2), mt.group(3))
    rng = {'home': [1500, 3500], 'hub': [600, 2200], 'problem': [900, 2600], 'pillar': [1200, 3200], 'service': [900, 2600], 'tool': [300, 8000], 'reference': [1200, 14000], 'about': [500, 2400], 'legal': [300, 4000]}
    cfg['words'] = rng.get(arg('--type', 'home'), [300, 3200])
    if arg('--example'): cfg['example'] = arg('--example')
    if arg('--original'): cfg['original'] = [x for x in arg('--original').split(';') if x]
    for _ in range(3): get(url)   # measure the page as visitors get it: from a warm cache
    rr = subprocess.run(['node', os.path.join(HERE, 'gate_render.js'), url], capture_output=True, text=True); render = {}
    try: render = json.loads(rr.stdout.strip().splitlines()[-1])
    except Exception: fails.append('FAIL · browser run did not finish · ' + (rr.stderr or rr.stdout)[-200:])
    for vp, v in render.get('sizes', {}).items():
        gate(f'{vp}: no sideways scroll', v['dw'] <= v['vw'] + 1, f"{v['dw']} vs {v['vw']}"); gate(f'{vp}: no script errors', not v['errors'], '; '.join(v['errors'])[:160]); gate(f'{vp}: no failed files', not v['bad'], '; '.join(v['bad'])[:160]); gate(f'{vp}: no broken images', v['broken'] == 0, str(v['broken']))
    if render.get('sizes'):
        ph = render['sizes'].get('phone', {}); dk = render['sizes'].get('desktop', {})
        gate('phone: no text under 12px in the copy', ph.get('small', 0) == 0, str(ph.get('small'))); gate('desktop: largest paint under 2.5 s', dk.get('lcp', 9e9) < 2500, f"{dk.get('lcp')} ms"); gate('phone: largest paint under 2.5 s', ph.get('lcp', 9e9) < 2500, f"{ph.get('lcp')} ms")
        gate('layout shift under 0.1 at every size', all(v.get('cls', 1) < 0.1 for v in render['sizes'].values()), ', '.join(f"{k} {v.get('cls')}" for k, v in render['sizes'].items()))
        cfg['cwv_lab'] = dk.get('lcp', 9e9) < 2500 and ph.get('lcp', 9e9) < 2500 and all(v.get('cls', 1) < 0.1 for v in render['sizes'].values())
    r = subprocess.run([sys.executable, '-I', CHECKER, d, path, '--keywords', ';'.join(kws) or 'relevant search media', '--json', out], capture_output=True, text=True, env=dict(os.environ, RSM_GATE_CFG=json.dumps(cfg)))
    print(r.stdout.strip() or r.stderr.strip()[-800:])
    std = json.load(open(out)) if os.path.exists(out) else {'results': {}, 'stats': {}}
    sfail = [n for n, v in std['results'].items() if v['status'] == 'FAIL']
    gate('D\'Souza Standard: no failed check', not sfail and bool(std['results']), f"{len(sfail)} failed" if sfail else f"{sum(1 for v in std['results'].values() if v['status']=='PASS')} pass")
    # ---------- part 2: extra gates ----------
    w = words(p.text); n = len(w)
    if lead:
        kwset = {lead, lead.replace(' in usa', ' in the usa'), lead.replace(' in usa', ' in the united states')}; kwset |= {x[:-1] for x in kwset if x.endswith('s') and not x.endswith('ss')} | {x + 's' for x in kwset if not x.endswith('s')}
        forms = [words(v) for v in kwset]; lw = words(lead)
        hits = sum(1 for i in range(n) for f in forms if w[i:i + len(f)] == f); dens = 100.0 * hits * len(lw) / max(1, n)
        gate('lead keyword present in copy', hits >= 1, f'{hits} uses in {n} words')
        gate('lead keyword density at or under 2%', dens <= 2.0, f'{dens:.2f}%')
        gate('lead keyword in title', all(x in p.title.lower().replace('’', "'") for x in lw), p.title.strip()[:70])
        first = w[:110]; gate('lead keyword in the first 100 words', any(first[i:i + len(f)] == f for i in range(len(first)) for f in forms), ' '.join(first[:14]) + '…')
        h2s = [words(x) for k, x in p.h if k == 'h2']; gate('lead keyword in one H2', any(hh[i:i + len(f)] == f for hh in h2s for i in range(len(hh)) for f in forms), f'{len(h2s)} H2s')
        h1 = [t for k, t in p.h if k == 'h1']; hw = words(h1[0]) if h1 else []; gate('one H1, carrying the lead keyword', len(h1) == 1 and (any(hw[i:i + len(f)] == f for i in range(len(hw)) for f in forms) or all(x in hw for x in lw)), ' | '.join(h1)[:90])
        top = Counter_top(w); gate('no single content word over 3% of the copy', top[1] <= 3.0, f'{top[0]} {top[1]:.2f}%')
    gate('title 30 to 60 characters', 30 <= len(p.title.strip()) <= 60, f'{len(p.title.strip())}')
    gate('description 110 to 155 characters', 110 <= len(p.desc) <= 155, f'{len(p.desc)}')
    gate('canonical points to itself', p.canon.rstrip('/') == url.rstrip('/'), p.canon)
    gate('indexable', 'noindex' not in p.robots, p.robots)
    gate('at least 300 words of copy', n >= 300, f'{n}')
    # against every other recorded page
    rec = json.load(open(RECORDS)) if os.path.exists(RECORDS) else {}
    mine = shingles(p.own); worst = ('', 0.0)
    for op, o in rec.items():
        if op == path: continue
        if lead and o.get('lead', '').lower() == lead: fails.append(f"FAIL · cannibalisation · {op} already targets “{lead}”")
        if o.get('title', '').strip().lower() == p.title.strip().lower(): fails.append(f"FAIL · duplicate title with {op}")
        if o.get('description', '') and o['description'] == p.desc: fails.append(f"FAIL · duplicate description with {op}")
        osh = set(o.get('shingles', []))
        if osh and mine:
            j = len(mine & osh) / max(1, min(len(mine), len(osh)))
            if j > worst[1]: worst = (op, j)
    gate('copy shared with any other page under 12%', worst[1] < 0.12, f'{worst[0] or "no other page"} {worst[1] * 100:.1f}%')
    # images
    big = []; noalt = [i.get('src', '')[-40:] for i in p.imgs if i.get('alt') is None]; nodim = [i.get('src', '')[-40:] for i in p.imgs if not (i.get('width') and i.get('height'))]
    for i in p.imgs:
        src = i.get('src', '');
        if not src or src.startswith('data:'): continue
        s3, _, h3, _ = get(src if src.startswith('http') else base + src, 'HEAD'); size = int(h3.get('Content-Length', 0) or 0)
        if s3 != 200: fails.append(f'FAIL · image missing · {src[-60:]} {s3}')
        elif size > 200_000: big.append(f'{src[-40:]} {size // 1024} KB')
    gate('every image under 200 KB', not big, '; '.join(big)); gate('every image has alt text', not noalt, '; '.join(noalt)); gate('every image has width and height', not nodim, '; '.join(nodim))
    gate('HTML under 250 KB', len(body) < 250_000, f'{len(body) // 1024} KB')
    best = min(get(url)[3] for _ in range(4))
    gate('cached response under 0.8 s (best of four)', best < 0.8, f'{best:.2f}s')
    # internal links
    seen = set(); broken = []; external = set()
    for l in p.links:
        if l.startswith(('#', 'tel:', 'mailto:')): continue
        full = l if l.startswith('http') else base + l
        if not full.startswith(base): external.add(full.split('/')[2] if '//' in full else full); continue
        full = full.split('#')[0]
        if full in seen: continue
        seen.add(full); s4, _, _, _ = get(full, 'HEAD')
        if s4 >= 400 or s4 == 0: broken.append(full.replace(base, ''))
    known_missing = {k for k in broken}
    planned = set(json.load(open(os.path.join(HERE, 'planned.json')))) if os.path.exists(os.path.join(HERE, 'planned.json')) else set()
    real = sorted(b for b in broken if b not in planned)
    gate('no broken internal link (pages still to be built are listed, not failed)', not real, ', '.join(real[:8]))
    notes.append(f'INFO · links to pages not built yet: {len(broken) - len(real)}')
    # record
    rec[path] = {'lead': lead, 'supporting': kws[1:], 'title': p.title.strip(), 'description': p.desc, 'h1': next((t for k, t in p.h if k == 'h1'), ''), 'words': n, 'shingles': sorted(mine)[:6000],
                 'standard': {'pass': sum(1 for v in std['results'].values() if v['status'] == 'PASS'), 'fail': len(sfail), 'nt': sum(1 for v in std['results'].values() if v['status'] == 'N/T')}, 'checked': time.strftime('%Y-%m-%d %H:%M'), 'gate': 'PASS' if not fails else 'FAIL'}
    json.dump(rec, open(RECORDS, 'w'), indent=0)
    print('\n'.join(notes)); print('\n'.join(fails)); print(f"\nGATE {'PASS' if not fails else 'FAIL'} · {path} · {len(notes)} passed · {len(fails)} failed")
    return 1 if fails else 0

def Counter_top(w):
    from collections import Counter
    stop = set("the a an and or of to in on for with by is are be as at it its that this from you your we our they their i he she his her them us not no do does did can will would should what which who how why when where if then than so but into out up about more most each every all any one two own over under was were been has have had".split())
    c = Counter(x for x in w if x not in stop and len(x) > 2); t, k = c.most_common(1)[0] if c else ('', 0); return t, 100.0 * k / max(1, len(w))

if __name__ == '__main__': sys.exit(main())
