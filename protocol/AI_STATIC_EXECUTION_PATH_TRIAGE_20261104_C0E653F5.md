# AI-Assisted Static Execution-Path Triage — 2026-11-04

## 1. Review identity and authority

- Repository: `AhmedPeaRL/maximal-one`
- Review branch: `review/type1-v4-remediation`
- Exact reviewed commit: `c0e653f524e210d4ac8c0589260127cfe71e0de8`
- Governance inventory run: `41757974155`
- Governance inventory job: `126338492574`
- Governance inventory artifact: `13288133721`
- Snapshot run: `41758174557`
- Snapshot job: `126339151936`
- Snapshot artifact: `13288914393`

This document is an AI-assisted static technical triage record. It is not a human adjudication, independent statistical review, protocol approval, execution authorization, or scientific claim.

No reviewer identity is attributed to an AI system.

## 2. Current inventory identity and scope

Review-branch inventory:

- Inventory paths: 250
- Occurrences: 1,603
- Inventory JSON SHA-256: `e2f982532aecb22cb75795477d1ff6dd82b24173d34110180af4d8aea3432f6f`
- Occurrence ledger SHA-256: `e606503cd73b05793d6d8cb2269fc39695d01737070a22fc120c65384aa3f021`
- Reconciliation SHA-256: `a3662880d2f46731dbf9b5c441861e5b93b9c04700e125b7077600f9971c8996`

Main-branch inventory:

- Occurrences: 581
- Main ledger SHA-256: `89b1fba99ba791d21112623d406e01a87f93f465374551fd467c6501a6e808d2`

Review-branch automated classification totals:

- PROTOCOL_OR_DOCUMENTATION_REFERENCE: 415
- GOVERNANCE_REFERENCE: 385
- CODE_PATH_REQUIRES_CALL_GRAPH_REVIEW: 243
- TEST_OR_GUARD: 186
- POLICY_OR_HISTORICAL_REFERENCE: 143
- WORKFLOW_REFERENCE: 131
- WORKFLOW_CONTROL_PATH: 83
- OTHER_REFERENCE: 14
- EXECUTION_CAPABLE_WORKFLOW_CANDIDATE: 3

All 1,603 review-branch records remain:

- `manual_classification=UNKNOWN`
- `status=OPEN`
- `reviewer_disposition=PENDING`

Reconciliation is `RECONCILED`, with matching identity and counts and no missing, extra, or duplicate occurrence IDs.

Reconciliation does not establish correctness of manual decisions or execution safety.

## 3. Priority occurrence A — Runtime pilot

Occurrence ID:

`HEAD/2f8523fcf7c5/73/4`

Source:

`.github/workflows/type1-calibration-runtime-pilot.yml`

Matched invocation at line 73:

`python -m analysis.type1_calibration_pilot`

Relevant source identities (Git blob SHA):

- Workflow: `5e18ec4db402e6d7719e17ecf321ba4861ec0274`
- Runner: `71585095128c650e5fa73f2aba3482830e1ab766`
- Branch guard: `046e06d82ce23e450a351de30b2747d1b59b8468`
- Branch-guard tests: `b04c809f5f8ade850ab6ae6fba293dc0baa4fc6c`

### Static evidence observed

1. The workflow supports `workflow_dispatch`.
2. It checks out the selected repository state.
3. It runs `scripts/type1_runtime_pilot_branch_guard.py` before output-directory creation and runner invocation.
4. It verifies `git rev-parse HEAD` against `GITHUB_SHA`.
5. The guard accepts only `refs/heads/review/type1-v4-remediation`.
6. The Python runner calls `require_authorized_branch()` at the beginning of `main()`, before argument parsing and simulation.
7. The pilot requires the V4 matrix to remain in draft status.
8. The pilot requires exactly 200 surrogates and limits total repetitions to 20.
9. The workflow command requests two repetitions and 200 surrogates.
10. Pilot artifacts explicitly retain `formal_calibration_pass=false`, `claim_support=false`, and `promotion_authority=false`.

### Existing negative-test coverage

`tests/test_type1_runtime_pilot_branch_guard.py` contains tests for:

- Unauthorized `main` branch rejection without output creation.
- Authorized review-branch acceptance.
- Direct runner-entry rejection on an unauthorized branch.
- Workflow guard ordering before output creation and runner invocation.

### Preliminary technical assessment

Suggested technical category: `EXECUTION_PATH_CANDIDATE`

This is a direct exploratory runner invocation with branch and checkout checks in the workflow and an entry-point branch guard in the Python runner.

### Remaining closure requirements

- Execute the candidate-specific test module in an attributable CI run.
- Preserve the exact test run, job, commit, and log.
- Review the full pilot call graph and any alternate entry points.
- Verify rejection behavior when `GITHUB_REF` is missing or incorrect.
- Verify exact commit identity and artifact identity in the resulting pilot artifact.
- Confirm that no pilot artifact can be interpreted as formal Type-I calibration.

Human manual classification: `UNKNOWN`

Human reviewer disposition: `PENDING`

Status: `OPEN`

No closure is claimed.

## 4. Priority occurrences B and C — Cross-runner engineering path

Occurrence B:

`HEAD/40d0253a5dd6/60/6`

Occurrence C:

`HEAD/40d0253a5dd6/123/9`

Source:

`.github/workflows/type1-v4-cross-runner-worker-order.yml`

Relevant source identities (Git blob SHA):

- Workflow: `88ae00a38d7a5cb4661c64cf4827c7dae7408da2`
- Scenario runner: `cfab9df289e33e6d5980b92cb8c48e25cb45f018`
- Workflow branch-guard tests: `69d5c7f0c6e882352c78cebb82450c0543baeabb`

### Static evidence observed

1. The workflow supports `workflow_dispatch`.
2. It also supports a path-filtered push trigger on `review/type1-v4-remediation`.
3. The `connected-reference`, `independent-workers`, and `compare` jobs each verify the expected review branch.
4. Each job verifies `git rev-parse HEAD` against `GITHUB_SHA`.
5. The branch and checkout checks precede Python setup and the respective execution commands.
6. Both calibration runner invocations explicitly pass `--engineering-test`.
7. The runner dispatches to `engineering_main()` only when that flag is present.
8. Engineering mode is restricted to the declared AR(2) baseline, at most six repetitions, exactly 1,000 surrogates, the candidate sample size, and candidate seed.
9. Engineering artifacts explicitly preserve false formal-calibration, claim-support, promotion, and confirmatory-authorization flags.
10. The formal runner currently has `V4_APPROVED = False`.
11. The formal acceptance rule and maximum acceptable Wilson upper bound remain unresolved.

### Existing negative-test coverage

`tests/test_type1_cross_runner_workflow_branch_guard.py` contains tests for:

- Branch and exact-checkout checks in all three jobs.
- Guard ordering before Python setup and runner commands.
- Explicit engineering-only invocation.

### Preliminary technical assessment

Suggested technical category for both occurrences: `EXECUTION_PATH_CANDIDATE`

Both are direct runner invocations in a bounded engineering workflow. Their workflow-level branch and checkout checks are visible in source.

The `--engineering-test` flag is not authentication by itself. Direct local invocation is a distinct route and must be considered in the call-graph review. The engineering route must remain explicitly separate from formal authorization.

### Remaining closure requirements

- Execute the candidate-specific workflow-guard tests in an attributable CI run.
- Trace all direct and indirect callers of `analysis.calibrate_null_type1_scenario`.
- Verify all invocations of `engineering_main()` and `formal_main()`.
- Verify that missing or altered authorization cannot reach formal simulation.
- Verify that wrong branch and mismatched commit fail before simulation.
- Test invalid engineering parameters, including excess repetitions, wrong scenario, wrong surrogate count, wrong sample size, and wrong seed.
- Verify checkpoint and worker artifact identity, manifest digest, and merge rejection behavior.
- Preserve the actual workflow run, job, artifacts, logs, and commit identity.

Human manual classification: `UNKNOWN`

Human reviewer disposition: `PENDING`

Status: `OPEN`

No closure is claimed.

## 5. Workflow-run evidence boundary

The supplied successful runs are:

- Governance inventory run `41757974155`.
- Exact-review snapshot run `41758174557`.

The governance run completed its 60-test suite successfully.

The snapshot run completed its six inventory-scope tests successfully.

The logs do not establish execution of the candidate-specific runtime-pilot branch-guard tests or cross-runner workflow branch-guard tests.

Neither supplied run is evidence that the runtime-pilot or cross-runner simulation workflow executed.

This distinction must remain explicit in every downstream report.

## 6. Snapshot packaging finding

The exact-review snapshot contains:

- `manifest.json`
- `SHA256SUMS.txt`

The manifest declares 257 present files and 1,603 inventory occurrences.

All 257 manifest paths match the 257 checksum paths, and all corresponding SHA-256 values match.

The snapshot does not contain the 257 source-file contents.

The current `scripts/create_type1_review_snapshot.py` defines a `create_self_contained_archive()` helper, but the current `main()` path writes only `manifest.json` and `SHA256SUMS.txt`. The current snapshot workflow does not invoke the helper.

Therefore:

`HASH_MANIFEST_VERIFICATION_PASSED`

`SELF_CONTAINED_SOURCE_ARCHIVE_NOT_PRODUCED`

The helper's existence is not evidence that a source archive was created.

## 7. Mandatory next gates

1. Preserve the two downloaded artifacts and their exact hashes.
2. Run the candidate-specific guard and negative-gate tests in a dedicated workflow.
3. Record exact run, job, commit, logs, and test outcomes.
4. Complete direct and indirect call-graph review for all three priority occurrences.
5. Obtain attributable human technical adjudication for the three occurrences.
6. Keep every occurrence OPEN until its evidence and reviewer decision are complete.
7. Expand the review to the 83 workflow-control occurrences and 243 code-path occurrences.
8. Review the 186 test/guard occurrences for actual enforcement, coverage, and false assurance.
9. Continue through governance, protocol/documentation, policy/historical, workflow-reference, and other occurrences.
10. Generate a self-contained source archive if external review requires source contents, and verify extracted files against the manifest.
11. Obtain independent human statistical-methods review of the exact protocol, matrix, and acceptance rule.
12. Preserve historical Type-I failures and all previous acceptance-rule decisions.
13. Keep protocol freeze, formal calibration authorization, confirmatory execution authorization, claim support, and promotion authority disabled until their separate gates are satisfied.

## 8. Decision

`INVENTORY_AND_RECONCILIATION_PASSED`

`PRIORITY_EXECUTION_PATHS_STATICALLY_TRIAGED`

`CANDIDATE_SPECIFIC_GUARD_TEST_EXECUTION_PENDING`

`HUMAN_OCCURRENCE_ADJUDICATION_PENDING`

`CALL_GRAPH_CLOSURE_PENDING`

`SELF_CONTAINED_SOURCE_ARCHIVE_NOT_PRODUCED`

`PROTOCOL_NOT_FROZEN`

`FORMAL_CALIBRATION_NOT_AUTHORIZED`

`CONFIRMATORY_EXECUTION_NOT_AUTHORIZED`

`CLAIM_SUPPORT_FALSE`

`PROMOTION_AUTHORITY_FALSE`

This document records evidence and unresolved work. It does not grant execution authority or close any occurrence.
