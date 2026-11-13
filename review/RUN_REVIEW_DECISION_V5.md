# Run review decision — 2026-11-12 (V5 source refresh)

## Executive decision

The latest verified source pair is **target `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876` / main `982c6a10f1bd4262a9915f40a3c821adfd5c58c2`**. The latest inventory and exact snapshot artifacts are successful and checksum-verified. The previous Batch V3 and Preflight V4 outputs are historically valid for their own source pair but are superseded by the latest main comparison. The next required actions are Batch V4, read-only Preflight V5, and target-commit Software Assurance V3, all on `review/type1-v4-remediation` only.

No scientific adjudication, protocol freeze, formal calibration, confirmatory execution, claim support, or promotion is authorized.

## Latest source identity

- Inventory run/job/artifact: `43285928305` / `131419191291` / `13975650287`
- Inventory artifact SHA-256: `9125e3c8f691e334df20fd082658e39d65f90621a87659fcdeb48a07850548ba`
- Inventory JSON SHA-256: `57623b58ca2025872be7d504012232b4f5874b76706af6d82c5b81bd2a344e77`
- Target ledger SHA-256: `10c45fcaaec47819dc59df75d6f28a801022d185187933f10c665d858016b5e8`
- Main ledger SHA-256: `6b2e8955256418c1db3d3084e889c9d284ba463fd8fadd3e3e7d08f2bc274c9d`
- Provenance SHA-256: `39788c5c2e3668e20b969efbf038f96d2519014528d4bdb9cbea0b699c648a85`
- Target reconciliation SHA-256: `5118de3094fc16bacaa7c2b4258f463a8242980cfa47058c396d4c0040336705`
- Main reconciliation SHA-256: `2ee3490ed1b4a43616e36b613f0c1df18f9415feed42bf9acacfdb10ad3f8747`
- Target: 1,800 occurrences / 271 paths; main: 865 occurrences / 196 paths.
- Snapshot run/job/artifact: `43286179153` / `131420071578` / `13975170830`
- Snapshot artifact SHA-256: `3b9cb35257013f57d992306cd903046bc32ea8d3cedf72fc129f6976eee81d83`; 289/289 selected files present; 292 extraction checks; zero errors; zero missing paths.
- Snapshot manifest SHA-256: `b1f2b82bcdb61bf8827b35084ae5483759c8633a750fca0d411e4d70480d8df8`; inner ZIP SHA-256: `2cb08ab485f74b4d88785448c4bc769b4cda12e4429d0ae10c053b3840d0a0ff`; certificate SHA-256: `2a88707ca8e6820a9c18ad5d708ec65f43fed2b125efe9dd780b94e726e3df47`; extraction verification SHA-256: `2e1f6c1134dd01d1cb39ce184865212f621bab3bf250aee0d6376f71971a31ef`.
- Both latest source workflows ran successfully from review branch commit `d7fdba128f88d9e7147dad92b52e101cf01af4f6`.

## Main-comparison change: do not silently exclude

Main moved from `e6234f6895e3bc6c10b089a5e4f741f2143bb02f` (789 occurrences / 193 paths) to `982c6a10f1bd4262a9915f40a3c821adfd5c58c2` (865 / 196). A record-level comparison found 76 additions and zero removals. All 76 additions are accounted for by exactly three commits, each adding one audit workflow:

| Added workflow | New main occurrences |
|---|---:|
| `.github/workflows/type1-human-overlay-preflight-v4.yml` | 35 |
| `.github/workflows/type1-target-batch-generation-v3.yml` | 29 |
| `.github/workflows/type1-software-assurance-v2.yml` | 12 |
| **Total** | **76** |

All 789 previous main occurrence IDs remain present. Preserve the full 865-record current-main ledger. These 76 are audit-infrastructure self-inclusion; they are not evidence of 76 new scientific/application-code changes. Do not delete or silently exclude them. Future audit tooling should remain on the review branch, not be added to `main`.

## Target ledger stability

Compared inventory run `43249081611` / artifact `13956859801` against `43285928305` / `13975650287`: all 1,800 target occurrence IDs remain in the same order and every occurrence record payload is byte-semantically equal. Only the inventory identity envelope changed. This supports preserving prior target-level navigation and review history while regenerating all source-bound outputs.

## Run-by-run dispositions

| Run | Workflow | Artifact | Decision |
|---|---|---|---|
| `43281405115` | Legacy Batch V1 | none | Failed: CLI omitted `--inventory`, `--provenance`, `--artifact-metadata`; not batch evidence. |
| `43282259219` | Overlay Apply V1 | `13972942067` | Preflight-only; 3 OPEN/PENDING rows, 0 adjudications; older source pair. |
| `43282035611` | Overlay Apply V2 | `13972742073` | Preflight-only; 3 OPEN/PENDING, 0 adjudications; older source pair. |
| `43282131463` | Preflight V3 | `13972333544` | 3 OPEN/PENDING, 0 adjudications; valid only for older source pair. |
| `43285036238` | Preflight V4 | `13974796188` | 3 OPEN/PENDING, 0 adjudications; valid at execution for inventory `43249081611` / snapshot `43249503611`, now superseded. |
| `43281830641` | Software Assurance V1 | `13973366106` | Scan commit was review branch `d7fdba128f88d9e7147dad92b52e101cf01af4f6`, not target `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`; preliminary only. |
| `43284828022` | Software Assurance V2 | `13974288142` | Correctly scanned detached target commit `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876` and verified 289 snapshot files; source-pair metadata is previous pair. Findings remain relevant to unchanged target commit, but rerun V3 to bind latest source pair. |
| `43281787384` | Batch V2 | `13972343443` | 72 batches / 1,800 IDs, but main commit `fe949...` / 728; older source pair. |
| `43278814319` | Batch V3 | `13971981832` | 72 batches / 1,800 IDs, but main commit `e623...` / 789; previous source pair, not current. |
| `43281950640` | Priority occurrence guard | `13973407050` | 23/23 identity-field mutations rejected; engineering negative-gate evidence only. |
| `43280973606` | Governance implementation snapshot | `13972975802` | 18-file curated snapshot, not the 289-file exact target snapshot. |
| `43280802583` | Manual adjudication governance tests | none | 44 tests passed; software/governance tests only, no human adjudication. |
| `43285928305` | Latest governance inventory | `13975650287` | Success; latest source pair. |
| `43286179153` | Latest exact review snapshot | `13975170830` | Success; latest 289-file exact target snapshot. |

All 12 available artifacts were downloaded and ZIP-tested; no artifact was available for runs `43281405115` and `43280802583`.

## Software assurance V2 findings (exact target commit)

Artifact `13974288142` binds `scan_commit` to `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876` and verifies all 289 snapshot-selected target files. Scanner outputs are triage evidence, not automatic vulnerability confirmations:

- actionlint exit 123; 97 diagnostic headers, including 92 ShellCheck diagnostics and 5 non-ShellCheck workflow diagnostics.
- zizmor exit 14; 205 findings: 164 High, 37 Medium, 4 Informational. Rule counts: 151 unpinned uses, 19 excessive permissions, 18 artipacked, 13 template injection, 2 dangerous triggers, 1 cache poisoning, 1 superfluous action.
- Scorecard exit 0; score 5.7. Its report lists 71 existing vulnerabilities; the zero exit code does not mean a clean security posture.

Highest-priority paths to triage first (scanner findings, not confirmed exploitability):

- `.github/workflows/scientific-validation.yml`: workflow-level write permissions (`contents`, `packages`, `pages`, `id-token`, `security-events`) and shell interpolation of `github.event.client_payload` around lines 1509, 1528, 3289, and 3293.
- `.github/workflows/build-image.yml`: workflow-level `packages: write` and shell interpolation involving `secrets.GITHUB_TOKEN` around line 30.
- `.github/workflows/evolution.yml` and `.github/workflows/release-lock.yml`: privileged `workflow_run` trigger patterns requiring upstream-artifact and privilege-boundary review.
- `.github/workflows/release-lock.yml`: cache-poisoning finding around the setup-node cache configuration.

These findings require path-specific human triage and independent software review. No finding is closed by this report.

## Required execution order

1. Upload the six new files in this package to `review/type1-v4-remediation` only; preserve paths. Do not add them to `main` and do not merge the review branch.
2. Commit on the review branch. Batch V4 may auto-run on push; otherwise dispatch it manually. Require 72 batches, 25 records each, 1,800 unique IDs, inventory artifact `13975650287`, main commit `982c6a10f1bd4262a9915f40a3c821adfd5c58c2`, and main ledger SHA `6b2e8955256418c1db3d3084e889c9d284ba463fd8fadd3e3e7d08f2bc274c9d`.
3. Dispatch Preflight V5 with `csv_path=adjudication/incoming/first-three-occurrences-v4.csv` and `preflight_only=true`. Require exactly 3 OPEN/PENDING rows, zero adjudications, and source pair `43285928305` / `13975650287` / `43286179153` / `13975170830`.
4. Dispatch Software Assurance V3. Require exact target worktree `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`, 289/289 file equality, current main branch equality to `982c6a10f1bd4262a9915f40a3c821adfd5c58c2`, scanner versions and raw outputs, and a complete immutable manifest.
5. Submit the latest software evidence to an independent software reviewer and the separate statistical package to an independent statistician. Require expertise, scope, conflicts, and written decisions.
6. Do not freeze the protocol, apply/merge adjudications, run formal calibration/confirmatory execution, support the scientific claim, or promote until all independent reviews and gates are complete.

## Scope and limits

This is a provenance and workflow decision, not an independent scientific review. It does not prove absence of exploitable vulnerabilities, establish scientific validity, or grant any execution/promotion authority. Unknowns remain open until evidence closes them.
