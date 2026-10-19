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
