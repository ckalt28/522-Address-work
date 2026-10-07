"""Fold research/findings.csv back into the listings without touching the text-only outputs.

Reads  data/derived/listings.csv + research/findings.csv
Writes data/derived/listings_verified.csv       listings + verified_* columns + effective (*_final) columns
       data/derived/landuse_by_lot_verified.csv lot land use recomputed with verified values where they exist
       data/derived/summary_verified.json       same shape as summary.json, plus before/after bucket deltas

Only findings with status confirmed / corrected / identified change anything; not_found and
transcription_issue rows are carried as notes. Land-use rules are the ones in classify.py.

Run from the repo root:  python3 scripts/apply_findings.py
"""
import csv, json, re
from collections import defaultdict, Counter

YEARS = ['1906', '1927', '1956', '1960', '1964', '1965', '1968', '1973', '1987']
CONF = {'low': 0, 'medium': 1, 'high': 2}
TYPE_CODE = {'Business': 'B', 'Institutional': 'I', 'Residential': 'R', 'Apartment building': 'H',
             'Vacant': 'V', 'Unknown': 'X'}
APPLY = {'confirmed', 'corrected', 'identified'}

def surname(s):
    t = re.findall(r"[A-Za-z']+", s)
    return t[0].lower() if t else ''

# ---- inputs
L = list(csv.DictReader(open('data/derived/listings.csv')))
F = {r['entity_id']: r for r in csv.DictReader(open('research/findings.csv'))}

# ---- per-listing effective classification
for r in L:
    f = F.get(r['entity_id']) if r['entity_id'] else None
    use = f and f['finding_status'] in APPLY
    r['finding_status'] = f['finding_status'] if f else ''
    r['verified_desc'] = f['verified_desc'] if use else ''
    r['verified_bucket'] = f['verified_bucket'] if use else ''
    r['verified_use_type'] = f['verified_use_type'] if use else ''
    r['verified_confidence'] = f['confidence'] if use else ''
    r['evidence_url'] = f['evidence_url'] if use else ''
    for c in ('owner_ethnicity', 'clientele_ethnicity', 'clientele_class'):
        r[c] = (f.get(c) or '') if f else ''
    r['use_type_final'] = r['verified_use_type'] or r['use_type']
    r['business_desc_final'] = r['verified_desc'] or r['business_desc']
    if r['use_type_final'] in ('Business', 'Institutional'):
        r['business_bucket_final'] = r['verified_bucket'] or r['business_bucket']
    else:
        r['business_bucket_final'] = ''
    r['confidence_final'] = r['verified_confidence'] or r['class_confidence']
    r['_t'] = TYPE_CODE[r['use_type_final']]
    r['_conf'] = r['confidence_final']
    r['_lot'] = int(r['lot'])

# ---- lot-year roll-up (same rules as classify.py)
def categorize(ls):
    types = [l['_t'] for l in ls]
    res = [l for l in ls if l['_t'] in 'RH']
    non = [l for l in ls if l['_t'] in 'BI']
    if res and non: return 'Mixed-use'
    if res:
        if any(l['_t'] == 'H' for l in res): return 'Residential – multifamily'
        units = {l['unit'] for l in res if l['unit']}
        addrs = {l['address'] for l in res}
        sn = {surname(l['listing']) for l in res if not l['unit']}
        if units or len(addrs) >= 2 or len(sn) >= 3:
            return 'Residential – multifamily'
        return 'Residential – single-family'
    if non:
        return 'Institutional' if all(l['_t'] == 'I' for l in non) else 'Commercial'
    if 'V' in types: return 'Vacant'
    return 'Unknown'

lots = defaultdict(lambda: defaultdict(list))
for r in L: lots[r['_lot']][r['year']].append(r)

landuse = {}
for lot in lots:
    for y, ls in lots[lot].items():
        ls2 = [l for l in ls if l['_t'] != 'X'] or ls
        cat = categorize(ls2)
        med = [l for l in ls2 if CONF[l['_conf']] >= 1]
        hi = [l for l in ls2 if CONF[l['_conf']] >= 2]
        if not med or categorize(med) != cat: conf = 'low'
        elif not hi or categorize(hi) != cat: conf = 'medium'
        else: conf = 'high'
        notes = []
        res_sn = {surname(l['listing']) for l in ls2 if l['_t'] == 'R' and not l['unit']}
        if cat == 'Residential – single-family' and len(res_sn) == 2:
            notes.append('two surnames at one number: boarders or a second unit'); conf = 'low' if conf == 'low' else 'medium'
        if not any(l['address'] == str(lot) for l in ls):
            notes.append(f'only a fractional address listed; {lot} itself not listed')
            if conf == 'high': conf = 'medium'
        buckets = sorted({l['business_bucket_final'] for l in ls2 if l['_t'] in 'BI' and l['business_bucket_final']})
        verified = sorted({l['entity_id'] for l in ls2 if l['verified_bucket'] or l['verified_use_type']})
        landuse[(lot, y)] = dict(cat=cat, conf=conf, buckets=buckets, notes='; '.join(notes), verified=verified)

for r in L:
    r['lot_land_use_final'] = landuse[(r['_lot'], r['year'])]['cat']

# ---- outputs
cols = [c for c in L[0].keys() if not c.startswith('_')]
with open('data/derived/listings_verified.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, cols, extrasaction='ignore'); w.writeheader(); w.writerows(L)

with open('data/derived/landuse_by_lot_verified.csv', 'w', newline='') as fh:
    w = csv.writer(fh)
    hdr = ['lot', 'side']
    for y in YEARS:
        hdr += [f'{y}_land_use', f'{y}_confidence', f'{y}_business_buckets', f'{y}_notes', f'{y}_verified_entities']
    w.writerow(hdr)
    for lot in sorted(lots):
        row = [lot, 'odd' if lot % 2 else 'even']
        for y in YEARS:
            v = landuse.get((lot, y))
            row += [v['cat'], v['conf'], '; '.join(v['buckets']), v['notes'], ' '.join(v['verified'])] if v else ['', '', '', '', '']
        w.writerow(row)

def bucket_counts(bucket_col, type_col):
    """lots with at least one business in each bucket, per year (same counting as summary.json)"""
    out, seen = defaultdict(Counter), set()
    for r in L:
        t = TYPE_CODE[r[type_col]]
        b = r[bucket_col]
        if t in 'BI' and b:
            k = (r['year'], r['_lot'], b)
            if k in seen: continue
            seen.add(k); out[r['year']][b] += 1
    return out

before = bucket_counts('business_bucket', 'use_type')
after = bucket_counts('business_bucket_final', 'use_type_final')
s1, s3 = defaultdict(Counter), defaultdict(Counter)
for (lot, y), v in landuse.items():
    s1[y][v['cat']] += 1; s3[y][v['conf']] += 1
delta = {}
for y in YEARS:
    ks = set(before[y]) | set(after[y])
    d = {k: after[y][k] - before[y][k] for k in sorted(ks) if after[y][k] != before[y][k]}
    if d: delta[y] = d
status = Counter(f['finding_status'] for f in F.values())
json.dump({'landuse': {y: dict(s1[y]) for y in YEARS},
           'buckets': {y: dict(after[y]) for y in YEARS},
           'lotconf': {y: dict(s3[y]) for y in YEARS},
           'buckets_text_only': {y: dict(before[y]) for y in YEARS},
           'bucket_change': delta,
           'findings_by_status': dict(status)},
          open('data/derived/summary_verified.json', 'w'), indent=1)

print('findings by status', dict(status))
print('listings with a verified value', sum(1 for r in L if r['verified_bucket'] or r['verified_use_type']))
for y in YEARS:
    if y in delta: print(y, 'bucket change', delta[y])
