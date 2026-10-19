# Prospective Type-I Calibration and Power Protocol — Draft V2

**Protocol ID:** `HCM_TYPE1_CALIBRATION_PREREGISTRATION_V2`  
**Status:** `DRAFT_PENDING_INDEPENDENT_REVIEW`  
**Freeze state:** `NOT_FROZEN`  
**Created (UTC):** `2026-10-19`  
**Reference commit reviewed:** `9fcd54bbc56ccf4c13b7b2020aa5f02b5f2b7ce5`  
**Claim support / promotion authority / confirmatory endpoint authorization:** `false`

## 1. Question and scope

Estimate the Type-I rejection probability of the **complete implemented test** under known stationary Gaussian short-memory DGPs. The operational null is the declared stationary Gaussian AR(p) surrogate procedure; the alternative is that the observed canonical spectral exponent exceeds the null-generated exponent distribution.

Freeze these properties: canonical frequency band `0.01–0.05`; AR(p) candidate order 1–20; AIC; constant trend; fixed hold-back so candidates use the same effective observations; stationary-root constraint; refit each surrogate using the same selection procedure; upper-tail p-value `(exceedances + 1)/(valid_surrogates + 1)`; rejection at p <= 0.05. Exact source, dependencies, configuration, and hashes must be recorded at freeze.

## 2. Implementation equivalence is mandatory

The existing calibration uses 200 surrogates while production requests 1000. No formal recalibration starts until the calibration runner uses the exact production setting and tests verify equivalence for endpoint, estimator, band, null function, surrogate count, selection, refitting, p-value rule, and invalid-result handling.

Record per outer replicate: p-value, requested and valid surrogate counts, refit failures, alpha-estimation failures, selected AR order, and boundary indicator. Invalid outer replicates must be counted and explained, never silently dropped. Use deterministic replicate-level seeds and test shard-order invariance.

## 3. Primary Type-I design

- 2,000 outer replicates per DGP.
- 1,000 requested surrogate draws per outer replicate, matching production.
- n = 1,024; Gaussian innovations; DGP burn-in = 2,000.
- Nominal test alpha = 0.05.
- Report empirical rejection rate, rejection count, two-sided 95% Wilson interval, one-sided 95% Wilson upper bound, invalid outer replicate count, surrogate-fit failures, selected-order distribution, and boundary saturation.
- Suite passes only if the one-sided 95% Wilson upper bound is <= 0.075 in **every** required DGP. Do not average across scenarios. Any required scenario failure means suite failure.
- No optional stopping. Incomplete runs are `INCOMPLETE`, not passes. Infrastructure reruns preserve earlier artifacts and record the reason.
- The 0.075 ceiling is inherited from current policy and must be explicitly approved by the independent reviewer before freeze; it must not be tuned using new results.

## 4. Scenario matrix

The exact coefficients and scenario IDs are in `TYPE1_CALIBRATION_SCENARIO_MATRIX_V2.json`. It includes the four historical scenarios, an additional moderate AR(1), AR(1) cases near the stability boundary, and AR(2) complex-root cases with radii 0.90 and 0.97. Each DGP must pass an automated stationarity/root check before simulation.

Only Gaussian innovations are in the primary matrix because the current null assumes Gaussian AR surrogates. Heavy tails, heteroskedasticity, breaks, seasonality, irregular sampling, and missingness are excluded unless a written scientific rationale and prospective amendment are committed before execution.

## 5. Power study

Run only after Type-I implementation equivalence is verified and the alternative generator is unit-tested. Proposed alternatives are ARFIMA(p,d,0) with AR(1) phi=[0.40] and AR(5) phi=[0.20,0.10,0.05,0.025,0.0125], for d=0.05, 0.10, 0.20. The expected low-frequency spectral slope contribution is approximately 2d, subject to finite-sample and estimator effects.

Use 1,000 outer replicates per alternative, n=1,024, and 1,000 surrogates per test. Report power, false-negative rate, and two-sided 95% Wilson intervals. Proposed targets: lower one-sided 95% Wilson bound >=0.75 for d=0.10 and >=0.85 for d=0.20. d=0.05 is reported as a weak-effect sensitivity result without a pass/fail threshold. Power cannot compensate for failed Type-I calibration. These proposed targets require independent reviewer approval before the power phase is frozen.

## 6. Failure policy

- Non-stationary DGP: stop and record implementation failure.
- Invalid outer replicates and invalid surrogate fits: record counts and reasons under a frozen rule.
- High selection of order 20 or surrogate boundary saturation: model-capacity warning requiring adequacy review; not evidence for or against HCM.
- No post-result changes to order cap, estimator, frequency band, tail, alpha threshold, or scenario definitions. Such changes require a new protocol version and fresh calibration.
- Preserve all historical outcomes and artifacts unchanged.

## 7. Provenance and freeze

Every artifact records exact commit SHA, workflow/run attempt, protocol hash, scenario/coefficient vector, seed schedule, Python/NumPy/SciPy/statsmodels versions, dependency-lock hash, source-code hashes, estimator/band/tail, rejection and failure counts, intervals, and `claim_support=false` / `promotion_authority=false`.

Current state remains `NOT_FROZEN`. Freeze requires implementation-equivalence tests, committed protocol and matrix, independent review with expertise/conflicts/date/rationale, hashes and freeze lock, completed acceptance record, passing Type-I and power criteria, and any required empirical reference registration. A CI pass alone is not scientific approval. No reviewer signature may be prefilled on another person's behalf.
