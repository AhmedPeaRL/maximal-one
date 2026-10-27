# V4 Acceptance-Rule Decision Record

Decision ID: TYPE1_V4_ACCEPTANCE_RULE_DECISION_V1

Repository: AhmedPeaRL/maximal-one

Branch: review/type1-v4-remediation

Status: PENDING_ATTRIBUTABLE_INDEPENDENT_HUMAN_REVIEW

## 1. Reviewed snapshot

- Reviewed commit SHA: PENDING
- V4 candidate matrix path:
  `protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json`
- Matrix SHA-256: PENDING
- Runner SHA-256: PENDING
- Dependency-lock SHA-256: PENDING
- Review date UTC: PENDING

## 2. Historical rule — immutable record

The historical decision rule required:
- The two-sided 95% Wilson interval to contain nominal alpha = 0.05.
- The upper endpoint not to exceed 0.075.

Historical outcomes remain classified under that rule.
No historical failure may be reclassified because a prospective rule differs.

## 3. V4 candidate rule — not approved

The V4 candidate has proposed a one-sided 95% Wilson upper-bound criterion of 0.075.

This proposal is not approved by this template.
No threshold is selected by the engineering workflow.

## 4. Required independent human review

Reviewer name and affiliation: PENDING

Relevant statistical expertise: PENDING

Conflicts of interest: PENDING

Reviewer confirmation that the exact snapshot was examined: PENDING

The reviewer must assess:
- The target Type-I error estimand.
- The confidence-bound convention and rationale.
- The acceptance boundary and its consequences.
- Monte Carlo precision at the planned number of outer repetitions.
- Invalid-attempt handling and denominator preservation.
- Multiplicity and the rule for passing the complete scenario suite.
- Scenario coverage and limitations of the declared null family.

AI-generated text or a successful CI run is not independent human approval.

## 5. Prospective decision

Selected rule: NOT DECIDED

Scientific rationale: PENDING

Reviewer disposition: PENDING

Required protocol changes: PENDING

Approval commit SHA: PENDING

Approved matrix and runner hashes: PENDING

## 6. Authorization boundary

Until the reviewer disposition is attributable, the decision is recorded,
and all applicable gates are closed:

- freeze_state = NOT_FROZEN
- confirmatory_execution_authorized = false
- claim_support = false
- promotion_authority = false
- formal calibration = NOT AUTHORIZED

This document does not authorize execution.
A separate explicit authorization is required after prospective review
and protocol freeze.
