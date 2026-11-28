"""Pictures for the problem cards: filled, lit panels in the site's own colours (no thin wireframes)."""
M = 'font-family="JetBrains Mono, monospace"'
S = 'font-family="Sora, sans-serif"'

def defs(u):
    return (f'<defs><linearGradient id="pn{u}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#34489A"/><stop offset=".55" stop-color="#1B2658"/><stop offset="1" stop-color="#0C1230"/></linearGradient>'
            f'<linearGradient id="gd{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFD98A"/><stop offset="1" stop-color="#F8B10F"/></linearGradient>'
            f'<linearGradient id="tl{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8EE3D0"/><stop offset="1" stop-color="#3DAE97"/></linearGradient>'
            f'<radialGradient id="gg{u}"><stop offset="0" stop-color="#F8B10F" stop-opacity=".55"/><stop offset="1" stop-color="#F8B10F" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="gt{u}"><stop offset="0" stop-color="#4CC0A8" stop-opacity=".5"/><stop offset="1" stop-color="#4CC0A8" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="gb{u}"><stop offset="0" stop-color="#6F8CF0" stop-opacity=".45"/><stop offset="1" stop-color="#6F8CF0" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="ar{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4CC0A8" stop-opacity=".45"/><stop offset="1" stop-color="#4CC0A8" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="ag{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F8B10F" stop-opacity=".4"/><stop offset="1" stop-color="#F8B10F" stop-opacity="0"/></linearGradient></defs>')

def wrap(u, label, body):
    return f'<svg class="pic" viewBox="0 0 340 190" role="img" aria-label="{label}" fill="none" stroke-linecap="round" stroke-linejoin="round">{defs(u)}{body}</svg>'

def panel(u, x, y, w, h, rx=12, stroke='rgba(163,181,242,.35)', fill=None, sw=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill or f"url(#pn{u})"}" stroke="{stroke}" stroke-width="{sw}"/>'

def bar(x, y, w, c='rgba(190,205,250,.5)', h=5):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{c}"/>'

def t(x, y, s, size=9, c='#B4C0E0', fam=M, w=700, ls=1, anchor='start'):
    return f'<text x="{x}" y="{y}" {fam} font-size="{size}" font-weight="{w}" letter-spacing="{ls}" fill="{c}" text-anchor="{anchor}">{s}</text>'

def star(cx, cy, r, c):
    import math
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5; rr = r if i % 2 == 0 else r * .45
        pts.append(f'{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}')
    return f'<polygon points="{" ".join(pts)}" fill="{c}"/>'

def p1():
    u = 'a'; b = f'<circle cx="170" cy="40" r="120" fill="url(#gb{u})"/>'
    b += panel(u, 30, 14, 280, 30, 15, 'rgba(190,205,250,.7)', sw=1.4) + '<circle cx="50" cy="29" r="6" stroke="#FFD98A" stroke-width="2"/><path d="M54.500 33.500l4.500 4.500" stroke="#FFD98A" stroke-width="2"/>' + t(68, 33, 'plumber near me', 11, '#fff', ls=.4)
    for i, y in enumerate((54, 82, 110)):
        b += panel(u, 30, y, 280, 23, 8) + f'<circle cx="46" cy="{y + 11.5}" r="6.5" fill="rgba(163,181,242,.3)"/>' + t(46, y + 15, str(i + 1), 8.5, '#fff', anchor='middle', ls=0) + bar(62, y + 7, 120 - i * 14, 'rgba(220,230,255,.75)') + bar(62, y + 15, 70 + i * 10, 'rgba(163,181,242,.4)', 3.5)
        b += ''.join(star(250 + k * 11, y + 11.5, 4.2, '#F8B10F') for k in range(5))
    b += '<path d="M30 143h110M200 143h110" stroke="rgba(248,177,15,.5)" stroke-width="1" stroke-dasharray="3 5"/>' + t(170, 146, 'PAGE TWO', 8, '#FFD98A', anchor='middle', ls=1.6)
    b += f'<rect x="30" y="155" width="280" height="24" rx="8" fill="rgba(248,177,15,.08)" stroke="#F8B10F" stroke-width="1.2" stroke-dasharray="4 4"/>' + t(46, 171, 'YOU', 9.5, '#FFD98A') + bar(78, 165, 96, 'rgba(255,217,138,.45)')
    return wrap(u, 'A results page with three other companies on page one and your business on page two', b)

def p2():
    u = 'b'; b = f'<circle cx="92" cy="95" r="118" fill="url(#gg{u})"/>'
    b += panel(u, 22, 16, 142, 158, 14, '#F8B10F', sw=1.6) + t(36, 36, 'THEM', 9, '#FFD98A', ls=1.6)
    b += f'<rect x="36" y="44" width="62" height="44" rx="7" fill="url(#gd{u})" opacity=".9"/><rect x="104" y="44" width="46" height="20" rx="5" fill="rgba(248,177,15,.55)"/><rect x="104" y="68" width="46" height="20" rx="5" fill="rgba(248,177,15,.35)"/>'
    b += ''.join(star(42 + k * 13, 102, 5.6, '#F8B10F') for k in range(5)) + t(112, 105.500, '4.9', 9.5, '#fff', ls=0)
    b += bar(36, 116, 110, 'rgba(255,255,255,.7)') + bar(36, 126, 78, 'rgba(255,255,255,.35)', 4)
    b += f'<rect x="36" y="140" width="114" height="24" rx="12" fill="url(#gd{u})"/>' + t(93, 156, 'CALL', 10, '#1A1200', anchor='middle', ls=2)
    b += '<path d="M132 150l0 22 6-6 5 11 4-2-5-11 8 0z" fill="#fff" stroke="#0C1230" stroke-width="1.2"/>'
    b += panel(u, 176, 16, 142, 158, 14, 'rgba(163,181,242,.3)', 'rgba(14,20,48,.7)') + t(190, 36, 'YOU', 9, '#8E9BC8', ls=1.6)
    b += '<rect x="190" y="44" width="114" height="44" rx="7" fill="none" stroke="rgba(163,181,242,.35)" stroke-width="1.2" stroke-dasharray="4 4"/>' + t(247, 70, 'NO PHOTOS', 8, '#8E9BC8', anchor='middle', ls=1.4)
    b += ''.join(star(196 + k * 13, 102, 5.6, '#F8B10F' if k < 2 else 'rgba(163,181,242,.25)') for k in range(5)) + t(266, 105.500, '2.1', 9.5, '#8E9BC8', ls=0)
    b += bar(190, 116, 84, 'rgba(163,181,242,.35)') + bar(190, 126, 50, 'rgba(163,181,242,.2)', 4)
    b += '<rect x="190" y="140" width="114" height="24" rx="12" fill="none" stroke="rgba(163,181,242,.35)" stroke-width="1.2"/>'
    return wrap(u, 'Two business listings side by side: theirs has photos, reviews and a call button; yours has none', b)

def p3():
    u = 'c'; b = f'<circle cx="86" cy="60" r="96" fill="url(#gt{u})"/><circle cx="250" cy="110" r="104" fill="url(#gg{u})"/>'
    b += t(24, 26, 'GOOGLE', 9, '#8EE3D0', ls=1.8)
    b += f'<rect x="24" y="36" width="130" height="30" rx="9" fill="rgba(76,192,168,.2)" stroke="#4CC0A8" stroke-width="1.6"/>' + t(36, 55, '1 · YOU', 10, '#fff') + '<path d="M128 51l5 5 9-11" stroke="#8EE3D0" stroke-width="2.4"/>'
    for i, y in enumerate((74, 106)):
        b += panel(u, 24, y, 130, 26, 9, 'rgba(163,181,242,.3)', 'rgba(14,20,48,.6)') + t(36, y + 17, f'{i + 2} · OTHER', 9, '#8E9BC8')
    b += '<path d="M160 51h18" stroke="rgba(163,181,242,.5)" stroke-width="1.4" stroke-dasharray="2 4"/>'
    b += t(190, 26, 'AI ASSISTANT', 9, '#FFD98A', ls=1.8)
    b += f'<path d="M190 36h126a8 8 0 0 1 8 8v96a8 8 0 0 1-8 8h-84l-18 18v-18h-24a8 8 0 0 1-8-8v-96a8 8 0 0 1 8-8z" fill="url(#pn{u})" stroke="#F8B10F" stroke-width="1.6"/>'
    b += t(202, 58, '“Who should I call?”', 9.5, '#fff', ls=0) + '<path d="M202 68h102" stroke="rgba(163,181,242,.3)"/>'
    b += f'<rect x="202" y="78" width="102" height="24" rx="7" fill="rgba(248,177,15,.16)" stroke="rgba(248,177,15,.6)"/>' + t(212, 94, 'Another Co.', 10, '#FFD98A', ls=0)
    b += t(202, 120, 'or someone else.', 9, '#B4C0E0', ls=0, w=500) + t(202, 137, 'You are not named.', 9, '#8E9BC8', ls=0, w=500)
    return wrap(u, 'Google lists you first, while an AI assistant names another company', b)

def p4():
    u = 'd'; b = f'<circle cx="212" cy="52" r="96" fill="url(#gg{u})"/>'
    b += ''.join(f'<path d="M34 {y}h282" stroke="rgba(163,181,242,.14)"/>' for y in (40, 76, 112, 148))
    b += '<path d="M34 22v126h282" stroke="rgba(163,181,242,.5)" stroke-width="1.4"/>'
    up = 'M40 132 L72 122 L100 126 L130 100 L160 84 L190 62 L212 50'; dn = 'M212 50 L232 108 L262 120 L290 126 L312 130'
    b += f'<path d="{up} L212 148 L40 148 Z" fill="url(#ar{u})"/><path d="{dn} L312 148 L212 148 Z" fill="url(#ag{u})"/>'
    b += f'<path d="{up}" stroke="#4CC0A8" stroke-width="3"/><path d="{dn}" stroke="#F8B10F" stroke-width="3"/>'
    b += '<path d="M212 26v122" stroke="#F8B10F" stroke-width="1.2" stroke-dasharray="3 4"/><circle cx="212" cy="50" r="12" fill="rgba(248,177,15,.25)"/><circle cx="212" cy="50" r="6" fill="#F8B10F" stroke="#FFE7AE" stroke-width="1.5"/>'
    b += f'<rect x="222" y="16" width="94" height="22" rx="11" fill="rgba(248,177,15,.16)" stroke="#F8B10F" stroke-width="1.2"/>' + t(269, 31, 'GOOGLE UPDATE', 8.5, '#FFD98A', anchor='middle', ls=1)
    b += t(34, 168, 'RANKINGS, WEEK BY WEEK', 8.5, '#8E9BC8', ls=1.4) + t(316, 168, '− 62%', 10, '#FFD98A', anchor='end', ls=.4)
    return wrap(u, 'A rankings chart that climbs week by week, then falls sharply on the day of a Google update', b)

def p5():
    u = 'e'; b = f'<circle cx="92" cy="95" r="110" fill="url(#gt{u})"/>'
    b += panel(u, 22, 16, 142, 158, 14, '#4CC0A8', sw=1.6) + t(36, 38, 'A FAIR QUOTE', 9, '#8EE3D0', ls=1.5)
    for i, s in enumerate(('What is mapped', 'What ships first', 'What is in writing')):
        y = 56 + i * 34
        b += f'<circle cx="46" cy="{y + 8}" r="10" fill="url(#tl{u})"/><path d="M41 {y + 8}l4 4 7-8" stroke="#0C1230" stroke-width="2.2"/>' + t(64, y + 12, s, 9.5, '#fff', ls=0, w=600, fam=S)
    b += '<path d="M36 156h114" stroke="rgba(76,192,168,.4)"/>'
    b += panel(u, 176, 16, 142, 158, 14, 'rgba(248,177,15,.7)', 'rgba(14,20,48,.7)') + '<rect x="176" y="16" width="142" height="158" rx="14" fill="none" stroke="#0A0F24" stroke-width="2" stroke-dasharray="0 9"/>' + t(190, 38, 'THE OTHER KIND', 9, '#FFD98A', ls=1.5)
    for i in range(3):
        y = 56 + i * 34
        b += f'<circle cx="200" cy="{y + 8}" r="10" fill="rgba(248,177,15,.14)" stroke="rgba(248,177,15,.6)" stroke-width="1.2"/>' + t(200, y + 12, '?', 11, '#FFD98A', anchor='middle', ls=0) + bar(218, y + 5, 80 - i * 14, 'rgba(163,181,242,.35)', 6)
    return wrap(u, 'Two quotes: one states what is mapped, what ships first and what is in writing; the other leaves all three blank', b)

def p6():
    u = 'f'; b = f'<circle cx="170" cy="36" r="118" fill="url(#gg{u})"/>'
    b += panel(u, 30, 14, 280, 32, 16, '#F8B10F', sw=1.6) + '<circle cx="52" cy="30" r="6.5" stroke="#FFD98A" stroke-width="2"/><path d="M56.500 34.500l5 5" stroke="#FFD98A" stroke-width="2"/>' + t(72, 34, 'my listing was suspended', 10.5, '#fff', ls=.2)
    rows = (('G', 'Google crawled it, won’t index', 0), ('L', 'Listing suspended after an edit', 1), ('P', 'Page one, then gone', 0), ('S', 'Schema shows, stars don’t', 0))
    for i, (k, s, on) in enumerate(rows):
        y = 58 + i * 30
        b += panel(u, 30, y, 280, 24, 8, '#F8B10F' if on else 'rgba(163,181,242,.3)', 'rgba(248,177,15,.14)' if on else None, 1.4 if on else 1)
        b += f'<rect x="38" y="{y + 4}" width="16" height="16" rx="5" fill="{"url(#gd" + u + ")" if on else "rgba(163,181,242,.25)"}"/>' + t(46, y + 16, k, 9, '#1A1200' if on else '#fff', anchor='middle', ls=0)
        b += t(64, y + 16, s, 9.5, '#fff' if on else '#B4C0E0', ls=0, w=600 if on else 500, fam=S) + f'<path d="M294 {y + 7}l5 5-5 5" stroke="{"#FFD98A" if on else "rgba(163,181,242,.5)"}" stroke-width="1.8"/>'
    return wrap(u, 'A search of the problem encyclopedia with one matching entry highlighted', b)

PROBLEM_ART = [p1(), p2(), p3(), p4(), p5(), p6()]
