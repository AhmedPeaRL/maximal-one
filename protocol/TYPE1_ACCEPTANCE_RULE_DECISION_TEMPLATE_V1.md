# Type-I Acceptance Rule Decision Template — V1

## Status

`PENDING_ATTRIBUTABLE_INDEPENDENT_STATISTICAL_REVIEW`

This template is not an approval and does not authorize confirmatory execution.

## 1. Historical rule — preserved without retrospective change

The historical rule requires:

1. The two-sided 95% Wilson interval to contain nominal rejection probability 0.05.
2. The two-sided Wilson upper endpoint to be no greater than 0.075.

Historical results retain their original classifications under the rule that governed those runs.

## 2. V4 candidate rule — not yet approved

The V4 candidate proposes a one-sided 95% Wilson upper confidence bound no greater than 0.075 for every required scenario.

The value 0.075 is not automatically justified by the nominal level 0.05. The tolerance and its decision consequences require explicit review.

## 3. Required reviewer decisions

The reviewer must document:

* The precise estimand and intended interpretation of Type-I error.
* Whether the rule is intended to establish control at 0.05 or accept a separately justified tolerance above 0.05.
* The justification for the confidence-bound convention and threshold.
* The operating characteristics under true rejection probabilities of 0.05, 0.065, 0.07, and 0.075.
* Whether 2,000 outer repetitions provide adequate decision precision.
* The handling of invalid attempts, missing surrogates, and incomplete runs.
* Whether the nine proposed scenarios are sufficient for the intended scope.
* Any required amendments, to be made prospectively before formal simulation.

## 4. Decision

Selected prospective rule: `PENDING`

Substantive rationale: `PENDING`

Reviewer full name and relevant expertise: `PENDING`

Affiliation or independent-review basis: `PENDING`

Conflict-of-interest statement: `PENDING`

Review date (UTC): `PENDING`

Reviewed commit SHA: `PENDING`

Reviewed matrix SHA-256: `PENDING`

Reviewed runner SHA-256: `PENDING`

Reviewer decision: `PENDING`

Permitted values:

* `APPROVE_PROSPECTIVE_RULE`
* `REVISE_AND_RESUBMIT`
* `REJECT_RULE`

## 5. Non-retroactivity declaration

This decision applies prospectively only.

It does not alter historical observations, historical workflow outcomes, prior failures, or the rule used to classify earlier runs.

## 6. Authorization

This template itself grants no authorization.

Confirmatory execution remains prohibited until the approved rule, matrix, runner, invalid-attempt policy, and independent review are recorded in a separate, attributable freeze and authorization decision.
