"""us_english.py [--write] -> converts British spellings and usage in the site's copy to American English. The site serves US customers only (fact register A5).
Without --write it only reports what it would change."""
import re, sys, os, collections
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
FILES = ['wordpress/pages.py', 'site/index.html', 'wordpress/art.py', 'wordpress/build.py', 'wordpress/rsm-elements/widgets.php', 'wordpress/rsm-elements/rsm-elements.php', 'wordpress/rsm-elements/data/standard.json', 'wordpress/rsm-theme/assets/site.js']
W = {'enquiries': 'inquiries', 'enquiry': 'inquiry', 'enquire': 'inquire', 'enquired': 'inquired', 'licence': 'license', 'licences': 'licenses', 'licenced': 'licensed', 'neighbourhood': 'neighborhood', 'neighbourhoods': 'neighborhoods', 'neighbour': 'neighbor', 'neighbours': 'neighbors',
     'labelled': 'labeled', 'labelling': 'labeling', 'unlabelled': 'unlabeled', 'colour': 'color', 'colours': 'colors', 'favour': 'favor', 'favours': 'favors', 'favourite': 'favorite', 'judgement': 'judgment', 'judgements': 'judgments', 'centre': 'center', 'centres': 'centers',
     'behaviour': 'behavior', 'analyse': 'analyze', 'analysed': 'analyzed', 'analyses': 'analyzes', 'programme': 'program', 'fortnight': 'two weeks', 'postcode': 'zip code', 'labour': 'labor', 'rota': 'schedule', 'cancelled': 'canceled', 'travelling': 'traveling', 'modelling': 'modeling',
     'grey': 'gray', 'whilst': 'while', 'learnt': 'learned', 'catalogue': 'catalog', 'cheque': 'check', 'defence': 'defense', 'offence': 'offense', 'fulfil': 'fulfill', 'skilful': 'skillful', 'tyres': 'tires', 'autumn': 'fall', 'remodelling': 'remodeling', 'remodelled': 'remodeled', 'counselling': 'counseling', 'jewellery': 'jewelry', 'kerb': 'curb', 'aluminium': 'aluminum', 'metre': 'meter', 'metres': 'meters'}
P = [(r'\bcar park\b', 'parking lot'), (r'\bstraight away\b', 'right away'), (r'\bwould sooner\b', 'would rather'), (r'\bmobile data\b', 'cellular data'), (r'\bwhat you fit\b', 'what you install'), (r'\bapproved to install\b', 'approved to install'),
     (r'\bWe tidy the files\b', 'We clean up the files'), (r'\btidy the main listings\b', 'clean up the main listings'), (r'(?<!real )\bestate agent\b', 'real estate agent'), (r'\bPictures of gardens you have built or kept\b', 'Pictures of landscapes you have built or maintained'), (r'\bon a schedule, and sooner when\b', 'on a schedule, and earlier when')]
KEEP = set('promise raise noise rise wise advise expertise franchise premise praise otherwise advertise exercise surprise precise concise disguise compromise enterprise likewise revise supervise devise arise demise merchandise paradise poise bruise cruise televise improvise comprise despise appraise clockwise treatise'.split())
def case(src, dst): return dst.capitalize() if src[0].isupper() and not src.isupper() else dst.upper() if src.isupper() and len(src) > 1 else dst
def ize(m):
    w = m.group(0); l = w.lower(); stem = re.sub(r'(ise|ises|ised|ising|isation|isations|iser|isers)$', '', l)
    if l in KEEP or re.sub(r'(s|d|r|rs)$', '', l) in KEEP or re.sub(r'ing$', 'e', l) in KEEP or len(stem) < 3: return w
    return case(w, re.sub(r'is(e|es|ed|ing|ation|ations|er|ers)$', r'iz\1', l))
tot = collections.Counter()
for f in FILES:
    p = os.path.join(R, f)
    if not os.path.exists(p): continue
    s = open(p, encoding='utf-8').read(); o = s
    for a, b in W.items():
        def rep(m, b=b):
            if re.search(r'[-_/=.]$', s[max(0, m.start() - 1):m.start()]) or s[m.end():m.end() + 1] in ('-', '_', '=', '(', '/'): return m.group(0)   # leave identifiers, classes and paths alone
            tot[m.group(0).lower()] += 1; return case(m.group(0), b)
        s = re.sub(r'(?:(?<=\\n)|\b)%s\b' % a, rep, s, flags=re.I)   # also right after a literal \n in the page specs
    for a, b in P: s, n = re.subn(a, b, s); tot[a] += n
    def rep2(m):
        if re.search(r'[-_/=.]$', s[max(0, m.start() - 1):m.start()]) or s[m.end():m.end() + 1] in ('-', '_', '=', '(', '/'): return m.group(0)
        r = ize(m)
        if r != m.group(0): tot[m.group(0).lower()] += 1
        return r
    s = re.sub(r'\b[A-Za-z]{3,}is(?:e|es|ed|ing|ation|ations|er|ers)\b', rep2, s)
    if s != o and '--write' in sys.argv: open(p, 'w', encoding='utf-8').write(s)
    print(f, 'changed' if s != o else 'same')
print(sorted(tot.items(), key=lambda x: -x[1]))
