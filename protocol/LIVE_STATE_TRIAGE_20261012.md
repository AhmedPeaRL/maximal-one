# Live-State Triage — 2026-10-12

**Purpose:** Consolidate the currently supplied repository evidence without changing scientific decisions or interpreting diagnostic outputs as confirmation.

## Identity and computational execution

- Reported workflow commit: `3d649a34a6cdf63a05dd8b5aeed03ee4c4d94a5c`.
- The supplied identity-check snippets show `git rev-parse HEAD == GITHUB_SHA` for those workflow jobs.
- Python reported as `3.11.15`; `PYTHONHASHSEED=42` and numerical thread limits of one were set in the shown jobs.
- These facts support commit identity for those jobs and reduce some sources of runtime variation. They do **not** establish scientific validity, external replication, or universal determinism across hardware and environments.

## Current claim state

- `strict_claim.json` status: `UNDER_INVESTIGATION`.
- Primary stochastic-null p-value in the supplied contract evaluation: `0.999001`; the current specified stochastic null was not rejected.
- `claim support: false`; `final promotion allowed: false`.
- Permutation-null rejection is explicitly diagnostic-only and is not a substitute for rejecting an adequate temporal stochastic null.
- The AR(p) family remains exploratory/not frozen. Boundary saturation triggered a capacity review; historical results are not to be reused as confirmatory evidence after protocol changes.
- Independent secondary replication remains `0/2`; HadCET and INDPRO are candidates, not approved replications.

## Type-I calibration evidence supplied

- `gaussian_ar2_phi_0_45_minus_0_10`: 60/1000 rejections; empirical rate `0.060`; Wilson 95% interval `[0.046896..., 0.076471...]`; status `TYPE1_CALIBRATION_FAILED` under the current rule.
- `gaussian_ar10_low_order_coefficients`: 73/1000 rejections; empirical rate `0.073`; Wilson 95% interval `[0.058459..., 0.090809...]`; status `TYPE1_CALIBRATION_FAILED` under the current rule.
- The current acceptance rule requires the two-sided Wilson 95% interval to contain 0.05 and its upper endpoint to be at most 0.075. These scenarios do not pass that rule.
- Do not describe AR(10) as a true signal because of its tail probability, and do not change the production rule merely to make these runs pass. The result motivates a prospective null-adequacy/calibration review.
- `punycode` and `url.parse()` deprecation warnings during artifact upload are not, by themselves, evidence that the statistical calculation failed; the calibration failure is explicitly recorded in the artifact JSON and step exit code.

## Dataset eligibility

- Gate status: `REPLICATION_ELIGIBILITY_INSUFFICIENT`.
- Eligible independent replication domains: `0/2`.
- HadCET (4404 monthly rows) and INDPRO (1284 monthly rows) pass basic structural measurement checks in the supplied JSON, but provenance/independence/null-adequacy approval remains pending.
- CO2 (816 rows) is below the canonical replication minimum of 1024. Shorter datasets cannot be made replication-eligible by silently adapting the canonical segmentation.
- Cosmic-ray series: 3698 observations, but the supplied time-integrity audit reports 321 gaps/non-hourly intervals and a longest hourly contiguous run of 486; it is blocked as replication evidence.
- Derived, synthetic, shuffled, or null-control datasets do not count as independent real-domain replications.

## Reconciliation items that remain open

1. `0.937` versus `0.947` surrogate boundary fractions: retain `RECONCILIATION_REQUIRED`; do not overwrite one value with the other. Link each to exact run, commit, artifact, and generation settings.
2. The supplied `REPLICATION ELIGIBILITY DIAGNOSTICS` excerpt appears to associate some printed labels/reasons with the wrong named datasets compared with the committed JSON and the label function. Review the complete job log and exact uploaded artifact before making any code change.
3. Prior Actions artifacts must be audited to determine whether endpoint values were generated and whether they were viewed before the preanalysis decision. Computation and researcher exposure are separate facts.
4. HadCET/INDPRO technical preanalysis decisions are not yet complete. Do not calculate endpoint alpha or p-values until the protocol choices are complete and committed.

## Decision boundary

This file is a dated status summary, not a preregistration, not a new analysis, and not a scientific result. It grants no claim-promotion authority and does not modify the current gate.
