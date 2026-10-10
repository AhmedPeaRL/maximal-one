# Secondary Domain Review Plan V1

Protocol ID: `SECONDARY_DOMAIN_REVIEW_PLAN_V1`
Status: `OPEN — NOT CONFIRMATORY`
Scientific role: Data provenance, transformation specification, nuisance review, and replication-readiness assessment
Claim authority: `NONE`
Promotion authority: `NONE`

---

## Purpose

This plan governs the review of HadCET monthly temperature and FRED INDPRO monthly industrial production data as candidate secondary domains for the Constrained Spectral Persistence Hypothesis.

Passing this plan does not establish the hypothesis, scientific replication, independence, or claim-promotion eligibility.

---

## Immutable Evidence

Before any new analysis, preserve:

- The exact Git commit SHA.
- The original raw source snapshots.
- The parsed CSV files.
- The source manifest and all recorded SHA-256 digests.
- The current canonical report and relevant audit artifacts.
- The existing strict claim and null-protocol versions.

Do not overwrite historical artifacts or silently replace source snapshots. Record every subsequent change in a new commit.

---

## Source and Transformation Specification

For each candidate domain, document before inspecting its new alpha result:

1. Source identifier, publisher, source URL, retrieval date, and raw-file checksum.
2. Observation variable, units, observation window, cadence, and missingness.
3. The exact transformation to be evaluated, including mathematical definition and implementation.
4. Whether the transformation preserves the scientific meaning of the variable.
5. Detrending, seasonal adjustment, differencing, standardization, and aggregation decisions, where applicable.
6. The treatment of gaps, non-finite values, revisions, and duplicate timestamps.
7. The rationale for the selected transformation and the alternatives considered.
8. The full set of candidate transformations and comparisons planned before inspecting their endpoint results.

Do not select a transformation because it produces a favorable alpha, smaller p-value, or stronger agreement with the primary domain.

If the transformation set or selection rule changes after endpoint inspection, record the change as post-observation and require a fresh prospective validation before confirmatory interpretation.

---

## Temporal Integrity

Require deterministic validation of:

- Strictly increasing and unique timestamps.
- Expected monthly cadence and complete calendar coverage.
- Explicit missingness and gap reports.
- The frozen analysis cutoff of 2025-12-01, inclusive.
- Raw-to-parsed provenance and checksum consistency.
- Reproducible preprocessing from preserved source snapshots.

A temporal-integrity pass does not establish scientific independence or replication eligibility.

---

## Independence and Shared Nuisance Review

For each candidate, document plausible shared drivers with the primary sunspot domain and with the other candidate domain.

The review must address, where scientifically applicable:

- Solar-cycle and geomagnetic influences.
- Climate and atmospheric processes.
- Industrial, energy, and policy cycles.
- Secular trends, periodic components, and common external drivers.
- Autocorrelation, nonstationarity, and changes in the observation process.

Distinguish a genuinely separate measurement domain from a statistically independent process.
Different subject matter or different source organizations alone does not prove independence.

Record unresolved nuisance pathways explicitly.
Do not grant replication eligibility while required independence reviews remain unresolved.

---

## Null Model Adequacy

The existing stationary Gaussian AR(p) null remains exploratory and unfrozen.

Before confirmatory use, review:

- Residual autocorrelation and partial autocorrelation.
- Stationarity and parameter stability.
- Goodness of fit and finite-sample calibration.
- Surrogate-generation validity and effective sample size.
- Order-selection stability and boundary saturation.
- Preservation of relevant nuisance structure.
- Monte Carlo uncertainty and the predeclared decision rule.

The observed surrogate boundary fraction of 0.947 against the recorded threshold of 0.50 requires a capacity review.
The separate diagnostic scan selecting AR order 40 at its upper boundary also requires investigation.

Do not increase the maximum AR order, change the null family, or select a new model based on which choice produces a favorable scientific result.
Any protocol amendment must be versioned and followed by fresh validation.

---

## Replication Eligibility

A candidate may be considered for independent replication only after all required conditions are independently checked:

- Valid source provenance.
- Valid timestamp and preprocessing integrity.
- Compliance with the frozen estimator and sample-length requirements.
- Documented independence from the primary domain and relevant shared nuisances.
- The same predeclared endpoint, null family, and direction of effect.
- Domain-level rejection of the declared appropriate null under the frozen protocol.
- Reproducible calculations and auditable artifacts.

Measurement eligibility is not replication eligibility.
A candidate is not a replication merely because its alpha can be computed.

---

## Required Outputs

Generate versioned artifacts containing:

- Source and checksum audit.
- Transformation specification and preprocessing audit.
- Missingness, cadence, and temporal-integrity report.
- Independence and nuisance assessment.
- Null-adequacy and capacity-review report.
- Per-domain endpoint and null-test results.
- Eligibility decision with explicit reasons.
- Reproducibility fingerprints and exact commit identity.

Preserve unfavorable results and excluded candidates with their exclusion reasons.

---

## Decision Rules

Until the required reviews and prospective validation are complete:

- Keep the confirmatory null unfrozen.
- Keep independent replication unestablished.
- Keep scientific claim support false.
- Keep claim-promotion authority false.
- Do not describe exploratory or diagnostic outputs as confirmatory evidence.

A failed gate must identify its scientific or technical reason.
A diagnostic failure must not be relabeled as a successful scientific result.

---

## Completion Criterion

This plan is complete only when the review artifacts are reproducible, the predeclared requirements are satisfied, and an independent assessment supports the resulting eligibility decisions.

Completion of this document alone grants no scientific authority.
