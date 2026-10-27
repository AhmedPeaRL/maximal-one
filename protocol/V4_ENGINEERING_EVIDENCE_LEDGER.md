# V4 Engineering Evidence Ledger

## 1. Scope

This ledger records observed engineering evidence for the HCM Type-I Calibration V4 draft.

It does not authorize formal calibration, confirmatory execution, scientific claim support, or promotion.

## 2. Exact observed run

* Repository: `AhmedPeaRL/maximal-one`
* Branch: `review/type1-v4-remediation`
* Commit: `2769b39d0a09165d92189c7bab412fb55a8d2200`
* Workflow run: `39520279867`
* Job: `118962176942`
* Workflow: `Type-I Calibration Runtime Pilot (Exploratory Only)`
* Observed job conclusion: `success`
* Checkout identity verification: passed
* Python compilation check: passed
* Unit tests: 8 passed
* Exploratory pilot: 2 requested replicate indices, `0` and `1`
* Requested surrogates per replicate: `200`
* Observed pilot status: `PILOT_COMPLETE_DIAGNOSTIC_ONLY`
* Uploaded artifact: `type1-calibration-runtime-pilot`
* Artifact ID: `12310642741`
* Artifact upload included both the JSON output and its `.manifest.json` sidecar.

## 3. Evidence classification

### Established for this run

* The workflow checked that the checked-out Git commit matched `GITHUB_SHA`.
* The compilation command completed successfully.
* The eight tests in `tests.test_type1_calibration_pilot` passed.
* The two-replicate exploratory pilot completed.
* The artifact upload step included the JSON artifact and its sidecar manifest.
* The V4 matrix remained an exploratory draft in the inspected commit.

### Not established

* Full production-equivalence across connected, sharded, merged, and resumed execution.
* Completion of every item in `tests/V4_ENGINEERING_ACCEPTANCE_TEST_PLAN.md`.
* Independent verification of every required manifest rejection case.
* Formal Type-I error calibration.
* Approval of the V4 acceptance rule or the historical 0.075 ceiling.
* Independent statistical review sufficient to authorize confirmatory execution.
* Scientific claim support or promotion authority.

## 4. Required next engineering gates

1. Add a dedicated production-equivalence test that invokes the real endpoint and stochastic-null implementation without mocking either function.
2. Compare per-replicate scientific fields across connected and sharded execution, reverse-order merge, and resume.
3. Exercise manifest verification against valid artifacts, missing manifests, altered artifact bytes, unsupported schema, wrong artifact filename, and mismatched run identity.
4. Verify that duplicate or overlapping indices, missing indices, invalid attempts, and incomplete ranges cannot produce a successful completion status.
5. Verify that requested repetition count, seed identities, scenario identity, matrix digest, runner digest, and commit identity are checked consistently.
6. Run each acceptance item and retain the exact command, result, commit SHA, and relevant artifact hashes.
7. Obtain attributable independent statistical review of the scientific design before freezing the matrix or authorizing confirmatory execution.

## 5. Status labels

Current engineering status:

`ENGINEERING_TESTS_PASS_DIAGNOSTIC_ONLY`

This label applies only to the limited checks observed in the identified workflow run. It does not mean that the complete engineering acceptance plan passed.

Formal calibration status:

`NOT ESTABLISHED`

V4 matrix status:

`DRAFT_PENDING_ATTRIBUTABLE_INDEPENDENT_STATISTICAL_REVIEW`

## 6. Non-promotion safeguards

The following fields must remain false until the applicable review and authorization gates are genuinely satisfied:

* `claim_support`
* `promotion_authority`
* `confirmatory_execution_authorized`

The V4 matrix must not be marked frozen merely because exploratory engineering tests pass.

## 7. Audit rule

Never replace missing evidence with an inference from a successful workflow status.

Never mark a test as passed unless the test was actually executed and its result was inspected.

Never describe exploratory pilot results as formal Type-I calibration results.

## 8. New evidence entry — 2026-10-26 official-runner engineering equivalence

Observed run

- Repository: "AhmedPeaRL/maximal-one"
- Branch: "review/type1-v4-remediation"
- Tested commit: "38694ecdc4bc44a48b86ab8a54221a5d67d6a89c"
- Workflow: "Type-I V4 Official Runner Engineering Equivalence"
- Workflow run: "40352081420"
- Job: "121674545367"
- Result: "success"
- Artifact ID: "12663848472"
- Artifact name: "type1-v4-official-runner-engineering-40352081420-1"
- Artifact size reported by GitHub: 20,217 bytes
- Full-path integration-test duration: 868.804 seconds

Results visible in the job log

- Artifact-integrity tests: 8 passed.
- Execution-shard merge rejection tests: 6 passed.
- Official-runner engineering-equivalence integration test: 1 passed.
- Test configuration: scenario "gaussian_ar2_phi_0_45_minus_0_10_n3328"; six replicate indices; n=3328; master seed 20261021; 1000 requested surrogates per replicate.
- Tested paths: connected execution, two disjoint shards, normal and reverse-order merges, interrupted checkpoint, and resume.
- The bounded "--engineering-test" mode kept "formal_calibration_pass" false.

Evidence classification

Established for this exact run: checkout identity verification, locked dependency installation, successful completion of the listed tests, and matching canonical records across the tested execution paths.

Not established: formal Type-I calibration; approval or freeze of the V4 matrix; independent statistical review; confirmatory execution authorization; independent empirical replication; broader HCM claim support; independent inspection of every file in the artifact ZIP. No ZIP digest is asserted here.

Status: "ENGINEERING_EQUIVALENCE_PASS_FOR_RECORDED_CONFIGURATION_ONLY"

Formal calibration remains "NOT AUTHORIZED". V4 remains "NOT_FROZEN"; "confirmatory_execution_authorized", "claim_support", and "promotion_authority" remain false.

### Evidence entry — 2026-10-26 — Resume-test fixture mismatch

Classification: ENGINEERING_TEST_FAILURE — FIX REQUIRED
Branch: "review/type1-v4-remediation"

Observed runs

- Run "40371121290", job "121741811161": failed in the full-path equivalence test.
- Run "40371737134", job "121743963162": failed in the full-path equivalence test.
- The separate resume identity and artifact rejection tests passed in run "40371737134".
- The artifact for run "40371737134" is available at artifact ID "12673738219".

Direct failure

The duplicated "test_resume_rejects_changed_runtime_identity" method inside "tests/test_type1_full_path_equivalence.py" attempts to create an engineering checkpoint with "--surrogates 1". The official engineering runner requires exactly 1000 surrogates per replicate and exits before creating the checkpoint.

Required remediation

Remove the invalid duplicated low-surrogate test from the full-path equivalence test module. Retain the standalone synthetic artifact identity rejection tests. Add or verify a separate official-runner identity-mismatch test using a valid engineering configuration.

Interpretation

The full workflow result remains FAILED. The successful standalone identity tests do not override the full-path failure. This is an engineering test-fixture defect, not evidence for or against the scientific HCM claim.

Governance

No Type-I calibration pass is established.
No acceptance rule is approved by this entry.

Keep the V4 candidate NOT_FROZEN, confirmatory execution unauthorized, claim support false, and promotion authority false until the required independent review and governance gates are completed.

## 9. New evidence entry — 2026-10-26 — Resume identity tests and official-runner engineering verification

A. Official-runner engineering workflow

- Repository: "AhmedPeaRL/maximal-one"
- Branch: "review/type1-v4-remediation"
- Tested commit: "a4b8698517c742a8bc5d579418d05c833462c87e"
- Workflow run: "40378112715"
- Job: "121766644902"
- Job conclusion: "success"
- Artifact ID: "12678142523"
- Artifact name: "type1-v4-official-runner-engineering-40378112715-1"
- Artifact size reported by GitHub: "20,219" bytes
- GitHub-reported artifact digest: "sha256:f158607d53aaff84039410f91ac72c16f26aada03b869c283437d285936b89e8"

The job completed the following steps successfully:

- Checkout identity verification.
- Locked dependency installation.
- Artifact integrity tests.
- Merger integrity and rejection tests.
- Resume identity and artifact rejection tests.
- Official-runner connected/sharded/merged/resumed engineering-equivalence test.
- Evidence-artifact upload step.

The separate resume-identity test module uses synthetic identity fixtures. It checks acceptance of an exact matching identity, rejection of multiple identity mismatches, and rejection of artifact bytes that no longer match the recorded SHA-256.

B. Full-path workflow

- Workflow run: "40378112711"
- Job: "121766644597"
- Job conclusion: "success"
- Artifact ID: "12678977860"
- Artifact name: "type1-full-path-equivalence-evidence"
- Artifact size reported by GitHub: "273" bytes
- GitHub-reported artifact digest: "sha256:12e0f6cb702e23be8cefd1e02e5b33b931ae445563a464cce4589b38d37620d2"

The job summary reports successful completion of the official-runner full-path test and its preceding engineering checks.

C. Exact scope and limitations

Classification:

"ENGINEERING_TESTS_PASS_FOR_RECORDED_RUNS_ONLY"

The results support successful completion of the specific engineering tests executed at the recorded commit. They do not establish that every production CLI resume mismatch is rejected, that a rejected CLI resume leaves an existing checkpoint byte-for-byte unchanged, or that worker-assignment invariance has been demonstrated.

The standalone resume identity tests exercise the artifact identity-verification helper using synthetic fixtures. They must not be described as complete end-to-end proof of every production resume safeguard.

The evidence does not establish:

- Formal Type-I error calibration.
- Approval of the 0.075 acceptance ceiling or any alternative acceptance rule.
- Validation of all nine V4 scenarios.
- Protocol freeze or authorization of confirmatory execution.
- Independent empirical replication or broader HCM claim support.
- Independent inspection of the downloaded artifact ZIP payloads.

The previous failed runs remain part of the historical record. The later successful runs address the tested engineering fixture and paths only; they do not retroactively change the earlier results.

D. Governance state

Keep the following unchanged until separately reviewed and authorized:

- "freeze_state = NOT_FROZEN"
- "confirmatory_execution_authorized = false"
- "claim_support = false"
- "promotion_authority = false"
- Formal calibration: "NOT AUTHORIZED"

The remaining CLI-resume, runtime-configuration, worker-assignment, scientific acceptance-rule, and independent-review gates remain open unless supported by their own attributable evidence.

## 10. Evidence — CLI resume identity rejection and partition verification — 2026-10-27

### A. Official CLI identity rejection

Workflow:
https://github.com/AhmedPeaRL/maximal-one/actions/runs/40401666237

Job:
https://github.com/AhmedPeaRL/maximal-one/actions/runs/40401666237/job/121848811028

Tested commit:
8164fc0d6b5364703574367f8ff52e6ec01f8ec1

Observed workflow result: SUCCESS.

The inspected job log reports:
- 8 artifact-integrity tests passed.
- 6 execution-merge rejection tests passed.
- 3 standalone resume-identity tests passed.
- The official CLI identity-rejection test passed.
- The official-runner full-path equivalence test passed.

The CLI test declares 19 identity fields and creates a checkpoint
through the bounded engineering CLI. It changes each field
individually, attempts resume, requires a non-zero return code,
requires non-empty output, and compares checkpoint and manifest
bytes before and after each rejected attempt.

Classification:
CLI_IDENTITY_REJECTION_PASS_FOR_RECORDED_TEST_ONLY

Required qualification:
The test currently does not assert the exact expected identity
error message or a specific exit code. Its byte comparison
protects the candidate artifact during each rejected attempt;
it does not yet retain a separate untouched baseline file and
prove that baseline remains byte-identical throughout all cases.

These are follow-up test-strengthening items, not grounds to
erase or relabel the observed successful run.

### B. Alternative partition and resume equivalence

Workflow:
https://github.com/AhmedPeaRL/maximal-one/actions/runs/40401149060

Job:
https://github.com/AhmedPeaRL/maximal-one/actions/runs/40401149060/job/121847012649

Observed workflow result: SUCCESS.

The tested procedure included connected execution, alternative
shard partitions, merge ordering, and interrupted/resumed
execution. It is evidence of equivalence only for the exact
bounded configuration and paths exercised by the test.

The tests were run within the same workflow job. They do not
establish invariance across distinct GitHub-hosted runners or
different worker environments.

### C. Scientific and governance limits

Neither run establishes:
- Type-I calibration at nominal alpha 0.05.
- Approval of the 0.075 threshold or another acceptance rule.
- Validation of all nine V4 scenarios.
- Independent statistical approval.
- Protocol freeze or formal execution authorization.
- Independent empirical replication or broader HCM claim support.

Preserve historical failures and their original classifications.

Required state remains:

freeze_state = NOT_FROZEN
confirmatory_execution_authorized = false
claim_support = false
promotion_authority = false
formal_calibration = NOT_AUTHORIZED

## 11. Engineering remediation record — 2026-10-27

Classification: OPEN — REMEDIATION REQUIRED

The following failures were observed in the recorded engineering runs:

1. Run 40417570720:
   the worker-order test passed a single-replicate shard to a helper
   that requires all six replicate records. This is a test-scope mismatch.
   The full-path test did not pass.

2. Run 40417595888:
   the CLI resume identity test failed for start_index because the
   mutated range was invalid before the expected identity comparison.
   The full CLI identity test did not pass.

3. Run 40419156405:
   the V3/V4 governance separation test failed two assertions.
   The legacy workflow validates V3 metadata but calls a scenario runner
   whose current implementation reads the V4 candidate matrix.
   This is a governance-path mismatch requiring a fail-closed guard
   and a separately verified V3 runner before any V3 calibration attempt.

These failures remain historical facts and must not be deleted,
overwritten, or retrospectively relabeled as passing.

Required re-test evidence:
- CLI identity mismatch rejection with valid ranges.
- Exit code and expected diagnostic asserted for every identity field.
- Original checkpoint and manifest retained as immutable baseline copies.
- Worker-order records validated individually and compared after merge.
- Missing, duplicate, or invalid attempts remain visible and cannot
  be silently replaced or counted as successful completion.
- V3 workflow blocked before invoking a V4 candidate runner.
- Evidence artifacts uploaded even when a test fails.

The remediation is not complete until a new workflow run on the
review branch demonstrates the corrected tests and retains its logs
and artifacts.

Governance state remains unchanged:
- freeze_state = NOT_FROZEN
- confirmatory_execution_authorized = false
- claim_support = false
- promotion_authority = false
- formal calibration = NOT AUTHORIZED

No acceptance threshold is approved by this record.
No historical result is reinterpreted by this record.

## 12. Required parallel worker-order and independent-runner evidence — 2026-10-27

Classification: PENDING EXECUTION AND EVIDENCE REVIEW

### A. Same-runner concurrent worker-order test

Planned test:
`tests/test_type1_parallel_worker_order_equivalence.py`

Purpose:
Compare a connected six-replicate reference with six separately
invoked CLI replicate tasks submitted concurrently in a permuted
worker assignment order.

Evidence required:
- Exact tested commit SHA and workflow run/job URLs.
- Full test log and uploaded evidence artifact.
- Requested indices exactly 0 through 5, with one attempt per index.
- Per-replicate seed identities and generated-series hashes.
- Endpoint estimates, requested/valid surrogate counts, exceedances,
  p-values, statuses, and failure reasons.
- Explicit confirmation that formal_calibration_pass remained false.

### B. Independent-runner comparison

Planned workflow:
`.github/workflows/type1-v4-cross-runner-worker-order.yml`

Purpose:
Execute each replicate in a separate GitHub Actions job and compare
the resulting records with the connected reference.

Evidence required:
- Reference and worker job conclusions.
- Exact checkout commit SHA for every job.
- Verified artifact and manifest hashes.
- Common run-identity comparison, including commit, matrix, runner,
  seed schedule, endpoint, null implementation, and dependency lock.
- Recorded platform_identity for the reference and each worker.
- A complete comparison report covering all requested indices.
- Evidence that missing, duplicate, invalid, or mismatching attempts
  cannot be treated as a successful complete result.

### C. Interpretation rule

Until the runs have completed and the actual logs and artifacts have
been inspected, these are planned tests, not successful evidence.

If the tests pass, the conclusion is limited to engineering
equivalence for the exact recorded configuration and execution
environments. It is not evidence of Type-I calibration, acceptance
threshold validity, protocol freeze, independent statistical approval,
or HCM claim support.

A failed run must remain in the historical record. A later successful
run may establish a corrected engineering test for its own recorded
configuration, but it does not erase or retroactively relabel earlier
failures.

Governance state remains unchanged:
- freeze_state = NOT_FROZEN
- confirmatory_execution_authorized = false
- claim_support = false
- promotion_authority = false
- formal calibration = NOT AUTHORIZED

No acceptance threshold is approved by this entry.
