# Type-I Calibration Independent Review Request V1

Protocol ID: TYPE1_CALIBRATION_SCENARIO_MATRIX_V2
Status: AWAITING_INDEPENDENT_REVIEW
Freeze state: NOT_FROZEN
Reference implementation commit: 4711b13e4b9617ef4ca1aa39b2ad47a6229efe5a

Claim support: NONE
Promotion authority: NONE

## 1. Purpose

Request an independent statistical and computational review of the proposed
Type-I calibration protocol before any prospective confirmatory execution.

This document records review questions. It does not constitute approval,
preregistration, a calibration pass, scientific replication, or claim support.

The reviewer must not infer approval from passing software tests or green
engineering workflow steps.

## 2. Known specification conflict requiring resolution

The current scenario matrix specifies a one-sided 95% Wilson upper confidence
bound with a maximum of 0.075.

The existing operating-characteristics audit describes a different rule:
the two-sided 95% Wilson interval must contain the nominal rejection rate 0.05,
and its upper endpoint must not exceed 0.075.

These rules are not interchangeable.

Before freezing the protocol, the reviewer must:

- Identify the exact acceptance rule intended for the production calibration.
- Explain why that rule is appropriate for the stated Type-I error objective.
- Specify whether containment of the nominal 0.05 rate is a separate requirement.
- Recompute operating characteristics for the exact proposed rule.
- Verify that the implementation and all protocol documents use the same rule.
- Confirm that the rule was not selected to make previously observed results pass.

No threshold or acceptance rule may be changed silently or retrospectively.

## 3. Monte Carlo design review

Review and document:

- The data-generating process for every required scenario.
- Stationarity and stability of each AR process.
- Burn-in, sample size, estimator, surrogate generation, and p-value calculation.
- The handling and reporting of invalid or failed replicates.
- The number of outer repetitions and the uncertainty of estimated rejection rates.
- Whether replicate-level seeds are deterministic and invariant to shard order.
- Whether the implementation matches the written protocol exactly.
- Whether multiplicity across scenarios affects the intended suite-level decision.

Any change must be versioned before the new confirmatory run.

## 4. Seed schedule and execution chronology

The current scenario matrix records:

- Master seed: 20261019
- Seed method: NumPy SeedSequence with stable scenario and replicate indices
- frozen_before_execution: false

Keep this field false until a complete protocol has actually been frozen before
the next execution intended to evaluate that frozen protocol.

Historical runs must remain labeled historical or exploratory when their
execution preceded protocol approval. They must not be relabeled as
prospectively preregistered.

Before the next confirmatory execution, record the approved protocol version,
commit SHA, seed-generation implementation, and independent review decision.

## 5. Scope and adequacy limits

Passing the synthetic Type-I matrix alone does not establish that the
scientific null model is adequate for the primary sunspot series or any
secondary real-world domain.

The independent review must separately assess the relevance of the synthetic
scenarios to the production null, including:

- Near-boundary persistence and AR order-selection behavior.
- Model-capacity and boundary-saturation diagnostics.
- Residual dependence and stationarity.
- Surrogate-generation validity and effective sample size.
- Additional nuisance processes required by the scientific question.

The current stationary Gaussian AR(p) null remains exploratory and unfrozen
until the null-adequacy review is completed.

## 6. Required reviewer record

Reviewer identity and relevant expertise:
[TO BE COMPLETED BY REVIEWER]

Date of review:
[TO BE COMPLETED]

Exact commit and protocol version reviewed:
[TO BE COMPLETED]

Acceptance-rule conflict resolved:
[YES / NO, WITH RATIONALE]

Seed implementation and shard-order invariance reviewed:
[YES / NO, WITH EVIDENCE]

Monte Carlo design and uncertainty reviewed:
[YES / NO, WITH EVIDENCE]

Production-null adequacy reviewed separately:
[YES / NO / NOT YET, WITH RATIONALE]

Required amendments:
[LIST OR NONE]

Decision:
[APPROVE FOR PROSPECTIVE FREEZE / REVISE AND REVIEW AGAIN / REJECT]

Reviewer rationale:
[TO BE COMPLETED BY REVIEWER]

## 7. Freeze authorization

This document does not itself freeze the protocol.

Freeze authorization is permitted only after the reviewer record is complete,
the acceptance rule is internally consistent, required implementation tests
pass, and the approved protocol is committed before the next confirmatory run.

Until then:

- freeze_state remains NOT_FROZEN;
- claim support remains false;
- promotion authority remains false;
- replication eligibility must not be inferred from calibration alone.

## 8. Exact-Snapshot Discrepancy Docket — 2026-10-19

Repository:
AhmedPeaRL/maximal-one

Snapshot commit:
71d331a5c6446f86ab76c7bd94f68feff73813ae

Review status:
AWAITING ATTRIBUTABLE INDEPENDENT STATISTICAL REVIEW

Freeze state:
NOT_FROZEN

Claim support:
false

Promotion authority:
false

### 8.1 Wilson acceptance-rule conflict

The current draft scenario matrix specifies:

- one-sided 95% Wilson upper confidence bound;
- per-scenario maximum upper bound of 0.075;
- suite passes only if every required scenario passes.

The existing historical calibration review instead applies:

- a two-sided 95% Wilson interval;
- the interval must contain the nominal Type-I rate of 0.05;
- the upper endpoint must be no greater than 0.075.

These are different acceptance rules. The historical results must not be reclassified by silently substituting one rule for the other.

The independent reviewer must select and justify one prospective rule, explain its operating characteristics and suite-level interpretation, and identify every implementation and document that must be aligned before protocol freeze.

No result-dependent threshold selection is permitted.

### 8.2 Scenario-matrix versus workflow mismatch

The draft file
protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V2.json
declares nine Type-I scenarios, 2,000 outer repetitions per scenario, 1,000 requested surrogates per outer replicate, and a proposed SeedSequence schedule with master seed 20261019. Its freeze flag remains false.

The workflow
.github/workflows/null-type1-calibration.yml
currently schedules only four scenarios, with 1,000 repetitions, 200 surrogates, and fixed scenario-specific seeds.

Therefore, the current workflow is not an execution of the full draft matrix as written. The independent reviewer must decide which design is approved for prospective use and require the implementation, seed schedule, repetition counts, scenario list, and acceptance rule to match that approved specification.

Do not describe the four-scenario workflow as a completed nine-scenario calibration.

### 8.3 Historical calibration boundary

The previously recorded four-scenario results remain historical evidence under their recorded rule and execution identities. They do not establish that the draft matrix has passed, and they must not be relabeled as a same-commit prospective calibration without matching run records and artifact hashes.

Any future calibration must record the exact commit SHA, scenario ID, seed schedule, repetition and surrogate counts, dependency-lock hash, implementation hash, interval method, acceptance decision, and artifact hash.

### 8.4 Independent review requirements

The reviewer must be independent of the protocol and implementation decisions under review, and must disclose relevant expertise, conflicts of interest, review date, exact commit, and materials reviewed.

The review must separately address:

1. The Wilson acceptance rule and suite-level error interpretation.
2. Monte Carlo uncertainty, invalid replicate handling, and seed/shard-order invariance.
3. Whether the synthetic scenarios cover the intended Type-I operating conditions.
4. Whether the production stochastic null is adequate for the temporal structure and observed model-capacity diagnostics.
5. The distinction between calibration, null adequacy, statistical replication, and scientific claim support.

Required reviewer decision:

[APPROVE FOR PROSPECTIVE FREEZE / REVISE AND REVIEW AGAIN / REJECT]

Rationale and required amendments:

[TO BE COMPLETED BY THE REVIEWER]

### 8.5 Hold decision pending review

Until an attributable independent review is complete and the approved protocol is committed before prospective execution:

- do not freeze the confirmatory protocol;
- do not run candidate confirmation endpoints;
- do not change the Wilson threshold to make historical results pass;
- do not manually promote dataset eligibility;
- preserve all historical artifacts and failures;
- keep claim support false and promotion authority false.

This docket records unresolved specification and execution discrepancies.
It is not an independent review, approval, preregistration, or calibration pass.
