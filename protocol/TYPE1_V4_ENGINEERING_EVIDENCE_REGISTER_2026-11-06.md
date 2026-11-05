# Type-I V4 — Engineering Evidence Register (2026-11-06)

Reviewed repository snapshot: `5b814ddf529b04b3ea9fda908373c3676eb647c1`
Branch: `review/type1-v4-remediation`
Main at review time: `fe0daded51229ed88d449c2eb68252455fd4ad7c`

All 31 artifact ZIPs linked in the supplied workflow runs were downloaded and opened. Every ZIP passed archive integrity testing. Each local ZIP SHA-256 matched the digest returned by GitHub Actions artifact metadata.

## Run-level outcomes

| Run | Workflow | Result | Main interpretation |
|---|---|---|---|
| [42106008752](https://github.com/AhmedPeaRL/maximal-one/actions/runs/42106008752) | Type-I V4 Official Runner Engineering Equivalence | SUCCESS | Six-replicate, one-scenario, 1,000-surrogate engineering equivalence only |
| [42108047580](https://github.com/AhmedPeaRL/maximal-one/actions/runs/42108047580) | Type-I Priority Occurrence Guard and Negative-Gate Tests | SUCCESS | 23 resume identity mismatches rejected; not calibration |
| [42106008761](https://github.com/AhmedPeaRL/maximal-one/actions/runs/42106008761) | Type-I V3/V4 Governance Inventory Audit | SUCCESS | Inventory and ledgers generated; all manual classifications remain open |
| [42106395007](https://github.com/AhmedPeaRL/maximal-one/actions/runs/42106395007) | Type-I Exact Review Snapshot and SHA-256 | SUCCESS | 262-file exact snapshot and hashes generated |
| [42106629892](https://github.com/AhmedPeaRL/maximal-one/actions/runs/42106629892) | SOS Robustness Gate | FAILURE | Final claim gate blocked: 0/2 eligible independent secondary domains |
| [42106684822](https://github.com/AhmedPeaRL/maximal-one/actions/runs/42106684822) | Scientific Claim Promotion Gate | FAILURE | Dataset eligibility contract blocked: 0/2 eligible independent secondary domains |

## Artifact inventory and SHA-256

### Run 42106629892 — SOS Robustness Gate

| Artifact ID | Name | ZIP SHA-256 |
|---|---|---|
| 13454540161 | autonomous-witness | `68b875c888c7dfcab50bcfdca2711e7564a988305fd94399b455622ba0179bb8` |
| 13453586453 | final-claim-gate-decision | `8e4fc40623b3c273a5d0a257884d755236de89dc97e0bce09a3d08dd3c72c76f` |
| 13453286384 | pip-freeze | `f3c251bb4e8cf2aa8b96a8bec5467e7248ca79119d3a7f4f4bfe66d23277fa92` |
| 13453092595 | final-provenance-closure | `eea615adb17f1a8e0e91dd0dc6b51d8878b7d21550121eea6ab3f8255c888e71` |
| 13453068093 | reproducibility-manifest | `ef7455acab4cd089dade02a96947c6a331408ef76c32e3817f04e1cfe0eb42ca` |
| 13452977668 | node-hash-18.20.8 | `a2c31d6326f36ccb549d1dfdb061bebb2304c1d7c421fc87f412aa9b5230b620` |
| 13452873085 | canonical-report | `28abb2b2489c3e24cc8d5de86e259374ec5c851b587a1428534ca57e27bb6202` |
| 13452786707 | dataset-eligibility-gate | `1c6bf21812f07a824b9e5f74921d24c73e158453614628c9c4238f9fea15ad6d` |
| 13452459261 | independent-verification | `7043e69d4b7b21adb609361f67d02885bb688350894070922f5ef5bfc6e1544f` |
| 13452338621 | node-hash-24.11.1 | `d3e3ea2f0e5a60a49058f195c87bc069da0b7a6978bc221c8ff4d9f692299984` |
| 13452324511 | report-hash | `2710868573b452c43b403b71ae5690d29b2f60b631ee07102132d565f7281539` |
| 13452277667 | secondary-monthly-integrity-audit | `e2f2dc02ff1c9a7a83d03215f988870b21f6bea2371929f3ff4bbced68fdd4ff` |
| 13452227760 | permutation-determinism-audit | `a28313c128ad5bf6ef73b1d1fcb87b9ddf94163d5728e03145e44a865beaa862` |
| 13451573913 | witness-run-42106629892 | `6d10ebc0dbc6165f900f669a5d6b989fce638a8d9f70e676efc0996b19e4f854` |
| 13451559582 | external-replay-verification | `115e4bc98258406d64f2aa6f3513abf364335a1a57336fe7c1a541ded8298677` |
| 13451498415 | public-report-retrieval-audit | `3847763dbdb6063f5ecc3f30d26a098151f262cccac729ba3792d73e04604edb` |
| 13451194322 | node-hash-20.20.0 | `d3e3ea2f0e5a60a49058f195c87bc069da0b7a6978bc221c8ff4d9f692299984` |

### Run 42106684822 — Scientific Claim Promotion Gate

| Artifact ID | Name | ZIP SHA-256 |
|---|---|---|
| 13452756579 | null-calibration-gate | `e02f7d226ba2ce95ebaa90eded93665799a36577a2dbf8ed897e8af46ed4d5d7` |
| 13452751719 | cosmic-rays-time-integrity-audit | `1db0bd0762458724c54e07ebc72b923036d03655a976bf98c6f28bb26939c1b5` |
| 13452427282 | estimator-sensitivity-audit | `2c4a0b54f46fb83cdcf6bf37fe9859bbc073c525e2877766e0a4e6baaca767a1` |
| 13452277676 | claim-readiness-audit | `7db97e24c3322996863093d17a1ce5df86bd012ff63bb7427d0c4cef6961a155` |
| 13451812768 | independent-domain-replication-gate | `344f6ad2e2a3551d528abf097b903adcd2706329faef601943b9bd6310ed0f5e` |
| 13451547965 | primary-null-capacity-audit | `1310b510dace79cb57242bc028dc2d36003b0068b249965a1fb52662c32a7a45` |
| 13451348259 | dataset-eligibility-gate | `87aa8a7523be2fd1a8bcad1bea10f8f748795ef5ed85ef2c404d5bca922f6198` |
| 13451313133 | permutation-determinism-audit | `c2cc3196ea834d99f0f137d4f960e0b4770b4f323c6d08890a8a6ee3e94c5b60` |
| 13451288292 | secondary-monthly-integrity-audit | `2bf07fd8c7eecdd48da6dcd9c75e6b4f8ff3ef7c9005d9e1fe12c5cfd713dba6` |
| 13451138316 | null-capacity-state-reconciliation | `eeadac5a57e24cf86c13d9e106c571af1802d7538c00c2593767e501606af67a` |

### Additional engineering/governance/snapshot runs

| Run | Artifact ID | Name | ZIP SHA-256 |
|---|---|---|---|
| 42106008752 | 13454677834 | type1-v4-official-runner-engineering | `9c6a328574542f17b2605c3ec8f7edfea0a2b400d7edd8d0325350620d29acdb` |
| 42108047580 | 13452328826 | type1-priority-guard-test-evidence | `36b11f08289e3d38bff53178f92c3f42413e0f1076084e021a4a72e80fd9e5dc` |
| 42106008761 | 13451387326 | type1-v3-v4-governance-inventory | `d786f9c7503bd1601547a030d28eaf7a0b04b7f925a3d2ba9d41d8ac6fe38a71` |
| 42106395007 | 13451792355 | type1-exact-review-snapshot | `58c152e6e7c9caa7078b0c0c46f674b7fb8b654e5826f74ea69ca68983ec69fa` |

## Key findings

### Engineering equivalence
Artifact 13454677834 records one V4 candidate scenario, six outer replicates, and 1,000 surrogates per attempt. All 19 recorded paths returned zero. Its explicit status is `ENGINEERING_EQUIVALENCE_PASS`; the artifact explicitly keeps `formal_calibration_pass`, `confirmatory_execution_authorized`, `claim_support`, and `promotion_authority` false.

### Resume guard
Artifact 13452328826 tests 23 identity fields. Every injected mismatch was rejected; checkpoint and manifest hashes were unchanged. This is a software-integrity test, not statistical calibration.

### Manual inventory is still open
Artifact 13451387326 contains:
- 1,649 review-branch occurrences: all `OPEN`, `UNKNOWN`, `PENDING`.
- 583 main-branch occurrences: all `OPEN`, `UNKNOWN`, `PENDING`.
- 3 execution-capable workflow candidate occurrences, none manually adjudicated.
- reconciliation status `RECONCILED`, which confirms count/identity coverage only.

### Primary null capacity
Artifact 13451547965 records 937/1,000 surrogate refits selecting AR order 20/20. Artifact 13452756579 records 94.7% boundary selection and `CALIBRATION_REQUIRED`. The canonical stochastic-null p-value is 0.999001 with 999 exceedances; no rejection at 0.05 under that declared procedure. High boundary saturation requires null-model calibration; it does not falsify the scientific hypothesis.

### Independent-domain eligibility
Both dataset-eligibility artifacts report 0/2 eligible independent secondary domains. HADCET and FRED are measurement-valid but their provenance/source-independence approvals remain pending. Cosmic-ray timestamps have 321 gaps and a longest hourly-contiguous run of 486, below 1,024. CO2 has 816 observations, below canonical `nperseg=1024`. The remaining listed short datasets are structurally ineligible.

### Final claim gate
Artifact 13453586453 reports `BLOCKED`, `eligible_replication_domain_count=0`, `minimum_replication_domains=2`, `scientific_claim_status=under_investigation`, `claim_support=false`, and `promotion_authority=false`.

## Evidence boundary

Do not describe any of these results as:
- a Type-I calibration pass;
- a V4 protocol freeze;
- confirmatory execution authorization;
- independent scientific replication;
- external laboratory replication;
- support or promotion of the HCM claim.

The strongest supported statement is: **limited V4 engineering-equivalence and resume-integrity tests passed for their declared bounded configurations; the statistical protocol remains unresolved and unfrozen; primary null capacity requires further calibration; independent real-domain replication remains 0/2; the claim remains under investigation.**
