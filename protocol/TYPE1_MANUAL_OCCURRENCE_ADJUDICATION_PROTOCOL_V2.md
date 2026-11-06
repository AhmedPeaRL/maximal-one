# Type-I V4 — Manual Occurrence Adjudication Protocol V2

## Status

`REVIEW_PROTOCOL_ONLY_NOT_ADJUDICATION_NOT_AUTHORIZATION`

This document defines how to adjudicate every discovered occurrence. It does not classify any occurrence, close any record, approve V4, authorize calibration, or support the HCM claim.

## 1. Scope and immutable populations

Maintain two distinct populations and never merge their identities:

- Review target: 1,711 occurrence records from the exact target commit inventory.
- Main comparison: 583 occurrence records from the separately identified main commit.

These are branch-specific populations. Do not assume that their sum is a count of unique repository-wide occurrences. Preserve each ledger's exact `occurrence_id`, commit SHA, path, line, matched text, inventory SHA-256, and ref identity.

For the supplied evidence, the review ledger is bound to `10a9d85551cd287ca051feb60afa0343fb0f001c`; the main ledger is bound to `fe0daded51229ed88d449c2eb68252455fd4ad7c`. The current adjudication overlay contains zero records. All 1,711 review rows and all 583 main rows remain `UNKNOWN`, `OPEN`, and `PENDING`.

## 2. Unit of review

The unit is one exact occurrence, not one file and not one keyword family. Each record must be adjudicated independently, even when multiple rows occur in the same file or line.

The automated inventory label is discovery metadata only. It must never be copied into `manual_classification` without independent inspection.

## 3. Required fields for every occurrence

Each adjudication record must include:

1. `occurrence_id` — exact immutable ID from the ledger.
2. `inventory_sha256` and `review_commit_sha` — bind the decision to the exact evidence snapshot.
3. `manual_classification` — one of `EXECUTION_ENTRY_POINT`, `EXECUTION_CALLER`, `WORKFLOW_TRIGGER_OR_CONTROL`, `AUTHORIZATION_GUARD`, `TEST_ONLY`, `DOCUMENTATION_ONLY`, `HISTORICAL_OR_SUPERSEDED`, `DIAGNOSTIC_ONLY`, `POLICY_OR_CONFIGURATION`, `NON_EXECUTABLE_REFERENCE`, or `UNRESOLVED`.
4. `can_influence_execution` — `YES`, `NO`, or `UNRESOLVED`, with rationale.
5. `direct_caller_or_workflow_step` — exact symbol, workflow/job/step, or `NONE` with evidence.
6. `indirect_call_path` — ordered path from entry point to occurrence/runner, or `NO_PATH_FOUND` with search method and scope. Never infer absence from a bounded text window.
7. `runner_entry_point_or_command` — exact command, module, callable, or `NOT_APPLICABLE`.
8. `trigger_conditions_and_branch_restrictions` — event, inputs, `if:` conditions, branch/tag filters, environment gates, manual dispatch, and caller workflow conditions.
9. `matrix_and_protocol_consumed` — exact matrix/spec/config files and relevant parameters consumed at runtime, or `NOT_APPLICABLE` with rationale.
10. `authorization_guard_and_execution_order` — ordered sequence of all guards before execution, including where each guard is evaluated.
11. `guard_fails_closed` — `YES`, `NO`, or `UNRESOLVED`, with a negative-test reference.
12. `negative_test` — test name, injected invalid condition, expected failure, observed exit/result, and artifact/run evidence. If no test exists, state `MISSING`.
13. `test_run_job_artifact_commit` — immutable links/IDs and exact commit for the evidence.
14. `historical_diagnostic_proposed_governance_status` — explicitly distinguish these roles; do not infer status from text alone.
15. `reviewer`, `reviewer_role`, `conflict_statement`, `reviewed_at_utc`, and `rationale`.
16. `status` — `OPEN` or `CLOSED`; `reviewer_disposition` — `ADJUDICATED` or `PENDING`.
17. `closure_evidence` — mandatory for `CLOSED`; must point to exact source lines, caller/trigger evidence, guard-order proof, and negative test.

## 4. Classification rules

- A string naming a runner is not necessarily executable; trace the actual workflow or program invocation.
- A workflow `uses:` action is not automatically a calibration runner.
- A test that asserts a guard exists is not proof that the production path invokes that guard first.
- A control field in JSON or documentation is not proof that runtime code consumes it.
- A `BLOCKED` string or `exit 1` line is not proof of fail-closed behavior for every route.
- A historical threshold mention is not a current acceptance rule.
- A diagnostic or pilot path is not formal calibration.
- If call graph, dynamic dispatch, shell indirection, reusable workflow, composite action, import, or environment behavior is unresolved, classify `UNRESOLVED` and leave `OPEN`.

## 5. Guard-order evidence

For any occurrence capable of influencing execution, record the actual order:

`event/dispatch -> branch/ref restriction -> input validation -> authorization-state read -> freeze/approval gate -> provenance/identity checks -> runner invocation -> result gate -> artifact/promotion step`.

This is a checklist, not an assumed architecture. Record only the order actually demonstrated in the exact snapshot. If a required guard is absent or occurs after the runner, mark the record `OPEN` and document the defect.

## 6. Negative tests

At minimum, execution-capable routes require tests for:

- wrong branch/ref;
- wrong target commit;
- mismatched inventory source commit;
- wrong inventory artifact ID or wrong artifact-producing run;
- altered inventory SHA-256;
- missing/expired artifact;
- missing/invalid authorization state;
- `NOT_FROZEN` state;
- confirmatory authorization false;
- promotion authority false;
- malformed or missing matrix/protocol;
- runner invoked through direct and indirect caller paths;
- failed guard must stop before runner side effects;
- attempt to resume from a mismatched checkpoint/manifest.

A test is evidence only for the exact path and conditions it executes. Record run, job, artifact, commit, expected result, observed result, and log location.

## 7. Reviewer independence and batching

The repository author may prepare evidence and propose classifications, but cannot be the sole independent adjudicator of the same work. The reviewer must disclose relevant authorship, financial, supervisory, collaboration, and intellectual conflicts.

Use immutable batches of at most 25–50 occurrence IDs. Each batch records first/last ID, count, inventory SHA, reviewer, date, and a SHA-256 digest of the batch input. No batch may be silently renumbered or regenerated against a changed inventory.

For high-impact execution and authorization occurrences, require a second reviewer. Disagreements remain `OPEN` until resolved in a signed decision record; never average or silently overwrite classifications.

## 8. Closure rule

An occurrence can be `CLOSED` only when all applicable fields are complete, the exact path is traced, guard order is evidenced, required negative tests pass, and a reviewer has recorded a rationale. `UNRESOLVED`, missing caller evidence, missing negative tests, and missing closure evidence must remain `OPEN`.

`CLOSED` means the occurrence has been reviewed and its role documented. It does not mean the underlying code is safe, the protocol is approved, or the scientific claim is true.

## 9. Completion gates

A population is adjudication-complete only if:

- every expected occurrence ID appears exactly once;
- no extra or duplicate IDs exist;
- all records are `ADJUDICATED` or explicitly remain `OPEN` with reasons;
- all execution-capable and authorization-related rows have second-review status;
- all closed rows have closure evidence;
- the overlay is bound to the exact inventory SHA and commit;
- independent reviewer sign-off is present.

Do not represent a partially adjudicated population as complete. Report exact counts by status and class.

## 10. Non-authority safeguards

Throughout this work:

- protocol freeze remains `NOT_FROZEN`;
- formal calibration remains `NOT_AUTHORIZED`;
- confirmatory execution remains `NOT_AUTHORIZED`;
- claim support remains `false`;
- promotion authority remains `false`.

No manual occurrence review can change these states. Separate statistical review, prospective protocol decision, freeze decision, and execution authorization are required.
