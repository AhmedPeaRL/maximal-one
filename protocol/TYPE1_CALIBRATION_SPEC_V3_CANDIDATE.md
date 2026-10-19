# HCM Type-I Calibration Specification V3 — Candidate for Review

**Status:** `CANDIDATE_PENDING_ATTRIBUTABLE_INDEPENDENT_STATISTICAL_REVIEW`  
**Freeze state:** `NOT_FROZEN`  
**Claim support:** `false`  
**Promotion authority:** `false`  
**Confirmatory execution authorized:** `false`  
**Single machine-readable scenario/design source:** `protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V3.json`

## Decision boundary

This file and its JSON matrix are a proposed aligned specification, not an approval or protocol freeze. An attributable independent statistical reviewer must approve the estimand, acceptance rule, scenario matrix, invalid-attempt policy, and computational feasibility before a freeze commit is designated. No confirmatory analysis or power phase is authorized by this draft.

## Target quantity

Estimate the Type-I rejection probability of the complete implemented upper-tail test under each of the nine declared stationary Gaussian AR data-generating processes (DGPs). The test compares the observed canonical spectral exponent with values from the declared stationary Gaussian AR(p) surrogate procedure. This is synthetic operating-characteristic evidence only; it does not establish that the AR null adequately represents the primary real series, and it does not support or falsify HCM by itself.

## Frozen-design candidate

- Sample size: 1,024 observations per synthetic series; DGP burn-in: 2,000.
- Outer attempts: 2,000 per scenario.
- Requested surrogates: 1,000 per outer attempt, matching the production setting declared in `core-scientific/strict_claim.json`.
- Nominal test level: 0.05; upper-tail Monte Carlo p-value `(exceedances + 1) / (valid_surrogates + 1)`; reject when `p <= 0.05`.
- Required scenarios: exactly the nine scenario IDs and coefficients in the JSON matrix.
- Acceptance rule: for every scenario, the one-sided 95% Wilson upper confidence bound on the empirical rejection probability must be `<= 0.075`. Two-sided Wilson intervals are reported for context but do not decide acceptance. The 0.075 tolerance is inherited from prior policy and requires explicit independent review; it is not a claim that the test is controlled at 0.05.
- No averaging across scenarios. Any required scenario failure fails the suite.
- Any invalid outer attempt, unresolved requested-surrogate shortfall, or incomplete run prevents a suite pass. Preserve every attempt, failure reason, and checkpoint; do not silently drop failures or count them as non-rejections.
- Deterministic per-replicate RNG: `SeedSequence([master_seed, stable_scenario_index, replicate_index, stream_id])`; stream 0 generates the DGP and stream 1 generates null surrogates. Results for a given scenario/replicate must not depend on shard order or scheduling.

## Production-equivalence gate

Before formal calibration, tests must verify that the calibration runner and production implementation use the same endpoint, open frequency band `(0.01, 0.05)`, Welch settings, AR orders 1–20, AIC, constant trend, stationarity constraint, common effective observations via hold-back, refitting of every surrogate, upper-tail direction, add-one p-value, rejection threshold, requested surrogate count (1,000), and invalid-result semantics. If exact equivalence cannot be established, the workflow must stop before simulation and label the run `IMPLEMENTATION_EQUIVALENCE_FAILED`.

## Required output per scenario

Record all requested outer attempt IDs; DGP and null seed identities; p-value where valid; requested and valid surrogate counts; refit and alpha-estimation failures; selected AR order; boundary indicator/fraction; invalid reason; rejection count/rate; two-sided 95% Wilson interval; one-sided 95% Wilson upper bound; code and dependency hashes; protocol hash; exact commit SHA; workflow run and attempt IDs; Python/platform versions; and status. A checkpoint is never a pass. Preserve all artifacts even if a scenario or job fails.

## Status semantics

- `CANDIDATE_PENDING_ATTRIBUTABLE_INDEPENDENT_STATISTICAL_REVIEW`: this draft only.
- `IMPLEMENTATION_EQUIVALENCE_FAILED`: no calibration simulation may proceed.
- `INCOMPLETE_NOT_A_PASS`: interrupted or incomplete run.
- `TYPE1_CALIBRATION_FAILED`: completed run with any failed required scenario or invalid attempt.
- `TYPE1_CALIBRATION_PASS_LIMITED_SYNTHETIC_SCOPE`: only if all predeclared criteria pass; still not proof of production-null adequacy, real-domain replication, or HCM.

## Explicitly not authorized

No power study before Type-I implementation equivalence and independent review; no alteration of historical results; no post-result threshold/scenario/estimator/order changes; no production-null freeze based on synthetic calibration alone; no promotion of HadCET, INDPRO, or cosmic rays; no claim-support or promotion flags set to true.

## Required independent review before freeze

The reviewer must be named and attributable and must document approval or requested revisions for: target quantity; the inherited 0.075 ceiling; one-sided Wilson rule; nine DGPs and their stationarity; zero-invalid-attempt policy; Monte Carlo precision and feasibility of 18,000,000 requested surrogate draws; implementation equivalence; reproducibility/seed design; and artifact-retention plan. An AI-assisted review is not a substitute for this independent human review.
