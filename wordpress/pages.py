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
                     '<p>Live work by day 5 and a report every 15 days. Every plan is month to month, with no setup fee. Prices are discussed on the call, not listed here.</p>', 'rs-trust-terms', mb=14),
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
            T('<p>For example, a plumber, a roofer or a dentist in Miami would start with searches such as “plumber near me” and “emergency plumber miami”. People search in far more ways than owners expect: our own map counts 166 different searches that plumbers in Miami make when they look for a company like ours (v4, 18 Nov 2026).</p>', 'small rs-note', mt=22, mb=18),
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
    # ------------------------------------------------------------------ /problems/not-showing-up-on-google/
    def steps(items, cols=4):
        return G([card('day', number=n, title=t, text=x) for n, t, x in items], cols, 2, 1, g=(16, 16))
    crumb = lambda name: [('Home', '/'), ('What’s wrong?', '/problems/'), (name, '')]

    P.append(page('not-showing-up-on-google', '/problems/not-showing-up-on-google/', 'Business Not Showing Up on Google | Relevant Search Media',
        'Business not showing up on Google? Run four checks to find the cause in ten minutes. Six causes, each with the fix that works.', [
        hero(crumb('Not showing up on Google'), 'Problem 1 of 5', 'Why is my business not showing up on Google?',
             'Your business is not showing up on Google because Google cannot yet read plainly what it is, where it works and what it answers, or cannot confirm that from anywhere else. The usual causes are an unverified or incomplete Business Profile, a website Google has not indexed, and details that differ from one listing to the next.',
             'Four checks tell you which cause is yours.'),
        sec('The ten-minute check', 'How do I check why my business is not on Google?', ['Run these four checks in order, in a private window so your own history does not flatter the result. Each one rules a cause in or out.'],
            steps([('Check 1', 'Search your exact name', 'Type the business name and city. If nothing of yours appears, Google has no confirmed record of the business.'),
                   ('Check 2', 'Search your trade and city', 'Type what a customer would, such as “roof repair denver”. Note page one and the map separately.'),
                   ('Check 3', 'Search site:yourdomain.com', 'This lists the pages Google holds from your site. No results means the site is not indexed.'),
                   ('Check 4', 'Open your Business Profile', 'Sign in and look at its status: verified, pending, suspended or duplicate.')]),
            T('<p>For example, a roofer in Denver would run Check 2 with “roof repair denver” and “roofing company denver”. Owners search in many ways too: our own map counts 170 different searches roofers in Denver make when they look for a company like ours (v4, 18 Nov 2026).</p>', 'small rs-note', mt=22, mb=18),
            B('See the searches for your trade and city', '/searches/', 'rs-more', mb=0), eid='check'),
        sec('Six causes', 'What are the reasons a business is not on Google?', ['A business not on Google has one of six causes. Match what the four checks showed you to the row, then to the fix.', 'More than one row can apply. Work from the top, because Google has to know the business exists before it can rank it.'],
            table('Why a business does not show up on Google: what you find, the cause and the fix', ('What you find', 'Cause', 'What fixes it'), [
                ('Your name search shows nothing', 'No verified Business Profile', 'Create or claim the profile and complete Google’s verification'),
                ('The profile says suspended', 'A guideline or address problem', 'Correct the profile, then file a reinstatement request'),
                ('site: search returns no pages', 'The site is not indexed', 'Remove the block or noindex tag and submit a sitemap in Search Console'),
                ('Your name shows, your trade and city do not', 'Google cannot tell what you do or where', 'State the service and the area plainly on the site and in the profile'),
                ('You are in search results, not on the map', 'The profile is thin next to nearby rivals', 'Right category, full services, photos, and reviews you reply to'),
                ('Name, address or phone differ between listings', 'Nothing confirms the business', 'Make all three identical on every listing and on the site'),
            ]), more=('How “Read” works in the equation', '/dsouza-equation/read/'), eid='causes'),
        sec('Search and Maps', 'Why is my business not on Google Maps when it shows in search?', ['Search results and the map are ranked separately. Google says local results turn mainly on relevance, distance and prominence: how well the profile matches the search, how far the business is from the searcher, and how well known it is.', 'A business not on Google Maps usually has a profile with the wrong primary category, missing services or few recent reviews. The website can rank while the profile stays invisible.'],
            quote('If Google cannot say in one sentence what you do and where, it will not show you. Fix that sentence first.'),
            more=('What we do for Google Business Profile', '/services/google-business-profile-optimization/'), eid='maps'),
        sec('How long', 'How long does it take to show up on Google?', ['It depends on the cause. A verified, completed profile can appear within days. A new website takes longer: Google says crawling can take from a few days to a few weeks.', 'On our plans the first fixes go live by day 5 and the first report arrives on day 15. Rankings usually start moving between day 30 and day 60.'],
            steps([('Day 1', 'Discover', 'One conversation. We learn the business and collect access.'),
                   ('Day 2 to 3', 'Map and check', 'Every search your customers make is mapped, and the 413 checks are run on your site and listings.'),
                   ('Day 4', 'Plan', 'You see what is wrong, in order, with a 90-day calendar.'),
                   ('Day 5', 'Live', 'The biggest fixes go live and your log opens.')]),
            more=('See the first fifteen days', '/dsouza-equation/method/'), eid='how-long'),
        faq('Questions about not showing up', 'What do owners ask when their business is not on Google?', 'Asked on discovery calls, answered here the same way. For anything else, use the <a href="/ask/">Ask page</a>.', [
            ('Why is my business not on Google when I have a website?', 'Having a website is not the same as being indexed. Google has to find the site, be allowed to read it and decide the pages are worth keeping.\nRun the site: search above. If it returns nothing, the site is blocked, too new, or carries a noindex tag.'),
            ('Why did my business disappear from Google?', 'A business that was showing and then vanished usually has a suspended profile, a site change that blocked Google, or a drop after an update. Each leaves a date.\nCheck the profile status first, then see our page on <a href="/problems/traffic-dropped/">traffic that dropped</a>.'),
            ('Do I have to pay Google to show up?', 'No. Organic results and Maps listings are free, and they are earned by being readable, confirmed and chosen. Ads are a separate, paid placement marked as sponsored.\nA Business Profile costs nothing to create or verify, so a business not on Google is never there for lack of a fee.'),
            ('Is a business not on Google also missing from AI answers?', 'Usually. AI assistants draw on the same sources search engines read: your site, your listings and what others say about you.\nA business Google cannot read is rarely named by ChatGPT, Gemini or Perplexity. No one can promise an AI placement, so we track it monthly.'),
            ('Can you guarantee my business shows up on Google?', 'We commit in writing that at least half the customer searches in your map reach page one of Google by the end of month four, or we keep working at no charge.\nWe do not promise a position on Google Maps or in AI answers, because no one honestly can.'),
        ]),
        trust(),
        closing('Not on Google? <span class="gold">Find out why in one call.</span>', 'A discovery call is 20 to 30 minutes with Thomas. He runs these four checks on your business while you watch, tells you which of the six causes he sees, and shows you what the first fifteen days would fix.', 'No audit to buy first, no trial. One business per trade per city.'),
    ], parent='problems'))
    # ------------------------------------------------------------------ /problems/not-getting-leads/
    P.append(page('not-getting-leads', '/problems/not-getting-leads/', 'Get More Leads for My Business | Relevant Search Media',
        'How to get more leads for my business when people find it and still pick a rival. Four checks show what loses the choice, and what to fix first.', [
        hero(crumb('Found, not picked'), 'Problem 2 of 5', 'How do I get more leads for my business from search?',
             'You get more leads when the listing and the page people already see win the choice. If your business is found and the phone still stays quiet, the cause is almost always what a searcher sees in the first ten seconds: the photos, the reviews, the answers, and how easy it is to call you.',
             'Being found is the engine’s job. Being picked is yours.'),
        sec('The ten-minute check', 'How do I check why people find me and do not pick me?', ['Look at your business the way a stranger does, on a phone, next to the three businesses shown beside you. These four checks take about ten minutes.'],
            steps([('Check 1', 'Open your listing as a stranger', 'Private window, your trade and city. Look at the photos, the hours, the services and the first two reviews.'),
                   ('Check 2', 'Compare with the three beside you', 'Count their reviews and yours. Note the rating, the date of the latest review and whether the owner replied.'),
                   ('Check 3', 'Tap to call', 'On a phone, tap your own call button. It should ring the right number in one tap, during the hours shown.'),
                   ('Check 4', 'Read your first screen', 'Open your page. Without scrolling, it should say what you do, where, and what to do next.')]),
            T('<p>For example, a dentist in Chicago would run Check 2 against the three practices shown for “emergency dentist chicago”. Owners look for help in many ways as well: our own map counts 186 different searches dentists in Chicago make when they look for a company like ours (v4, 18 Nov 2026).</p>', 'small rs-note', mt=22, mb=18),
            B('See the searches for your trade and city', '/searches/', 'rs-more', mb=0), eid='check'),
        sec('Six causes', 'Why is my website not getting leads?', ['A website not getting leads is losing people at one of six points. Match what you see to the row, then to the fix.', 'Start at the top. The listing is seen before the website, so it loses more people than any page does.'],
            table('Why a business is found and not chosen: what you see, the cause and the fix', ('What you see', 'Cause', 'What fixes it'), [
                ('Many views of the listing, few calls', 'The listing loses the side-by-side comparison', 'Recent photos, every service listed, reviews you reply to'),
                ('Visits to the site, no enquiries', 'The first screen does not say what, where and what next', 'One plain sentence and one clear action above the fold'),
                ('Calls come, for the wrong jobs', 'The page draws the wrong searches', 'Map searches by what the person wants and write for the jobs you want'),
                ('People start the form and leave', 'The form asks for too much, or is broken', 'Ask only what you need and test it every month'),
                ('Only the cheapest work comes in', 'Nothing shows why you are worth more', 'Proof beside the button: results, guarantees, licences'),
                ('Good reviews, all of them old', 'A rival’s latest review is from this week', 'Ask every customer, and reply to each review'),
            ]), more=('How “Choose” works in the equation', '/dsouza-equation/choose/'), eid='causes'),
        sec('The call button', 'How do I get more calls from Google?', ['Most local searches end on the listing, not on a website. To get more calls from Google, the Business Profile has to answer the three things a caller checks: are you open, do you do this job, and do other people trust you.', 'That means correct hours, the right primary category, every service named, and recent reviews with replies. Engines then watch who gets chosen and show that business more often.'],
            quote('Being found is the engine’s job. Being picked is yours. The engine only keeps showing the business that people pick.'),
            more=('What we do for Google Business Profile', '/services/google-business-profile-optimization/'), eid='calls'),
        sec('Counting leads', 'What counts as a lead, and how is it measured?', ['A lead is a call, a form or a message from someone who wants the work you do, in the area you serve. Clicks and impressions are not leads.', 'On our plans every item that ships is logged with its link. Every 15 days you get a report with the Relevance Rate: the share of leads you confirm were relevant.'],
            steps([('Every day', 'Work, logged with its link', 'Each item goes in your log the day it goes live.'),
                   ('Every 15 days', 'A report and the Relevance Rate', 'What moved, what came in, and which leads you confirm were relevant.'),
                   ('Every month', 'The map re-read', 'New searches and new engines are added as rows.'),
                   ('Always', 'Month to month', 'The site, the content and every account stay yours.')]),
            more=('What we do for lead generation', '/services/lead-generation/'), eid='counting'),
        faq('Questions about leads', 'What do owners ask about getting more leads?', 'Asked on discovery calls, answered here the same way. For anything else, use the <a href="/ask/">Ask page</a>.', [
            ('How to get more leads for my business without paying for ads?', 'Win the choice on the results you already appear in. Complete the Business Profile, keep photos and reviews recent, and make the first screen of your page say what you do and where.\nAds rent attention by the click. Being the business people pick is an asset you keep.'),
            ('Why do people visit my website and not call?', 'Usually because the first screen makes them work. If a visitor cannot tell within a few seconds what you do, where you do it and how to reach you, they go back and pick the next result.\nPut the phone number and one clear action at the top.'),
            ('How many reviews do I need to get picked?', 'There is no fixed number. What matters is how you compare with the three businesses shown beside you: the count, the rating and how recent the latest review is.\nA steady flow of new reviews, each with a reply, does more than a large old total.'),
            ('Are bought leads better than leads from search?', 'A bought lead is often sold to several businesses at once, and it stops the day you stop paying. A lead from search comes to you alone, from a person who chose you.\nOwners search for leads for sale far more than for service names, which is why this page exists.'),
            ('How soon will I see more leads?', 'On our plans the first fixes go live by day 5 and the first report arrives on day 15. Rankings usually start moving between day 30 and day 60.\nWe do not promise a number of leads. We report the leads that came in and the share you confirm were relevant.'),
        ]),
        trust(),
        closing('Found, but not picked? <span class="gold">See why in one call.</span>', 'A discovery call is 20 to 30 minutes with Thomas. He opens your listing beside the three businesses shown next to you, tells you where the choice is being lost, and shows you what the first fifteen days would fix.', 'No audit to buy first, no trial. One business per trade per city.'),
    ], parent='problems'))
    # ------------------------------------------------------------------ /problems/not-recommended-by-chatgpt/
    P.append(page('not-recommended-by-chatgpt', '/problems/not-recommended-by-chatgpt/', 'Get Recommended by ChatGPT | Relevant Search Media',
        'Get recommended by ChatGPT by giving it facts it can read and sources that confirm them. Four checks show why AI names a rival, and what to fix.', [
        hero(crumb('Google shows me, AI doesn’t'), 'Problem 3 of 5', 'How do I get recommended by ChatGPT as a local business?',
             'To get recommended by ChatGPT, a business needs facts an assistant can read and independent sources that say the same thing. When Google shows you and an AI assistant names a rival, the cause is nearly always the second part: nothing outside your own website confirms who you are and what you do.',
             'Ask it yourself first. It takes ten minutes.'),
        sec('The ten-minute check', 'How do I check whether I show up in ChatGPT?', ['Ask the assistants what a customer would ask, and read the answers the way a customer would. Use a fresh chat each time so earlier questions do not steer the reply.'],
            steps([('Check 1', 'Ask the customer’s question', 'In ChatGPT, type the question a customer would, with your trade and city. Note every business it names.'),
                   ('Check 2', 'Ask two more assistants', 'Put the same question to Gemini and Perplexity. One answer proves little; three show a pattern.'),
                   ('Check 3', 'Ask about your business by name', 'Type “What do you know about” and your business name. Write down anything wrong or missing.'),
                   ('Check 4', 'Read the sources', 'Where an assistant shows its sources, open them. Those are the places you need to be named.')]),
            T('<p>For example, a lawyer in New York would run Check 1 with “divorce lawyer in new york” and note who is named. Owners ask in many ways too: our own map counts 211 different searches law firms in New York make when they look for a company like ours (v4, 18 Nov 2026).</p>', 'small rs-note', mt=22, mb=18),
            B('See who AI names, by trade and city', '/ai-recommendation-index/', 'rs-more', mb=0), eid='check'),
        sec('Six causes', 'Why is AI not recommending my business?', ['When AI is not recommending my business, owners often assume the assistant is random. It is not: each of these six answers points to a cause.', 'Match what the assistant said to the row. The fix is rarely on your own website alone.'],
            table('Why an AI assistant names another business: what it says, the cause and the fix', ('What the assistant does', 'Cause', 'What fixes it'), [
                ('Names rivals and never you', 'Few independent sources mention you', 'Be listed and mentioned where it reads: directories, review sites, local press, trade bodies'),
                ('Names you with wrong details', 'The web holds conflicting facts about you', 'Make name, address, phone and services identical everywhere'),
                ('Says it has no information', 'Your site is hard to read, or says little', 'A plain facts page, question-led answers, structured data, AI crawlers allowed'),
                ('Names you for the wrong service', 'The site does not say plainly what you do', 'One page per service, each opening with the answer'),
                ('Google ranks you, the assistant does not', 'Ranking is not the same as being confirmed', 'Reviews on more than one platform and mentions from others'),
                ('Named you last month, not this month', 'Answers vary from run to run', 'Track the same questions monthly; never judge on one reply'),
            ]), more=('How “Confirm” works in the equation', '/dsouza-equation/confirm/'), eid='causes'),
        sec('What gets you named', 'What makes an AI assistant name one business over another?', ['An assistant does the same job as a search engine: it takes a person’s question and names the most relevant business it can trust. It gets there with the three checks in the D’Souza Equation.', 'Read is your own site. Confirm is everyone else. Choose is what real customers did.'],
            G([card('clause', number='1', title='Read: facts it can lift.', text='Plain sentences that say who you are, what you do, where and for whom. Questions as headings, answers directly under them.'),
               card('clause', number='2', title='Confirm: others say the same.', text='Listings, reviews, press and profiles that match your site, on sources the assistant already trusts.'),
               card('clause', number='3', title='Choose: people picked you.', text='Recent reviews, replies and repeat customers. Signs that naming you would be a safe answer.')], 3, 1, 1),
            quote('An AI assistant will not vouch for a business it has only heard about from the business itself.'),
            more=('What we do for AI SEO', '/services/ai-seo/'), eid='named'),
        sec('No guarantees', 'Can anyone guarantee a ChatGPT recommendation?', ['No. Nobody outside the companies that build these assistants controls what they answer, and the same question can return different names on different days. Anyone selling a guaranteed AI placement is selling something they do not own.', 'What can be done is the work the assistants draw on, and honest tracking. Our AI Recommendation Index records who ChatGPT, Gemini and Perplexity name for each trade in each city, and is re-run every month.'],
            C([B('Open the AI Recommendation Index', '/ai-recommendation-index/'), B('Read the two commitments', '/commitments/', 'rs-more')], 'rs-actions', 'row', flex_gap=gap(14), flex_wrap='wrap', flex_align_items='center', margin=box(0, 0, 0, 0)), eid='guarantee'),
        faq('Questions about AI answers', 'What do owners ask about being named by AI?', 'Asked on discovery calls, answered here the same way. For anything else, use the <a href="/ask/">Ask page</a>.', [
            ('How to get my business recommended by ChatGPT if it is new?', 'Start with what the assistant can read and check. Publish a plain facts page, complete your Google Business Profile, and get listed on the directories and review sites your trade uses.\nA new business has few mentions, so consistency matters most: the same name, address, phone and services everywhere.'),
            ('Does ChatGPT use Google rankings?', 'Not directly. ChatGPT can search the web when a question needs current information, and it also draws on what many sources say about a business.\nRanking well makes it more likely your pages are among those it reads. It is not the same as being named in the answer.'),
            ('Do I need an llms.txt file?', 'It helps and costs little. An llms.txt file is a plain text page that tells AI systems what your site is and where its key pages are.\nIt is not a ranking switch, and not every assistant reads it. We publish one on this site and on every client site.'),
            ('How often do AI answers change?', 'Often. The same question can name different businesses on different days, and for different people. That is why one screenshot proves very little.\nWe put the same questions to the same assistants every month, so the trend is visible and one lucky answer is not mistaken for progress.'),
            ('What is the AI Recommendation Index?', 'It is our public record of who ChatGPT, Gemini and Perplexity name for each trade in each city, re-run every month. The first run covers plumbing in the ten launch cities.\nIt shows where a business stands today, and whether the work is moving the answer.'),
        ]),
        trust(),
        closing('Google shows you. <span class="gold">AI names someone else.</span>', 'A discovery call is 20 to 30 minutes with Thomas. He asks three assistants the question your customers ask, shows you who they name and why, and tells you what the first fifteen days would change.', 'No audit to buy first, no trial. One business per trade per city.'),
    ], parent='problems'))
    # ------------------------------------------------------------------ /problems/traffic-dropped/
    P.append(page('traffic-dropped', '/problems/traffic-dropped/', 'Website Traffic Dropped Suddenly | Relevant Search Media',
        'Website traffic dropped suddenly? Date the drop and match it to a cause in ten minutes. Seven causes, the check for each, and what fixes it.', [
        hero(crumb('Ranking, then lost it'), 'Problem 4 of 5', 'Website traffic dropped suddenly: how do I find the cause?',
             'When website traffic dropped suddenly, the first job is to find the week it began. A drop with a start date has a cause: a Google update, a change made to the site, a lost listing, or tracking that broke. Match the date to what changed that week and the cause is usually plain within ten minutes.',
             'Date it first. Everything else follows from the date.'),
        sec('The ten-minute check', 'How do I check why my traffic dropped?', ['Do these four checks in order. Each one narrows the cause, and none needs a paid tool.'],
            steps([('Check 1', 'Date the drop', 'In your analytics or call log, find the week the fall began. Write the date down.'),
                   ('Check 2', 'See what fell', 'In Search Console, compare the weeks before and after. Is it every page, or a few? Search only, or all visits?'),
                   ('Check 3', 'Match Google’s updates', 'Open Google’s Search Status Dashboard and look for a ranking update in that week.'),
                   ('Check 4', 'List your own changes', 'A redesign, a new plugin, a host move, changed addresses, an edited listing: anything from that week.')]),
            T('<p>For example, an HVAC company in Dallas whose calls fell in one week would check “hvac repair dallas” before and after that date. That is one search among many. Our own map holds 165 separate searches that HVAC owners in Dallas type when they want a company such as ours (v4, 18 Nov 2026).</p>', 'small rs-note', mt=22, mb=18),
            B('Look up your own trade and city', '/searches/', 'rs-more', mb=0), eid='check'),
        sec('Seven causes', 'Why have my Google rankings dropped?', ['When Google rankings dropped, one of seven things happened. The date and the pattern from your four checks point to the row.', 'Rule out the top three first. They are the ones an owner can cause by accident, and the quickest to put right.'],
            table('Why traffic and rankings fall: the pattern, the cause and the fix', ('The pattern', 'Cause', 'What fixes it'), [
                ('Every page fell on one day', 'The site was blocked or broken', 'Remove the noindex tag or robots block and ask Google to recrawl'),
                ('It fell the week of a redesign or move', 'Addresses changed without redirects', 'Redirect every old address to its new one'),
                ('Visits “fell” and calls did not', 'Tracking broke; traffic did not', 'Put the analytics tag back and compare with Search Console'),
                ('It began the week of a Google update', 'Google re-weighed what it values', 'Compare the pages that fell with those that rose, and improve them'),
                ('Map calls fell, the website held', 'The Business Profile was edited or suspended', 'Check its status and correct or reinstate it'),
                ('A slow slide over months', 'Rivals improved while the site stood still', 'Refresh the pages that matter and earn new reviews and mentions'),
                ('Search Console shows a notice', 'A manual action by Google', 'Fix what the notice names and request a review'),
            ]), more=('See all 413 checks we run', '/dsouza-equation/standard/'), eid='causes'),
        sec('After an update', 'What should I do if I lost rankings after an update?', ['First, do not undo things in a panic. Google says a page that falls after a core update has not necessarily done anything wrong, and that there may be nothing specific to fix.', 'What helps is honest comparison. Open the pages that rose for your searches and ask what they answer that yours does not. Improvements are often recognised over the following weeks and at later updates.'],
            quote('A drop with a date is not bad luck. It is a cause you have not found yet.'),
            more=('How the equation explains a drop', '/dsouza-equation/'), eid='update'),
        sec('How long', 'How long does it take to recover lost traffic?', ['That turns on the cause. A block or a missing redirect is a one-day repair, and the pages come back as Google recrawls them over days or weeks.', 'A fall after an update is slower and nobody can promise its return. On our plans the first fixes go live by day 5 and the first report arrives on day 15.'],
            steps([('Day 1', 'The date', 'On the first call we fix the week the fall began and get access to Search Console.'),
                   ('Day 2 to 3', 'The diagnosis', 'Pages that fell are set beside pages that rose, and the 413 checks are run on both.'),
                   ('Day 4', 'The order of repair', 'You are shown the cause and which fix comes first, second and third.'),
                   ('Day 5', 'Repairs go live', 'The first fixes are published and each one is entered in your log.')]),
            more=('See the first fifteen days', '/dsouza-equation/method/'), eid='how-long'),
        faq('Questions about a drop', 'What do owners ask when traffic falls?', 'The five questions owners ask most once the numbers fall. Something else on your mind? Try the <a href="/ask/">Ask page</a>.', [
            ('Why did my website traffic drop overnight?', 'An overnight fall across the whole site is usually technical: a noindex tag left on after a rebuild, a robots block, an expired certificate or a host problem.\nIf only search visits fell and the site works, look for a Google update or a change to your Business Profile on that date.'),
            ('I lost rankings after an update. Will they come back?', 'Sometimes, and nobody can promise it. Google re-weighs what it values at each update, so pages can return when they improve or when the next update lands.\nIf you lost rankings after an update, compare your pages with the ones that rose and close the gap.'),
            ('Can a website redesign cause a traffic drop?', 'Yes, and it is one of the most common causes. A redesign often changes page addresses, removes text Google relied on, or goes live with a noindex tag still in place.\nKeep the old addresses or redirect each one, and check indexing the day the new site launches.'),
            ('How do I know if Google penalised my site?', 'Open Search Console and look at the Manual actions report. If Google has taken action, it says so there and names the reason.\nMost falls are not penalties. They are updates, technical mistakes or stronger rivals, and each is handled differently.'),
            ('Should I pay for ads until my traffic recovers?', 'Ads can replace lost calls while the cause is fixed, and for some businesses that is the right bridge. They do not repair what caused the fall.\nFind and fix the cause first, or the ads become a permanent cost for a problem that had a cure.'),
        ]),
        trust(),
        closing('Ranking, then gone? <span class="gold">Date it in one call.</span>', 'A discovery call is 20 to 30 minutes with Thomas. He dates the drop with you, matches it against Google’s updates and your own changes, and shows you what the first fifteen days would fix.', 'Nothing to buy before the call. We take one business per trade in each city.'),
    ], parent='problems'))
    # ------------------------------------------------------------------ /problems/seo-cost/
    P.append(page('seo-cost', '/problems/seo-cost/', 'How Much Does SEO Cost? | Relevant Search Media',
        'How much does SEO cost? It depends on what is mapped, what ships and what is in writing. Four questions show whether a quote is fair.', [
        hero(crumb('Is this quote fair?'), 'Problem 5 of 5', 'How much does SEO cost, and is my quote fair?',
             'How much SEO costs depends on three things: how many searches are mapped, how much work ships each month, and what is promised in writing. A price means little until those are stated. A fair quote tells you what will be mapped, what ships in the first fifteen days, and what happens if it does not.',
             'Judge the quote, not the number.'),
        sec('The ten-minute check', 'How do I check an SEO quote in ten minutes?', ['Put these four questions to whoever sent the quote, in writing. A company that does the work answers all four the same day.'],
            steps([('Step 1', 'Ask for the map', 'Ask for the list of searches the work is aimed at, and how many there are. No list means no target.'),
                   ('Step 2', 'Ask for the first fifteen days', 'Ask for named items with dates. “Onboarding” and “strategy” are not items.'),
                   ('Step 3', 'Ask what is in writing', 'Ask what is promised, what happens if it is missed, how you cancel and what you keep.'),
                   ('Step 4', 'Ask to see the log', 'Ask to see a log with links you can open. A monthly PDF of charts is not a log.')]),
            T('<p>For example, a contractor in Atlanta comparing two quotes would ask each agency which searches it mapped, such as “kitchen remodel atlanta”. The map is the measure of the job: ours counts 177 separate searches contractors in Atlanta make when they want a company such as ours (v4, 18 Nov 2026).</p>', 'small rs-note', mt=22, mb=18),
            B('See a map for your trade and city', '/searches/', 'rs-more', mb=0), eid='check'),
        sec('Six ways to charge', 'How does SEO pricing work?', ['SEO pricing comes in six shapes. Each sells something different, so two quotes can differ widely and both be honest.', 'Find the row that matches your quote, then ask the question in the last column.'],
            table('How SEO is priced: the model, what it buys and what to ask', ('How it is priced', 'What you are buying', 'What to ask'), [
                ('A monthly fee', 'Ongoing work, month after month', 'Can I see the list of what shipped last month?'),
                ('A one-off audit or project', 'A report, or one fixed job', 'Who carries out what the audit finds?'),
                ('By the hour', 'Time', 'Is there a cap, and a log of what the hours produced?'),
                ('Per lead', 'Enquiries, often resold', 'Are the leads mine alone, and who owns the page they come from?'),
                ('A ranking guarantee', 'A promise', 'For which searches, on which engine, and what if it is missed?'),
                ('A long contract with a setup fee', 'A commitment from you', 'What do I keep, and what do I owe, if I leave?'),
            ]), more=('How we work, day by day', '/dsouza-equation/method/'), eid='models'),
        sec('What moves the price', 'What makes SEO cost more or less?', ['Three things move the price of honest work. None of them is the agency’s office or its sales deck.'],
            G([card('clause', number='1', title='The size of the map.', text='How many customer searches the work must win. Our plans map 300, 600 or 2,000 of them.'),
               card('clause', number='2', title='The contest in your trade and city.', text='A dentist in Chicago faces more rivals than a dentist in a small town, and each rival is also doing the work.'),
               card('clause', number='3', title='What is already in place.', text='A sound site, complete listings and recent reviews mean less to build. A blocked site or a suspended listing means more.')], 3, 1, 1),
            more=('See all 413 checks', '/dsouza-equation/standard/'), eid='drivers'),
        sec('The fair-quote test', 'Is my SEO quote fair? Three questions.', ['Is my SEO quote fair? It is if it answers three questions: what will be mapped, what ships in the first fifteen days, and what is in writing. A quote that answers all three can be compared with any other.', 'Ours puts two commitments in writing on every plan. Everything ships or that period is free, and half the mapped searches reach page one by month four or we work on at no charge.'],
            quote('A fair quote is one you can check. If you cannot tell what will ship in the first fifteen days, you are not being quoted. You are being sold.'),
            more=('Read the two commitments', '/commitments/'), eid='fair'),
        sec('No price list', 'Why are there no prices on this page?', ['Because a price without a map is a guess. What a plan costs depends on your trade, your city and how many searches have to be won, and we take only one business per trade per city.', 'The price is given on the discovery call, after Thomas has looked at your searches. The call takes 20 to 30 minutes and there is no audit to buy first.'],
            C([B('Book a discovery call', '/book/'), B('Check whether your city is open', '/open-board/', 'rs-more')], 'rs-actions', 'row', flex_gap=gap(14), flex_wrap='wrap', flex_align_items='center', margin=box(0, 0, 0, 0)), eid='no-prices'),
        faq('Questions about cost', 'What do owners ask about the cost of SEO?', 'The questions that come up once a quote is on the table. For anything else, use the <a href="/ask/">Ask page</a>.', [
            ('How much does SEO cost for a small business?', 'It depends on how many searches the business needs to win and how hard its market is. A one-trade business in one city needs a smaller map than a company serving several.\nCompare quotes by what will be mapped and what ships each month, not by the monthly figure alone.'),
            ('Is cheap SEO worth it?', 'Sometimes a low price buys real work on a small map, and that can be right for a small business. Often it buys a monthly report and little else.\nAsk the four questions on this page. Cheap work that ships and is logged beats expensive work that cannot be shown.'),
            ('Why do SEO quotes vary so much?', 'Because they are rarely quoting the same thing. One agency prices a large map and daily work; another prices a few pages and a report.\nUntil each states what is mapped, what ships and what is in writing, the two numbers cannot be compared.'),
            ('Do I have to sign a long contract?', 'Not with us. Every plan is month to month, with no setup fee, and you cancel by email.\nYou keep the website, the content, the listings and every account from day one. Nothing is held back and nothing is charged to leave.'),
            ('What should an SEO proposal include?', 'The list of searches it targets, the items that ship in the first fifteen days, what is promised in writing, how the work is logged, and what you keep if you leave.\nA proposal missing any of the five is missing the part that lets you hold the agency to it.'),
        ]),
        trust(),
        closing('Holding a quote? <span class="gold">Check it in one call.</span>', 'A discovery call is 20 to 30 minutes with Thomas. Bring the quote you were given. He tells you what it covers, what it leaves out, and what the first fifteen days of real work would look like for your trade and city.', 'Nothing to pay for the call. One business per trade per city.'),
    ], parent='problems'))
    # ------------------------------------------------------------------ /ask/
    P.append(page('ask', '/ask/', 'Ask an SEO Question | Relevant Search Media',
        'Ask an SEO question in your own words. This page finds the answer among every question answered on the site, each one checked by Thomas D’Souza.', [
        hero([('Home', '/'), ('What’s wrong?', '/problems/'), ('Ask a question', '')], 'Ask', 'Ask an SEO question and find the page that answers it',
             'Ask an SEO question in your own words and this page points you to the answer. Every answer on this site is written once, checked against one signed fact register and reviewed by Thomas D’Souza. If no page answers your question yet, send it to us and it gets one.',
             'Type below. Nothing is sent anywhere until you choose to send it.', ctas=(('Book a discovery call', '/book/'), ('Ask a question', '#ask'))),
        sec('Find the answer', 'What is your question?', ['Type it the way you would say it. The list narrows as you type, and each line opens the page that answers it.'],
            steps([('Step 1', 'Type it your way', 'A few plain words are enough: “reviews disappeared”, “not on maps”, “quote too high”.'),
                   ('Step 2', 'Open the page', 'Each line opens the page that answers it, at the question.'),
                   ('Step 3', 'Not there? Send it', 'If nothing matches, send the question. A person replies, and it gets a page.')], 3),
            W('rsm-ask', {}, 'rv', mt=22),
            T('<p>For example, typing “why did my reviews disappear” or “chatgpt” narrows the list to the pages that deal with it. Each answer was checked against the D’Souza Standard: 413 numbered checks, v1.0, 23 Nov 2026.</p>', 'small rs-note', mt=22, mb=18),
            B('See the five problems owners bring us', '/problems/', 'rs-more', mb=0), eid='ask'),
        sec('Where to look', 'Which page answers which kind of question?', ['Most questions fall into one of five kinds. This table shows where each kind is answered, so you can go straight there.'],
            table('Kinds of SEO question and the page that answers each', ('The question sounds like', 'Kind', 'Where it is answered'), [
                ('“Why can nobody find my business?”', 'Being found', 'Business not showing up on Google'),
                ('“People see me and call someone else.”', 'Being chosen', 'Get more leads for my business'),
                ('“Why does ChatGPT name my rival?”', 'AI answers', 'Get recommended by ChatGPT'),
                ('“My calls fell last month.”', 'A drop', 'Website traffic dropped suddenly'),
                ('“Is this quote fair?”', 'Cost', 'How much does SEO cost'),
            ]), more=('Open the five problem pages', '/problems/'), eid='kinds'),
        sec('How answers are made', 'How are the SEO questions answered on this site checked?', ['Each of the SEO questions answered here is written once and kept current, so the same question never gets two different answers on two pages. Every figure comes from one signed fact register.', 'When we get something wrong, the corrections page says what changed and when.'],
            G([card('clause', number='1', title='Written once.', text='One question, one answer, one page. If the facts change, that page changes and its review date moves.'),
               card('clause', number='2', title='Checked against the register.', text='Numbers, dates and promises are taken from the signed fact register, never from memory.'),
               card('clause', number='3', title='Signed.', text='Each page names who reviewed it and when. On this site that is Thomas D’Souza, the founder.')], 3, 1, 1),
            quote('If a question has two answers on one site, at least one of them is wrong. We answer it once and keep it right.'),
            more=('How we write and check', '/about/editorial-policy/'), eid='checked'),
        sec('Not here yet', 'Where do I get SEO help if my question is not here?', ['Send it. For SEO help with a question this page cannot answer, call or email and a person replies, usually within one working day. Questions that come up more than once get their own page.', 'If the question is about your own business, a discovery call is quicker: Thomas looks at your trade and city while you talk.'],
            C([B('Book a discovery call', '/book/'), B('Email info@relevantsearchmedia.com', 'mailto:info@relevantsearchmedia.com', 'rsm-btn rsm-btn-ghost')], 'rs-actions', 'row', flex_gap=gap(14), flex_wrap='wrap', flex_align_items='center', margin=box(0, 0, 0, 0)), eid='help'),
        faq('About this page', 'What do people ask about asking?', 'Short answers about how this page works. For the questions owners ask most, start with <a href="/problems/">the five problems</a>.', [
            ('Is it free to ask an SEO question?', 'Yes. Reading every answer on this site is free, and so is sending a question we have not answered yet. Nothing here sits behind a form or a sign-up.\nThe discovery call is also free: 20 to 30 minutes with Thomas, with no audit to buy first.'),
            ('Who answers the questions?', 'The team writes the answers and Thomas D’Souza, the founder, reviews each one before it is published. His name and the review date are on every page.\nHe has worked in digital marketing since 2010 and wrote the D’Souza Equation that the answers follow.'),
            ('How quickly will I get a reply?', 'A question sent by email or phone gets a reply from a person, usually within one working day. The team works US hours.\nIf many owners ask the same thing, it becomes a page on this site, so the next person finds it without waiting.'),
            ('Can I ask about my own website?', 'Yes, and a discovery call is the better place for it. A page can answer a general question, but your site, your listings and your city need someone to look.\nOn the call Thomas checks who Google, Maps and the AI engines name for your trade.'),
            ('What if the answer on a page is wrong?', 'Tell us. Every factual claim comes from one signed register, and when one turns out to be wrong we fix the page and record the change on the corrections page.\nWe would rather be corrected in public than stay wrong quietly.'),
        ]),
        trust(),
        closing('Still unsure? <span class="gold">Ask Thomas directly.</span>', 'A discovery call is 20 to 30 minutes with Thomas. He looks at who Google, Maps and the AI engines name when your customers ask, tells you what he sees, and shows you what the first fifteen days would be.', 'No audit to buy first, no trial. One business per trade per city.'),
    ]))
    # ------------------------------------------------------------------ /book/
    P.append(page('book', '/book/', 'Book a Discovery Call | Relevant Search Media',
        'Book a discovery call: 20 to 30 minutes with Thomas D’Souza. See who engines name for your trade and city, and what fifteen days would fix.', [
        hero([('Home', '/'), ('Book a discovery call', '')], 'Start here', 'Book a discovery call with Thomas',
             'Book a discovery call and you get 20 to 30 minutes with Thomas D’Souza. He looks at who Google, Maps and the AI engines name when your customers ask, tells you plainly what he sees, and shows you what the first fifteen days would be. There is no audit to buy first and no trial.',
             'Fill in the form and we reply with times within one working day.', ctas=(('Request my call', '/book/#form'), ('Ask a question', '/ask/')), note='Prefer the phone? Call +1 (202) 609-6641.'),
        S([G([W('rsm-form', {'title': 'Tell us where to reach you', 'intro': 'Your trade and city are enough for Thomas to prepare. We reply within one working day with times.'}, 'rv', eid='form'),
              C([H('What happens next', 'p', 'eyebrow'), H('What happens on an SEO consultation call?', 'h2', mb=18),
                 T('<p>This SEO consultation is a working call, not a sales pitch. You leave knowing which problem you have and what would be done about it first.</p>', 'lead', mb=22),
                 G([card('day', number='Step 1', title='You tell us trade and city', text='That is all we need to prepare. Send a quote you were given, or the date of a drop, if you have one.'),
                    card('day', number='Step 2', title='Thomas looks before the call', text='He checks who Google, Maps and three AI assistants name for your trade in your city.'),
                    card('day', number='Step 3', title='You talk for 20 to 30 minutes', text='He shows you what he found, which of the five problems it is, and the first fifteen days of work.'),
                    card('day', number='Step 4', title='You decide, in your own time', text='You get the price on the call. There is nothing to sign that day.')], 2, 2, 1, g=(14, 14)),
                 B('See the first fifteen days', '/dsouza-equation/method/', 'rs-more', mt=18, mb=0)], 'rv')],
             'minmax(0,6fr) minmax(0,6fr)', 'minmax(0,1fr)', 'minmax(0,1fr)', g=(36, 56))], eid='request'),
        sec('Minute by minute', 'What happens in the 20 to 30 minutes?', ['The call follows the same order every time, so nothing is left to a sales script. This is how the time is spent.'],
            table('How the discovery call is spent, minute by minute', ('Minutes', 'What happens', 'What you leave with'), [
                ('0 to 5', 'You describe the business and what is wrong', 'A plain name for the problem'),
                ('5 to 15', 'Thomas shows who Google, Maps and AI assistants name for your trade', 'A picture of where you stand today'),
                ('15 to 25', 'He walks through the first fifteen days of work', 'The order of fixes, biggest first'),
                ('25 to 30', 'Price, the two commitments, your questions', 'Everything you need to decide'),
            ]), more=('Read the two commitments', '/commitments/'), eid='minutes'),
        sec('Be ready', 'What should I have ready for the call?', ['Very little. Your trade, your city and your website address are enough for Thomas to prepare.', 'If another agency sent you a quote, or your calls fell on a date you remember, bring that. You do not need to share a password or give access to anything.'],
            more=('See the five problems owners bring', '/problems/'), eid='ready'),
        sec('Before you book', 'Who is the discovery call for?', ['It is for the owner of a US business that depends on being found: a plumber, a dentist, a law firm, a roofer, a clinic. We take one business per trade per city, so the first thing Thomas checks is whether your place is still open.', 'For example, if a roofer in Denver is already a client, a second “roofing company denver” is told so on the call and is not sold a plan.'],
            quote('I would rather tell you in ten minutes that we cannot take you on than sell you a plan that competes with a client.'),
            more=('Check whether your city is open', '/open-board/'), eid='who'),
        faq('About the call', 'What do owners ask before they book?', 'Short answers. For anything else, use the <a href="/ask/">Ask page</a>.', [
            ('Is this a free SEO consultation call?', 'Yes. The discovery call costs nothing, and there is no audit to buy first and no trial to sign up for. You are not asked for a card.\nA free SEO consultation call is only worth having if you leave with something, so Thomas shows you what he found.'),
            ('How long is the call, and who is on it?', 'It takes 20 to 30 minutes and it is with Thomas D’Souza, the founder, not a salesperson. He has worked in digital marketing since 2010.\nBring anyone who helps you decide. One conversation is all we ask of you before work would begin.'),
            ('What do I need to have ready?', 'Only your trade, your city and your website address. If you were given a quote by another agency, or your calls fell on a known date, bring that too.\nYou do not need to share passwords or give access to anything before the call.'),
            ('Will I get a price on the call?', 'Yes. Prices are not listed on this site because they depend on your trade, your city and how many searches have to be won. Thomas gives you the price on the call.\nEvery plan is month to month, with no setup fee.'),
            ('What if my trade is already taken in my city?', 'Then we tell you straight away and do not sell you a plan. We take one business per trade per city, because two rivals cannot both be the business an engine names.\nYou can ask to be told if the place opens again.'),
        ]),
        trust(),
        closing('One conversation. <span class="gold">Then you decide.</span>', 'The call is 20 to 30 minutes with Thomas. He looks at who Google, Maps and the AI engines name when your customers ask, tells you what he sees, and shows you what the first fifteen days would be.', 'No audit to buy first, no trial. One business per trade per city.'),
    ]))
    # ================================================================== THE EQUATION
    eq = lambda name: [('Home', '/'), ('The Equation', '/dsouza-equation/'), (name, '')]
    def terms(items, cols=3):
        return G([card('look', tag=k, status=st, title=t, text=x, link_text=lt, link=link(u)) for k, st, t, x, lt, u in items], cols, 2, 1)

    P.append(page('dsouza-equation', '/dsouza-equation/', "D'Souza Equation, Explained | Relevant Search Media",
        "The D'Souza Equation explains how every search engine and AI assistant picks a business. Relevance equals Read times Confirm times Choose.", [
        hero([('Home', '/'), ('The Equation', '')], 'The D’Souza Equation', "The D'Souza Equation: how every engine decides which business to name",
             "The D'Souza Equation says Relevance = Read × Confirm × Choose. A search engine or an AI assistant names a business when it can read plainly what the business is, when independent sources confirm it, and when real people choose it. The three are multiplied, so a business that fails one check is not named.",
             'One equation. Every engine obeys it.'),
        sec('Try it', "What is the D'Souza Equation?", ['It is a way of seeing what every engine has to decide before it names a business. Google, Maps, ChatGPT, Gemini and Perplexity look different, but each takes a person’s question and names the most relevant business it can trust.', 'Move the three dials below. The lights are customers asking, and the number is how many of every hundred are sent to you.'],
            W('rsm-lab', {'logo': {'url': '{{media:logo}}', 'id': '{{mediaid:logo}}'}, 'plain': 'Out of 100 people who ask, the engine sends roughly {n} your way. Let one check fall to nothing and it sends none.', 'terms': [
                {'_id': h['uid'](), 'k': 'Check one', 'name': 'Read', 'q': 'Is it plain from the site itself who this is and which questions it settles?', 'where_label': 'Raised by:', 'where': 'clear facts, direct answers, clean structure and markup on your own pages.', 'more': 'How Read works', 'link': link('/dsouza-equation/read/'), 'value': 80, 'color': '#F8B10F', 'ask': 'Can it read you?'},
                {'_id': h['uid'](), 'k': 'Check two', 'name': 'Confirm', 'q': 'Does the rest of the web describe the business the same way?', 'where_label': 'Raised by:', 'where': 'matching listings, real reviews, mentions and press on other sites.', 'more': 'How Confirm works', 'link': link('/dsouza-equation/confirm/'), 'value': 70, 'color': '#4CC0A8', 'ask': 'Do others back you up?'},
                {'_id': h['uid'](), 'k': 'Check three', 'name': 'Choose', 'q': 'When shown this business, do searchers pick it?', 'where_label': 'Raised by:', 'where': 'a listing and a first screen that win the click, the call and the return visit.', 'more': 'How Choose works', 'link': link('/dsouza-equation/choose/'), 'value': 75, 'color': '#A3B5F2', 'ask': 'Do people pick you?'}]}, 'rv'),
            T('<p>For example, when a customer asks “who fixes a burst pipe?”, the engine reads each plumber’s site, checks what others say, and looks at who people chose. With Read at 80, Confirm at 70 and Choose at 75, about 42 in 100 are sent to you.</p>', 'small rs-note', mt=22, mb=18),
            B('See the five problems the equation explains', '/problems/', 'rs-more', mb=0), eid='try'),
        sec('Three checks', 'How search engines choose a business: three checks', ['This is how search engines choose a business, and how AI assistants do. Each check is a question the engine asks, and each has a place where the work is done.'],
            terms([('Term one', 'gold', 'Read', 'The engine has to understand the business from its own pages: who it is, what it does, where, and which questions it settles.', 'How Read works', '/dsouza-equation/read/'),
                   ('Term two', 'green', 'Confirm', 'The engine then looks elsewhere. If directories, review sites and other publishers describe the business the same way, it trusts what it read.', 'How Confirm works', '/dsouza-equation/confirm/'),
                   ('Term three', 'green', 'Choose', 'Last, the engine watches behaviour. A business that searchers click, call and come back to is shown to the next searcher.', 'How Choose works', '/dsouza-equation/choose/')]),
            eid='checks'),
        sec('Why multiply', 'Why is the relevance equation a multiplication?', ['Because the checks depend on each other. In a sum, a strong score could cover for a weak one. In the relevance equation it cannot: a low score in any term pulls the whole result down, and a zero ends it.', 'The table shows four businesses. The figures are an illustration of the arithmetic, not a measurement of any site.'],
            table('Four illustrative businesses scored on Read, Confirm and Choose', ('The business', 'Read × Confirm × Choose', 'Sent to it, in 100'), [
                ('A fine website nobody vouches for', '90 × 20 × 60', '11'),
                ('Well known, hard to read', '30 × 80 × 70', '17'),
                ('Read and confirmed, not chosen', '85 × 80 × 25', '17'),
                ('All three in good order', '85 × 80 × 80', '54'),
            ]),
            quote('You cannot add your way out of a zero. A business the engine cannot read is not named, however good its reviews.'),
            more=('See which check to raise first', '/problems/'), eid='multiply'),
        sec('Every engine', 'Does the equation hold for AI assistants as well as Google?', ['Yes. An AI assistant cannot name a business it cannot read, will not vouch for one nobody else mentions, and learns from what people chose. The engines differ in how they read; they agree on what they are looking for.', 'That is why the same work moves a business on Google, on Maps and in an AI answer at once, and why we do not sell a separate method for each.'],
            more=('See every engine we cover', '/dsouza-equation/engines/'), eid='engines'),
        sec('In practice', 'How is the equation used on a real business?', ['It becomes a checklist. The D’Souza Standard turns the three terms into 413 numbered checks, and every client site is run through all of them in the first three days.', 'The weakest term is raised first, because that is where the multiplication gains most.'],
            steps([('Day 1', 'Score the three terms', 'After one conversation, the business gets a first reading on Read, Confirm and Choose.'),
                   ('Day 2', 'Find the searches', 'The questions customers really type are listed, so each term is scored against real demand.'),
                   ('Day 3', 'Run the Standard', 'All 413 checks are applied, and each failed check is filed under the term it weakens.'),
                   ('Day 4 to 5', 'Raise the weakest term', 'The plan starts where the multiplication gains most, and the first fixes are published.')]),
            more=('Read all 413 checks', '/dsouza-equation/standard/'), eid='practice'),
        sec('Where it came from', 'Who wrote the equation, and when?', ['Thomas D’Souza, the founder of Relevant Search Media, who has worked in digital marketing since 2010. The company was founded in 2020 and the equation has been in writing since 2025.', 'It was written to answer one question owners kept asking: why does the engine name them and not me?'],
            more=('How the equation came about', '/about/'), eid='origin'),
        faq('Questions about the equation', "What do people ask about the D'Souza Equation?", 'Short answers. For anything else, use the <a href="/ask/">Ask page</a>.', [
            ("Is the D'Souza Equation Google's ranking formula?", 'No. Nobody outside Google has that, and it changes. The equation is a model of what every engine has to decide before it names a business.\nIt is useful because it stays true when an algorithm changes: an engine still has to read you, confirm you and see you chosen.'),
            ('Which of the three should I raise first?', 'The weakest one. Because the terms are multiplied, lifting the lowest score moves the result more than polishing the highest.\nFor most businesses that is Read at the start, then Confirm. The checks on the <a href="/problems/">problems page</a> show which is yours in about ten minutes.'),
            ('Can a business score 100?', 'Not in practice. The dials are an illustration, and no site is perfectly readable, confirmed everywhere and always chosen.\nWhat matters is the comparison with the other businesses the engine could name for the same search, in the same city.'),
            ('How is it different from E-E-A-T?', 'E-E-A-T is Google’s shorthand for how its quality raters judge experience, expertise, authority and trust. It describes one part of the picture, for one engine.\nThe equation covers reading, confirmation and choice across every engine. Most of E-E-A-T sits inside Confirm.'),
            ('Does it apply to Maps and voice search?', 'Yes. A map result and a voice answer are the same decision with less room: the engine names fewer businesses, so each check counts for more.\nA listing that is read, confirmed and chosen wins on Maps for the same reasons a page wins in search.'),
        ]),
        trust(),
        closing('See the equation <span class="gold">applied to your business.</span>', 'A discovery call is 20 to 30 minutes with Thomas. He scores your business on Read, Confirm and Choose while you watch, tells you which term is holding you back, and shows you what the first fifteen days would raise.', 'No audit to buy first, no trial. One business per trade per city.'),
    ]))
    # ------------------------------------------------------------------ /dsouza-equation/read/
    P.append(page('read', '/dsouza-equation/read/', 'Can Search Engines Read My Website | Relevant Search Media',
        'Can search engines read my website? Four checks answer it in ten minutes. Read is the first term of the D’Souza Equation and holds 250 of its 413 checks.', [
        hero(eq('Read'), 'Term one of three', 'Can search engines read my website? The Read check, explained',
             'Search engines can read your website when four things hold: the pages can be crawled, the words are in the page itself, each page says plainly who you are, what you do and where, and the facts are marked up. Read is the first term of the D’Souza Equation, and nothing else counts until it passes.',
             'Read comes first, because an engine cannot confirm or choose what it cannot read.'),
        sec('The ten-minute check', 'How do I check whether an engine can read my site?', ['Four checks, no tools to buy. Each one tests a different way a page can be open to people and closed to machines.'],
            steps([('Check 1', 'Count your pages in Google', 'Search site: followed by your domain. Compare the number with the pages you actually have.'),
                   ('Check 2', 'Look for the words in the source', 'Open a page, view its source and search for your phone number. If it is missing, the text is added by script.'),
                   ('Check 3', 'Read the first screen aloud', 'Does it say who you are, what you do and where, in one sentence a stranger would understand?'),
                   ('Check 4', 'Ask an assistant what the site does', 'Give an AI assistant your web address and ask what the business does. Its answer is what it could read.')]),
            T('<p>For example, a law firm in New York might find that “site:” shows 40 pages when it published 120. The other 80 are unread, whatever they say. In the D’Souza Standard, Read holds 250 of the 413 checks (v1.0, 23 Nov 2026), more than the other two terms together.</p>', 'small rs-note', mt=22, mb=18),
            B('Is your business missing from Google?', '/problems/not-showing-up-on-google/', 'rs-more', mb=0), eid='check'),
        sec('Eight blockers', 'What makes a crawlable website, and what stops one?', ['A crawlable website lets an engine fetch every page, see its words and follow its links. Eight things commonly stop that, and most are accidents left over from a rebuild.'],
            table('What stops an engine reading a site: the blocker, the sign and the fix', ('The blocker', 'How to tell', 'What fixes it'), [
                ('A robots.txt rule shuts the site', 'Search Console reports “blocked by robots.txt”', 'Remove the rule and name the crawlers you welcome'),
                ('A noindex tag was left on', 'Pages are crawled and never listed', 'Take the tag off and ask for a recrawl'),
                ('Text arrives only by script', 'The words are not in the page source', 'Put the content in the HTML the server sends'),
                ('Words are locked inside images', 'You cannot select the text with a cursor', 'Write it as text and describe the image'),
                ('Pages nobody links to', 'A page is live and absent from the menu and the sitemap', 'Link it from a related page and list it in the sitemap'),
                ('Two addresses, one page', 'The same text loads with and without www', 'Choose one address and point the other at it'),
                ('The server is slow or failing', 'Pages time out, or return errors in Search Console', 'Fix the hosting before anything else'),
                ('A pop-up or log-in covers the page', 'The content cannot be reached without a click', 'Show the content first and ask afterwards'),
            ]), more=('See all 413 checks', '/dsouza-equation/standard/'), eid='blockers'),
        sec('Four layers', 'On-page SEO explained: what does an engine read on a page?', ['On-page SEO explained in one line: it is everything on your own pages that helps an engine understand them. It comes in four layers, and each is useless without the one before.'],
            G([card('clause', number='1', title='Facts.', text='Who the business is, what it does, where and for whom, stated in plain sentences that could be lifted whole.'),
               card('clause', number='2', title='Answers.', text='The question as the heading and a direct answer under it, before any background.'),
               card('clause', number='3', title='Structure.', text='One main heading, sub-headings in order, short paragraphs, and links between related pages.'),
               card('clause', number='4', title='Markup.', text='Structured data that labels the facts for a machine: the organisation, the place, the questions, the author.')], 4, 2, 1),
            quote('Write so that a machine can lift one sentence and still be right. That sentence is the one that gets you named.'),
            more=('What we do for technical SEO', '/services/technical-seo/'), eid='layers'),
        sec('AI readers', 'Do AI assistants read a site differently from Google?', ['They fetch pages with their own crawlers, such as GPTBot, ClaudeBot and PerplexityBot, and many sites block them without knowing. A robots.txt file can welcome each by name.', 'They also favour text that answers directly. A paragraph that states a fact in full is quoted; one that hints at it is skipped. An llms.txt file helps by listing the key pages in plain text.'],
            more=('What we do for AI SEO', '/services/ai-seo/'), eid='ai'),
        sec('Inside the Standard', 'Which of the 413 checks belong to Read?', ['Read holds 250 checks in 16 groups, from technical health and speed through headings, verified facts and AI readiness. They are run on every client site in the first three days.', 'The largest groups are technical health with 36 checks, speed and stability with 24, and AI readiness with 24.'],
            terms([('36 checks', 'gold', 'Technical health', 'Crawling, indexing, canonical addresses, redirects and the sitemap.', 'See the Standard', '/dsouza-equation/standard/'),
                   ('24 checks', 'green', 'AI readiness', 'Direct answers, quotable facts, AI crawlers allowed and an llms.txt file.', 'See the Standard', '/dsouza-equation/standard/'),
                   ('20 checks', 'green', 'Verified facts', 'Every number and claim traced to a signed register before it is published.', 'How we check', '/about/editorial-policy/')]),
            eid='standard'),
        faq('Questions about Read', 'What do owners ask about being read?', 'Short answers. For anything else, use the <a href="/ask/">Ask page</a>.', [
            ('How do I know if Google has indexed my site?', 'Search site: followed by your domain. The results are the pages Google holds. Search Console shows the same thing in more detail, with the reason for each page it left out.\nIf the count is far below the pages you published, something on this page’s list of blockers applies.'),
            ('Does my site need to be fast to be read?', 'It needs to respond. A server that times out or returns errors is read less often and less deeply. Speed beyond that mostly affects whether people stay.\nThe Standard has 24 checks on speed and stability for that reason.'),
            ('Is a website builder a problem?', 'Not by itself. Most builders produce pages an engine can read. Trouble comes from settings: a noindex switch left on, text drawn by script, or addresses that change at each edit.\nRun the four checks above; they work on any platform.'),
            ('What is structured data, in plain words?', 'It is a label attached to a fact. It tells a machine that this string is a phone number, that one is an opening hour, and this block is a question with its answer.\nIt does not replace clear writing. It makes clear writing unmistakable.'),
            ('How long until a fixed page is read again?', 'Google says crawling can take from a few days to a few weeks. Asking for a recrawl in Search Console usually shortens it for an important page.\nOn our plans the first fixes go live by day 5 and each is logged with its link.'),
        ]),
        trust(),
        closing('Can an engine read you? <span class="gold">Find out in one call.</span>', 'A discovery call is 20 to 30 minutes with Thomas. He runs the four Read checks on your site while you watch, tells you what an engine can and cannot see, and shows you what the first fifteen days would open up.', 'No audit to buy first, no trial. One business per trade per city.'),
    ], parent='dsouza-equation'))
    # ------------------------------------------------------------------ /dsouza-equation/confirm/
    P.append(page('confirm', '/dsouza-equation/confirm/', 'Search Engine Trust Signals | Relevant Search Media',
        'Search engine trust signals are what others say about your business. Confirm is the second term of the D’Souza Equation, with 99 of its 413 checks.', [
        hero(eq('Confirm'), 'Term two of three', 'Search engine trust signals: the Confirm check, explained',
             'Search engine trust signals are the things an engine finds about a business outside its own website: listings, reviews, mentions, profiles and press. Confirm is the second term of the D’Souza Equation. An engine that has read your site looks elsewhere to see whether the rest of the web agrees, and names you only if it does.',
             'Your site can say anything. Confirm is everyone else saying the same.'),
        sec('The ten-minute check', 'How do I check whether anything confirms my business?', ['Four checks. Each looks at the business from outside, the way an engine does once it has finished reading the site.'],
            steps([('Check 1', 'Search your name in quotes', 'Put the business name in quotation marks. Count the results that are not your own site.'),
                   ('Check 2', 'Compare three listings', 'Open your Google profile and two directories. The name, address and phone should match to the letter.'),
                   ('Check 3', 'Read your latest review', 'Note its date and platform. An engine notices when the newest praise is two years old.'),
                   ('Check 4', 'Ask who recommends you', 'Ask an AI assistant which sources mention your business. An empty answer is the finding.')]),
            T('<p>For example, a contractor in Atlanta who appears as “Smith Build”, “Smith Building Co.” and “Smith Builders LLC” on three sites has three weak records and no strong one. In the D’Souza Standard, Confirm holds 99 of the 413 checks (v1.0, 23 Nov 2026), in seven groups.</p>', 'small rs-note', mt=22, mb=18),
            B('Google shows you and AI does not?', '/problems/not-recommended-by-chatgpt/', 'rs-more', mb=0), eid='check'),
        sec('Seven sources', 'Off-page SEO explained: where does confirmation come from?', ['Off-page SEO explained simply is the work done away from your own pages. It has seven sources, and an engine weighs them together.'],
            table('The seven sources of confirmation, what each proves and how many checks cover it', ('The source', 'What it proves', 'Checks in the Standard'), [
                ('Local signals', 'The business is where it says it is', '26'),
                ('Google Business Profile', 'The listing is complete, accurate and active', '22'),
                ('Off-site presence', 'Other websites describe the business the same way', '12'),
                ('Author and entity', 'A real, named person stands behind the content', '12'),
                ('Reviews and reputation', 'Customers have said so, lately, and were answered', '10'),
                ('Social presence', 'The business is alive on the platforms it claims', '9'),
                ('Video and visual search', 'There is footage and imagery of real work', '8'),
            ]), more=('See all 413 checks', '/dsouza-equation/standard/'), eid='sources'),
        sec('Listings and mentions', 'Do citations and mentions still matter?', ['Yes, with a change of emphasis. Citations and mentions matter less as a count and more as agreement. Ten listings that match exactly do more than a hundred that differ.', 'A mention without a link also counts. AI assistants read what a local paper or a trade body wrote about a business even when no link was given.'],
            quote('Nobody is confirmed by their own website. Confirmation is what the rest of the web says when you are not in the room.'),
            more=('What we do for links and earned mentions', '/services/link-building/'), eid='mentions'),
        sec('Reviews', 'How do reviews work as a trust signal?', ['Reviews confirm three things at once: that customers exist, that they were satisfied, and that the business is active now. Recency and replies carry as much weight as the rating.', 'We do not write, buy or filter reviews. We set up the asking, so every real customer is invited, and every review gets a reply.'],
            more=('What we do for reputation and reviews', '/services/reputation-management/'), eid='reviews'),
        sec('The named author', 'Why does a named person matter?', ['Because an engine trusts a claim more when it can tie it to someone accountable. A page signed by a named founder, with a profile that matches elsewhere, is easier to confirm than an anonymous one.', 'Every page on this site carries the name of Thomas D’Souza and the date he reviewed it.'],
            more=('About Thomas', '/thomas-dsouza/'), eid='author'),
        faq('Questions about Confirm', 'What do owners ask about trust signals?', 'Short answers. For anything else, use the <a href="/ask/">Ask page</a>.', [
            ('What is the difference between a citation and a backlink?', 'A citation is a listing of the business name, address and phone on another site, such as a directory. A backlink is a link from another site to yours.\nBoth confirm the business. Citations prove the place; links and mentions prove that others find it worth pointing to.'),
            ('How many directory listings do I need?', 'There is no number to hit. Start with the listings your customers and your trade actually use, and make each one identical to your Google profile.\nAccuracy across a dozen good listings beats volume across hundreds nobody reads.'),
            ('Can I pay for reviews or links?', 'You can, and you should not. Paid reviews break the platforms’ rules and the law in many places, and bought links are what search engines discount first.\nConfirmation only works because it comes from someone with no reason to flatter you.'),
            ('Does social media count as a trust signal?', 'It counts as evidence that the business is real and active. A profile with the same name, address and services, posting now and then, supports the rest.\nIt is not a ranking lever by itself, and an abandoned profile helps less than none.'),
            ('How long does confirmation take to build?', 'Fixing mismatched listings is quick and shows within weeks. Earning reviews and mentions is steady work, month after month.\nOn our plans every item is logged with its link, and the report every 15 days shows what was added.'),
        ]),
        trust(),
        closing('Does the web back you up? <span class="gold">See in one call.</span>', 'A discovery call is 20 to 30 minutes with Thomas. He looks at what other sites, listings and reviewers say about your business, shows you where the story breaks, and tells you what the first fifteen days would put right.', 'No audit to buy first, no trial. One business per trade per city.'),
    ], parent='dsouza-equation'))
    # ------------------------------------------------------------------ /dsouza-equation/choose/
    P.append(page('choose', '/dsouza-equation/choose/', 'User Signals in SEO | Relevant Search Media',
        'User signals in SEO are what people do when they see your business: click, call, stay, return. Choose is the third term of the D’Souza Equation.', [
        hero(eq('Choose'), 'Term three of three', 'User signals in SEO: the Choose check, explained',
             'User signals in SEO are the things people do when an engine shows them your business: they click or scroll past, call or leave, come back or never return. Choose is the third term of the D’Souza Equation. An engine that has read and confirmed you still watches whether real people pick you, and shows the chosen business more often.',
             'The engine finds you. People decide whether it keeps showing you.'),
        sec('The ten-minute check', 'How do I check whether people choose my business?', ['Four checks, done on a phone. Each one looks at a moment where a searcher either picks you or moves on.'],
            steps([('Check 1', 'Look at your result beside the others', 'Search your trade and city. Is your title and line of text the one you would tap?'),
                   ('Check 2', 'Time the first screen', 'Open your page and count to five. Could a stranger say what you do and how to reach you?'),
                   ('Check 3', 'Make the call yourself', 'Tap your number from the listing. Count the taps, and whether a person answers.'),
                   ('Check 4', 'Find your own proof', 'Look for a result, a review or a guarantee near the button. If you cannot see one, neither can they.')]),
            T('<p>For example, a dentist in Chicago whose listing shows “Open now”, forty recent reviews and a one-tap call button is chosen over a better dentist whose listing shows none of them. In the D’Souza Standard, Choose holds 50 of the 413 checks (v1.0, 23 Nov 2026).</p>', 'small rs-note', mt=22, mb=18),
            B('Found, and still not picked?', '/problems/not-getting-leads/', 'rs-more', mb=0), eid='check'),
        sec('Four moments', 'Click-through rate, calls and visits: where is the choice made?', ['Click-through rate is only the first of four moments. A searcher chooses, or does not, at each one, and a business can win three and lose at the fourth.'],
            table('The four moments of choice, what the searcher sees and what wins it', ('The moment', 'What the searcher sees', 'What wins it'), [
                ('The result', 'A title, a line of text, stars, a distance', 'A title that answers the search and a rating worth a tap'),
                ('The listing', 'Photos, hours, services, the latest reviews', 'Recent photos, every service named, replies to reviews'),
                ('The first screen', 'One headline, one button, a few seconds', 'What you do, where, and one clear next step'),
                ('The contact', 'A phone that rings, a form that sends', 'One tap to call, a short form, an answer the same day'),
            ]), more=('What we do for Google Business Profile', '/services/google-business-profile-optimization/'), eid='moments'),
        sec('Proof', 'What makes a stranger pick one business over another?', ['Proof, placed where the decision happens. A stranger cannot judge your work, so they judge the evidence: what others said, what you promise, and whether you look ready.'],
            G([card('clause', number='1', title='Results, with a source.', text='A number means more when it says where it came from. Ours cite the fact register they are drawn from.'),
               card('clause', number='2', title='A promise in writing.', text='A commitment that costs you something if you miss it removes the risk the stranger was weighing.'),
               card('clause', number='3', title='Signs of life.', text='Opening hours that are right, a review from this month, a reply from the owner.')], 3, 1, 1),
            quote('Ranking first and being chosen are two different jobs. The engine does the first for you once. It only keeps doing it if people do the second.'),
            more=('Read the two commitments', '/commitments/'), eid='proof'),
        sec('Measuring it', 'How is being chosen measured?', ['By what happened, not by what was shown. Impressions and rankings say you were offered. Calls, forms and messages say you were chosen.', 'On our plans the report every 15 days carries the Relevance Rate: the share of leads you confirm were relevant. The Standard has 12 checks on tracking alone, so the count can be trusted.'],
            terms([('22 checks', 'gold', 'Conversion elements', 'The call to action, the form, the proof beside it and the risk it removes.', 'See the Standard', '/dsouza-equation/standard/'),
                   ('16 checks', 'green', 'AI answer verification', 'What assistants say about the business, checked for accuracy and tracked monthly.', 'Open the Index', '/ai-recommendation-index/'),
                   ('12 checks', 'green', 'Tracking and measurement', 'Calls, forms and messages counted properly, so leads are not guessed.', 'Lead generation', '/services/lead-generation/')]),
            eid='measure'),
        faq('Questions about Choose', 'What do owners ask about being chosen?', 'Short answers. For anything else, use the <a href="/ask/">Ask page</a>.', [
            ('Does Google really use clicks to rank pages?', 'Google has said for years that it studies how people interact with results, and court filings have described systems that learn from it. The details are not public.\nYou do not need them. A result people prefer is a result an engine has every reason to keep showing.'),
            ('What is a good click-through rate?', 'It depends on the position and the search, so a single target is misleading. Compare a page with itself over time, and with the pages ranked around it.\nA title and description that answer the search directly lift the rate at any position.'),
            ('Why do I rank well and still get few calls?', 'Because ranking gets you seen and something after that loses the choice: the listing, the first screen, or a phone nobody answers.\nRun the four checks on this page. The moment you lose people at is usually obvious once you look.'),
            ('Do reviews belong to Confirm or to Choose?', 'Both. To an engine, reviews on independent platforms confirm that the business is real. To a searcher, the same reviews decide the choice.\nThat double duty is why asking every customer, and replying to each review, repays the effort twice.'),
            ('Can design alone raise how often I am chosen?', 'It helps when it removes friction: a clear first screen, a visible number, a short form. It does not help when it only decorates.\nPeople choose on clarity and proof. Design serves both, or it is in the way.'),
        ]),
        trust(),
        closing('Seen, but not chosen? <span class="gold">Find the moment in one call.</span>', 'A discovery call is 20 to 30 minutes with Thomas. He walks through the four moments with your business on a phone, shows you where people leave, and tells you what the first fifteen days would change.', 'No audit to buy first, no trial. One business per trade per city.'),
    ], parent='dsouza-equation'))
    # ------------------------------------------------------------------ /dsouza-equation/standard/
    P.append(page('standard', '/dsouza-equation/standard/', 'SEO Checklist: All 413 Checks | Relevant Search Media',
        'This SEO checklist is the D’Souza Standard: 413 numbered checks, published in full. Use it on your own site, or hold any agency to it.', [
        hero(eq('The Standard'), 'The D’Souza Standard', "SEO checklist: the D'Souza Standard, all 413 checks",
             'This SEO checklist is the D’Souza Standard: 413 numbered checks, version 1.0, dated 23 Nov 2026, published here in full. Every page we build and every client site we take on is run through all of them. You can use the list on your own site, or hold any agency, including us, to it.',
             'Most agencies keep the method private. This is ours, in the open.', ctas=(('Book a discovery call', '/book/'), ('Ask a question', '/ask/'))),
        sec('How it is built', 'How is this SEO audit checklist organised?', ['The SEO audit checklist follows the D’Souza Equation. Every check belongs to one of its terms, so a failed check tells you which part of the equation it weakens.', 'The 413 checks sit in 27 groups. Of them, 193 apply to every page, 149 to the whole site and 71 to places beyond the site, such as listings and reviews.'],
            table('The 413 checks by equation term', ('Equation term', 'What it covers', 'Groups and checks'), [
                ('Read', 'Whether an engine can read the site: health, speed, structure, copy, facts, AI readiness', '16 groups, 250 checks'),
                ('Confirm', 'Whether others say the same: listings, the Business Profile, reviews, mentions, the author', '7 groups, 99 checks'),
                ('Choose', 'Whether people pick you: the call to action, tracking, what AI answers say', '3 groups, 50 checks'),
                ('The question', 'Whether the right customer searches were mapped to begin with', '1 group, 14 checks'),
            ]), more=('How the equation works', '/dsouza-equation/'), eid='organised'),
        sec('The list', 'The 413 SEO checks, group by group', ['All 413 SEO checks are below, numbered and worded exactly as we use them. Open a group to read its checks, or type a word to find the ones that mention it.', 'For example, check 104 reads: “The title is 30 to 60 characters and is not cut off in results.” This page was held to it, and to the other 412.'],
            W('rsm-standard', {}, 'rv'),
            B('See how the checks are applied in the first fifteen days', '/dsouza-equation/method/', 'rs-more', mt=22, mb=0), eid='list'),
        sec('Scoring', 'How is a page scored against the checklist?', ['Each check ends one of three ways: pass, fail, or not testable yet. A page is published only with no failed check.', 'Not testable yet is used honestly. Some checks need Search Console data, a second reviewer’s signature or seven days to pass, and they are listed as open until that exists. They are never counted as passes.'],
            G([card('clause', number='1', title='Pass.', text='The page was measured and met the check. The measurement is recorded with the date.'),
               card('clause', number='2', title='Fail.', text='The page did not meet it. It is fixed and measured again before anything is published.'),
               card('clause', number='3', title='Not testable yet.', text='The check needs data or a person that the page alone cannot supply. It stays open, by name.')], 3, 1, 1),
            quote('A method is only worth something if it can fail in public. So here it is, all of it, with a number on every line.'),
            more=('See our own results in the Open Log', '/open-log/'), eid='scoring'),
        sec('Use it', 'Can I use this checklist on my own site?', ['Yes. Nothing here is behind a form. An owner can work through the groups that apply to one page in an afternoon, and the checks say plainly what to look for.', 'Where it gets heavy is scale: 413 checks across every page, every listing and every AI answer, repeated as engines change. That is the work a team does.'],
            steps([('Step 1', 'Pick one page', 'Start with the page that should bring the most customers, usually the home page or a main service.'),
                   ('Step 2', 'Open the page groups', 'Titles and descriptions, headings and copy, images and conversion elements all apply to a single page.'),
                   ('Step 3', 'Mark each line', 'Pass, fail or cannot tell. Be strict: a check you are unsure of is a fail until shown otherwise.'),
                   ('Step 4', 'Fix the fails in order', 'Work from the top of the list. The early groups decide whether the later ones matter.')]),
            more=('What to check first, by problem', '/problems/'), eid='use'),
        sec('Versions', 'How often does the Standard change?', ['It is versioned and dated. This is version 1.0 of 23 Nov 2026. When a new engine or a new kind of question matters, checks are added as numbered rows and the version moves.', 'A check is never quietly reworded. Changes are recorded on the corrections page.'],
            more=('See the corrections record', '/about/corrections/'), eid='versions'),
        faq('Questions about the Standard', 'What do people ask about the checklist?', 'Short answers. For anything else, use the <a href="/ask/">Ask page</a>.', [
            ('Why publish the whole checklist?', 'Because a method you cannot see cannot be checked. Publishing all 413 lines lets a client hold us to them, and lets anyone compare another agency’s work with the same list.\nIt also means we cannot quietly skip the hard ones.'),
            ('Do all 413 checks apply to every page?', 'No. 193 apply to every page, 149 to the site as a whole and 71 to things beyond the site, such as listings, reviews and profiles.\nA single page is held to the page checks; the site and off-site checks are run once and re-run on a schedule.'),
            ('What does “not testable yet” mean?', 'It means the answer is not in the page. A check that needs real-visitor speed data, a second reviewer’s sign-off or a week of indexing cannot be judged at publish time.\nThose checks stay open and are closed, by name, when the data arrives.'),
            ('Is this the same as an SEO audit?', 'An audit is one run of a checklist on one day. The Standard is the checklist itself, run on day three and then kept running.\nAn audit that is never acted on changes nothing, which is why our plans ship fixes from day 5.'),
            ('Can I download the checklist?', 'It is all on this page, in plain text you can copy, with every check numbered. We have not put it behind an email form.\nIf you would like it applied to your site, a discovery call is the next step.'),
        ]),
        trust(),
        closing('413 checks. <span class="gold">See how your site scores.</span>', 'A discovery call is 20 to 30 minutes with Thomas. He runs a sample of the checks on your site while you watch, shows you which term of the equation is weakest, and tells you what the first fifteen days would fix.', 'No audit to buy first, no trial. One business per trade per city.'),
    ], parent='dsouza-equation'))
    return P

GATE = {
    '/dsouza-equation/standard/': {'kw': 'seo checklist;seo audit checklist;413 seo checks', 'type': 'reference', 'example': 'the title is 30 to 60 characters', 'original': '413;v1.0, 23 Nov 2026', 'trade': 'checks;page;site'},
    '/dsouza-equation/read/': {'kw': 'can search engines read my website;on-page seo explained;crawlable website', 'type': 'pillar', 'example': 'law firm in new york', 'original': '250;v1.0, 23 Nov 2026', 'trade': 'crawl;index;markup'},
    '/dsouza-equation/confirm/': {'kw': 'search engine trust signals;off-page seo explained;citations and mentions', 'type': 'pillar', 'example': 'contractor in atlanta', 'original': '99;v1.0, 23 Nov 2026', 'trade': 'listings;reviews;mentions'},
    '/dsouza-equation/choose/': {'kw': 'user signals in seo;click-through rate;calls and visits', 'type': 'pillar', 'example': 'dentist in chicago', 'original': '50;v1.0, 23 Nov 2026', 'trade': 'reviews;listing;call'},
    '/dsouza-equation/': {'kw': "d'souza equation;how search engines choose a business;relevance equation", 'type': 'pillar', 'example': 'who fixes a burst pipe', 'original': '413;v1.0, 23 Nov 2026', 'trade': 'engine;customers;reviews'},
    '/ask/': {'kw': 'ask an seo question;seo questions answered;seo help', 'type': 'tool', 'example': 'why did my reviews disappear', 'original': '413;v1.0, 23 Nov 2026', 'trade': 'question;answer;page'},
    '/book/': {'kw': 'book a discovery call;seo consultation;free seo consultation call', 'type': 'tool', 'example': 'roofing company denver', 'original': '413;v1.0, 23 Nov 2026', 'trade': 'call;plumber;dentist'},
    '/problems/seo-cost/': {'kw': 'how much does seo cost;is my seo quote fair;seo pricing', 'type': 'problem', 'example': 'kitchen remodel atlanta', 'original': '177;v4, 18 Nov 2026', 'trade': 'quote;contract;month to month'},
    '/problems/traffic-dropped/': {'kw': 'website traffic dropped suddenly;google rankings dropped;lost rankings after an update', 'type': 'problem', 'example': 'hvac repair dallas', 'original': '165;v4, 18 Nov 2026', 'trade': 'update;rankings;search console'},
    '/problems/not-recommended-by-chatgpt/': {'kw': 'get recommended by chatgpt;how to get my business recommended by chatgpt;show up in chatgpt;ai not recommending my business', 'type': 'problem', 'example': 'divorce lawyer in new york', 'original': '211;v4, 18 Nov 2026', 'trade': 'lawyer;sources;reviews'},
    '/problems/not-getting-leads/': {'kw': 'get more leads for my business;how to get more leads for my business;website not getting leads;more calls from google', 'type': 'problem', 'example': 'emergency dentist chicago', 'original': '186;v4, 18 Nov 2026', 'trade': 'dentist;reviews;listing'},
    '/problems/not-showing-up-on-google/': {'kw': 'business not showing up on google;business not on google;not on google maps;why is my business not showing up on google', 'type': 'problem', 'example': 'roof repair denver', 'original': '170;v4, 18 Nov 2026', 'trade': 'roofer;profile;listing'},  # what the gate is told about each page: keywords, page type, the specific example and the dated original figure it must carry
    '/problems/': {'kw': 'seo problems;search marketing problems;why is my seo not working', 'type': 'hub', 'example': 'emergency plumber miami', 'original': '166;v4, 18 Nov 2026', 'trade': 'plumber;roofer;dentist'},
}
