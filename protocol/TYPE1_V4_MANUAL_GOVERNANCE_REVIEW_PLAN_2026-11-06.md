# Type-I V3/V4 Manual Governance Review Plan — 2026-11-06

## 1. Snapshot identity

- Repository: `AhmedPeaRL/maximal-one`
- Review branch: `review/type1-v4-remediation`
- Commit: `5b814ddf529b04b3ea9fda908373c3676eb647c1`
- Inventory artifact: workflow 42106008761, artifact 13451387326
- Exact review snapshot: workflow 42106395007, artifact 13451792355
- Inventory JSON SHA-256: `cf3d05b060edbc1a813b5cfc3b96ef1ee52ccb4fc40dab60629e228a8aba0c74`
- Snapshot contains 262 selected files; 262/262 manifest hashes match the nested snapshot ZIP.
- Manual adjudication overlay: zero records.

## 2. What reconciliation proves

The review-branch ledger has 1,649 occurrence records. The main-branch ledger has 583. Both reconciliation files report `RECONCILED`, with matching counts, no missing IDs, no extra IDs, no duplicate IDs, and no identity mismatches.

This proves occurrence identity and coverage only. It does not prove:
- that a runner cannot be reached indirectly;
- that an authorization guard executes before every output or execution path;
- that every path consumes the intended protocol;
- that every negative test exercises the real path;
- that the protocol is approved or frozen;
- that the scientific result is valid.

All 1,649 review-branch records remain `OPEN`; manual classification is `UNKNOWN`; reviewer disposition is `PENDING`; `can_influence_execution` and `guard_fails_closed` remain `UNKNOWN`.

All 583 main-branch records remain in the same open/unknown/pending state.

## 3. Highest-priority execution-path candidates

The automated inventory identified three candidate occurrences. These are discovery flags, not human conclusions.

### Candidate A — Runtime pilot

- Path: `.github/workflows/type1-calibration-runtime-pilot.yml`
- Occurrence: `HEAD/2f8523fcf7c5/73/4`
- Runner command: `python -m analysis.type1_calibration_pilot`
- Workflow uses `scripts/type1_runtime_pilot_branch_guard.py` before output creation and before runner invocation.
- Guard restricts the workflow to `refs/heads/review/type1-v4-remediation`.
- Test: `tests/test_type1_runtime_pilot_branch_guard.py`.
- The workflow is explicitly an exploratory pilot and runs two outer replicates with 200 surrogates for one V4 draft scenario.
- It is not formal calibration.
- Manual disposition remains pending.

Required reviewer action:
1. Inspect the workflow from trigger to upload.
2. Inspect the guard and runner entry point.
3. Verify that the guard cannot be bypassed by direct module invocation.
4. Verify that all pilot outputs remain non-authorizing.
5. Confirm the exact matrix consumed is the V4 design draft and that no pilot result changes the formal matrix or acceptance rule.
6. Record the exact negative tests and their evidence.

### Candidate B — Cross-runner worker 0

- Path: `.github/workflows/type1-v4-cross-runner-worker-order.yml`
- Occurrence: `HEAD/40d0253a5dd6/60/6`
- Runner command: `python -m analysis.calibrate_null_type1_scenario`
- Invocation includes `--engineering-test`.
- Bounded test: six replicates, one scenario, 1,000 surrogates per replicate.
- Manual disposition remains pending.

### Candidate C — Cross-runner worker 1

- Path: `.github/workflows/type1-v4-cross-runner-worker-order.yml`
- Occurrence: `HEAD/40d0253a5dd6/123/9`
- Runner command: `python -m analysis.calibrate_null_type1_scenario`
- Invocation includes `--engineering-test`.
- This is a second occurrence in the same workflow and must be adjudicated separately because its job/step/branch context may differ.
- Manual disposition remains pending.

For B and C, verify:
1. exact trigger and branch restriction;
2. the engineering-only flag is mandatory and cannot be omitted through another workflow path;
3. the runner rejects formal execution while `V4_APPROVED` is false;
4. all output flags remain false;
5. the merge and worker paths preserve identity, index coverage, and hashes;
6. no job or downstream workflow treats engineering success as calibration approval.

## 4. Next review tier

After the three execution-path candidates, manually inspect:
1. all `CODE_PATH_REQUIRES_CALL_GRAPH_REVIEW` occurrences (248 in the review inventory);
2. all `WORKFLOW_CONTROL_PATH` occurrences (84);
3. any additional occurrence whose path can reach a calibration entry point or mutate protocol/authorization state;
4. relevant tests, negative controls, and artifact-upload paths.

The inventory also contains references and documentation occurrences that may not influence execution. They may be classified as non-executable only after the reviewer records the local context and reason. Do not classify an occurrence from its label alone.

## 5. Required fields for each manual adjudication

Each reviewed occurrence should have:
- exact occurrence ID;
- exact commit and file hash;
- manual classification;
- reviewer disposition;
- direct caller/workflow step;
- indirect call path;
- runner entry point or command;
- trigger conditions and branch restrictions;
- protocol/matrix consumed;
- authorization guard and its execution order;
- whether the occurrence can influence execution;
- whether the guard fails closed;
- negative test and exact test run/job/artifact;
- closure evidence;
- unresolved reason, if any.

Use explicit values such as `VERIFIED_EXECUTION_PATH`, `VERIFIED_NON_EXECUTABLE_REFERENCE`, `VERIFIED_TEST_ONLY`, or `UNRESOLVED`. Avoid converting `UNKNOWN` to `NO` without evidence.

## 6. Required negative controls

At minimum, the reviewer should verify:
- `main` is rejected by the runtime-pilot branch guard;
- the authorized review branch is accepted only for the explicitly declared pilot path;
- direct runner invocation without authorization is rejected;
- V3 cannot invoke the V4 runner;
- V4 engineering mode cannot set formal calibration, claim support, or promotion flags;
- changing any resume identity field is rejected without mutating the original checkpoint or manifest;
- missing, duplicate, overlapping, out-of-range, or hash-invalid shards are rejected;
- no workflow artifact or downstream job can transform a pilot or engineering artifact into an authorization record.

## 7. Completion rule

Do not describe the governance audit as complete until:
- every execution-capable candidate is manually adjudicated;
- every call-graph-review occurrence relevant to the calibration runner is closed or explicitly unresolved;
- all control-path orderings are inspected;
- negative tests are linked to exact workflow runs and artifacts;
- the manual adjudication overlay is populated and hash-bound to the exact inventory and commit;
- unresolved paths are reported rather than silently treated as safe.

The current automated inventory is a useful discovery and reconciliation artifact. It is not a completed manual governance review.
