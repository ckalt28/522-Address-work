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
