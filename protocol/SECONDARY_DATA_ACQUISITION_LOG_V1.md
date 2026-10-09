# Secondary Data Acquisition Log V1

## Status

- Protocol status: `PRE_CONFIRMATORY_CANDIDATE_REVIEW`
- Scientific claim status: `UNDER_INVESTIGATION`
- Confirmatory status: `NOT_READY`
- Approved secondary domains: 0
- Claim-promotion authority: NONE

This log records source acquisition and data-integrity review. It does not establish scientific replication.

---

## Candidate A — FRED DEXUSEU

- Candidate ID: `fred_dexuseu`
- Source URL: `https://fred.stlouisfed.org/series/DEXUSEU`
- Raw snapshot path: NOT_YET_CREATED
- Retrieval date and time (UTC): NOT_YET_RECORDED
- Original filename: NOT_YET_RECORDED
- SHA-256: NOT_YET_COMPUTED
- Parsed dataset path: NOT_YET_CREATED
- Observation count: NOT_YET_MEASURED
- First and last observation dates: NOT_YET_AUDITED
- Duplicate dates: NOT_YET_AUDITED
- Out-of-order dates: NOT_YET_AUDITED
- Missing source-calendar sessions: NOT_YET_AUDITED
- Units and source metadata: NOT_YET_VERIFIED
- Sampling interpretation approved: NO
- Endpoint computed before eligibility decision: MUST REMAIN NO
- Replication eligibility: FALSE

---

## Candidate B — USGS daily streamflow

- Candidate ID: `usgs_daily_streamflow`
- Documentation URL: `https://waterservices.usgs.gov/docs/dv-service/`
- Selected site ID: NOT_YET_SELECTED
- Parameter code and units: NOT_YET_SELECTED
- Site-selection basis: MUST USE SOURCE COMPLETENESS AND DATA QUALITY, NOT SPECTRAL RESULTS
- Raw source response path: NOT_YET_CREATED
- Retrieval date and time (UTC): NOT_YET_RECORDED
- Original filename: NOT_YET_RECORDED
- SHA-256: NOT_YET_COMPUTED
- Parsed dataset path: NOT_YET_CREATED
- Observation count: NOT_YET_MEASURED
- First and last observation dates: NOT_YET_AUDITED
- Duplicate dates: NOT_YET_AUDITED
- Out-of-order dates: NOT_YET_AUDITED
- Missing daily observations: NOT_YET_AUDITED
- Quality flags and units: NOT_YET_VERIFIED
- Endpoint computed before eligibility decision: MUST REMAIN NO
- Replication eligibility: FALSE

---

## Mandatory acquisition rules

1. Preserve the original source response without editing it.
2. Record retrieval time, source URL, query parameters, source identifier, units, and observation window.
3. Compute SHA-256 for the preserved source snapshot.
4. Keep raw source data separate from parsed and analysis-ready files.
5. Do not impute, interpolate, pad, or concatenate across missing observations to meet a minimum length.
6. Evaluate sampling semantics and eligibility before calculating or inspecting the scientific endpoint.
7. Record failed checks and retain excluded candidates in the audit trail.
8. Do not change thresholds after viewing endpoint results to make a candidate pass.
9. A source record or checksum alone does not establish provenance authenticity, independence, or replication success.
10. Any protocol amendment made after examining existing endpoint results is exploratory and requires a documented fresh validation plan.

---

## Decision rule

A candidate remains NOT_APPROVED until source provenance, timestamp integrity, sampling compatibility, minimum valid length, nuisance structure, and independent-domain status have been explicitly reviewed.

Passing data-integrity checks does not itself establish replication. The declared null-adequacy and scientific-claim gates remain independently binding.
