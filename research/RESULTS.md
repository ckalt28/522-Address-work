# Results: outside-source research on the Sunset Blvd businesses

Status as of 2026-10-08. Priorities 1–3 are complete. The priority 4 pass is nearly done (17 rows so far; a retry of failed phone searches is running).
Findings are in `research/findings.csv`. `scripts/apply_findings.py` folds them into
`data/derived/listings_verified.csv`, `landuse_by_lot_verified.csv` and `summary_verified.json`. The
text-only files are unchanged.

## How many entities were resolved

| priority | entities | confirmed | corrected | identified | not_found |
|---|---|---|---|---|---|
| 1 (unidentified) | 37 | 3 | 0 | 3 | 31 |
| 2 (low confidence) | 33 | 4 | 0 | 0 | 29 |
| 3 (medium) | 20 | 4 | 3 | 0 | 13 |
| 4 (high; lighter pass — rows only where a source adds something) | 572 | 14 | 3 | 0 | — |

The results are thin, and that is mostly about what sources exist. Businesses from the 1950s–80s on this
strip have almost no web presence. CDNC, HathiTrust and HistoricPlacesLA could not be read from this session,
and latimes.com and UCLA's LA Times photo archive opt out of Anthropic's crawler (see `LOG.md`). What did work:
- **City of LA Office of Finance tax registrations**: the 1987 personal names.
- **CA ABC liquor licenses**: the 1980s bars and restaurants.
- **Trade magazines and high-school yearbook ads on Internet Archive**: the 1950s–70s owners and phones.
- **LAPL's menu and photo catalogue**.

Several sources that would have settled entities are lending-only on IA, so their text can't be read. These
include a 1981 Cal State LA alumni directory, a 1969 business directory and a 1990 restaurant guide. They are
listed as unread leads in the notes but never used as evidence.

Each confirmed, corrected or identified row has a source that ties the name to the address or phone in the
right era. In 15 of the 21 rows, the quoted source itself prints the street number or the phone. In the
other six, the source establishes what the business was, and the address comes from the directory or a second
cited record. Those six are JWCH, Cass & Johansing, the Peace Officers association and the three Winston
Schaefer rows.

## How the bucket counts changed

Lots with at least one business in each bucket, text-only → verified (bold = changed):

| bucket | 1906 | 1927 | 1956 | 1960 | 1964 | 1965 | 1968 | 1973 | 1987 |
|---|---|---|---|---|---|---|---|---|---|
| Food stores | 2 | 7 | 13 | 12 | **9→10** | **10→11** | 9 | 9 | **9→8** |
| Restaurants & bars | 0 | 0 | 10 | 16 | 19 | 18 | 19 | 18 | 17 |
| Apparel, shoes & fabric | 0 | 0 | 11 | 9 | 10 | 11 | 10 | **11→12** | **7→8** |
| General & specialty retail | 0 | 0 | 13 | 15 | 18 | 15 | 14 | 18 | 17 |
| Home furnishings, hardware & appliances | 0 | 0 | 12 | 13 | 12 | 11 | 14 | 8 | 4 |
| Personal services | 0 | 0 | 15 | 14 | 10 | 11 | 11 | 10 | 11 |
| Auto sales & service | 1 | 0 | 5 | 6 | 5 | 5 | 6 | 4 | 6 |
| Health & medical | 0 | 8 | 15 | 13 | 11 | 10 | 10 | 13 | 9 |
| Finance, insurance & real estate | 1 | 0 | **12→11** | **13→12** | **12→11** | **12→11** | 10 | 10 | 5 |
| Professional & business services | 0 | 0 | 8 | 7 | 4 | 3 | 6 | 7 | **9→10** |
| Media, printing & entertainment | 0 | 0 | 5 | 6 | 4 | 4 | 5 | 5 | 3 |
| Light industrial, trades & wholesale | 0 | 0 | 8 | **7→8** | **4→5** | **5→6** | 3 | 4 | **1→2** |
| Institutional & civic | 0 | 0 | 4 | 4 | 2 | 2 | 2 | 4 | 2 |
| Unidentified business | 0 | 1 | 1 | **3→2** | **3→2** | **3→2** | 3 | **6→5** | **18→16** |

No lot changed its land-use category: every correction kept the listing a business or institution.

## 1987: the 18 unidentified lots

Two of the 18 lots were resolved:
- **1511 "CARMELA'S"** is Carmela's Fashions, a women's clothing store. The proof is a 1972 yearbook ad at the
  same address with the 1973 listing's phone number. Apparel goes from 7 to 8 lots.
- **1566 "ZOZULA CARLOS E"** is the Zozula-Vasquez Income Tax service. Its city registration at this address
  dates from 1965. Professional & business services goes from 9 to 10 lots.

Three more were confirmed as businesses: THI HUNG TRINH (1498 #4, registered 1984), ENRIQUE ZUNIGA
(1513½, 1985) and EUSEBIO J REYES (1529, 1980). Each has a city business-tax account in that name at that
address, so the directory's convention of setting businesses in capitals holds up. The accounts give no trade,
though, so these lots stay *Unidentified business*.

The other 13 unidentified 1987 lots had no usable source. Treat the 1987 bucket counts as having roughly 16
lots of unknown type. That is more than the gap between most buckets, so the 1987 mix shouldn't be compared
bucket by bucket with earlier years without that caveat.

## Findings that change the story

1. **Pioneer Supermarket was hidden behind its holding company.** The text-only data treats
   "Winston Schaefer Inc" at 1601 (1956–65) as a real-estate office. A 1961 cattle-trade article names
   "Winston Schaefer, Inc., owner of the Pioneer Supermarket on Los Angeles' Sunset Boulevard". It shares
   Pioneer's phone. In 1964–65 the directory prints only the company name at 1601, so the supermarket
   didn't show up in the text-only counts for those years.
   - Food stores gains a lot in 1964–65.
   - Finance, insurance & real estate loses one in every year from 1956 to 1965.
   - Real estate's later decline is therefore a little less steep than the text-only data shows.
   - A 1978 teaching module describes Pioneer as a 24-hour market that took food stamps (see below).
2. **The bar cluster is stable and confirmed.** Bars that rested on name-only guesses now have sources:
   - The Gold Room is a "Cocktail Lounge ... Open 10 a.m. to 2 a.m. 7 Days" in a 1977 *Gráfica* ad with
     the 1968/73 phone, and has held a bar licence since 1983.
   - El Prado has held a beer-bar licence since 1990.
   - Little Joy (1477) has held a bar licence since 1977.
   - Sam's Service Station (1475) is confirmed by a 1959 ad.

   These don't change the counts, but the Restaurants & bars series no longer depends on guesses.
3. **There was a small graphic-arts supply business at 1402 (1959–65).** The "Polychrome Corp" listing turns
   out to be Polychrome's Southern California distribution point (Westco Litho Products, 1959). It adds one
   lot to Light industrial, trades & wholesale in 1960–65.
4. **Two professional offices are more specific than "Dr".** Fernando Barreto (1612) is a DDS (dentist) and
   Michael B. Cohen (1830) is a DPM (podiatrist). The bucket doesn't change.
5. **Most low-confidence "shop" calls are still unknown.** These are Dora's Shoppe, Dolores Shop, Toni's,
   Jay Leslie's, Ben's Shop and similar. None turned up in any source. They remain the biggest soft spot in the
   1956–73 retail counts.

## Priority 4: what the lighter pass added

Rows were recorded only where a source sharpened or contradicted the printed trade:

- **Bucket changes.**
  - **Wing Lee Shrimp Co (1422, 1987)** was a seafood importer, according to a 1994 world directory of
    seafood importers with the same phone. It moves from Food stores to Light industrial, trades & wholesale.
    That is the 1987 change in both rows of the table above.
- **Sharper descriptions (same bucket).**
  - Henry's (1602, 1956/60) was a men's store ("Henry's For Men", 1958 ad).
  - Helen's (1414 → 1484) made natural fruit bars that were also sold through health-food stores (KPFK
    Folio ad, October 1974).
  - Barragan's Cafe (1536/1544) was a Mexican restaurant (April 1974 dining review).
  - Pioneer was a 24-hour supermarket (1978).
  - Capri Beauty Salon (1515) also had a men's stylist (1983 ad).
  - Hitchcock Publishing (1910) was a Wheaton, Illinois trade-magazine publisher's Los Angeles office, not
    a local paper.
  - Helitac Aviation (1910, Suite 900) was a helicopter charter operator.
  - Libreria Mexico (1632) was one branch of a four-store Spanish-language bookstore chain.
  - Taix (1911) was a French restaurant from 1962.
  - KFSG, the church's radio station, was in the Angelus Temple suite at 1910.
  - Dr. Barreto (1612) was a dentist, and Dr. Cohen (1830) a podiatrist.
- **Address conflicts noted, not resolved.**
  - Helen's appears at both 1414 and 1484 in 1974 sources.
  - Barragan's is listed at 1544 in 1964–65 and at 1536 from 1968, with the same phone.
  - The 1974 Libreria Mexico ad reads "4032 Sunset".

Most of the 572 priority 4 entities had nothing to add. Their printed trades stand as transcribed.

## Ownership ethnicity, clientele ethnicity, clientele class

None of the new demographic columns is filled yet. I didn't find any source from the right era that states
a business's owner ethnicity, clientele ethnicity or clientele class outright. My rule is to never infer these
from a surname or business name (`OPEN_QUESTIONS.md` #1). Evidence that comes close is kept in
`researcher_notes`:
- **Language of service.**
  - Pescado Mojado's 1988 menu is in English and Spanish.
  - A 1983 Capri Beauty Salon ad (1515) is mostly in Spanish ("Estilista para hombres ... Para su
    Conveniencia Abrimos Domingos ... Abierto 7 Dias"), with its hours also in English.
  - A 1972 bookkeeping and income-tax ad at 1463 says "Se Habla Español".
  - LAPL's 1980 photos note Spanish-language signs at 1539 (a carnicería) and at 1547 and 1555.
  - The Gold Room advertised in *Gráfica* (1977), whose pages mix Spanish and English.
- **Community ties.** In 1986, Suite 460 at 1910 W Sunset (the Lew & Wang phone) was the contact address
  for the LA Lodge of the Chinese American Citizens Alliance's scholarships. The source says nothing about the
  firm's owners.
- **Clientele class.** A 1978 home-economics module on "Community Resources for Economically Depressed Areas"
  lists Pioneer Market as one of three supermarkets in central Echo Park. It notes that Pioneer takes food
  stamps and is open 24 hours. This describes the area and how people paid more than it labels the store's
  clientele, so it isn't coded.
- **Later-era descriptions.** A 2012 article says Little Joy had "in recent years taken turns catering to
  Spanish-speaking gay men, the post-college crowd and Dodger fans". That is decades after the directory years.

If you want a looser rule, for example coding "Spanish-language service" as a clientele indicator, it's a
one-line change per row. See `OPEN_QUESTIONS.md`.

## Context found that isn't in the directory

- "20 de Mayo", a Spanish-language newspaper edited by Abel Pérez, was at 1824 W Sunset, Suite 202, in 1980
  and 1983. Its sources are a 1980 newspaper list and a 1983 list of Hispanic publications. It falls between
  directory years.

## Files

- `research/findings.csv`: one row per researched entity, with the standard columns plus five demographic
  columns.
- `data/derived/listings_verified.csv`: listings plus `verified_*` columns, `evidence_url`, demographic columns
  and effective `*_final` columns.
- `data/derived/landuse_by_lot_verified.csv`: lot land use per year, recomputed. It adds a
  `{year}_verified_entities` column.
- `data/derived/summary_verified.json`: same shape as `summary.json`, plus `buckets_text_only`,
  `bucket_change` and `findings_by_status`.
- `scripts/apply_findings.py`: run it from the repo root after any change to findings.csv. With an empty
  findings file it reproduces `landuse_by_lot.csv` and `summary.json` exactly (checked).
