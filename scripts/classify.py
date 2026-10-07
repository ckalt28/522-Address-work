import csv, re, json, sys
from collections import defaultdict, Counter
sys.path.insert(0, 'scripts')
from classify_rules import match, B_UNK, B_INST
from overrides import O, OY, OFFICE_LOTS

L = list(csv.DictReader(open('data/derived/listings_flagged.csv')))
YEARS = ['1906','1927','1956','1960','1964','1965','1968','1973','1987']
TYPE_NAME = {'B':'Business','I':'Institutional','R':'Residential','H':'Apartment building','V':'Vacant','X':'Unknown'}
CONF = {'low':0,'medium':1,'high':2}

def is_caps(s):
    l = re.sub(r'[^A-Za-z]', '', s)
    return bool(l) and l.isupper()
def surname(s):
    t = re.findall(r"[A-Za-z']+", s)
    return t[0].lower() if t else ''

# index: per (year, exact address) any keyword/override business present
def base_class(r):
    y, n, unit = int(r['year']), r['listing'], r['unit']
    if (y, n) in OY: return OY[(y, n)]
    if n in O: return O[n]
    if 'phone listed, no name' in n or n.startswith('[unit phone only]'):
        return ('R', 'apartment unit (phone only)', '', 'medium', 'unit phone listed without a name')
    m = match(n)
    if m:
        typ, desc, bucket, rx = m
        conf = 'high'
        return (typ, desc, bucket, conf, f"trade/name keyword")
    return None

rows = []
for r in L:
    rows.append(r)
    r['_lot'] = int(r['street_number'])
    r['_c'] = base_class(r)

# evidence for 1964-68 bare names: same surname as a bare/resident listing at the same lot in another year
res_surnames = defaultdict(set)   # lot -> surnames seen as clear residents (1956/60/73 bare, 1987 mixed)
for r in rows:
    if r['_c'] is None and not r['unit'] and r['year'] in ('1956','1960','1973'):
        res_surnames[r['_lot']].add(surname(r['listing']))
    if r['_c'] is None and r['year'] == '1987' and not is_caps(r['listing']):
        res_surnames[r['_lot']].add(surname(r['listing']))

# apartment lots (any year has H or 3+ unit listings)
unit_counts = Counter((r['_lot']) for r in rows if r['unit'])
apt_lots = {r['_lot'] for r in rows if r['_c'] and r['_c'][0] == 'H'} | {l for l, c in unit_counts.items() if c >= 3}

biz_at = defaultdict(bool)
for r in rows:
    if r['_c'] and r['_c'][0] in 'BI':
        biz_at[(r['year'], r['address'])] = True

def down(c): return {'high':'medium','medium':'low','low':'low'}[c]

for r in rows:
    if r['_c']: continue
    y, n, unit, lot = r['year'], r['listing'], r['unit'], r['_lot']
    if unit:
        if lot in OFFICE_LOTS:
            r['_c'] = ('B', 'office tenant (trade not stated)', B_UNK, 'low', 'name in an office-building suite'); continue
        if y == '1987' and is_caps(n):
            if lot in apt_lots:
                r['_c'] = ('R', 'household (apartment unit)', '', 'low', '1987 capitals usually mean a business, but this is a unit in an apartment building'); continue
            r['_c'] = ('B', 'unidentified business (name only)', B_UNK, 'low', '1987 capitals in a suite'); continue
        r['_c'] = ('R', 'household (apartment unit)', '', 'high', 'listed by unit number'); continue
    # building-level bare name
    if lot in OFFICE_LOTS:
        r['_c'] = ('B', 'office tenant (trade not stated)', B_UNK, 'low', 'name listed in an office building'); continue
    if y == '1987':
        if is_caps(n):
            r['_c'] = ('B', 'unidentified business (personal name in capitals)', B_UNK, 'low', '1987 sets businesses in capitals; no trade given')
        else:
            r['_c'] = ('R', 'household', '', 'high', '1987 sets residents in mixed case')
        continue
    if y in ('1906','1927'):
        conf, basis = 'medium', 'bare name; this directory adds a trade for businesses'
    elif y in ('1956','1960'):
        conf, basis = 'medium', 'bare name; this directory usually adds a trade for businesses'
        if re.search(r'\br\b', n): basis += "; trailing 'r'"
    elif y == '1973':
        conf, basis = 'medium', 'bare personal name, no business name'
    else:  # 1964-68 printouts drop trades
        if surname(n) in res_surnames[lot]:
            conf, basis = 'medium', 'bare name; same surname listed as a resident here in another year'
        else:
            conf, basis = 'low', '1964-68 printouts often drop trades; bare name with no other evidence'
    if biz_at[(y, r['address'])]:
        conf = down(conf); basis += '; a business shares this exact address (could be the proprietor)'
    r['_c'] = ('R', 'household', '', conf, basis)

# ---- lot-year roll-up
def categorize(ls):
    types = [l['_c'][0] for l in ls]
    res = [l for l in ls if l['_c'][0] in 'RH']
    non = [l for l in ls if l['_c'][0] in 'BI']
    if res and non: return 'Mixed-use'
    if res:
        if any(l['_c'][0] == 'H' for l in res): return 'Residential – multifamily'
        units = {l['unit'] for l in res if l['unit']}
        addrs = {l['address'] for l in res}
        sn = {surname(l['listing']) for l in res if not l['unit']}
        if units or len(addrs) >= 2 or len(sn) >= 3:
            return 'Residential – multifamily'
        return 'Residential – single-family'
    if non:
        return 'Institutional' if all(l['_c'][0] == 'I' for l in non) else 'Commercial'
    if 'V' in types: return 'Vacant'
    return 'Unknown'

lots = defaultdict(lambda: defaultdict(list))
for r in rows: lots[r['_lot']][r['year']].append(r)

landuse = {}
for lot in lots:
    for y, ls in lots[lot].items():
        ls2 = [l for l in ls if l['_c'][0] != 'X'] or ls
        cat = categorize(ls2)
        med = [l for l in ls2 if CONF[l['_c'][3]] >= 1]
        hi = [l for l in ls2 if CONF[l['_c'][3]] >= 2]
        if not med or categorize(med) != cat: conf = 'low'
        elif not hi or categorize(hi) != cat: conf = 'medium'
        else: conf = 'high'
        notes = []
        res_sn = {surname(l['listing']) for l in ls2 if l['_c'][0] == 'R' and not l['unit']}
        if cat == 'Residential – single-family' and len(res_sn) == 2:
            notes.append('two surnames at one number: boarders or a second unit'); conf = 'low' if conf == 'low' else 'medium'
        base_listed = any(l['address'] == str(lot) for l in ls)
        if not base_listed:
            notes.append(f'only a fractional address listed; {lot} itself not listed')
            if conf == 'high': conf = 'medium'
        buckets = sorted({l['_c'][2] for l in ls2 if l['_c'][0] in 'BI' and l['_c'][2]})
        landuse[(lot, y)] = dict(cat=cat, conf=conf, buckets=buckets, notes='; '.join(notes))

# ---- write long with new columns
for r in rows:
    t, d, b, c, basis = r['_c']
    r['use_type'] = TYPE_NAME[t]
    r['business_desc'] = d if t in 'BI' else ''
    r['business_bucket'] = b if t in 'BI' else ''
    r['class_confidence'] = c
    r['class_basis'] = basis
    r['lot'] = r['_lot']
    r['lot_land_use'] = landuse[(r['_lot'], r['year'])]['cat']
cols = list(L[0].keys())
cols = [c for c in cols if not c.startswith('_')]
with open('data/derived/listings_classified.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, cols, extrasaction='ignore'); w.writeheader(); w.writerows(rows)

with open('data/derived/landuse_by_lot.csv', 'w', newline='') as fh:
    w = csv.writer(fh)
    hdr = ['lot', 'side']
    for y in YEARS: hdr += [f'{y}_land_use', f'{y}_confidence', f'{y}_business_buckets', f'{y}_notes']
    w.writerow(hdr)
    for lot in sorted(lots):
        row = [lot, 'odd' if lot % 2 else 'even']
        for y in YEARS:
            v = landuse.get((lot, y))
            row += [v['cat'], v['conf'], '; '.join(v['buckets']), v['notes']] if v else ['', '', '', '']
        w.writerow(row)

# summaries
s1 = defaultdict(Counter); s2 = defaultdict(Counter); s3 = defaultdict(Counter)
for (lot, y), v in landuse.items():
    s1[y][v['cat']] += 1; s3[y][v['conf']] += 1
seen=set()
for r in rows:
    if r['_c'][0] in 'BI' and r['_c'][2]:
        k=(r['year'], r['_lot'], r['_c'][2])
        if k in seen: continue
        seen.add(k); s2[r['year']][r['_c'][2]] += 1
json.dump({'landuse': {y: dict(s1[y]) for y in YEARS}, 'buckets': {y: dict(s2[y]) for y in YEARS}, 'lotconf': {y: dict(s3[y]) for y in YEARS}}, open('data/derived/summary.json', 'w'), indent=1)
print('listing types', Counter(r['use_type'] for r in rows))
print('listing conf', Counter(r['class_confidence'] for r in rows))
for y in YEARS: print(y, dict(s1[y]), dict(s3[y]))
