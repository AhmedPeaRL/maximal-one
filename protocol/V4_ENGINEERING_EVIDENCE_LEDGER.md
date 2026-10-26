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
