#!/usr/bin/env python3
"""Builds the WordPress import data from the approved static site, then packages the theme and plugin.

  python3 build.py          -> rsm-theme/import/site.json, dist/rsm-theme.zip, dist/rsm-elements.zip
"""
import json, re, os, sys, zipfile, shutil
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
soup = BeautifulSoup(open(os.path.join(ROOT, 'site/index.html'), encoding='utf-8').read(), 'html.parser')
DOMAIN = 'https://www.relevantsearchmedia.com'

_n = [0]
def uid():
    _n[0] += 1; return '%07x' % (0x1a2b3c + _n[0] * 7919)
def box(t=0, r=0, b=0, l=0): return {'unit': 'px', 'top': str(t), 'right': str(r), 'bottom': str(b), 'left': str(l), 'isLinked': False}
def gap(row, col=None): col = row if col is None else col; return {'unit': 'px', 'size': row, 'column': str(col), 'row': str(row), 'isLinked': row == col}
def inner(el): return el.decode_contents().strip() if el else ''
def txt(el): return ' '.join(el.get_text(' ', strip=True).split()) if el else ''
def link(u): return {'url': u or '', 'is_external': '', 'nofollow': '', 'custom_attributes': ''}

def W(kind, settings, cls='', mt=0, mb=0, eid=''):
    s = dict(settings)
    if cls: s['_css_classes'] = cls
    if mt or mb: s['_margin'] = box(mt, 0, mb, 0)
    if eid: s['_element_id'] = eid
    return {'id': uid(), 'elType': 'widget', 'widgetType': kind, 'settings': s, 'elements': []}
def H(text, tag='h2', cls='', **k):
    if cls == 'eyebrow' and 'mb' not in k: k['mb'] = 18
    return W('heading', {'title': text, 'header_size': tag}, cls, **k)
def T(html, cls='', mb=None, **k):
    if mb is None: mb = 0 if any(c in cls for c in ('lead-after', 'quote', 'rs-facts', 'rs-footer', 'rs-links', 'rs-meta')) else 20 if 'lead' in cls else 14 if 'small' in cls else 17
    return W('text-editor', {'editor': html}, cls, mb=mb, **k)
def last0(els):
    """The last text in a stack carries no bottom margin, as in the approved design."""
    if els and els[-1].get('widgetType') in ('text-editor', 'button'):
        m = els[-1]['settings'].get('_margin')
        if m: m['bottom'] = '0'
    return els
def B(text, url, cls='rsm-btn', **k): return W('button', {'text': text, 'link': link(url)}, cls, **k)
def C(children, cls='', direction='column', top=False, **s):
    st = {'content_width': 'full', 'flex_direction': direction, 'flex_gap': gap(0), **s}
    if cls: st['css_classes'] = cls
    return {'id': uid(), 'elType': 'container', 'isInner': not top, 'settings': st, 'elements': children}
def G(children, cols, tablet=None, mobile=1, g=(20, 20), cls='', mt=0, align='', **s):
    def col(v): return {'unit': 'custom', 'size': v, 'sizes': []} if isinstance(v, str) else {'unit': 'fr', 'size': v, 'sizes': []}
    st = {'container_type': 'grid', 'content_width': 'full', 'grid_columns_grid': col(cols), 'grid_rows_grid': {'unit': 'custom', 'size': 'auto', 'sizes': []},
          'grid_columns_grid_tablet': col(tablet if tablet is not None else cols), 'grid_columns_grid_mobile': col(mobile),
          'grid_rows_grid_tablet': {'unit': 'custom', 'size': 'auto', 'sizes': []}, 'grid_rows_grid_mobile': {'unit': 'custom', 'size': 'auto', 'sizes': []},
          'grid_gaps': {'unit': 'px', 'column': str(g[1]), 'row': str(g[0]), 'isLinked': g[0] == g[1]}, 'grid_auto_flow': 'row', **s}
    if align: st['grid_align_items'] = align
    if cls: st['css_classes'] = cls
    if mt: st['margin'] = box(mt, 0, 0, 0)
    return {'id': uid(), 'elType': 'container', 'isInner': True, 'settings': st, 'elements': children}
def S(children, cls='rs-sec', eid='', pad=(96, 96), pad_m=(68, 68), tag='section'):
    st = {'content_width': 'boxed', 'flex_direction': 'column', 'flex_gap': gap(0), 'html_tag': tag, 'padding': box(pad[0], 32, pad[1], 32), 'padding_mobile': box(pad_m[0], 20, pad_m[1], 20), 'css_classes': cls}
    if eid: st['_element_id'] = eid
    return {'id': uid(), 'elType': 'container', 'isInner': False, 'settings': st, 'elements': children}

def intro(sec, extra=(), mb=44):
    """eyebrow, h2 and paragraphs of a section's intro block as native widgets."""
    out = []; it = sec.select_one('.intro') or sec
    for el in it.find_all(['p', 'h2'], recursive=False):
        c = el.get('class') or []
        if 'eyebrow' in c: out.append(H(inner(el), 'p', 'eyebrow'))
        elif el.name == 'h2': out.append(H(inner(el), 'h2', mb=18))
        elif el.find('a', class_='more') and len(el.find_all()) == 1: a = el.a; out.append(B(txt(a), a['href'], 'rs-more', mb=14))
        else: out.append(T('<p>%s</p>' % inner(el), 'lead' if 'lead' in c else ('small' if 'small' in c else '')))
    out += list(extra)
    return C(last0(out), 'rs-intro rv', margin=box(0, 0, mb, 0), width={'unit': 'px', 'size': 800, 'sizes': []})

def card(variant, **f):
    s = {'variant': variant, 'svg': '', 'number': '', 'tag': '', 'status': 'green', 'title': '', 'text': '', 'link_text': '', 'link': link(''), 'highlight': ''}
    s.update(f); return W('rsm-card', s, 'rv')

# ------------------------------------------------------------------ home page
def home():
    E = []
    # hero
    h = soup.select_one('section.hero'); copy = h.select_one('.hero-copy'); acts = copy.select('.actions a')
    left = C([H(inner(copy.select_one('.eyebrow')), 'p', 'eyebrow'), H(inner(copy.h1), 'h1'), T('<p>%s</p>' % inner(copy.select_one('#answer')), 'lead', mt=24, eid='answer'),
              T('<p>%s</p>' % inner(copy.select_one('.lead-after')), 'lead-after', mt=16),
              C([B(txt(acts[0]), acts[0]['href']), B(txt(acts[1]), acts[1]['href'], 'rsm-btn rsm-btn-ghost')], 'rs-actions', 'row', flex_gap=gap(14), flex_wrap='wrap', margin=box(30, 0, 12, 0)),
              T('<p>%s</p>' % inner(copy.select_one('p.small')), 'small', mb=0), T(str(copy.select_one('ul.facts')).replace(' aria-label="Facts"', ''), 'rs-facts', mt=28)], 'rs-hero-copy', padding=box(40, 0, 48, 0), padding_tablet=box(44, 0, 0, 0))
    orbit = W('rsm-orbit', {'logo': {'url': '{{media:logo}}', 'id': '{{mediaid:logo}}'}, 'label': h.select_one('.orbit')['aria-label'], 'tiles': [dict(_id=uid(), **t) for t in json.load(open(os.path.join(HERE, 'rsm-elements/data/icons.json')))]}, 'rs-orbit-w')
    E.append(S([G([left, orbit], 'minmax(0,5.6fr) minmax(0,6.4fr)', 'minmax(0,1fr)', 'minmax(0,1fr)', g=(0, 24), cls='rs-hero-grid', align='center')], 'rs-hero', pad=(0, 0), pad_m=(0, 0)))
    # trust
    st = []
    for li in soup.select('.trust li'):
        b = li.b.extract(); a = li.find('a'); lt = lu = ''
        if a: lt, lu = txt(a), a['href']; a.extract()
        st.append(W('rsm-stat', {'number': txt(b), 'label': txt(li).rstrip(' ·').strip(), 'link_text': lt, 'link': link(lu)}))
    E.append(S([G(st, 6, 3, 2, g=(16, 24))], 'rs-trust', pad=(24, 24), pad_m=(20, 20), tag='div'))
    # film
    f = soup.select_one('#film'); it = f.select_one('.intro'); v = f.video
    chapters = W('rsm-chapters', {'label': f.select_one('.beats')['aria-label'], 'items': [{'_id': uid(), 'title': txt(b.b), 'text': txt(b.span), 'time': float(b['data-t'])} for b in f.select('.beats button')]}, mb=22)
    vo = next(x for x in json.loads(soup.find('script', type='application/ld+json').string)['@graph'] if x['@type'] == 'VideoObject')
    film = W('rsm-film', {'video': {'url': '{{media:film}}', 'id': '{{mediaid:film}}'}, 'poster': {'url': '{{media:poster}}', 'id': '{{mediaid:poster}}'}, 'captions': '{{assets}}/film-answer.vtt', 'title': v['title'], 'caption': txt(f.figcaption),
                         'fallback': txt(v), 'sound_off': 'Play with sound', 'sound_on': 'Sound on', 'roll': 'yes', 'description': vo['description'], 'transcript': vo['transcript'], 'date': vo['uploadDate'], 'duration': 58}, 'rv')
    E.append(S([G([C([H(inner(it.select_one('.eyebrow')), 'p', 'eyebrow'), H(inner(it.h2), 'h2', mb=18), chapters, T('<p>%s</p>' % inner(it.select_one('p.small')), 'small', mb=0)], 'rs-intro rv'), film],
                  'minmax(0,4.4fr) minmax(0,7.6fr)', 'minmax(0,1fr)', 'minmax(0,1fr)', g=(40, 56), align='center')], eid='film', pad=(88, 88), pad_m=(60, 60)))
    # equation
    q = soup.select_one('#equation'); hd = q.select('.eq-head > div'); bq = q.select_one('blockquote.quote')
    eq_head = G([C([H(inner(hd[0].select_one('.eyebrow')), 'p', 'eyebrow'), H(inner(hd[0].h2), 'h2')]), C(last0([T('<p>%s</p>' % inner(p), 'lead' if 'lead' in (p.get('class') or []) else '') for p in hd[1].find_all('p')]))],
                'minmax(0,6fr) minmax(0,6fr)', 'minmax(0,1fr)', 'minmax(0,1fr)', g=(24, 64), align='end', cls='rs-eq-head rv')
    eq_head['settings']['margin'] = box(0, 0, 36, 0)
    E.append(S([eq_head, W('rsm-engines', {'logo': {'url': '{{media:logo}}', 'id': '{{mediaid:logo}}'}}, 'rv', mb=28), W('rsm-lab', {'logo': {'url': '{{media:logo}}', 'id': '{{mediaid:logo}}'}}, 'rv'),
                T('<p>%s</p><footer>%s</footer>' % (inner(bq.p), inner(bq.footer)), 'quote rv', mt=56)], eid='equation'))
    # map
    m = soup.select_one('#map')
    E.append(S([intro(m), W('rsm-console', {'foot': txt(m.select_one('.console-foot'))}, 'rv')], eid='map'))
    # commitments
    c = soup.select_one('#commitments'); cl = c.select('.clauses li'); sg = c.select_one('.signed')
    E.append(S([intro(c), G([card('clause', number=txt(li.select_one('.roman')), title=inner(li.h3), text=inner(li.p)) for li in cl], 2, 2, 1, g=(22, 22)),
                W('rsm-seal', {'ring': 'IN WRITING · SIGNED BEFORE YOU PAY · ', 'name': txt(sg.select_one('.sig')), 'role': txt(sg.select_one('.signature .small')), 'note': txt(sg.find('p', class_='small'))}, 'rv', mt=30)], eid='commitments'))
    # what's wrong
    w = soup.select_one('#whats-wrong'); cards = []
    for a in w.select('a.card'):
        tag = a.select_one('.tag')
        cards.append(card('problem', svg=str(a.svg), tag=txt(tag) if tag else '', title=inner(a.h3), text=inner(a.p), link_text=txt(a.select_one('.go')), link=link(a['href']), highlight='yes' if 'feature' in a['class'] else ''))
    E.append(S([intro(w), G(cards, 3, 2, 1)], eid='whats-wrong'))
    # machine
    mc = soup.select_one('#machine')
    E.append(S([intro(mc), G([card('stat', number=txt(a.select_one('.n')), tag=txt(a.select_one('.k')), text=inner(a.select_one('.d')), link_text=txt(a.select_one('.go')), link=link(a['href'])) for a in mc.select('.stats a')], 3, 2, 1)], eid='machine'))
    # look yourself up
    lk = soup.select_one('#look'); fig = lk.select_one('figure')
    look_cards = [card('look', tag=txt(a.select_one('.status')), status='green' if 'green' in a.select_one('.status')['class'] else 'gold', title=inner(a.h3), text=inner(a.p), link_text=txt(a.select_one('.go')), link=link(a['href'])) for a in lk.select('a.card')]
    it = intro(lk, mb=0)
    E.append(S([G([it, W('rsm-us-map', {'caption': txt(fig.figcaption), 'label': fig.svg['aria-label']}, 'rv')], 'minmax(0,5fr) minmax(0,7fr)', 'minmax(0,1fr)', 'minmax(0,1fr)', g=(48, 64), align='center'), G(look_cards, 4, 2, 1, mt=48)], eid='look'))
    # record
    r = soup.select_one('#record'); rows = [{'_id': uid(), 'a': txt(tr.th), 'b': txt(tr.find_all('td')[0]), 'c': txt(tr.find_all('td')[1])} for tr in r.select('tbody tr')]; ths = r.select('thead th')
    E.append(S([intro(r), W('rsm-table', {'caption': txt(r.caption), 'h1': txt(ths[0]), 'h2': txt(ths[1]), 'h3': txt(ths[2]), 'rows': rows}, 'rv'), T('<p>%s</p>' % inner(r.select_one('.record-foot')), 'small', mt=16, mb=0)], eid='record'))
    # method
    me = soup.select_one('#method'); days = me.select('.days li'); cad = me.select('.cadence li'); acts = me.select('.actions a')
    E.append(S([intro(me), W('rsm-path', {}, 'rv', mb=28),
                G([card('day', number=txt(li.select_one('.day-n')), title=inner(li.h3), text=inner(li.p), highlight='yes' if i == len(days) - 1 else '') for i, li in enumerate(days)], 5, 2, 1, g=(16, 16)),
                G([card('cadence', number=txt(li.select_one('.k')), title=inner(li.h3), text=inner(li.p)) for li in cad], 4, 2, 1, mt=24),
                C([B(txt(acts[0]), acts[0]['href']), B(txt(acts[1]), acts[1]['href'], 'rs-more')], 'rs-actions', 'row', flex_gap=gap(14), flex_wrap='wrap', flex_align_items='center', margin=box(30, 0, 0, 0))], eid='method'))
    # services
    sv = soup.select_one('#services'); idx = sv.select('.index > div')
    def chips(d): return W('rsm-chips', {'heading': txt(d.h3), 'items': [{'_id': uid(), 'label': txt(a), 'link': link(a['href']), 'more': 'yes' if 'more' in (a.get('class') or []) else ''} for a in d.select('.chips a')]})
    E.append(S([intro(sv), G([card('service', svg=str(a.svg), title=inner(a.h3), text=inner(a.p), link=link(a['href'])) for a in sv.select('.services a')], 4, 2, 1, g=(18, 18)),
                G([chips(idx[0]), chips(idx[1])], 2, 1, 1, g=(24, 44), mt=40)], eid='services'))
    # about
    ab = soup.select_one('#about'); fg = ab.figure; right = fg.find_next_sibling('div'); ps = right.find_all('p')
    rw = [H(inner(ps[0]), 'p', 'eyebrow'), H(inner(right.h2), 'h2'), T('<p>%s</p>' % inner(ps[1]), 'lead', mt=16)] + [T('<p>%s</p>' % inner(p)) for p in ps[2:-1]] + [T('<p class="links">%s</p>' % inner(ps[-1]), 'rs-links')]
    E.append(S([G([W('rsm-portrait', {'photo': {'url': '', 'id': ''}, 'logo': {'url': '{{media:logo}}', 'id': '{{mediaid:logo}}'}, 'name': txt(fg.figcaption.b), 'caption': txt(fg.figcaption).replace(txt(fg.figcaption.b), '', 1).strip(), 'label': fg['aria-label']}, 'rv'), C(rw, 'rv')],
                  'minmax(0,5fr) minmax(0,7fr)', 'minmax(0,1fr)', 'minmax(0,1fr)', g=(56, 56), align='center')], eid='about'))
    # faq
    fq = soup.select_one('#faq'); lf = fq.select_one('.faq-grid > div'); ps = lf.find_all('p')
    items = [{'_id': uid(), 'q': txt(d.h3), 'a': '\n\n'.join(txt(p) for p in d.find_all('p'))} for d in fq.select('.faq details')]
    E.append(S([G([C([H(inner(ps[0]), 'p', 'eyebrow'), H(inner(lf.h2), 'h2'), T('<p>%s</p>' % inner(ps[1]), 'lead', mt=16), T('<p>%s</p>' % inner(ps[2]), mb=0)], 'rv'), W('rsm-faq', {'items': items, 'open_first': 'yes', 'schema': 'yes'}, 'rv')],
                  'minmax(0,4fr) minmax(0,8fr)', 'minmax(0,1fr)', 'minmax(0,1fr)', g=(48, 48), align='start')], eid='faq'))
    # closing
    cz = soup.select_one('section.closing'); acts = cz.select('.actions a'); sm = cz.select('p.small')
    E.append(S([C([W('image', {'image': {'url': '{{media:logo}}', 'id': '{{mediaid:logo}}'}, 'image_size': 'full', 'align': 'center'}, 'rs-disc', mb=26), H(inner(cz.h2), 'h2', mb=20), T('<p>%s</p>' % inner(cz.select_one('.lead')), 'lead'),
                   C([B(txt(acts[0]), acts[0]['href']), B(txt(acts[1]), acts[1]['href'], 'rsm-btn rsm-btn-ghost')], 'rs-actions', 'row', flex_gap=gap(14), flex_wrap='wrap', flex_justify_content='center', margin=box(30, 0, 12, 0)),
                   T('<p>%s</p>' % inner(sm[0]), 'small'), T('<p>%s</p>' % inner(sm[1]), 'small rs-meta', mt=40)], 'rs-closing-in', flex_align_items='center')], 'rs-closing', pad=(120, 120), pad_m=(80, 80)))
    return E

# ------------------------------------------------------------------ header, footer, menus
def menus():
    main = []
    for li in soup.select('header nav.nav > ul > li'):
        top = li.select_one('a.top'); mg = li.select_one('.mega'); cls = ' '.join(c for c in (mg.get('class') or []) if c in ('wide', 'right')) if mg else ''
        cols = [{'title': txt(mc.select_one('.mh')), 'url': '#', 'children': [{'title': txt(a.b), 'url': a['href'], 'description': txt(a.span) if a.span else ''} for a in mc.select('ul a')]} for mc in (mg.select('.mcol') if mg else [])]
        main.append({'title': txt(top), 'url': top['href'], 'classes': cls, 'children': cols})
    out = [{'name': 'RSM Main', 'slug': 'rsm-main', 'location': 'primary', 'items': main}]; foot = []
    for nav in soup.select('footer nav'):
        name = txt(nav.h2); slug = 'rsm-footer-' + re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
        out.append({'name': 'RSM Footer: ' + name, 'slug': slug, 'items': [{'title': txt(a), 'url': a['href']} for a in nav.select('ul a')]}); foot.append((name, slug))
    return out, foot

def header():
    hd = soup.select_one('header.site-header'); br = hd.select_one('.brand'); ph = hd.select_one('.phone'); cta = hd.select_one('.nav-right .btn')
    brand = W('rsm-brand', {'logo': {'url': '{{media:logo}}', 'id': '{{mediaid:logo}}'}, 'name': txt(br.select_one('.brand-name')), 'tag': txt(br.select_one('.brand-tag')), 'link': link('/')})
    right = C([B(txt(ph), ph['href'], 'rs-phone'), B(txt(cta), cta['href'], 'rsm-btn rs-cta')], 'rs-nav-right', 'row', flex_gap=gap(18), flex_align_items='center')
    bar = S([brand, W('rsm-nav', {'menu': 'rsm-main', 'label': 'Main'}), right, W('rsm-mobile-menu', {'menu': 'rsm-main', 'phone_text': 'Call ' + txt(ph), 'phone_link': link(ph['href']), 'cta_text': txt(cta), 'cta_link': link(cta['href'])})], 'rs-masthead', pad=(0, 0), pad_m=(0, 0), tag='div')
    bar['settings'].update({'flex_wrap': 'nowrap', 'flex_direction_mobile': 'row', 'flex_direction_tablet': 'row', 'flex_direction': 'row', 'flex_align_items': 'center', 'flex_justify_content': 'space-between', 'flex_gap': gap(28), 'min_height': {'unit': 'px', 'size': 74, 'sizes': []}})
    return [bar]

def footer(foot):
    ft = soup.select_one('footer.site-footer'); fb = ft.select_one('.footer-brand'); br = fb.select_one('.brand'); btm = ft.select('.footer-bottom span')
    brand = W('rsm-brand', {'logo': {'url': '{{media:logo}}', 'id': '{{mediaid:logo}}'}, 'name': txt(br.select_one('.brand-name')), 'tag': txt(br.select_one('.brand-tag')), 'link': link('/')})
    about = T(''.join(str(p) for p in fb.find_all('p')) + str(fb.address), 'rs-footer-about')
    grid = G([C([brand, about], 'footer-brand')] + [W('rsm-link-list', {'heading': n, 'menu': s}) for n, s in foot], 'minmax(0,2.2fr) repeat(5,minmax(0,1fr))', 'repeat(3,minmax(0,1fr))', 'repeat(2,minmax(0,1fr))', g=(36, 28), cls='rs-footer-grid')
    bottom = C([T('<p>%s</p>' % inner(btm[0])), T('<p>%s</p>' % inner(btm[1]))], 'footer-bottom rs-footer-bottom', 'row', flex_justify_content='space-between', flex_wrap='wrap', flex_gap=gap(10, 24), margin=box(44, 0, 0, 0))
    ph = soup.select_one('header.site-header .phone'); cta = soup.select_one('header.site-header .nav-right .btn')
    mbar = C([B('Call', ph['href'], 'rsm-btn rsm-btn-ghost'), B(txt(cta), cta['href'], 'rsm-btn')], 'rs-mobilebar', 'row', top=True)
    return [S([grid, bottom], 'rs-footer', pad=(60, 36), pad_m=(48, 30), tag='div'), mbar]

def site():
    mn, foot = menus(); head = soup.head
    graph = json.loads(soup.find('script', type='application/ld+json').string)['@graph']
    keep = [g for g in graph if g['@type'] in ('Organization', 'WebSite', 'Person', 'DefinedTerm')]
    gs = json.dumps(keep, ensure_ascii=False).replace(DOMAIN + '/assets/rsm-logo-512.png', '{{media:logo}}').replace(DOMAIN + '/assets/rsm-og.png', '{{media:og}}').replace(DOMAIN, '{{home}}')
    return {
        'version': '1.0.0',
        'media': [{'key': 'logo', 'file': 'rsm-logo-512.png', 'title': 'Relevant Search Media logo', 'alt': 'Relevant Search Media'}, {'key': 'og', 'file': 'rsm-og.png', 'title': 'Relevant Search Media share image', 'alt': 'Relevant Search Media'},
                  {'key': 'poster', 'file': 'film-answer-poster.jpg', 'title': 'Be the answer: film poster', 'alt': 'Relevance equals Read times Confirm times Choose'}, {'key': 'film', 'file': 'film-answer.mp4', 'title': 'Be the answer: film'}],
        'menus': mn,
        'options': {'elementor_disable_color_schemes': 'yes', 'elementor_disable_typography_schemes': 'yes', 'elementor_google_font': '0', 'elementor_experiment-container': 'active', 'elementor_experiment-e_optimized_markup': 'active', 'elementor_experiment-e_lazyload': 'inactive', 'elementor_lazy_load_background_images': '0', 'elementor_unfiltered_files_upload': ''},
        'kit': {
            'system_colors': [{'_id': 'primary', 'title': 'Gold', 'color': '#F8B10F'}, {'_id': 'secondary', 'title': 'Periwinkle', 'color': '#A3B5F2'}, {'_id': 'text', 'title': 'Text', 'color': '#E9EEFB'}, {'_id': 'accent', 'title': 'Teal', 'color': '#4CC0A8'}],
            'custom_colors': [{'_id': 'rsmsky', 'title': 'Sky', 'color': '#0B1033'}, {'_id': 'rsmdeep', 'title': 'Deep sky', 'color': '#060919'}, {'_id': 'rsmgold2', 'title': 'Pale gold', 'color': '#FFD98A'}, {'_id': 'rsmtext2', 'title': 'Soft text', 'color': '#B9C4EA'}, {'_id': 'rsmivory', 'title': 'Ivory', 'color': '#F6F1E6'}],
            'system_typography': [{'_id': 'primary', 'title': 'Headings', 'typography_typography': 'custom', 'typography_font_family': 'Sora', 'typography_font_weight': '700'}, {'_id': 'secondary', 'title': 'Sub headings', 'typography_typography': 'custom', 'typography_font_family': 'Sora', 'typography_font_weight': '600'},
                                  {'_id': 'text', 'title': 'Text', 'typography_typography': 'custom', 'typography_font_family': 'Plus Jakarta Sans', 'typography_font_weight': '400'}, {'_id': 'accent', 'title': 'Buttons', 'typography_typography': 'custom', 'typography_font_family': 'Plus Jakarta Sans', 'typography_font_weight': '700'}],
            'container_width': {'unit': 'px', 'size': 1296, 'sizes': []}, 'container_padding': {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': True},
            'space_between_widgets': {'unit': 'px', 'size': 0, 'column': '0', 'row': '0', 'sizes': [], 'isLinked': True}, 'active_breakpoints': ['viewport_mobile', 'viewport_tablet'], 'viewport_mobile': 760, 'viewport_tablet': 1100,
        },
        'parts': {'header': {'key': 'header', 'title': 'Site header', 'slug': 'site-header', 'data': header()}, 'footer': {'key': 'footer', 'title': 'Site footer', 'slug': 'site-footer', 'data': footer(foot)}},
        'pages': [{'key': 'home', 'title': 'Home', 'slug': 'home', 'front': True, 'seo': {'title': txt(head.title), 'description': head.find('meta', attrs={'name': 'description'})['content'], 'image': '{{media:og}}'}, 'data': home()}],
        'schema_graph': json.loads(gs),
        'llms': open(os.path.join(ROOT, 'site/llms.txt'), encoding='utf-8').read().replace(DOMAIN, '{{home}}'),
    }

def zipdir(src, dest, top):
    with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as z:
        for d, _, files in os.walk(src):
            for f in sorted(files):
                p = os.path.join(d, f)
                if f.endswith(('.DS_Store', '.pyc')): continue
                z.write(p, os.path.join(top, os.path.relpath(p, src)))

def sync_assets():
    """The theme's stylesheet is the approved site stylesheet, with font paths made relative."""
    css = open(os.path.join(ROOT, 'site/assets/site.css'), encoding='utf-8').read().replace('url(/assets/', 'url(')
    open(os.path.join(HERE, 'rsm-theme/assets/site.css'), 'w', encoding='utf-8').write(css)

if __name__ == '__main__':
    sync_assets()
    data = site()
    os.makedirs(os.path.join(HERE, 'rsm-theme/import'), exist_ok=True)
    json.dump(data, open(os.path.join(HERE, 'rsm-theme/import/site.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    def count(els): return sum(1 + count(e['elements']) for e in els)
    print('home elements:', count(data['pages'][0]['data']), '| menus:', len(data['menus']), '| main menu items:', sum(1 + sum(1 + len(c['children']) for c in t['children']) for t in data['menus'][0]['items']))
    os.makedirs(os.path.join(HERE, 'dist'), exist_ok=True); os.makedirs(os.path.join(HERE, 'rsm-theme/plugins'), exist_ok=True)
    zipdir(os.path.join(HERE, 'rsm-elements'), os.path.join(HERE, 'rsm-theme/plugins/rsm-elements.zip'), 'rsm-elements')
    shutil.copy(os.path.join(HERE, 'rsm-theme/plugins/rsm-elements.zip'), os.path.join(HERE, 'dist/rsm-elements.zip'))
    zipdir(os.path.join(HERE, 'rsm-theme'), os.path.join(HERE, 'dist/rsm-theme.zip'), 'rsm-theme')
    for f in ('rsm-theme.zip', 'rsm-elements.zip'): print(f, os.path.getsize(os.path.join(HERE, 'dist', f)) // 1024, 'KB')
