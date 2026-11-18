import re, collections
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

# ---------------- CITIES ----------------
LAUNCH = [("New York","NY",["nyc"]),("Los Angeles","CA",[]),("Chicago","IL",[]),("Houston","TX",[]),("Dallas","TX",[]),
          ("Miami","FL",[]),("Atlanta","GA",[]),("Phoenix","AZ",[]),("Denver","CO",[]),("Fresno","CA",[])]
WAVE2 = ["Philadelphia, PA","San Antonio, TX","San Diego, CA","Austin, TX","San Jose, CA","Jacksonville, FL","Fort Worth, TX","Columbus, OH","Charlotte, NC","Indianapolis, IN",
         "San Francisco, CA","Seattle, WA","Washington, DC","Boston, MA","Nashville, TN","Las Vegas, NV","Orlando, FL","Tampa, FL","Detroit, MI","Minneapolis, MN"]
WAVE3 = ["Portland, OR","Oklahoma City, OK","El Paso, TX","Memphis, TN","Louisville, KY","Baltimore, MD","Milwaukee, WI","Albuquerque, NM","Tucson, AZ","Sacramento, CA",
         "Kansas City, MO","Mesa, AZ","Omaha, NE","Raleigh, NC","Colorado Springs, CO","Long Beach, CA","Virginia Beach, VA","Oakland, CA","Tulsa, OK","Frisco, TX"]

# ---------------- BUYER CATEGORIES ----------------
# name, adj, extra adjs, plural, singular business, their customers, tier
IND = [
("Dental","dental",["dentist"],"dentists","dental practice","patients","A"),
("Orthodontics","orthodontist",[],"orthodontists","orthodontic practice","patients","B"),
("Law Firm","law firm",["lawyer","attorney"],"lawyers","law firm","clients","A"),
("Personal Injury Law","personal injury lawyer",[],"personal injury lawyers","personal injury law firm","cases","A"),
("Family Law","family law",[],"family lawyers","family law firm","clients","B"),
("Criminal Defense Law","criminal defense",[],"criminal defense lawyers","criminal defense law firm","clients","B"),
("Immigration Law","immigration lawyer",[],"immigration lawyers","immigration law firm","clients","B"),
("Plumbing","plumbing",["plumber"],"plumbers","plumbing company","service calls","A"),
("HVAC","hvac",[],"hvac companies","hvac company","service calls","A"),
("Roofing","roofing",["roofer"],"roofers","roofing company","roofing leads","A"),
("Electrical","electrician",[],"electricians","electrical company","service calls","B"),
("Home Services","home services",[],"home service companies","home service company","booked jobs","A"),
("General Contractor","contractor",["construction"],"contractors","construction company","project leads","A"),
("Home Remodeling","remodeling",[],"remodeling contractors","remodeling company","project leads","B"),
("Painting","painting",["painter"],"painters","painting company","estimates","B"),
("Landscaping","landscaping",[],"landscapers","landscaping company","customers","B"),
("Pest Control","pest control",[],"pest control companies","pest control company","customers","B"),
("Cleaning Services","cleaning company",[],"cleaning companies","cleaning company","customers","B"),
("Moving","moving company",[],"movers","moving company","bookings","B"),
("Garage Door","garage door",[],"garage door companies","garage door company","service calls","C"),
("Flooring","flooring",[],"flooring companies","flooring company","customers","C"),
("Pool Builders","pool company",[],"pool builders","pool company","project leads","C"),
("Tree Service","tree service",[],"tree service companies","tree service company","customers","C"),
("Solar","solar",[],"solar companies","solar company","leads","B"),
("Real Estate","real estate",["realtor"],"realtors","real estate business","buyer and seller leads","A"),
("Mortgage","mortgage broker",[],"mortgage brokers","mortgage company","loan leads","C"),
("Financial Advisors","financial advisor",[],"financial advisors","financial advisory firm","clients","A"),
("Insurance","insurance agency",[],"insurance agents","insurance agency","policy leads","B"),
("Accounting","accounting",["cpa"],"accountants","accounting firm","clients","B"),
("Medical Practice","medical",["healthcare"],"doctors","medical practice","patients","A"),
("Med Spa","med spa",[],"med spas","med spa","bookings","A"),
("Plastic Surgery","plastic surgery",[],"plastic surgeons","plastic surgery practice","consultations","B"),
("Chiropractic","chiropractic",["chiropractor"],"chiropractors","chiropractic practice","patients","B"),
("Dermatology","dermatology",[],"dermatologists","dermatology practice","patients","C"),
("Therapy & Counseling","therapist",[],"therapists","therapy practice","clients","C"),
("Veterinary","veterinary",[],"veterinarians","veterinary clinic","clients","C"),
("Home Care","home care",[],"home care agencies","home care agency","client inquiries","C"),
("Restaurants","restaurant",[],"restaurants","restaurant","reservations","B"),
("Hotels","hotel",[],"hotels","hotel","direct bookings","C"),
("Auto Repair","auto repair",[],"auto repair shops","auto repair shop","customers","B"),
("Car Dealerships","car dealership",[],"car dealerships","car dealership","buyers","C"),
("Limo & Transportation","limo",[],"limo companies","limo company","bookings","C"),
("Laundry & Dry Cleaning","laundromat",[],"laundromats","laundromat","customers","C"),
("Security Companies","security company",[],"security companies","security company","contracts","C"),
("Gyms & Fitness","gym",[],"gyms","gym","members","C"),
("Ecommerce","ecommerce",[],"ecommerce stores","ecommerce store","sales","A"),
("B2B & SaaS","b2b",["saas"],"b2b companies","b2b company","qualified leads","B"),
("Manufacturing","manufacturing",["industrial"],"manufacturers","manufacturing company","quote requests","B"),
("Small Business","small business",["local business"],"small businesses","small business","customers","A"),
]

# ---------------- CORE SERVICE LINES ----------------
# line, terms, takes provider nouns?
SVC = [
("SEO",["seo","search engine optimization"],True),
("Local SEO",["local seo","google maps seo"],True),
("AI SEO",["ai seo","ai search optimization","ai search engine optimization"],True),
("AEO",["aeo","answer engine optimization"],True),
("GEO",["geo","generative engine optimization"],True),
("AIO",["aio","ai overview optimization"],True),
("ChatGPT & LLM",["chatgpt seo","chatgpt optimization","llm seo","llm optimization"],True),
("Digital Marketing",["digital marketing","internet marketing","online marketing"],True),
("Web Design",["web design","website design","web development"],True),
("Lead Generation",["lead generation"],True),
("Google Business Profile",["google business profile optimization","google my business optimization"],True),
("Content Marketing",["content marketing"],True),
("Link Building",["link building"],True),
("Social Media",["social media marketing"],True),
("Reputation Management",["reputation management"],True),
("Ecommerce SEO",["ecommerce seo","shopify seo"],True),
("Technical SEO",["technical seo"],True),
("Small Business SEO",["small business seo"],True),
("Voice Search",["voice search optimization"],True),
]
SOLO = [ # term, line
("seo consultant","SEO"),("seo expert","SEO"),("seo specialist","SEO"),("seo firm","SEO"),("seo audit","SEO"),("seo marketing","SEO"),
("ai seo consultant","AI SEO"),("ai seo expert","AI SEO"),("aeo consultant","AEO"),("geo consultant","GEO"),
("local seo expert","Local SEO"),("google ranking services","SEO"),("marketing agency","Digital Marketing"),("marketing company","Digital Marketing"),
("web designer","Web Design"),("wordpress web design","Web Design"),("shopify web design","Web Design"),("website redesign","Web Design"),
("schema markup services","Technical SEO"),("google ai overview seo","AIO"),("perplexity seo","ChatGPT & LLM"),("gemini seo","ChatGPT & LLM"),
("ai visibility agency","AI SEO"),("ai marketing agency","AI SEO"),("search everywhere optimization","AI SEO"),
]

def art(s): return ("an " if s[0] in "aeio" or s.startswith(("hvac","mri")) else "a ")+s

NOTE = {
"Primary - Core":"Money term: buyer is looking for a provider in this city now. Locked to its city service page.",
"Primary - Industry":"Money term: a business owner in this category looking for a specialist in this city. Locked to its category x city page.",
"Secondary":"Qualifier variant (best / top / affordable / cost) of a primary. Supports the same locked page; never gets its own competing page.",
"Question":"Real question a buyer asks before hiring. One question page, answer in the first 40-60 words, links up to the locked page.",
"AEO":"Direct-answer query (voice, featured answer, assistant). Needs a standalone quotable answer block.",
"AIO":"Query type that triggers Google AI Overviews / AI Mode. Needs list-style, source-worthy content with fresh dates.",
"GEO & AI SEO":"Demand for being named by ChatGPT, Gemini, Perplexity and Google AI. RSM's differentiator layer.",
"E-E-A-T":"Trust-check search made before contacting an agency. Served by proof, reviews, method and author pages.",
"Comparison":"Buyer weighing options. One fair comparison page per pair, feeding the locked page.",
"AI Prompt":"Full prompt typed into ChatGPT / Gemini / Perplexity / Claude. Tracked for mentions, not Google rank.",
}
INTENT = {"Primary - Core":"Transactional","Primary - Industry":"Transactional","Secondary":"Commercial","Question":"Informational > Commercial",
"AEO":"Informational","AIO":"Commercial investigation","GEO & AI SEO":"Commercial","E-E-A-T":"Trust / validation","Comparison":"Commercial investigation","AI Prompt":"Conversational"}

def gen(city, aliases):
    C = city.lower(); rows=[]; seen=set()
    def add(kw, sec, cat, line, pri, lower=True):
        k = kw.lower() if lower else kw
        k = re.sub(r"\s+"," ",k).strip()
        if k.lower() in seen: return
        seen.add(k.lower())
        grp = f"{city} | {cat} | {line}"
        rows.append([k, sec, cat, line, INTENT[sec], pri, grp, NOTE[sec]])
    G="Agency (all industries)"
    # ---- Primary core
    for line,terms,_ in SVC:
        top = line in ("SEO","Local SEO","AI SEO","Digital Marketing","Web Design","AEO","GEO")
        for t in terms:
            for p in ("company","agency","services"):
                add(f"{t} {p} {C}","Primary - Core",G,line,"P1" if top else "P2")
                add(f"{C} {t} {p}","Primary - Core",G,line,"P1" if top else "P2")
            add(f"{t} {C}","Primary - Core",G,line,"P1" if top else "P2")
            add(f"{C} {t}","Primary - Core",G,line,"P1" if top else "P2")
            add(f"{t} experts {C}","Primary - Core",G,line,"P2")
            for a in aliases:
                add(f"{t} company {a}","Primary - Core",G,line,"P2"); add(f"{t} agency {a}","Primary - Core",G,line,"P2")
                add(f"{a} {t}","Primary - Core",G,line,"P2"); add(f"{t} services {a}","Primary - Core",G,line,"P2")
    for t,line in SOLO:
        add(f"{t} {C}","Primary - Core",G,line,"P2"); add(f"{C} {t}","Primary - Core",G,line,"P2")
        for a in aliases: add(f"{t} {a}","Primary - Core",G,line,"P3")
    # ---- Secondary core
    heads=[("seo company","SEO"),("seo agency","SEO"),("seo services","SEO"),("local seo company","Local SEO"),("ai seo agency","AI SEO"),
           ("digital marketing agency","Digital Marketing"),("web design company","Web Design"),("aeo agency","AEO"),("geo agency","GEO"),("lead generation company","Lead Generation")]
    for h,line in heads:
        for m in ("best","top","top rated","affordable","professional","local"):
            if m=="local" and "local" in h: continue
            add(f"{m} {h} in {C}","Secondary",G,line,"P2")
        add(f"hire {art(h) if not h.endswith('services') else h} in {C}","Secondary",G,line,"P2")
        add(f"{h} near {C}","Secondary",G,line,"P3")
    for t,line in [("seo pricing","SEO"),("seo packages","SEO"),("seo cost","SEO"),("monthly seo services","SEO"),("seo for small business","Small Business SEO"),
                   ("seo for local business","Local SEO"),("first page google ranking services","SEO"),("google maps ranking service","Local SEO"),
                   ("organic lead generation","Lead Generation"),("website and seo services","Web Design"),("seo and web design company","Web Design"),
                   ("full service digital marketing agency","Digital Marketing"),("ai search visibility services","AI SEO"),("ai overview ranking service","AIO"),
                   ("get found on chatgpt service","ChatGPT & LLM"),("b2b seo agency","SEO"),("national seo company","SEO"),("enterprise seo agency","SEO"),
                   ("seo company for startups","SEO"),("bilingual seo services","SEO"),("spanish seo services","SEO"),("seo content writing services","Content Marketing"),
                   ("press release distribution services","Link Building"),("digital pr agency","Link Building"),("online reputation management company","Reputation Management")]:
        add(f"{t} {C}","Secondary",G,line,"P2")
    # ---- Questions core
    for q,line in [
        (f"how much does seo cost in {C}","SEO"),(f"who is the best seo company in {C}","SEO"),(f"how do i choose an seo company in {C}","SEO"),
        (f"how long does seo take to work in {C}","SEO"),(f"is seo worth it for a small business in {C}","Small Business SEO"),
        (f"how do i get my business on the first page of google in {C}","SEO"),(f"how do i rank higher on google maps in {C}","Local SEO"),
        (f"how do i get more leads from my website in {C}","Lead Generation"),(f"why is my business not showing up on google in {C}","Local SEO"),
        (f"how much does a website cost in {C}","Web Design"),(f"how much does digital marketing cost in {C}","Digital Marketing"),
        (f"what does an seo company in {C} actually do","SEO"),(f"how do i find a trustworthy seo agency in {C}","SEO"),
        (f"do i need a local seo company in {C}","Local SEO"),(f"how many seo companies are there in {C}","SEO"),
        (f"what should i ask an seo agency in {C} before hiring","SEO"),(f"how do i get more google reviews for my {C} business","Reputation Management"),
        (f"how do i get my {C} business recommended by chatgpt","ChatGPT & LLM"),(f"how do i show up in google ai overviews in {C}","AIO"),
        (f"why are my competitors in {C} ranking above me","SEO"),(f"how do i stop paying for shared leads in {C}","Lead Generation"),
        (f"can i do seo myself or should i hire an agency in {C}","SEO"),(f"what is the average seo retainer in {C}","SEO"),
        (f"how do i know if my {C} seo company is working","SEO"),(f"how do i switch seo companies in {C}","SEO")]:
        add(q,"Question",G,line,"P2")
    # ---- AEO core
    for q,line in [
        (f"what is answer engine optimization for {C} businesses","AEO"),(f"what is the best seo company in {C}","SEO"),
        (f"what is local seo for {C} businesses","Local SEO"),(f"what is the cost of seo services in {C}","SEO"),
        (f"what is the fastest way to rank on google in {C}","SEO"),(f"what is the best digital marketing agency in {C}","Digital Marketing"),
        (f"which seo agency in {C} has the best reviews","SEO"),(f"which {C} agency does ai search optimization","AI SEO"),
        (f"what is generative engine optimization for {C} companies","GEO"),(f"what is ai seo and do {C} businesses need it","AI SEO"),
        (f"is seo dead for {C} businesses","AI SEO"),(f"what is the difference between seo and aeo for {C} businesses","AEO"),
        (f"how does voice search find local businesses in {C}","Voice Search"),(f"what makes a business show up first on google in {C}","Local SEO"),
        (f"where can i find an seo expert in {C}","SEO"),(f"when should a {C} business hire an seo agency","SEO")]:
        add(q,"AEO",G,line,"P2")
    # ---- AIO core
    for q,line in [
        (f"best seo companies in {C}","SEO"),(f"top seo agencies in {C}","SEO"),(f"best digital marketing agencies in {C}","Digital Marketing"),
        (f"best ai seo agencies in {C}","AI SEO"),(f"best aeo agencies in {C}","AEO"),(f"best geo agencies in {C}","GEO"),
        (f"best local seo companies in {C}","Local SEO"),(f"best web design companies in {C}","Web Design"),(f"top lead generation companies in {C}","Lead Generation"),
        (f"ai overview optimization {C}","AIO"),(f"how to rank in google ai overviews {C}","AIO"),(f"google ai mode optimization {C}","AIO"),
        (f"how to get cited in google ai overviews {C}","AIO"),(f"ai overviews seo agency {C}","AIO"),(f"list of seo companies in {C}","SEO"),
        (f"seo companies in {C} ranked","SEO")]:
        add(q,"AIO",G,line,"P2")
    # ---- GEO & AI SEO core
    for q,line in [
        (f"how to get recommended by chatgpt {C}","ChatGPT & LLM"),(f"how to rank in chatgpt {C}","ChatGPT & LLM"),(f"chatgpt ranking agency {C}","ChatGPT & LLM"),
        (f"how to show up in perplexity {C}","ChatGPT & LLM"),(f"how to show up in gemini {C}","ChatGPT & LLM"),(f"ai search ranking services {C}","AI SEO"),
        (f"ai visibility audit {C}","AI SEO"),(f"ai search audit {C}","AI SEO"),(f"llm visibility agency {C}","ChatGPT & LLM"),
        (f"generative ai seo services {C}","GEO"),(f"ai citation building {C}","GEO"),(f"brand mentions in ai answers {C}","GEO"),
        (f"ai search optimization for local businesses {C}","AI SEO"),(f"ai seo for small business {C}","AI SEO"),(f"geo and aeo services {C}","GEO"),
        (f"seo aeo geo agency {C}","AI SEO"),(f"ai first seo agency {C}","AI SEO"),(f"zero click search optimization {C}","AEO")]:
        add(q,"GEO & AI SEO",G,line,"P1" if "chatgpt" in q or "ai search" in q else "P2")
    # ---- EEAT core
    for q,line in [
        (f"seo company {C} reviews","SEO"),(f"seo agency {C} reviews","SEO"),(f"seo company {C} case studies","SEO"),(f"seo results {C}","SEO"),
        (f"trusted seo company {C}","SEO"),(f"experienced seo company {C}","SEO"),(f"reputable seo agency {C}","SEO"),(f"proven seo company {C}","SEO"),
        (f"seo company {C} testimonials","SEO"),(f"established seo agency {C}","SEO"),(f"seo company with guaranteed results {C}","SEO"),
        (f"transparent seo reporting {C}","SEO"),(f"white hat seo company {C}","SEO"),(f"digital marketing agency {C} reviews","Digital Marketing"),
        (f"ai seo agency {C} reviews","AI SEO"),(f"web design company {C} reviews","Web Design"),(f"seo company {C} portfolio","SEO"),
        (f"long term seo partner {C}","SEO")]:
        add(q,"E-E-A-T",G,line,"P2")
    # ---- Comparison core
    for q,line in [
        (f"seo vs google ads {C}","SEO"),(f"seo vs ppc for {C} businesses","SEO"),(f"seo agency vs freelancer {C}","SEO"),(f"seo agency vs in house {C}","SEO"),
        (f"seo vs aeo vs geo {C}","AI SEO"),(f"local seo vs national seo {C}","Local SEO"),(f"seo vs social media marketing {C}","SEO"),
        (f"seo company vs marketing agency {C}","Digital Marketing"),(f"seo vs paid leads {C}","Lead Generation"),(f"angi vs seo for {C} contractors","Lead Generation"),
        (f"thumbtack vs seo {C}","Lead Generation"),(f"ai seo vs traditional seo {C}","AI SEO"),(f"cheap seo vs professional seo {C}","SEO"),
        (f"monthly seo vs one time seo {C}","SEO")]:
        add(q,"Comparison",G,line,"P3")
    # ---- AI prompts core
    for q,line in [
        (f"Who are the best SEO companies in {city} for a local business?","SEO"),
        (f"Recommend an agency in {city} that can get my business mentioned in ChatGPT and Google AI answers.","AI SEO"),
        (f"I own a small business in {city} and my website gets no leads. Who should I hire?","Lead Generation"),
        (f"Compare the top digital marketing agencies in {city} for small businesses.","Digital Marketing"),
        (f"Which {city} SEO agency works on a site every day instead of once a month?","SEO"),
        (f"What should I expect to get from an SEO agency in {city} in the first 90 days?","SEO"),
        (f"Find me an AI search optimization company serving {city}.","AI SEO"),
        (f"Which agencies in {city} do answer engine optimization and generative engine optimization?","AEO"),
        (f"My competitors in {city} show up in Google AI Overviews and I don't. Who can fix that?","AIO"),
        (f"Who builds websites in {city} that actually rank and bring in calls?","Web Design"),
        (f"I'm tired of paying for shared leads in {city}. What's a better way to get customers?","Lead Generation"),
        (f"Which {city} marketing agency is best for getting on page one of Google?","SEO")]:
        add(q,"AI Prompt",G,line,"P2",lower=False)

    # ================= INDUSTRY =================
    for name,adj,adj2,pl,sg,cust,tier in IND:
        p1 = "P1" if tier=="A" else ("P2" if tier=="B" else "P3")
        p2 = "P2" if tier=="A" else "P3"
        for a in [adj]:
            for t in ("seo company","seo agency","seo services","seo expert"): add(f"{a} {t} {C}","Primary - Industry",name,"SEO",p1)
            add(f"{C} {a} seo","Primary - Industry",name,"SEO",p1); add(f"{a} seo {C}","Primary - Industry",name,"SEO",p1)
            add(f"seo for {pl} {C}","Primary - Industry",name,"SEO",p1); add(f"local seo for {pl} {C}","Primary - Industry",name,"SEO",p1)
            for t in ("marketing company","marketing agency","digital marketing agency","internet marketing"): add(f"{a} {t} {C}","Primary - Industry",name,"Marketing",p1)
            add(f"{C} {a} marketing","Primary - Industry",name,"Marketing",p1); add(f"marketing for {pl} {C}","Primary - Industry",name,"Marketing",p1)
            add(f"{a} lead generation {C}","Primary - Industry",name,"Marketing",p1)
            for t in ("web design company","web company","website design"): add(f"{a} {t} {C}","Primary - Industry",name,"Web Design",p1)
            add(f"websites for {pl} {C}","Primary - Industry",name,"Web Design",p1)
            for t in ("ai seo company","aio company","aeo company","geo company","ai search optimization"): add(f"{a} {t} {C}","Primary - Industry",name,"AI Search",p1)
        for a in adj2:
            for t in ("seo","seo company","seo services"): add(f"{a} {t} {C}","Primary - Industry",name,"SEO",p1)
            add(f"{a} marketing agency {C}","Primary - Industry",name,"Marketing",p1); add(f"{a} web design {C}","Primary - Industry",name,"Web Design",p1)
        # secondary
        add(f"best {adj} seo company in {C}","Secondary",name,"SEO",p2); add(f"top {adj} seo agency in {C}","Secondary",name,"SEO",p2)
        add(f"affordable {adj} seo services {C}","Secondary",name,"SEO",p2); add(f"{adj} seo consultant {C}","Secondary",name,"SEO",p2)
        add(f"best {adj} marketing agency in {C}","Secondary",name,"Marketing",p2); add(f"{adj} seo pricing {C}","Secondary",name,"SEO",p2)
        add(f"best website designer for {pl} in {C}","Secondary",name,"Web Design",p2)
        # questions
        add(f"how do {pl} get more {cust} in {C}","Question",name,"Marketing",p2)
        add(f"how much does {adj} seo cost in {C}","Question",name,"SEO",p2)
        add(f"how can {art(sg)} in {C} rank higher on google","Question",name,"SEO",p2)
        add(f"who is the best {adj} seo company in {C}","Question",name,"SEO",p2)
        add(f"how long does seo take for {pl} in {C}","Question",name,"SEO",p2)
        add(f"why is my {sg} not showing up on google maps in {C}","Question",name,"SEO",p2)
        # aeo
        add(f"is seo worth it for {pl} in {C}","AEO",name,"SEO",p2)
        add(f"what is the best way to market {art(sg)} in {C}","AEO",name,"Marketing",p2)
        add(f"what does {art(adj+' seo company')} do for {pl} in {C}","AEO",name,"SEO",p2)
        add(f"what do people search for when looking for {pl} in {C}","AEO",name,"SEO",p2)
        # aio
        add(f"best {adj} marketing agencies in {C}","AIO",name,"Marketing",p2)
        add(f"best {adj} seo companies in {C}","AIO",name,"SEO",p2)
        add(f"how to get {art(sg)} into google ai overviews in {C}","AIO",name,"AI Search",p2)
        add(f"ai overview optimization for {pl} {C}","AIO",name,"AI Search",p2)
        # geo
        add(f"how to get {art(sg)} recommended by chatgpt in {C}","GEO & AI SEO",name,"AI Search",p2)
        add(f"ai seo for {pl} {C}","GEO & AI SEO",name,"AI Search",p1)
        add(f"generative engine optimization for {pl} {C}","GEO & AI SEO",name,"AI Search",p2)
        add(f"answer engine optimization for {pl} {C}","GEO & AI SEO",name,"AI Search",p2)
        add(f"chatgpt seo for {pl} {C}","GEO & AI SEO",name,"AI Search",p2)
        # eeat
        add(f"{adj} seo company {C} reviews","E-E-A-T",name,"SEO",p2)
        add(f"{adj} seo case studies {C}","E-E-A-T",name,"SEO",p2)
        add(f"experienced {adj} seo experts {C}","E-E-A-T",name,"SEO",p2)
        add(f"{adj} marketing agency {C} results","E-E-A-T",name,"Marketing",p2)
        # comparison
        add(f"seo vs google ads for {pl} in {C}","Comparison",name,"SEO","P3")
        add(f"{adj} seo agency vs in house marketing {C}","Comparison",name,"SEO","P3")
        add(f"seo vs paid leads for {pl} in {C}","Comparison",name,"Marketing","P3")
        # prompts
        add(f"Recommend the best marketing agency in {city} for {art(sg)} that wants more {cust}.","AI Prompt",name,"Marketing",p2,lower=False)
        add(f"Which {city} agency can get my {sg} recommended in ChatGPT and Google AI answers?","AI Prompt",name,"AI Search",p2,lower=False)
        add(f"I run {art(sg)} in {city}. Who should I hire to get found on Google?","AI Prompt",name,"SEO",p2,lower=False)
    return rows, add


NOTE.update({
"Primary - Specialty":"Money term for a sub-specialty or a city-signature industry. Narrower buyer, less competition, same service.",
"Leads & Outcomes":"How owners actually talk: they search for leads, patients, cases and growth, not for the name of the service. Highest lead intent in the sheet.",
"Alternative":"Buyer is unhappy with a lead platform or another agency and is looking for a replacement.",
"Switcher":"Buyer already has a provider or a problem (lost rankings, no leads) and is ready to change. Short sales cycle.",
"Local Area":"Suburb / borough / metro-area version of the money terms. Lower competition than the city head term, same buyer.",
})
INTENT.update({"Primary - Specialty":"Transactional","Leads & Outcomes":"Transactional (problem-led)","Alternative":"Commercial - switching","Switcher":"Transactional - switching","Local Area":"Transactional"})
LIVES={"Primary - Core":"City service page","Primary - Industry":"Category x city page","Primary - Specialty":"Specialty section on its category x city page; own page once it shows impressions",
"Secondary":"Same page as its primary (heading / section)","Question":"Question page, linked up to its locked page","AEO":"Answer block on the locked page + question page",
"AIO":"List-style article with dated sources","GEO & AI SEO":"AI-answer page","E-E-A-T":"Proof page (results, method, reviews, team)","Comparison":"Comparison article",
"AI Prompt":"Tracked prompt in the AI mention log","Leads & Outcomes":"Opening section of the category x city page + supporting article","Alternative":"Comparison page",
"Switcher":"Second-opinion page for the city","Local Area":"Area page under the city"}

AREAS={"New York":["Manhattan","Brooklyn","Queens","Bronx","Staten Island","Long Island","Jersey City","Westchester"],
"Los Angeles":["Santa Monica","Pasadena","Beverly Hills","Burbank","Torrance","Orange County","Irvine","Anaheim"],
"Chicago":["Naperville","Schaumburg","Evanston","Oak Brook","Joliet","Arlington Heights","Oak Park","Elgin"],
"Houston":["Katy","Sugar Land","The Woodlands","Pearland","Cypress TX","Spring TX","League City","Conroe"],
"Dallas":["Plano","Frisco","Fort Worth","Irving","Arlington TX","McKinney","Richardson","Garland"],
"Miami":["Fort Lauderdale","Coral Gables","Doral","Miami Beach","Hialeah","Boca Raton","Kendall","West Palm Beach"],
"Atlanta":["Marietta","Alpharetta","Sandy Springs","Roswell GA","Decatur GA","Buckhead","Duluth GA","Kennesaw"],
"Phoenix":["Scottsdale","Mesa","Tempe","Chandler","Gilbert","Glendale AZ","Surprise AZ","Peoria AZ"],
"Denver":["Lakewood CO","Boulder","Littleton","Englewood CO","Centennial","Arvada","Westminster CO","Highlands Ranch"],
"Fresno":["Clovis","Visalia","Madera","Hanford","Tulare","Merced","Sanger","Selma CA"]}
STATES={"NY":"New York State","CA":"California","IL":"Illinois","TX":"Texas","FL":"Florida","GA":"Georgia","AZ":"Arizona","CO":"Colorado"}
SIGN={"New York":["fintech","financial services","luxury real estate","fashion brand","startup"],
"Los Angeles":["entertainment","cosmetic surgery","luxury real estate","fashion brand","startup"],
"Chicago":["logistics","commercial real estate","staffing agency","food manufacturing"],
"Houston":["oil and gas","energy company","industrial services","commercial construction"],
"Dallas":["commercial real estate","oil and gas","franchise","it services"],
"Miami":["luxury real estate","yacht charter","hospitality","cosmetic surgery","import export"],
"Atlanta":["logistics","film production","franchise","fintech"],
"Phoenix":["solar installer","senior living","golf course","pool service"],
"Denver":["outdoor brand","cannabis dispensary","tourism","craft brewery"],
"Fresno":["agriculture","farm equipment","trucking","irrigation"]}
SPEC=[("Dental","dental implant"),("Dental","cosmetic dentist"),("Dental","pediatric dentist"),("Dental","invisalign"),("Dental","emergency dentist"),
("Law Firm","divorce lawyer"),("Law Firm","dui lawyer"),("Law Firm","estate planning lawyer"),("Law Firm","bankruptcy lawyer"),("Law Firm","workers comp lawyer"),("Law Firm","car accident lawyer"),("Law Firm","employment lawyer"),("Law Firm","real estate lawyer"),
("Medical Practice","urgent care"),("Medical Practice","physical therapy"),("Medical Practice","optometrist"),("Medical Practice","fertility clinic"),("Medical Practice","podiatrist"),("Medical Practice","pediatrician"),("Medical Practice","dental lab"),
("Home Services","water damage restoration"),("Home Services","kitchen remodeling"),("Home Services","bathroom remodeling"),("Home Services","fence company"),("Home Services","concrete contractor"),("Home Services","window replacement"),
("Home Services","junk removal"),("Home Services","appliance repair"),("Home Services","locksmith"),("Home Services","towing company"),("Home Services","carpet cleaning"),("Home Services","handyman"),("Home Services","foundation repair"),("Home Services","septic service"),
("Real Estate","property management"),("Real Estate","commercial real estate broker"),("Real Estate","home builder"),("Real Estate","real estate investor"),
("Financial Advisors","wealth management"),("Accounting","tax preparation"),("Accounting","bookkeeping"),
("Small Business","daycare"),("Small Business","private school"),("Small Business","wedding venue"),("Small Business","funeral home"),("Small Business","self storage"),("Small Business","dog boarding"),
("Small Business","hair salon"),("Small Business","auto detailing"),("Small Business","body shop"),("Small Business","photographer"),("Small Business","jewelry store"),("Small Business","furniture store"),("Small Business","sign and printing company"),
("B2B & SaaS","it services"),("B2B & SaaS","managed service provider"),("B2B & SaaS","cybersecurity company"),("B2B & SaaS","staffing agency"),("B2B & SaaS","architecture firm"),("B2B & SaaS","engineering firm"),("B2B & SaaS","trucking company"),("B2B & SaaS","consulting firm")]
HOME={"Plumbing","HVAC","Roofing","Electrical","Home Services","General Contractor","Home Remodeling","Painting","Landscaping","Pest Control","Cleaning Services","Moving","Garage Door","Flooring","Pool Builders","Tree Service","Solar"}
LEGAL={"Law Firm","Personal Injury Law","Family Law","Criminal Defense Law","Immigration Law"}
MED={"Dental","Orthodontics","Medical Practice","Chiropractic","Dermatology","Plastic Surgery","Med Spa"}
def plats(n):
    if n in HOME: return ["angi leads","homeadvisor","thumbtack","yelp ads"]
    if n in LEGAL: return ["findlaw","avvo","scorpion","justia"]
    if n in MED: return ["zocdoc","healthgrades","yelp ads"]
    if n=="Therapy & Counseling": return ["psychology today","zocdoc"]
    if n=="Real Estate": return ["zillow leads","realtor.com leads"]
    if n=="Restaurants": return ["doordash","yelp ads"]
    if n=="Hotels": return ["booking.com","expedia"]
    return ["yelp ads","google ads"]
G="Agency (all industries)"
TIERA=[i for i in IND if i[6]=="A"]

def gen2(city,st,aliases):
    rows,add=gen(city,aliases); C=city.lower()
    # platform + hire-step (primary core)
    for t in ("wordpress seo company","wordpress seo expert","wix seo expert","squarespace seo expert","webflow seo agency","woocommerce seo agency","shopify seo expert","bigcommerce seo agency","godaddy website seo help"):
        add(f"{t} {C}","Primary - Core",G,"Platform SEO","P2")
    for t in ("seo consultation","seo quote","seo proposal","seo audit company","website audit","ai visibility check","google business profile audit"):
        add(f"{t} {C}","Primary - Core",G,"SEO","P2")
    # switcher
    for t in ("seo company not getting results","switch seo company","second opinion seo audit","seo not working","replace my seo agency","better seo company","unhappy with seo company",
              "website not getting leads","website traffic dropped","lost google rankings","google ranking drop recovery","website not showing on google","google business profile suspended help",
              "traffic dropped after ai overviews","leads dropped after google update","competitor outranking me on google"):
        add(f"{t} {C}","Switcher",G,"SEO","P1")
    # agency alternatives
    for t in ("thrive agency","webfx","scorpion marketing","hibu","smartsites","ignite visibility","yelp advertising","lead generation websites","pay per lead services","google ads"):
        add(f"{t} alternative {C}","Alternative",G,"Digital Marketing","P2")
    # industry: leads & outcomes + alternatives
    for name,adj,adj2,pl,sg,cust,tier in IND:
        p="P1" if tier=="A" else ("P2" if tier=="B" else "P3")
        for k in (f"{adj} leads {C}",f"exclusive {adj} leads {C}",f"get more {cust} for my {sg} in {C}",f"how to grow {art(sg)} in {C}",f"{adj} advertising agency {C}",
                  f"{adj} lead generation company {C}",f"{adj} marketing consultant {C}",f"{adj} marketing services {C}",f"{adj} online marketing {C}",f"{sg} not getting enough {cust} in {C}"):
            add(k,"Leads & Outcomes",name,"Marketing",p)
        ps=plats(name)
        for pt in ps: add(f"{pt} alternative for {pl} {C}","Alternative",name,"Marketing","P2" if tier=="A" else "P3")
        add(f"{ps[0]} vs seo for {pl} {C}","Alternative",name,"Marketing","P2" if tier=="A" else "P3")
    # specialties + city signature
    for parent,sp in SPEC:
        for k in (f"{sp} seo {C}",f"{sp} seo company {C}",f"{sp} marketing agency {C}",f"{sp} marketing {C}",f"{sp} leads {C}"): add(k,"Primary - Specialty",parent,sp.title(),"P2")
    for sp in SIGN[city]:
        for k in (f"{sp} seo {C}",f"{sp} seo company {C}",f"{sp} marketing agency {C}",f"{sp} marketing {C}",f"{sp} web design {C}",f"ai seo for {sp} companies {C}"): add(k,"Primary - Specialty","City signature",sp.title(),"P1")
    # local areas
    for a in AREAS[city]:
        A=a.lower()
        for k in (f"seo company {A}",f"{A} seo company",f"seo agency {A}",f"seo services {A}",f"local seo {A}",f"digital marketing agency {A}",f"web design company {A}",f"ai seo agency {A}",f"marketing agency {A}",f"best seo company in {A}"):
            add(k,"Local Area",G,f"Area: {a}","P2")
        for name,adj,adj2,pl,sg,cust,tier in TIERA:
            add(f"{adj} seo {A}","Local Area",name,f"Area: {a}","P3"); add(f"{adj} marketing {A}","Local Area",name,f"Area: {a}","P3")
    return rows, add

NAVY="1B2A4A"; GOLD="BD8E47"
hf=Font(name="Arial",bold=True,color="FFFFFF",size=10); hfill=PatternFill("solid",fgColor=NAVY); bf=Font(name="Arial",size=10)
def header(ws,cols,widths):
    ws.append(cols)
    for i,w in enumerate(widths,1):
        c=ws.cell(row=1,column=i); c.font=hf; c.fill=hfill; c.alignment=Alignment(vertical="center",wrap_text=True)
        ws.column_dimensions[get_column_letter(i)].width=w
    ws.freeze_panes="A2"; ws.sheet_properties.tabColor=GOLD
COLS=["#","Keyword","Section","Buyer Category","Service Line","Intent","Priority","Keyword Group (one page per group)","Where it lives","Why it is here / how it is used"]; W=[6,60,18,22,22,24,9,44,44,70]
def dump(ws,rows):
    header(ws,COLS,W)
    for i,r in enumerate(rows,1): ws.append([i]+r[:7]+[LIVES[r[1]],r[7]])
    ws.auto_filter.ref=f"A1:J{len(rows)+1}"


import re
NOTE.update({"Owner Research":"Owner researching how to do it themselves (ideas, strategies, plan). Real, frequent searches. Won with a practical guide that ends in an offer.",
"Spanish":"Spanish-language buyer searches. Confirmed live for Miami; applied to every city with a large Spanish-speaking business base."})
INTENT.update({"Owner Research":"Informational > Commercial","Spanish":"Transactional"})
LIVES.update({"Owner Research":"Practical guide article per category, linked to its category x city page","Spanish":"Spanish city page (/es/)"})
EXTRA={"Dental":["dentist"],"Law Firm":["attorney","lawyer"],"Personal Injury Law":["personal injury attorney","personal injury"],"Family Law":["family lawyer"],"Criminal Defense Law":["criminal defense lawyer","criminal defense attorney"],
"Immigration Law":["immigration attorney"],"Plumbing":["plumber"],"Roofing":["roofing contractor"],"HVAC":["hvac contractor"],"Electrical":["electrical contractor"],"General Contractor":["general contractor","construction company"],
"Home Remodeling":["home remodeling"],"Painting":["painting company","painter"],"Landscaping":["lawn care"],"Cleaning Services":["cleaning service","cleaning business","commercial cleaning"],"Tree Service":["tree removal"],
"Pool Builders":["pool service","pool contractor"],"Flooring":["flooring contractor","flooring company"],"Garage Door":["garage door repair"],"Financial Advisors":["financial planner"],"Insurance":["insurance agent","life insurance"],
"Accounting":["accountant","accounting firm"],"Medical Practice":["doctor"],"Plastic Surgery":["plastic surgeon","cosmetic surgery"],"Chiropractic":["chiropractor"],"Veterinary":["vet","veterinarian"],"Home Care":["senior care","home health"],
"Auto Repair":["auto shop","auto body"],"Car Dealerships":["car dealer","auto dealership"],"Limo & Transportation":["limousine"],"Security Companies":["security guard company","alarm company"],"Real Estate":["realtor","real estate agent"],
"Therapy & Counseling":["therapy","counselor"],"B2B & SaaS":["saas","startup"],"Small Business":["nonprofit","interior designer"]}
ST={c:s for c,s,_ in LAUNCH}
def gen3(city,st,al):
    rows,add=gen2(city,st,al); C=city.lower(); S=st.lower()
    # core: state-suffix forms + live-confirmed head forms
    for t,line in (("seo company","SEO"),("seo services","SEO"),("seo agency","SEO"),("seo","SEO"),("digital marketing agency","Digital Marketing"),("web design","Web Design"),("local seo","Local SEO")):
        add(f"{t} {C} {S}","Primary - Core",G,line,"P1")
    for t,line in (("best seo company","SEO"),("top seo company","SEO"),("affordable seo company","SEO"),("best local seo company","Local SEO"),("top rated seo","SEO"),("affordable seo","SEO"),("seo agencies","SEO"),("seo companies","SEO"),
                   ("seo consultants","SEO"),("hire seo expert","SEO"),("hire seo specialist","SEO"),("hire seo consultant","SEO"),("hire seo freelancer","SEO"),("seo cost per month","SEO"),("seo pricing packages","SEO"),
                   ("seo services for small business","Small Business SEO"),("local seo services for small business","Local SEO"),("local seo for contractors","Local SEO"),("local seo lead generation","Local SEO"),
                   ("website design seo company","Web Design"),("seo for chatgpt","ChatGPT & LLM"),("seo for ai search","AI SEO"),("seo for llms","ChatGPT & LLM"),("ai seo optimization","AI SEO"),("ai search optimization company","AI SEO")):
        add(f"{t} {C}","Primary - Core" if t.startswith(("hire","seo ","local","website","ai")) else "Secondary",G,line,"P1")
    for q in ("why is my business not showing up on google maps","why is my business not showing up on google","why is my website not showing up on google","why is my website not ranking on google","why is my website not converting",
              "how to rank higher on google maps","how to rank higher on google business profile","how to get into the google map pack"):
        add(f"{q} {C}","Switcher",G,"Local SEO","P1")
    for q in ("how to get my business found on chatgpt","how to get my business to show up on chatgpt","how to get my business recommended on chatgpt","how to get my business listed on chatgpt","how to get my business cited by chatgpt",
              "how to rank my business in chatgpt","how to rank higher in chatgpt search results","how to show up in google ai overviews","how to show up in ai results","how to appear in ai overview"):
        add(f"{q} {C}","GEO & AI SEO",G,"ChatGPT & LLM","P1")
    for q,line in (("seo vs geo","AI SEO"),("seo vs aeo","AEO"),("aeo vs geo","AEO"),("seo vs aio","AIO"),("seo vs sem","SEO"),("seo vs paid search","SEO"),("seo vs ai optimization","AI SEO"),("generative engine optimization vs seo","GEO")):
        add(f"{q} {C}","Comparison",G,line,"P2")
    for t,line in (("agencia seo","SEO"),("consultor seo","SEO"),("agencia de marketing digital","Digital Marketing"),("posicionamiento web","SEO"),("diseno web","Web Design"),("seo en espanol","SEO"),("empresa de seo","SEO"),("marketing digital para negocios","Digital Marketing"),("experto seo","SEO"),("seo local","Local SEO")):
        add(f"{t} {C}","Spanish",G,line,"P1" if city in ("Miami","Los Angeles","Houston") else "P2")
    for name,adj,adj2,pl,sg,cust,tier in IND:
        p="P1" if tier=="A" else ("P2" if tier=="B" else "P3")
        for k in (f"marketing agency for {pl} {C}",f"lead generation for {pl} {C}",f"digital marketing agency for {pl} {C}",f"website design for {pl} {C}",f"{adj} marketing companies {C}",f"{adj} local seo {C}",f"{adj} seo services company {C}"):
            add(k,"Primary - Industry",name,"Marketing" if "seo" not in k else "SEO",p)
        for k in (f"{adj} leads for sale {C}",f"buy {adj} leads {C}",f"free {adj} leads {C}",f"pay per lead {adj} leads {C}",f"get {adj} leads {C}",f"best {adj} leads {C}",f"{adj} lead generation companies {C}",
                  f"how to get {adj} leads in {C}",f"how to get more leads for my {sg} in {C}",f"how to get more customers for my {sg} in {C}"):
            add(k,"Leads & Outcomes",name,"Marketing",p)
        for k in (f"{adj} marketing ideas {C}",f"{adj} marketing strategies {C}",f"{adj} marketing plan {C}",f"{adj} seo keywords {C}",f"{adj} advertising ideas {C}"):
            add(k,"Owner Research",name,"Marketing","P2" if tier=="A" else "P3")
        add(f"{adj} seo case study {C}","E-E-A-T",name,"SEO","P2")
        for a in EXTRA.get(name,[]):
            for k in (f"{a} seo {C}",f"{a} seo company {C}",f"{a} seo services {C}",f"{a} marketing {C}",f"{a} marketing agency {C}",f"{a} leads {C}",f"{a} lead generation {C}"):
                add(k,"Primary - Industry" if "leads" not in k and "lead gen" not in k else "Leads & Outcomes",name,"SEO" if "seo" in k else "Marketing",p)
    return rows, add

# ---- live data
live={}; liveseed={}
for l in open("source/google-suggestions-2026-11-18.txt"):
    s,r=l.strip().split("|")
    for x in r.split(" / "):
        k=(x[1:] if x.startswith("~") else (s+" "+x)).strip().lower()
        k=re.sub(r"\s+"," ",k)
        live[k]=s
CITYTOK=[c.lower() for c,_,_ in LAUNCH]+["nyc","new york city"]
def strip_city(k):
    for c in sorted(CITYTOK,key=len,reverse=True):
        k=re.sub(rf"\b(in )?{c}\b( (ny|ca|il|tx|fl|ga|az|co))?","",k)
    return re.sub(r"\s+"," ",k).strip()
def signal(k):
    k=k.lower()
    if k in live: return "Seen live in Google suggestions"
    if strip_city(k) in live: return "National form seen live"
    return ""

def catof(seed):
    for name,adj,adj2,pl,sg,cust,tier in IND:
        if seed.startswith(adj): return name
    return G
def secof(k):
    if any(w in k for w in ("leads","lead gen","customers for","more clients")): return "Leads & Outcomes"
    if any(w in k for w in ("ideas","strateg","plan","tips","guide","checklist","keywords")): return "Owner Research"
    if k.startswith(("why is","how to rank higher on google")): return "Switcher"
    if "chatgpt" in k or "ai overview" in k or "ai results" in k or "generative" in k or "answer engine" in k or k.startswith(("ai ","aeo","seo for ai","seo for chatgpt","seo for llm")): return "GEO & AI SEO"
    if " vs " in k: return "Comparison"
    if k.startswith(("best","top")) or "companies" in k or "agencies" in k: return "AIO"
    if "case study" in k or "reddit" in k: return "E-E-A-T"
    return "Primary - Industry" if catof(live[k])!=G else "Primary - Core"
COLS=["#","Keyword","Section","Buyer Category","Service Line","Intent","Priority","Keyword Group (one page per group)","Where it lives","Live demand signal","Why it is here / how it is used"]; W=[6,58,18,22,22,22,9,42,42,30,66]
def put(ws,rows,lives=None):
    header(ws,COLS,W); c=0
    for i,r in enumerate(rows,1):
        sg=signal(r[0]); c+= 1 if sg else 0
        ws.append([i]+r[:7]+[lives or LIVES[r[1]],sg,r[7]])
    ws.auto_filter.ref=f"A1:K{len(rows)+1}"; return c


BR="Broad (head terms)"
NOTE[BR]="Broad head term with the location in it. The widest net: any business owner in that place looking for a provider."
INTENT[BR]="Transactional"; LIVES[BR]="Main service page for that location"
BTERMS=[("seo company","SEO"),("seo agency","SEO"),("seo services","SEO"),("seo firm","SEO"),("seo expert","SEO"),("seo experts","SEO"),("seo consultant","SEO"),("seo specialist","SEO"),("seo marketing company","SEO"),
("search engine optimization company","SEO"),("search engine optimization services","SEO"),("local seo company","Local SEO"),("local seo services","Local SEO"),
("digital marketing agency","Digital Marketing"),("digital marketing company","Digital Marketing"),("digital marketing services","Digital Marketing"),("marketing agency","Digital Marketing"),("marketing company","Digital Marketing"),
("internet marketing company","Digital Marketing"),("internet marketing agency","Digital Marketing"),("online marketing agency","Digital Marketing"),("advertising agency","Digital Marketing"),("branding agency","Digital Marketing"),
("web design company","Web Design"),("web design agency","Web Design"),("web design services","Web Design"),("website design company","Web Design"),("website designers","Web Design"),("web designer","Web Design"),
("web development company","Web Design"),("website developer","Web Design"),("wordpress web design","Web Design"),("ecommerce web design","Web Design"),
("social media marketing agency","Social Media"),("social media agency","Social Media"),("lead generation company","Lead Generation"),("lead generation services","Lead Generation"),
("ai seo agency","AI SEO"),("ai seo company","AI SEO"),("ai seo services","AI SEO"),("ai search optimization","AI SEO"),("answer engine optimization","AEO"),("generative engine optimization","GEO"),
("google business profile optimization","Google Business Profile"),("content marketing agency","Content Marketing")]
def broad(L,full=True,suffix=None):
    out=[]
    for t,line in BTERMS:
        out+= [(f"{t} {L}",line),(f"{L} {t}",line),(f"{t} in {L}",line)]
        if full: out+=[(f"best {t} in {L}",line),(f"top {t} in {L}",line)]
        if suffix: out.append((f"{t} {L} {suffix}",line))
    return out
MORE={"New York":["Nassau County","Suffolk County","Harlem","White Plains","Yonkers","Hoboken"],"Los Angeles":["Los Angeles County","Glendale CA","Long Beach","Hollywood","Santa Clarita","Culver City"],
"Chicago":["Cook County","DuPage County","Aurora IL","Skokie","Wheaton","Orland Park"],"Houston":["Harris County","Fort Bend County","Pasadena TX","Humble TX","Missouri City","Baytown"],
"Dallas":["Dallas County","Collin County","Tarrant County","Denton","Carrollton","Allen TX","Grand Prairie"],"Miami":["Miami-Dade County","Broward County","Palm Beach County","Aventura","Pembroke Pines","Hollywood FL","Homestead"],
"Atlanta":["Fulton County","Cobb County","Gwinnett County","Lawrenceville","Smyrna GA","Dunwoody","Peachtree City"],"Phoenix":["Maricopa County","Goodyear","Avondale","Queen Creek","Fountain Hills","Paradise Valley"],
"Denver":["Jefferson County CO","Arapahoe County","Aurora CO","Thornton","Broomfield","Castle Rock","Parker CO"],"Fresno":["Fresno County","Tulare County","Kings County CA","Reedley","Kerman","Fowler","Porterville"]}
for c in MORE: AREAS[c]=AREAS[c]+MORE[c]
TB=[i for i in IND if i[6]=="B"]
def sig(k,toks):
    k=k.lower()
    if k in live: return "Seen live"
    for t in sorted(toks,key=len,reverse=True): k=re.sub(rf"\b(in |near )?{re.escape(t)}\b","",k)
    k=re.sub(r"\s+"," ",k).strip()
    return "National form seen live" if k in live else ""
def mk(k,sec,catg,line,pri,loc): return [k.lower(),sec,catg,line,INTENT[sec],pri,f"{loc} | {catg} | {line}",NOTE[sec]]

def gen4(city,st,al):
    rows,add=gen3(city,st,al); C=city.lower(); bset={}
    for k,line in broad(C,True,st.lower()): bset[k]=line
    for a_ in al:
        for k,line in broad(a_,False): bset[k]=line
    for r in rows:
        if r[0] in bset: r[1]=BR; r[4]=INTENT[BR]; r[7]=NOTE[BR]; r[5]="P1"
    have={r[0] for r in rows}
    for k,line in bset.items():
        if k not in have: add(k,BR,G,line,"P1")
    for a in AREAS[city]:
        A=a.lower()
        for t in ("web design","website design","marketing company","seo expert","seo consultant","digital marketing company","web design agency","lead generation company","social media marketing agency","ai seo company"):
            add(f"{t} {A}","Local Area",G,f"Area: {a}","P2")
        for name,adj,adj2,pl,sg,cust,tier in TIERA: add(f"{adj} leads {A}","Local Area",name,f"Area: {a}","P3"); add(f"{adj} marketing agency {A}","Local Area",name,f"Area: {a}","P3")
        for name,adj,adj2,pl,sg,cust,tier in TB: add(f"{adj} seo {A}","Local Area",name,f"Area: {a}","P3")
    return rows

def gen_lite(city,st):
    C=city.lower(); rows=[]; seen=set()
    def add(k,sec,catg,line,pri):
        k=k.lower()
        if k in seen: return
        seen.add(k); rows.append(mk(k,sec,catg,line,pri,city))
    for k,line in broad(C,False,st.lower()): add(k,BR,G,line,"P1")
    for name,adj,adj2,pl,sg,cust,tier in IND:
        p="P1" if tier=="A" else "P2"
        add(f"{adj} seo {C}","Primary - Industry",name,"SEO",p); add(f"{adj} marketing agency {C}","Primary - Industry",name,"Marketing",p); add(f"{adj} leads {C}","Leads & Outcomes",name,"Marketing",p)
        if tier=="A":
            for k in (f"{adj} seo company {C}",f"{adj} seo services {C}",f"{adj} marketing {C}",f"{adj} marketing company {C}",f"{adj} web design {C}",f"seo for {pl} {C}",f"marketing agency for {pl} {C}",f"lead generation for {pl} {C}",f"{C} {adj} seo"): add(k,"Primary - Industry",name,"SEO" if "seo" in k else "Marketing","P1")
            for k in (f"{adj} leads for sale {C}",f"exclusive {adj} leads {C}",f"{adj} lead generation {C}",f"how to get more leads for my {sg} in {C}"): add(k,"Leads & Outcomes",name,"Marketing","P1")
    for q in ("seo not working","lost google rankings","website not getting leads","why is my business not showing up on google maps","how to rank higher on google maps","second opinion seo audit","switch seo company"): add(f"{q} {C}","Switcher",G,"SEO","P1")
    for q in ("how to get my business recommended on chatgpt","how to get my business found on chatgpt","how to show up in google ai overviews","chatgpt seo agency","ai seo for small business"): add(f"{q} {C}","GEO & AI SEO",G,"AI SEO","P1")
    for t in ("agencia seo","agencia de marketing digital","diseno web"): add(f"{t} {C}","Spanish",G,"SEO","P2")
    return rows

US50=["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York State","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington State","West Virginia","Wisconsin","Wyoming"]
def gen_state(stn):
    S=stn.lower(); rows=[]; seen=set()
    def add(k,sec,catg,line,pri):
        k=k.lower()
        if k in seen: return
        seen.add(k); rows.append(mk(k,sec,catg,line,pri,stn))
    for t,line in BTERMS[:30]+BTERMS[35:41]:
        add(f"{t} {S}",BR,G,line,"P2"); add(f"{S} {t}",BR,G,line,"P2"); add(f"{t} in {S}",BR,G,line,"P2")
    for name,adj,adj2,pl,sg,cust,tier in IND:
        add(f"{adj} seo {S}","Primary - Industry",name,"SEO","P2"); add(f"{adj} marketing agency {S}","Primary - Industry",name,"Marketing","P2"); add(f"{adj} leads {S}","Leads & Outcomes",name,"Marketing","P2")
        if tier=="A": add(f"{adj} seo company {S}","Primary - Industry",name,"SEO","P2"); add(f"{adj} leads for sale {S}","Leads & Outcomes",name,"Marketing","P2")
    return rows
def gen_usa():
    rows=[]; seen=set()
    def add(k,sec,catg,line,pri):
        k=k.lower()
        if k in seen: return
        seen.add(k); rows.append(mk(k,sec,catg,line,pri,"USA"))
    for t,line in BTERMS:
        for f in (f"{t} usa",f"{t} in usa",f"{t} in the united states",f"best {t} in usa",f"top {t} in usa",f"usa {t}"): add(f,BR,G,line,"P1")
    for name,adj,adj2,pl,sg,cust,tier in IND:
        for a in [adj]+adj2+EXTRA.get(name,[]):
            for k in (f"{a} seo company usa",f"{a} seo services usa",f"{a} marketing agency usa",f"{a} marketing company usa",f"best {a} seo company in usa"): add(k,"Primary - Industry",name,"SEO" if "seo" in k else "Marketing","P1")
            add(f"{a} leads usa","Leads & Outcomes",name,"Marketing","P1"); add(f"{a} lead generation company usa","Leads & Outcomes",name,"Marketing","P1")
    return rows

C7=["Keyword","Location","Section","Buyer Category","Priority","Keyword Group (one page per group)","Live demand signal"]; W7=[60,22,20,24,9,44,24]
order={"P1":0,"P2":1,"P3":2}
def write(ws,rows,toks,locf):
    header(ws,C7,W7); c=0
    data=[(r,sig(r[0],toks)) for r in rows]
    data.sort(key=lambda x:(0 if x[0][1]==BR else 1, 0 if x[1] else 1, order[x[0][5]]))
    for r,sg in data:
        c+=1 if sg else 0; ws.append([r[0],locf(r),r[1],r[2],r[5],r[6],sg])
    ws.auto_filter.ref=f"A1:G{len(rows)+1}"; return c
ALL={}
def check(rows,where,prob):
    keep=[]
    for r in rows:
        k=r[0]
        if k in ALL: prob.append((k,where,ALL[k])); continue
        ALL[k]=where; keep.append(r)
    rows[:]=keep
def readme(ws,rowsR):
    ws.column_dimensions["A"].width=30; ws.column_dimensions["B"].width=125
    for a_,b_ in rowsR: ws.append([a_,b_])
    for row in ws.iter_rows():
        row[0].font=Font(name="Arial",bold=True,size=10,color=NAVY); row[1].font=bf; row[1].alignment=Alignment(wrap_text=True,vertical="top")
    ws["A1"].font=Font(name="Arial",bold=True,size=14,color=NAVY); ws["B1"].font=Font(name="Arial",bold=True,size=11,color=GOLD); ws.sheet_properties.tabColor=NAVY
SECALL=[BR,"Primary - Core","Primary - Industry","Primary - Specialty","Leads & Outcomes","Switcher","Alternative","Owner Research","Spanish","Local Area","Secondary","Question","AEO","AIO","GEO & AI SEO","E-E-A-T","Comparison","AI Prompt"]
def legend(wb):
    ws=wb.create_sheet("Section Guide"); header(ws,["Section","What it is","Where it lives on the site"],[24,100,60])
    for s_ in SECALL: ws.append([s_,NOTE[s_],LIVES[s_]])
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment=Alignment(wrap_text=True,vertical="top"); c.font=bf

prob=[]
# ---------- SHEET A: 10 cities full depth
wbA=Workbook(); rdA=wbA.active; rdA.title="READ ME"; sumA=wbA.create_sheet("Summary"); legend(wbA)
matrix=[]; totA=0; confA=0; nocity=0; broadn=0
for city,st,al in LAUNCH:
    rows=gen4(city,st,al)
    have={r[0] for r in rows}
    for k,sd in live.items():
        if (re.search(rf"\b{city.lower()}\b",k) or any(re.search(rf"\b{x}\b",k) for x in al)) and k not in have:
            sec=secof(k); rows.append(mk(k,sec,catof(sd),"Live query","P1",city)); have.add(k)
    toks=[city.lower()]+al+[x.lower() for x in AREAS[city]]+[st.lower()]
    for r in rows:
        if not any(t in r[0].lower() for t in toks[:-1]): nocity+=1
    check(rows,city,prob)
    ws=wbA.create_sheet(city); c=write(ws,rows,toks,lambda r:(r[3][6:] if r[3].startswith("Area: ") else city)); confA+=c
    cnt=collections.Counter(r[1] for r in rows); broadn+=cnt[BR]
    matrix.append([f"{city}, {st}"]+[cnt[s_] for s_ in SECALL]+[len(rows),c]); totA+=len(rows)
header(sumA,["City"]+SECALL+["Total","Live-confirmed"],[18]+[12]*len(SECALL)+[10,14])
for m in matrix: sumA.append(m)
sumA.append(["ALL 10 CITIES"]+[sum(m[i] for m in matrix) for i in range(1,len(SECALL)+3)])

# ---------- SHEET B
wbB=Workbook(); rdB=wbB.active; rdB.title="READ ME"; legend(wbB)
ld=wbB.create_sheet("Live Demand (Google)"); wh=wbB.create_sheet("Where Buyers Are")
lrows=[]; ltoks=[]
for c in WAVE2+WAVE3:
    city,st=[x.strip() for x in c.split(",")]; r=gen_lite(city,st); check(r,city,prob); lrows+=r; ltoks+=[city.lower(),st.lower()]
ws=wbB.create_sheet("40 More Cities"); confL=write(ws,lrows,ltoks,lambda r:r[6].split(" | ")[0])
srows=[]
for stn in US50: r=gen_state(stn); check(r,stn,prob); srows+=r
ws=wbB.create_sheet("50 States"); confS=write(ws,srows,[x.lower() for x in US50]+["new york","washington"],lambda r:r[6].split(" | ")[0])
urows=gen_usa(); check(urows,"USA",prob)
ws=wbB.create_sheet("USA"); confU=write(ws,urows,["usa","the united states"],lambda r:"USA")
header(ld,["#","Real query typed on Google (US)","Seed it came from","Buyer Category","Has a location in it"],[6,62,34,26,22])
PL=CITYTOK+["usa","near me","tx","fl","ga","az","new jersey","florida","california","texas","colorado","tampa","nashville","austin","charlotte","san antonio","boise","san diego","sarasota","long island","hoboken"]
lv=sorted(live.items(),key=lambda x:(catof(x[1]),x[1],x[0]))
for i,(k,sd) in enumerate(lv,1): ld.append([i,k,sd,catof(sd),"Yes" if any(re.search(rf"\b{p}\b",k) for p in PL) else "No - used as the pattern, location added"])
ld.auto_filter.ref=f"A1:E{len(lv)+1}"
cnt_reddit=sum(1 for k in live if k.endswith("reddit")); cnt_near=sum(1 for k in live if "near me" in k)
cnt_buy=sum(1 for k in live if any(w in k for w in ("for sale","buy ","pay per","exclusive","free")) and "lead" in k)
cnt_ideas=sum(1 for k in live if any(w in k for w in ("ideas","strateg","plan","tips")))
cnt_list=sum(1 for k in live if any(w in k for w in ("companies","agencies","best ","top ")))
cnt_gpt=sum(1 for k in live if "chatgpt" in k)

header(wh,["#","Where buyers are","What they do there","Evidence","RSM move"],[5,34,52,58,70])
WH=[("Google search - category terms","Type '[their trade] marketing agency / seo / leads', often with 'usa', a state or a city",f"{len(live):,} real suggestions collected across 197 seeds","National category hub + city version for every Tier A category; city tabs sorted with live-confirmed terms first"),
("Google search - buying leads",f"Look to buy leads: 'for sale', 'pay per lead', 'exclusive', 'free', 'buy'",f"{cnt_buy} live lead-buying queries","One 'own your leads' page per category: what bought leads cost, why shared leads lose, what RSM builds instead"),
("Google Maps / near me",f"Search '... near me' and ask why they are missing from Maps",f"{cnt_near} live 'near me' queries; 'why is my business not showing up on google maps' seen live","Closed to RSM as a listing without a real staffed US location. Reached instead through the 'not showing up on Maps' pages and city pages"),
("ChatGPT / Gemini / Perplexity","Ask how to get their business found, listed, recommended or cited",f"{cnt_gpt} live ChatGPT queries","AI-answer pages for each of these questions + the tracked prompts on every city tab"),
("Reddit","Ask peers which agency or lead source works",f"'reddit' attached to {cnt_reddit} seeds live (plumbing leads, hvac leads, law firm marketing, real estate leads and more)","Named-person answers in trade subreddits, written to help, no link dropping; mirror the same questions as pages"),
("'Best companies' lists and directories","Search '[trade] marketing companies', 'best ... companies', 'top ... agencies' and click a ranked list",f"{cnt_list} live list-style queries","Get RSM onto the lists that already rank (Clutch, UpCity, DesignRush and trade roundups - RSM judgement on which) and publish RSM's own category lists"),
("How-to research","Search ideas, strategies, plans, tips before hiring anyone",f"{cnt_ideas} live ideas / strategy / plan queries","Owner Research section: one practical guide per category, with video, ending in the offer"),
("Lead platforms they are leaving","Angi, HomeAdvisor, Thumbtack, Yelp, Zocdoc, FindLaw, Zillow","Lead-buying queries above; platform names are RSM judgement, not yet checked live","Alternative pages per platform per category"),
("Spanish-language search","Search in Spanish for an agency","'agencia seo miami' and 'consultor seo miami' seen live","Spanish section on every city tab; P1 in Miami, Los Angeles, Houston"),
("Apple Maps / Yelp","Ask why the business is missing there","'why is my business not showing up on apple maps' and '... on yelp' seen live","Covered inside the 'not showing up' pages"),
("LinkedIn","B2B owners look for leads there","'linkedin b2b leads' seen live","Thomas's profile as the publishing face for B2B, manufacturing and professional services categories"),
("YouTube, Facebook trade groups, industry associations","Watch how-tos, ask peers","Not measured in this pull - RSM judgement","Video versions of the Owner Research guides; presence in the largest trade groups")]
for i,r in enumerate(WH,1): wh.append([i]+list(r))

for i,r in enumerate(WH,1): wh.append([i]+list(r))
for row in wh.iter_rows(min_row=2):
    for c in row: c.alignment=Alignment(wrap_text=True,vertical="top"); c.font=bf
totB=len(lrows)+len(srows)+len(urows); GT=totA+totB
common=[("The rule","Every keyword in both sheets carries a location: a city, a suburb or county, a state, or USA. Checked by script on every row."),
("Broad head terms","'seo agency miami', 'seo company miami', 'web design company miami' and 42 more head terms, in every word order, for every location. They sit at the top of every tab."),
("Live demand signal","'Seen live' = the exact phrase is a Google suggestion (US, 18 Nov 2026). 'National form seen live' = the phrase without its location is. Blank = built from the pattern. No monthly volumes: Keyword Planner and Semrush were both unavailable."),
("Keyword Group","The no-cannibalization lock: one keyword = one group = one home on the site. See Section Guide for what each section is and where it lives."),
("Priority","P1 build first, P2 second, P3 long tail. Nothing dropped for low volume.")]
readme(rdA,[("RSM KEYWORD UNIVERSE v4 - SHEET 1 OF 2","10 launch cities at full depth"),("Total in this sheet",f"{totA:,} keywords; {confA:,} confirmed by live Google data; {broadn:,} broad head terms."),
("Whole universe",f"{GT:,} unique keywords across both sheets, zero duplicates. Sheet 2 holds 40 more cities, all 50 states, USA, the live Google data and the Where Buyers Are map."),
("Locations per city","The city itself, its state-suffix form, and 14-15 suburbs, boroughs and counties each.")]+common)
readme(rdB,[("RSM KEYWORD UNIVERSE v4 - SHEET 2 OF 2","40 more cities, 50 states, USA, live data"),("Total in this sheet",f"{totB:,} keywords: {len(lrows):,} across 40 more cities, {len(srows):,} across 50 states, {len(urows):,} USA. {confL+confS+confU:,} confirmed by live Google data."),
("Whole universe",f"{GT:,} unique keywords across both sheets, zero duplicates. Sheet 1 holds the 10 launch cities at full depth."),
("Depth","These 40 cities carry the broad head terms, every buyer category and the lead terms. They are promoted to full depth (about 7,000+ keywords each) on go-ahead.")]+common)
wbA.save("RSM_KU_v4_1_Launch_Cities.xlsx"); wbB.save("RSM_KU_v4_2_More_Locations.xlsx")
print("unique",len(ALL));print("A",totA,"conf",confA,"broad",broadn,"nocity",nocity,"| B",totB,len(lrows),len(srows),len(urows),"conf",confL,confS,confU,"| GT",GT,"dropped cross-tab dups",len(prob),prob[:5])
print(matrix[5])
