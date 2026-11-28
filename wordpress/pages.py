"""Inner pages, one spec each. build.py turns a spec into an Elementor page with the same widgets the home page uses.

Rules every spec follows: one lead keyword (qa/keyword-map.csv), a 40 to 60 word answer under the H1, question H2s,
facts only from the signed register, one specific example, a dated original figure, FAQs of 40 to 60 words, a clear next step."""
PUB = ('2026-11-28', '28 Nov 2026')

def make(h):
    W, H, T, B, C, G, S, card, link, box, gap = (h[k] for k in ('W', 'H', 'T', 'B', 'C', 'G', 'S', 'card', 'link', 'box', 'gap'))
    ART = h['PROBLEM_ART']

    def hero(crumbs, eyebrow, h1, answer, after='', ctas=(('Book a discovery call', '/book/'), ('Ask a question', '/ask/')), note='20 to 30 minutes with Thomas. No audit to buy first.'):
        trail = ' <span aria-hidden="true">›</span> '.join(('<a href="%s">%s</a>' % (u, t)) if u else '<span aria-current="page">%s</span>' % t for t, u in crumbs)
        els = [T('<nav aria-label="Breadcrumb"><p>%s</p></nav>' % trail, 'rs-crumbs', mb=18), H(eyebrow, 'p', 'eyebrow'), H(h1, 'h1', mb=22), T('<p>%s</p>' % answer, 'lead', mb=0, eid='answer')]
        if after: els.append(T('<p>%s</p>' % after, 'lead-after', mt=18))
        btns = [B(ctas[0][0], ctas[0][1])] + [B(t, u, 'rsm-btn rsm-btn-ghost') for t, u in ctas[1:]]
        els += [C(btns, 'rs-actions', 'row', flex_gap=gap(14), flex_wrap='wrap', margin=box(28, 0, 12, 0)), T('<p>%s</p>' % note, 'small', mb=0)]
        return S([C(els, 'rs-pagehero-in')], 'rs-sec rs-pagehero', pad=(72, 72), pad_m=(44, 48))

    def sec(eyebrow, h2, paras, *content, eid='', more=None):
        intro = [H(eyebrow, 'p', 'eyebrow'), H(h2, 'h2', mb=18)] + [T('<p>%s</p>' % p, 'lead' if i == 0 else '', mb=(0 if i == len(paras) - 1 and not more else None)) for i, p in enumerate(paras)]
        if more: intro.append(B(more[0], more[1], 'rs-more', mb=0))
        return S([C(intro, 'rs-intro rv', margin=box(0, 0, 40 if content else 0, 0), width={'unit': 'px', 'size': 800, 'sizes': []})] + list(content), eid=eid)

    def faq(eyebrow, h2, lead, items):
        return S([G([C([H(eyebrow, 'p', 'eyebrow'), H(h2, 'h2'), T('<p>%s</p>' % lead, 'lead', mt=16, mb=0)], 'rv'), W('rsm-faq', {'items': [{'_id': h['uid'](), 'q': q, 'a': a.replace('\n', '\n\n')} for q, a in items], 'open_first': 'yes', 'schema': 'yes'}, 'rv')],
                    'minmax(0,5fr) minmax(0,7fr)', 'minmax(0,1fr)', 'minmax(0,1fr)', g=(32, 56))], eid='questions')

    def closing(h2, text, small, dates=PUB):
        meta = 'Published %s · Last reviewed %s by <a href="/thomas-dsouza/">Thomas D’Souza</a>, Founder · <a href="/about/editorial-policy/">How we write and check</a>' % (dates[1], dates[1])
        return S([C([W('image', {'image': {'url': '{{media:logo}}', 'id': '{{mediaid:logo}}', 'alt': 'Relevant Search Media'}, 'image_size': 'full'}, 'rs-disc', mb=26), H(h2, 'h2'), T('<p>%s</p>' % text, 'lead', mt=20, mb=0),
                   C([B('Book a discovery call', '/book/'), B('Call +1 (202) 609-6641', 'tel:+12026096641', 'rsm-btn rsm-btn-ghost')], 'rs-actions', 'row', flex_gap=gap(14), flex_wrap='wrap', flex_justify_content='center', margin=box(30, 0, 12, 0)),
                   T('<p>%s</p>' % small, 'small'), T('<p>%s</p>' % meta, 'small rs-meta', mt=40)], 'rs-closing-in', flex_align_items='center')], 'rs-closing', pad=(110, 110), pad_m=(72, 72))

    def quote(text):
        """The author's verdict for this page, as a quotation an assistant can lift."""
        return T('<blockquote><p>“%s”</p><footer><cite>Thomas D’Souza</cite>, Founder, Relevant Search Media</footer></blockquote>' % text, 'quote rv', mt=48)

    def trust():
        """Who wrote this, what stands behind it, what it costs to try. The same on every inner page by design (class rs-boiler)."""
        who = C([H('Who is behind this page', 'p', 'eyebrow'), H('Written and checked by Thomas D’Souza', 'h2', mb=14),
                 T('<p>Thomas D’Souza is the founder of Relevant Search Media and the author of the D’Souza Equation. He has worked in digital marketing since 2010.</p>'
                   '<p>Relevant Search Media was founded in 2020. The team works from New Delhi, India, on US hours, for businesses across the United States. Call <a href="tel:+12026096641">+1 (202) 609-6641</a>.</p>', mb=14),
                 B('About Thomas', '/thomas-dsouza/', 'rs-more', mb=0)], 'rs-trust-who')
        proof = C([T('<ul class="rs-proof"><li><b>900+</b> businesses served since 2020. <span>Fact register C1</span></li>'
                     '<li><b>About 400</b> projects, 90% successful. Successful means the mapped searches reached page one of Google. <span>Fact register C3</span></li>'
                     '<li><b>413</b> numbered checks, published in full. <span>The D’Souza Standard, v1.0, 23 Nov 2026</span></li></ul>', mb=16),
                   T('<p><b>Two commitments, in writing.</b> Everything ships, or that 15-day period is free. Half on page one by month four, or we keep working at no charge.</p>'
                     '<p>Every plan is month to month, with no setup fee. Prices are discussed on the call, not listed here.</p>', 'rs-trust-terms', mb=14),
                   B('Read the two commitments', '/commitments/', 'rs-more', mb=0)], 'rs-trust-proof glass')
        return S([G([who, proof], 'minmax(0,5fr) minmax(0,7fr)', 'minmax(0,1fr)', 'minmax(0,1fr)', g=(32, 56), cls='rs-boiler', align='center')], eid='trust')

    def table(caption, heads, rows):
        return W('rsm-table', {'caption': caption, 'h1': heads[0], 'h2': heads[1], 'h3': heads[2], 'rows': [{'_id': h['uid'](), 'a': a, 'b': b, 'c': c} for a, b, c in rows]}, 'rv rs-plain-table')

    def page(key, path, title, desc, data, parent='', words_note=''):
        slug = path.strip('/').split('/')[-1]
        return {'key': key, 'slug': slug, 'parent': parent, 'title': title.split(' | ')[0], 'seo': {'title': title, 'description': desc, 'image': '{{media:og}}', 'published': PUB[0], 'reviewed': PUB[0], 'images': ['{{media:og}}']}, 'data': data}

    P = []
    # ------------------------------------------------------------------ /problems/
    five = [
        ('“Nobody can find my business online.”', 'You search your own trade and city and someone else comes up. <b>What it means:</b> engines cannot yet read what you do and where.', '/problems/not-showing-up-on-google/'),
        ('“People find me, but they don’t pick me.”', 'The listing gets seen and the phone stays quiet. <b>What it means:</b> you are shown, and a rival wins the choice.', '/problems/not-getting-leads/'),
        ('“Google shows me. ChatGPT doesn’t.”', 'You rank, yet an AI assistant names another company. <b>What it means:</b> nothing outside your own site confirms you.', '/problems/not-recommended-by-chatgpt/'),
        ('“I was ranking, and I lost it.”', 'Calls fell from one week to the next. <b>What it means:</b> a drop with a start date has a cause that can be found.', '/problems/traffic-dropped/'),
        ('“I’m being quoted and don’t know if it’s fair.”', 'Two agencies, two very different prices. <b>What it means:</b> the work has not been written down, so it cannot be compared.', '/problems/seo-cost/'),
    ]
    P.append(page('problems', '/problems/', 'SEO Problems: Find Yours, Check It | Relevant Search Media',
        'The five SEO problems business owners bring us, and how to tell which one is yours. Each comes with a first check you can run yourself in ten minutes.', [
        hero([('Home', '/'), ('What’s wrong?', '')], 'What’s wrong?', 'SEO problems: find yours and the first thing to check',
             'Most SEO problems are one of five: nobody can find the business, people find it and pick someone else, Google shows it and AI does not, rankings were lost, or a quote cannot be judged. Each has a first check you can run yourself in ten minutes, before you pay anyone.',
             'Start with the one that sounds like you.'),
        sec('The five problems', 'Which of the five SEO problems is yours?', ['Owners describe the same five search marketing problems in their own words. Each card goes to a page that answers that problem completely, in plain language.'],
            G([card('problem', svg=ART[i], title=t, text=x, link_text='Read the full answer', link=link(u)) for i, (t, x, u) in enumerate(five)]
              + [card('problem', svg=ART[5], tag='Something else?', title='A narrower problem than these five.', text='A suspended listing, a page Google will not index, reviews that vanished. Ask it in your own words and we point you to the answer.', link_text='Ask a question', link=link('/ask/'), highlight='yes')], 3, 2, 1, cls='rs-probs'), eid='five'),
        sec('Tell them apart', 'How do I tell which SEO problem I have?', ['Go by what you see, not by what you were told. The table matches each symptom to the likely problem and to the first thing worth checking.', 'One business can have two of these at once. Fix them in the order shown, because being found comes before being chosen.'],
            table('Symptoms of the five SEO problems, the likely cause and the first check', ('What you see', 'Likely problem', 'First check'), [
                ('You search your trade and city and you are not there', 'Engines cannot read the business yet', 'Search in a private window, on a phone, from inside your service area'),
                ('You show up, the phone stays quiet', 'The listing or page does not win the choice', 'Compare your photos, reviews and answers with the top three'),
                ('You rank on Google, ChatGPT names a rival', 'Nothing independent confirms you', 'Ask three AI assistants the question a customer would ask'),
                ('Calls fell from one week to the next', 'A drop with a date', 'Match the start date to Google’s published updates'),
                ('Two quotes, very different prices', 'The work is not written down', 'Ask what is mapped, what ships first and what is in writing'),
            ]), more=('See how the first fifteen days fix them', '/dsouza-equation/method/'), eid='tell'),
        sec('Three causes', 'Why is my SEO not working? Three causes.', ['When an owner asks “why is my SEO not working?”, the answer is nearly always one of three failed checks. Every engine takes a person’s question and names the most relevant business it can trust, and it decides with the same three checks.', 'Those checks are the D’Souza Equation: Relevance = Read × Confirm × Choose. That is why one fix works on Google, on Maps and in an AI answer.'],
            G([card('clause', number='1', title='Read fails: you cannot be found.', text='The engine cannot tell plainly what the business is, where it works and what it answers. Nothing else counts until this passes.'),
               card('clause', number='2', title='Confirm fails: AI names someone else.', text='Your own site says it, but listings, reviews and mentions elsewhere do not say the same thing. The engine will not vouch for you.'),
               card('clause', number='3', title='Choose fails: found, then passed over.', text='People see you and then click, call or book someone else. Engines watch that choice and move the chosen business up.')], 3, 1, 1),
            quote('An SEO problem is never “Google hates my site.” It is one of three checks failing, and you can find out which one in ten minutes.'),
            more=('Read the equation in full', '/dsouza-equation/'), eid='causes'),
        sec('Before you pay', 'What should I check before I pay anyone to fix SEO problems?', ['Five checks, about ten minutes, no tools to buy. They tell you which problem you have, and they make any quote easier to judge.'],
            G([card('day', number='Check 1', title='Search yourself', text='Private window, your trade plus your city. Note whether you are on page one, on the map, or neither.'),
               card('day', number='Check 2', title='Read your listing as a stranger', text='Photos, hours, services, reviews and replies. Would you call this business?'),
               card('day', number='Check 3', title='Ask an AI assistant', text='Type the question a customer would ask. See which business it names, and why.'),
               card('day', number='Check 4', title='Date the drop', text='If calls fell, find the week it began. A date turns a mystery into a cause.'),
               card('day', number='Check 5', title='Ask three things of a quote', text='What will be mapped, what ships in the first fifteen days, and what is in writing.')], 5, 2, 1, g=(16, 16)),
            T('<p>For example, a plumber, a roofer or a dentist in Miami would start with searches such as “plumber near me” and “emergency plumber miami”. Our own map for plumbing in that city holds 166 searches like these (v4, 18 Nov 2026).</p>', 'small rs-note', mt=22, mb=18),
            B('See your own trade and city', '/searches/', 'rs-more', mb=0), eid='checks'),
        sec('Everything else', 'What if mine is one of the narrower search marketing problems?', ['Then it is probably one of these: a suspended Google listing, a page Google crawled and will not index, reviews that vanished, a redesign that lost its rankings. The encyclopedia holds 1,822 entries so far, one per problem, each signed by the specialist who checked it.', 'Entries are being published here in batches. Until yours is up, the Ask page finds the closest answer, and a discovery call covers the rest.'],
            C([B('Ask a question', '/ask/'), B('See all 413 checks', '/dsouza-equation/standard/', 'rs-more')], 'rs-actions', 'row', flex_gap=gap(14), flex_wrap='wrap', flex_align_items='center', margin=box(0, 0, 0, 0)), eid='else'),
        faq('Questions about SEO problems', 'What do owners ask about SEO problems?', 'Asked on discovery calls, answered here the same way. For anything else, use the <a href="/ask/">Ask page</a>.', [
            ('Which SEO problem should I fix first?', 'Fix being found before being chosen. If engines cannot read what your business is and where it works, better photos and more reviews change nothing, because nobody is shown the listing.\nStart with Read, then Confirm, then Choose: the order of the D’Souza Equation and the order we work in.'),
            ('Can I fix SEO problems myself?', 'Some of them, yes. Completing your Google Business Profile, answering reviews and stating plainly on your site what you do and where are all things an owner can do.\nThe checks on this page show where you stand. Mapping every search and running all 413 checks is where a team earns its fee.'),
            ('How long does it take to fix an SEO problem?', 'It depends on which one. On our plans, live work goes up by day 5 and the first report arrives on day 15.\nRankings usually start moving between day 30 and day 60. By the end of month four, at least half the searches in your map reach page one of Google, or we keep working at no charge.'),
            ('How do I know if my SEO company is the problem?', 'Ask them three things: which searches they mapped for you, what shipped in the last fifteen days, and where it is logged. A company doing the work can answer in a minute, with links.\nIf the answer is a slide deck or a ranking screenshot, the problem may be the company.'),
            ('Do SEO problems also keep me out of AI answers?', 'Usually, yes. AI assistants draw on the same things search engines read: your site, your listings and what independent sources say about you.\nA business that Google cannot read or confirm is rarely named by ChatGPT, Gemini or Perplexity either. No one can promise an AI placement, so we track it monthly.'),
        ]),
        trust(),
        closing('Bring the problem. <span class="gold">Leave with the plan.</span>', 'A discovery call is 20 to 30 minutes with Thomas. He looks at who Google, Maps and the AI engines name when your customers ask, tells you which of the five problems he sees, and shows you what the first fifteen days would be.', 'No audit to buy first, no trial. One business per trade per city.'),
    ]))
    return P

GATE = {  # what the gate is told about each page: keywords, page type, the specific example and the dated original figure it must carry
    '/problems/': {'kw': 'seo problems;search marketing problems;why is my seo not working', 'type': 'hub', 'example': 'emergency plumber miami', 'original': '166;v4, 18 Nov 2026', 'trade': 'plumber;roofer;dentist'},
}
