# AR(p) Null-Family Adequacy Review

**Review date:** 2026-10-17
**Repository:** `AhmedPeaRL/maximal-one`
**Reviewed commit:** `6e48f53cc474e67f1d06ffd7e753b68d8271adb9`
**Review status:** `CURRENT_AR_P_SPECIFICATION_NOT_APPROVED_FOR_CONFIRMATORY_USE`
**Scientific claim status:** `UNDER_INVESTIGATION`

---

## 1. Purpose

This document records a methodological review of the currently specified stationary Gaussian AR(p) stochastic-null procedure, using AIC order selection over p = 1,...,20.

The review distinguishes computational consistency, null-model adequacy, statistical calibration, independent replication, and scientific claim support. These are separate requirements.

This review does not establish or falsify the Constrained Spectral Persistence Hypothesis.

---

## 2. Current specification under review

The current exploratory specification declares:

* Null family: stationary Gaussian AR(p).
* Candidate orders: p = 1,...,20.
* Order-selection criterion: AIC.
* Trend: constant.
* Stationarity: required.
* Candidate-order comparison: common effective observations using maximum-order holdback.
* Surrogate procedure: refit the order-selection procedure on each surrogate.
* Primary endpoint: `canonical_primary_alpha`.
* Alternative: observed alpha greater than the null distribution.
* Monte Carlo p-value: `(exceedances + 1) / (valid_surrogates + 1)`.
* Existing minimum valid-surrogate requirement: 200.
* Current protocol status: exploratory, amended after observation, not preregistered.

The common-observation comparison repair is necessary for a fair information-criterion comparison. It does not, by itself, establish that the selected model family is adequate.

---

## 3. Boundary-saturation evidence

The recorded primary-domain capacity audit reports:

* Valid surrogate refits: 1,000.
* Valid surrogate alpha estimates: 1,000.
* Refits selecting the maximum declared order, p = 20: 937.
* Observed boundary fraction: 0.937.
* Declared review threshold: 0.50.

The observed boundary fraction exceeds the declared review threshold.

Interpretation: the selected order is frequently at the edge of the candidate set. The available evidence does not establish whether this reflects an insufficient candidate range, a mismatch between the model family and the data-generating process, or another feature of the fitting procedure. Boundary saturation is a capacity warning, not proof of any particular explanation.

The historical capacity result must not be used as confirmatory evidence after a protocol change.

---

## 4. Type-I calibration evidence

The currently recorded calibration scenarios use the declared acceptance rule:

1. The two-sided 95% Wilson interval must contain the nominal Type-I error rate of 0.05.
2. The interval's upper endpoint must not exceed 0.075.

Recorded results:

| Scenario                                | Rejections / trials |  Rate | Wilson 95% interval  | Recorded decision                |
| --------------------------------------- | ------------------: | ----: | -------------------- | -------------------------------- |
| Gaussian AR(1), phi = 0.4               |          52 / 1,000 | 0.052 | [0.039873, 0.067556] | Passes this scenario             |
| Gaussian AR(2), phi = 0.45, -0.10       |          60 / 1,000 | 0.060 | [0.046896, 0.076471] | Fails upper-bound rule           |
| Gaussian AR(5), low-order coefficients  |          49 / 1,000 | 0.049 | [0.037261, 0.064191] | Passes this scenario             |
| Gaussian AR(10), low-order coefficients |          73 / 1,000 | 0.073 | [0.058459, 0.090809] | Fails both acceptance conditions |

Passing two scenarios does not imply that the full calibration suite passes. The AR(2) and AR(10) failures must remain visible.

The acceptance rule must not be changed after observing these results merely to obtain a pass. Any future change requires a documented methodological rationale, versioning, and fresh validation. A post-observation change is not preregistered evidence.

---

## 5. Required adequacy review

Before any AR-based null family is considered for confirmation, the review must address:

1. **Order-selection behavior**

   * Preserve the selected-order distribution, not only the boundary fraction.
   * Report fit failures, nonstationary fits, rejected fits, and invalid surrogate counts.
   * Check whether conclusions depend materially on the candidate-order cap.

2. **Stationarity and parameter stability**

   * Verify the declared stationarity condition for every accepted fit.
   * Record near-boundary roots and numerical fitting failures.
   * Examine stability across prespecified temporal segments where scientifically justified.

3. **Residual diagnostics**

   * Report residual autocorrelation diagnostics at prespecified lags.
   * Account for estimated model parameters in diagnostic degrees of freedom.
   * Examine conditional heteroskedasticity and innovation-distribution assumptions.
   * Treat a non-significant residual test as failure to detect a particular problem, not proof of model adequacy.

4. **Calibration**

   * Preserve every required scenario and every failure.
   * Increase simulation precision only under a documented development plan.
   * Use fixed scenario definitions, trial counts, seeds, and acceptance rules before a new calibration run.
   * Keep method-development calibration separate from untouched confirmatory analysis.

5. **Null-family scope**

   * State exactly which temporal structures the candidate null is intended to represent.
   * Identify scientifically plausible departures that the null does not cover.
   * Do not treat rejection of one inadequately specified null as evidence that all stochastic explanations have been excluded.

6. **Independent review**

   * Record the reviewer's identity, scope, date, and decision.
   * Record the exact code commit and artifact hashes.
   * Separate computational reproduction from independent scientific replication.

---

## 6. Decision

**Decision: DO NOT APPROVE THE CURRENT AR(p), AIC, p = 1...20 SPECIFICATION FOR CONFIRMATORY USE.**

Reasons:

* The recorded boundary fraction is 0.937, exceeding the declared 0.50 review threshold.
* The existing Type-I calibration suite contains at least two failed scenarios.
* The null-adequacy review has not been completed and independently accepted.
* The current protocol is explicitly post-observation and not preregistered.

This decision concerns the current specification. It does not establish that every AR(p) model is invalid.

---

## 7. Permitted next steps

Permitted:

* Preserve the current results and failed calibration scenarios.
* Conduct a clearly labelled method-development audit.
* Compare prespecified candidate null families using development data only.
* Document the null-family selection rule before inspecting fresh confirmation outcomes.
* Obtain independent technical review.
* Prepare a new protocol for timestamping before confirmation data are inspected.

Not permitted:

* Reclassifying current exploratory results as preregistered.
* Changing thresholds solely to turn a failed gate into a pass.
* Replacing the primary null with the permutation null because it gives a smaller p-value.
* Promoting the scientific claim on the basis of internal consistency, a diagnostic score, or one p-value.
* Counting synthetic, derived, or null-generated datasets as independent real-domain replications.

---

## 8. Promotion status

The claim remains `UNDER_INVESTIGATION`.

The confirmatory null remains unfrozen. A new prospective analysis must use a fully specified, justified, and independently reviewed null protocol. It must be run on data that have not been used to choose or tune the protocol.

The requirement for at least two eligible independent secondary real domains remains unchanged.

---

## 9. Audit trail

This document records the evidence and decision available at the review date. It does not modify scientific inputs, estimator settings, thresholds, source datasets, claim-support flags, or promotion authority.

Any future revision must retain this version and explain what new evidence justifies the change.
