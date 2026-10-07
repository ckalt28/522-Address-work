# Keyword rules: (regex on lowercased listing, description, bucket). First match wins, so order matters.
import re

B_FOOD = "Food stores"
B_REST = "Restaurants & bars"
B_APP = "Apparel, shoes & fabric"
B_RET = "General & specialty retail"
B_HOME = "Home furnishings, hardware & appliances"
B_PERS = "Personal services"
B_AUTO = "Auto sales & service"
B_HEALTH = "Health & medical"
B_FIRE = "Finance, insurance & real estate"
B_PROF = "Professional & business services"
B_MEDIA = "Media, printing & entertainment"
B_IND = "Light industrial, trades & wholesale"
B_INST = "Institutional & civic"
B_UNK = "Unidentified business"

RULES = [
 # institutional / civic first
 (r"post office|post ofc|us govt|u s govt|united states government", "post office (Edendale Station)", B_INST, "I"),
 (r"water & power", "LA Dept of Water & Power branch office", B_INST, "I"),
 (r"american legion", "veterans' post (American Legion)", B_INST, "I"),
 (r"lodge no|f&am", "Masonic lodge", B_INST, "I"),
 (r"angelus temple", "church office (Angelus Temple)", B_INST, "I"),
 (r"hebrew mission", "religious mission", B_INST, "I"),
 (r"cystic fibrosis|endowment fund", "nonprofit / charitable organization", B_INST, "I"),
 (r"inner city housing", "nonprofit housing organization", B_INST, "I"),
 (r"central city action", "community action agency", B_INST, "I"),
 (r"circulo chileno", "community / social club", B_INST, "I"),
 (r"telegraph workers|afl-cio", "labor union office", B_INST, "I"),
 (r"internatl geneva|international geneva", "Geneva Association (hospitality workers' society)", B_INST, "I"),
 (r"peace officers|professional employees|calif assn", "professional / employee association", B_INST, "I"),
 (r"los angeles city of", "City of Los Angeles office", B_INST, "I"),
 # health
 (r"pharm|phrm|drug|rexall", "pharmacy / drugstore", B_HEALTH, "B"),
 (r"medical clinic|echo pk medical|echo park medical|medical care program|urgent care", "medical clinic", B_HEALTH, "B"),
 (r"medical lab", "medical laboratory", B_HEALTH, "B"),
 (r"dental lab|dntl lab", "dental laboratory", B_HEALTH, "B"),
 (r"dntst|\bdds\b|\bdmd\b", "dentist's office", B_HEALTH, "B"),
 (r"optm|optometr|\bod\b", "optometrist's office", B_HEALTH, "B"),
 (r"\bdc\b|chirpr|chiropr", "chiropractor's office", B_HEALTH, "B"),
 (r"\bmd\b|-md\b|phy ?& ?sur|\bdr\b", "physician's office", B_HEALTH, "B"),
 (r"nurses professional registry", "nurse staffing registry", B_HEALTH, "B"),
 (r"holistic", "holistic health center", B_HEALTH, "B"),
 # finance, insurance, real estate
 (r"\bbank\b|\bbnk\b|savings|savngs|savng", "bank / savings & loan branch", B_FIRE, "B"),
 (r"credit union", "credit union", B_FIRE, "B"),
 (r"check cashing", "check cashing", B_FIRE, "B"),
 (r"\bfinance\b|financial|\bloan\b|leasing", "finance / loan company", B_FIRE, "B"),
 (r"state farm|\bins\b|insurance|ins agcy|travelers ins|\bclu\b", "insurance agency", B_FIRE, "B"),
 (r"realty|\brlty\b|rltr|real est|rl est|rental|land co|investment|investmts|homeowners|lien serv|equity corp|property", "real estate / property", B_FIRE, "B"),
 # professional & business services
 (r"\batty\b|attys", "attorney's office", B_PROF, "B"),
 (r"\bacct\b|\bcpa\b|cpas|pub acct", "accountant", B_PROF, "B"),
 (r"income tax|tax serv", "tax preparation", B_PROF, "B"),
 (r"creditors serv", "collection agency", B_PROF, "B"),
 (r"advertising", "advertising agency", B_PROF, "B"),
 (r"travel", "travel agency", B_PROF, "B"),
 (r"immigration", "immigration services", B_PROF, "B"),
 (r"parking", "parking operator", B_PROF, "B"),
 (r"driving school", "driving school", B_PROF, "B"),
 (r"vocational testing", "vocational testing service", B_PROF, "B"),
 (r"gas co", "gas utility customer office", B_PROF, "B"),
 (r"bartending", "bartending school", B_PROF, "B"),
 (r"aviation", "aviation company office", B_PROF, "B"),
 (r"world book", "encyclopedia sales office", B_PROF, "B"),
 (r"construction|contractors", "construction contractor", B_IND, "B"),
 # media, printing & entertainment
 (r"journal|leader|publication|publishing|fanfare", "newspaper / publisher", B_MEDIA, "B"),
 (r"printing|printers|offset press|lithograph", "printing shop", B_MEDIA, "B"),
 (r"photograph|photgrphr|portrait|photoland|studios?\b", "photography / portrait studio", B_MEDIA, "B"),
 (r"video", "video store", B_MEDIA, "B"),
 (r"record|music", "record / music store", B_MEDIA, "B"),
 (r"theatre|theater", "theater", B_MEDIA, "B"),
 (r"camera", "camera store / repair", B_RET, "B"),
 (r"gallery", "art gallery / shop", B_RET, "B"),
 (r"\bsigns\b", "sign maker", B_IND, "B"),
 # restaurants & bars
 (r"snack bar", "snack bar", B_REST, "B"),
 (r"body & fender", "auto body repair", B_AUTO, "B"),
 (r"sierra room", "restaurant & cocktail lounge", B_REST, "B"),
 (r"cocktail|tavern|tavrn|beer bar|\bbar\b|lounge", "bar / cocktail lounge", B_REST, "B"),
 (r"pizza", "pizzeria", B_REST, "B"),
 (r"restaurant|restrnt|rstrnt|\bcafe\b|coffee shop|chef|snack bar|fast food|burger|taco|burrito king|orange julius", "restaurant / cafe", B_REST, "B"),
 (r"donut|doughnt", "donut shop", B_REST, "B"),
 # food stores
 (r"liquor|vins et|vin &", "liquor store", B_FOOD, "B"),
 (r"winery", "winery / wine shop", B_FOOD, "B"),
 (r"bakery|bakers", "bakery", B_FOOD, "B"),
 (r"ice cream|confection", "ice cream / candy shop", B_FOOD, "B"),
 (r"poultry", "poultry market", B_FOOD, "B"),
 (r"meat|shrimp|fish emporium", "meat / seafood market", B_FOOD, "B"),
 (r"delicatessen|tortilleria|food mart|produce", "deli / specialty food", B_FOOD, "B"),
 (r"\bmkt\b|market|grocer|groc\b|\bgro\b|supermarket|foods inc|grocery", "grocery / market", B_FOOD, "B"),
 # apparel, shoes, fabric
 (r"shoe repair", "shoe repair", B_PERS, "B"),
 (r"shoe", "shoe store", B_APP, "B"),
 (r"wearing apparel|wear\b|apprl|frock|mode o.?day|dresses|sportswear|fashion|knits|children.?s shop|childrens shop|store for men|finers? store|boutique|dress shop", "clothing store", B_APP, "B"),
 (r"fabric|yardage|remnants", "fabric / yardage store", B_APP, "B"),
 (r"tlr|tailor", "tailor", B_PERS, "B"),
 (r"dressmaking|alterations", "dressmaker / alterations", B_PERS, "B"),
 # personal services
 (r"beauty supply|beauty supplies", "beauty supply store", B_RET, "B"),
 (r"beauty|\bbty\b|salon|hair|wig|nail", "beauty salon", B_PERS, "B"),
 (r"barber|barbr|brbr", "barber shop", B_PERS, "B"),
 (r"laundr|lndromt|launderette|cleaners|clnrs", "laundry / dry cleaner", B_PERS, "B"),
 (r"watch reprng", "watch repair", B_PERS, "B"),
 (r"key shop|locksmith", "key shop / locksmith", B_PERS, "B"),
 (r"bike", "bicycle & key shop", B_PERS, "B"),
 (r"pet shop|tropical fish|trpcl fsh", "pet / tropical fish shop", B_RET, "B"),
 # auto
 (r"chevron|chvrn|shell|standard oil|serv stn|\bserv\b$|service station|mcmahon", "gas / service station", B_AUTO, "B"),
 (r"car wash", "car wash", B_AUTO, "B"),
 (r"tire", "tire shop", B_AUTO, "B"),
 (r"auto supply|auto parts|honest abe", "auto parts store", B_AUTO, "B"),
 (r"auto repair|body & fender|top shop|motor rebuilding|motor rebldg|general repair|transmission", "auto repair", B_AUTO, "B"),
 # home furnishings, hardware, appliances
 (r"furn|furniture", "furniture store", B_HOME, "B"),
 (r"paint|hdwe|hdw|hardware|bolt & screw", "hardware / paint store", B_HOME, "B"),
 (r"blind|shade|interiors", "window blinds / shades", B_HOME, "B"),
 (r"glass|mirror", "glass & mirror shop", B_HOME, "B"),
 (r"rug|carpet|floor cvrng", "carpet / floor covering", B_HOME, "B"),
 (r"television|radio|\btv\b|appliances", "TV / radio sales & repair", B_HOME, "B"),
 (r"vacuum", "vacuum cleaner sales", B_HOME, "B"),
 (r"mattress", "mattress store", B_HOME, "B"),
 (r"elec co|electric co|elec mfg", "electrical contractor / manufacturer", B_IND, "B"),
 # general & specialty retail
 (r"dept store|department store|variety|woolworth|dollar store|giant store|discount|bargain|economica|big m stores|house of bargains|trading post|factory outlet|almacenes|rene store|mdse|mdsng", "department / variety / discount store", B_RET, "B"),
 (r"jewel|jewlr|joyeria", "jewelry store", B_RET, "B"),
 (r"gift|greeting cards|party|flowers|florist|toys|dolls", "gift / florist / toy shop", B_RET, "B"),
 (r"books|libreria|stationer", "book / stationery store", B_RET, "B"),
 (r"sporting goods", "sporting goods store", B_RET, "B"),
 (r"pawnbroker", "pawnshop", B_RET, "B"),
 (r"office mach|office equipt", "office machine sales & repair", B_RET, "B"),
 (r"oil portraits", "portrait painting studio", B_MEDIA, "B"),
 (r"leather goods", "leather goods shop", B_RET, "B"),
 # light industrial, trades, wholesale
 (r"plumb", "plumbing contractor / shop", B_IND, "B"),
 (r"carpenter", "carpentry shop", B_IND, "B"),
 (r"storage|movers|transfr|van-storage", "moving & storage", B_IND, "B"),
 (r"lighting|lightng|\bdaad\b", "lighting fixtures", B_HOME, "B"),
 (r"mfg|mfrs|products co", "manufacturing / manufacturers' agent", B_IND, "B"),
 (r"wholesale|whse", "wholesale", B_IND, "B"),
 (r"auction", "auctioneer", B_PROF, "B"),
]

def match(name):
    s = name.lower()
    for rx, desc, bucket, typ in RULES:
        if re.search(rx, s):
            return typ, desc, bucket, rx
    return None
