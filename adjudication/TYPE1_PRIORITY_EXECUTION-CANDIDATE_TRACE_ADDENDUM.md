# Type-I Priority Execution-Candidate Trace Addendum — 2026-11-10

Status: AI_TRACE_PROPOSAL_ONLY  
Human adjudication: PENDING  
Authority: REVIEW EVIDENCE ONLY

Protocol freeze: NOT_FROZEN  
Formal calibration: NOT_AUTHORIZED  
Confirmatory execution: NOT_AUTHORIZED  
Claim support: FALSE  
Promotion authority: FALSE

## 1. Exact evidence identity

Repository: `AhmedPeaRL/maximal-one`

Main comparison commit: `00bbd1fbd6df41b3e988ace75c480ea6232cfb86`

Target inventory commit: `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`

Review branch: `review/type1-v4-remediation`

Review branch head at inspection: `c82ddeac792332a5b40002e6c98106f70e3121e9`

Inventory workflow-definition commit: `4cd9197f7bbe418bb064ddcc1d4e8173e4c559ca`

Target inventory SHA-256: `88222e3178bc62854ffb8d1fa961c1fb4cfe582c9ff1082878ab759e011cc635`

Target occurrence-ledger SHA-256: `5aaa4a796fe99eb1aeb9f803aba1517d5724c5e92b6c0400098f2e38d858651c`

Main occurrence-ledger SHA-256: `a16b2133d495e9a018d77f43eeefd39c417fb0995cc6d3eb43ec5328d4bfe4d0`

Inventory run: `42790631758`  
Inventory artifact: `13750094091`

Snapshot run: `42791517735`  
Snapshot artifact: `13751029604`

The target ledger contains 1,800 occurrences. The main ledger contains 633 occurrences. Both reconciliations report `RECONCILED`, with no missing IDs, extra IDs, duplicate IDs, or identity mismatches.

All target rows remain:

- `manual_classification=UNKNOWN`
- `status=OPEN`
- `reviewer_disposition=PENDING`

Reconciliation establishes identity and accounting coverage only. It does not establish manual classification, call-graph completeness, guard correctness, or scientific validity.

## 2. Snapshot integrity

The target snapshot identifies:

- Target commit: `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`
- Inventory workflow definition: `4cd9197f7bbe418bb064ddcc1d4e8173e4c559ca`
- Snapshot workflow definition: `4cd9197f7bbe418bb064ddcc1d4e8173e4c559ca`
- Selected files: 289
- Present files: 289
- Missing required paths: 0
- Missing scope paths: 0
- Manual adjudication overlay records: 0

Self-contained snapshot ZIP SHA-256:

`0b6f1c656b9ab7e5e44f61074ed49e24e196b8557f14f236fadbaddf7d7a6496`

Snapshot manifest SHA-256:

`1636a1eea6618817392f34ae9dde9961de6de57c8dfd74dc6b12e68bcf3a06ab`

Extraction verification:

- `verified=true`
- `checked_file_count=292`
- `errors=[]`

The snapshot is a valid source-bound package for the target commit. It contains no manual adjudication overlay records.

## 3. Priority occurrence A — Runtime pilot

Occurrence ID:

`refs/audit/target/2f8523fcf7c5/73/4`

Source:

`.github/workflows/type1-calibration-runtime-pilot.yml`

Source line: 73

Invocation:

`python -m analysis.type1_calibration_pilot`

### Static call trace

`workflow_dispatch`
→ workflow branch guard  
→ exact checkout identity check (`git rev-parse HEAD == GITHUB_SHA`)  
→ `analysis.type1_calibration_pilot.main()`  
→ `require_authorized_branch()`  
→ pilot matrix and parameter checks  
→ `execute_attempt()`  
→ `generate_ar()`  
→ `estimate_alpha()`  
→ `parametric_short_memory_null()`  
→ pilot artifact and manifest.

The pilot consumes:

`protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_DRAFT.json`

The declared workflow command uses:

- Scenario: `gaussian_ar2_inband_f_0_02_radius_0_90_n3328`
- Start index: 0
- Stop index: 2
- Total repetitions: 2
- Surrogates per replicate: 200
- Master seed: 20261021

### Guard assessment

The workflow checks the authorized review branch before Python setup, output creation, and runner invocation. It also verifies exact checkout identity.

The Python entry point calls `require_authorized_branch()` before argument parsing and simulation.

However, the Python branch guard itself checks `GITHUB_REF`; it does not independently require `GITHUB_ACTIONS=true` or verify `git rev-parse HEAD` against `GITHUB_SHA`. The workflow performs the exact checkout check, but a direct local invocation with a manually supplied environment variable is a separate path that is not excluded by this entry-point guard alone.

### Test and run evidence

`tests.test_type1_runtime_pilot_branch_guard` is included in priority guard verification run `42786690942`, job `129729584482`.

That overall job failed because two other negative-gate assertions expected the previous rejection message. The run does not establish a standalone runtime-pilot execution.

No standalone runtime-pilot workflow run or pilot artifact is claimed in the supplied evidence.

### Preliminary AI trace assessment

The occurrence is a direct exploratory runner invocation.

The trace reaches the endpoint and null implementation, but it does not establish formal calibration authority.

Human classification: `UNKNOWN`  
Human disposition: `PENDING`  
Status: `OPEN`

Required human review:

- Verify the local direct-invocation boundary.
- Verify all alternate pilot entry points.
- Verify exact artifact and manifest identity for any future pilot run.
- Confirm that no pilot output can be treated as formal Type-I calibration.

## 4. Priority occurrence B — Connected engineering reference

Occurrence ID:

`refs/audit/target/40d0253a5dd6/60/6`

Source:

`.github/workflows/type1-v4-cross-runner-worker-order.yml`

Source line: 60

Invocation:

`python -m analysis.calibrate_null_type1_scenario --engineering-test ...`

### Static call trace

`workflow_dispatch` or path-filtered push on the review branch  
→ connected-reference job  
→ review-branch guard  
→ exact checkout identity check  
→ `analysis.calibrate_null_type1_scenario.main()`  
→ `engineering_main()`  
→ `require_authorized_branch()`  
→ `GITHUB_ACTIONS == true` check  
→ `GITHUB_SHA` and checked-out HEAD equality check  
→ engineering argument and parameter restrictions  
→ `execute_attempt()`  
→ `generate_ar()`  
→ `estimate_alpha()`  
→ `parametric_short_memory_null()`  
→ engineering artifact and manifest.

The engineering runner uses the V4 candidate matrix through `analysis.calibrate_null_type1.py`.

The connected-reference command uses:

- Scenario: `gaussian_ar2_phi_0_45_minus_0_10_n3328`
- Repetitions: 6
- Surrogates per replicate: 1,000
- Sample size: 3,328
- Master seed: 20261021
- Replicate range: 0–6

The `--engineering-test` path is explicitly separated from `formal_main()`.

### Guard assessment

The workflow checks branch and exact checkout identity before setup and execution.

The engineering entry point independently checks:

- Authorized branch
- GitHub Actions context
- Presence of `GITHUB_SHA`
- Exact equality between `GITHUB_SHA` and checked-out HEAD
- Explicit `--engineering-test`
- Declared scenario and engineering parameter limits

The engineering artifact explicitly preserves false formal-calibration, confirmatory-authorization, claim-support, and promotion-authority fields.

### Run evidence

Workflow run: `42783734065`  
Connected-reference job: `129719706947`  
Reference artifact: `13748246463`  
Comparison artifact: `13748361580`

The connected reference matched all six worker replicate records.

This run used commit:

`7731c56dcdfd67d3a2a8c0edd2190e3202cd5138`

The workflow file Git blob identity is unchanged between target commit `ad106...` and tested commit `7731...`. The scenario-runner file changed in `7731...` because the formal path gained a preflight call; the commit diff adds that preflight to `formal_main()`, while the engineering entry-point body is unchanged in that diff.

This remains later-commit engineering evidence, not a claim that the exact target commit `ad106...` was executed.

Human classification: `UNKNOWN`  
Human disposition: `PENDING`  
Status: `OPEN`

## 5. Priority occurrence C — Distributed worker replicate path

Occurrence ID:

`refs/audit/target/40d0253a5dd6/123/9`

Source:

`.github/workflows/type1-v4-cross-runner-worker-order.yml`

Source line: 123

Invocation:

`python -m analysis.calibrate_null_type1_scenario --engineering-test ...`

### Static call trace

`workflow_dispatch` or path-filtered push on the review branch  
→ independent-workers matrix job  
→ branch and exact checkout identity checks  
→ `analysis.calibrate_null_type1_scenario.main()`  
→ `engineering_main()`  
→ branch, GitHub Actions, and exact HEAD checks  
→ engineering parameter restrictions  
→ `execute_attempt()` for the assigned replicate  
→ `generate_ar()`  
→ `estimate_alpha()`  
→ `parametric_short_memory_null()`  
→ worker artifact and manifest  
→ comparison job.

The matrix assigns one replicate index to each worker. The six worker jobs cover indices 0 through 5.

### Guard assessment

Each worker job performs the branch and exact checkout checks before Python setup and runner invocation.

The runner independently performs the engineering-entry checks described for occurrence B.

This is a distinct invocation occurrence from line 60. It must remain a separate ledger row even though both occurrences reach the same engineering entry point.

### Run evidence

Workflow run: `42783734065`

Worker jobs:

- Worker 0: `129719707265`
- Worker 1: `129719707185`
- Worker 2: `129719707474`
- Worker 3: `129719707519`
- Worker 4: `129719707331`
- Worker 5: `129719707320`

Comparison job: `129722836393`

Worker artifacts:

- `13748335425`
- `13748425210`
- `13747217846`
- `13748235383`
- `13747566575`
- `13747755573`

Comparison artifact:

`13748361580`

All six worker records matched the connected reference.

All seven reported platform identities were:

`Linux-7.0.0-1017-azure-x86_64-with-glibc2.39`

The runner instance IDs were distinct, but the platform identity was the same. This establishes worker/runner execution equivalence on the same platform, not cross-platform equivalence and not independent scientific replication.

Human classification: `UNKNOWN`  
Human disposition: `PENDING`  
Status: `OPEN`

## 6. Supporting engineering evidence boundary

The following successful engineering runs are relevant:

- Run `42783734080`, artifact `13748013008`: worker assignment matrix comparison; `PASS_ENGINEERING_ONLY`; no mismatches.
- Run `42783733930`, artifact `13751662923`: official runner connected/sharded/merged/resumed equivalence; engineering-only.
- Run `42783734154`, artifact `13748090699`: 19 CLI resume-identity mismatch fields rejected.
- Run `42786690942`, artifact `13749118741`: 23 CLI resume-identity mismatch fields rejected; the CLI identity subtest artifact passed, but the overall priority guard job failed on two other assertions.

The full-path run `42783734020`, job `129719707011`, failed because a test expected the older message:

`BLOCKED: V4 matrix is not approved`

The new preflight returned:

`BLOCKED: matrix has no independently approved_design. Candidate dimensions cannot authorize execution.`

The test failure is a message-contract mismatch. The run did not produce its expected full-path artifact because the test failure stopped later steps.

None of these engineering results is formal Type-I calibration.

## 7. Formal preflight findings

Current governance records remain:

- Matrix status: `DRAFT_PENDING_REMEDIATION_AND_INDEPENDENT_REVIEW`
- Freeze decision: `NOT_APPROVED`
- Freeze state: `NOT_FROZEN`
- Execution authorization: `NOT_AUTHORIZED`
- `V4_APPROVED`: `False`
- Confirmatory execution: `false`
- Claim support: `false`
- Promotion authority: `false`

The current preflight correctly blocks because the matrix has no `approved_design`.

A separate source-of-truth issue remains: `analysis/calibrate_null_type1.py` still reads `candidate_dimensions_not_frozen` to populate runtime constants. A future approved protocol must migrate the formal runner to `approved_design` only, with no fallback to candidate dimensions.

The preflight also needs additional equality checks before any future approval:

- Authorized R must equal approved-design R.
- Authorized M must equal approved-design M.
- Authorized sample size and burn-in must equal the approved design.
- Authorized master seed and seed schedule must equal the approved design.
- Authorized acceptance rule must equal the approved design.
- Authorized invalid-attempt policy must equal the approved design.
- Authorized entry point must equal the actual invoked formal entry point.
- The exact workflow definition and workflow identity must be bound to the authorization.
- Test evidence must be attributable to the exact reviewed commit and source hashes.

The present helper checks that several fields exist, but does not yet establish all of those equalities.

Do not change `V4_APPROVED=False` or authorize execution.

## 8. Batch-generation implementation boundary

The target ledger tracked at:

`evidence/occurrence_level_manual_ledger.json`

has Git blob SHA-1:

`1b4a5bb63e5840876629ea61a23fc688ae6c4b33`

Its SHA-256 is:

`5aaa4a796fe99eb1aeb9f803aba1517d5724c5e92b6c0400098f2e38d858651c`

The generator in `adjudication/generate_target_batches.py` uses this source path and the expected target inventory metadata.

The current branch contains the generator and `tests/test_type1_target_batch_generation.py`.

The generated directory is not present in the current branch:

`adjudication/target_1800_batches/`

The test suite was reproduced locally against the current generator source and passed four tests. A local generation check produced 72 batches covering 1,800 unique occurrence IDs, with batch hashes matching the register and no adjudication authority.

This local reproduction is not a GitHub Actions run and does not establish that generated files have been committed.

The generator should be run in a dedicated branch-restricted workflow that verifies the exact source-ledger SHA-256 and Git blob identity before generation, runs the tests, verifies all 72 batches, and uploads the result as an artifact.

## 9. Required next actions

1. Preserve the current target and main ledgers unchanged.
2. Add the three AI trace proposals to `adjudication/AI_CALL_GRAPH_TRACE_REGISTER_V1.csv`.
3. Add this trace addendum without rewriting historical triage documents.
4. Add a dedicated target-batch-generation workflow and run it on the review branch.
5. Verify the generated artifact and then add the batch files to the review branch.
6. Update the two negative-gate tests to assert the new preflight block reason.
7. Add `tests.test_type1_formal_authorization` and include it in the priority guard test workflow.
8. Run the priority guard workflow again and preserve its full logs and artifacts.
9. Keep the three occurrence rows `UNKNOWN / OPEN / PENDING` until a human reviewer records an attributable disposition.
10. Expand only after that to the 118 workflow-control occurrences and 253 code-path occurrences.
11. Obtain independent human statistical-methods review before any protocol freeze or formal execution.

## 10. Final disposition

`TARGET_INVENTORY_RECONCILED`

`MAIN_INVENTORY_RECONCILED`

`SELF_CONTAINED_TARGET_SNAPSHOT_VERIFIED`

`THREE_PRIORITY_EXECUTION_CANDIDATES_STATICALLY_TRACED`

`ENGINEERING_EQUIVALENCE_EVIDENCE_PRESENT`

`CANDIDATE_A_STANDALONE_PILOT_EXECUTION_NOT_ESTABLISHED`

`CANDIDATES_B_AND_C_ENGINEERING_ONLY`

`HUMAN_ADJUDICATION_PENDING`

`BATCH_GENERATION_LOCALLY_REPRODUCED`

`BATCH_GENERATION_GITHUB_ARTIFACT_PENDING`

`FORMAL_PREFLIGHT_HARDENING_REQUIRED`

`PROTOCOL_NOT_FROZEN`

`FORMAL_CALIBRATION_NOT_AUTHORIZED`

`CONFIRMATORY_EXECUTION_NOT_AUTHORIZED`

`CLAIM_SUPPORT_FALSE`

`PROMOTION_AUTHORITY_FALSE`

This document is an AI-assisted technical trace proposal.
It is not a human adjudication, independent statistical review, protocol approval, execution authorization, or scientific claim.
