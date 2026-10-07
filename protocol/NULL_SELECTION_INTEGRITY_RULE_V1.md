# Null Selection Integrity Rule V1

## Status

`EXPLORATORY METHODOLOGICAL CONTROL`

This protocol does not provide scientific support for the HCM hypothesis.

---

## Purpose

The current primary stochastic null reached a capacity warning:

- maximum declared AR order: `20`;
- observed selected order: `20`;
- surrogate boundary fraction: `0.937`.

Therefore the current AR(p)-AIC implementation is not accepted as a
fully calibrated confirmatory null.

A future null must be selected by scientific adequacy criteria rather
than by the inferential result it produces.

---

## Prohibited selection

The following procedures are prohibited:

1. selecting the null with the smallest p-value;
2. selecting the null with the largest p-value;
3. selecting the null that produces rejection;
4. selecting the null that preserves a preferred HCM result;
5. changing AIC to BIC after observing a confirmatory result;
6. increasing or decreasing model order after observing the result;
7. changing the endpoint after null comparison;
8. changing the frequency band after null comparison;
9. excluding an inconvenient domain after null comparison.

---

## Candidate adequacy

A candidate null may be considered scientifically adequate only after
evaluation of:

- temporal residual structure;
- residual autocorrelation;
- residual partial autocorrelation;
- stationarity;
- parameter stability;
- finite-sample calibration;
- surrogate validity;
- model-selection stability;
- capacity saturation;
- effective sample size;
- declared nuisance temporal structure.

No single adequacy diagnostic is sufficient.

---

## Solar nuisance

Because the primary sunspot domain contains approximately decadal
solar structure with harmonics entering the canonical frequency band,
future confirmatory null evaluation must explicitly state whether the
solar component is:

- represented as nuisance structure;
- residualized;
- modeled jointly with the stochastic component; or
- demonstrated to be irrelevant under a separately validated protocol.

The nuisance treatment must be frozen before confirmation.

---

## Calibration data

Candidate selection must not use the final confirmation outcome.

Calibration/reference data must be declared before candidate comparison.

If a dataset is used to select the final null, it must not later be
described as untouched confirmation data.

---

## Scientific outcome

If no candidate satisfies the declared adequacy criteria:

`CONFIRMATORY_INFERENCE_REMAINS_BLOCKED`

This is a valid scientific result.

The repository must not weaken the criteria merely to permit promotion.

---

## Claim boundary

Null adequacy or null rejection does not by itself establish:

- HCM causation;
- consciousness;
- mechanism;
- universality;
- new physics;
- predictive superiority;
- market advantage.
