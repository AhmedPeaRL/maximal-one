# Type-I V4 — Manual Occurrence Adjudication Protocol V3 (Corrective Revision)

## Status

`REVIEW_PROTOCOL_ONLY_NOT_ADJUDICATION_NOT_AUTHORIZATION`

This protocol governs manual documentation of occurrences. It does not classify occurrences automatically, freeze a calibration protocol, authorize confirmatory execution, support a scientific claim, or grant promotion authority.

## 1. Current evidence identity

Repository: `AhmedPeaRL/maximal-one`

Review branch: `refs/heads/review/type1-v4-remediation`

Workflow-definition commit: `785f3259bcda7529e9ce1b75186f881992259dda`

Current target inventory:

- Ref: `refs/audit/target`
- Commit: `e41fb7392b58198e8a4d8fa28b470b12b6ad2c31`
- Occurrences: `1711`
- Reconciliation: `RECONCILED`

Current main comparison inventory:

- Ref: `refs/audit/main`
- Commit: `00bbd1fbd6df41b3e988ace75c480ea6232cfb86`
- Occurrences: `633`
- Reconciliation: `RECONCILED`

Current inventory run/artifact: `42412946073` / `13590456464`.

Current reference-inventory SHA-256: `5b4fbdca1bbdf56d47f38519fecf2b7cc325e3b41df2b9fe97dcd70cd9fd0b9a`.

Current snapshot run/artifact: `42413097084` / `13589957465`.

Snapshot manifest SHA-256: `1d847035a307e810825ebfaaf6f790a1c829d88282ee1f80ac8351fb185f14e8`.

Self-contained snapshot ZIP SHA-256: `23ee07fa1533f5f0f0cad136ab187d2707e35c4fd95a54ca820cadd61b18f25a`.

The machine-readable register is `protocol/EVIDENCE_REGISTER_V3.json`.

**Snapshot boundary:** the current target-commit snapshot (`42413097084`) checks out `e41fb7392b58198e8a4d8fa28b470b12b6ad2c31`. It verifies the selected target-code scope, but it does not include the V3 governance implementation introduced on review-branch commit `785f3259bcda7529e9ce1b75186f881992259dda`. The two snapshots answer different questions and must not be conflated. A separate `type1-v3-governance-implementation-snapshot.yml` workflow must capture the exact review-branch implementation commit before external governance review.

## 2. Historical evidence must not be rebound

An earlier inventory used target commit `e41fb7392b58198e8a4d8fa28b470b12b6ad2c31`, main commit `9a3390acedbb146111be64f9a45a00b41a85be25`, target count `1711`, main count `622`, and reference-inventory SHA-256 `7171edb8da35b46a470e819626266f497983f4dee77c32ecc8aac2f82b9f86ec`.

That older inventory and any batch digest created against it remain historical. Do not change their metadata, reuse their register identity, or silently rebind their batch digest to the current inventory. A new batch must be created only after the corrective governance implementation is committed and a fresh inventory/snapshot has been generated.

Target and main populations are separate populations. Never merge their occurrence IDs or counts.

## 3. Primary reviewer and conflicts

A repository author may act as primary reviewer only with explicit disclosure of repository authorship and all relevant intellectual, financial, supervisory, collaboration, and other conflicts.

The primary reviewer must be a human and must provide a stable reviewer identity, role, conflict statement, UTC timestamp, and rationale.

AI systems may assist with navigation, transcription, code search, and evidence summaries. They cannot sign as human reviewers, replace independent human adjudication, or serve as second reviewer.

## 4. High-impact definition

A record is high-impact if any of the following holds:

- `can_influence_execution == YES`
- `can_influence_execution == UNRESOLVED`
- `manual_classification` is `EXECUTION_ENTRY_POINT`, `EXECUTION_CALLER`, `WORKFLOW_TRIGGER_OR_CONTROL`, or `AUTHORIZATION_GUARD`
- `manual_classification == UNRESOLVED`

An unresolved or unknown value must never be inferred downward to `NO` or a low-impact classification.

## 5. Mandatory second human review

Every V3 record must contain a `second_review` object.

Allowed statuses: `NOT_REQUIRED`, `PENDING`, `AGREED`, `DISAGREED`.

- Low-impact records may use `NOT_REQUIRED`, with a specific rationale.
- High-impact records cannot use `NOT_REQUIRED`.
- High-impact records may remain `OPEN` with `PENDING` or `DISAGREED`.
- A second review marked `AGREED` or `DISAGREED` must identify a distinct human, role, conflict statement, UTC timestamp, and rationale.
- `DISAGREED` must remain `OPEN`; disagreement must not be averaged or silently overwritten.
- A high-impact record may be `CLOSED` only with `second_review.status == AGREED`.

A text field claiming a reviewer is human is a self-attestation, not independent identity verification. The review register must retain the reviewer's stable public identity (for example, GitHub login or ORCID) and conflict disclosure for external scrutiny.

## 6. Closure evidence

A record may be `CLOSED` only when all required evidence is present and independently inspectable:

- Exact direct caller and indirect execution path.
- Runner entry point or command.
- Trigger conditions and branch restrictions.
- Matrix/protocol consumed.
- Authorization guard and execution order.
- Whether the guard fails closed.
- A specific negative test and its observed result.
- Run ID, job ID, artifact ID, and the exact commit tested.
- Exact source/test references and a concise evidence description.

The merger must reject placeholders, missing references, an unpassed negative test, an unresolved classification/influence value, missing second review for high-impact records, or reviewer identity collisions.

`CLOSED` documents only the occurrence role under this protocol. It does not establish code safety, protocol approval, statistical validity, or truth of the HCM claim.

## 7. Identity and population gates

Before merging any overlay, the implementation must:

1. Hash the exact inventory JSON bytes and compare the digest with the overlay and ledger.
2. Select exactly one inventory `refs[]` entry matching both `inventory_ref` and `review_commit_sha`.
3. Reconstruct every occurrence ID from that selected inventory entry, including path hash, line, and per-file match ordinal.
4. Reject unsafe paths, duplicate paths, malformed line numbers, duplicate reconstructed IDs, and missing/extra IDs.
5. Require exact set equality between reconstructed inventory IDs and ledger IDs.
6. Verify every ledger row's `path`, `line`, `commit_sha`, `repository_ref`, and `occurrence_id` against the reconstructed identity.
7. Reject duplicate overlay IDs and overlay IDs absent from the verified ledger.

Hash equality alone is not a substitute for inventory-to-ledger identity verification.

## 8. Non-authority invariants

The workflow must preserve all of the following:

```text
protocol_freeze = NOT_FROZEN
formal_calibration_authorized = false
confirmatory_execution_authorized = false
claim_support = false
promotion_authority = false
```

## 9. Batches

Use batches of 25–50 exact occurrence IDs. Each batch must bind to one exact target commit and one exact current inventory SHA-256, and must record count, first/last ID, and SHA-256 of the canonical UTF-8 sequence (one ID per line, including the final newline).

Do not start a new adjudication batch until the corrected merger, schema validation, integration/rejection tests, and fresh post-change inventory/snapshot all pass. Historical batches remain immutable and separate.

## 10. Completion

A population is complete only if every expected ID appears exactly once, no extras or duplicates exist, every record has an explicit disposition, every high-impact record has a second-review state, and every closed record passes all closure gates.
