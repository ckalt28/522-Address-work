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
- Context found but not tied to a directory listing: "20 de Mayo", a Spanish-language weekly (Abel Pérez,
  editor), at 1824 W Sunset #202 in a 1980 federal report and a 1983 RJR report. Not in the 1973 or 1987
  directory pages.
