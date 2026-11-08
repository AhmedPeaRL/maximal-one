# Type-I V4 — Manual Occurrence Adjudication Protocol V3 (Corrective Revision)

## Status

`REVIEW_PROTOCOL_ONLY_NOT_ADJUDICATION_NOT_AUTHORIZATION`

This protocol governs manual documentation of occurrences. It does not classify occurrences automatically, freeze a calibration protocol, authorize confirmatory execution, support a scientific claim, or grant promotion authority.

## 1. Current evidence identity

Repository: `AhmedPeaRL/maximal-one`

Review branch: `refs/heads/review/type1-v4-remediation`

Evidence-bearing implementation commit: `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`.

V3 governance CI run `42496439182`, job `128779691121`, completed successfully on the exact `ad106...` commit. The log records **28 tests passed** under Python `3.11.15` with `jsonschema==4.26.0`, followed by `V3_NON_AUTHORITY_INVARIANTS_PRESERVED`. This is software verification only.

Current V3 manual-adjudication target inventory:

- Target ref: `refs/audit/target`
- Target commit: `e41fb7392b58198e8a4d8fa28b470b12b6ad2c31`
- Target occurrences: `1711`
- Target reconciliation: `RECONCILED`
- Main comparison commit: `00bbd1fbd6df41b3e988ace75c480ea6232cfb86`
- Main comparison occurrences: `633`
- Main reconciliation: `RECONCILED`
- Inventory run/artifact: `42499309283` / `13624359912`
- Reference-inventory SHA-256: `5b4fbdca1bbdf56d47f38519fecf2b7cc325e3b41df2b9fe97dcd70cd9fd0b9a`
- Provenance SHA-256: `6835bedf923142231d76a52874ce3fad5327508f4f95d955a215962c597d318b`

The target inventory and its occurrence ledger are bound to `e41fb...`, not to the current review-branch head `ad106...`. All 1,711 target rows and 633 main rows remain `OPEN`, `UNKNOWN`, and `PENDING`.

Target-code snapshot run/artifact: `42499453986` / `13624771675`.

- Snapshot target commit: `e41fb7392b58198e8a4d8fa28b470b12b6ad2c31`
- Manifest SHA-256: `aede6957e79a7d91a7866e833bf6dd67856c65a1b863cf0c5a57c9e1dc140e1d`
- Self-contained snapshot ZIP SHA-256: `087a9c01c6e8c549c05d8a30120fcaa8f9cc8e4c6a240c381946af99114d907f`
- Selected/present files: `264` / `264`
- Extraction checks: `267`; verified: `true`; errors: none

Separate governance-implementation snapshot run/artifact: `42496227821` / `13623039718`.

- Implementation commit: `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`
- Outer artifact SHA-256: `ebc8ddf4b04594e81818374862cd274e781ff4d88223224b76f15008352c7748`
- Manifest SHA-256: `e0b301df102b7772cadac371bfd41a12915edf7cbe3953ecd6c31864b1ab4e46`
- Embedded governance ZIP SHA-256: `2cd3b7bd76a0d39e866b8d182f30edf6f131f82a9f076dbb6bdda55e5ad199ea`
- Files: `13`; all 13 manifest file hashes verified.

**Snapshot boundary:** the target snapshot at `e41fb...` and the governance implementation snapshot at `ad106...` answer different questions. The first is a target-code snapshot; the second is a curated governance-source snapshot. The 13-file governance snapshot does not include `protocol/TYPE1_BATCH_REGISTER_V3_B001.json` or `tests/test_type1_evidence_register_v3.py`. The next snapshot-workflow revision is required to include both and must produce a new post-commit artifact before the expanded governance package is called complete.

**Separate V4 statistical-review boundary:** the current V4 human-review request requires its inventory source commit to equal the exact review commit. The current inventory and target-snapshot artifacts above are both bound to `e41fb...`, so they do not satisfy an exact statistical-review handoff for `ad106...`. The V4 handoff addendum specifies the required fresh inventory and exact-snapshot dispatches. Do not describe the `e41fb...` snapshot as the exact V4 review snapshot for `ad106...`.

The machine-readable evidence register is `protocol/EVIDENCE_REGISTER_V3.json`.

## 2. Historical evidence must not be rebound

An earlier inventory used target commit `e41fb7392b58198e8a4d8fa28b470b12b6ad2c31`, main commit `9a3390acedbb146111be64f9a45a00b41a85be25`, target count `1711`, main count `622`, and reference-inventory SHA-256 `7171edb8da35b46a470e819626266f497983f4dee77c32ecc8aac2f82b9f86ec`.

That older inventory and any batch digest created against it remain historical. Do not change their metadata, reuse their register identity, or silently rebind their batch digest to the current inventory. The current `BATCH_001` uses the next 25 IDs (ledger positions 26–50), not the historical positions 1–25, and is bound to the current inventory SHA-256. It remains navigation-only until a human reviewer begins and records adjudication.

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

The corrected merger, schema tests, integration/rejection tests (28 tests in the V3 CI run), fresh inventory, target snapshot, and separate governance implementation snapshot have passed their stated engineering and identity checks. This permits a navigation-only batch to be prepared; it does not itself adjudicate any occurrence. Before substantive review, confirm the primary reviewer declaration and arrange a distinct human second reviewer for every high-impact occurrence. AI and automated systems are not reviewers. Historical batches remain immutable and separate.

## 10. Completion

A population is complete only if every expected ID appears exactly once, no extras or duplicates exist, every record has an explicit disposition, every high-impact record has a second-review state, and every closed record passes all closure gates.
## 11. Current V4 statistical-review handoff gate

The V4 candidate remains `DRAFT_PENDING_REMEDIATION_AND_INDEPENDENT_REVIEW`; its acceptance rule is unresolved (`acceptance_rule: null`). The historical `0.075` ceiling is not justified or approved for V4. The V4 review request contains required reviewer-attribution fields and must be completed by an attributable independent human statistician.

Before that review begins, generate a fresh governance inventory with `target_commit=ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876` and `main_commit=00bbd1fbd6df41b3e988ace75c480ea6232cfb86`. Then generate the exact review snapshot with `review_commit=ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`, `inventory_source_commit` equal to that same SHA, the newly generated inventory artifact ID, and `inventory_workflow_commit=ad106dddd2b6c9a57c90bd5bdd9f4530fe7`. Accept the handoff only if the three-way identity certificate binds target, inventory source, and snapshot review commit to the same SHA and all manifest hashes verify.

This V4 statistical-review inventory is separate from the V3 manual-adjudication target ledger and `BATCH_001`, which remain bound to `e41fb...`. Do not rebind or overwrite the V3 ledger or batch. No formal calibration, power analysis, protocol freeze, claim support, or promotion is authorized by this handoff.
