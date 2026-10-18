# Closure Decision and Freeze Reassessment — 2026-10-18

**Repository:** `AhmedPeaRL/maximal-one`  
**Decision ID:** `CLOSURE_FREEZE_REASSESSMENT_20261018_V1`  
**Decision type:** Evidence-gated scientific status decision  
**Status:** `HOLD_CONFIRMATORY_ANALYSIS`  
**Phenomenon review:** `PROVISIONAL_NOT_CLOSED`  
**Calibration acceptance:** `NOT_PASSED / SAME_COMMIT_RERUN_UNVERIFIED`  
**Independent secondary domains:** `0/2`  
**Confirmatory freeze:** `NOT_FROZEN`  
**Claim support:** `false`  
**Promotion authority:** `false`

## 1. Decision

Do not run a confirmatory endpoint analysis and do not promote the scientific claim.

Continue only:
1. outcome-blind methods review;
2. calibration implementation and simulation;
3. exact-commit reproducibility checks;
4. source-provenance and timestamp/missingness audits;
5. independent review of nuisance structure and domain independence;
6. documentation of acceptance and freeze decisions.

This decision does not say HCM is false. It says the current evidence is insufficient to authorize confirmatory inference.

## 2. Phenomenon and nuisance decision

The provisional operational target is **excess spectral persistence**: a prespecified `canonical_primary_alpha` higher than expected under an adequate, prospectively specified stochastic null representing the declared non-target temporal structure.

This wording is not yet closed. Before closure, an attributable independent methods reviewer must explicitly decide whether this is the intended estimand, rather than long-memory itself being the target. The reviewer must classify each relevant feature as:
- target;
- nuisance preserved under H0;
- nuisance modeled/conditioned on;
- measurement defect/exclusion; or
- unresolved.

The review must cover cadence/gaps, trend and regime changes, seasonality, short-lag dependence, marginal tails/outliers, heteroskedasticity, possible long-memory, source revisions, and estimator/model-selection uncertainty.

## 3. Evidence state at this decision

- The current stationary Gaussian AR(p), AIC-selected over p=1..20, is exploratory and not approved for confirmation.
- The primary capacity stream reports boundary fraction `0.937`; a separate stream reports `0.947`; the review threshold is `0.50`. Preserve each source-scoped estimate and its run identity. Do not average them or treat them as interchangeable.
- Historical Type-I counts are AR(1): 52/1000, AR(2): 60/1000, AR(5): 49/1000, AR(10): 73/1000. Under the currently recorded rule (two-sided 95% Wilson interval contains 0.05 and upper endpoint <= 0.075), AR(2) and AR(10) fail.
- The four historical scenario jobs were not established as one same-commit suite in the reviewed record.
- The V2 calibration plan lists no registered reference datasets and leaves future acceptance-rule fields unresolved.
- Candidate data structural validity does not establish scientific independence or replication. The currently documented replication count remains `0/2`.
- The current primary p-value `0.999001` does not reject the current exploratory null. It neither establishes nor falsifies HCM as a whole.

## 4. Acceptance decision

**Overall null calibration: NOT ACCEPTED for confirmatory use.**

Reasons:
1. Two of four recorded scenarios fail the declared historical rule.
2. Same-commit reproduction of all four scenarios is not established.
3. The expanded nuisance/scenario matrix is not yet implemented and accepted.
4. The prospective suite-level acceptance rule, power target, and invalid-fit policy have not received attributable independent approval.
5. No approved confirmatory null family exists.

Do not change the historical acceptance rule to make old results pass. Any new rule must be justified, reviewed, versioned, and committed before fresh runs; old results remain assessed under the rule that applied to them.

## 5. Reference data versus replication data

These are different evidence roles and must not be conflated.

### Calibration reference material
Known-data-generating-process simulations are required to estimate Type-I error and power because their generating truth is specified. Real-world reference series can test whether the method behaves sensibly under realistic nuisance structures, but they do not have known null truth and therefore cannot, by themselves, establish Type-I calibration.

### Replication domains
Replication requires untouched, eligible real-world domains selected before endpoint inspection, with reviewed source provenance, measurement validity, nuisance structure, and independence. A calibration series is not automatically a replication domain; a synthetic series never counts as real-domain replication.

### Candidate disposition
- HadUKP EWP: candidate only; structural checks were reported as passing, but independence, source vintage/homogeneity, exposure, and null compatibility remain unresolved.
- CPIAUCNS: retain the current snapshot and its missing value at `2025-10-01`; it remains blocked under the current completeness rule. Do not impute, interpolate, silently drop the month, or overwrite the snapshot.
- HadCET and INDPRO: prior endpoint-like exposure was recorded in the repository history; treat those results as exploratory/post-observation unless a reviewer approves a clearly separate, untouched future dataset and protocol.
- Cosmic-ray data: do not count until timestamp continuity, source provenance, and shared solar-cycle nuisance are resolved.

## 6. Freeze reassessment rule

The confirmatory protocol remains `NOT_FROZEN`. Freeze may be reconsidered only when every item in `CONFIRMATORY_FREEZE_REASSESSMENT_CHECKLIST_V1.md` is evidenced on an exact commit and the independent review is attributable.

A successful engineering workflow alone does not close a scientific review. No reviewer identity, signature, date, source hash, or approval may be inferred or backdated.

## 7. Required next decision

After the calibration and review evidence is complete, issue a new dated decision record with one of:
- `ACCEPTED_FOR_PROSPECTIVE_CONFIRMATION` — only if every gate passes;
- `REJECTED_FOR_CONFIRMATORY_USE` — if the candidate procedure is inadequate under the predeclared criteria; or
- `HOLD_INCOMPLETE_EVIDENCE` — if required evidence/review is missing.

The new decision must cite the exact commit, run IDs, artifacts and SHA-256 hashes, all failures, and the attributable reviewer disposition.

## 8. Interpretation boundary

Even a future rejection of one adequate, prespecified stochastic null is evidence against that null under that protocol. It does not by itself establish HCM causation, consciousness, universality, mechanism, or a new physical law.
