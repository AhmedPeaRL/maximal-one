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

- [x] Every requested index has exactly one attempt record.
- [x] Connected and sharded execution produce identical scientific outputs per index.
- [x] Resumed and uninterrupted execution produce identical scientific outputs per index.
- [x] Canonical per-replicate records match across the specifically tested connected, sharded, reverse-merge, and resumed paths.
- [ ] Seed identity and scientific outputs remain invariant under alternative worker assignments and alternative valid shard partitions.
- [ ] Resume rejects mismatched commit, matrix hash, runner hash, scenario, seed schedule, or range.
- [x] Merge rejects duplicate indices and overlapping ranges.
- [x] Merge identifies missing indices and cannot report completion.
- [x] Merge independently verifies each shard artifact SHA-256 against its manifest.
- [x] Invalid attempts remain in the ledger and force scenario failure.
- [ ] The rejection-rate denominator is the requested repetition count N.
- [x] A pilot always declares formal_calibration_pass=false.
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

- [x] Manifest/run-identity mismatch rejection test.
- [x] Artifact SHA-256 mismatch rejection test.
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

## Resume identity and runtime-configuration gate — 2026-10-26

Status: NOT YET VERIFIED BY THE NEW TESTS

### Required evidence

- [ ] The exact same run identity can be loaded from a valid artifact and
      its matching manifest.
- [ ] Resume rejects a changed commit identity.
- [ ] Resume rejects a changed matrix hash.
- [ ] Resume rejects a changed runner hash.
- [ ] Resume rejects a changed scenario.
- [ ] Resume rejects a changed seed schedule or master seed.
- [ ] Resume rejects a changed sample size, burn-in, or surrogate count.
- [ ] Resume rejects changed total repetitions or requested shard range.
- [ ] Resume rejects a changed endpoint/null implementation identity.
- [ ] Resume rejects a changed dependency-lock identity.
- [ ] Resume rejects an artifact whose bytes no longer match its manifest.
- [ ] A rejected resume leaves the existing checkpoint unchanged.
- [ ] The actual CLI resume path is tested, not only the identity helper.
- [ ] Worker-assignment invariance is tested separately from shard-order
      invariance.
- [ ] A deterministic test covers alternative valid shard partitions.
- [ ] Every requested replicate has exactly one preserved attempt record.
- [ ] Invalid attempts remain visible and block scenario success.
- [ ] The rejection-rate denominator remains the predeclared requested
      repetition count N, including invalid attempts according to the
      reviewed protocol.
- [ ] Bounded engineering output cannot authorize formal calibration,
      claim support, or promotion.

### V3/V4 governance reconciliation

- [ ] Identify every active workflow that invokes the legacy V3 protocol.
- [ ] Identify every acceptance-rule constant and historical reference
      to the 0.075 boundary.
- [ ] Document whether each legacy workflow is historical, diagnostic,
      or capable of attempting formal execution.
- [ ] Ensure no legacy V3 workflow can authorize a V4 confirmatory run.
- [ ] Preserve historical V3 results and their original interpretation.
- [ ] Link the prospective acceptance-rule decision record.
- [ ] Obtain attributable independent human statistical review.
- [ ] Freeze only the reviewed and approved V4 specification.
- [ ] Authorize confirmatory execution only in a separate, explicit,
      traceable decision.

### Evidence rule

Every checked item must cite the exact commit, workflow run, job,
test result, and retained artifact where applicable. Until those
records exist, the item remains unchecked.

Passing engineering tests does not constitute Type-I calibration,
protocol approval, independent replication, or HCM claim support.

## Resume identity follow-up — evidence reconciliation — 2026-10-26

Evidence observed

- Commit: "a4b8698517c742a8bc5d579418d05c833462c87e"
- Workflow run: "40378112715"
- Job: "121766644902"
- Result: "success"
- Standalone test module: "tests/test_type1_resume_identity_rejections.py"

The standalone module tests exact identity acceptance, rejection of multiple identity mismatches, and rejection of corrupted artifact bytes.

Scope restriction

These tests call the artifact identity-verification helper using synthetic fixtures. They do not exercise the complete production CLI resume path for every mismatch.

Keep these items open

- [ ] Actual CLI resume rejects changed commit, matrix hash, runner hash, scenario, seed schedule, configuration, dependency-lock identity, endpoint/null identity, and requested range.
- [ ] Rejected CLI resume leaves the existing checkpoint byte-for-byte unchanged.
- [ ] Alternative valid shard partitions and worker assignments preserve canonical scientific outputs.
- [ ] Every requested replicate has exactly one preserved attempt record after interruption and resume.
- [ ] The requested repetition denominator N is preserved under the prospectively reviewed invalid-attempt policy.
- [ ] Bounded engineering output cannot authorize formal calibration, claim support, or promotion.

Governance status

The engineering tests do not resolve the scientific acceptance-rule conflict. V4 remains "NOT_FROZEN"; confirmatory execution remains "NOT_AUTHORIZED"; "claim_support" and "promotion_authority" remain false.
