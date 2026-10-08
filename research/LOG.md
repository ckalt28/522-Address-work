# Research log

## Source access (checked 2026-10-07, cloud session with Full network access)

Usable:
- **Internet Archive full-text search** (`archive.org/services/search/beta/page_production/?service_backend=fts&page_type=search_results`).
  Searches OCR text of trade journals, magazines, some directories and the LA Times (IA's LA Times run ends 1950,
  so it only helps 1906/1927). Ranking is loose; quoted phrases are not strictly enforced, so every hit is
  re-read in the item's `_djvu.txt` before it is used. No 1950s–80s LA phone books or criss-cross directories
  on IA (only a 1939 and a 1951 "Los Angeles extended area" phone book).
- **LAPL TESSA** (photos + Menu Collection). The public site redirects to `tessa2.lapl.org`, whose server omits
  its intermediate certificate; verified by adding the "SSL.com TLS Issuing RSA CA R1" intermediate (from crt.sh)
  to the CA bundle. TLS verification was never disabled. API at `/digital/api/` (robots.txt disallows the HTML
  `/digital/search/` pages, not the API; queries are throttled to its 1 s crawl delay).
  Useful: Menu Collection (street addresses on menus), William Reagh 1963/1980 Echo Park storefronts,
  Roy Hankey 1976 Echo Park slides. Most photos give a block or cross street, not a number.
- **Web search** works for current businesses but rarely reaches 1950s–80s small businesses.

Not usable:
- **CDNC (cdnc.ucr.edu)**: Cloudflare bot challenge, also blocks headless Chromium. Not bypassed.
- **HathiTrust (babel.hathitrust.org)**: 403. In-copyright items would be snippet-only anyway.
- **HistoricPlacesLA (historicplacesla.org)**: serves a `*.azurewebsites.net` certificate (hostname mismatch); can't be verified, so not read.
- **latimes.com** (incl. 1985+ archive articles): opts out of Anthropic's crawler; the search tool refuses the domain. Not fetched by other means.
- **UCLA Digital Library** (LA Times photo archive): robots.txt disallows `anthropic-ai`. Not used.
- **Calisphere**: robots.txt disallows `/search/`; its LAPL items are reached through TESSA instead.
- **OpenStreetMap** `start_date` on Sunset Blvd buildings = building year from the LA County assessor import, not a business's opening date. Don't cite it for a business.

Added later in the session (also usable):
- **CA ABC License Query System** (abc.ca.gov license lookup; results are rendered by JavaScript, so read with
  headless Chromium). Search by business address `NNNN W SUNSET BLVD`, then open each license for owner,
  business name, license type (40 beer bar, 41 beer & wine restaurant, 47 full-liquor restaurant,
  48 bar, 20/21 off-sale market/liquor store) and original issue date. Cancelled licenses are kept, but
  nothing earlier than about 1977–1980 shows up, so it helps the 1987 listings, not earlier years.
- **City of LA Office of Finance business-tax registrations** (data.lacity.org dataset `r4uk-afju`, "Listing of
  All Businesses", includes closed accounts). 883 accounts on W Sunset 1400–2100 (ZIP 90026). Gives
  owner/business name, DBA, NAICS and location start date. Most pre-1990 accounts have no NAICS, so they
  confirm a business existed at the address but not its trade. Many start dates are 01-01 (likely approximate).
  Citable per account: `https://data.lacity.org/resource/r4uk-afju.json?location_account=...`
- **IA yearbook ads** (classmates.com yearbooks on IA: Our Lady of Loretto, Bishop Conaty, Cathedral HS).
  Local merchants' ads carry address and phone. Found Carmela's Fashions (1511, 1972).

## Batch 1 (priority 1–3 start), 2026-10-07
- Searched each p1–3 entity in IA full text by address ("NNNN Sunset", "NNNN W. Sunset"), phone (exchange
  name and digits) and name; by name and address in TESSA; by address in ABC; and against Office of Finance
  accounts. IA's search backend often returned 502 errors; failed queries are retried before an entity is
  marked not_found.
- Useful: ABC (Gold Room, El Prado, Nikola's, Pescado Mojado), Office of Finance (four 1987 capitals names
  confirmed as businesses; Zozula-Vasquez Income Tax), LAPL menus (Pescado Mojado), IA trade journals
  (Polychrome / Westco Litho at 1402), IA yearbook ad (Carmela's Fashions).
- Dead ends: general web search for 1950s–80s names (returns only current businesses); TESSA photos are
  rarely captioned with a street number.
- Context found but not tied to a directory listing: "20 de Mayo", a newspaper at 1824 W Sunset: listed as
  "20 de Mayo Newspaper, 1824 W. Sunset Blvd." in the newspaper list of an ERIC program report (Aug 1980,
  archive.org/details/micro_IA41153518_0192), and as "20 De Mayo, 1824 Sunset Blvd. Suite 202 ... Editor:
  Abel Perez" in a 1983 RJR list of Los Angeles Hispanic publications
  (archive.org/details/6162278-1983-11-RJR-Social-Responsibility-Interim-Report). Not in the 1973 or 1987
  directory pages.

## Batch 2 (priority 1–3 continued, some priority 4), 2026-10-07
- Yearbook scan: streamed the OCR text of every 1950–92 yearbook on IA from schools named Cathedral, Belmont,
  Marshall, Lincoln, Franklin, Sacred Heart, Bishop Conaty, Loretto, Immaculate Heart, LA High, Cantwell, St.
  Bernard (about 400 items; many are same-named schools elsewhere, filtered out by requiring an LA context
  near the address). 13 ads on this strip: Sam's Service Station 1475 (1959), Henry's For Men 1602 (1958),
  Uncle Ben Furniture 1555 (1969), Brite Spot 1918 (1969), Parsons' Stationers 1723 (1969), Carmela's
  Fashions 1511, M. Dolores Garcia bookkeeping 1463, Pioneer 1601, Nayarit 1822, Valdes sewing center 1714
  (all 1972), Pioneer (1981), Gerry's Dept Store 1554 (1987, 1988). OCR often runs neighbouring ads together
  (e.g. a "Japanese Realty Assn" ad with its own address on W Jefferson sits beside the 1714 ad), so each ad
  is re-read before use.
- Trade/consumer magazines on IA were the best source for 1950s–70s owners: The Cattleman 1961 (Winston
  Schaefer Inc = owner of Pioneer Supermarket), Gráfica 1977 (Gold Room Cocktail Lounge, same phone as 1968/73).
- Dead ends / limits: many IA books are lending-only and return 401/403 for their text (Paul Wallach's 1990
  restaurant guide, a 1969 "Business Directory and Buyers Guide" with Nikolas Inc, the 1981 Cal State LA alumni
  directory with Glynn Boxer & Phillips at 1824 Sunset, a 1999 trade-associations directory). Their search
  snippets are not used as evidence; they are listed in notes as unread leads.
- A 1987 Haines criss-cross directory ("CA Los Angeles County West Suburban 1987") is in IA's full-text index
  but the item itself is dark (404). It covers the West Suburban area anyway; no central-LA Haines volume found.

## Priority 1–3 wrap-up and priority 4 start, 2026-10-07
- All 90 priority 1–3 entities have a row (21 resolved, 69 not_found with what was searched).
  `apply_findings.py` and `RESULTS.md` written; the script reproduces the text-only outputs exactly when
  findings.csv is empty.
- Priority 4 approach: rows only where a source adds something. Sources so far: yearbook ads (Henry's For
  Men, Capri Beauty Salon), the 1978 ERIC module (Pioneer, 24 hours), LA Office of Finance titles (DDS, DPM,
  KFSG radio, Taix). Running: IA full text for every p4 address, phone and multi-word name (1,432 queries;
  slow, roughly 1–3 per minute); TESSA name search at 1 query/s.
- Note: ABC license 187442 (Dos Leos Inc, type 48 bar, 1455 W Sunset) was issued and canceled the same day,
  14-APR-1987; the 1987 directory lists nothing at 1455. Not recorded (no entity; may never have operated).
- TESSA name search for p4 business names finished: only Pioneer Super Market photos (1934–47, no new
  information for the listed years), Angelus Temple photos (temple on Glendale Blvd, not the 1910 Sunset
  offices), a 1976 Burrito King / liquor store photo at 2109 Sunset (outside the 1400–2100 range), and the
  1980 street photo at 1547. Nothing recorded from it.

## Priority 4 bulk search, 2026-10-07/08
- IA full text for all p4 phones, multi-word names and lot addresses (1,266 queries, ~25 s each on IA's
  side). 140 failed with backend errors on the first pass and are being retried at lower concurrency.
- Useful: KPFK Folio classified ads (Helen's fruit bars), a 1974 gay men's magazine dining column
  (Barragan's Cafe), the 1994 World Directory of Seafood Importers (Wing Lee Shrimp), Infosystems 1978
  masthead (Hitchcock Publishing), 1989 Helicopter Annual (Helitac), California Librarian 1974 ad (Libreria
  Mexico). Lending-only and so not used: The Flavor of Los Angeles (1982; Madrid "Cuban and Spanish",
  Celaya Bakery, Tonita's, Roy's Meat Co), Los Angeles Underground Gourmet (1970), Paul Wallach's guide
  (1990), The Organic Directory (1974), Ethnic Information Sources (1983), Frommer's (1999/2004).
- Context not tied to an entity: Coin M-Porium, a coin dealer at 2034 Sunset in 1962–63 numismatic
  periodicals (between directory years).
- The container restarted on 2026-10-08; nothing was lost (outputs were in the scratchpad and the repo was
  pushed).
