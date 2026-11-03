# Type-I Caller Trace and Occurrence Adjudication — V2

Status: INVENTORY RECONCILED — MANUAL OCCURRENCE ADJUDICATION OPEN

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


## 10. Evidence update — 2026-11-03

This addendum supersedes earlier evidence references only for
the current inventory and snapshot identity. Earlier run records
remain historical and unchanged.

Repository:
AhmedPeaRL/maximal-one

Review branch:
review/type1-v4-remediation

Exact review commit:
bab449da0ec15eadeb7d5cc1ca27c4bc92f1cebb

Main comparison commit:
2ed03db704ccc93838e00db4db9aa7e75c20973c

### 10.1 Governance inventory run

Workflow:
Type-I V3 V4 Governance Inventory Audit

Run:
41667056999

Job:
126025095632

Artifact:
13245867785

Artifact name:
type1-v3-v4-governance-inventory-41667056999-1

Artifact ZIP SHA-256:
50f29efd1c660e60f4d70dff719c4d2aad0d0180a99a34c0028b303de656f6c3

Inventory JSON SHA-256:
39def0ddd0ee35444d51f2c718f1c283e100b83cbae84020cc80395be551ff63

Workflow conclusion:
SUCCESS

### 10.2 Exact inventory counts

Review branch:

- Commit: bab449da0ec15eadeb7d5cc1ca27c4bc92f1cebb
- Files with matching references: 245
- Occurrence matches: 1,563
- Workflow files with matches: 35
- Analysis/scripts files with matches: 54
- Test files with matches: 24
- Protocol files with matches: 98
- Documentation/README files with matches: 5
- Workflow runner-invocation candidate files: 2

Main:

- Commit: 2ed03db704ccc93838e00db4db9aa7e75c20973c
- Files with matching references: 179
- Occurrence matches: 581
- Workflow files with matches: 30
- Analysis/scripts files with matches: 49
- Test files with matches: 6
- Protocol files with matches: 60
- Documentation/README files with matches: 5
- Workflow runner-invocation candidate files: 1

These are occurrence and file counts from the declared
pattern-based inventory. They are not counts of independently
confirmed execution paths.

### 10.3 Automated occurrence-label distribution

Review branch, 1,563 occurrences:

- PROTOCOL_OR_DOCUMENTATION_REFERENCE: 402
- GOVERNANCE_REFERENCE: 367
- CODE_PATH_REQUIRES_CALL_GRAPH_REVIEW: 241
- TEST_OR_GUARD: 180
- POLICY_OR_HISTORICAL_REFERENCE: 143
- WORKFLOW_REFERENCE: 130
- WORKFLOW_CONTROL_PATH: 83
- OTHER_REFERENCE: 14
- EXECUTION_CAPABLE_WORKFLOW_CANDIDATE: 3

Main, 581 occurrences:

- CODE_PATH_REQUIRES_CALL_GRAPH_REVIEW: 151
- GOVERNANCE_REFERENCE: 142
- WORKFLOW_REFERENCE: 73
- WORKFLOW_CONTROL_PATH: 71
- POLICY_OR_HISTORICAL_REFERENCE: 58
- PROTOCOL_OR_DOCUMENTATION_REFERENCE: 40
- TEST_OR_GUARD: 31
- OTHER_REFERENCE: 14
- EXECUTION_CAPABLE_WORKFLOW_CANDIDATE: 1

These are automated labels attached to individual matching
occurrences. They are not manual adjudications.

### 10.4 Inventory-to-ledger reconciliation

Review branch:

- Expected occurrences: 1,563
- Observed occurrences: 1,563
- Missing occurrence IDs: 0
- Extra occurrence IDs: 0
- Duplicate occurrence IDs: 0
- Identity field mismatches: 0
- Status: RECONCILED

Main:

- Expected occurrences: 581
- Observed occurrences: 581
- Missing occurrence IDs: 0
- Extra occurrence IDs: 0
- Duplicate occurrence IDs: 0
- Identity field mismatches: 0
- Status: RECONCILED

Reconciliation verifies occurrence identity and accounting
coverage only.

It does not establish:
- human classification;
- direct or indirect caller completeness;
- authorization guard correctness;
- guard execution order;
- negative-test effectiveness;
- statistical validity;
- protocol approval.

### 10.5 Manual adjudication state

All 1,563 review-branch records remain:

- manual_classification: UNKNOWN
- status: OPEN
- reviewer_disposition: PENDING
- direct_caller_or_workflow_step: OPEN
- indirect_call_path: OPEN
- authorization_guard_and_execution_order: OPEN
- guard_fails_closed: UNKNOWN
- negative_test: NOT_YET_IDENTIFIED

All 581 main-branch records remain subject to the same
discovery-only and OPEN limitations.

No occurrence is closed by reconciliation or classifier output.

### 10.6 Exact snapshot run

Workflow:
Type-I Exact Review Snapshot and SHA-256

Run:
41667505773

Job:
126026683231

Artifact:
13245973048

Artifact name:
type1-exact-review-snapshot-41667505773-1

Artifact ZIP SHA-256:
78a5ca1283771780c4b94d94c56e242e36245a4302c38bd4edf82bb26244f009

Snapshot schema:
HCM_TYPE1_REVIEW_SNAPSHOT_V3

Snapshot review commit:
bab449da0ec15eadeb7d5cc1ca27c4bc92f1cebb

Inventory artifact ID:
13245867785

Inventory source commit:
bab449da0ec15eadeb7d5cc1ca27c4bc92f1cebb

Inventory JSON SHA-256:
39def0ddd0ee35444d51f2c718f1c283e100b83cbae84020cc80395be551ff63

Snapshot accounting:

- Inventory-derived unique paths: 245
- Mandatory anchors: 40
- Selected unique scope paths: 252
- Present files: 252
- Missing required paths: 0
- Missing scope paths: 0
- Explicit excluded paths: 0
- Scanner exclusions retained in snapshot scope: 1
- Inventory occurrences represented: 1,563

The one scanner exclusion is:

protocol/TYPE1_V3_V4_OCCURRENCE_LEVEL_MANUAL_LEDGER_2026-10-31.json

It is excluded from recursive occurrence scanning to avoid
duplicating serialized historical occurrence rows, but retained
in snapshot hash scope.

The snapshot workflow completed its six inventory-scope tests.
The artifact contains manifest.json and SHA256SUMS.txt only.
It does not contain copies of the 252 source files.

Therefore this artifact is an inventory-bound hash manifest,
not yet a self-contained source review package.

The manifest also does not currently record a per-file
scope_origin or per-file occurrence-ID mapping.

### 10.7 Runtime pilot branch-control finding

Reviewed workflow:

.github/workflows/type1-calibration-runtime-pilot.yml

Reviewed runner:

analysis/type1_calibration_pilot.py

The workflow uses workflow_dispatch and verifies checkout
commit identity, but does not currently enforce the authorized
review branch.

The runner enforces draft-matrix status and pilot-size limits,
but does not independently enforce the authorized branch.

Consequently, commit identity validation alone does not
establish branch authorization.

Required remediation:

1. Add an explicit fail-closed branch guard to the workflow
   before setup, pilot execution, or output creation.
2. Enforce the same branch guard inside the runner entry point
   so direct invocation cannot bypass the workflow guard.
3. Add an executable negative test for an unauthorized branch.
4. Verify that the rejection occurs before any pilot output
   or artifact is created.
5. Record the actual test run, job, artifact state, and commit
   after execution.

No branch-guard negative-test run is claimed by this addendum.

### 10.8 Current disposition

INVENTORY_IDENTITY_RECONCILED.

INVENTORY_OCCURRENCE_ACCOUNTING_RECONCILED.

MANUAL_OCCURRENCE_ADJUDICATION_OPEN.

EXECUTION_PATH_ADJUDICATION_OPEN.

DIRECT_AND_INDIRECT_CALLER_REVIEW_OPEN.

AUTHORIZATION_GUARD_ORDER_REVIEW_OPEN.

RUNTIME_PILOT_BRANCH_GUARD_REMEDIATION_REQUIRED.

SELF_CONTAINED_SOURCE_SNAPSHOT_PENDING.

INDEPENDENT_HUMAN_STATISTICAL_REVIEW_PENDING.

PROTOCOL_NOT_FROZEN.

FORMAL_CALIBRATION_NOT_AUTHORIZED.

CONFIRMATORY_EXECUTION_NOT_AUTHORIZED.

CLAIM_SUPPORT_FALSE.

PROMOTION_AUTHORITY_FALSE.
