# Independent Review Request — Primary Stochastic Null Adequacy

Protocol ID: "INDEPENDENT_REVIEW_REQUEST_NULL_ADEQUACY_V1"

Date: 2026-10-14

Status: "OPEN — REVIEW NOT YET COMPLETED"

Scientific role: Independent methodological review

Claim-support authority: None

Claim-promotion authority: None

1. Purpose

Request an independent review of the adequacy and calibration of the primary stochastic null used to evaluate the Constrained Spectral Persistence Hypothesis.

The purpose is to assess whether the declared null model is scientifically suitable for the question and whether the validation design controls false-positive risk under relevant temporal processes.

The review is not a request to obtain a favorable result, validate HCM causation, or approve claim promotion.

2. Current Evidence to Review

The current repository records the following:

- Primary dataset: "real-data/sunspots_full.csv".
- Canonical sample size: 3,328 observations.
- Primary endpoint: "canonical_primary_alpha".
- Canonical estimator: Welch PSD, "nperseg = 1024".
- Declared frequency band: 0.01–0.05.
- Existing null family: stationary Gaussian AR(p), with AIC order selection over p = 1..20.
- Primary capacity audit: 937 of 1,000 valid surrogate refits selected the maximum declared order of 20.
- A separate canonical null-gate estimate reports a boundary fraction of 0.947 from a different recorded random stream.
- A diagnostic scan through order 40 selected the upper boundary of that scan.
- The current reported primary stochastic-null p-value is 0.999001; the null was not rejected.
- The confirmatory null remains unfrozen.
- Type-I calibration did not pass every declared synthetic scenario.
- Two eligible independent secondary real-domain replications have not been established.

These are recorded diagnostics, not evidence that the hypothesis is supported or falsified.

3. Questions for the Reviewer

Please assess the following without selecting models according to the observed scientific outcome:

1. Is a stationary Gaussian AR(p) family appropriate for the declared scientific question and temporal characteristics of the primary series?
2. What do the observed boundary-selection rates imply about model capacity, and what conclusions cannot be drawn from them?
3. Which alternative null families, if any, are justified by the scientific assumptions rather than by the observed result?
4. Which temporal features must the null preserve, including relevant periodicity, long-memory behavior, nonstationarity, and nuisance structure?
5. What simulation scenarios are necessary to evaluate Type-I error, statistical power, surrogate validity, and finite-sample behavior?
6. How should model-selection uncertainty, boundary-selected fits, failed fits, and invalid surrogate samples be handled?
7. What acceptance criteria should be specified before a fresh confirmatory run, including Monte Carlo uncertainty and multiple calibration scenarios?
8. What evidence would be sufficient to freeze the protocol prospectively, and what results would require rejecting or revising the proposed null?
9. Which independent implementation checks and replication requirements are needed before scientific claim support can be reconsidered?

4. Change-Control Requirements

The review must not authorize:

- Increasing the AR maximum order solely because the selected order reached the existing boundary.
- Replacing the primary stochastic null with a permutation diagnostic merely because its result differs.
- Changing the endpoint, frequency band, or acceptance thresholds to favor the observed result.
- Treating historical exploratory results as prospectively preregistered evidence.
- Promoting a null model solely because it reduces boundary saturation.
- Treating computational reproducibility as scientific replication.

Any proposed methodological change must include its scientific rationale, assumptions, limitations, implementation specification, calibration plan, and fresh-validation requirements.

5. Reviewer Record

Complete this section only after an actual independent review.

- Reviewer identity or attributable reviewer record: "PENDING"
- Relevant expertise: "PENDING"
- Exact repository commit reviewed: "PENDING"
- Protocol revision reviewed: "PENDING"
- Main objections and responses: "PENDING"
- Recommended disposition: "PENDING"
- Review date: "PENDING"

Do not fill these fields by inference or backdate the review.

6. Decision Until Review Is Complete

The current AR(p) protocol remains exploratory and unfrozen for confirmatory inference.

The primary claim remains under investigation.

Claim support remains false.

Claim-promotion authority remains false.

No new confirmatory outcome may be treated as valid confirmation until a scientifically justified protocol has been reviewed, frozen prospectively, calibrated, and linked to a fresh validation plan.

Current decision: "HOLD CONFIRMATORY INFERENCE — INDEPENDENT REVIEW REQUIRED"
