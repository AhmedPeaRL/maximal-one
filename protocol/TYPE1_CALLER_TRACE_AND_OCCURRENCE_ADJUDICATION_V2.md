# Type-I Caller Trace and Occurrence Adjudication — V2

Status: PARTIAL STATIC REVIEW — MANUAL OCCURRENCE ADJUDICATION OPEN

Authority: REVIEW EVIDENCE ONLY

Protocol freeze: NOT FROZEN

Formal calibration: NOT AUTHORIZED

Confirmatory execution: NOT AUTHORIZED

Claim support: FALSE

Promotion authority: FALSE

## 1. Exact evidence snapshots

Repository: AhmedPeaRL/maximal-one

Main commit:
2ed03db704ccc93838e00db4db9aa7e75c20973c

Review branch:
review/type1-v4-remediation

Review commit:
8bd41aa6181608d6c2d131bdf1abaf5767e7c883

Governance inventory run:
41604692993

Governance inventory job:
125811506081

Governance artifact:
13216031909

Snapshot run:
41660914140

Snapshot job:
126003571942

Snapshot artifact:
13241976587

Main validation run:
41661215704

Main validation job:
126004611333

## 2. Inventory reconciliation

Review branch:
- Expected occurrences: 1543
- Observed occurrences: 1543
- Missing occurrences: 0
- Extra occurrences: 0
- Duplicate occurrence IDs: 0
- Reconciliation: RECONCILED

Main:
- Expected occurrences: 581
- Observed occurrences: 581
- Missing occurrences: 0
- Extra occurrences: 0
- Duplicate occurrence IDs: 0
- Reconciliation: RECONCILED

All generated ledger records remain:
- manual_classification: UNKNOWN
- status: OPEN
- reviewer_disposition: PENDING
- direct_caller_or_workflow_step: OPEN
- indirect_call_path: OPEN
- authorization_guard_and_execution_order: OPEN
- guard_fails_closed: UNKNOWN
- negative_test: NOT_YET_IDENTIFIED

Reconciliation establishes identity and coverage only. It does not establish manual classification, caller-chain completeness, guard correctness, or scientific validity.

## 3. Main V3 workflow

Entry point:
.github/workflows/null-type1-calibration.yml

The preparation job checks:
- APPROVED_FROZEN
- freeze_state == FROZEN
- confirmatory_execution_authorized == true
- archive_git_identity_verified == true

The dependent matrix job is skipped when preparation fails.

The current main commit removed the declared V3 scenario-calibration invocation. Therefore a successful preparation or workflow completion must not be interpreted as evidence that calibration simulations ran.

Run 41661215704 failed at protocol-freeze validation. The matrix job was skipped. No calibration was started in this run.

## 4. V4 formal runner

Relevant files:
- analysis/calibrate_null_type1.py
- analysis/calibrate_null_type1_scenario.py
- protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json
- protocol/TYPE1_CALIBRATION_FREEZE_DECISION.json
- protocol/TYPE1_CALIBRATION_EXECUTION_AUTHORIZATION.json

The formal runner checks V4 approval before proceeding. The current freeze decision is NOT_APPROVED and NOT_FROZEN. The execution authorization is NOT_AUTHORIZED.

No formal calibration is authorized.

## 5. Separate engineering and pilot routes

The following routes must be adjudicated independently:

A. V4 formal runner.

B. V4 engineering-test runner.

C. analysis/type1_calibration_pilot.py.

D. .github/workflows/type1-calibration-runtime-pilot.yml.

E. Direct callers of execute_attempt().

F. Direct callers of parametric_short_memory_null() and estimate_alpha().

G. Shard, merge, checkpoint, and resume entry points.

An engineering or pilot route must never be interpreted as formal calibration merely because it exercises the production endpoint or null implementation.

## 6. Required occurrence-level fields

For every execution-capable or governance-related occurrence, record:

- Exact occurrence ID, path, line, and commit.
- Manual classification and rationale.
- Direct caller or workflow step.
- Complete indirect caller chain.
- Trigger conditions and branch restrictions.
- Protocol and matrix consumed.
- Authorization guard and exact execution order.
- First side effect or computation after the guard.
- Whether the guard fails closed.
- Negative test identifier and expected rejection.
- Exact workflow run, job, artifact, and commit.
- Reviewer disposition and closure evidence.

No occurrence may be closed by an automated classifier alone.

## 7. Required negative tests

Each independently executable route must demonstrate rejection for:
- Missing protocol approval.
- Missing freeze state.
- Missing confirmatory authorization.
- Wrong branch or event context where restriction is required.
- Commit identity mismatch.
- Matrix hash mismatch.
- Source hash mismatch.
- Missing or corrupt checkpoint manifest.
- Resume identity mismatch.
- Missing shard or attempt.
- Duplicate or overlapping shard indices.

A rejection test must verify the expected non-zero exit, explicit rejection message, absence of unauthorized output, and preservation of original artifacts where applicable.

## 8. Statistical review and authorization boundary

The V4 candidate remains unapproved.

The independent statistical reviewer must provide attributable qualifications, conflict disclosures, exact reviewed commit and file hashes, parameter decisions, acceptance-rule rationale, multiplicity policy, invalid-attempt policy, and an explicit disposition.

A favorable statistical review is not itself a protocol freeze or execution authorization.

Freeze and execution authorization must remain separate, prospective, attributable, and bound to exact source identities.

## 9. Current disposition

INVENTORY_IDENTITY_RECONCILED.

MANUAL_OCCURRENCE_ADJUDICATION_OPEN.

DIRECT_AND_INDIRECT_CALLER_REVIEW_OPEN.

GUARD_ORDER_REVIEW_OPEN.

NEGATIVE_TEST_MAPPING_INCOMPLETE.

INDEPENDENT_HUMAN_STATISTICAL_REVIEW_PENDING.

PROTOCOL_NOT_FROZEN.

FORMAL_CALIBRATION_NOT_AUTHORIZED.

CLAIM_SUPPORT_FALSE.

PROMOTION_AUTHORITY_FALSE.
