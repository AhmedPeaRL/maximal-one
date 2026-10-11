# Secondary-Domain Preanalysis Decision Template — V1

**Status:** incomplete template; not a registration, approval, or replication claim. Complete and commit this document before computing or inspecting any endpoint `alpha` for HadCET or INDPRO. Record any prior endpoint exposure honestly; do not label an already observed decision preregistered.

## A. Decision record

- Decision date (UTC): `TO_BE_COMPLETED`
- Commit SHA containing this completed decision: `TO_BE_COMPLETED`
- Authors/reviewers: `TO_BE_COMPLETED`
- Were endpoint values, alpha estimates, p-values, or endpoint plots inspected for these candidates before this decision? `YES / NO / UNKNOWN`
- If yes or unknown, describe exposure and classify the analysis as exploratory or post-observation: `TO_BE_COMPLETED`

## B. Shared confirmatory endpoint and null

- Exact endpoint formula and estimator version: `TO_BE_COMPLETED`
- Frequency band and normalization: `TO_BE_COMPLETED`
- Same endpoint direction across primary and secondary domains: `TO_BE_COMPLETED`
- Null family, parameter fitting, order-selection rule, and calibration status: `TO_BE_COMPLETED`
- Current status of AR(p) null: `EXPLORATORY / NOT FROZEN`; no confirmatory promotion until the declared adequacy review passes.
- Primary-domain shared nuisance structure and planned controls: `TO_BE_COMPLETED`

## C. HadCET monthly series

Known source facts to preserve:

- Source: UK Met Office HadCET monthly mean Central England temperature.
- Raw source series is composite: early historical record is attributed in its header to Manley (1974), with later data attributed to Parker et al. (1992).
- The committed parsed file has 4404 monthly rows from 1659-01 through 2025-12; its raw source includes future-year sentinel values that must not be interpreted as actual observations. The parsed cutoff excludes the 2026 `-99.9` sentinel rows.
- Early observations have coarser numerical precision. This is a measurement/provenance consideration, not evidence for or against the hypothesis.

Predeclare the analysis-window rule using source provenance or a measurement-quality criterion, not alpha:

- Chosen window start: `TO_BE_COMPLETED`
- Objective source/precision rule and supporting citation: `TO_BE_COMPLETED`
- Whether the full window and alternate windows will be reported as sensitivity analyses: `TO_BE_COMPLETED`
- Rule for missing values, gaps, and sentinel rows: `TO_BE_COMPLETED`
- Climate/solar forcing and other shared nuisance review: `TO_BE_COMPLETED`
- Why this domain is independent enough to count as replication rather than merely a different dataset: `TO_BE_COMPLETED`
- Approval decision and independent reviewer: `PENDING`

Do not choose the window that yields the most favorable alpha. If multiple windows are analyzed, specify them now and treat the resulting multiplicity transparently.

## D. FRED INDPRO monthly series

Known source facts to preserve:

- Source: FRED INDPRO, Industrial Production: Total Index, seasonally adjusted, index 2017=100.
- The committed parsed series has 1284 monthly rows from 1919-01 through 2025-12.
- The level has a large long-term change, so the raw level, log level, log difference/growth, and detrended residuals are not interchangeable endpoints.

Predeclare exactly one primary transformation and its scientific rationale before computing endpoint alpha:

- Primary input: `RAW LEVEL / LOG LEVEL / LOG DIFFERENCE / OTHER (SPECIFY)`
- Mathematical transformation, including handling of nonpositive values and initial lost observations: `TO_BE_COMPLETED`
- Why this transformation matches the stated scientific estimand rather than optimizing the result: `TO_BE_COMPLETED`
- Whether alternatives will be sensitivity-only, and how multiplicity will be reported: `TO_BE_COMPLETED`
- Seasonal adjustment status and other known preprocessing: `TO_BE_COMPLETED`
- Independence review against the sunspot primary domain, including energy use, policy, wars, climate, and possible solar-related covariation: `TO_BE_COMPLETED`
- Why this domain is independent enough to count as replication: `TO_BE_COMPLETED`
- Approval decision and independent reviewer: `PENDING`

A transformation decision changes the series and can change the scientific question. Do not quietly switch transformations after seeing alpha or p-values.

## E. Shared eligibility and promotion rule

- Measurement eligibility rule: `TO_BE_COMPLETED`
- Estimator precision/segment-coverage rule, with justification: `TO_BE_COMPLETED`
- Provenance verification rule: `TO_BE_COMPLETED`
- Independence review rule: `TO_BE_COMPLETED`
- Null adequacy/calibration prerequisite: `TO_BE_COMPLETED`
- Treatment of failed/ineligible candidates: retain the record and reason; do not replace them after seeing outcomes without documenting the selection procedure.
- Current decision for both candidates: `NOT APPROVED FOR REPLICATION`

## F. Sign-off

- Decision complete before endpoint computation: `YES / NO`
- Reviewer sign-off: `TO_BE_COMPLETED`
- Any post-observation amendments: `TO_BE_COMPLETED`
- Claim/promotion authority granted by this template: `FALSE`
