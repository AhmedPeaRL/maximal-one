# Null Adequacy Decision Rule

## Purpose

This document defines how a future primary stochastic null may be selected
after the diagnostic capacity review.

It does not select a null model by p-value preference.

---

## Current Trigger

The primary-domain capacity audit reported:

- maximum declared AR order: 20;
- observed selected order: 20;
- valid surrogate refits: 1000;
- surrogate boundary fraction: 0.937;
- capacity threshold: 0.50.

Therefore:

`CAPACITY_REVIEW_REQUIRED = TRUE`

---

## Prohibited Selection Rule

The future null must not be selected using:

"choose the model that produces the smallest p-value."

The future null must not be selected using:

"choose the model that rejects the hypothesis."

The future null must not be selected by inspecting the primary
confirmatory outcome and then changing the null specification.

---

## Scientific Selection Principle

A candidate null is admissible only if its scientific role is stated
before confirmatory inference.

The candidate must preserve nuisance temporal structure that the
hypothesis does not claim as distinctive while removing the structure
that the hypothesis claims is distinctive.

---

## Candidate Adequacy Dimensions

Candidate models may be evaluated using:

1. residual autocorrelation;
2. residual partial autocorrelation;
3. information criteria;
4. parameter stability;
5. stationarity;
6. reproduction of relevant temporal dependence;
7. finite-sample calibration;
8. surrogate validity rate;
9. model-selection stability;
10. independence of the inferential decision from the adequacy-selection
    criterion.

---

## Candidate Families

Candidate families may include:

- stationary Gaussian AR(p);
- stationary Gaussian ARMA(p,q);
- other explicitly justified short-memory linear Gaussian models.

Additional families require an explicit scientific justification.

No candidate family is promoted merely because it produces rejection.

---

## Confirmation Freeze

Before future confirmatory inference, the repository must record:

- selected null family;
- model-selection criterion;
- candidate range;
- adequacy criteria;
- surrogate generator;
- number of surrogates;
- minimum valid surrogates;
- endpoint;
- tail;
- alpha threshold;
- replication requirements.

The resulting protocol becomes frozen.

---

## Exploratory Status

All model-capacity comparisons performed using the already-observed
primary dataset are:

`EXPLORATORY`

They cannot be represented as preregistered confirmation.

---

## Claim Gate

Until a frozen future null protocol has been validated:

`CLAIM_PROMOTION = BLOCKED`

The capacity review itself:

`DOES_NOT_SUPPORT_CLAIM = TRUE`

The capacity review itself:

`DOES_NOT_FALSIFY_CLAIM = TRUE`
