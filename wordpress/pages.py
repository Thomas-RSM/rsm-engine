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
    return P

GATE = {
    '/problems/not-recommended-by-chatgpt/': {'kw': 'get recommended by chatgpt;how to get my business recommended by chatgpt;show up in chatgpt;ai not recommending my business', 'type': 'problem', 'example': 'divorce lawyer in new york', 'original': '211;v4, 18 Nov 2026', 'trade': 'lawyer;sources;reviews'},
    '/problems/not-getting-leads/': {'kw': 'get more leads for my business;how to get more leads for my business;website not getting leads;more calls from google', 'type': 'problem', 'example': 'emergency dentist chicago', 'original': '186;v4, 18 Nov 2026', 'trade': 'dentist;reviews;listing'},
    '/problems/not-showing-up-on-google/': {'kw': 'business not showing up on google;business not on google;not on google maps;why is my business not showing up on google', 'type': 'problem', 'example': 'roof repair denver', 'original': '170;v4, 18 Nov 2026', 'trade': 'roofer;profile;listing'},  # what the gate is told about each page: keywords, page type, the specific example and the dated original figure it must carry
    '/problems/': {'kw': 'seo problems;search marketing problems;why is my seo not working', 'type': 'hub', 'example': 'emergency plumber miami', 'original': '166;v4, 18 Nov 2026', 'trade': 'plumber;roofer;dentist'},
}
