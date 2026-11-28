import re, json, math
S='/tmp/claude-0/-home-user/047ff176-183a-5204-85cb-638a9dde03fc/scratchpad/'
R='/home/user/rsm-engine/'
o=open(R+'design/canvas/project/Origin.dc.html').read()
I=json.loads(re.search(r'this\.I = (\[.*?\]);\n',o,re.S).group(1))
by={i['name']:i for i in I}
def icon(name,x,y,s):
    svg=by[name]['svg']; inner=re.sub(r'^<svg[^>]*>|</svg>$','',svg.strip())
    fill=' fill="none"' if 'fill="none"' in svg.split('>')[0] else ''
    return f'<svg x="{x}" y="{y}" width="{s}" height="{s}" viewBox="0 0 48 48"{fill}>{inner}</svg>'

# ---- engines plate
W,H=1000,400; qx,qy=250,200; ax=750
eng=['Google','Maps','ChatGPT','Gemini','Perplexity']; ys=[44,122,200,278,356]; tx=500; ts=56
p=[f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="One question goes to Google, Maps, ChatGPT, Gemini and Perplexity, and one business is named">',
 '<defs><linearGradient id="eg-in" x1="0" x2="1"><stop offset="0" stop-color="#A3B5F2" stop-opacity=".15"/><stop offset="1" stop-color="#A3B5F2" stop-opacity=".7"/></linearGradient><linearGradient id="eg-out" x1="0" x2="1"><stop offset="0" stop-color="#FFD98A" stop-opacity=".75"/><stop offset="1" stop-color="#F8B10F" stop-opacity=".25"/></linearGradient><radialGradient id="eg-glow"><stop offset="0" stop-color="#F8B10F" stop-opacity=".5"/><stop offset="1" stop-color="#F8B10F" stop-opacity="0"/></radialGradient><linearGradient id="eg-tile" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3C5096" stop-opacity=".7"/><stop offset=".4" stop-color="#1E2A56" stop-opacity=".9"/><stop offset="1" stop-color="#0A1024"/></linearGradient></defs>']
for i,y in enumerate(ys):
    d1=f'M{qx} {qy} C {qx+130} {qy}, {tx-ts/2-110} {y}, {tx-ts/2-4} {y}'
    d2=f'M{tx+ts/2+4} {y} C {tx+ts/2+110} {y}, {ax-130} {qy}, {ax} {qy}'
    p.append(f'<path id="ein{i}" d="{d1}" fill="none" stroke="url(#eg-in)" stroke-width="1.4"/><path class="eg-o" id="eout{i}" d="{d2}" fill="none" stroke="url(#eg-out)" stroke-width="1.6"/>')
    p.append(f'<circle r="3.2" fill="#DCE6FF"><animateMotion dur="3.6s" begin="{i*0.55:.2f}s" repeatCount="indefinite"><mpath href="#ein{i}"/></animateMotion></circle>')
    p.append(f'<circle class="eg-o eg-spark" r="3.8" fill="#FFD98A"><animateMotion dur="3.6s" begin="{i*0.55+1.8:.2f}s" repeatCount="indefinite"><mpath href="#eout{i}"/></animateMotion></circle>')
INFO={'Google': 'Google reads your pages, your links and how people use them.', 'Maps': 'Maps reads your listing: categories, hours, photos and reviews.', 'ChatGPT': 'ChatGPT reads what the wider web says about you, then answers in a sentence.', 'Gemini': 'Gemini reads Google’s index and your business profile together.', 'Perplexity': 'Perplexity reads live sources and shows which ones it used.'}
for n,y in zip(eng,ys):
    p.append(f'<g class="eg-tile" tabindex="0" role="button" aria-label="{n}: {INFO[n]}" data-info="{INFO[n]}"><rect x="{tx-ts/2}" y="{y-ts/2}" width="{ts}" height="{ts}" rx="16" fill="url(#eg-tile)" stroke="rgba(190,205,250,.45)"/>'+icon(n,tx-15,y-15,30)+'</g>')
    p.append(f'<text x="{tx+ts/2+12}" y="{y-ts/2+2}" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" letter-spacing="1.5" fill="#B4C0E0">{n.upper()}</text>')
# question card
p.append(f'<rect x="18" y="{qy-66}" width="232" height="132" rx="20" fill="url(#eg-tile)" stroke="rgba(163,181,242,.4)"/><text x="40" y="{qy-34}" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" letter-spacing="2" fill="#A3B5F2">THE QUESTION</text><text x="40" y="{qy+2}" font-family="Sora, sans-serif" font-size="23" font-weight="650" fill="#fff" id="eg-q1">“Who should</text><text x="40" y="{qy+32}" font-family="Sora, sans-serif" font-size="23" font-weight="650" fill="#fff" id="eg-q2">I call?”</text>')
# answer
p.append(f'<circle id="eg-glowc" cx="{ax+110}" cy="{qy}" r="150" fill="url(#eg-glow)"/><rect id="eg-ansr" x="{ax}" y="{qy-66}" width="232" height="132" rx="20" fill="url(#eg-tile)" stroke="rgba(248,177,15,.75)"/><circle cx="{ax+50}" cy="{qy}" r="28" fill="#F6EFDF" stroke="#E2AE45" stroke-width="1.5"/><image href="/assets/rsm-logo-512.png" x="{ax+31}" y="{qy-17}" width="38" height="34"/><text x="{ax+92}" y="{qy-14}" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" letter-spacing="2" fill="#FFD98A" id="eg-ansl">THE ANSWER</text><text x="{ax+92}" y="{qy+16}" font-family="Sora, sans-serif" font-size="23" font-weight="650" fill="#fff" id="eg-ans">You.</text>')
p.append('</svg>'); ENG=''.join(p)

# ---- path plate (first fifteen days)
def bez(p0,p1,p2,p3,t): return tuple((1-t)**3*a+3*(1-t)**2*t*b+3*(1-t)*t*t*c+t**3*d for a,b,c,d in zip(p0,p1,p2,p3))
seg1=((100,250),(300,250),(420,120),(600,120)); seg2=((600,120),(780,120),(950,78),(1120,78))
def y_at(x):
    seg=seg1 if x<=600 else seg2; best=None
    for k in range(0,401):
        px,py=bez(*seg,k/400)
        if best is None or abs(px-x)<best[0]: best=(abs(px-x),py)
    return best[1]
d='M100 250 C 300 250, 420 120, 600 120 S 950 78, 1120 78'
ico={1:'<path d="M-11 -9h22v14h-12l-7 6v-6h-3z"/>',2:'<circle cx="-2" cy="-2" r="8"/><path d="M4 4l7 7"/>',3:'<path d="M-10 -8l4 4 7-8M-10 4l4 4 7-8M5 -6h7M5 6h7"/>',4:'<rect x="-11" y="-9" width="22" height="20" rx="3"/><path d="M-11 -3h22M-5 -13v6M5 -13v6"/>',5:'<circle r="3" fill="#1A1200" stroke="none"/><path d="M-7 -7a10 10 0 0 0 0 14M7 -7a10 10 0 0 1 0 14M-12 -12a17 17 0 0 0 0 24M12 -12a17 17 0 0 1 0 24"/>'}
q=['<svg viewBox="0 0 1220 350" role="img" aria-label="Five days from the first conversation to live work, then work logged every day until the first report on day fifteen">',
 '<defs><linearGradient id="pg" x1="0" x2="1"><stop offset="0" stop-color="#6F8CF0"/><stop offset=".45" stop-color="#A3B5F2"/><stop offset=".5" stop-color="#F8B10F"/><stop offset="1" stop-color="#4CC0A8"/></linearGradient><radialGradient id="pglow"><stop offset="0" stop-color="#F8B10F" stop-opacity=".6"/><stop offset="1" stop-color="#F8B10F" stop-opacity="0"/></radialGradient><linearGradient id="pmed" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4760B4"/><stop offset=".5" stop-color="#243268"/><stop offset="1" stop-color="#121A40"/></linearGradient><filter id="pblur" x="-10%" y="-80%" width="120%" height="260%"><feGaussianBlur stdDeviation="9"/></filter><linearGradient id="parea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6F8CF0" stop-opacity=".22"/><stop offset="1" stop-color="#6F8CF0" stop-opacity="0"/></linearGradient></defs>',
 f'<path d="{d} L1120 300 L100 300 Z" fill="url(#parea)"/>',
 '<path d="M100 300H1120" stroke="rgba(163,181,242,.3)" stroke-width="1.5"/>']
xs={n:100+(n-1)*125 for n in range(1,6)}; xs.update({n:600+(n-5)*52 for n in range(6,16)})
for n in range(1,16):
    x=xs[n]; big=n in (1,5,10,15)
    q.append(f'<path d="M{x} 300v{10 if big else 6}" stroke="rgba(163,181,242,.55)" stroke-width="1.5"/>'+(f'<text x="{x}" y="330" text-anchor="middle" font-size="11" font-weight="700" letter-spacing="1.5" fill="#B4C0E0">DAY {n}</text>' if big else ''))
q.append(f'<path d="{d}" fill="none" stroke="url(#pg)" stroke-width="14" stroke-linecap="round" filter="url(#pblur)" opacity=".7"/><path id="launch" d="{d}" fill="none" stroke="url(#pg)" stroke-width="5" stroke-linecap="round"/>')
for n in range(6,15):
    x=xs[n]; y=y_at(x)
    q.append(f'<g><circle cx="{x}" cy="{y:.1f}" r="9" fill="#121A40" stroke="#4CC0A8" stroke-width="2"/><path d="M{x-4} {y:.1f}l3 3 5-6" fill="none" stroke="#4CC0A8" stroke-width="2" stroke-linecap="round"><animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{(n-5)/11:.2f};{(n-4.5)/11:.2f};1" dur="6s" repeatCount="indefinite"/></path></g>')
names={1:'DISCOVER',2:'MARKET STUDY',3:'413 CHECKS',4:'GROWTH PLAN',5:'LIVE'}
for n in range(1,6):
    x=xs[n]; y=y_at(x); gold=n==5; r=38 if gold else 30
    if gold: q.append(f'<circle cx="{x}" cy="{y:.1f}" r="110" fill="url(#pglow)"/><circle cx="{x}" cy="{y:.1f}" r="{r}" fill="none" stroke="#F8B10F" stroke-width="1.5"><animate attributeName="r" values="{r};{r+40}" dur="2.6s" repeatCount="indefinite"/><animate attributeName="opacity" values=".8;0" dur="2.6s" repeatCount="indefinite"/></circle>')
    q.append(f'<circle cx="{x}" cy="{y:.1f}" r="{r}" fill="{"#F8B10F" if gold else "url(#pmed)"}" stroke="{"#FFD98A" if gold else "rgba(190,205,250,.6)"}" stroke-width="2"/><g transform="translate({x},{y:.1f}) scale({1.25 if gold else 1.1})" fill="none" stroke="{"#1A1200" if gold else "#FFD98A"}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ico[n]}</g>')
    q.append(f'<text x="{x}" y="{y-r-14:.1f}" text-anchor="middle" font-size="12" font-weight="700" letter-spacing="2" fill="{"#FFD98A" if gold else "#fff"}">{names[n]}</text>')
x=xs[15]; y=y_at(x)
q.append(f'<circle cx="{x}" cy="{y:.1f}" r="34" fill="#121A40" stroke="#4CC0A8" stroke-width="2.5"/><g transform="translate({x},{y:.1f})" fill="none" stroke="#8EE3D0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M-9 -13h13l6 6v20h-19z"/><path d="M-4 0h9M-4 6h9"/></g><text x="{x}" y="{y-48:.1f}" text-anchor="middle" font-size="12" font-weight="700" letter-spacing="2" fill="#8EE3D0">FIRST REPORT</text>')
q.append(f'<text x="{(xs[6]+xs[14])/2}" y="{y_at(xs[10])+44:.1f}" text-anchor="middle" font-size="11" font-weight="700" letter-spacing="2" fill="#B4C0E0">WORK SHIPPED AND LOGGED EVERY DAY</text>')
q.append('<circle r="7" fill="#fff"><animateMotion dur="6s" repeatCount="indefinite"><mpath href="#launch"/></animateMotion></circle><circle r="16" fill="#fff" opacity=".25"><animateMotion dur="6s" repeatCount="indefinite"><mpath href="#launch"/></animateMotion></circle></svg>')
PATH=''.join(q)

# ---- pictograms (340x170)
def pic(inner,label): return f'<svg class="pic" viewBox="0 0 340 170" role="img" aria-label="{label}" fill="none" stroke-linecap="round" stroke-linejoin="round">{inner}</svg>'
P='#A3B5F2'; G='#F8B10F'; T='#4CC0A8'; D='rgba(163,181,242,.28)'; M='font-family="JetBrains Mono, monospace" font-weight="700" stroke="none"'
def row(x,y,w,label,col,fillc='none',dash=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="24" rx="7" stroke="{col}" stroke-width="1.4" fill="{fillc}" {dash}/><text x="{x+10}" y="{y+16}" font-size="9" letter-spacing="1" fill="{col}" {M}>{label}</text>'
stars=lambda x,y,n,col: ''.join(f'<path d="M{x+i*11} {y}l1.8 3.6 4 .6-2.9 2.8.7 4-3.6-1.9-3.6 1.9.7-4-2.9-2.8 4-.6z" fill="{col if i<n else "none"}" stroke="{col}" stroke-width=".8"/>' for i in range(5))
PIC=[
 # 1 not found: results list without you
 pic(f'<rect x="24" y="14" width="292" height="26" rx="13" stroke="{P}" stroke-width="1.4"/><circle cx="40" cy="27" r="5" stroke="{P}" stroke-width="1.4"/><path d="M43.500 30.500l3.500 3.500" stroke="{P}" stroke-width="1.4"/><text x="56" y="31" font-size="10" fill="#fff" {M}>plumber near me</text>'
     +row(24,50,292,'1 · ANOTHER COMPANY',P)+row(24,80,292,'2 · ANOTHER COMPANY',P)+row(24,110,292,'3 · ANOTHER COMPANY',P)
     +f'<rect x="24" y="140" width="292" height="22" rx="7" stroke="{G}" stroke-width="1.4" stroke-dasharray="4 5"><animate attributeName="opacity" values="1;.35;1" dur="2.4s" repeatCount="indefinite"/></rect><text x="34" y="155" font-size="9" letter-spacing="1" fill="{G}" {M}>YOU · NOT ON PAGE ONE</text>','A results page that lists three other companies; yours is not on page one'),
 # 2 found, not chosen
 pic(f'<rect x="20" y="16" width="144" height="138" rx="12" stroke="{G}" stroke-width="1.5" fill="rgba(248,177,15,.08)"/><text x="32" y="34" font-size="9" letter-spacing="1.5" fill="{G}" {M}>THEM</text><rect x="32" y="42" width="54" height="34" rx="6" fill="rgba(248,177,15,.25)" stroke="{G}" stroke-width="1"/><rect x="92" y="42" width="26" height="16" rx="4" fill="rgba(248,177,15,.25)" stroke="{G}" stroke-width="1"/><rect x="92" y="60" width="26" height="16" rx="4" fill="rgba(248,177,15,.25)" stroke="{G}" stroke-width="1"/>{stars(36,86,5,G)}<path d="M32 108h100M32 118h70" stroke="{G}" stroke-width="2" opacity=".6"/><rect x="32" y="128" width="120" height="18" rx="9" fill="{G}"/><text x="92" y="141" text-anchor="middle" font-size="9" letter-spacing="1.5" fill="#1A1200" {M}>CALL</text>'
     +f'<rect x="176" y="16" width="144" height="138" rx="12" stroke="{D}" stroke-width="1.5"/><text x="188" y="34" font-size="9" letter-spacing="1.5" fill="{P}" {M}>YOU</text><rect x="188" y="42" width="54" height="34" rx="6" stroke="{D}" stroke-width="1" stroke-dasharray="3 4"/><text x="215" y="63" text-anchor="middle" font-size="8" fill="rgba(163,181,242,.6)" {M}>NO PHOTO</text>{stars(192,86,2,P)}<path d="M188 108h60" stroke="{D}" stroke-width="2"/><rect x="188" y="128" width="120" height="18" rx="9" stroke="{D}" stroke-width="1.2"/>'
     +f'<path d="M118 150l8 16 3-7 7-2z" fill="#fff" stroke="#0B1123" stroke-width="1"><animateTransform attributeName="transform" type="translate" values="60 0;0 0;0 0;60 0" dur="4s" repeatCount="indefinite"/></path>','Two listings side by side: theirs has photos, stars and a call button; yours has no photo and few stars'),
 # 3 google yes, AI no
 pic(f'<text x="24" y="24" font-size="9" letter-spacing="1.5" fill="{T}" {M}>GOOGLE</text>'+row(24,32,136,'1 · YOU',T,'rgba(76,192,168,.12)')+row(24,62,136,'2 · OTHER',D)+row(24,92,136,'3 · OTHER',D)+f'<path d="M138 40l5 5 9-10" stroke="{T}" stroke-width="2.2"/>'
     +f'<text x="184" y="24" font-size="9" letter-spacing="1.5" fill="{G}" {M}>AI ASSISTANT</text><path d="M184 32h132v92h-96l-16 14v-14h-20z" stroke="{G}" stroke-width="1.5"/><text x="196" y="52" font-size="9" fill="#fff" {M}>“Who should I call?”</text><path d="M196 62h108" stroke="{D}" stroke-width="1"/><text x="196" y="80" font-size="9" fill="{G}" {M}>Try Another Co.</text><text x="196" y="98" font-size="9" fill="rgba(163,181,242,.7)" {M}>or Someone Else.</text><text x="196" y="116" font-size="9" fill="rgba(163,181,242,.45)" {M}>(you are not named)</text>'
     +f'<path d="M164 78h14" stroke="{D}" stroke-width="1.5" stroke-dasharray="2 4"/>','Google lists you first, but an AI assistant names two other companies'),
 # 4 lost it
 pic(f'<path d="M30 140h284M30 140V22" stroke="{D}" stroke-width="1.4"/><path d="M30 110h284M30 80h284M30 50h284" stroke="rgba(163,181,242,.10)" stroke-width="1"/><path d="M36 118l34-12 30 4 34-34 34-18 22-10" stroke="{T}" stroke-width="2.4"/><path d="M190 48l26 62 30 10 34 8 30 4" stroke="{G}" stroke-width="2.4"/><path d="M190 22v118" stroke="{G}" stroke-width="1.2" stroke-dasharray="3 5"/><circle cx="190" cy="48" r="6" fill="{G}" stroke="none"><animate attributeName="r" values="6;9;6" dur="2s" repeatCount="indefinite"/></circle><rect x="198" y="18" width="104" height="20" rx="10" fill="#0B1123" stroke="{G}" stroke-width="1.2"/><text x="250" y="32" text-anchor="middle" font-size="9" letter-spacing="1" fill="{G}" {M}>GOOGLE UPDATE</text><text x="36" y="158" font-size="8" letter-spacing="1" fill="rgba(163,181,242,.7)" {M}>RANKINGS, WEEK BY WEEK</text>','A rankings chart that climbs, then falls from the day of a Google update'),
 # 5 quote
 pic(f'<rect x="22" y="14" width="140" height="142" rx="10" stroke="{T}" stroke-width="1.5"/><text x="34" y="34" font-size="9" letter-spacing="1.5" fill="{T}" {M}>A FAIR QUOTE</text>'
     +''.join(f'<path d="M36 {58+i*30}l5 5 9-10" stroke="{T}" stroke-width="2.2"/><text x="58" y="{62+i*30}" font-size="9" fill="#fff" {M}>{t}</text>' for i,t in enumerate(['What is mapped','What ships first','What is in writing']))
     +f'<rect x="178" y="14" width="140" height="142" rx="10" stroke="{G}" stroke-width="1.5" stroke-dasharray="5 5"/><text x="190" y="34" font-size="9" letter-spacing="1.5" fill="{G}" {M}>THE OTHER KIND</text>'
     +''.join(f'<text x="194" y="{63+i*30}" font-size="13" fill="{G}" {M}>?</text><path d="M214 {58+i*30}h{w}" stroke="{D}" stroke-width="6"/>' for i,w in enumerate([84,60,76])),'Two quotes: one answers what is mapped, what ships first and what is in writing; the other answers none'),
 # 6 encyclopedia
 pic(f'<rect x="24" y="14" width="292" height="26" rx="13" stroke="{G}" stroke-width="1.4"/><circle cx="40" cy="27" r="5" stroke="{G}" stroke-width="1.4"/><path d="M43.500 30.500l3.500 3.500" stroke="{G}" stroke-width="1.4"/><text x="56" y="31" font-size="10" fill="#fff" {M}>my listing was suspended</text>'
     +''.join(f'<text x="30" y="{66+i*26}" font-size="10" fill="{G}" {M}>{l}</text><path d="M52 {62+i*26}h{w}" stroke="{"#FFD98A" if i==1 else D}" stroke-width="{2.4 if i==1 else 2}"/><path d="M296 {58+i*26}l6 4-6 4" stroke="{G if i==1 else D}" stroke-width="1.6"/>' for i,(l,w) in enumerate([('G',150),('L',210),('P',120),('S',180)]))
     ,'A searchable index of problems, one entry per problem'),
]

# ---- US map (lighter)
poly=[(-124.7,48.4),(-123.0,48.9),(-117.0,49.0),(-104.0,49.0),(-95.2,49.0),(-94.6,48.7),(-89.6,48.0),(-88.4,48.3),(-84.8,46.8),(-84.1,46.5),(-82.5,45.3),(-82.4,43.0),(-83.1,42.0),(-79.0,42.9),(-76.8,43.6),(-74.9,45.0),(-71.5,45.0),(-69.2,47.4),(-67.8,47.1),(-67.0,44.8),(-70.0,43.7),(-70.7,42.0),(-70.0,41.6),(-73.9,40.6),(-74.2,39.6),(-75.5,38.4),(-76.0,36.9),(-75.5,35.3),(-77.9,33.9),(-80.9,32.0),(-81.4,30.4),(-80.0,26.8),(-80.4,25.2),(-81.8,25.9),(-82.8,27.9),(-82.7,29.0),(-84.0,30.1),(-85.3,29.7),(-88.0,30.4),(-89.6,30.2),(-89.4,29.0),(-91.3,29.3),(-93.8,29.7),(-97.2,27.8),(-97.4,25.9),(-99.2,26.5),(-101.4,29.8),(-103.1,29.0),(-104.9,30.6),(-106.5,31.8),(-108.2,31.8),(-108.2,31.3),(-111.1,31.3),(-114.8,32.5),(-117.1,32.5),(-118.5,34.0),(-120.6,34.6),(-122.4,37.2),(-123.8,39.4),(-124.4,40.4),(-124.2,42.0),(-124.6,43.0),(-124.0,46.3),(-124.7,48.4)]
def inside(x,y):
    c=False
    for i in range(len(poly)-1):
        x1,y1=poly[i];x2,y2=poly[i+1]
        if (y1>y)!=(y2>y) and x<(x2-x1)*(y-y1)/(y2-y1)+x1: c=not c
    return c
def proj(lon,lat): return ((lon+125)*math.cos(math.radians(38))*13.2+40, (50-lat)*16.6)
dots=[]; lat=49.0
while lat>24.5:
    lon=-125.0
    while lon<-66:
        if inside(lon,lat): dots.append(proj(lon,lat))
        lon+=1.45
    lat-=1.13
cities={'New York':(-74.0,40.7),'Los Angeles':(-118.2,34.05),'Chicago':(-87.6,41.9),'Houston':(-95.4,29.76),'Dallas':(-96.8,32.8),'Miami':(-80.2,25.8),'Atlanta':(-84.4,33.75),'Phoenix':(-112.1,33.45),'Denver':(-105.0,39.74),'Fresno':(-119.8,36.74)}
side={'New York':'r','Los Angeles':'l','Chicago':'t','Houston':'b','Dallas':'t','Miami':'r','Atlanta':'r','Phoenix':'b','Denver':'t','Fresno':'l'}
svg=['<svg class="usmap" viewBox="-70 -4 800 440" role="img" aria-label="Map of the United States with the ten launch cities marked">','<g class="land">'+''.join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="2.1"/>' for x,y in dots)+'</g>']
for i,(n,(lo,la)) in enumerate(cities.items()):
    x,y=proj(lo,la); s=side[n]
    txx,tyy,anc={'r':(x+12,y+4,'start'),'l':(x-12,y+4,'end'),'t':(x,y-13,'middle'),'b':(x,y+21,'middle')}[s]
    svg.append(f'<g class="city" style="--d:{i*0.35:.2f}s"><circle class="halo" cx="{x:.0f}" cy="{y:.0f}" r="5"/><circle class="pin" cx="{x:.0f}" cy="{y:.0f}" r="4.5"/><text x="{txx:.0f}" y="{tyy:.0f}" text-anchor="{anc}">{n}</text></g>')
svg.append('</svg>'); US=''.join(svg)

body=open(S+'body4.html',encoding='utf-8').read()
for k,v in {'{{ENGINES}}':ENG,'{{PATH}}':PATH,'{{USMAP}}':US,**{f'{{{{PIC{i+1}}}}}':PIC[i] for i in range(6)}}.items():
    assert k in body,k; body=body.replace(k,v)
body=body.replace('<ul class="cards four" style="margin-top:44px">','<ul class="cards four look-cards">')
p=R+'site/index.html'; s=open(p,encoding='utf-8').read(); head=s[:s.index('<body>')]
head=re.sub(r'\s*<link rel="preload"[^>]*>','',head)
pre='\n  <link rel="preload" href="/assets/fonts/sora.woff2" as="font" type="font/woff2" crossorigin>\n  <link rel="preload" href="/assets/fonts/jakarta.woff2" as="font" type="font/woff2" crossorigin>'
head=head.replace('<link rel="stylesheet" href="/assets/site.css">',pre+'\n  <link rel="stylesheet" href="/assets/site.css">',1)
head=re.sub(r'<html lang="en-US"[^>]*>','<html lang="en-US" class="no-js">',head)
if 'theme-color' not in head: head=head.replace('<meta charset="utf-8">','<meta charset="utf-8">\n  <meta name="theme-color" content="#0B1033">',1)
open(p,'w',encoding='utf-8').write(head+body); print('ok', len(head+body)//1024,'KB', 'dots',len(dots))
