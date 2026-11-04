# Engineering Review Delta and Execution-Path Triage — 2026-11-04

## 1. Review identity

- Repository: `AhmedPeaRL/maximal-one`
- Branch: `review/type1-v4-remediation`
- Exact commit: `fed77fe73d930c54f1217dca7506c4d0d7cd8fd4`
- Main inventory commit: `2ed03db704ccc93838e00db4db9aa7e75c20973c`

This record documents engineering evidence and preliminary static observations. It does not constitute independent human statistical review, occurrence-level human adjudication, protocol approval, or execution authorization.

## 2. Workflow evidence

### Governance inventory

- Run: `41754791331`
- Job: `126328257865`
- Artifact: `13287169845`
- Artifact ZIP SHA-256: `19fa686fbfbbf68d8746269f57fe52c564c5b5d4085435b6c2189b62d9b5d545`
- Result: SUCCESS

The artifact contains five files:
- `type1_governance_inventory/reference_inventory.json`
- `type1_occurrence_ledger/occurrence_level_manual_ledger.json`
- `type1_occurrence_ledger/reconciliation.json`
- `type1_occurrence_ledger/main_occurrence_level_manual_ledger.json`
- `type1_occurrence_ledger/main_reconciliation.json`

The inventory JSON SHA-256 is:

`f521e110c56d5914179869bf735bbcde2711004adb3bc6879412d4820d17097b`

### Exact-review snapshot

- Run: `41754999586`
- Job: `126328921482`
- Artifact: `13288345427`
- Artifact ZIP SHA-256: `5d2591c9785b549288832ba18ef87b1f952f4d0025c133ce6470f4a2f861b6f4`
- Result: SUCCESS

Manifest SHA-256:

`af6f65025122906bed074b3d244d3a925bb1cb8d3629ecbab290c5d1297be014`

The archive contains `manifest.json` and `SHA256SUMS.txt`. The 256 manifest paths and checksum paths match exactly, and all 256 digests match.

This remains a hash-manifest snapshot, not a self-contained source archive.

## 3. Updated inventory scope

Review branch:
- Files with matched occurrences: 249
- Occurrences: 1,596

Main branch:
- Files with matched occurrences: 179
- Occurrences: 581

Review-branch classification totals:

- PROTOCOL_OR_DOCUMENTATION_REFERENCE: 411
- GOVERNANCE_REFERENCE: 382
- CODE_PATH_REQUIRES_CALL_GRAPH_REVIEW: 243
- TEST_OR_GUARD: 186
- POLICY_OR_HISTORICAL_REFERENCE: 143
- WORKFLOW_REFERENCE: 131
- WORKFLOW_CONTROL_PATH: 83
- OTHER_REFERENCE: 14
- EXECUTION_CAPABLE_WORKFLOW_CANDIDATE: 3

The review ledger contains 1,596 records. All remain UNKNOWN, OPEN, and PENDING. No manual closure is claimed.

The main ledger contains 581 records and remains separately scoped.

## 4. Reconciliation

Review-branch reconciliation:
- Status: RECONCILED
- Expected occurrences: 1,596
- Observed occurrences: 1,596
- Count matches: true
- Identity matches: true
- Manual review state preserved: true
- Duplicate IDs: none
- Missing IDs: none
- Extra IDs: none
- Authority: NO_CLASSIFICATION_OR_EXECUTION_AUTHORITY
- Diagnostic only: true

Main-branch reconciliation:
- Status: RECONCILED
- Expected occurrences: 581
- Observed occurrences: 581
- Count matches: true
- Identity matches: true
- Manual review state preserved: true
- Duplicate IDs: none
- Missing IDs: none
- Extra IDs: none
- Authority: NO_CLASSIFICATION_OR_EXECUTION_AUTHORITY
- Diagnostic only: true

Reconciliation establishes identity and coverage only. It does not establish correctness of manual classifications, call paths, guard ordering, statistical validity, or scientific claims.

## 5. Priority execution-path candidates

Three automated candidates require occurrence-specific human review:

1. `.github/workflows/type1-calibration-runtime-pilot.yml`, line 73
2. `.github/workflows/type1-v4-cross-runner-worker-order.yml`, line 60
3. `.github/workflows/type1-v4-cross-runner-worker-order.yml`, line 123

### Preliminary static observations

The runtime-pilot workflow:
- Supports workflow_dispatch.
- Checks out the exact repository state.
- Invokes `scripts/type1_runtime_pilot_branch_guard.py` before output creation and runner invocation.
- Checks `HEAD` against `GITHUB_SHA`.
- The branch guard restricts execution to `refs/heads/review/type1-v4-remediation`.
- The pilot is explicitly described as exploratory, not formal calibration.

The cross-runner workflow:
- Supports workflow_dispatch and a path-filtered push trigger on the review branch.
- Its connected-reference, worker, and comparison jobs each check the review branch and exact checkout identity before Python setup and their respective commands.
- The two calibration runner invocations explicitly pass `--engineering-test`.
- The runner separates engineering mode from formal mode.
- Engineering mode is restricted to at most six outer replicates, exactly 1,000 surrogates, the declared AR(2) baseline, candidate sample size, and candidate seed.
- Engineering artifacts explicitly retain `formal_calibration_pass=false`, `claim_support=false`, `promotion_authority=false`, and `confirmatory_execution_authorized=false`.

These are preliminary source observations, not closure decisions. The exact caller graph, all indirect invocation routes, guard behavior under adversarial conditions, and negative tests remain open.

The two successful workflow runs documented in this record are the inventory and snapshot workflows. They are not evidence that the runtime-pilot or cross-runner simulation workflows were executed.

## 6. Required occurrence-level review fields

For each occurrence, preserve its exact occurrence ID and record:

- `manual_classification`
- `reviewer_disposition`
- `can_influence_execution`
- `direct_caller_or_workflow_step`
- `indirect_call_path`
- `runner_entry_point_or_command`
- `trigger_conditions_and_branch_restrictions`
- `authorization_guard_and_execution_order`
- `guard_fails_closed`
- `matrix_and_protocol_consumed`
- `negative_test`
- `test_run_job_artifact_commit`
- `closure_evidence`

Every conclusion must cite exact file paths, commit identity, line ranges, relevant tests, and immutable run or artifact references where applicable.

Do not infer NO from missing evidence. Retain UNKNOWN and OPEN whenever evidence is insufficient.

## 7. Mandatory next gates

1. Preserve both artifacts and their hashes.
2. Reconcile all downstream documents to the current count of 1,596 review-branch occurrences.
3. Complete the three priority execution-path reviews.
4. Trace direct and indirect callers for all execution-relevant code and workflow occurrences.
5. Verify guard order, exact commit binding, trigger conditions, protocol and matrix consumption.
6. Add negative tests for missing authorization, wrong branch, mismatched commit, mismatched artifact identity, invalid digest, unfrozen protocol, and unauthorized invocation.
7. Decide whether the snapshot is intentionally hash-manifest-only or must include all 256 source-file contents.
8. If a source archive is required, generate it and verify every extracted file against the manifest.
9. Obtain attributable independent human statistical-methods review of the exact protocol, matrix, and acceptance rule.
10. Preserve historical failures and thresholds; resolve any prospective acceptance-rule decision without retrospective rewriting.
11. Keep protocol freeze and all scientific execution authorization disabled until the required reviews and gates are satisfied.

## 8. Preserved governance state

- Protocol freeze: NOT_FROZEN
- Formal calibration authorized: false
- Confirmatory execution authorized: false
- Claim support: false
- Promotion authority: false

Engineering workflow success is not Type-I calibration success. Inventory reconciliation is not manual occurrence closure. Static source inspection is not independent human review.

## 9. Decision

`INVENTORY_AND_RECONCILIATION_PASSED`

`EXACT_COMMIT_SNAPSHOT_MANIFEST_PASSED`

`SOURCE_ARCHIVE_CONTENTS_NOT_INCLUDED`

`OCCURRENCE_COUNT_UPDATED_TO_1596`

`MANUAL_OCCURRENCE_ADJUDICATION_OPEN`

`PRIORITY_EXECUTION_PATH_REVIEW_OPEN`

`INDEPENDENT_STATISTICAL_REVIEW_PENDING`

`PROTOCOL_NOT_FROZEN`

`FORMAL_CALIBRATION_NOT_AUTHORIZED`

`CONFIRMATORY_EXECUTION_NOT_AUTHORIZED`

`CLAIM_SUPPORT_FALSE`

`PROMOTION_AUTHORITY_FALSE`

Next gate: Complete occurrence-specific adjudication, caller-graph review, guard-order verification, negative tests, and snapshot packaging clarification before any request for scientific authorization.
