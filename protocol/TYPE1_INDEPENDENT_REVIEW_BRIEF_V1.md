# Type-I Calibration Independent Statistical Review Brief V1

- **Repository:** `AhmedPeaRL/maximal-one`
- **Required branch:** `review/type1-v4-remediation`
- **Review status:** `NOT_STARTED_OR_NOT_DOCUMENTED`
- **Protocol status:** `DRAFT_PENDING_ATTRIBUTABLE_INDEPENDENT_STATISTICAL_REVIEW`
- **Freeze state:** `NOT_FROZEN`
- **Confirmatory execution authorized:** `false`
- **Claim support:** `false`
- **Promotion authority:** `false`

## 1. Purpose and limits

This document requests an attributable independent human statistical review of the proposed Type-I error calibration procedure.

The review must evaluate the estimand, endpoint, stochastic null, data-generating scenarios, invalid-attempt policy, acceptance rule, Monte Carlo precision, computational feasibility, and evidence-retention plan.

This brief is not itself an approval, a protocol freeze, evidence of calibration, or support for the broader Hybrid Consciousness Model.

## 2. Exact materials to review

The reviewer must record the exact commit SHA and SHA-256 hashes of the reviewed files.

Required materials include:

* `protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_DRAFT.json`
* `protocol/TYPE1_CALIBRATION_SPEC_V3_CANDIDATE.md`
* `analysis/numerical_spectral_verification.py`
* `analysis/appropriate_stochastic_null.py`
* `analysis/type1_calibration_pilot.py`
* `tests/test_type1_production_equivalence.py`
* The actual shard-merge and checkpoint-resume implementation.
* The workflow that executes and retains pilot artifacts.
* The current Type-I acceptance evidence ledger.

If any path differs or a required file is absent, record the discrepancy. Do not silently substitute a similarly named file.

## 3. Questions requiring explicit decisions

### A. Statistical estimand

1. Define precisely what Type-I error rate is being estimated.
2. State the null hypothesis, alternative, rejection rule, sampling unit, and target population of simulated scenarios.
3. Explain whether the proposed nine scenarios support only scenario-specific operating-characteristic statements or any broader statement.
4. Explain the interpretation of the upper-tail test and its relationship to the intended scientific question.

### B. Endpoint definition

Review and specify:

* Input length and minimum-validity rules.
* Demeaning and standardization.
* Welch window, segment length, overlap, FFT length, detrending, scaling, and averaging.
* Frequency-band boundaries and their strict or inclusive treatment.
* The minimum number of usable frequency bins.
* The regression used to estimate the spectral slope.
* The sign convention and rounding rule.
* All invalid-input and non-finite-result conditions.

The specification must be independently reviewed and versioned. A test that merely transcribes the production implementation is not sufficient evidence of independent scientific validation.

### C. Stochastic null and surrogate generation

Explicitly review:

* Gaussian stationary AR(p) surrogate family.
* Candidate order range and AIC selection.
* Constant-trend specification.
* Fixed hold-back and equality of effective observations.
* Stationarity and root checks.
* Initial-state, innovation, and burn-in conventions.
* Re-estimation of AR(p) for every surrogate.
* Treatment of failed model fits and invalid endpoint estimates.
* Upper-tail exceedance definition.
* Monte Carlo add-one p-value:
  `(exceedances + 1) / (valid_surrogates + 1)`.

The reviewer must determine whether the production requirement is exactly 1,000 valid surrogates or permits a prospectively specified shortfall. The current implementation and pilot must not be assumed equivalent on this point.

### D. Acceptance rule

The current candidate proposes a one-sided 95% Wilson upper confidence bound no greater than 0.075. This is a proposed acceptance rule, not an established scientific result.

The reviewer must evaluate:

* The justification for the 0.075 ceiling.
* Its relationship to the nominal alpha of 0.05.
* The number of outer repetitions per scenario.
* The nine-scenario design and scenario-specific interpretation.
* Monte Carlo uncertainty and power to detect unacceptable Type-I inflation.
* Whether the rule is suitable for each scenario and for any proposed aggregate conclusion.

Any amendment must be documented prospectively, before confirmatory outcomes are inspected.

### E. Invalid attempts and missing evidence

The reviewer must explicitly decide how the protocol handles:

* Invalid outer attempts.
* Failed or insufficient surrogate generation.
* Missing, duplicated, overlapping, or mismatched shard records.
* Corrupted or absent artifacts and manifests.
* Interrupted execution and checkpoint resume.
* Failed jobs and reruns.
* Multiple comparisons, if applicable.

No failed or invalid attempt may be silently dropped, replaced, or reclassified as a pass.

### F. Computational feasibility and reproducibility

Review:

* Estimated number of endpoint and surrogate evaluations.
* Runtime and storage estimates based on measured pilot evidence.
* Deterministic seed derivation and independent random streams.
* Environment and dependency capture.
* Artifact hashes, manifest verification, and retention.
* Reproducibility across connected execution, sharded execution, reverse-order merge, checkpoint resume, and a fresh uninterrupted run.

A small runtime pilot may support feasibility estimates. It does not establish formal Type-I calibration.

## 4. Required full-path equivalence evidence

Before formal calibration is authorized, the acceptance suite must demonstrate that the actual production path yields identical canonical per-replicate records across:

1. A fresh uninterrupted run.
2. A connected multi-run execution.
3. Separate shards merged in normal order.
4. The same shards merged in reverse order.
5. A checkpointed run resumed from a verified artifact.

The test must use the actual endpoint, actual null procedure, actual shard runner, actual merger, and actual resume path.

It must reject missing records, duplicate replicate identities, overlapping shards, incompatible run identities, corrupted bytes, mismatched manifests, incomplete shards, and invalid records under the approved policy.

Tests must preserve enough evidence to inspect each expected and observed result. Mocked endpoint or null implementations do not satisfy this requirement.

## 5. Required reviewer disposition

The reviewer must select and justify one disposition for each section:

* `APPROVE`
* `APPROVE_WITH_SPECIFIED_CONDITIONS`
* `REVISE_AND_RESUBMIT`
* `REJECT`
* `NOT_REVIEWED`

Required sections:

* Statistical estimand.
* Endpoint definition.
* Stochastic-null specification.
* Scenario design.
* Acceptance rule.
* Invalid-attempt policy.
* Monte Carlo precision.
* Computational feasibility.
* Full-path equivalence evidence.
* Artifact and reproducibility requirements.

An overall approval must not conceal a failed or unresolved critical section.

## 6. Attribution and audit record

Record the following only after the review actually occurs:

* Reviewer name and professional affiliation, if provided.
* Reviewer role and relevant statistical expertise.
* Conflict-of-interest declaration, if provided.
* Exact reviewed commit SHA.
* SHA-256 hashes of the reviewed protocol and implementation files.
* Review date.
* Written rationale and requested revisions.
* Final disposition and any conditions.
* Location of the retained review record.

Do not invent or backdate attribution. AI-assisted analysis is not independent human statistical approval.

## 7. Freeze gate

Protocol freeze is a separate decision and must not be inferred from a passing test suite.

A freeze decision requires:

1. All required equivalence criteria to have inspectable outcomes.
2. All critical acceptance items to be closed or explicitly blocking.
3. An attributable independent human review.
4. Resolution of every required reviewer condition.
5. A versioned, hash-identified protocol and implementation snapshot.
6. A distinct freeze record identifying the exact commit and approved files.

Until those conditions are documented:

* `freeze_state = NOT_FROZEN`
* `confirmatory_execution_authorized = false`
* `claim_support = false`
* `promotion_authority = false`

## 8. Current decision

`CONTINUE_REMEDIATION`

This brief defines the required review. It does not assert that the review has occurred, that implementation equivalence has passed, or that formal calibration is authorized.
