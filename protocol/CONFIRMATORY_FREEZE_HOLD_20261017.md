# Confirmatory Freeze Hold — 2026-10-17

**Decision ID:** `CONFIRMATORY_FREEZE_HOLD_20261017_V1`  
**Status:** `DO_NOT_RUN_CONFIRMATORY_ANALYSIS`  
**Claim status:** `UNDER_INVESTIGATION`  
**Claim support:** `false`  
**Promotion authority:** `false`

## Decision

The two prospective source candidates are recorded in `CONFIRMATORY_DOMAIN_CANDIDATE_REGISTRY_V1.json`, but the complete confirmatory protocol must not yet be labeled frozen. The stationary Gaussian AR(p), AIC-selected over p=1..20, remains exploratory because the independent null-adequacy and calibration review is unresolved. A domain list cannot repair an inadequate or unfrozen null protocol.

## Mandatory gates before any candidate endpoint is calculated

- [ ] Independent methods review defines the estimand and the temporal structure the null must preserve.
- [ ] Null-family choice is justified from scientific assumptions, not from HadCET/INDPRO or candidate alpha/p-values.
- [ ] Calibration suite and its overall acceptance rule are declared, including Monte Carlo uncertainty, type-I error, power, boundary-fit handling, and multiplicity across scenarios.
- [ ] Existing calibration failures are retained; no thresholds are changed post hoc to turn failures into passes.
- [ ] Exact endpoint formula, estimator implementation/version, frequency band, normalization, windowing, test direction/tail, surrogate count, random seed policy, and missingness rules are frozen.
- [ ] Domain candidate registry is committed before data acquisition/endpoint calculation.
- [ ] Exact raw source files, source vintage, timestamps, retrieval time, SHA-256, code commit, lockfile, and runtime versions are recorded before parsing or endpoint analysis.
- [ ] Independent reviewers complete the shared-nuisance and independence assessment for both candidates.
- [ ] Fresh clean-checkout validation and the existing eligibility/replication/promotion gates are run on the same exact commit.

## Fail-closed outcomes

- If the null-methodology review does not approve the protocol, do not compute confirmation endpoints.
- If either domain fails eligibility, provenance, frequency-resolution, or independence criteria, retain the failure and do not count it.
- If fewer than two domains pass all requirements, keep replication at `0/2` (or the actual independently verified count, if the gate reports a different one).
- A failed workflow is not permission to weaken the gate. A passing engineering workflow is not scientific claim support.

## Interpretation boundary

Even a future rejection of a declared stochastic null would only be evidence against that null under the frozen protocol. It would not alone establish HCM causation, consciousness, universality, mechanism, or a novel physical law.
