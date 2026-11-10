# Type-I V4 — Current Exact-Snapshot Identity Addendum
**Prepared:** 2026-11-09  
**Purpose:** Administrative identity binding for independent human review  
**Repository:** https://github.com/AhmedPeaRL/maximal-one  
**Review branch:** `review/type1-v4-remediation`

> This addendum binds the review request to the exact immutable snapshot below. It does not replace, erase, or rewrite historical handoff records. It is not an independent statistical opinion, approval, protocol freeze, execution authorization, or claim endorsement. The project author/maintainer must review, complete, and sign the author fields before distribution.

## 1. Controlling identity for this review

| Item | Exact value |
|---|---|
| Scientific/source target commit | `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876` |
| Main comparison commit | `00bbd1fbd6df41b3e988ace75c480ea6232cfb86` |
| Workflow-definition commit used by inventory and snapshot | `8ea2a4a13abfab4d4bf36d2aa64e79dafce87ab6` |
| Inventory workflow run / job | `42523935885` / `128863209001` |
| Inventory artifact ID | `13634199148` |
| Exact-snapshot workflow run / job | `42524103929` / `128863716926` |
| Exact-snapshot artifact ID | `13634392345` |
| Snapshot review commit | `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876` |
| Inventory source commit | `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876` |
| Protocol freeze | `NOT_FROZEN` |

The target, inventory source, and snapshot review commit are identical. The workflow-definition identity is separately recorded and must not be confused with the scientific/source target.

## 2. Downloaded artifact identities and SHA-256

| Artifact | ID | SHA-256 |
|---|---:|---|
| Governance implementation snapshot | `13634122584` | `3d001df8becd23549ca5a36a0bece508a297646421bc20f1aec5def44a80584b` |
| Governance inventory + ledgers | `13634199148` | `5ceca1e6c5a2950bddd4b4e4f2fb04028b69b8ed4f7b424184538bed7198c69b` |
| Exact review snapshot | `13634392345` | `72e49ad7f84d888fcd254a822b5aecf9a7fa9c0923cbb5327f809b60e1cedc33` |

Additional content hashes:
- Inventory JSON: `88222e3178bc62854ffb8d1fa961c1fb4cfe582c9ff1082878ab759e011cc635`
- Inventory scanner source: `e8a0ed0c9ccb129a693cdd322a8b4bbcd90922805763dd3abe371e06a7b5906d`
- Exact-snapshot manifest: `f0c084f888e8d4b9f168f243668fca70a58f68f9f5c770b576dc5153ea3aee51`
- Nested self-contained snapshot ZIP: `50f5989341556786db6899ffb5a9bbcc0e88eb3461a71c4444e7100f0bff04c3`

## 3. Verified inventory and snapshot facts

- Governance audit run `42523663514`: 31 tests passed.
- Governance implementation snapshot run `42523663482`: 18 source files captured; the 18 source-file hashes passed.
- Inventory run `42523935885`: binary-safe scanner tests 2/2; generated-evidence exclusion tests 2/2.
- Target inventory: 271 files with matches; 1,800 occurrence rows; 12 paths excluded from line-based occurrence discovery.
- Main inventory: 184 files with matches; 633 occurrence rows; zero excluded paths.
- Target and main reconciliation both report `RECONCILED`; no missing, extra, duplicate, or identity-mismatched occurrence IDs.
- All target rows (1,800) and main rows (633) remain `OPEN`, `UNKNOWN`, `PENDING`; execution influence and guard status remain `UNKNOWN`; historical diagnostic governance status remains `UNDETERMINED`.
- Manual adjudication overlay records: zero.
- Exact snapshot selected scope: 289 files; present: 289; missing scope paths: zero; missing required paths: zero.
- Nested archive integrity check passed; all 292 nested SHA-256 entries verified. The 289 repository-source checksums also matched the corresponding files in the nested archive.
- All 12 scanner-excluded paths are retained in the exact snapshot and its hash scope. In the snapshot manifest, `excluded_paths: []` means no selected-scope files were missing; scanner exclusions are separately recorded under `scanner_exclusions` with `scanner_exclusion_count: 12`.

### The 12 target scanner exclusions

Nine generated text files added by this remediation:
1. `evidence/CURRENT_EVIDENCE_REGISTER.json`
2. `evidence/main_occurrence_level_manual_ledger.json`
3. `evidence/occurrence_level_manual_ledger.json`
4. `evidence/provenance.json`
5. `evidence/reference_inventory.json`
6. `evidence/snapshot_manifest.json`
7. `evidence/three_way_identity_certificate.json`
8. `adjudication/review_1711_e41fb_adjudication_template.csv`
9. `adjudication/main_583_fe0d_adjudication_template.csv`

Two pre-existing explicit generated-evidence exclusions:
10. `protocol/TYPE1_EVIDENCE_GOVERNANCE_REGISTER_V1.md`
11. `protocol/TYPE1_V3_V4_OCCURRENCE_LEVEL_MANUAL_LEDGER_2026-10-31.json`

One non-text Git blob:
12. `evidence/self-contained-review-snapshot.zip` (retained and recorded with blob identity, size, and SHA-256; not line-scanned).

The nine-path regression test explicitly checks the nine generated text paths are reported as `EXCLUDED_FROM_OCCURRENCE_SCAN_RETAIN_IN_SNAPSHOT_SCOPE` and are not emitted as scanned source entries, while an ordinary source file remains scanned. The separate binary-safe test suite passed 2/2.

## 4. Automated discovery priorities — not adjudications

The current target inventory reports:
- 3 `EXECUTION_CAPABLE_WORKFLOW_CANDIDATE` occurrences:
  - `.github/workflows/type1-calibration-runtime-pilot.yml`, line 73
  - `.github/workflows/type1-v4-cross-runner-worker-order.yml`, lines 60 and 123
- 253 `CODE_PATH_REQUIRES_CALL_GRAPH_REVIEW` occurrences.
- 118 `WORKFLOW_CONTROL_PATH` occurrences.

These are automated discovery labels only. They do not prove that a path is authorized, reachable, blocked, safe, or scientifically valid. Human reviewers must inspect workflow triggers, branch restrictions, exact commands, direct and indirect callers, guard ordering, environment variables, outputs, artifacts, negative tests, and all alternate/legacy execution routes.

## 5. Historical identity references inside the snapshot

Some embedded handoff and decision documents preserve older review identities, including references to `5b814ddf529b04b3ea9fda908373c3676eb647c1`, `fe0daded51229ed88d449c2eb68252455fd4ad7c`, `e41fb7392b58198e8a4d8fa28b470b12b6ad2c31`, and `e8e127...` (as well as older main-branch identities).

Those records are retained as historical documents. They are **not** the controlling identity for the present review. For this review only, use the controlling identity in Section 1 and the file/artifact hashes in Section 2. Do not silently edit historical records or treat their old snapshot hashes as current.

## 6. Required independent reviewer attribution

**Reviewer full name:** [REQUIRED]  
**Affiliation:** [REQUIRED]  
**Relevant statistical / software-governance qualifications:** [REQUIRED]  
**Relevant publications or experience:** [REQUIRED]  
**Prior involvement with this project:** [REQUIRED — state NONE if applicable]  
**Financial, professional, or personal conflicts:** [REQUIRED — state NONE if applicable]  
**Exact commit and hashes actually reviewed:** [REQUIRED]  
**Review date:** [REQUIRED]  
**Attributable signature or written confirmation:** [REQUIRED]

AI-generated analysis is not independent human review. The reviewer must state what was actually inspected and must not imply review of files, runs, or artifacts they did not inspect.

## 7. Required dispositions

### Statistical-methods reviewer
Must explicitly resolve or recommend, with rationale:
- estimand and operational Type-I error definition;
- one-sided versus two-sided confidence-bound criterion;
- confidence level and numerical tolerance;
- multiplicity / all-scenarios decision rule;
- number of outer repetitions and operating characteristics;
- surrogate count and treatment of invalid, failed, or short attempts;
- scenario coverage and parameterizations;
- implementation equivalence and limits;
- prospective freeze requirements.

Historical V1 outcomes remain `NOT_PASSED` under the historical two-sided Wilson rule. No retrospective reclassification is permitted. The `0.075` ceiling is not approved by this addendum.

### Governance / execution-path reviewer
Must inspect occurrence-level evidence and call paths, prioritizing the 3 workflow runner candidates, 253 code-path occurrences, and 118 workflow-control occurrences, and must document exact dispositions, evidence, guard ordering, and negative tests. Unresolved rows must remain unresolved; no `UNKNOWN` may be converted to `NO` without evidence.

## 8. Non-authorization

This addendum and all successful CI jobs are review infrastructure only. They do **not** authorize:
- protocol freeze;
- formal Type-I calibration;
- confirmatory execution;
- power analysis as a confirmatory result;
- claim support;
- scientific claim promotion.

The exact snapshot records: `protocol_freeze = NOT_FROZEN`; `formal_calibration_authorized = false`; `confirmatory_execution_authorized = false`; `claim_support = false`; `promotion_authority = false`.

A later freeze and any execution authorization must be separate, prospective, attributable, and bound to a reviewed exact commit and digests.

## 9. Project-author attestation before sending

I confirm that I am distributing the exact artifacts identified above, that the historical records are preserved, and that no claim of independent review or scientific authorization is being made.

**Project author / maintainer:** [COMPLETE]  
**Date:** [COMPLETE]  
**Signature / attributable confirmation:** [COMPLETE]
