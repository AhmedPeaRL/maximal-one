# Claim Status

---

## Current Status

UNDER INVESTIGATION

The current canonical validation pipeline does not support promotion
of the Constrained Spectral Persistence Hypothesis.

---

## Canonical Primary Measurement

Primary dataset:

"real-data/sunspots_full.csv"

Sample size:

"N = 3328"

Canonical Welch spectral exponent:

"alpha = 2.525347"

Independent FFT-periodogram estimate:

"alpha = 2.423397"

Absolute method difference:

"0.101950"

The cross-method agreement is a measurement-consistency result.
It is not independent scientific replication.

---

## Primary Stochastic Null

The current exploratory primary stochastic null is:

"stationary_gaussian_AR_p_aic"

with:

- AIC order selection
- order range 1..20
- stationary fitted models
- Gaussian innovations
- refitting for every surrogate
- canonical primary alpha as endpoint
- upper-tail direction

Current canonical result:

- valid surrogates: 1000
- observed alpha: 2.525347
- null mean: 3.197386
- null SD: 0.235076
- null q05: 2.816685
- null q95: 3.584700
- exceedances: 999
- Monte Carlo p-value: 0.999001
- rejection at 0.05: false

Therefore:

The primary stochastic null is not rejected.

---

## Null Capacity Diagnostic

The surrogate AR-order boundary fraction is:

"0.965"

That means 96.5% of surrogate refits select the maximum
declared order of 20.

This is treated as a model-capacity/calibration warning.

It is not evidence for the scientific claim.

A larger order range must not be selected merely because it
produces a preferred p-value. Any amended null protocol must be
declared before a fresh confirmation run.

---

## Secondary Diagnostics

Permutation-null result:

"p = 0.0002"

Role:

DIAGNOSTIC ONLY

It is not the primary stochastic null and has no claim-promotion
authority.

The current scale diagnostic satisfies its declared numerical
thresholds, but scale stability alone cannot establish the claim.

The current predictive validation has:

"structural_match = false"

and is therefore diagnostic only.

---

## Independent Real-Domain Replication

The project requires at least two independent real secondary
domains.

Measurement validity is explicitly different from scientific
replication.

Scientific replication requires each domain to reject the same
declared primary stochastic null using the same endpoint,
direction, tail, and null family.

That condition is not currently established.

---

## Reproducibility Boundary

Clean-checkout replay is computational reproducibility.

It is not:

- scientific replication
- independent implementation replication
- laboratory replication

---

## Epistemic Boundary

The current evidence does not establish:

- HCM causation
- consciousness
- a physical field
- universality
- novel physics
- market advantage
- predictive superiority

---

## Next Scientific Objective

The next objective is not to force promotion.

The next objective is to:

1. characterize estimator behavior over the relevant alpha range;
2. audit the capacity and adequacy of the primary stochastic-null family;
3. declare a fixed prospective null protocol;
4. perform fresh validation under that protocol;
5. require independent domain-level null rejection;
6. preserve the current result if the hypothesis fails.

No threshold, tail, endpoint, or null family should be changed solely
to obtain a favorable result.

---

## Scientific Decision Rule

Until all machine-gated prerequisites are satisfied:

CLAIM = NOT ESTABLISHED

The system must remain capable of producing a negative result.
