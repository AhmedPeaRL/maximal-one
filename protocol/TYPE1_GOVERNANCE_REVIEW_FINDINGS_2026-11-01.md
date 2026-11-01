# Type-I Governance Review Findings — 2026-11-01

Status: PARTIAL TECHNICAL INVENTORY COMPLETE
Human classification: OPEN
Execution authorization: NOT AUTHORIZED
Protocol freeze: NOT FROZEN
Claim support: FALSE
Promotion authority: FALSE

## 1. Exact snapshot

Repository: AhmedPeaRL/maximal-one
Review branch: review/type1-v4-remediation
Review commit: 6b76f53356fef9f869412960b24e5b5b9fea9965

Main commit:
116686b03077f2521ab320635a098d5359c8d337

Merge base:
a9808bd999a7ad902daf15606272529ca9af4580

## 2. Inventory evidence

Governance inventory workflow:
41264316424

Exact review snapshot workflow:
41264414937

Governance inventory artifact:
13066946292

Exact review snapshot artifact:
13066752097

Review-branch inventory:
- Files with matching references: 129
- Occurrences: 2208
- Missing required paths: 0
- Missing scope paths: 0
- Excluded paths: 0

Main inventory:
- Files with matching references: 69
- Occurrences: 203

The occurrence-level ledger was generated for the review
branch only. A separate main-branch occurrence ledger remains
required.

## 3. Human classification status

All 2208 records in the generated review-branch ledger
remain:

- manual_classification: UNKNOWN
- status: OPEN
- reviewer_disposition: PENDING
- direct_call_path: OPEN
- indirect_call_path: OPEN
- authorization_guard: OPEN
- negative_test: NOT_YET_IDENTIFIED

Inventory reconciliation does not constitute manual review.

## 4. Automated classification limitations

The current discovery classifier assigns workflow classifications
using whole-file content rather than occurrence-specific evidence.

Consequently, an occurrence may be labeled as an execution
candidate because an unrelated line elsewhere in the same
workflow contains an execution-related token.

The current automated categories are discovery labels only.
They must not be treated as human adjudications or closure
evidence.

The pattern inventory is also not a complete call graph.
Execution paths without the selected search tokens may remain
outside the inventory.

## 5. High-priority review scope

Current discovery labels:

- EXECUTION_CAPABLE_WORKFLOW_CANDIDATE: 75 occurrences
- WORKFLOW_CONTROL_PATH: 23 occurrences
- CODE_PATH_REQUIRES_CALL_GRAPH_REVIEW: 67 occurrences

These counts are occurrences, not confirmed independent
execution paths.

Every occurrence must retain its stable identity and receive
an occurrence-specific human disposition.

## 6. V3/V4 execution findings

V3 on main:

- The legacy workflow contains a direct runner invocation.
- The current V3 matrix is NOT_FROZEN.
- Confirmatory execution is not authorized.
- The current preparation gate is expected to reject execution.

V3 on the review branch:

- The workflow contains an explicit fail-closed step before
  the legacy runner invocation.
- This does not by itself close the main-branch execution path.

V4 formal runner:

- V4_APPROVED is false.
- The formal runner rejects execution.
- The V4 candidate matrix is not frozen.
- The execution authorization record is NOT_AUTHORIZED.

Exploratory and engineering paths:

- Runtime pilot: 2 outer repetitions, 200 surrogates.
- Engineering cross-runner path: 6 outer repetitions,
  1000 surrogates, engineering-test mode.
- These are not formal Type-I calibration results.

## 7. Branch divergence

The review branch is 201 commits ahead of main.
Main is 7 commits ahead of the review branch.
The branches have diverged from the recorded merge base.

No merge, force push, or main-branch mutation is authorized
by this report.

## 8. Required next actions

1. Correct the occurrence-level discovery classifier.
2. Generate a separate occurrence ledger for main.
3. Manually adjudicate all high-priority workflow occurrences.
4. Trace direct and indirect callers for all code-path occurrences.
5. Test every relevant unauthorized path for fail-closed behavior.
6. Bind every authorized entry point to an exact protocol
   identity, commit, matrix hash, source hashes, and decision.
7. Reconcile V3 legacy behavior with the V4 candidate design.
8. Obtain attributable independent human statistical review.
9. Preserve NOT_FROZEN and NOT_AUTHORIZED until all required
   decisions are evidenced.

## 9. Non-negotiable state

No change is made to:
- scientific acceptance thresholds;
- historical calibration results;
- claim_support;
- promotion_authority;
- confirmatory_execution_authorized;
- protocol freeze state.

Engineering success is not scientific approval.

Final disposition:

INVENTORY_RECONCILED;
MANUAL_CLASSIFICATION_OPEN;
MAIN_LEDGER_PENDING;
CALL_GRAPH_REVIEW_PENDING;
LEGACY_PATH_REVIEW_PENDING;
PROTOCOL_NOT_FROZEN;
CONFIRMATORY_EXECUTION_NOT_AUTHORIZED;
CLAIM_NOT_ESTABLISHED.
