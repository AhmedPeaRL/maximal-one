# Primary Stochastic Null Model Capacity Review

## Status

**CAPACITY REVIEW REQUIRED**

The primary-domain capacity audit has completed successfully.

The audit is diagnostic-only and does not establish, reject, or falsify the Constrained Spectral Persistence Hypothesis.

---

## Primary Dataset

Dataset:

`real-data/sunspots_full.csv`

Sample size:

`N = 3328`

Canonical loader:

`analysis.load_real_datasets.load_series`

---

## Declared Null

The current exploratory null is:

`stationary_gaussian_AR_p`

with:

- AIC order selection;
- candidate orders `1..20`;
- constant trend;
- stationarity requirement;
- fixed comparison hold-back equal to the maximum candidate order;
- identical effective observations across candidate orders;
- refitting of the selected order for every surrogate.

Protocol revision:

`ar_order_comparison_holdback_v1`

---

## Capacity Audit

Seed:

`90210`

Requested surrogate refits:

`1000`

Minimum valid surrogate refits:

`200`

Valid surrogate refits:

`1000`

Valid surrogate alpha estimates:

`1000`

Observed selected order:

`20`

Maximum declared order:

`20`

Surrogate boundary fraction:

`0.937`

Boundary review threshold:

`0.50`

Review status:

`TRIGGERED`

---

## Scientific Meaning

The result means that the declared AR order-selection range is boundary-saturated in the primary-domain surrogate experiment.

This is evidence about the **capacity of the declared model-selection procedure**.

It is not evidence that:

- the scientific hypothesis is true;
- the scientific hypothesis is false;
- the null is false;
- the null is true;
- HCM causation exists;
- the observed spectral exponent represents a new physical mechanism.

The capacity audit therefore remains:

`scientific_role = diagnostic_only`

and:

`claim_support = false`

---

## Prohibited Response

The repository must not respond to boundary saturation by automatically increasing the maximum AR order until a favorable inferential result is obtained.

In particular, the following procedure is prohibited:

1. observe the primary result;
2. observe null boundary saturation;
3. choose a new model family or order because it produces a more favorable p-value;
4. present the resulting p-value as confirmatory evidence.

Such a procedure would make the inferential protocol outcome-dependent.

---

## Required Null Adequacy Review

Before any future confirmatory claim is evaluated, the project must determine what structure the null is required to preserve.

The null must be selected according to its scientific role, not according to which null produces the most favorable result.

The review must consider, where scientifically justified:

- higher-order autoregressive models;
- ARMA-type short-memory models;
- residual whiteness and residual autocorrelation diagnostics;
- information-criterion behavior;
- parameter stability;
- stationarity constraints;
- surrogate reproduction of relevant temporal dependence;
- sensitivity to the declared endpoint;
- finite-sample behavior;
- whether the null preserves or removes the specific structure under test.

No candidate null becomes the confirmatory null merely because it produces rejection of the null.

---

## Primary Scientific Principle

The null must remove the structure that the hypothesis claims is distinctive while preserving nuisance structure that is not part of the hypothesis.

Therefore null adequacy cannot be established by p-value preference alone.

A candidate null that reproduces the observed spectral structure so closely that it removes the hypothesized signal is not automatically "stronger."

Its scientific role must be defined before confirmatory inference.

---

## Confirmation Freeze

After the adequacy review, the future confirmatory protocol must freeze:

- dataset inclusion rule;
- endpoint;
- estimator;
- frequency band;
- preprocessing;
- null family;
- model-selection rule;
- candidate model range;
- adequacy criteria;
- surrogate-generation procedure;
- number of surrogates;
- minimum valid surrogates;
- test direction;
- tail;
- significance threshold;
- replication rule;
- exclusion criteria.

After freeze, these parameters must not be changed because of the resulting p-value.

---

## Fresh Data Requirement

The present primary-domain capacity audit is post-observation.

It is not preregistered confirmation.

A future confirmatory result must therefore be evaluated under a protocol frozen before that confirmation dataset is used for inferential decision-making.

Historical exploratory results remain available for transparency but cannot be promoted retroactively to preregistered evidence.

---

## Current Scientific Decision

The scientific claim remains:

`CLAIM = NOT ESTABLISHED`

The current state is:

`UNDER INVESTIGATION`

The capacity review does not itself falsify the hypothesis.

It blocks confirmatory interpretation until null adequacy has been addressed.

---

## HCM Boundary

No spectral result in this review establishes:

- consciousness;
- HCM causation;
- a physical consciousness field;
- universal behavior;
- novel physics;
- predictive superiority;
- market profitability.

Those propositions require independent evidence beyond the present spectral validation program.
