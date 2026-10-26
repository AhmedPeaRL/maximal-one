Type-I V4 Engineering Execution Contract

Status: DRAFT — ENGINEERING REQUIREMENTS ONLY
Branch: "review/type1-v4-remediation"
Protocol freeze: NOT FROZEN
Confirmatory execution: NOT AUTHORIZED

1. Purpose

This contract defines the engineering requirements for executing the V4 candidate scenario matrix reproducibly. It does not approve the scientific protocol, select an acceptance threshold, or authorize confirmatory calibration.

The official scientific calculation path must remain unchanged unless a separately reviewed, versioned amendment explicitly authorizes a change.

2. Run identity

Every shard and checkpoint must bind to a canonical run identity containing, at minimum:

- Protocol and scenario identifiers.
- Scenario coefficients and declared sample size.
- DGP burn-in.
- Requested surrogate count.
- Requested total outer repetitions.
- Master seed and seed-schedule identifier.
- Exact shard start and stop indices.
- Git commit SHA.
- Scenario-matrix SHA-256.
- Official runner SHA-256.
- Scientific endpoint and null-implementation identities.
- Relevant dependency-lock and runtime identity.

The identity must be serialized deterministically. Missing, malformed, or conflicting identity fields must fail closed.

3. Deterministic execution

Replicate indices are zero-based and assigned before execution.

Seed identity must depend on the frozen master seed, stable scenario identifier, replicate index, and declared stream identifier. It must not depend on shard order, worker assignment, execution order, or scenario list position.

The official scientific calculation path must be identical across connected, sharded, resumed, and merged execution.

4. Checkpoint and manifest integrity

Every checkpoint or shard artifact must have a sidecar manifest that records its schema version, artifact filename, artifact SHA-256, and exact run identity.

Writes must be atomic. A checkpoint must not be accepted when its artifact hash, manifest identity, run identity, or requested range differs from the current execution.

Resume must reject duplicate replicate indices and records outside the declared range. Previously completed valid records must not be silently regenerated or replaced.

5. Merge contract

The merger must independently verify every shard artifact and manifest.

It must reject:

- Missing or invalid manifests.
- Artifact SHA-256 mismatches.
- Manifest/artifact identity mismatches.
- Incompatible common run identities.
- Duplicate replicate indices.
- Overlapping shard ranges.
- Records outside their declared shard range.
- Missing required indices when completion is claimed.
- Invalid attempts represented as successful completion.

A merge result must distinguish complete, incomplete, and failed execution. A complete engineering artifact is not a formal calibration pass.

6. Production-path equivalence

A separate production-path equivalence test must exercise the official runner and scientific calculation path using 1,000 requested surrogates per outer replicate.

The engineering fixture may use a small number of outer replicates. It must compare per-replicate scientific fields across:

1. Connected execution.
2. Disjoint shard execution.
3. Normal-order merge.
4. Reverse-order merge.
5. Verified checkpoint resume.

Comparison fields must include replicate index, seed identity, generated-series digest, observed endpoint, requested and valid surrogate counts, Monte Carlo p-value, selected null order, attempt status, and failure reason.

Only explicitly declared volatile metadata may be excluded from equality comparisons.

7. Evidence retention

Retain the exact commit SHA, dependency-lock hash, matrix hash, runner hash, workflow hash, shard manifests, artifact hashes, per-replicate comparison report, test logs, and final engineering status.

The CI workflow must upload evidence even when a test fails.

8. Scientific authority boundary

Passing engineering tests does not establish Type-I error calibration, validate the scientific null, establish independent empirical replication, or support the HCM claim.

Until the scientific protocol is prospectively reviewed and frozen, and a separate authorization is recorded, the following values remain unchanged:

- "freeze_state = NOT_FROZEN"
- "confirmatory_execution_authorized = false"
- "claim_support = false"
- "promotion_authority = false"
- "formal_calibration_pass = false"

9. Acceptance rule

The engineering contract is accepted only when the required tests have been run against the exact recorded commit and their evidence has been retained.

No checkbox may be marked complete merely because the corresponding requirement has been documented.
No scientific acceptance threshold may be inferred from an engineering test result.
