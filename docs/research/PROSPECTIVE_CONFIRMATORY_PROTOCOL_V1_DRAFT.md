# Prospective Confirmatory Protocol v1 — Draft

**Status:** `DRAFT_NOT_FROZEN`
**Confirmation status:** `DO_NOT_RUN_CONFIRMATORY_ANALYSIS`
**Claim status:** `UNDER_INVESTIGATION`
**Purpose:** Define the conditions required before a prospective confirmatory analysis can begin.

---

## 1. Status rule

This document is a protocol draft, not a preregistration and not authorization to run confirmatory analysis.

The protocol may be frozen only after:

* the candidate null family passes its documented adequacy review;
* the Type-I calibration acceptance rule is resolved and passed in every required scenario;
* the exact primary test and all failure-handling rules are specified;
* the development and confirmation data are separated;
* the final protocol and analysis code are versioned;
* independent review and durable timestamping occur before confirmation outcomes are inspected.

An unresolved mandatory item keeps the status `DRAFT_NOT_FROZEN`.

---

## 2. Scientific hypothesis and estimand

The hypothesis under investigation is that a spectral persistence signature in selected heterogeneous temporal datasets remains distinguishable from an appropriately specified stochastic null.

The operational endpoint is `canonical_primary_alpha`, calculated by the declared canonical spectral estimator.

The hypothesized direction is:

`observed canonical alpha > the corresponding null distribution`

A lower-than-null alpha does not support this directional hypothesis.

The hypothesis remains unestablished unless the appropriate null is rejected, independent real-domain replication is demonstrated, and the declared reproducibility and validation requirements pass.

---

## 3. Primary measurement specification

The existing measurement specification is recorded here for review; it is not automatically validated for confirmation merely because it exists in the repository.

* Primary estimator: Welch power spectral density.
* Window: Hann.
* Detrending: linear.
* Scaling: density.
* Segment length: 1024.
* Overlap: 50%.
* FFT length: segment length.
* Frequency band: 0.01–0.05.
* Minimum canonical frequency-bin requirement: 20 strictly interior bins.
* Missing-data, timestamp, cadence, normalization, and provenance rules: must be explicitly versioned and tested before freeze.
* No synthetic padding or adaptive estimator change may override the declared eligibility requirements.

Any proposed change must be documented before the confirmation analysis. Post-observation amendments are not preregistered evidence.

---

## 4. Primary null family — unresolved

**Current candidate:** stationary Gaussian AR(p), with AIC selection over p = 1,...,20.

**Current decision:** not approved for confirmatory use.

The candidate cannot be frozen until the AR(p) capacity and calibration review is completed and independently accepted.

The protocol owner must document one of the following outcomes before confirmation:

* approve a specified null family after all required adequacy and calibration gates pass; or
* reject the candidate and document a prespecified alternative-selection procedure.

The final protocol must specify the model family, parameter estimation, order-selection rule, stationarity checks, surrogate-generation method, burn-in, refitting policy, number of surrogates, treatment of failed fits, and all diagnostic criteria.

No family may be selected because it produces a preferred p-value on the confirmation data.

---

## 5. Test and Monte Carlo rules

Before freeze, specify and record:

* The exact observed statistic.
* The null distribution and its scientific interpretation.
* The alternative and tail.
* The Monte Carlo p-value formula.
* The fixed number of surrogate draws.
* The minimum number of valid surrogate fits.
* The seed-generation policy.
* The handling of invalid fits and failed diagnostics.
* The significance level.
* Any multiplicity adjustment or intersection-union decision rule.
* The rule preventing outcome-dependent stopping or extra draws.

The existing add-one formula is:

`p = (exceedances + 1) / (valid_surrogates + 1)`

The formula alone does not establish null adequacy or calibration. The number of draws and all failure policies must be frozen before confirmation.

---

## 6. Calibration gate

All required calibration scenarios must pass the acceptance rule frozen before the calibration run.

The current repository rule requires:

1. the two-sided 95% Wilson interval to contain 0.05; and
2. the upper endpoint to be no greater than 0.075.

The current calibration results include failures. They must not be hidden, overwritten, or reclassified as passes.

Any future methodological revision must have a rationale independent of the desire to make existing results pass. Its status must remain development-only until independently reviewed and prospectively frozen.

---

## 7. Dataset eligibility and replication

The primary dataset and eligibility rules must be fixed before confirmation.

The protocol requires at least two genuinely independent secondary real-world domains.

Each qualifying secondary domain must:

* be eligible under the same frozen rules;
* use the same primary endpoint;
* use the same approved null family and test direction;
* meet the domain-level null-rejection requirement;
* have documented provenance and source-data hashes;
* not be derived from the primary dataset;
* not be synthetic or generated by the null procedure;
* not have been selected because its result supported the hypothesis.

Measurement validity is not the same as independent replication. Internal computational reproducibility is not scientific replication.

---

## 8. Residual, stability, and failure diagnostics

The frozen protocol must state the required checks and their decision rules for:

* residual serial dependence;
* model-adjusted residual-test degrees of freedom;
* stationarity and near-boundary roots;
* parameter stability;
* innovation distribution and variance behavior;
* optimizer failures and invalid parameter estimates;
* surrogate-refit failures;
* boundary saturation in order selection;
* numerical reproducibility and deterministic inputs.

A failed mandatory diagnostic must have a prespecified consequence. It must not be silently dropped after results are seen.

---

## 9. Separation of development and confirmation

All existing observed results, exploratory runs, protocol repairs, and calibration failures belong to the development record unless independently established otherwise.

The confirmation dataset or confirmation period must remain untouched while the protocol is chosen, tuned, and reviewed.

The confirmation run must record:

* exact commit SHA;
* protocol version and SHA-256 hash;
* source-data hashes and provenance;
* locked dependencies and runtime versions;
* seeds and fixed simulation counts;
* all exclusions and failures;
* full canonical report and machine-readable audit artifacts.

No protocol change may be made after inspecting confirmation outcomes without declaring the analysis amended and non-preregistered.

---

## 10. Claim-promotion gate

The claim remains blocked unless every mandatory condition passes:

* the frozen primary null is adequately specified and calibrated;
* the primary null is rejected under the frozen test;
* the primary result passes internal-consistency checks;
* at least two independent secondary real domains meet the frozen replication criterion;
* clean-checkout computational reproducibility passes;
* fingerprint and provenance checks pass;
* required adversarial controls and exclusions pass;
* the independent review record is complete.

A significant diagnostic, a low p-value from a different null, an evidence score, or internal consistency alone cannot substitute for these requirements.

---

## 11. Freeze record — must be completed before confirmation

* Protocol version: `PENDING`
* Approved primary null family: `PENDING`
* Calibration report hash: `PENDING`
* Primary analysis code commit: `PENDING`
* Confirmation data identity and hash: `PENDING`
* Dependency lock hash: `PENDING`
* Independent reviewer and review date: `PENDING`
* Durable timestamp or registration record: `PENDING`
* Confirmation authorization: `NOT_AUTHORIZED`

---

## 12. Current decision

`DRAFT_NOT_FROZEN — DO_NOT_RUN_CONFIRMATORY_ANALYSIS`

This draft defines the conditions for a future confirmation. It does not certify that the current AR(p) family is adequate, that the scientific hypothesis is supported, or that any result is preregistered.
