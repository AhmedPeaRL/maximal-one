# Future Confirmation Null Protocol

## Status

PROSPECTIVE PROTOCOL TEMPLATE — NOT CURRENT CONFIRMATION EVIDENCE

This document defines the requirements for a future confirmatory stochastic-null protocol.

It does not replace the current canonical primary null.

It does not reinterpret the current dataset as preregistered confirmation.

It does not authorize selection of a null model after observing the desired inferential outcome.

---

## Current Primary Null

The current canonical primary null is:

- stationary Gaussian AR(p)
- AIC order selection
- p = 1..20
- upper-tail comparison
- canonical primary spectral exponent as endpoint

The current primary null is not rejected:

p = 0.999001

The current null-capacity audit also shows that AIC reaches the declared order boundary at order caps 20, 40, and 60.

Therefore the current finite-order AR null is retained as historical canonical evidence, but is not treated as a fully capacity-resolved confirmatory null.

---

## Prohibited Actions

The following are prohibited:

1. Increasing the AR order solely because the current null was not rejected.
2. Selecting AR, ARMA, ARFIMA, seasonal, harmonic, or other null families after observing the confirmation dataset.
3. Choosing the null family by maximizing claim-supporting significance.
4. Changing the test direction after observing the sign of the effect.
5. Changing the frequency band after observing the resulting alpha.
6. Correcting the observed alpha post hoc.
7. Treating a diagnostic permutation null as a substitute for the declared primary stochastic null.
8. Treating internal reproducibility as scientific replication.

---

## Required Prospective Sequence

Before fresh confirmation data are analyzed:

1. Freeze the endpoint

The primary endpoint must be declared exactly.

Example:

canonical_primary_alpha

No alternate endpoint may become primary after data inspection.

2. Freeze the estimator

The following must be declared before confirmation:

- estimator
- frequency band
- nperseg
- window
- detrending
- normalization
- frequency-bin validity rule
- handling of short series

3. Freeze the candidate null families

A finite candidate set must be declared before confirmation.

The candidate set may include, where scientifically justified:

- stationary AR
- stationary ARMA
- fractionally integrated models
- seasonal or harmonic-plus-residual models
- other explicitly justified stochastic families

The candidate set itself must not be expanded after observing the confirmation outcome.

4. Freeze the model-selection rule

If more than one null family is permitted, the selection rule must be declared independently of the desired claim outcome.

Selection may use predeclared process-adequacy criteria.

Selection must not use the final claim-support p-value as its criterion.

5. Freeze the direction

The current hypothesis direction is:

greater_than_null

A lower-than-null result is not support for the current alternative.

6. Freeze the simulation procedure

The protocol must declare:

- number of surrogates
- burn-in
- parameter fitting procedure
- parameter refitting rules
- stationarity requirements
- random-seed policy
- Monte Carlo p-value rule

7. Freeze replication domains

At least two independent real secondary domains must be declared before fresh confirmation analysis.

A domain qualifies only if:

- it is genuinely independent,
- it uses the same primary endpoint,
- it uses the same null family,
- it uses the same direction,
- it uses the same tail,
- its measurement is valid,
- it independently rejects the declared null.

Measurement validity alone is not replication.

---

## Confirmation Dataset Rule

The confirmation dataset must not be used to redesign the protocol.

If the current dataset is used to refine:

- estimator,
- frequency band,
- null family,
- model order,
- eligibility,
- direction,
- replication domains,

then the resulting protocol is exploratory/post-observation.

A fresh dataset or an explicitly held-out confirmation dataset must subsequently be analyzed under the frozen protocol.

---

## Success Condition

A future confirmation may support promotion only if all of the following are simultaneously true:

1. Primary null rejected at the predeclared threshold.
2. Null model passes the predeclared adequacy requirements.
3. At least two independent real secondary domains independently reject the same null.
4. Endpoint and direction remain unchanged.
5. Estimator settings remain unchanged.
6. No post-observation correction was applied.
7. Adversarial controls pass.
8. Clean-checkout computational reproducibility is verified.
9. Fingerprint verification succeeds.
10. The full provenance chain is preserved.

Failure of any required condition blocks promotion.

---

## Scientific Scope

Even successful confirmation would not by itself establish:

- HCM causation
- consciousness
- universality
- a new physical law
- mechanism
- market advantage
- financial profitability

Those are separate claims requiring separate evidence.

---

## Epistemic Status

The current project status remains:

UNDER INVESTIGATION

The purpose of this protocol is not to manufacture a positive result.

Its purpose is to make a future positive result difficult to obtain unless it survives a protocol that was fixed before confirmation.
