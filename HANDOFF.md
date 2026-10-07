# Handoff: research the businesses on Sunset Blvd 1400–2100

You're picking up a dataset built from Los Angeles reverse directories. Read `README.md` for the layout. This file is your task.

## Background

Corey Alt (USC Price, MPP/MUP) is doing a group project for a planning-theory-for-social-justice class. The project tells the story of Echo Park through the changing business mix on Sunset Blvd between 1400 and 2100. The directory pages for nine years have been transcribed (`data/transcriptions/`), every listing has been classified from its printed text alone, and each lot has a land use per year.

The text-only classification leaves gaps. Many listings give a name but no trade (“El Rodeo”, “Carmela's”), and the 1987 directory prints many businesses under an owner's name in capitals (“NHAN DUC DUONG”). Your job is to find out what these businesses actually were, using outside sources, and fold that back into the data without losing the original calls.

## The task

1. Work through `research/research_queue.csv` in priority order. One row is one **entity**: listings on the same lot with the same normalized name, across years.

   | priority | count | what it is | what to do |
   |---|---|---|---|
   | 1 | 37 | Unidentified business: name only, or a 1987 personal name in capitals | Full research. Most important. |
   | 2 | 33 | Low-confidence call (a guess from the name, from outside knowledge, or a likely-but-unconfirmed bar) | Full research. |
   | 3 | 20 | Medium: identified from the same name or phone at the same address in another year | Confirm or correct. |
   | 4 | 572 | High: the printed text names the trade | Lighter pass. Record a finding only when a source adds something (a sharper description, a contradiction). Leave the rest out of findings.csv. |

2. Record every result in `research/findings.csv`, one row per entity you checked. Never edit the `current_*` columns, the transcriptions or `listings.csv` by hand.

3. Write `scripts/apply_findings.py`. It should read `findings.csv` and add `verified_desc`, `verified_bucket`, `verified_use_type`, `verified_confidence` and `evidence_url` columns to the listings (via `entity_id`). Then recompute the lot land use and the bucket counts with the verified values where they exist. Write new files (for example `data/derived/listings_verified.csv`, `landuse_by_lot_verified.csv`, `summary_verified.json`) rather than overwriting the text-only versions. The before/after comparison matters for the project.

4. Finish with `research/RESULTS.md`: how many entities were resolved at each priority, and how the bucket counts by year changed (especially 1987, where 18 lots are unidentified). List anything that changed the story, such as a bucket that grew or shrank once unidentified businesses were resolved.

## `research/findings.csv` columns

| column | allowed values / format |
|---|---|
| entity_id | from the queue |
| finding_status | `confirmed` (source agrees with current call) · `corrected` (source shows a different type) · `identified` (was unidentified, now known) · `not_found` (searched, nothing usable) · `transcription_issue` (source suggests the name or address was misread; also log in `research/transcription_issues.csv`) |
| verified_desc | plain words, same style as `current_desc` (“Mexican restaurant”, “botanica / religious goods”) |
| verified_bucket | one of the 14 buckets below, exactly as spelled |
| verified_use_type | Business or Institutional (or Residential if the source shows it wasn't a business) |
| evidence_url | the page you actually read |
| evidence_title | page or document title |
| evidence_date | date of the source, or the date range it describes |
| evidence_quote | a short verbatim quote that ties the name to the address and the trade |
| source_type | newspaper · directory · photo archive · government record · book · website · other |
| confidence | high: the source names this business at this address (or with this phone) in the right era · medium: name and era match, address implied · low: suggestive only |
| researcher_notes | anything else, including what you searched when `not_found` |
| checked_on | YYYY-MM-DD |

## Evidence rules

Corey cares about these more than coverage. Saying less is better than a plausible guess.

- **Read the source itself.** A search-result snippet is not evidence. Fetch the page, find the passage and quote it. If the page won't load, is paywalled, or you can't confirm what it says, record `not_found` with a note. Don't fall back on the snippet or on your own general knowledge.
- **Match on more than the name.** A source counts only if it ties the business to this address, or to the phone number in `phones`, in roughly the right years. A same-named business elsewhere in LA, or decades off, is not a match. Many of these names are common (“El Rodeo”, “Los Pinos”).
- **One source per claim, cited.** Every `confirmed`, `corrected` or `identified` row needs `evidence_url` and `evidence_quote`.
- **Never use Grokipedia**, even as corroboration. Skip it in search results.
- **Outside knowledge isn't evidence.** A few current calls rest on general knowledge and are marked as such in `current_basis` (the Gold Room as a bar, White Cross as a drug chain, JWCH Institute as a nonprofit). Treat those as unverified until a source is found.
- If a fact you find contradicts something already in the data (a different address, a different year), note the conflict rather than silently picking one.

## Where to look

These are starting points. None has been checked yet for coverage of this stretch or for whether it's reachable from your session, so confirm before relying on one:

- Digitized newspapers (California Digital Newspaper Collection; LA Times archive if accessible; neighborhood papers. The directories list the *Parkside Journal* and *Northwest Leader* at 1727 Sunset.)
- LAPL digital collections and photo archives (storefront photos often show signage with the address)
- Other city directories and phone books on Internet Archive or HathiTrust for nearby years, which can show the same name with a trade
- City of LA historic resource surveys (SurveyLA / HistoricPlacesLA) and LA Conservancy pages for Echo Park buildings
- Historic Echo Park and similar local-history sites (check that they cite sources)
- For 1987, business registration data or news items from the 1980s; many of these are Mexican, Central American, Chinese, Vietnamese and Thai-owned businesses, so Spanish-language and community press may be the best record

The phone number in `phones` is a strong matching key when a source prints one. Phone exchange names (MU, MA, DU, NO) changed to digits in the early 1960s.

## Definitions

**Use types:** Business; Institutional (public agencies, churches, nonprofits, unions, veterans' and professional associations); Residential; Apartment building (a named building or APARTMENT heading); Vacant; Unknown.

**Lot land use (per year):** Commercial; Mixed-use (households plus business or institution on the same lot, counting ½ ¼ ¾ addresses); Residential – multifamily (named apartments, unit numbers, households at 2+ addresses on the lot, or 3+ households at one number); Residential – single-family; Institutional; Vacant; Unknown.

**Business buckets** (defined to map onto NAICS sectors):

| bucket | includes |
|---|---|
| Food stores | groceries and markets, meat/poultry/seafood, bakeries, delis, ice cream and candy, liquor stores, winery |
| Restaurants & bars | restaurants, cafes, pizzerias, donut shops, food stands, bars, taverns, cocktail lounges |
| Apparel, shoes & fabric | clothing, children's wear, shoe stores, fabric and yardage |
| General & specialty retail | department, variety and discount stores, jewelry, gifts, florists, toys, books, cameras, pets, pawnshop, unspecified “shoppes” |
| Home furnishings, hardware & appliances | furniture, hardware and paint, blinds and shades, glass, carpet, lighting, TV/radio, vacuums |
| Personal services | beauty salons, barbers, laundries and cleaners, tailors, dressmakers, shoe and watch repair, key shops |
| Auto sales & service | gas stations, repair, parts, tires, car wash; 1906 carriage maker |
| Health & medical | pharmacies, physicians, dentists, optometrists, chiropractors, clinics, labs |
| Finance, insurance & real estate | banks and S&Ls, credit union, loans and check cashing, insurance, real estate |
| Professional & business services | attorneys, accountants, tax prep, collections, advertising, travel agencies, parking, schools, utility office |
| Media, printing & entertainment | newspapers and publishers, printers, photo and portrait studios, record and video stores, theater |
| Light industrial, trades & wholesale | plumbing, carpentry and electrical shops, moving and storage, manufacturers and agents, wholesale, sign maker |
| Institutional & civic | post office, DWP, American Legion, Masonic lodge, church office, nonprofits, unions, associations |
| Unidentified business | listed as a business, but the type can't be determined |

If a business doesn't fit any bucket, use the closest one and flag it in `researcher_notes`. Don't add buckets; list proposals in `research/OPEN_QUESTIONS.md` for Corey to decide.

## How to work

- Commit `findings.csv` in batches (about every 25 entities) with a one-line message, so progress survives an interrupted session.
- Keep a short running log in `research/LOG.md`: what you searched for each batch, and which sources were useful or dead ends. That lets the next session skip what didn't work.
- Don't stop to ask questions. Make the reasonable call, note it in `research/OPEN_QUESTIONS.md`, and keep going. The exception is anything that would delete or overwrite existing data.
- If you notice a transcription error while researching (a misread name, a wrong number), don't fix the transcription. Log it in `research/transcription_issues.csv` (`listing_id, what's printed, what it should be, evidence`). The scans are in `sources/directory_scans/` if you need to check the page.

## Known open issues (don't try to resolve these unless a source happens to)

- On the north side in 1906, the Alvarado heading sits between 1945 and 2013, but by 1956 the north-side 2000s are east of Alvarado. A source showing 1906 north-side numbering near Alvarado would settle it.
- The 1968 directory prints EICKHOFF W at 1446 (likely 1546) and SUNSET CAMERA at 1643 (1634 in every other year).
