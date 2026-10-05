# Future Null Freeze Rule

## Scientific role

This protocol governs future confirmatory testing of the Constrained
Spectral Persistence Hypothesis.

It does not retroactively convert the current exploratory sunspot
analysis into preregistered confirmation.

---

## Current status

The current stationary Gaussian AR(p) exploratory null is NOT cleared
for confirmatory use.

The primary-domain capacity audit observed:

- maximum declared AR order: `20`
- observed selected order: `20`
- valid surrogate refits: `1000`
- surrogate boundary fraction: `0.937`
- review threshold: `0.50`
- review triggered: `true`

This is a model-capacity warning.

It does not by itself establish that the null is scientifically false.

---

## Null-selection principle

The future primary null must be selected according to scientific
adequacy for the nuisance structure under the hypothesis.

The null MUST NOT be selected according to which model produces the
smallest p-value or the largest separation from the observed endpoint.

---

## Candidate-family principle

Candidate null families may include short-memory stochastic models
appropriate to the temporal structure of the data.

Candidate families must be declared before fresh confirmatory data are
used for endpoint optimization.

Examples of candidate classes that may be considered include:

- stationary AR(p);
- bounded ARMA(p,q);
- other explicitly justified short-memory linear stochastic models;
- state-space formulations when required by the known nuisance structure.

These are candidate families, not automatic choices.

---

## Adequacy dimensions

Null adequacy must be evaluated using criteria that do not optimize the
scientific endpoint.

The declared assessment may include:

- stability;
- residual dependence;
- residual whiteness;
- parameter admissibility;
- out-of-sample predictive adequacy;
- effective sample-size consistency;
- boundary saturation;
- treatment of known periodic nuisance structure;
- reproducibility of the fitted null under declared resampling.

---

## Endpoint separation

The adequacy assessment MUST remain conceptually separate from the
confirmatory endpoint.

A model must not be rejected merely because it produces an unfavorable
scientific p-value.

A model must not be accepted merely because it produces a favorable
scientific p-value.

---

## Model-capacity rule

If the selected model repeatedly reaches the maximum declared model
capacity under either the observed data or a substantial fraction of
valid null surrogates, the model family is not automatically accepted
for confirmation.

The event triggers a capacity review.

---

## Fresh-data rule

After the null family and all selection criteria have been frozen,
confirmatory inference must use data that were not used to optimize the
null protocol.

---

## Post-observation rule

Any change made after observing the confirmatory endpoint is an
exploratory amendment and MUST NOT be labeled preregistered confirmation.

---

## Claim gate

No null-adequacy result alone can promote the scientific claim.

Claim promotion still requires all other declared gates, including:

- primary-domain null rejection;
- independent real-domain replication;
- cross-method agreement;
- internal consistency;
- bootstrap consistency;
- clean-checkout computational reproducibility;
- fingerprint agreement;
- adversarial controls.

---

## HCM boundary

No null-model result may be interpreted as evidence for HCM causation,
consciousness, NEF, a new physical field, universality, or mechanism.
