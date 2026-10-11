# Secondary-Domain Preanalysis Completion Guide — V1

This guide complements `SECONDARY_DOMAIN_PREANALYSIS_DECISION_TEMPLATE_V1.md`; it does not replace that file and does not constitute approval.

## Mandatory honest fields

- Prior exposure: answer `YES`, `NO`, or `UNKNOWN` based on what actually happened. If any endpoint alpha, endpoint plot, p-value, or outcome-driven exploratory analysis has already been inspected for either candidate, record `YES` and describe it. Do not use `NO` for analyses that were viewed but not remembered precisely; use `UNKNOWN` if that is genuinely the best answer and explain why.
- Status: if endpoint exposure preceded the current decision, describe the candidate analysis as exploratory/post-observation. A later commit cannot retroactively make it preregistered.
- Independence: provide a domain-specific rationale, identify plausible shared causes/nuisance structure, and seek an independent review. Different CSV filenames or different measurement scales do not by themselves establish independent replication.
- Estimator and null: reference the exact current estimator/protocol version and status; do not imply the AR(p) null is confirmatory while its own registry says it is unfrozen.

## HadCET decision

Choose the primary start date using a source-backed measurement/provenance rule, not the alpha result. Cite the source/header that motivates the precision boundary or keep the full record as primary and declare any objectively justified alternatives as sensitivity analyses. Document sentinel values, missing/gap handling, cadence, source snapshot and raw/parsed hashes. The committed series ends at 2025-12; the raw 2026 `-99.9` values are sentinel values, not observations.

Do not present the selection of a later start as automatically more valid: the rule and rationale have to be stated before endpoint inspection, and the early period cannot be removed merely because its estimate is inconvenient.

## INDPRO decision

Choose one primary transformation by the scientific quantity intended to be measured, not by which transformation gives a desirable alpha or p-value:

- `RAW LEVEL`: models persistence in the index level but may confound long-run growth/trend with the proposed spectral signature.
- `LOG LEVEL`: preserves a level-based estimand on the log scale; it does not remove a stochastic or deterministic trend by itself.
- `LOG DIFFERENCE`: targets approximately proportional month-to-month changes/growth and loses the first observation; this is a different scientific estimand from persistence in levels.
- `OTHER`: specify an exact reproducible formula and reason before computing endpoint results.

Record treatment of missing/zero/negative values, differencing loss, preprocessing/seasonal adjustment, and every sensitivity transformation in advance. Do not silently switch after observing results.

## Approval status

Until an authorized, independent review has examined the completed decisions, source provenance, endpoint/null identity, nuisance structure and dataset independence, keep both candidates `NOT APPROVED FOR REPLICATION`. The workflow's current zero-of-two eligible independent secondary domains is a valid blocking outcome; do not edit eligibility flags to make the gate pass.
