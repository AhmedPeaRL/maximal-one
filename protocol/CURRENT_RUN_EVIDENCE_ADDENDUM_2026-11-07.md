# Type-I V3/V4 current evidence addendum — 2026-11-07

## Exact evidence identity

- Repository: `AhmedPeaRL/maximal-one`
- Review branch workflow-definition commit: `e1c4849f8507eed80c8ab3efb94ee7aedd6b8a68`
- Target/source commit: `e41fb7392b58198e8a4d8fa28b470b12b6ad2c31`
- Main comparison commit: `fe0daded51229ed88d449c2eb68252455fd4ad7c`
- Inventory run/job/artifact: `42310101658` / `128209129904` / `13547224511`
- Snapshot run/job/artifact: `42310673682` / `128211028323` / `13547798098`
- Inventory JSON SHA-256: `502690ed3186644e8dfad01abb31ae27e6950afebb9b20d18b36298a8e4075c8`
- Inventory ZIP SHA-256: `49e2f07b1798f3072662d2965fdcded54ca49a8efc6aedf23eea69d7c5b00b38`
- Snapshot ZIP SHA-256: `45195e93ee4197a6496fda7a52f2ebe3a8b4e2c37c81f49e78c504b3c7f6695a`

## Verified inventory and snapshot

- Target inventory: 256 paths and 1,711 occurrence records.
- Main comparison inventory: 180 paths and 583 occurrence records.
- Both ledger record counts equal their declared occurrence counts.
- Both ledgers are fully unresolved: `manual_classification=UNKNOWN`, `status=OPEN`, `reviewer_disposition=PENDING` for every record.
- Snapshot manifest: 264 selected files, 264 present files, zero missing scope paths, zero missing required paths.
- Nested self-contained archive: 264/264 repository files match manifest SHA-256 values.
- Extraction verification: `verified=true`, 267 checked, no errors.
- Snapshot manual overlay: zero records.

## Current target-ledger triage counts

| Automated discovery class | Occurrences |
|---|---:|
| `EXECUTION_CAPABLE_WORKFLOW_CANDIDATE` | 3 |
| `CODE_PATH_REQUIRES_CALL_GRAPH_REVIEW` | 248 |
| `WORKFLOW_CONTROL_PATH` | 84 |
| `TEST_OR_GUARD` | 199 |
| `WORKFLOW_REFERENCE` | 135 |
| `GOVERNANCE_REFERENCE` | 405 |
| `PROTOCOL_OR_DOCUMENTATION_REFERENCE` | 478 |
| `POLICY_OR_HISTORICAL_REFERENCE` | 145 |
| `OTHER_REFERENCE` | 14 |

Automated classes are triage labels only, not manual adjudications.

## First three occurrences to adjudicate

1. `refs/audit/target/2f8523fcf7c5/73/4` — `.github/workflows/type1-calibration-runtime-pilot.yml:73` — invokes `analysis.type1_calibration_pilot` with two outer repetitions and 200 surrogates. Determine the exact trigger, branch guard, direct and indirect call path, output authority, and negative controls. Do not call it formal calibration based on its label.
2. `refs/audit/target/40d0253a5dd6/60/6` — `.github/workflows/type1-v4-cross-runner-worker-order.yml:60` — one occurrence of `analysis.calibrate_null_type1_scenario`. Trace this worker separately, including its `--engineering-test` context and all downstream artifact consumers.
3. `refs/audit/target/40d0253a5dd6/123/9` — `.github/workflows/type1-v4-cross-runner-worker-order.yml:123` — second occurrence of the same runner in a distinct workflow location. Adjudicate independently; do not merge it with item 2.

After these three, proceed through all 248 code call-graph candidates and 84 workflow-control candidates, preserving every occurrence ID and recording exact file hash/line, caller chain, trigger, protocol consumed, guard order, execution influence, negative test, exact test run/job/artifact, and closure evidence. Use `UNRESOLVED` when evidence is insufficient. Do not convert `UNKNOWN` to `NO` by inference.

## Checksum-register defect

The inventory artifact contains all six intended payload files and their hash values are individually correct, but `artifacts/SHA256SUMS.txt` contains literal backslash-n sequences instead of physical line breaks. It has one physical line, not six. This is a defect in the checksum register format, not a mismatch in the inventory JSON hash or the snapshot's independent manifest verification. Correct the newline handling, assert exactly six physical lines, and run `sha256sum -c` before uploading the next inventory artifact.

## Authority and disposition

- `protocol_freeze=NOT_FROZEN`
- `formal_calibration_authorized=false`
- `confirmatory_execution_authorized=false`
- `claim_support=false`
- `promotion_authority=false`

This addendum records artifact identity and automated discovery. It does not constitute human adjudication, independent statistical review, protocol approval, calibration evidence, or permission to execute confirmatory analysis. AI-assisted tracing must be labelled as such and must not be represented as an independent human review.

## Stale-document warning

The older `TYPE1_V4_MANUAL_GOVERNANCE_REVIEW_PLAN_2026-11-06.md` in the snapshot identifies commit `5b814ddf...`, inventory run `42106008761`, artifact `13451387326`, and 1,649 review occurrences. Those are historical references and must not be used as the current evidence identity. Use the exact identity block at the top of this addendum for the 2026-11-07 runs. Historical engineering registers remain historical; do not silently rewrite their original run outcomes.
