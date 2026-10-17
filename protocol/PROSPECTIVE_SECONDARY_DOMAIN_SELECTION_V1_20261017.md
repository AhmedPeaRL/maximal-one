# Prospective Secondary-Domain Selection — V1

**Decision record date:** 2026-10-17  
**Status:** `DOMAIN_CANDIDATES_SELECTED_BY_SOURCE_CRITERIA; NOT_YET_APPROVED_FOR_REPLICATION`  
**Endpoint values inspected for these candidates:** No endpoint analysis has been run by this selection record. This is a procedural declaration; it must be checked against the repository and acquisition logs before final sign-off.  
**Claim support / promotion authority:** `false`

## 1. Selection objective

Select two *new candidate domains* for prospective evaluation without inspecting alpha, p-values, endpoint plots, or any other candidate outcome. Selection is based only on source identity, documented monthly cadence, historical coverage sufficient in principle for the existing 1,024-observation replication minimum, and a different measured quantity from the primary sunspot series.

This document does not assert that either candidate is already a valid independent replication. The candidate data must not be downloaded into the analysis pipeline, transformed, or passed to an endpoint estimator until the null-methodology and calibration hold is resolved and a complete protocol is frozen.

## 2. Predeclared candidates

### Candidate A — UK England and Wales precipitation (HadUKP EWP)

- **Source:** UK Met Office Hadley Centre, HadUKP.
- **Series:** England and Wales Precipitation (EWP), monthly totals.
- **Source page:** https://www.metoffice.gov.uk/hadobs/hadukp/
- **Data/download page:** https://hadleyserver.metoffice.gov.uk/hadobs/hadukp/data/download.html
- **Documented coverage:** monthly EWP series begins in 1766; official format documentation identifies monthly totals and sentinel missing values `-99.9`.
- **Source-based reason for selection:** official source, monthly series, long historical coverage that can exceed the current 1,024-month structural minimum, and a precipitation measurement distinct from sunspot number and from HadCET temperature.
- **Predeclared data handling:** preserve the exact raw download and source page; hash the raw file before parsing; expand monthly rows in chronological order; treat `-99.9` as missing, never as a measurement; do not interpolate missing months; document revisions and all gaps.
- **Nuisance/independence risk:** rainfall is a climate variable and may share climate drivers or possible solar-related forcing with the primary sunspot domain and with HadCET. Different variable/source does not itself prove independence. An independent reviewer must assess whether this is adequate for the stated replication claim.
- **Current decision:** `CANDIDATE_ONLY; NOT_APPROVED`.

### Candidate B — U.S. CPI, all urban consumers, not seasonally adjusted (CPIAUCNS)

- **Source:** U.S. Bureau of Labor Statistics, distributed through FRED.
- **Series ID:** `CPIAUCNS`.
- **Source page:** https://fred.stlouisfed.org/series/CPIAUCNS
- **Table data:** https://fred.stlouisfed.org/data/cpiaucns
- **Documented coverage/frequency:** monthly from 1913-01; FRED metadata showed 1,365 observations through 2026-09 as of the 2026-10-16/17 review period. Recheck coverage at acquisition time without inspecting the endpoint.
- **Source-based reason for selection:** documented official BLS source, monthly cadence, sufficient historical length in principle for the 1,024-observation minimum, and an economic price-index measurement distinct from sunspot number and from industrial production.
- **Predeclared data handling:** preserve the exact FRED/BLS vintage and retrieval date; record revision/vintage policy; hash the raw download before parsing; enforce unique increasing monthly timestamps; do not interpolate missing months; do not silently change between not-seasonally-adjusted and seasonally adjusted series.
- **Transformation decision:** no transformation is authorized yet. Raw level, log level, and differenced inflation measure different estimands. An independent methods review must choose and justify one primary transformation before endpoint analysis; alternatives, if any, must be declared sensitivity-only in advance.
- **Nuisance/independence risk:** CPI can share macroeconomic, energy-price, policy, war, and climate-related drivers with industrial production and other systems. Its suitability as an independent replication domain relative to the sunspot primary endpoint requires explicit review.
- **Current decision:** `CANDIDATE_ONLY; NOT_APPROVED`.

## 3. Outcome-blind eligibility and rejection rules

The following rules are fixed before candidate endpoint analysis:

1. No alpha, p-value, endpoint plot, or endpoint summary may be computed or inspected for either candidate until a complete confirmatory protocol is committed and the null-methodology hold is lifted.
2. A candidate must pass source identity, raw-file hash, timestamp/order, monthly cadence, missingness, minimum length, estimator resolution, and provenance checks.
3. The candidate must pass an independent scientific assessment of shared nuisance structure and independence from the primary domain. Data-source difference alone is insufficient.
4. The existing 1,024-observation replication minimum and current frequency-resolution rule remain unchanged unless an independent, outcome-blind methods review proposes a prospective amendment. No post-result threshold changes are permitted.
5. The same declared endpoint, null family, alternative direction, test tail, and inferential rule must be applied across the primary and replication domains. If the scientific estimand requires a different transformation or physical-frequency band, that change must be justified and frozen before any confirmation endpoint is calculated.
6. If either candidate fails, record the failure and keep it excluded. Do not replace it because its result is inconvenient. A replacement requires a documented source-based selection rule applied without endpoint outcomes, before analyzing the replacement.
7. `0/2` remains `0/2` unless two independent real domains pass all declared gates and show the required domain-level evidence.

## 4. Explicit protocol boundary

The domain identities are selected here, but the *full confirmatory protocol is not frozen*. The current AR(p) null is exploratory and its calibration review remains unresolved. Therefore this record does not authorize endpoint computation, replication credit, claim support, or promotion.

## 5. References consulted for source metadata only

- Met Office HadUKP overview, including EWP coverage from 1766: https://www.metoffice.gov.uk/hadobs/hadukp/
- Met Office HadUKP download/format pages, including monthly totals and `-99.9` missing sentinel: https://hadleyserver.metoffice.gov.uk/hadobs/hadukp/data/download.html and https://www.metoffice.gov.uk/hadobs/hadukp/data/data_format.html
- FRED CPIAUCNS table data, BLS source, monthly frequency, and 1913 start: https://fred.stlouisfed.org/data/cpiaucns

These references were used for source and coverage metadata, not to select candidates based on endpoint results.
