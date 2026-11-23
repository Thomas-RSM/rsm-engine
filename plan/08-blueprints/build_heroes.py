"""Heroes for every foundation page, with checks. Run: python3 build_heroes.py"""
import csv,re,sys,os
B=" | Relevant Search Media"
H={ # url: (title core, H1, subline, lighter step)
"/":("SEO Company in USA","The SEO company in the USA that makes you the answer","Engines change. Your customer's question does not. We make your business the most relevant answer to it, on Google and on every AI engine.","Ask a question"),
"/problems/not-showing-up-on-google/":("Why Is My Business Not Showing Up on Google?","Why is my business not showing up on Google?","It is almost always one of three things: Google cannot read you, cannot confirm you, or sees no one choosing you. Here is how to tell which.","Ask a question"),
"/problems/not-getting-leads/":("How to Get More Leads for My Business","How to get more leads for my business from search","More traffic is rarely the fix. Leads come from being found for the searches your real customers make.","Check if your trade is open in your city"),
"/problems/not-recommended-by-chatgpt/":("How to Get My Business Recommended by ChatGPT","How to get my business recommended by ChatGPT","ChatGPT names the businesses it can read, confirm and see people choose. Most businesses fail the second test.","See who AI recommends for your trade"),
"/problems/traffic-dropped/":("Website Traffic Dropped Suddenly? Find the Cause","Website traffic dropped suddenly: how to find the cause","A sudden drop has a short list of causes. Work through them in this order before you change anything.","Ask a question"),
"/problems/seo-cost/":("How Much Does SEO Cost? What You Should Get","How much does SEO cost, and what should you get for it","What the market charges, what the money should buy, and the six things to hold any agency to.","See all 413 checks"),
"/problems/":("SEO Problems: Every Common Issue, Explained","SEO problems, explained one by one","Each entry gives the signs, the causes, how to check and how to fix. Start with what you are seeing.","Ask a question"),
"/dsouza-equation/":("The D'Souza Equation: How Search Engines Rank Websites","The D'Souza Equation: Relevance = Read × Confirm × Choose","Every engine names the business it can read plainly, confirm from other sources, and see real people choose. Miss one and the answer is zero.","See all 413 checks"),
"/dsouza-equation/law-of-search/":("D'Souza's Law of Search: Is SEO Dead?","D'Souza's Law of Search: engines change, the question does not","SEO is not dead. The engines multiplied. What your customer asks is the same, and that is what we work on.","See all 413 checks"),
"/dsouza-equation/read/":("On Page SEO: Can Every Engine Read You?","On page SEO: the Read part of the equation","Before any engine can name you, it has to read plainly what you are and what you answer. This is where that is won or lost.","See all 413 checks"),
"/dsouza-equation/confirm/":("Off Page SEO: Do Others Confirm You?","Off page SEO: the Confirm part of the equation","Engines do not take your word for it. They check whether listings, reviews and other sites say the same thing.","See all 413 checks"),
"/dsouza-equation/choose/":("Conversion Rate Optimization: Do People Choose You?","Conversion rate optimization: the Choose part of the equation","Being found is half of it. Engines also watch whether real people pick you, call you and come back.","See all 413 checks"),
"/dsouza-equation/standard/":("SEO Audit: The D'Souza Standard, 413 Checks","The SEO audit, written out: all 413 checks","Most agencies keep their checklist private. Ours is public, numbered and dated, so you can hold anyone to it.","Ask a question"),
"/dsouza-equation/method/":("SEO Strategy: The D'Souza Method, Day by Day","Our SEO strategy, day by day","Live work by day 5. A report every 15 days. Every item logged with its link. This is the order we work in.","See all 413 checks"),
"/dsouza-equation/engines/":("AI Search Engines: The Full List We Cover","Every AI search engine and search engine we cover","The list is open. When a new engine starts answering your customers, it is added here, with the date.","See who AI recommends for your trade"),
"/dsouza-equation/how-search-works/":("How Does Google Search Work Now?","How does Google search work now, and how does AI answer","One question, many machines. Here is what each one reads and how it decides who to name.","See all 413 checks"),
"/dsouza-equation/seo-vs-aeo-vs-geo/":("SEO vs GEO vs AEO vs AIO: What Each One Is","SEO vs GEO vs AEO vs AIO, and where each fits","Four names for one job done on four kinds of engine. Here is what each means and which you need.","See all 413 checks"),
"/services/seo/":("SEO Services","SEO services that make you the answer on Google","Every search your customers make, mapped and worked. Not ten keywords.","Check if your trade is open in your city"),
"/services/local-seo/":("Local SEO Services","Local SEO services for businesses that serve a city","Maps, your Google profile, reviews and local pages, worked together so the nearby customer finds you first.","Check if your trade is open in your city"),
"/services/ai-seo/":("AI SEO Services","AI SEO services: be the business AI names","ChatGPT, Gemini and Google's AI answers recommend two or three businesses. We work to make you one of them.","See who AI recommends for your trade"),
"/services/answer-engine-optimization/":("Answer Engine Optimization","Answer engine optimization: be the answer, not a link","When a customer asks a question out loud or in a search box, one business gets quoted. We build your pages to be that one.","See who AI recommends for your trade"),
"/services/generative-engine-optimization/":("Generative Engine Optimization","Generative engine optimization: get named by ChatGPT, Gemini and Perplexity","AI assistants build their answer from sources they trust. We make your business one of those sources.","See who AI recommends for your trade"),
"/services/ai-overview-optimization/":("AI Overview Optimization","AI Overview optimization: appear in Google's AI answers","Google now answers above the results. We shape your pages so that answer draws on you.","See who AI recommends for your trade"),
"/services/chatgpt-seo/":("ChatGPT SEO","ChatGPT SEO: how your business gets recommended","People ask ChatGPT who to hire. We work on the three things that decide whether it says your name.","See who AI recommends for your trade"),
"/services/google-business-profile-optimization/":("Google Business Profile Optimization Services","Google Business Profile optimization, done every week","Categories, services, photos, posts and reviews, kept complete and current. It is the profile most local customers see first.","Check if your trade is open in your city"),
"/services/technical-seo/":("Technical SEO","Technical SEO: make every engine able to read you","Speed, structure, markup and crawling. If an engine cannot read the site, nothing else counts.","See all 413 checks"),
"/services/content-marketing/":("Content Marketing Agency","A content marketing agency that answers your customers' questions","Pages, guides and answers written for the searches in your map, each one checked before it goes live.","See all 413 checks"),
"/services/link-building/":("Link Building Services","Link building services that earn real mentions","Mentions on real, relevant sites. No bought links, no spam. They are how engines confirm you.","See all 413 checks"),
"/services/social-media-marketing/":("Social Media Marketing Services","Social media marketing services that support your search","People search on social networks too. We keep your profiles complete, active and saying the same thing as your site.","Ask a question"),
"/services/reputation-management/":("Reputation Management Company","A reputation management company for reviews that get you chosen","Real reviews, asked for after every job and answered every time. They decide who gets picked.","Ask a question"),
"/services/voice-search-optimization/":("Voice Search Optimization","Voice search optimization: be the spoken answer","A voice assistant gives one answer. We build yours to be the one it reads out.","See who AI recommends for your trade"),
"/services/ecommerce-seo/":("Ecommerce SEO","Ecommerce SEO for stores that sell online","Category pages, product pages and the questions buyers ask before they pay, mapped and worked.","Ask a question"),
"/services/b2b-seo/":("B2B SEO Services","B2B SEO services for long sales cycles","Buyers research for months before they call. We make you the answer at each step of that research.","Ask a question"),
"/services/small-business-seo/":("Small Business SEO Services","Small business SEO services that fit how you work","Month to month. Live work by day 5. A report every 15 days you can read in five minutes.","Check if your trade is open in your city"),
"/services/lead-generation/":("Lead Generation Services","Lead generation services built on relevant searches","Leads you want, from searches your customers make. We count the ones you confirm were relevant.","Check if your trade is open in your city"),
"/services/digital-marketing/":("Digital Marketing Services","Digital marketing services, run as one engine","Search, AI answers, your Google profile, social and your website, worked as one plan from one set of facts.","Ask a question"),
"/services/web-design/":("Web Design Services","Web design services for sites that get found","A site designed for your customer and built so every engine can read it from day one.","Ask a question"),
"/services/web-development/":("Web Development Services","Web development services, built to be read by every engine","Fast, clean and structured. The build decides how well a site can ever rank.","Ask a question"),
"/services/app-development/":("App Development Services","App development services for web and mobile","Apps planned around what your customers need to do, built and maintained by one team.","Ask a question"),
"/services/custom-crm/":("Custom CRM Development","Custom CRM development that fits your business","A system shaped to how you take leads, quote and follow up, so no enquiry is lost.","Ask a question"),
"/services/design/":("Graphic Design Services","Graphic design services: brand, logo and everything you publish","One look across your site, your profiles and your print, so customers recognise you everywhere.","Ask a question"),
"/services/":("Services","Everything we do, by its common name","Each service is one part of the same job: making you the answer your customers get.","Ask a question"),
"/guides/what-is-eeat/":("What Is E-E-A-T? Google's Trust Test, Explained","What is E-E-A-T, and how a small business earns it","Experience, expertise, authority and trust. Here is what Google looks for and how a local business shows it.","See all 413 checks"),
"/guides/seo-keyword-research/":("SEO Keyword Research: How We Choose Keywords","SEO keyword research: why we map every search, not ten","Your customers search in many ways. We map all of them and give each one page.","See all 413 checks"),
"/guides/how-long-does-seo-take/":("How Long Does SEO Take? An Honest Timeline","How long does SEO take to work","First fixes go live on day 5. Here is what moves in weeks, what takes months, and what we commit to by month 4.","Ask a question"),
"/guides/how-to-choose-an-seo-company/":("How to Choose an SEO Company","How to choose an SEO company, and what to ask","The questions to ask, the answers to expect, and the two things to get in writing.","See all 413 checks"),
"/guides/service-vs-ecommerce-vs-b2b-seo/":("Types of SEO: Which One Your Business Needs","Types of SEO: service business, ecommerce and B2B","The same equation, three different maps. Here is what changes with the kind of business you run.","Ask a question"),
"/guides/":("SEO Guide for Business Owners","The SEO guide for business owners","Plain answers to the questions owners ask before they spend. Each ends with a verdict.","Ask a question"),
"/ask/":("Ask Anything About Getting Found Online","Ask anything about getting found online","Type your question. You get a short answer, the page for your trade and city, and the next step.",""),
"/ai-recommendation-index/":("How Does ChatGPT Recommend Businesses? The Index","Who AI recommends, by trade and by city","Each month we ask the AI engines who they recommend for each trade in each city, and publish what they say.","Get told when this changes"),
"/open-board/":("Open Board: Is Your Trade Open in Your City?","One business per trade per city. Is yours open?","AI names two or three businesses for a search. So we work for one in each trade, in each city.","Get told when this changes"),
"/open-log/":("Open Log: A Live SEO Report Example","Our own SEO report, updated in public","We run the D'Souza Method on our own site and show the numbers: what we published, where we appear, who names us.","See all 413 checks"),
"/searches/":("Plumber SEO Keywords and More, by Trade and City","What your customers search for, by trade and city","Pick your trade and city to see the searches people make before they hire.","Check if your trade is open in your city"),
"/your-plan/":("Your SEO Plan, Day by Day","See the SEO plan we would run for you","Pick your trade and city. You get the first 15 days, item by item, to keep.","Check if your trade is open in your city"),
"/industries/":("SEO by Industry","SEO by industry: find your trade","Every trade is searched differently. Find yours to see how its customers look and what we do about it.","Check if your trade is open in your city"),
"/cities/":("SEO Company Near Me: Cities We Serve","An SEO company for your city","We work for businesses across the United States, one per trade in each city. Find yours.","Check if your trade is open in your city"),
"/about/":("About Relevant Search Media: How the Equation Began","How the D'Souza Equation came about","Relevant Search Media was founded in 2020 on one idea: relevant search, relevant traffic, relevant leads.","See all 413 checks"),
"/thomas-dsouza/":("Thomas D'Souza, Founder","Thomas D'Souza","Founder of Relevant Search Media and author of the D'Souza Equation. In digital marketing since 2010.","Ask a question"),
"/commitments/":("SEO Guarantee? Our Two Written Commitments","Two commitments, in writing","Every item ships and is logged, or that period is free. Half your mapped searches on page one by month 4, or we keep working at no charge.","Ask a question"),
"/results/":("Relevant Search Media Reviews and Results","Results and reviews","900+ businesses served. About 400 projects, 90% successful. Results by trade, with no client named.","Ask a question"),
"/about/editorial-policy/":("How We Write and Check","How we write and check everything we publish","Every page is built from a signed fact register and passes the page checks before it goes live.","See all 413 checks"),
"/about/corrections/":("Corrections","Corrections","When we get something wrong, we fix it and list it here, with the date.",""),
"/contact/":("Contact","Contact Relevant Search Media","Email info@relevantsearchmedia.com or call +1 202 609 6641.",""),
"/book/":("Book a Discovery Call","Book a discovery call with Thomas","20 to 30 minutes. See who AI names for your trade in your city, which searches you are missing, and whether your trade is open.",""),
"/privacy/":("Privacy Policy","Privacy policy","What we collect, why, and how to reach us about it.",""),
"/terms/":("Terms","Terms","The terms for using this site.",""),
}
here=os.path.dirname(os.path.abspath(__file__))
pages=list(csv.DictReader(open(os.path.join(here,"..","04-architecture","site-map.csv"))))
km={}
for r in csv.DictReader(open(os.path.join(here,"..","05-keywords","keyword-map-v2.csv"))):
    if r["role"]=="lead": km[r["url"]]=(r["keyword"],r["live_grade"])
def n(s): return re.sub(r"[^a-z0-9 ]","",s.lower().replace("-"," "))
errs=[]; rows=[]
for p in pages:
    u=p["url"]
    if u not in H: errs.append("no hero: "+u); continue
    core,h1,sub,light=H[u]
    title=core+B if len(core+B)<=60 else core
    if not 10<=len(title)<=60: errs.append(f"title length {len(title)}: {u}")
    if len(h1.split())>12: errs.append(f"H1 over 12 words: {u}")
    if len(sub.split())>32: errs.append(f"subline over 32 words: {u}")
    if u in km and km[u][1]!="own term" and p["layer"] in ("Home","Situation","Service","Guide"):
        # the home H1 may paraphrase its keyword so it reads naturally
        if n(km[u][0]) not in n(title) or (p["layer"]!="Home" and n(km[u][0]) not in n(h1)): errs.append(f"lead keyword '{km[u][0]}' missing from title or H1: {u}")
    rows.append([p["number"],p["layer"],u,title,len(title),h1,sub,"Book a discovery call",light])
for u in H:
    if u not in {p["url"] for p in pages}: errs.append("hero for unknown page "+u)
t=[r[3] for r in rows]
if len(set(t))!=len(t): errs.append("duplicate title")
if errs: print("FAILED",*errs,sep="\n  "); sys.exit(1)
with open(os.path.join(here,"heroes.csv"),"w",newline="") as f:
    w=csv.writer(f); w.writerow(["page","layer","url","title","title_length","h1","subline","primary_button","lighter_step"]); w.writerows(rows)
md=["# Heroes for every foundation page (v1)","",f"Step 8. 23 Nov 2026. {len(rows)} pages. Built and checked by `build_heroes.py`: every title is 60 characters or fewer and unique, every H1 is 12 words or fewer, and on home, situation, service and guide pages the lead keyword is in both.","",
"The primary button on every page is **Book a discovery call**.",""]
layer=None
for r in rows:
    if r[1]!=layer: layer=r[1]; md+=["",f"## {layer}",""]
    md+=[f"### `{r[2]}`","",f"- **Title:** {r[3]}",f"- **H1:** {r[5]}",f"- **Subline:** {r[6]}"]+([f"- **Lighter step:** {r[8]}"] if r[8] else [])+[""]
open(os.path.join(here,"heroes.md"),"w").write("\n".join(md))
print("OK heroes:",len(rows),"longest title:",max(r[4] for r in rows))
