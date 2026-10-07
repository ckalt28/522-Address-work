"""Add stable listing_id / entity_id to the classified listings and build the research queue.

Reads  data/derived/listings_classified.csv
Writes data/derived/listings.csv        (one row per printed listing, with ids)
       research/research_queue.csv      (one row per business entity to look up)
Does NOT touch research/findings.csv.

entity = business or institutional listings on the same lot with the same normalized name.
listing_id = YEAR-ADDRESS-NN (h/q/t stand for 1/2, 1/4, 3/4), stable as long as transcriptions don't change order.
"""
import csv, re
from collections import defaultdict, Counter

L = list(csv.DictReader(open('data/derived/listings_classified.csv')))
cnt = defaultdict(int)
for r in L:
    k = (r['year'], r['address']); cnt[k] += 1
    a = r['address'].replace('½', 'h').replace('¼', 'q').replace('¾', 't')
    r['listing_id'] = f"{r['year']}-{a}-{cnt[k]:02d}"

def norm(n):
    n = n.upper()
    n = re.sub(r"\[.*?\]|\(.*?\)", "", n)
    n = re.sub(r"[^A-Z0-9 ]", " ", n)
    n = re.sub(r"\b(THE|INC|CO|CORP|LTD|S)\b", " ", n)
    return ' '.join(n.split())

RANK = {'low': 0, 'medium': 1, 'high': 2}
ent = defaultdict(list)
for r in L:
    if r['use_type'] in ('Business', 'Institutional'):
        ent[(int(r['lot']), norm(r['listing']))].append(r)

rows = []
for (lot, nm), rs in ent.items():
    worst = min((x['class_confidence'] for x in rs), key=RANK.get)
    buck = rs[-1]['business_bucket']
    p = 1 if buck == 'Unidentified business' else (2 if worst == 'low' else (3 if worst == 'medium' else 4))
    rows.append(dict(entity_id='', priority=p, lot=lot,
        addresses=' '.join(sorted({x['address'] for x in rs})),
        years=' '.join(sorted({x['year'] for x in rs})),
        name_variants=' | '.join(dict.fromkeys(x['listing'] for x in rs)),
        phones=' | '.join(dict.fromkeys(f"{x['year']}:{x['phone']}" for x in rs if x['phone'])),
        current_desc=rs[-1]['business_desc'], current_bucket=buck, current_confidence=worst,
        current_basis=rs[-1]['class_basis'], listing_ids=' '.join(x['listing_id'] for x in rs)))
rows.sort(key=lambda r: (r['priority'], r['lot'], r['years']))
for i, r in enumerate(rows, 1):
    r['entity_id'] = f"E{i:04d}"
lid2e = {l: r['entity_id'] for r in rows for l in r['listing_ids'].split()}
for r in L:
    r['entity_id'] = lid2e.get(r['listing_id'], '')

cols = ['listing_id', 'entity_id'] + [c for c in L[0] if c not in ('listing_id', 'entity_id')]
with open('data/derived/listings.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, cols); w.writeheader(); w.writerows(L)
with open('research/research_queue.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(L), 'listings;', len(rows), 'entities; by priority', dict(sorted(Counter(r['priority'] for r in rows).items())))
