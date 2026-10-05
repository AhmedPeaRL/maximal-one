# MAXIMAL-ONE — Scientific Status Report

## Current Status

**UNDER INVESTIGATION**

The current canonical validation pipeline does not establish the
Constrained Spectral Persistence Hypothesis.

No scientific claim is promoted by the current evidence.

---

## Current Canonical Measurement

Primary dataset:

`real-data/sunspots_full.csv`

Primary sample size:

`N = 3328`

Canonical estimator:

`Welch_PSD`

Canonical frequency band:

`0.01–0.05`

Canonical segmentation:

`nperseg = 1024`

Canonical spectral exponent:

`alpha = 2.525347`

Independent FFT-periodogram estimate:

`alpha = 2.423397`

Absolute method difference:

`0.101950`

The agreement between Welch and FFT is a measurement-consistency
result. It is not independent scientific replication.

---

## Historical Primary Stochastic-Null Result

A pre-repair exploratory analysis reported:

- observed canonical alpha: `2.525347`
- surrogate boundary fraction: approximately `0.965`
- Monte Carlo p-value: approximately `0.999001`

These values belong to the historical pre-repair protocol.

They are retained for provenance only.

They are not current confirmatory evidence.

The AR order-comparison procedure was subsequently repaired under:

`ar_order_comparison_holdback_v1`

using:

`hold_back = max_candidate_order = 20`

for identical effective observations across candidate orders.

The repair was made after observation and is explicitly classified as
non-preregistered.

Therefore the historical p-value and historical boundary fraction must
not be reused for claim promotion.

---

## Current Primary-Null Status

A fresh primary reanalysis is required after the protocol repair.

A separate primary-null capacity audit is also required to determine
whether the declared finite-order AR(p) family is adequately calibrated
for the primary sunspot process.

Known-process AR calibration is diagnostic only.

Passing AR(1)/AR(2) calibration does not establish adequacy of the
primary sunspot stochastic null.

Until the fresh primary reanalysis and capacity assessment are complete:

`CLAIM = NOT ESTABLISHED`

and the scientific claim remains:

`UNDER INVESTIGATION`.

### Scientific decision

No current confirmatory decision is available for the primary stochastic null.

The previously reported primary-null result belongs to the
pre-repair protocol and is retained only for provenance.

It must not be interpreted as the current inferential outcome.

Therefore:

`CLAIM = NOT ESTABLISHED`

and the scientific claim remains:

`UNDER INVESTIGATION`.

---

## Null Capacity Diagnostic

The surrogate AR-order boundary fraction is:

`0.965`

Therefore 96.5% of surrogate refits selected the maximum declared
order of 20.

This is treated as a null-model capacity/calibration warning.

It is not evidence for the scientific hypothesis.

The repository must not increase the AR order merely to obtain a more
favorable inferential result.

Any replacement null protocol must be declared prospectively before
fresh confirmation data are used.

---

## Estimator Sensitivity

A prospective estimator sensitivity audit was performed.

Across valid combinations of declared frequency bands and Welch
segment lengths:

- minimum observed alpha: `0.329523`
- maximum observed alpha: `3.209988`
- alpha range: `2.880465`

The canonical configuration produces:

`alpha = 2.525347`

Several reasonable alternative configurations produce materially
different values.

Therefore the current data do not justify treating `alpha` as a
configuration-independent universal scalar.

The sensitivity audit is diagnostic only.

No favorable estimator configuration may replace the canonical
endpoint after observing the data.

---

## Secondary Diagnostics

The permutation null produced:

`p = 0.0002`

This result concerns the specified exchangeability/permutation null
only.

It is **diagnostic only** and is not the primary stochastic-null
decision.

Other diagnostic layers include:

- cross-method agreement;
- multi-scale behavior;
- perturbation stability;
- phase-surrogate behavior;
- predictive validation;
- adversarial controls.

None of these independently establishes the scientific claim.

---

## Independent Real-Domain Replication

The repository requires at least two independent real secondary
domains.

A valid alpha measurement is not scientific replication.

Scientific replication requires each eligible independent domain to
reject the same declared primary stochastic null using:

- the same endpoint;
- the same null family;
- the same direction;
- the same tail;
- the same scientific decision rule.

That condition is not currently established.

---

## Computational Reproducibility

Clean-checkout replay establishes computational reproducibility of the
declared execution path.

It does not establish:

- scientific replication;
- independent implementation replication;
- laboratory replication;
- truth of the scientific hypothesis.

---

## HCM Interpretation Boundary

The current canonical spectral result does not establish:

- HCM causation;
- consciousness;
- a physical field;
- universality;
- novel physics;
- predictive superiority;
- market advantage;
- mechanism.

HCM-related interpretations remain conceptual hypotheses outside the
current empirical claim authority.

---

## Scientific Decision

The current machine-gated decision is:

`CLAIM = NOT ESTABLISHED`

This is an intended scientific outcome.

The system must remain capable of producing and preserving a negative
result.

---

## Next Scientific Phase

The next phase is methodological:

1. complete prospective estimator characterization;
2. complete null-model calibration and adequacy analysis;
3. formally predeclare the future primary null;
4. freeze the future confirmation protocol;
5. analyze fresh confirmation data;
6. require independent real-domain replication;
7. require clean-checkout computational reproducibility;
8. preserve all failed outcomes.

No threshold, endpoint, tail, estimator, or null family should be
changed solely to obtain a favorable result.
