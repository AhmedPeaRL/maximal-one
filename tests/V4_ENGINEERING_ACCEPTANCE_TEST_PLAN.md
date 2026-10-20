# Engineering Test Acceptance Record — V4 Candidate

Status: NOT RUN

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
