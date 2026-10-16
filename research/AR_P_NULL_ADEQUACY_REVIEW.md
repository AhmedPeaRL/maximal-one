# AR(p) Null-Adequacy Review — Working Record

## Status

`REVIEW_REQUIRED — NOT_APPROVED_FOR_CONFIRMATORY_USE`

This document records a methodological review. It is not an external peer review, a preregistration, or evidence supporting the scientific hypothesis.

---

## Reviewed state

* Repository: `AhmedPeaRL/maximal-one`
* Reviewed commit: `958fd9e624ec1ae19a435956fb1e6cc123a14d74`
* Workflow run: `38906222470`
* Relevant job: `116990344416`
* Claim status: `UNDER_INVESTIGATION`
* Claim support and promotion authority: false

Historical results must retain their own run, commit, seed, input hash, and configuration.

---

## Findings

### 1. Unequal estimation samples

The reviewed `analysis/null_order_capacity_audit.py` calls `AutoReg` without an explicit `hold_back`. Candidate AR orders may therefore be compared using different effective observations.

The repaired diagnostic should use a common `hold_back` at least as large as the largest candidate order. For the declared 20/40/60 capacity comparison, use 60 across all candidate orders and caps.

This is a post-observation diagnostic repair, not preregistered evidence.

Reference: https://www.statsmodels.org/stable/generated/statsmodels.tsa.ar_model.AutoReg.html

### 2. Ljung–Box degrees of freedom

The reviewed audit calls `acorr_ljungbox` without `model_df`. The repaired diagnostic should use the selected AR order as `model_df` and only interpret requested lags for which `lag - model_df > 0`.

If no requested lag is eligible, record `NOT_EVALUABLE`; do not treat the result as a pass.

Reference: https://www.statsmodels.org/stable/generated/statsmodels.stats.diagnostic.acorr_ljungbox.html

### 3. Historical boundary saturation

The current claim specification records 937/1000 valid surrogate refits selecting p=20 under a prior configuration, with a 0.50 review trigger.

Preserve this historical result as a diagnostic warning with its original provenance. Do not overwrite it or imply that the repaired 20/40/60 audit is the same experiment.

The repaired audit cannot, by itself, approve the AR family as a confirmatory null.

### 4. Workflow blocker

The reviewed workflow reports `insufficient genuinely independent secondary real domains: 0 < 2`. The run also records `confirmatory_protocol_not_frozen` as the reason candidates were excluded.

Do not bypass this condition by relabeling datasets, lowering sample thresholds, or counting synthetic, shuffled, derived, or null datasets as independent real-domain replications.

### 5. P-value separation

The workflow reports permutation-null rejection while also explicitly reporting that the appropriate stochastic short-memory null was not rejected.

The printed `P-value: 0.0002` must not be treated as the primary stochastic-null p-value without tracing its source field and test identity. A permutation-null result does not replace the primary temporal-null test.

---

## Required review ledger

* [ ] Repaired common-sample capacity audit completed and artifact preserved.
* [ ] AIC selection stability and boundary behavior evaluated at every declared cap.
* [ ] Residual ACF/PACF reviewed.
* [ ] Ljung–Box diagnostics use adjusted degrees of freedom; non-evaluable lags are explicitly marked.
* [ ] Stationarity and parameter stability assessed, including failed fits and exclusions.
* [ ] Surrogate generation, burn-in, refitting, and effective sample size audited.
* [ ] Type-I calibration reviewed under the existing acceptance rule.
* [ ] Failed calibration scenarios remain visible and are not made to pass by retrospective threshold changes.
* [ ] Sensitivity to series length and estimator configuration evaluated using declared scenarios.
* [ ] Null-family selection rule specified without reference to future confirmation outcomes.
* [ ] Independent technical review and its scope recorded.

---

## Decision

Until all required items have documented outcomes:

`confirmatory_null_approved = false`

No expansion of the AR order range, replacement of the null family, endpoint change, tail switch, or threshold adjustment is allowed merely to obtain a smaller p-value.

Failure to reject an adequate stochastic null is a valid scientific result. This review neither establishes nor falsifies the broader HCM hypothesis.
