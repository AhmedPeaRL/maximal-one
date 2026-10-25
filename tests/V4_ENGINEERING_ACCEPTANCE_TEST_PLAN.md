# Engineering Test Acceptance Record — V4 Candidate

Status: PARTIALLY RUN — NOT COMPLETE

## Test fixture

Use a tiny synthetic fixture with replicate indices 0 through 5.

- Connected run: indices [0, 6)
- Shard A: indices [0, 2)
- Shard B: indices [2, 4)
- Shard C: indices [4, 6)
- Merge the shards in reverse order.
- Repeat after interrupting and resuming a valid checkpoint.

## Required tests

- [ ] Every requested index has exactly one attempt record.
- [ ] Connected and sharded execution produce identical scientific outputs per index.
- [ ] Resumed and uninterrupted execution produce identical scientific outputs per index.
- [ ] Seed identities are independent of shard order and worker assignment.
- [ ] Resume rejects mismatched commit, matrix hash, runner hash, scenario, seed schedule, or range.
- [ ] Merge rejects duplicate indices and overlapping ranges.
- [ ] Merge identifies missing indices and cannot report completion.
- [ ] Merge independently verifies each shard artifact SHA-256 against its manifest.
- [ ] Invalid attempts remain in the ledger and force scenario failure.
- [ ] The rejection-rate denominator is the requested repetition count N.
- [ ] A pilot always declares formal_calibration_pass=false.
- [ ] A pilot never changes claim_support or promotion_authority.
- [ ] Production-equivalence tests pass against the declared endpoint and null implementation.

## Scientific fields to compare per replicate

- replicate index and seed identities
- generated-series digest
- observed endpoint estimate
- requested and valid surrogate counts
- Monte Carlo p-value
- selected AR order
- attempt status and failure reason

Only explicitly declared volatile metadata, such as elapsed duration and timestamps, may be excluded from equality comparisons.

## Evidence to retain

- exact branch and commit SHA
- dependency-lock SHA-256
- protocol matrix SHA-256
- runner and workflow SHA-256
- per-shard manifest and artifact hashes
- test output and per-index comparison report
- merge rejection tests
- independent reviewer response

## Allowed result labels

- ENGINEERING_TESTS_PASS_DIAGNOSTIC_ONLY
- ENGINEERING_TESTS_FAIL
- NOT_RUN

Passing this engineering plan is not a Type-I calibration pass.

## Evidence reconciliation — 2026-10-25

### Pilot full-path evidence

Status: PASS FOR THE EXACT RECORDED PILOT CONFIGURATION ONLY

- Commit: f84a4990caee2bd6341151f92abdf37c8e1b63c2
- Workflow run: 40144016182
- Job: 121021438641
- Test: tests.test_type1_full_path_equivalence
- Outer indices: 0 through 5
- Surrogates per attempt: 200
- Observed test duration: 152.783 seconds
- Workflow result: success
- Artifact ID: 12579803125
- Artifact ZIP SHA-256:
  4b3e9a308e36ba57041117955b4e82a37a88966d84f233a69c09faca2567902c

The workflow log reports that the six-index connected/sharded/reverse-merge/
checkpoint-resume pilot test passed.

This evidence does not establish production-runner equivalence, formal
Type-I calibration, acceptance-rule approval, protocol freeze, confirmatory
execution authorization, or support for the scientific claim.

### Remaining engineering blockers

- [ ] Pilot rejection tests for duplicate indices, overlapping ranges,
      missing indices, common-identity mismatch, and invalid attempts.
- [ ] Manifest/run-identity mismatch rejection test.
- [ ] Production runner supports and validates deterministic shard ranges.
- [ ] Production runner preserves a manifest bound to the exact run identity.
- [ ] Production checkpoint resume verifies commit, matrix, runner,
      scenario, seed schedule, configuration, and requested range.
- [ ] Production merger verifies shard hashes and rejects duplicate,
      overlapping, missing, and mismatched inputs.
- [ ] Production-equivalence test is separate from the pilot test.
- [ ] Production-equivalence test exercises B=1000 with a small engineering
      fixture and compares scientific output per replicate.
- [ ] Runtime measurement at B=1000 is retained and reviewed.
- [ ] V3 workflow and acceptance references are explicitly superseded or
      safely disabled; no V3 rule is treated as the V4 decision.
- [ ] The acceptance ledger records run 40144016182 and its exact scope.
- [ ] Attributable independent human statistical review is completed.

### Status policy

The pilot test may be marked PASS for its recorded configuration.
The complete V4 engineering plan remains NOT COMPLETE until the applicable
remaining tests have run and their artifacts have been inspected.

The protocol remains NOT_FROZEN.
Confirmatory execution remains NOT_AUTHORIZED.
Claim support remains NOT_ESTABLISHED.
Promotion authority remains false.


## Evidence reconciliation — 2026-10-25 — latest run

### Pilot merge rejection tests

Status: PASS FOR THE TESTED CASES ONLY

- Commit: 5563000b7911502ec9d69251e85ac1bad1b86af6
- Workflow run: 40148534671
- Job: 121034983759
- Test module: tests.test_type1_pilot_merge_rejections
- Result: 6 tests passed

Verified rejection/incompleteness cases:
- Duplicate replicate index inside one shard.
- Duplicate replicate index across shards.
- Overlapping declared shard ranges.
- Missing indices cannot report completion.
- Common run-identity mismatch across shards.
- Invalid attempt prevents a pilot completion pass.

### Pilot full-path integration test

Status: PASS FOR THE RECORDED ENGINEERING CONFIGURATION ONLY

- Commit: 5563000b7911502ec9d69251e85ac1bad1b86af6
- Workflow run: 40148534671
- Job: 121034983759
- Test: tests.test_type1_full_path_equivalence
- Result: 1 test passed
- Recorded test duration: 302.261 seconds
- Artifact ID: 12582046447
- Artifact ZIP SHA-256:
  dd323d70fb70d4822a8920f90a670f42fa0601589ee045020d7f5e0d05e3c9e1

This run provides engineering evidence for the exact tested paths and
configuration. It does not establish formal Type-I calibration,
production equivalence at B=1000, protocol freeze, confirmatory
execution authorization, or support for the scientific claim.

### Remaining engineering blockers

- [ ] Manifest/run-identity mismatch rejection test.
- [ ] Artifact SHA-256 mismatch rejection test.
- [ ] Production runner supports and validates deterministic shard ranges.
- [ ] Production runner preserves a manifest bound to the exact run identity.
- [ ] Production checkpoint resume verifies commit, matrix, runner,
      scenario, seed schedule, configuration, and requested range.
- [ ] Production-equivalence test is separate from the pilot test.
- [ ] Production-equivalence test exercises B=1000 with a small
      engineering fixture and compares scientific output per replicate.
- [ ] Runtime measurement at B=1000 is retained and reviewed.
- [ ] V3 workflow and acceptance references are explicitly superseded
      or safely disabled; no V3 rule is treated as the V4 decision.
- [ ] The acceptance ledger records the latest run and exact scope.
- [ ] Attributable independent human statistical review is completed.

### Authority boundary

The engineering plan remains NOT COMPLETE.
The protocol remains NOT_FROZEN.
Confirmatory execution remains NOT_AUTHORIZED.
Claim support remains NOT_ESTABLISHED.
Promotion authority remains false.
