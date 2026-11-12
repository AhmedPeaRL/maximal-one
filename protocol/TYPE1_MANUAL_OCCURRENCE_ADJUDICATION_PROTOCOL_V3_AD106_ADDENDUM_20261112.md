# Manual Occurrence Adjudication Protocol V3 — ad106 Population Addendum

**Record date:** 2026-11-12  
**Status:** `SUPPLEMENTAL_IDENTITY_RULES_ONLY — NOT ADJUDICATION — NOT AUTHORIZATION`

## 1. Scope

This addendum supplements `TYPE1_MANUAL_OCCURRENCE_ADJUDICATION_PROTOCOL_V3.md` for the separate ad106 target population. It does not replace the historical V3 target population, ledger, or batch.

The exact ad106 target is `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`. Its latest inventory re-verification is run `43072014463`, artifact `13877643344`, inventory SHA-256 `b30db3cb254f276a6d2707cbdbc4bef06f1dad92c4063c7098eedaae84154c92`. The exact target snapshot is run `43072282939`, artifact `13877613612`, with target, inventory source, and snapshot review commit all equal to `ad106...`.

The target contains 1,800 occurrence records across 271 inventory paths. The separate main comparison contains 711 records across 189 paths at `0fa531bc844b1891f0574564add8eef5e20813d8`. These populations must never be merged.

## 2. Historical identity preservation

The existing `protocol/EVIDENCE_REGISTER_V3.json` and `protocol/TYPE1_BATCH_REGISTER_V3_B001.json` retain their earlier `e41fb...` / 1,711-occurrence identity. Do not edit, overwrite, or rebind them.

The 72-batch ad106 archive (`13876574962`) is a separate navigation-only batch set. If its batch files are later committed, place them under a new identity-bearing directory such as `protocol/ad106_batches_20261111/`; do not write them over the historical `BATCH_001` path.

## 3. Current human-review state

The three priority occurrence IDs are:

1. `refs/audit/target/2f8523fcf7c5/73/4`
2. `refs/audit/target/40d0253a5dd6/60/6`
3. `refs/audit/target/40d0253a5dd6/123/9`

The preflight artifact `13877758502` records all three as OPEN/PENDING and records zero applied adjudications. Its lineage points to inventory run `42870936071` and snapshot run `42871210051`; those identities must remain unchanged in that artifact. The newer inventory/snapshot re-verification pair is `43072014463` / `43072282939`. If a new review action is to rely on the latest pair, create a new preflight artifact bound to those exact run IDs rather than editing the old artifact.

## 4. Reviewer roles and closure

Ahmed Salahuddin may be recorded as the human repository owner and primary reviewer, with authorship, intellectual, professional, reputational, and prospective-benefit interests disclosed. This is not an independent review.

AI assistance may support navigation, transcription, drafting, code search, and evidence summaries. ChatGPT is not a human reviewer, second reviewer, academic supervisor, or legally accountable co-author.

Every high-impact or unresolved occurrence remains OPEN until a distinct human second reviewer records identity, role, conflicts, UTC timestamp, explicit agreement/disagreement, and rationale. A CLOSED status additionally requires a specific passing negative test and inspectable run/job/artifact/commit evidence. Disagreement remains OPEN. Unknown must never be converted to NO.

## 5. Non-authority invariants

```text
protocol_freeze = NOT_FROZEN
formal_calibration_authorized = false
confirmatory_execution_authorized = false
claim_support = false
promotion_authority = false
```

This addendum does not adjudicate any occurrence and does not authorize any execution.
