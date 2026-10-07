# Open questions for Corey

## Decisions made without asking (change any of these and I'll redo the affected rows)

1. **New demographic columns in `findings.csv`.** Per your request, findings.csv has five extra columns after
   `checked_on`: `owner_ethnicity`, `clientele_ethnicity`, `clientele_class` (upscale / mid / downscale),
   `demographic_evidence_url`, `demographic_evidence_quote`. Rules applied:
   - Filled only when a source says it outright (e.g. "Vietnamese-owned", "catering to Spanish-speaking ...",
     "working-class bar"), with the quote in `demographic_evidence_quote`.
   - Never inferred from a surname, a Spanish/Asian-language business name, or the trade.
   - Menu language or signage language (e.g. LAPL records noting "signs are written in Spanish") is recorded in
     `researcher_notes`, not as owner or clientele ethnicity. It says something about the intended market but
     isn't a statement about who owned or used the place.
   - A clientele description from a much later era (e.g. a 2012 article on a bar that was at the address in
     1973) goes in `researcher_notes` only, with its date, not in the demographic columns.
   A finding row can be added for a priority-4 entity just for demographic information if a source supplies it.

2. **Nonprofits that deliver health care** (JWCH Institute, 1987): kept in *Institutional & civic* per the
   HANDOFF definition (nonprofits), though *Health & medical* (clinics) is defensible. Tell me if you want
   nonprofit clinics moved.

## Bucket proposals

(none yet)

## Questions raised during the research

3. **Language of service as a clientele indicator?** Several sources show who a business was serving without
   saying it outright: a mostly-Spanish salon ad ("Estilista para hombres ... Abierto 7 Dias"), "Se Habla Español", a bilingual menu,
   Spanish signage in LAPL's 1980 photos, an ad placed in a magazine whose pages mix Spanish and English (Gráfica). Under rule 1 these are
   in `researcher_notes` only. If you want them coded, I'd suggest a separate column
   (`service_language`, e.g. "Spanish", "Spanish/English") rather than putting them in `clientele_ethnicity`.
4. **Area-level descriptions** (e.g. a 1978 teaching module listing Pioneer Market as a resource for
   "economically depressed areas" that takes food stamps): coded nothing for now. Code `clientele_class`
   from these?
5. **Owner-name business registrations without a trade.** Three 1987 capitals listings (1498 #4, 1513½,
   1529) are confirmed as businesses by city tax accounts but stay *Unidentified business*. They are recorded
   as `confirmed` against the current call. If you'd rather keep `confirmed` for trade confirmations only,
   these could be `not_found` with the registration in the notes; the counts don't change either way.
6. **Possible new bucket?** None needed so far. Polychrome/Westco (lithographic supplies distributor) went
   to Light industrial, trades & wholesale as the closest fit.
7. **Air transport.** Helitac Aviation (1910 Sunset, Suite 900, 1987) was a helicopter charter operator's
   office. No transportation bucket exists; filed under Professional & business services. A
   "Transportation" bucket (NAICS 48–49) would hold it, plus any moving/trucking now in Light industrial.
8. **Makers who sell mainly wholesale** (Helen's Natural Fruit Bars, 1484) kept in Food stores; move to
   Light industrial, trades & wholesale?
