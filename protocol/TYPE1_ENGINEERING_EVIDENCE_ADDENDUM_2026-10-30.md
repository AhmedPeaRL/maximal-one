# Type-I V4 Engineering Evidence Addendum
## Evidence recorded on 2026-10-30

**Repository:** AhmedPeaRL/maximal-one
**Working branch:** review/type1-v4-remediation
**Record date:** 2026-10-30
**Purpose:** Record additional bounded engineering evidence for independent review.

## 1. Authority and status

This addendum records engineering evidence only.

- Protocol: HCM_TYPE1_CALIBRATION_V4_CANDIDATE
- Protocol freeze: NOT_FROZEN
- Independent statistical review: PENDING
- Acceptance rule: UNRESOLVED
- Confirmatory execution: NOT_AUTHORIZED
- Formal calibration: NOT_STARTED
- Claim support: false
- Promotion authority: false

This document does not approve a protocol, change a threshold,
authorize confirmatory execution, or establish scientific validity.

## 2. Evidence records

### E8 — Worker assignment matrix invariance

- Commit: 2821077407a21e764f99143bf6df9e29bf163b69
- Workflow run: 40768558101
- Job: 123099219597
- Artifact: 12851468942
- Test:
  tests.test_type1_worker_assignment_matrix_invariance
- Observed result: PASS
- Recorded test:
  Two assignment matrices were compared with the connected reference.

Scope limitation:
This supports the tested assignment-invariance behavior only.
It does not establish statistical calibration or general equivalence
for every possible partition or execution environment.

### E9 — CLI resume identity rejection

- Commit: 57f60723f012d3c8dbe94e3fa57963cd92ce890c
- Workflow run: 40783850430
- Job: 123151990547
- Artifact: 12858910681
- Test:
  tests.test_type1_resume_cli_identity_rejections
- Observed result: PASS
- Recorded test:
  Supported identity mismatches are rejected without mutating
  the existing resume state.

Scope limitation:
This supports the tested rejection cases only. It does not establish
that every possible resume or recovery path has been reviewed.

### E10 — V3/V4 governance inventory

- Commit: d49c428ad9633739db1c17c28ea1e9793a69c40f
- Workflow run: 40802782354
- Job: 123214546453
- Artifact: 12866603073
- Observed result: PASS
- Automated inventory and V3/V4 separation regression tests completed.

Scope limitation:
The corresponding manual classification ledger remains incomplete.
Automated inventory success is not equivalent to human disposition
of every execution-capable occurrence.

### E11 — Cross-runner worker-order comparison

- Commit: f8e4c4a9fa73cb8022cfa738cb02cb6b31ac5a99
- Workflow run: 40830639931
- Comparison job: 123306217103
- Reference job: 123303808024
- Worker jobs:
  123303808372
  123303808466
  123303808381
  123303808483
  123303808299
  123303808382
- Comparison artifact: 12879330111
- Reference artifact: 12878951942
- Worker artifacts:
  12878532460
  12879020783
  12878990877
  12878935436
  12878831235
  12878267328
- Observed workflow/job outcomes: SUCCESS

The comparison job downloaded the connected reference and six worker
artifacts, verified their artifact digests, and generated a comparison
report.

Scope limitation:
This is bounded engineering evidence for the recorded workers,
inputs, and comparison procedure. It does not establish independent
scientific replication or independence of the underlying method.

### E12 — Official runner, 1000-surrogate engineering equivalence

- Commit: 5369f9a0c565b2f917b8613ea69842cb68e25bd8
- Workflow run: 40830437451
- Job: 123303151899
- Artifact: 12880224200
- Artifact ZIP SHA-256:
  ac62cc3ad8fe577ca55ebd2eca21dda9262158995539df34b133383fba799d84
- Test:
  tests.test_type1_full_path_equivalence
- Observed result: PASS

The inspected job log records successful completion of:
- Artifact integrity tests.
- Artifact-loss and denominator-protection tests.
- Merge rejection tests.
- Resume identity rejection tests.
- CLI resume identity rejection.
- V3/V4 governance separation tests.
- Connected/sharded/merged/resumed official-runner equivalence.
- Parallel worker-order equivalence.

The full-path test source specifies:
- One declared AR(2) scenario.
- Six outer replicate indices.
- 1000 requested surrogates per replicate.
- Connected execution.
- Two-shard and alternative three-shard execution.
- Normal and reverse merge.
- Checkpoint/resume comparison.

Scope limitation:
This is an engineering equivalence test, not formal Type-I calibration.
It does not execute the nine-scenario, 2000-repetition-per-scenario
candidate calibration design. It does not approve the endpoint,
null family, acceptance rule, or scientific claim.

## 3. Consolidated engineering interpretation

The recorded evidence strengthens support for the following bounded
engineering properties:

- Artifact and manifest integrity checks.
- Rejection of selected missing, duplicate, overlapping,
  corrupted, or mismatched execution records.
- Preservation of requested replicate identity and denominator.
- Resume rejection for tested identity mismatches.
- Assignment-matrix invariance for the tested matrices.
- Connected versus sharded execution equivalence for the tested
  configuration.
- Merge-order invariance for the tested configuration.
- Worker-order comparison for the recorded worker set.

The evidence does not establish universal implementation equivalence.
The exact tests, inputs, commits, logs, and artifacts must be inspected
before a reviewer accepts any item.

## 4. Outstanding acceptance requirements

The following remain open:

1. Complete the manual V3/V4 occurrence-classification ledger.
2. Review every workflow and indirect runner path for fail-closed
   authorization behavior.
3. Independently review the mathematical endpoint specification.
4. Independently review the stochastic-null procedure and its
   production implementation.
5. Resolve the acceptance-rule conflict prospectively.
6. Justify the scenario matrix, including resonance scenarios.
7. Resolve invalid-attempt, failed-fit, and surrogate-shortfall policy.
8. Pin the exact reviewed commit and SHA-256 digests of every
   protocol, source, dependency-lock, and workflow input.
9. Obtain an attributable independent human statistical review.
10. Record the reviewer disposition and all required amendments.
11. Only after review closure, consider a separate freeze decision.
12. Only after a valid freeze, consider a separate execution
    authorization.

## 5. Non-retroactivity and safeguards

- Preserve all historical results and their original classifications.
- Do not change the historical Wilson rule.
- Do not treat the 0.075 ceiling as approved.
- Do not select a new acceptance rule after inspecting results.
- Do not silently remove or replace invalid attempts.
- Do not treat AI-generated review as independent human approval.
- Do not treat engineering success as scientific calibration.
- Do not modify main as part of this remediation.

## 6. Current decision

CONTINUE_TO_INDEPENDENT_REVIEW_PREPARATION

Engineering evidence has materially advanced for the recorded
configurations.

The manual governance inventory, independent statistical review,
protocol freeze, and formal execution authorization remain open.

Formal Type-I calibration remains NOT_AUTHORIZED.
The HCM scientific claim remains NOT_ESTABLISHED.
