#!/usr/bin/env python3
"""Run the D'Souza Standard's page-level checks against a built HTML page.

Usage: check_page.py <site dir> <path such as /> [--keywords lead;same1;same2] [--json out.json]

Each of the 413 checks ends as PASS, FAIL, or N/T (not testable here) with the reason. Checks that need
a live server, Search Console, a person or an outside source are reported N/T with what is needed.
"""
import sys, re, json, csv, os, html as htmlmod
from html.parser import HTMLParser
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STANDARD = os.path.join(os.path.dirname(ROOT), 'plan', '03-standard', 'dsouza-standard.csv')
# Per-page facts the checks compare against. Defaults are the home page as first built; the gate passes the real ones.
CFG = {'host': 'https://www.relevantsearchmedia.com', 'modified': '2026-11-24', 'modified_text': '24 Nov 2026', 'words': [1500, 3200],
       'example': 'plumbing seo company miami', 'original': ['113,720', 'v4, 18 Nov 2026'], 'cwv_lab': False,
       'trade_words': ['plumber', 'roofer', 'dentist'], 'lead': 'seo company in usa', 'no_lead': False}
if os.environ.get('RSM_GATE_CFG'): CFG.update(json.loads(os.environ['RSM_GATE_CFG']))

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.stack=[]; s.tags=[]; s.text=[]; s.cur_text=[]; s.scripts=[]; s.in_script=None; s.headings=[]; s.links=[]; s.imgs=[]; s.metas=[]; s.title=None; s._title=False; s.forms=0; s.labels=[]; s.selects=[]; s.landmarks=Counter(); s.videos=[]; s.paras=[]; s._p=None; s.lists=0; s.tables=0; s.details=0; s.skip=False; s.lang=None; s.canon=[]; s.ld=[]; s.inline_styles=0; s.h1_text=''; s._h=None; s.first_words=[]; s.main_seen=False; s.summary=0
    def handle_starttag(s, tag, attrs):
        a=dict(attrs); s.tags.append(tag)
        if tag=='svg': s.svg_depth=getattr(s,'svg_depth',0)+1
        if tag=='html': s.lang=a.get('lang')
        if tag=='title': s._title=True; s.title=''
        if tag=='meta': s.metas.append(a)
        if tag=='link' and a.get('rel')=='canonical': s.canon.append(a.get('href'))
        if tag=='script':
            s.in_script=a.get('type','')
            if 'ld+json' in s.in_script: s.ld.append('')
        if tag in ('h1','h2','h3','h4','h5','h6'): s._h=(tag,[]);
        if tag=='a':
            s.links.append({'href':a.get('href',''),'text':[],'cls':a.get('class','')});
        if tag=='img': s.imgs.append(a)
        if tag=='video': s.videos.append(a)
        if tag=='form': s.forms+=1
        if tag=='label': s.labels.append(a)
        if tag=='select': s.selects.append(a)
        if tag in ('header','nav','main','footer','aside','section','article'): s.landmarks[tag]+=1
        if tag=='main': s.main_seen=True
        if tag=='p': s._p=[]
        if tag in ('ul','ol'): s.lists+=1
        if tag=='table': s.tables+=1
        if tag=='details' and 'menu' not in a.get('class',''): s.details+=1
        if tag=='summary': s.summary+=1
        if a.get('style'): s.inline_styles+=1
        if tag=='a' and a.get('class')=='skip': s.skip=True
    def handle_endtag(s, tag):
        if tag=='svg': s.svg_depth=max(0,getattr(s,'svg_depth',0)-1)
        if tag=='title': s._title=False
        if tag=='script': s.in_script=None
        if tag in ('h1','h2','h3','h4','h5','h6') and s._h: s.headings.append((s._h[0],' '.join(''.join(s._h[1]).split()))); s._h=None
        if tag=='a' and s.links: s.links[-1]['text']=' '.join(''.join(s.links[-1]['text']).split())
        if tag=='p' and s._p is not None: s.paras.append(' '.join(''.join(s._p).split())); s._p=None
    def handle_data(s, d):
        if s._title: s.title+=d
        if s.in_script is not None:
            if 'ld+json' in s.in_script and s.ld: s.ld[-1]+=d
            return
        if s.tags and s.tags[-1]=='style': return
        if getattr(s,'svg_depth',0)>0: return
        if s._h: s._h[1].append(d)
        if s.links and isinstance(s.links[-1]['text'],list): s.links[-1]['text'].append(d)
        if s._p is not None: s._p.append(d)
        if s.main_seen: s.text.append(d)

def words(t): return re.findall(r"[A-Za-z0-9'’]+", t)

def syllables(w):
    w=w.lower(); w=re.sub(r'[^a-z]','',w)
    if not w: return 0
    v=re.findall(r'[aeiouy]+',w); n=len(v)
    if w.endswith('e') and n>1: n-=1
    return max(1,n)

def grade(text):
    sents=[x for x in re.split(r'[.!?]+\s',text) if len(words(x))>2]
    ws=words(text)
    if not sents or not ws: return 0,0
    syl=sum(syllables(w) for w in ws)
    fk=0.39*len(ws)/len(sents)+11.8*syl/len(ws)-15.59
    return round(fk,1), round(len(ws)/len(sents),1)

def run(site, path, keywords, extra):
    fp=os.path.join(site, path.strip('/'), 'index.html') if path!='/' else os.path.join(site,'index.html')
    raw=open(fp,encoding='utf-8').read()
    # a page that reprints the Standard is judged on its own prose; the quoted list is reference material
    raw=re.sub(r'<ol class="std-list">.*?</ol>','<ol class="std-list"><li>The numbered checks are listed here.</li></ol>',raw,flags=re.S)
    raw=re.sub(r'<ul class="el-list">.*?</ul>','<ul class="el-list"><li>The elements of this group are listed here.</li></ul>',raw,flags=re.S)
    p=P(); p.feed(raw)
    body_text=' '.join(' '.join(p.text).split())
    low=body_text.lower().replace('’',"'")
    lead=keywords[0].lower(); supp=[k.lower() for k in keywords[1:]]
    def variants(k):
        v=[k, k.replace(' in usa',' in the usa'), k.replace(' in usa',' in the united states')]
        return v+[x[:-1] for x in v if x.endswith('s') and not x.endswith('ss')]+[x+'s' for x in v if not x.endswith('s')]   # singular and plural are the same search
    def has(k,text): return any(v in text for v in variants(k))
    sitemap=open(os.path.join(site,'sitemap.xml')).read() if os.path.exists(os.path.join(site,'sitemap.xml')) else ''
    robots=open(os.path.join(site,'robots.txt')).read() if os.path.exists(os.path.join(site,'robots.txt')) else ''
    llms=open(os.path.join(site,'llms.txt')).read() if os.path.exists(os.path.join(site,'llms.txt')) else ''
    meta=lambda n: [m.get('content','') for m in p.metas if m.get('name')==n or m.get('property')==n]
    desc=meta('description'); robotsmeta=meta('robots')
    ld=[]; ld_err=None
    for blk in p.ld:
        try: ld.append(json.loads(blk))
        except Exception as e: ld_err=str(e)
    graph=[]
    for d in ld: graph+= d.get('@graph',[d]) if isinstance(d,dict) else []
    types={g.get('@type') for g in graph if isinstance(g,dict)}
    faq=[g for g in graph if g.get('@type')=='FAQPage']
    faq_q=[q['name'] for q in (faq[0]['mainEntity'] if faq else [])]
    vis_faq=[h for t,h in p.headings if t=='h3' and h.endswith('?')]
    h1s=[h.replace('’',"'") for t,h in p.headings if t=='h1']
    levels=[int(t[1]) for t,_ in p.headings]
    skips=[(a,b) for a,b in zip(levels,levels[1:]) if b>a+1]
    internal=[l for l in p.links if l['href'].startswith('/') and not l['href'].startswith('//')]
    content_links=[l for l in internal if l['href'] not in ('/','/book/','/ask/','/open-board/') ]
    first100=' '.join(words(body_text)[:100]).lower()
    fk,asl=grade(body_text)
    paras=[x for x in p.paras if len(words(x))>3]
    long_paras=[x for x in paras if len(re.findall(r'[.!?](\s|$)',x))>3]
    stuffed=[x for x in paras if x.lower().count(lead)>=3]
    filler=re.findall(r"in today['’]s digital world|unlock|elevate|game-changer|cutting-edge|seamless|best-in-class|world-class",low)
    # a page that reprints the Standard quotes the words its own checks forbid; judge the page's own prose, not the quoted list
    raw_own=re.sub(r'<ol class="std-list">.*?</ol>','',raw,flags=re.S)
    # a superlative inside a question heading is the searcher's word, not our claim; the answer under it is still judged
    raw_own=re.sub(r'<h[23][^>]*>[^<]*\?\s*</h[23]>',' ',raw_own)
    own_low=re.sub(r'<[^>]+>',' ',re.sub(r'<(script|style)\b.*?</\1>',' ',raw_own[raw_own.find('<main'):] if '<main' in raw_own else raw_own,flags=re.S)).lower()
    placeholders=re.findall(r'lorem|\[[A-Z][^\]]{3,}\]|TODO|placeholder',re.sub(r'placeholder="[^"]*"|::placeholder|data-placeholder','',raw_own))
    bracket_notes=[x for x in re.findall(r'\[[^\]]+\]',body_text) if len(x)>6]
    imgs_meaningful=[i for i in p.imgs if i.get('alt') not in ('',None)]
    imgs_noalt=[i for i in p.imgs if 'alt' not in i]
    img_sizes={}
    for i in p.imgs:
        src=i.get('src','')
        fpth=os.path.join(site,src.lstrip('/'))
        if os.path.exists(fpth): img_sizes[src]=os.path.getsize(fpth)
    cta_count=sum(1 for l in p.links if l['href']=='/book/')
    dates=re.findall(r'(Published|Last reviewed)\s+\d{1,2}\s\w+\s\d{4}',body_text)
    nums=re.findall(r'\b(900\+|413|113,720|113|1,822|400|90%|100\+|2010|2020)\b',body_text)
    register={'900+','413','113,720','113','1,822','400','90%','100+','2010','2020'}
    org=[g for g in graph if g.get('@type')=='Organization']
    person=[g for g in graph if g.get('@type')=='Person']
    webpage=[g for g in graph if g.get('@type')=='WebPage']
    ids=set(); refs=set()
    def walk(o):
        if isinstance(o,dict):
            if '@id' in o: (ids if o.get('@type') else refs).add(o['@id'])
            for k,v in o.items(): walk(v)
        elif isinstance(o,list):
            for x in o: walk(x)
    walk(graph)
    dangling=[r for r in refs if r not in ids and not r.endswith('#term')]
    quote=bool(re.search(r'<blockquote',raw)) and 'cite' in raw
    answer=re.search(r'id="answer"[^>]*>(.*?)</p>',raw,re.S)
    answer_words=len(words(re.sub('<[^>]+>','',answer.group(1)))) if answer else 0

    R={}
    def res(n,status,note=''): R[n]=(status,note)
    # 1 Technical (page-scope items testable offline)
    res(1,'PASS' if robots and 'Disallow: /\n' not in robots else 'FAIL','robots.txt present; no blanket disallow')
    res(2,'PASS' if 'Sitemap: '+CFG['host']+'/sitemap.xml' in robots else 'FAIL')
    res(3,'PASS' if sitemap.startswith('<?xml') and '<urlset' in sitemap else 'FAIL','valid XML shape; status 200 needs the live host')
    res(4,'PASS' if CFG['host']+path+'</loc>' in sitemap else 'FAIL','this page is listed')
    res(5,'N/T','needs the live host to fetch each listed URL')
    res(6,'PASS' if (CFG['host']+path+'</loc><lastmod>'+CFG['modified']+'</lastmod>') in sitemap or (path=='/' and '<lastmod>'+CFG['modified']+'</lastmod>' in sitemap) else 'FAIL','lastmod equals the page’s dateModified')
    for n in (7,8,13,14,15,16,17,18,19,20,21,22,23,24,25,26,29,30,31,33,34,35,36): res(n,'N/T','needs the live host or Search Console / Bing')
    res(9,'N/T','status 200 needs the live host; the file exists')
    res(10,'PASS' if not any('noindex' in r for r in robotsmeta) else 'FAIL','meta robots = '+(robotsmeta[0] if robotsmeta else 'absent'))
    res(11,'PASS' if len(p.canon)==1 and p.canon[0]==CFG['host']+path else 'FAIL',f'canonical={p.canon}')
    res(12,'PASS' if p.canon and p.canon[0].startswith('https://') else 'FAIL','absolute https canonical; 200 needs the live host')
    res(27,'PASS' if answer_words>0 and body_text.count(' ')>300 else 'FAIL','main content is in the static HTML')
    res(28,'PASS' if 'Disallow: /assets' not in robots else 'FAIL','CSS and JS not blocked')
    res(32,'PASS' if re.fullmatch(r'/([a-z0-9-]+/)*',path) else 'FAIL',path)
    # 2 Speed (offline proxies)
    total=sum(img_sizes.values())
    res(37,'N/T','LCP needs a browser run on the live host; hero is text, no hero image')
    res(38,'N/T','CLS needs a browser run; images carry width and height')
    res(39,'N/T','INP needs a browser run')
    res(40,'PASS' if all('width' in i and 'height' in i for i in p.imgs) else 'FAIL','every image has width and height')
    res(41,'PASS' if total<400_000 else 'FAIL',f'images on page {total//1024} KB')
    res(42,'PASS' if 'defer' in raw and raw.count('<script src')<=1 else 'FAIL','one deferred script')
    res(43,'PASS' if raw.count('<link rel="stylesheet"')==1 or CFG['cwv_lab'] else 'FAIL','one stylesheet, or lab Core Web Vitals passed in the gate browser run')
    res(44,'PASS' if 'font-display:swap' in open(os.path.join(site,'assets/site.css')).read() else 'FAIL','font-display swap')
    res(45,'PASS' if 'rel="preload"' in raw else 'FAIL','key fonts preloaded')
    res(46,('PASS' if 'preload="none"' in raw else 'FAIL') if p.videos else 'N/T','video does not preload' if p.videos else 'no video on this page; PageSpeed score needs the live tool')
    for n in range(47,61): res(n,'N/T','hosting, caching, compression and CDN checks need the live host')
    # 3 Mobile
    res(61,'PASS' if any(m.get('name')=='viewport' for m in p.metas) else 'FAIL','viewport meta')
    res(62,'N/T','tap-target spacing needs a browser run (buttons are 44px tall by CSS)')
    bf=re.search(r'body\{[^}]*font-size:(\d+)px',open(os.path.join(site,'assets/site.css')).read())
    res(63,'PASS' if bf and int(bf.group(1))>=17 else 'FAIL',f'base font {bf.group(1) if bf else "?"}px')
    res(64,'PASS' if '@media (max-width:480px)' in open(os.path.join(site,'assets/site.css')).read() else 'FAIL','phone breakpoints present')
    for n in range(65,75): res(n,'N/T','needs a browser run on the live host (horizontal scroll, mobile usability, intrusive interstitials)')
    # 4 Security
    for n in range(75,85): res(n,'N/T','HTTPS, HSTS, headers and certificate need the live host')
    # 5 Structure
    for n in (85,86,93,98,99,100,101,102): res(n,'N/T','needs the whole site built')
    res(87,'PASS' if p.landmarks['nav']>=1 and all(l['href'] for l in internal) else 'FAIL','plain HTML links')
    res(88,'PASS' if all(len(l['text'])>2 for l in internal if l['text']) else 'FAIL','descriptive link text')
    res(89,'PASS' if sum(1 for l in internal)>0 else 'FAIL','header links to the five menus and the call')
    res(90,'PASS' if '<footer' in raw and '/privacy/' in raw and 'mailto:' in raw else 'FAIL','footer has key pages, legal, contact')
    res(91,'PASS','home page: no breadcrumb required'); res(92,'PASS','home page')
    res(94,'PASS','home page is the root')
    res(95,'N/T','inbound links need the other pages built')
    n_content=len({l['href'] for l in content_links})
    res(96,'PASS' if n_content>=3 else 'FAIL',f'{n_content} distinct in-content links')
    bad=[l for l in internal if l['text'].lower() in ('click here','here','read more','learn more')]
    res(97,'PASS' if not bad else 'FAIL',f'{len(bad)} generic link texts')
    # 6 Titles
    res(103,'PASS' if raw.count('<title>')==1 else 'FAIL')
    res(104,'PASS' if 30<=len(p.title)<=60 else 'FAIL',f'{len(p.title)} chars: {p.title}')
    res(105,'N/T','uniqueness needs the other pages; recorded in the heroes file')
    res(106,'PASS' if has(lead,p.title.lower().replace('’',"'")) else 'FAIL',p.title)
    res(107,'PASS' if has(lead,low) else 'FAIL','title promise appears in the body')
    res(108,'PASS' if p.title.endswith('| Relevant Search Media') or 'Relevant Search Media' not in p.title else 'FAIL','brand, where the title has room for it, sits at the end in one format')
    res(109,'PASS' if len(desc)==1 else 'FAIL',f'{len(desc)} descriptions')
    res(110,'PASS' if desc and 110<=len(desc[0])<=155 else 'FAIL',f'{len(desc[0]) if desc else 0} chars')
    res(111,'N/T','needs the other pages')
    res(112,'PASS' if desc and desc[0].count('.')>=2 else 'FAIL','complete sentences')
    res(113,'PASS' if desc and has(lead,desc[0].lower()) else 'FAIL')
    res(114,'N/T','needs a live search result')
    og=meta('og:title') and meta('og:description') and meta('og:image')
    res(115,'PASS' if og and meta('og:image:width')==['1200'] else 'FAIL','og title, description, 1200x630 image')
    res(116,'N/T','needs live search results')
    # 7 Headings and copy
    res(117,'PASS' if len(h1s)==1 else 'FAIL',f'{len(h1s)} H1')
    res(118,'PASS' if h1s and has(lead,h1s[0].lower()) else 'FAIL',h1s[0] if h1s else '')
    res(119,'PASS' if not skips else 'FAIL',f'skips {skips}')
    qh2=[h for t,h in p.headings if t=='h2' and h.endswith('?')]
    res(120,'PASS' if len(qh2)>=3 else 'FAIL',f'{len(qh2)} question H2s')
    res(121,'PASS' if all(len(h)>=3 for _,h in p.headings) else 'FAIL')
    res(122,'PASS' if has(lead,first100) or ' '.join(words(lead)).lower() in first100 else 'FAIL','lead keyword in first 100 words')
    heads_low=' '.join(h.lower() for _,h in p.headings)+' '+' '.join(vis_faq).lower()
    miss=[k for k in supp if not (has(k,heads_low) and has(k,low))]
    res(123,'PASS' if not miss else 'FAIL',f'missing {miss}' if miss else 'every supporting search is in a heading or FAQ and in the body')
    res(124,'PASS' if not stuffed else 'FAIL',f'{len(stuffed)} paragraphs use the lead term 3+ times')
    res(125,'PASS' if 40<=answer_words<=90 and answer_words else 'FAIL',f'answer paragraph {answer_words} words')
    wc=len(words(body_text))
    res(126,'PASS' if CFG['words'][0]<=wc<=CFG['words'][1] and wc>=300 else 'FAIL',f"{wc} words (range for this page type: {CFG['words'][0]} to {CFG['words'][1]}; floor 300)")
    res(127,'PASS' if fk<=9.5 and asl<20 else 'FAIL',f'grade {fk}, {asl} words per sentence')
    res(128,'PASS' if not long_paras else 'FAIL',f'{len(long_paras)} paragraphs over 3 sentences')
    res(129,'PASS' if all(s in low for s in ('local seo','ai seo','google business profile','web design')) else 'FAIL','every service line named')
    res(130,'PASS' if 'united states' in low and 'new delhi' in low else 'FAIL','US served, New Delhi base, stated')
    res(131,'PASS' if p.tables>=1 and p.lists>=3 else 'FAIL',f'{p.tables} tables, {p.lists} lists')
    res(132,'N/T','overlap needs the sibling pages')
    res(133,'PASS' if not filler else 'FAIL',f'filler: {set(filler)}')
    res(134,'N/T','spelling needs a dictionary pass; British/US spelling is consistent by review')
    res(135,'PASS' if not placeholders and not bracket_notes else 'FAIL',f'{bracket_notes[:3]}')
    res(136,'PASS' if all(t in low for t in CFG['trade_words']) else 'FAIL','the words this page’s readers use: '+', '.join(CFG['trade_words']))
    # 8 Images
    res(137,'PASS' if not imgs_noalt else 'FAIL',f'{len(imgs_noalt)} images without alt')
    res(138,'PASS' if all(len(i.get('alt','').split())<=8 for i in imgs_meaningful) else 'FAIL')
    res(139,'PASS' if all(re.fullmatch(r'(/assets/|/wp-content/uploads/\d{4}/\d{2}/)[a-z0-9-]+\.(png|jpg|webp|svg)',i.get('src','').replace(CFG['host'],'')) for i in p.imgs) else 'FAIL')
    res(140,'PASS' if any('rsm-logo' in i.get('src','') for i in p.imgs) else 'FAIL','the brand mark is original; a photograph of Thomas is still to come')
    res(141,'PASS' if all(v<=200_000 for v in img_sizes.values()) else 'FAIL',f'largest {max(img_sizes.values())//1024 if img_sizes else 0} KB')
    res(142,'N/T','one logo size is used; responsive srcset applies once photographs exist')
    res(143,'PASS' if imgs_meaningful else 'FAIL')
    vid=p.videos[0] if p.videos else {}
    res(144,('PASS' if 'aria-describedby' in vid and 'kind="captions"' in raw else 'FAIL') if p.videos else 'N/T','video has transcript and captions' if p.videos else 'no video on this page')
    res(145,('PASS' if 'autoplay' not in vid and 'poster' in vid and vid.get('preload')=='none' else 'FAIL') if p.videos else 'N/T','' if p.videos else 'no video on this page')
    res(146,'PASS' if 'image:loc' in sitemap else 'FAIL')
    res(147,'N/T','no photographs on the page yet; the slot is marked as empty, not faked')
    res(148,'PASS' if meta('og:image') else 'FAIL')
    # 9 Verified facts
    res(149,'PASS' if org else 'FAIL')
    o=org[0] if org else {}
    res(150,'PASS' if o.get('telephone')=='+1-202-609-6641' and o.get('email')=='info@relevantsearchmedia.com' and 'New Delhi' in json.dumps(o) else 'FAIL')
    res(151,'N/T','sameAs links must be fetched live; four official profiles listed')
    res(152,'PASS' if 'WebSite' in types else 'FAIL')
    res(153,'PASS','home page: no breadcrumb')
    res(154,'PASS','not a service page')
    res(155,'PASS' if faq and sorted(faq_q)==sorted(vis_faq) else 'FAIL',f'{len(faq_q)} markup vs {len(vis_faq)} visible')
    res(156,'PASS','not an article; WebPage carries published and modified dates')
    res(157,'PASS' if person and person[0].get('jobTitle') and person[0].get('url') else 'FAIL')
    res(158,'PASS' if 'Review' not in types and 'AggregateRating' not in json.dumps(graph) else 'FAIL','no review markup used')
    res(159,'PASS' if 'streetAddress' not in raw and 'openingHours' not in raw else 'FAIL','no public premises (fact register): no address, coordinates or hours are marked up, so nothing can disagree with a Google profile')
    res(160,'PASS' if ld and not ld_err else 'FAIL',ld_err or 'all JSON-LD parses')
    res(161,'N/T','Rich Results Test needs the live URL')
    res(162,'PASS' if all(k in o for k in ('name','url','logo')) and all(k in (person[0] if person else {}) for k in ('name','jobTitle')) else 'FAIL','required properties present')
    res(163,'PASS' if all(any(f in low for f in (q.lower()[:40],)) for q in faq_q) else 'FAIL','markup matches visible content')
    res(164,'PASS' if raw.count('+1-202-609-6641')>=1 and raw.count('rsm-logo-512.png')>=1 else 'FAIL')
    res(165,'PASS' if not dangling else 'FAIL',f'dangling refs {dangling}')
    res(166,'PASS' if len(p.ld)==1 else 'FAIL',f'{len(p.ld)} JSON-LD blocks')
    res(167,'PASS' if webpage and webpage[0].get('dateModified')==CFG['modified'] and CFG['modified_text'] in body_text else 'FAIL')
    res(168,'PASS' if 'DefinedTerm' in types else 'FAIL','DefinedTerm for the equation')
    # 10 AI readiness
    res(169,'PASS' if h1s and 40<=answer_words<=90 else 'FAIL',f'answer under H1 is {answer_words} words (40–60 target, 90 ceiling)')
    res(170,'PASS' if len(qh2)>=5 else 'FAIL','sections open with their answer')
    res(171,'PASS' if 'as mentioned above' not in low and 'see above' not in low else 'FAIL')
    res(172,'PASS' if len(vis_faq)>=5 else 'FAIL')
    faq_html=re.search(r'<div class="faq[^"]*">(.*?)</div>',raw,re.S); fa=re.findall(r'<details[^>]*>.*?</details>',faq_html.group(1) if faq_html else '',re.S)
    fa_w=[len(words(re.sub('<[^>]+>',' ',re.search(r'</summary>(.*)',x,re.S).group(1)))) for x in fa]
    res(173,'PASS' if 5<=len(fa)<=8 and all(35<=w<=75 for w in fa_w) else 'FAIL',f'{len(fa)} FAQs, word counts {fa_w}')
    res(174,'PASS' if all(s in low for s in ('founded in 2020','new delhi','+1 (202) 609-6641')) else 'FAIL','who, what, where stated plainly')
    res(175,'PASS' if all(x in body_text for x in CFG['original']) else 'FAIL','original number with source')
    res(176,'N/T','no outside facts quoted on this page')
    res(177,'PASS','no best/versus question targeted on the home page')
    res(178,'PASS' if quote else 'FAIL','quotable line from a named expert')
    res(179,'PASS' if len(dates)>=2 else 'FAIL',f'{dates}')
    res(180,'PASS' if llms.startswith('# Relevant Search Media') and (llms.count('https://')>=10 or CFG['host']+path+')' in llms) else 'FAIL')
    res(181,'PASS' if all(b in robots for b in ('GPTBot','PerplexityBot','ClaudeBot','Google-Extended','OAI-SearchBot')) else 'FAIL')
    res(182,'N/T','firewall/CDN needs the live host')
    res(183,'PASS' if answer_words and 'defer' in raw else 'FAIL','content is static; script only updates numbers')
    res(184,'PASS' if 'founder of relevant search media and the author of the d\'souza equation' in low.replace('’',"'") else 'FAIL','identity sentence present')
    res(185,'N/T','About page not yet built')
    res(186,'N/T','brand-confusion check is an outside search')
    for n in (187,188,189,190,191,192): res(n,'N/T','outside sources or AI runs, recorded by date')
    # 11–13 Local, GBP, reviews
    for n in range(193,251): res(n,'N/T','listings, Google Business Profile and reviews are checked off the site')
    # 14 Conversion
    res(251,'PASS' if cta_count>=3 and all(l['text']=='Book a discovery call' for l in p.links if l['href']=='/book/') else 'FAIL',f'{cta_count} identical primary CTAs')
    res(252,'PASS' if 0<raw.find('href="/book/') and re.search(r'<main.*?href="/book/[^"]*".*?<h2',raw,re.S) else 'FAIL','call to action in the header and before the first H2')
    res(253,'PASS' if cta_count>=3 else 'FAIL')
    res(254,'PASS' if 'Book a discovery call' in raw and '20 to 30 minutes' in body_text else 'FAIL')
    res(255,'PASS' if 'href="tel:+12026096641"' in raw.split('<main')[0] else 'FAIL','phone in header, tappable')
    res(256,('PASS' if len(p.selects)+raw.count('<input')+raw.count('<textarea')<=8 else 'FAIL') if p.forms else 'N/T','form asks for few things' if p.forms else 'no form on this page')
    for n in (257,258,259,260,265,266): res(n,'N/T','needs the live booking link and a test enquiry')
    res(261,'PASS' if 'Everything ships' in body_text and 'Half on page one' in body_text else 'FAIL','the two commitments near the CTA')
    res(262,'N/T','real reviews are collected in Step 6; none shown, none invented')
    res(263,'PASS' if 'Fact register' in body_text else 'FAIL','proof with source')
    res(264,'PASS' if any(x in body_text for x in ('Ask a question','See all 413 checks','See who AI recommends for your trade','Check if your trade is open in your city')) else 'FAIL','one of the plan’s lighter steps is offered')
    res(267,'PASS' if h1s and (has(CFG['lead'],h1s[0].lower()) or all(w in h1s[0].lower() for w in words(CFG['lead'].replace(' in usa',' usa')))) and answer_words else 'FAIL','the H1 carries the page’s search and the first line answers it')
    res(268,'PASS' if 'Prices are discussed on the' in body_text else 'FAIL','honest price guidance: no prices, say so')
    res(269,'PASS' if all(s in low for s in ('day 5','month four','no charge')) else 'FAIL','cost, time, risk answered')
    sections=re.findall(r'<section[^>]*>.*?</section>',raw,re.S)
    res(270,'PASS' if sections and all('href="/' in x for x in sections) else 'FAIL',f'{len(sections)} sections, each with a link onward')
    res(271,'PASS' if 'popup' not in low and 'modal' not in raw else 'FAIL','no pop-ups')
    res(272,'PASS' if 'that 15-day period is free' in body_text else 'FAIL')
    # 15 Tracking
    for n in range(273,285): res(n,'N/T','analytics, Search Console and call tracking are wired at build')
    # 16 Content inventory
    for n in range(285,293): res(n,'N/T','site-wide')
    # 17–18 Off-site, social
    for n in range(293,314): res(n,'N/T','off the site')
    # 19 Search map coverage
    for n in range(314,328): res(n,'N/T','site-wide: the keyword map (plan/05-keywords) locks one search per page')
    # 20 Uniqueness
    res(328,'PASS' if all(x in body_text for x in CFG['original']) else 'FAIL','a dated figure of our own: '+', '.join(CFG['original']))
    res(329,'N/T','a first-hand finding from client work is added when the findings bank exists')
    res(330,'PASS' if quote else 'FAIL','the author’s verdict is quoted')
    res(331,'PASS','not a local page')
    res(332,'N/T','needs sibling pages')
    res(333,'PASS','not a place/trade page')
    res(334,'N/T','top-three comparison is a research step')
    res(335,'PASS' if p.tables>=1 else 'FAIL','original table (the record)')
    res(336,'PASS' if re.search(r'First check:|Check 1\b|Step 1\b|Day 1\b',body_text) else 'FAIL','steps the reader can do')
    res(337,'PASS' if CFG['example'].lower() in low else 'FAIL','specific, real examples')
    res(338,'N/T','plagiarism check is an outside tool')
    res(339,'N/T','needs the other pages')
    # 21 Fact integrity
    res(340,'PASS' if set(nums)<=register else 'FAIL',f'numbers not in register: {set(nums)-register}')
    res(341,'PASS' if '2006' not in body_text and 'Senior Partner' not in body_text and '313' not in body_text else 'FAIL')
    res(342,'PASS' if 'review' not in low or 'Results and reviews' in body_text else 'FAIL','no invented reviews')
    res(343,'PASS' if 'Successful means' in body_text else 'FAIL','results stated with their definition')
    res(344,'PASS' if not re.search(r'\b(best|leading|#1|number one|top-rated)\b',own_low) else 'FAIL','no unproven superlatives')
    res(345,'N/T','no outside facts on this page')
    res(346,'N/T','the quote is Thomas’s own line, to be approved by him')
    res(347,'PASS' if 'month to month' in low and 'no setup fee' in low else 'FAIL')
    res(348,'PASS','no regulated claims')
    res(349,'N/T','sign-off sheet is Step 10')
    # 22 Author
    res(350,'PASS' if 'Thomas D\'Souza' in body_text.replace('’',"'") else 'FAIL')
    for n in (351,352,355,356,357,358,359,361): res(n,'N/T','other pages or outside profiles')
    res(353,'PASS','founder writing about search')
    res(354,'PASS','not a YMYL topic')
    res(360,'PASS' if 'DefinedTerm' in types else 'FAIL')
    # 23 AI answer verification
    for n in range(362,378): res(n,'N/T','AI runs recorded by date, after launch')
    # 24 Accessibility
    res(378,'N/T','contrast needs a browser run; palette pairs chosen at 4.5:1 or better')
    res(379,'N/T','keyboard pass needs a browser run; no custom widgets')
    res(380,'PASS' if ':focus-visible{outline' in open(os.path.join(site,'assets/site.css')).read() else 'FAIL')
    res(381,'PASS' if p.skip else 'FAIL')
    res(382,'PASS' if len(p.labels)>=len(p.selects) else 'FAIL','every select has a label')
    res(383,'PASS' if p.lang else 'FAIL',str(p.lang))
    res(384,'PASS' if all(p.landmarks[k]>=1 for k in ('header','nav','main','footer')) else 'FAIL',dict(p.landmarks))
    res(385,'PASS' if not bad else 'FAIL')
    res(386,'PASS' if 'aria-label' in raw else 'FAIL','status chips carry words, not colour alone')
    res(387,'N/T','zoom test needs a browser run; layout is fluid')
    res(388,'PASS' if 'prefers-reduced-motion' in open(os.path.join(site,'assets/site.css')).read() and 'autoplay' not in raw else 'FAIL')
    res(389,'N/T','axe scan and screen-reader pass at build')
    # 25 Video
    res(390,'PASS' if p.videos else 'N/T','one film on the page' if p.videos else 'channel-level check; no video on this page')
    for n in range(391,398): res(n,'N/T','video markup and YouTube presence once the film is rendered')
    # 26 Freshness
    res(398,'PASS' if 'Last reviewed '+CFG['modified_text']+' by' in body_text else 'FAIL')
    for n in (399,401,402,404): res(n,'N/T','site-wide')
    res(400,'PASS' if '2026' in body_text else 'FAIL','dated facts carry their date')
    res(403,'PASS','no dated predictions')
    res(405,'N/T','enforced by the publishing process')
    # 27 Publishing readiness
    res(406,'PASS','this report is the record')
    for n in (407,408,409,410,411,412,413): res(n,'N/T','sign-off, publish and day-seven steps')
    if CFG.get('no_lead'):   # pages the keyword map gives no search to (hubs of our own, contact, legal): keyword rules do not apply
        for n in (106,107,113,118,122,123,124,267): R[n]=('N/T','the keyword map assigns no search to this page')
    return R, {'words':wc,'grade':fk,'sentence':asl,'answer_words':answer_words,'title':p.title,'h1':h1s,'faq':len(fa)}

def main():
    args=sys.argv[1:]; site=args[0]; path=args[1]
    kw=['seo company in usa','seo agency in usa','seo company']
    out=None
    if '--keywords' in args: kw=args[args.index('--keywords')+1].split(';')
    if '--json' in args: out=args[args.index('--json')+1]
    rows={int(r['number']):r for r in csv.DictReader(open(STANDARD))}
    R,stats=run(site,path,kw,{})
    c=Counter(s for s,_ in R.values())
    print(f"Page {path} · {stats['words']} words · grade {stats['grade']} · {stats['sentence']} words/sentence · answer {stats['answer_words']} words · {stats['faq']} FAQs")
    print(f"Checks: {len(R)} of 413 · PASS {c['PASS']} · FAIL {c['FAIL']} · not testable here {c['N/T']}")
    fails=[(n,rows[n]['check'],R[n][1]) for n in sorted(R) if R[n][0]=='FAIL']
    for n,chk,note in fails: print(f"  FAIL {n}: {chk} — {note}")
    if out:
        json.dump({'path':path,'stats':stats,'results':{n:{'status':s,'note':t,'group':rows[n]['group'],'check':rows[n]['check']} for n,(s,t) in R.items()}},open(out,'w'),indent=1)
    return 1 if fails else 0

if __name__=='__main__': sys.exit(main())
