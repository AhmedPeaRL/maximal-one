# Null Adequacy Freeze

## Status

`PROSPECTIVE METHODOLOGICAL PROTOCOL`

This protocol does not constitute evidence for the scientific
hypothesis.

Historical sunspot results remain exploratory and non-confirmatory.

---

## Purpose

The declared stationary Gaussian AR(p) null reached the maximum
candidate order in the observed primary fit and in `93.7%` of valid
surrogate refits.

Therefore the current `AR(1..20)` implementation is not accepted as
a fully calibrated confirmatory null.

---

## Separation of model adequacy and scientific inference

Null adequacy is evaluated independently of the confirmatory endpoint.

A candidate null is not selected because it produces a `smaller p-value`.

A candidate null is not rejected because it produces a `larger p-value`.

---

## Candidate evaluation

Candidate null families may be evaluated using:

1. residual autocorrelation;
2. residual partial autocorrelation;
3. stationarity;
4. parameter stability;
5. finite-sample calibration;
6. surrogate validity;
7. model-selection stability;
8. boundary saturation;
9. preservation of declared nuisance temporal structure;
10. preservation of effective sample size.

---

## Confirmation-data separation

The primary confirmation dataset must not be used to select the final
null family or its hyperparameters.

Candidate adequacy must be established on an explicitly declared
calibration or reference dataset.

---

## Solar nuisance

The primary sunspot domain contains approximately decadal periodic
structure whose harmonics enter the canonical frequency band.

Therefore any confirmatory null used for the primary sunspot domain
must explicitly state whether and how the declared solar nuisance
structure is represented.

No solar component may be removed after inspecting the confirmatory
endpoint.

No frequency band may be changed after inspecting the nuisance result.

---

## Frozen decision

Before confirmatory evaluation, the repository must record:

- null family;
- parameter-selection rule;
- candidate range;
- nuisance treatment;
- surrogate generator;
- number of surrogates;
- minimum valid surrogates;
- burn-in;
- endpoint;
- alternative direction;
- tail;
- p-value rule;
- domain eligibility;
- replication requirement;
- multiple-testing policy;
- failure policy.

---

## Prohibited rescue

The following cannot convert exploratory evidence into confirmation:

- increasing model order after observing the result;
- switching AIC/BIC after observing the result;
- changing the null family after observing the result;
- changing the endpoint;
- changing the tail;
- changing the frequency band;
- removing solar harmonics after observing the result;
- excluding unfavorable domains;
- lowering replication requirements.

---

## Epistemic rule

If no candidate null passes the declared adequacy criteria,
confirmatory inference remains unavailable.

This is a valid scientific outcome.

---

## Claim boundary

This protocol does not establish:

- HCM causation;
- consciousness;
- universality;
- new physics;
- mechanism;
- predictive superiority;
- market advantage.

Scientific claim promotion remains blocked until all declared
validation layers independently pass.
