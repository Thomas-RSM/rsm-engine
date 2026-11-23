"""Element pages: one page per thing RSM checks or does, grouped the way the D'Souza Standard is.
Run: python3 build_elements.py"""
import csv,sys,os,re
here=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(here,"..","05-keywords"))
from kwlib import grade,save
# where, equation term, standard group, element (page name), slug, lead keyword
E=[
# ---- On the site: technical
("On the site","Read","Technical health","Robots.txt","robots-txt","robots.txt"),
("On the site","Read","Technical health","XML sitemap","xml-sitemap","xml sitemap"),
("On the site","Read","Technical health","Canonical tags","canonical-tags","canonical url"),
("On the site","Read","Technical health","Redirects","301-redirects","301 redirect"),
("On the site","Read","Technical health","404 pages and broken links","broken-links","broken links"),
("On the site","Read","Technical health","Indexing","google-indexing","google indexing"),
("On the site","Read","Technical health","Crawling","crawl-errors","crawl errors"),
("On the site","Read","Technical health","Duplicate pages","duplicate-content","duplicate content"),
("On the site","Read","Technical health","URL structure","url-structure","url structure"),
("On the site","Read","Technical health","IndexNow","indexnow","indexnow"),
("On the site","Read","Speed and stability","Core Web Vitals","core-web-vitals","core web vitals"),
("On the site","Read","Speed and stability","Page speed","page-speed","page speed"),
("On the site","Read","Speed and stability","Largest Contentful Paint","largest-contentful-paint","largest contentful paint"),
("On the site","Read","Speed and stability","Interaction to Next Paint","interaction-to-next-paint","interaction to next paint"),
("On the site","Read","Speed and stability","Cumulative Layout Shift","cumulative-layout-shift","cumulative layout shift"),
("On the site","Read","Speed and stability","Image compression","image-compression","image compression"),
("On the site","Read","Speed and stability","Lazy loading","lazy-loading","lazy loading"),
("On the site","Read","Speed and stability","Website hosting and uptime","website-uptime","website uptime"),
("On the site","Read","Mobile experience","Mobile-friendly pages","mobile-friendly-website","mobile friendly website"),
("On the site","Read","Mobile experience","Click-to-call","click-to-call","click to call"),
("On the site","Read","Security","HTTPS and SSL","ssl-certificate","ssl certificate"),
("On the site","Read","Security","Security headers","security-headers","security headers"),
("On the site","Read","Security","Website backups","website-backup","website backup"),
("On the site","Read","Site structure","Site structure","site-structure","website structure"),
("On the site","Read","Site structure","Internal links","internal-linking","internal linking"),
("On the site","Read","Site structure","Navigation menu","website-navigation","website navigation"),
("On the site","Read","Site structure","Breadcrumbs","breadcrumbs","breadcrumbs seo"),
("On the site","Read","Site structure","Orphan pages","orphan-pages","orphan pages"),
("On the site","Read","Site structure","Keyword cannibalization","keyword-cannibalization","keyword cannibalization"),
# ---- On the site: page
("On the site","Read","Page titles and descriptions","Title tags","title-tag","title tag"),
("On the site","Read","Page titles and descriptions","Meta descriptions","meta-description","meta description"),
("On the site","Read","Page titles and descriptions","Open Graph tags","open-graph-tags","open graph tags"),
("On the site","Read","Headings and copy","H1 and heading tags","heading-tags","heading tags"),
("On the site","Read","Headings and copy","Keyword placement","keyword-density","keyword density"),
("On the site","Read","Headings and copy","Thin content","thin-content","thin content"),
("On the site","Read","Headings and copy","Readability","readability","readability score"),
("On the site","Read","Headings and copy","Service pages","service-pages","service page"),
("On the site","Read","Images and media","Image alt text","alt-text","alt text"),
("On the site","Read","Images and media","Image file names","image-seo","image seo"),
("On the site","Read","Verified facts","Schema markup","schema-markup","schema markup"),
("On the site","Read","Verified facts","Local business schema","local-business-schema","local business schema"),
("On the site","Read","Verified facts","FAQ schema","faq-schema","faq schema"),
("On the site","Read","Verified facts","Organization schema","organization-schema","organization schema"),
("On the site","Read","Verified facts","Review schema","review-schema","review schema"),
("On the site","Read","Verified facts","Breadcrumb schema","breadcrumb-schema","breadcrumb schema"),
("On the site","Read","AI readiness","Answer blocks","featured-snippets","featured snippets"),
("On the site","Read","AI readiness","FAQ sections","faq-page","faq page"),
("On the site","Read","AI readiness","llms.txt","llms-txt","llms.txt"),
("On the site","Read","AI readiness","AI crawler access","ai-crawlers","ai crawlers"),
("On the site","Read","AI readiness","People Also Ask","people-also-ask","people also ask"),
("On the site","Read","Content inventory","Content audit","content-audit","content audit"),
("On the site","Read","Content inventory","Content pruning","content-pruning","content pruning"),
("On the site","Read","Uniqueness and information gain","Original content","information-gain","information gain seo"),
("On the site","Read","Uniqueness and information gain","Doorway pages","doorway-pages","doorway pages"),
("On the site","Read","Fact integrity","Fact checking","fact-checking","fact checking"),
("On the site","Read","Accessibility","Website accessibility","website-accessibility","website accessibility"),
("On the site","Read","Accessibility","Color contrast","color-contrast","color contrast checker"),
("On the site","Read","Freshness and corrections","Content freshness","content-freshness","content freshness"),
("On the site","Read","Publishing readiness","Publishing checklist","seo-checklist","seo checklist"),
# ---- On the site: choose
("On the site","Choose","Conversion elements","Calls to action","call-to-action","call to action"),
("On the site","Choose","Conversion elements","Contact forms","contact-form","contact form"),
("On the site","Choose","Conversion elements","Landing pages","landing-page","landing page"),
("On the site","Choose","Conversion elements","Trust badges","trust-badges","trust badges"),
("On the site","Choose","Conversion elements","Live chat","live-chat","live chat for website"),
("On the site","Choose","Conversion elements","Speed to lead","speed-to-lead","speed to lead"),
("On the site","Choose","Conversion elements","Pricing pages","pricing-page","pricing page"),
# ---- Listings and local
("Listings","Confirm","Local signals","NAP consistency","nap-consistency","nap consistency"),
("Listings","Confirm","Local signals","Local citations","local-citations","local citations"),
("Listings","Confirm","Local signals","Business directories","business-directories","business directories"),
("Listings","Confirm","Local signals","Service area pages","service-area-pages","service area business"),
("Listings","Confirm","Local signals","Apple Business Connect","apple-business-connect","apple business connect"),
("Listings","Confirm","Local signals","Bing Places","bing-places","bing places"),
("Listings","Confirm","Local signals","Duplicate listings","duplicate-listings","duplicate listings"),
("Listings","Confirm","Google Business Profile","Google Business Profile categories","google-business-profile-categories","google business profile categories"),
("Listings","Confirm","Google Business Profile","Google Business Profile posts","google-business-profile-posts","google business profile posts"),
("Listings","Confirm","Google Business Profile","Google Business Profile photos","google-business-profile-photos","google business profile photos"),
("Listings","Confirm","Google Business Profile","Google Business Profile services","google-business-profile-services","google business profile services"),
("Listings","Confirm","Google Business Profile","Google Business Profile suspension","google-business-profile-suspended","google business profile suspended"),
("Listings","Confirm","Google Business Profile","Google Maps ranking","google-maps-ranking","google maps ranking"),
("Listings","Confirm","Reviews and reputation","Google reviews","google-reviews","how to get google reviews"),
("Listings","Confirm","Reviews and reputation","Responding to reviews","respond-to-reviews","how to respond to google reviews"),
("Listings","Confirm","Reviews and reputation","Negative reviews","negative-reviews","how to respond to negative reviews"),
# ---- Off the site
("Off the site","Confirm","Off-site presence","Backlinks","backlinks","backlinks"),
("Off the site","Confirm","Off-site presence","Brand mentions","brand-mentions","brand mentions"),
("Off the site","Confirm","Off-site presence","Press releases","press-release","press release"),
("Off the site","Confirm","Off-site presence","Guest posts","guest-posting","guest posting"),
("Off the site","Confirm","Off-site presence","Toxic links","toxic-backlinks","toxic backlinks"),
("Off the site","Confirm","Off-site presence","Anchor text","anchor-text","anchor text"),
("Off the site","Confirm","Off-site presence","Digital PR","digital-pr","digital pr agency"),
("Off the site","Confirm","Off-site presence","Reddit and forums","reddit-marketing","reddit marketing"),
("Off the site","Confirm","Author and entity","Author pages","author-bio","author bio"),
("Off the site","Confirm","Author and entity","Knowledge panel","google-knowledge-panel","google knowledge panel"),
("Off the site","Confirm","Author and entity","Entity SEO","entity-seo","entity seo"),
("Off the site","Confirm","Video and visual search","YouTube SEO","youtube-seo","youtube seo"),
("Off the site","Confirm","Video and visual search","Video SEO","video-seo","video seo"),
# ---- Social
("Social","Confirm","Social presence","Facebook business page","facebook-business-page","facebook business page"),
("Social","Confirm","Social presence","Instagram for business","instagram-for-business","instagram for business"),
("Social","Confirm","Social presence","LinkedIn company page","linkedin-company-page","linkedin company page"),
("Social","Confirm","Social presence","TikTok for business","tiktok-for-business","tiktok for business"),
("Social","Confirm","Social presence","Social media posting schedule","social-media-posting-schedule","social media posting schedule"),
("Social","Confirm","Social presence","Social media profiles","social-media-profiles","social media profiles"),
# ---- The question and measurement
("Research","Question","Search map coverage","Search intent","search-intent","search intent"),
("Research","Question","Search map coverage","Keyword mapping","keyword-mapping","keyword mapping"),
("Research","Question","Search map coverage","Long-tail keywords","long-tail-keywords","long tail keywords"),
("Research","Question","Search map coverage","Competitor analysis","seo-competitor-analysis","seo competitor analysis"),
("Measurement","Choose","Tracking and measurement","Google Analytics 4","google-analytics-4","google analytics 4"),
("Measurement","Choose","Tracking and measurement","Google Search Console","google-search-console","google search console"),
("Measurement","Choose","Tracking and measurement","Call tracking","call-tracking","call tracking"),
("Measurement","Choose","Tracking and measurement","UTM tracking","utm-parameters","utm parameters"),
("Measurement","Choose","Tracking and measurement","Rank tracking","rank-tracking","rank tracker"),
("Measurement","Choose","Tracking and measurement","SEO reporting","seo-report","seo report"),
("Measurement","Choose","AI answer verification","AI visibility tracking","ai-visibility","ai visibility"),
("Measurement","Choose","AI answer verification","AI citations","ai-citations","ai citations"),
]
errs=[]; slugs=[e[4] for e in E]; kws=[e[5] for e in E]
if len(set(slugs))!=len(slugs): errs.append("duplicate slug: "+str({s for s in slugs if slugs.count(s)>1}))
if len(set(kws))!=len(kws): errs.append("duplicate keyword")
locked={r["keyword"] for r in csv.DictReader(open(os.path.join(here,"..","05-keywords","keyword-map-v2.csv"))) if r["keyword"]}
clash=[k for k in kws if k in locked]
if clash: errs.append("keyword already locked to a foundation page: "+str(clash))
groups={r["group"] for r in csv.DictReader(open(os.path.join(here,"..","03-standard","dsouza-standard.csv")))}
for e in E:
    if e[2] not in groups: errs.append("unknown standard group: "+e[2])
    if not re.fullmatch(r"[a-z0-9-]+",e[4]): errs.append("bad slug "+e[4])
if errs: print("FAILED",*errs,sep="\n  "); sys.exit(1)
rows=[[i,e[0],e[1],e[2],e[3],f"/elements/{e[4]}/",e[5],grade(e[5])] for i,e in enumerate(E,1)]
save()
with open(os.path.join(here,"elements.csv"),"w",newline="") as f:
    w=csv.writer(f); w.writerow(["number","where","equation_term","standard_group","element","url","lead_keyword","live_grade"]); w.writerows(rows)
from collections import Counter
g=Counter(r[7] for r in rows); wh=Counter(r[1] for r in rows); tm=Counter(r[2] for r in rows)
md=["# Element pages (v1)","",
f"Added 23 Nov 2026 at Thomas's direction. **{len(rows)} element pages**: one page for each thing RSM analyses or does, on the site, off the site, on listings and on social.","",
"## What an element page is","",
"The D'Souza Standard lists 413 checks. An element is the thing a group of those checks is about: a title tag, a Google review, a local citation, a schema block. Each element gets its own page, so the Standard becomes a library an owner can search and read.","",
"Every element page follows one blueprint:","",
"1. **What it is**, in 40 to 60 words, under the term people search.",
"2. **Why engines care**: which part of the equation it serves, Read, Confirm or Choose.",
"3. **What good looks like**, with a real example.",
"4. **Check yours in ten minutes.**",
"5. **How everyone should do it, and how RSM does it.**",
"6. **The checks**: the numbered checks of the Standard that cover it.",
"7. **Related elements**, and the service that includes it.",
"8. Book a discovery call. Lighter step: see all 413 checks.","",
"## Where they sit","",
"- Address: `/elements/<name>/`, under a hub at `/elements/`.",
"- Menu: a column in \"The Equation\" menu, grouped as below.",
"- Links: every service page links to its elements; every element links to its Standard group, its part of the equation and its service.","",
"## Count","","| Where the work happens | Pages |","|---|---|"]+[f"| {k} | {v} |" for k,v in wh.items()]+[f"| **Total** | **{len(rows)}** |","",
"| Part of the equation | Pages |","|---|---|"]+[f"| {k} | {v} |" for k,v in tm.items()]+["",
f"Live evidence for the lead keywords: {g.get('A',0)} confirmed real searches, {g.get('B',0)} weak signals, {g.get('C',0)+g.get('D',0)} without a signal. No element keyword is already locked to a foundation page.","",
"## All elements","","| # | Element | Where | Equation | Standard group | Lead keyword | Evidence |","|---|---|---|---|---|---|---|"]
for r in rows: md.append(f"| {r[0]} | {r[4]} | {r[1]} | {r[2]} | {r[3]} | {r[6]} | {r[7]} |")
md+=["","## Order of building","",
"The 66 foundation pages come first. Element pages follow in this order: the ones every service page links to, then the rest by group. Each passes the page gate before it goes live."]
open(os.path.join(here,"elements.md"),"w").write("\n".join(md))
print("OK elements:",len(rows),dict(wh),"grades:",dict(g))
for r in rows:
    if r[7] not in ("A",): print(" ",r[7],r[6])
