import csv
P=[]
def a(cat,name,url,pri,why,post,note="",us="No"):
    P.append([cat,name,url,pri,why,post,note,us])

C="US presence setup (do first)"
a(C,"US business entity (LLC) + EIN","irs.gov/businesses","P1","US buyers, BBB, Yelp, US directories and US payment accounts expect a US company. Unlocks most US-only rows below.","None (setup)","Confirm structure with a US accountant before filing","Prerequisite")
a(C,"US business phone number (local area code)","google.com/voice","P1","US buyers call and trust a US number; required on most US profiles. Use one number everywhere.","None (setup)","Google Voice, RingCentral, OpenPhone or similar","Prerequisite")
a(C,"US office address (staffed)","n/a","P1","Needed for US Google Business Profile, Bing, Apple Maps, Yelp, BBB and US citations.","None (setup)","Google does not allow a virtual office or mailbox. A coworking office counts only with signage, customer visits and your own staff present during listed hours","Prerequisite")
a(C,"US mailing address (virtual mailbox)","n/a","P2","Acceptable for invoices, LLC filings and directories that do not need a storefront. Not for Google, Bing or Apple Maps listings.","None (setup)","Never use on Google Business Profile","Prerequisite")
a(C,"Dun & Bradstreet (D-U-N-S)","dnb.com","P1","Business credibility record US enterprise buyers and vendor forms check.","Keep updated","Get it for the US entity","Yes")

C="Core social"
a(C,"LinkedIn Company Page","linkedin.com/company/setup/new","P1","Main B2B channel. LinkedIn is among the top sources AI assistants cite for agency and B2B questions.","3-4 posts a week, case results, carousels, short video")
a(C,"LinkedIn personal profile (Pranay + Thomas)","linkedin.com","P1","Personal profiles get cited by ChatGPT and Google AI Mode more often than company pages. Founder voice sells.","Daily founder posts, client wins, opinions on AI search","Optimise headline, About, Featured section with RSM links")
a(C,"LinkedIn Newsletter + Articles","linkedin.com","P1","Long-form posts that get indexed and cited.","Weekly or fortnightly newsletter")
a(C,"LinkedIn Showcase Page","linkedin.com","P3","Separate page for a sub-brand (e.g. AI search service line).","Service-line updates","Only after main page is active")
a(C,"LinkedIn Groups (own group)","linkedin.com/groups","P2","Owned community for US business owners.","Weekly discussion prompt")
a(C,"Facebook Business Page","facebook.com/pages/create","P1","Trust signal, retargeting audiences, Google AI Overviews and AI Mode cite Facebook often.","3-5 posts a week, reels, reviews")
a(C,"Facebook Group (own group)","facebook.com/groups","P2","Owned community for small business owners.","Weekly tips, Q&A threads")
a(C,"Instagram Business","instagram.com","P1","Visual proof, reels, brand recall.","Reels, carousels, stories 4-5 a week")
a(C,"YouTube Channel","youtube.com","P1","Second most-cited domain in AI search after Reddit. Owns video search.","Weekly long video + Shorts (audits, walkthroughs)")
a(C,"X (Twitter)","x.com","P2","Quick takes on Google and AI-search updates; Grok sources from X.","Daily short posts, threads")
a(C,"Threads","threads.net","P2","Easy cross-post from Instagram, growing reach.","Cross-post from X/Instagram")
a(C,"Bluesky","bsky.app","P3","Reserve handle, marketing crowd present.","Cross-post")
a(C,"TikTok Business","tiktok.com/business","P3","Short video reach, younger owners.","Short tips, myth-busting")
a(C,"Pinterest Business","business.pinterest.com","P3","Infographics get long-life traffic and links.","Infographics, checklists")
a(C,"Mastodon","joinmastodon.org","P3","Reserve handle.","Cross-post")
a(C,"Snapchat Public Profile","snapchat.com","P3","Reserve handle only.","Optional")
a(C,"WhatsApp Business + Channel","business.whatsapp.com","P3","Useful for India and international clients; US buyers prefer phone, text and email.","Updates, offers")
a(C,"Telegram Channel","telegram.org","P3","Broadcast channel, reserve handle.","Cross-post updates")

C="Community / Q&A"
a(C,"Reddit (brand account + founder account)","reddit.com","P1","Most-cited domain across ChatGPT, Perplexity, Gemini and Google AI. Threads get cited, not profiles.","Genuine answers in r/smallbusiness, r/Entrepreneur, r/SEO, r/marketing, r/PPC and US city/business subreddits","No self-promo; build karma first, follow each subreddit's rules")
a(C,"Quora (profile + Quora Space)","quora.com","P1","Frequently cited by AI and ranks in Google.","3-5 detailed answers a week, own Space")
a(C,"Stack Exchange (Webmasters)","webmasters.stackexchange.com","P3","Technical authority answers.","Technical answers")
a(C,"Indie Hackers","indiehackers.com","P3","Founder audience.","Growth stories")
a(C,"Hacker News","news.ycombinator.com","P3","Tech audience, high authority.","Only strong original research")
a(C,"Product Hunt (maker profile)","producthunt.com","P3","Launch RSM tools (audit tool, Chrome extension).","Tool launches")
a(C,"Warrior Forum","warriorforum.com","P3","Marketing forum with profile signature.","Helpful replies")
a(C,"Digital Point Forums","forums.digitalpoint.com","P3","Old SEO forum, profile + signature.","Helpful replies")
a(C,"GrowthMentor / Growth communities","growthmentor.com","P3","Mentor profile, credibility.","Mentoring sessions")

C="Blogging / publishing"
a(C,"Medium (profile + publication)","medium.com","P1","Cited by Google AI Overviews and Gemini; good indexing.","Repurposed blog posts with link back")
a(C,"Substack","substack.com","P2","Newsletter + blog, strong discovery network.","Weekly AI-search newsletter")
a(C,"Blogger (Blogspot)","blogger.com","P2","Google-owned, quick indexing.","Repurposed posts, case studies")
a(C,"Google Sites","sites.google.com","P2","Google-owned brand page.","Service overview + links")
a(C,"WordPress.com","wordpress.com","P2","Free blog, extra brand page.","Repurposed posts")
a(C,"Tumblr","tumblr.com","P3","Extra brand property.","Short posts, visuals")
a(C,"HubPages","hubpages.com","P3","Long-form articles.","Guides")
a(C,"Vocal Media","vocal.media","P3","Long-form articles.","Guides")
a(C,"Beehiiv","beehiiv.com","P3","Alternative newsletter platform.","Optional if not using Substack")
a(C,"Notion public page","notion.so","P3","Public resource hub (templates, checklists).","Free resources")
a(C,"Weebly","weebly.com","P3","Extra brand page.","Service overview")
a(C,"Wix free site","wix.com","P3","Extra brand page.","Service overview")
a(C,"Strikingly","strikingly.com","P3","Extra brand page.","Service overview")
a(C,"Write.as","write.as","P3","Simple blog property.","Short posts")
a(C,"Flipboard","flipboard.com","P3","Curate own articles into a magazine.","Article curation")

C="Documents / slides"
a(C,"SlideShare","slideshare.net","P2","Decks get indexed, B2B audience.","Case study decks, reports")
a(C,"Issuu","issuu.com","P2","Publish PDF reports and guides.","Guides, reports")
a(C,"Scribd","scribd.com","P3","PDF publishing.","Guides")
a(C,"Speaker Deck","speakerdeck.com","P3","Slide decks.","Talks, decks")
a(C,"Calameo","calameo.com","P3","PDF publishing.","Guides")

C="Video / audio"
a(C,"Vimeo","vimeo.com","P2","Second video home, embeds on site.","Case study videos")
a(C,"Dailymotion","dailymotion.com","P3","Extra video reach.","Cross-post YouTube")
a(C,"Rumble","rumble.com","P3","Extra video reach.","Cross-post YouTube")
a(C,"Spotify for Creators (podcast)","creators.spotify.com","P2","Podcast hosting and distribution.","Weekly or fortnightly podcast")
a(C,"Apple Podcasts","podcastsconnect.apple.com","P2","Podcast listing.","Same podcast feed")
a(C,"YouTube Podcasts","youtube.com","P2","Podcast in YouTube.","Same podcast")
a(C,"Amazon Music / Audible podcasts","podcasters.amazon.com","P3","Podcast listing.","Same feed")
a(C,"SoundCloud","soundcloud.com","P3","Audio clips.","Podcast clips")

C="Visual / design"
a(C,"Behance","behance.net","P2","Show website and design work.","Website projects, designs")
a(C,"Dribbble","dribbble.com","P3","Design showcase.","UI shots")
a(C,"Flickr","flickr.com","P3","Image hosting with links.","Infographics, team photos")
a(C,"Visual.ly","visual.ly","P3","Infographic sharing.","Infographics")

C="Search engine / map profiles"
a(C,"Google Business Profile (US office)","business.google.com","P1","Shows RSM to US buyers in Google Maps and local results, feeds Google AI answers.","Weekly posts, photos, US client reviews","Only once the staffed US office exists","Yes")
a(C,"Google Business Profile (New Delhi office)","business.google.com","P2","Verifies RSM as a real company with a real team; supports hiring and the brand entity.","Team photos, office posts","Set up now with the Delhi address")
a(C,"Bing Places for Business","bingplaces.com","P1","Feeds Bing and Copilot; ChatGPT search draws on Bing data.","Keep in sync with GBP","List Delhi now, add the US location when staffed")
a(C,"Apple Business Connect","businessconnect.apple.com","P1","Apple Maps and Siri, heavily used in the US.","Showcases, photos","List Delhi now, add the US location when staffed")
a(C,"Bing Webmaster Tools + Google Search Console","bing.com/webmasters","P1","Not a profile, but required so new pages and posts get crawled fast.","Submit sitemaps")

C="Agency directories / reviews"
a(C,"Clutch","clutch.co","P1","Clutch appears in about 84.5% of AI-generated agency recommendations. Top priority.","Collect verified client reviews, portfolio","Prioritise reviews from US clients; list US service areas")
a(C,"The Manifest","themanifest.com","P2","Clutch sister site, auto-populates from Clutch.","Same reviews")
a(C,"GoodFirms","goodfirms.co","P1","Strong agency directory, often cited.","Reviews, portfolio")
a(C,"DesignRush","designrush.com","P1","Agency directory, ranks for agency queries.","Profile, portfolio")
a(C,"UpCity","upcity.com","P1","US-focused agency directory.","Reviews")
a(C,"Sortlist","sortlist.com","P2","Agency marketplace with leads.","Profile, reviews")
a(C,"Agency Spotter","agencyspotter.com","P2","Agency directory.","Profile, reviews")
a(C,"TopSEOs","topseos.com","P2","SEO agency rankings.","Profile")
a(C,"Agency Vista","agencyvista.com","P2","Agency directory.","Profile")
a(C,"Digital Agency Network","digitalagencynetwork.com","P3","Agency directory.","Profile")
a(C,"G2 (services listing)","g2.com","P2","Perplexity cites G2 for B2B queries.","Reviews")
a(C,"Trustpilot","trustpilot.com","P1","Review trust signal, shows in Google and AI answers.","Invite every happy client")
a(C,"Yelp for Business","biz.yelp.com","P1","Main US review site; Google AI Mode cites Yelp.","US client reviews","Needs US address","Yes")
a(C,"Better Business Bureau (BBB)","bbb.org","P1","US trust badge buyers recognise.","Accreditation","Needs US/Canada business presence","Yes")
a(C,"Expertise.com","expertise.com","P3","Curated lists, invite-based.","Apply when eligible")

C="Partner directories"
a(C,"Semrush Agency Partners","semrush.com/agencies","P1","Agency listing on a tool buyers already use.","Profile, case studies")
a(C,"Google Partners","google.com/partners","P1","Badge + partner search listing.","Needs Google Ads spend and certifications")
a(C,"HubSpot Solutions Directory","ecosystem.hubspot.com/marketplace/solutions","P1","Perplexity cites it in most agency answers in one 2026 study.","Needs HubSpot partner program")
a(C,"Meta Business Partners","facebook.com/business/marketing-partners","P3","Ads partner badge.","Needs ad spend")
a(C,"Shopify Partners Directory","shopify.com/partners/directory","P2","RSM builds Shopify stores.","Store builds")
a(C,"Wix Marketplace","wix.com/marketplace","P2","RSM builds Wix sites.","Projects")
a(C,"WordPress / Elementor Experts","elementor.com/experts","P3","RSM builds Elementor sites.","Projects")
a(C,"Microsoft Advertising Partners","about.ads.microsoft.com","P3","Bing Ads partner badge.","Needs ad spend")

C="Business data / entity profiles"
a(C,"Crunchbase","crunchbase.com","P1","Company data used by AI models and journalists.","Keep updated")
a(C,"Wikidata","wikidata.org","P2","Structured entity record AI models read.","Factual entry with references","Follow notability rules; no promotional text")
a(C,"ZoomInfo (claim profile)","zoominfo.com","P3","B2B data profile.","Keep updated")
a(C,"Owler","owler.com","P3","Company profile.","Keep updated")
a(C,"Kompass","kompass.com","P3","B2B directory.","Profile")
a(C,"F6S","f6s.com","P3","Startup/company profile.","Profile")
a(C,"About.me","about.me","P3","Founder profile page.","Founder bio")
a(C,"Gravatar","gravatar.com","P3","Founder identity across blogs.","Founder bio")
a(C,"Linktree","linktr.ee","P3","One link for all profiles.","Bio link hub")

C="Employer profiles"
a(C,"Glassdoor","glassdoor.com","P2","Employer brand, shows a 100+ team.","Team photos, culture")
a(C,"AmbitionBox","ambitionbox.com","P2","India employer brand.","Culture, reviews")
a(C,"Indeed Company Page","indeed.com","P3","Employer profile.","Openings")
a(C,"Naukri Employer","naukri.com","P3","Hiring in India.","Openings")

C="Freelance / lead marketplaces"
a(C,"Upwork (Agency profile)","upwork.com","P2","Inbound US projects.","Portfolio, proposals")
a(C,"Bark","bark.com","P2","Inbound leads US/UK/AU.","Lead responses")
a(C,"Fiverr Pro","fiverr.com","P3","Productised packages.","Gigs")
a(C,"PeoplePerHour","peopleperhour.com","P3","UK leads.","Proposals")
a(C,"Contra","contra.com","P3","Freelance profile.","Portfolio")
a(C,"Guru","guru.com","P3","Freelance profile.","Portfolio")
a(C,"Thumbtack","thumbtack.com","P2","US small business leads.","Lead responses","Needs US presence","Yes")

C="Earned mentions / PR"
a(C,"Featured.com","featured.com","P1","Expert quotes in publications, earned mentions AI picks up.","Answer 3-5 queries a week")
a(C,"Qwoted","qwoted.com","P2","Journalist requests.","Expert pitches","Pitch US publications first")
a(C,"Source of Sources","sourceofsources.com","P2","Journalist requests.","Expert pitches","Pitch US publications first")
a(C,"Help a B2B Writer","helpab2bwriter.com","P2","B2B journalist requests.","Expert pitches","Pitch US publications first")
a(C,"EIN Presswire","einpresswire.com","P3","Press release distribution.","Launch announcements")
a(C,"PR.com (company profile)","pr.com","P3","Company profile + releases.","Releases")
a(C,"OpenPR","openpr.com","P3","Free press releases.","Releases")

C="US citations"
for n,u in [("Yellow Pages","yellowpages.com"),("Manta","manta.com"),("Hotfrog","hotfrog.com"),("Foursquare","foursquare.com"),("MerchantCircle","merchantcircle.com"),("Brownbook","brownbook.net"),("Cylex","cylex.us.com"),("EZlocal","ezlocal.com"),("ShowMeLocal","showmelocal.com"),("Chamber of Commerce","chamberofcommerce.com")]:
    a(C,n,u,"P2","Consistent US name, address and phone across the web supports US map and AI visibility.","Profile only","Needs US address; keep NAP identical","Yes")
C="US business networks"
a(C,"Alignable","alignable.com","P2","Largest US small business network; referrals from US owners.","Weekly posts, Q&A","Needs US address","Yes")
a(C,"Local US Chamber of Commerce membership","uschamber.com/co/chambers","P2","Membership listing and events in the target US city.","Events, member posts","Needs US address","Yes")
a(C,"Nextdoor Business","business.nextdoor.com","P3","Local US neighbourhood reach.","Local offers","Needs US address","Yes")
a(C,"Forbes Agency Council","councils.forbes.com/forbesagencycouncil","P3","Vetted, paid membership; bylined articles on Forbes, which ChatGPT cites often.","Expert articles","Paid and application-based")
a(C,"US-based podcasts (guest appearances)","podmatch.com","P2","US audience hears the founder directly; episodes get cited and linked.","1-2 guest spots a month","PodMatch, MatchMaker.fm")
C="Canada / Australia citations"
for n,u,note in [("Yelp Canada","yelp.ca","Needs Canada address"),("Canada411 / YellowPages.ca","yellowpages.ca","Needs Canada address"),("Yellow Pages Australia","yellowpages.com.au","Needs AU address"),("True Local","truelocal.com.au","Needs AU address"),("Hotfrog Australia","hotfrog.com.au","Needs AU address")]:
    a(C,n,u,"P3","Presence for Canada/Australia clients (secondary markets).","Profile only",note)
C="India listings"
for n,u in [("Justdial","justdial.com"),("IndiaMART","indiamart.com"),("Sulekha","sulekha.com"),("TradeIndia","tradeindia.com")]:
    a(C,n,u,"P3","Delhi office presence and hiring only; not for US buyers.","Profile only","Do not spend posting time here")

with open("platforms.csv","w",newline="") as f:
    w=csv.writer(f)
    w.writerow(["#","Category","Platform","Sign-up / URL","Priority","Why it matters for RSM","What to post","Notes","Needs US presence","Status","Profile URL","Owner"])
    for i,r in enumerate(P,1):
        w.writerow([i]+r+["Not started","",""])
from collections import Counter
print(len(P), Counter(r[3] for r in P))
