# V4 Engineering Gap Closure Record — 2026-10-27

## 1. Scope

Repository: `AhmedPeaRL/maximal-one`

Working branch: `review/type1-v4-remediation`

Purpose: record the remaining engineering and governance gaps after the successful bounded engineering workflows. This record does not authorize formal calibration, freeze the V4 matrix, or support scientific claim promotion.

## 2. Evidence already observed

### A. Official CLI resume identity rejection

Workflow: https://github.com/AhmedPeaRL/maximal-one/actions/runs/40443323549

Job: https://github.com/AhmedPeaRL/maximal-one/actions/runs/40443323549/job/121988559332

Tested commit: `bdb8a76db71fbcd3202f974e33b6b9cd14bb6ff9`

Observed job conclusion: `success`.

The job steps report successful execution of:

* Artifact-integrity tests.
* Merge rejection tests.
* Resume identity and artifact rejection tests.
* Actual CLI resume identity rejection test.
* V3/V4 governance separation test.
* Official-runner connected/sharded/merged/resumed equivalence test.

Classification: `ENGINEERING_PASS_FOR_RECORDED_TESTS_ONLY`.

### B. Full-path engineering verification

Workflow: https://github.com/AhmedPeaRL/maximal-one/actions/runs/40443938628

Job: https://github.com/AhmedPeaRL/maximal-one/actions/runs/40443938628/job/121990580255

Tested commit: `e611fbdee3400be60d405633dc5141cb3008355a`

Observed job conclusion: `success`.

The job reports successful checkout identity verification, locked dependency installation, merge and manifest rejection tests, full-path integration testing, and evidence upload.

Classification: `ENGINEERING_PASS_FOR_RECORDED_TESTS_ONLY`.

## 3. Remaining engineering gates

### G1 — Checkpoint identity and byte preservation

* [ ] Inspect the uploaded CLI test summary and all 19 individual rejection logs.
* [ ] Confirm every tested mismatch returns the expected non-zero exit code.
* [ ] Confirm each log records the intended identity field and the expected rejection diagnostic.
* [ ] Verify checkpoint and manifest SHA-256 values are identical before and after each rejected resume attempt.
* [ ] Verify the original valid checkpoint fixture remains unchanged and is not overwritten by a mutated test fixture.
* [ ] Confirm missing, corrupt, stale, and identity-mismatched manifests fail closed.
* [ ] Confirm all failures remain available as evidence artifacts.

### G2 — Shard and worker-assignment invariance

* [ ] Compare connected execution against at least two distinct valid shard partitions.
* [ ] Compare normal-order and reverse-order merges.
* [ ] Test alternative replicate-to-worker assignment orders.
* [ ] Where feasible, test concurrent independent CLI workers with separate output paths and independently verified manifests.
* [ ] Compare each replicate by stable index, DGP seed identity, null seed identity, generated-series SHA-256, endpoint estimate, requested surrogate count, valid surrogate count, Monte Carlo p-value, attempt status, and failure reason.
* [ ] Confirm the comparison is field-by-field and does not rely solely on a summary status.
* [ ] Confirm the merged result has exactly one record for every requested replicate index.
* [ ] Confirm a missing or invalid attempt cannot be silently replaced or counted as a successful scientific result.

Any worker test executed on one hosted runner must be described as such. Do not call it cross-machine replication.

### G3 — Runtime and execution identity

* [ ] Record the exact commit, matrix hash, runner hash, dependency-lock hash, Python version, platform, seed schedule, scenario, sample size, burn-in, surrogate count, and requested index range.
* [ ] Verify these fields are enforced on resume and merge.
* [ ] Record observed runtime and resource use for each tested configuration.
* [ ] Do not extrapolate the six-replicate engineering test into a claim that the full nine-scenario workload is computationally feasible.

### G4 — V3/V4 governance inventory

* [ ] Enumerate every workflow that references the V3 matrix or V3 runner.
* [ ] Enumerate every occurrence of `0.075` in source, tests, workflows, specifications, reports, and decision records.
* [ ] Classify each occurrence as `HISTORICAL`, `DIAGNOSTIC`, or `FORMAL_EXECUTION_CAPABLE`.
* [ ] Record the exact guard that prevents each legacy workflow from authorizing V4 execution.
* [ ] Verify that the V3 workflow cannot silently execute V4 files or authorize V4 confirmatory work.
* [ ] Preserve all historical records and failed runs.
* [ ] Do not delete or disable a legacy workflow until its purpose, dependencies, and replacement or blocking mechanism are documented.

## 4. Acceptance-rule decision gate

The historical rule and the V4 candidate rule are different.

Historical rule:

* The two-sided 95% Wilson interval must contain nominal 0.05.
* Its upper endpoint must not exceed 0.075.

V4 candidate rule:

* The one-sided 95% Wilson upper bound must not exceed 0.075.

Neither rule is approved for future confirmatory execution by this record.

Required before freezing V4:

* An attributable independent human statistical reviewer must assess the estimand, decision consequences, confidence-bound convention, Monte Carlo precision, invalid-attempt policy, and scenario coverage.
* The reviewer must document the selected prospective rule and its rationale.
* The selected rule must be recorded in a new decision commit before any confirmatory data collection.
* Historical outcomes must remain labelled under the rule that actually governed them.
* No historical failure may be relabelled as a pass because a future rule differs.

## 5. Governance invariants

Until all applicable gates are completed and approved:

* `freeze_state = NOT_FROZEN`
* `confirmatory_execution_authorized = false`
* `claim_support = false`
* `promotion_authority = false`
* `formal_calibration_pass = false` for engineering-only outputs
* V4 formal execution remains `NOT_AUTHORIZED`

A successful engineering workflow is not Type-I calibration evidence.

## 6. Closure rule

Close a gate only when its exact test, commit SHA, workflow run, job result, and relevant artifact evidence are recorded and inspected.

A missing artifact, uninspected failure log, or untested configuration remains `OPEN` or `UNKNOWN`; it must never be inferred to be a pass.

No item in this record authorizes formal calibration, protocol freeze, or scientific claim promotion.
