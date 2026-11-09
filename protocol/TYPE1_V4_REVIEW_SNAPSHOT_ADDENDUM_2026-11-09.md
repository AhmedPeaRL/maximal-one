# Type-I V4 — Exact Review Snapshot Addendum (2026-11-09)

**Status:** `EXACT_SNAPSHOT_VERIFIED — REVIEW_ONLY — ADJUDICATION_OPEN`

**Repository:** `AhmedPeaRL/maximal-one`

**Target review commit:** `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`

**Inventory workflow-definition commit:** `8ea2a4a13abfab4d4bf36d2aa64e79dafce87ab6`

**Snapshot workflow-definition commit:** `8ea2a4a13abfab4d4bf36d2aa64e79dafce87ab6`

**Review branch head at evidence checkpoint:** `8ea2a4a13abfab4d4bf36d2aa64e79dafce87ab6`

**Main comparison commit:** `00bbd1fbd6df41b3e988ace75c480ea6232cfb86`

## 1. Identity roles

These three identities are separate and must never be conflated:

1. `ad106...` is the immutable target commit whose files and occurrence population are under review.
2. `8ea2...` is the workflow-definition revision used by the inventory and snapshot runs. At this checkpoint, it is also the review-branch head.
3. `00bbd...` is the exact `main` comparison commit.

Later branch movement must be recorded as a new observation. It must not be backdated into this addendum.

## 2. Exact inventory and snapshot provenance

### Inventory

- Workflow run: `42523935885`
- Job: `128863209001`
- Artifact: `13634199148`
- Inventory JSON SHA-256: `88222e3178bc62854ffb8d1fa961c1fb4cfe582c9ff1082878ab759e011cc635`
- Inventory source commit: `ad106...`
- Workflow-definition commit: `8ea2...`

### Snapshot

- Workflow run: `42524103929`
- Job: `128863716926`
- Artifact: `13634392345`
- Outer artifact ZIP SHA-256: `72e49ad7f84d888fcd254a822b5aecf9a7fa9c0923cbb5327f809b60e1cedc33`
- Three-way identity certificate SHA-256: `03a42303b38c20ff9fd139bb9492d2cf2f70d7941331807da9865d529c9504c1`
- Outer manifest SHA-256: `f0c084f888e8d4b9f168f243668fca70a58f68f9f5c770b576dc5153ea3aee51`
- Nested self-contained snapshot ZIP SHA-256: `50f5989341556786db6899ffb5a9bbcc0e88eb3461a71c4444e7100f0bff04c3`
- Extraction verification: `verified=true`; 292 checked files; no errors.

The certificate binds:

`target_commit = inventory_source_commit = snapshot_review_commit = ad106...`

It separately records:

`inventory_workflow_definition_commit = snapshot_workflow_definition_commit = 8ea2...`

## 3. Exact occurrence populations

| Population | Commit | Paths with matches | Occurrences | Scanner exclusions |
|---|---|---:|---:|---:|
| Target | `ad106...` | 271 | 1,800 | 12 |
| Main comparison | `00bbd...` | 184 | 633 | 0 |

The 12 target scanner exclusions remain in the snapshot/hash scope with explicit reasons and handling. They must not be silently removed or described as zero exclusions.

Target discovery counts:

- `EXECUTION_CAPABLE_WORKFLOW_CANDIDATE`: 3
- `CODE_PATH_REQUIRES_CALL_GRAPH_REVIEW`: 253
- `WORKFLOW_CONTROL_PATH`: 118

These are automated discovery labels only. All 1,800 target rows remain `UNKNOWN / OPEN / PENDING`. The manual overlay contains zero records. No complete call-graph review or human adjudication is claimed here.

## 4. Historical documents and embedded ledgers

The exact snapshot contains documents and evidence records that correctly describe earlier review epochs. They remain historical evidence; they must not be treated as current identity for the `ad106...` review.

| File / record | Historical identity | Required treatment |
|---|---|---|
| `evidence/provenance.json` | target `e41fb7392b58198e8a4d8fa28b470b12b6ad2c31`; main `fe0daded51229ed88d449c2eb68252455fd4ad7c`; workflow definition `8073c6566f0342a748042d82762621479b2c34ad`; run `42292957449`; counts 1,711 / 583 | Preserve as historical. |
| `evidence/CURRENT_EVIDENCE_REGISTER.json` | target `e41fb...`; main `fe0dad...`; workflow definition `8073c...`; artifacts `13540293414` / `13540244231` | Its filename does not make its contents current. |
| `evidence/occurrence_level_manual_ledger.json` in the repository snapshot | target `e41fb...`; 1,711 rows | Historical target ledger. Do not substitute for the current 1,800-row ledger. |
| `evidence/main_occurrence_level_manual_ledger.json` in the repository snapshot | main `fe0dad...`; 583 rows | Historical main ledger. It does not cover current main `00bbd...` with 633 occurrences. |
| `protocol/CURRENT_RUN_EVIDENCE_ADDENDUM_2026-11-07.md` | target `e41fb...`; main `fe0dad...`; workflow definition `e1c4849f8507eed80c8ab3efb94ee7aedd6b8a68`; runs `42310101658` / `42310673682`; artifacts `13547224511` / `13547798098`; counts 1,711 / 583 | Preserve as the 2026-11-07 checkpoint. |
| `protocol/TYPE1_MANUAL_OCCURRENCE_ADJUDICATION_PROTOCOL_V3.md` | target `e41fb...`, 1,711 occurrences; main `9a3390acedbb146111be64f9a45a00b41a85be25`, 622 occurrences | Its batch identity is historical. Generate new batches for the current inventory. |
| `protocol/INDEPENDENT_HUMAN_STATISTICAL_REVIEW_EXACT_SNAPSHOT_ADDENDUM.md` | older target `e8e127259e475b06599d3f5fc550cd6a616a127f`; runs `41349619676` / `41349751627` | Historical handoff, not the current V4 snapshot. |
| `protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json` | `reviewed_base_commit=a9808bd999a7ad902daf15606272529ca9af4580` | Design ancestry field, not current review target. |
| `protocol/TYPE1_GOVERNANCE_REVIEW_FINDINGS_2026-11-01.md` | references `a9808...` | Preserve as historical findings. |

The 2026-11-08 handoff addendum is a later branch-level document, not part of the 289-file `ad106...` target snapshot. It must remain a separate later document.

## 5. Current-ledger reconciliation requirement

The new target ledger in the exact snapshot is bound to `ad106...`, contains 1,800 rows, and has SHA-256:

`5aaa4a796fe99eb1aeb9f803aba1517d5724c5e92b6c0400098f2e38d858651c`

The repository-embedded main ledger is still bound to `fe0dad...` and has 583 rows, while the new main inventory at `00bbd...` contains 633 occurrences.

This is an evidence-generation gap. It is not a reason to infer classifications for 50 records.

Required actions:

1. Generate a new main occurrence ledger from the exact `00bbd...` inventory.
2. Reconcile it against all 633 current main occurrence IDs.
3. Require zero duplicates, zero missing IDs, zero extra IDs, and exact identity-field matches.
4. Preserve the 583-row `fe0dad...` ledger unchanged as historical.

## 6. Priority execution-path occurrences

1. `refs/audit/target/2f8523fcf7c5/73/4` — `.github/workflows/type1-calibration-runtime-pilot.yml:73`
   - Invokes `analysis.type1_calibration_pilot` with 2 outer repetitions and 200 surrogates.
   - Workflow-level branch and checkout guards are present before invocation.
   - Pilot artifact is `PILOT_COMPLETE_DIAGNOSTIC_ONLY`; `formal_calibration_pass=false`.
   - Full occurrence adjudication remains OPEN.

2. `refs/audit/target/40d0253a5dd6/60/6` — `.github/workflows/type1-v4-cross-runner-worker-order.yml:60`
   - Invokes `analysis.calibrate_null_type1_scenario` with `--engineering-test`.
   - Workflow requires `refs/heads/review/type1-v4-remediation` and exact `HEAD == GITHUB_SHA` before invocation.
   - This is an engineering reference, not formal calibration.
   - Full occurrence adjudication remains OPEN.

3. `refs/audit/target/40d0253a5dd6/123/9` — `.github/workflows/type1-v4-cross-runner-worker-order.yml:123`
   - Invokes the same runner in a separate matrix-worker path with `--engineering-test`.
   - The workflow repeats the branch and checkout guard before invocation.
   - This occurrence is distinct from item 2 and remains separately OPEN.

The engineering entry point in `analysis/calibrate_null_type1_scenario.py` calls `require_authorized_branch()` and checks the exact GitHub checkout identity.

The formal entry point `formal_main()` does not currently perform those checks itself. Its static `V4_APPROVED=False` gate currently blocks execution, but the formal path does not independently load and hash-verify the separate freeze and authorization JSON records. This defense-in-depth gap must be remediated before any future approval.

## 7. Statistical review status

The V4 matrix remains:

- `DRAFT_PENDING_REMEDIATION_AND_INDEPENDENT_REVIEW`
- `freeze_state=NOT_FROZEN`
- `confirmatory_execution_authorized=false`
- `claim_support=false`
- `promotion_authority=false`

Candidate dimensions remain candidates: nine stationary Gaussian AR scenarios; `N=3328`; DGP burn-in 2,000; `R=2000`; `M=1000`; nominal alpha 0.05; candidate seed 20261021.

The acceptance rule remains `null`. The historical 0.075 ceiling remains `NOT_JUSTIFIED_OR_APPROVED`.

Historical V1 outcomes remain unchanged under their historical two-sided 95% Wilson rule:

- AR1: 52/1000 — pass
- AR5: 49/1000 — pass
- AR2: 60/1000 — fail upper endpoint
- AR10: 73/1000 — fail

Do not retroactively apply a V4 one-sided rule to V1.

## 8. Authority state

Until independent human statistical review, main-ledger reconciliation, occurrence adjudication, and a new prospective protocol are complete:

```text
protocol_freeze = NOT_FROZEN
formal_calibration_authorized = false
confirmatory_execution_authorized = false
claim_support = false
promotion_authority = false
```

No formal calibration, confirmatory analysis, power analysis, or claim promotion is authorized by this addendum.
