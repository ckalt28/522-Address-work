import re, csv, json, glob
from fractions import Fraction

YEARS=[1906,1927,1956,1960,1964,1965,1968,1973,1987]
SRC={}
rows=[]
for y in YEARS:
    lines=open(f'data/transcriptions/{y}.txt').read().splitlines()
    src=lines[0].split('source=')[1]
    SRC[y]=src
    for ln in lines[1:]:
        if not ln.strip(): continue
        parts=ln.split('|')
        addr,unit,name=parts[0].strip(),parts[1].strip(),parts[2].strip()
        phone=parts[3].strip() if len(parts)>3 else ''
        rows.append(dict(year=y,addr=addr,unit=unit,raw=name,phone=phone))

def addr_key(a):
    m=re.match(r'(\d+)(?:\s+(\d)/(\d))?$',a)
    n=int(m.group(1)); f=Fraction(int(m.group(2)),int(m.group(3))) if m.group(2) else Fraction(0)
    return (n,f)
def addr_label(a):
    return a.replace(' 1/2','½').replace(' 1/4','¼').replace(' 3/4','¾')

TITLES=[('Mrs','Mrs'),('Miss','Miss'),('Dr','Dr'),('MD','MD'),('DDS','DDS'),('DMD','DMD'),('DC','DC'),('OD','OD'),
        ('atty','atty'),('ATTY','atty'),('ATTYS','atty'),('Rev','Rev'),('REV','Rev'),('CPA','CPA'),('CPAS','CPA'),('Sr','Sr'),('Jr','Jr'),('JR','Jr')]
ORG=['Inc','INC','Co','CO','Corp','CORP','Corporation','Assn','ASSN','Association','Ltd','Company','COMPANY','Bros','BROS','Associates','ASSOCIATES','Assocs','ASSOCS','Agcy','Agency','AGENCY','Foundation','Fund','Union','UNION']
TRADE=r"\b(mkt|market|grocer|gro\b|groc|meat|poultry|bakery|baker|donut|doughnt|cafe|restaurant|restrnt|rstrnt|restrant|pizza|taco|burrito|burger|food|deli|delicatessen|tortilleria|liquor|winery|cocktail|tavern|tavrn|bar\b|lounge|inn\b|ice cream|confection|drug|pharm|phrm|rexall|clinic|medical|dental|dntl|dntst|optm|chirop|chirpr|phy & surg|phy&sur|hospital|beauty|bty|salon|barber|brbr|hair|wig|nail|cleaner|clnrs|clnrs|laundr|lndromt|launderette|tailor|tlr|dressmak|shoe|apparel|wear|frock|dress|fashion|yardage|fabric|knits|store|stores|shop|shoppe|dept|outlet|furn|furniture|appliance|hardware|hdwe|hdw|paint|lumber|plumb|glass|mirror|carpet|rug|blind|shade|auto|tire|motor|garage|serv stn|chevron|shell|oil|car wash|transmission|radiator|cycle|realty|rlty|rltr|real est|rl est|rlest|ins\b|insurance|bank|bnk|savings|savngs|loan|finance|financial|credit|check cashing|acct|tax|travel|photo|photgr|studio|camera|record|music|video|radio|television|tv\b|printing|printers|press|publish|publications|pub\b|journal|leader|advertising|sign|jewel|jewlr|watch|gift|flowers|florist|toys|pet\b|pet shop|tropical fsh|fish|vacuum|piano|movers|storage|van\b|transfr|parking|church|temple|mission|lodge|legion|post office|post ofc|govt|government|water & power|gas co|school|theatre|theater|auction|lithograph|mfg|mfrs|mattress|antiq|produce|wholesale|whse|investment|investmts|leasing|cpa|attys?\b|propert)"
def flags(r):
    y=r['year']; raw=r['raw']; f={}
    clean=re.sub(r'\[.*?\]|\(if no ans call.*?\)','',raw).strip()
    f['is_vacant']= 'Y' if clean.lower()=='vacant' else ''
    f['is_bldg_header']='Y' if raw.startswith('[') and ('APARTMENT' in raw or 'BUILDING' in raw or 'address printed' in raw) else ''
    f['unit_only_phone']='Y' if 'unit phone only' in raw else ''
    # typography: caps only informative in 1987 (bold caps vs mixed); 1964-68 are all-caps printouts
    if y==1987:
        letters=re.sub(r'[^A-Za-z]','',clean)
        f['caps_business_style']='Y' if letters and letters.isupper() else 'N'
    else:
        f['caps_business_style']=''
    toks=re.findall(r"[A-Za-z&'\.]+",clean)
    tl=[t.strip('.') for t in toks]
    f['title_suffix']=','.join(sorted({v for k,v in TITLES if k in tl}))
    f['org_word']='Y' if any(t in ORG for t in tl) or '&' in clean or "'s" in clean.lower() or "s " in '' else ''
    m=re.findall(TRADE,clean.lower())
    f['trade_words']=','.join(sorted(set(m)))
    f['resident_r_flag']='Y' if y in (1956,1960) and re.search(r'\br\b',clean) else ''
    f['parenthetical_bldg_name']='Y' if re.match(r'\(.*\)',clean) else ''
    return f

def clean_name(raw):
    n=re.sub(r'\s*\[(?!APARTMENT|BUILDING|address|unit phone).*?\]','',raw)  # strip editorial notes
    n=re.sub(r'\s*\(if no ans call.*?\)','',n)
    return n.strip()
def note(raw):
    m=re.findall(r'\[(.*?)\]',raw); n=[x for x in m if not x.startswith(('APARTMENT','BUILDING','address','unit phone'))]
    m2=re.findall(r'\((if no ans call.*?)\)',raw)
    return '; '.join(n+m2)

def unit_label(u,y):
    if not u: return ''
    if re.match(r'^(Apt|Rm|2nd|FL)',u): return u
    if u=='-': return '(unit not given)'
    if u=='rear': return 'rear'
    return f'#{u}'

long=[]
for i,r in enumerate(rows):
    a=r['addr']
    n,frac=addr_key(a)
    if not (1400<=n<=2100): continue
    f=flags(r)
    long.append(dict(year=r['year'],address=addr_label(a),street_number=n,
        half_address=('Y' if frac else ''),unit=unit_label(r['unit'],r['year']),
        listing=clean_name(r['raw']),
        phone=r['phone'],notes=note(r['raw']),**f,_k=addr_key(a),_ord=i))
long.sort(key=lambda d:(d['_k'],d['year'],d['_ord']))
# listings per address-year
from collections import Counter,defaultdict
cnt=Counter((d['address'],d['year']) for d in long)
for d in long: d['listings_at_address_that_year']=cnt[(d['address'],d['year'])]

# wide
cells=defaultdict(lambda: defaultdict(list))
order={}
for d in long:
    order[d['address']]=d['_k']
    nm=d['listing']
    if d['unit_only_phone']: nm='(phone listed, no name)'
    entry=(d['unit'],nm)
    if entry not in cells[d['address']][d['year']]:
        cells[d['address']][d['year']].append(entry)
def fmt(entries):
    bldg=[n for u,n in entries if not u]
    units=[(u,n) for u,n in entries if u]
    out=[]
    out+=bldg
    # group unit entries
    g=defaultdict(list)
    for u,n in units:
        if n not in g[u]: g[u].append(n)
    for u,ns in g.items(): out.append(f"{u}: {' / '.join(ns)}")
    return '; '.join(out)
wide=[]
for a in sorted(cells,key=lambda x:order[x]):
    row={'address':a,'street_number':order[a][0],'side':('odd' if order[a][0]%2 else 'even')}
    for y in YEARS: row[str(y)]=fmt(cells[a][y]) if y in cells[a] else ''
    row['years_listed']=sum(1 for y in YEARS if y in cells[a])
    wide.append(row)

LONG_COLS=['year','address','street_number','half_address','unit','listing','listings_at_address_that_year','caps_business_style','title_suffix','org_word','trade_words','resident_r_flag','parenthetical_bldg_name','is_vacant','is_bldg_header','unit_only_phone','phone','notes']
WIDE_COLS=['address','street_number','side']+[str(y) for y in YEARS]+['years_listed']
with open('data/derived/listings_flagged.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,LONG_COLS,extrasaction='ignore'); w.writeheader(); w.writerows(long)
with open('data/derived/by_address_wide.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,WIDE_COLS); w.writeheader(); w.writerows(wide)
json.dump(SRC,open('data/sources.json','w'),indent=1)
print(len(long),'listings;',len(wide),'addresses')
print(Counter(d['year'] for d in long))
