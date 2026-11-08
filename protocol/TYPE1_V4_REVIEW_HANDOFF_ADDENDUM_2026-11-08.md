# HCM Type-I V4 — Exact Statistical Review Handoff Addendum

**Date:** 2026-11-08  
**Status:** `HANDOFF_BLOCKED_PENDING_EXACT_AD106_INVENTORY_AND_SNAPSHOT`  
**Candidate review commit:** `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`  
**Branch:** `review/type1-v4-remediation`

## 1. Why the current artifacts are not yet the V4 review snapshot

The V4 independent-human review request requires the inventory source commit to equal the exact commit under review. The artifacts currently available do not satisfy that condition:

| Artifact | Run / artifact | Commit actually bound |
|---|---|---|
| Governance inventory | `42499309283` / `13624359912` | `e41fb7392b58198e8a4d8fa28b470b12b6ad2c31` |
| Target review snapshot | `42499453986` / `13624771675` | `e41fb7392b58198e8a4d8fa28b470b12b6ad2c31` |
| Governance implementation snapshot | `42496227821` / `13623039718` | `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`, but only 13 curated governance files |

The first two artifacts are valid evidence for the V3 occurrence ledger target `e41fb...`; they are not the exact full V4 statistical-review snapshot for `ad106...`. The third artifact is a curated governance snapshot and does not contain the complete V4 matrix/runner review scope. Do not relabel or conflate these artifacts.

The current V3 occurrence ledger and `BATCH_001` remain correctly bound to `e41fb...`. Preserve them unchanged. A new V4 review inventory for `ad106...` is a separate population and must not overwrite or rebind `BATCH_001`. The inventory workflow-definition commit and snapshot workflow-definition commit are provenance fields; they may be the newer branch head and must not be confused with the target/review commit.

## 2. Exact workflow dispatch sequence

Run these workflows on branch `review/type1-v4-remediation`.

### A. Generate the V4 review-commit inventory

Open the GitHub Actions workflow **Type-I Target-Commit Governance Inventory**:

`https://github.com/AhmedPeaRL/maximal-one/actions/workflows/type1-v3-v4-governance-audit.yml`

Choose **Run workflow** and enter:

```text
target_commit = ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876
main_commit   = 00bbd1fbd6df41b3e988ace75c480ea6232cfb86
```

Wait for the run to finish. Record its run ID, job ID, artifact ID, artifact SHA-256, and the `reference_inventory.json` SHA-256. Confirm that `provenance.json` reports both `target_commit` and `inventory_source_commit` as `ad106...`. Record its `workflow_definition_commit` exactly; this is the workflow-definition revision used by the run (normally the review-branch head at dispatch) and it need not equal the target commit.

### B. Generate the exact V4 review snapshot

Open **Type-I Target-Commit Review Snapshot**:

`https://github.com/AhmedPeaRL/maximal-one/actions/workflows/type1-review-snapshot.yml`

Choose **Run workflow** and enter:

```text
review_commit             = ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876
inventory_source_commit   = ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876
inventory_artifact_id     = <NEW ARTIFACT ID FROM STEP A>
inventory_workflow_commit = <EXACT workflow_definition_commit RECORDED IN THE NEW INVENTORY provenance.json>
```

Do not substitute the current inventory artifact `13624359912`; it is for `e41fb...`.

Accept the snapshot only if the three-way identity certificate has:

```text
target_commit == inventory_source_commit == snapshot_review_commit
                 == ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876
```

Also require zero missing required paths, zero missing scope paths, `extraction_verification.verified == true`, and successful SHA-256 verification for every manifest entry. Download and retain the full ZIP, manifest, `SHA256SUMS.txt`, and certificate.

## 3. Exact V4 candidate inputs already identified at ad106

The following Git blob IDs identify files at the candidate commit. **These are Git blob IDs, not SHA-256 digests.** The SHA-256 values must be taken from the newly generated exact snapshot manifest and checksum register.

| File | Git blob ID |
|---|---|
| `protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json` | `48b113905fc6052ba8874374a9a9c9eeeba1d671` |
| `protocol/TYPE1_V4_INDEPENDENT_HUMAN_STATISTICAL_REVIEW_REQUEST_V1.md` | `71db1d5b83fc7fe93066158911977e79fa17aaa2` |
| `protocol/TYPE1_CALIBRATION_V4_ACCEPTANCE_RULE_DECISION_REQUEST.md` | `5c2f15b8c47cd978dfbddbb2b15ac4b5945df552` |
| `analysis/appropriate_stochastic_null.py` | `bb6a6d7c88e2713352a586ed2b32ff62291e703a` |
| `analysis/numerical_spectral_verification.py` | `abe3816f24b4d58565174ff5d74b71c07af8d11c` |
| `analysis/calibrate_null_type1_scenario.py` | `4f89fe200886d6b10db9c6d3dc4eecaae5965ef3` |
| `analysis/calibrate_null_type1.py` | `ff17c125c545c722bfbab3649a813400ff3395ac` |
| `analysis/type1_calibration_pilot.py` | `71585095128c650e5fa73f2aba3482830e1ab766` |
| `analysis/merge_type1_calibration_pilot_shards.py` | `09c6d2197017ec2f9d1fd0f3b60f8cc9d2fd854d` |
| `requirements-lock.txt` | `3fc46eb5c65c02c80a8b37444aee21590f057735` |
| `.github/workflows/null-type1-calibration.yml` | `4fec09473d8e4e5b6be3186287c60edf00a68a9a` |
| `.github/workflows/type1-calibration-runtime-pilot.yml` | `5e18ec4db402e6d7719e17ecf321ba4861ec0274` |

The reviewer must inspect the full snapshot and actual source files, not only this list.

## 4. Statistical issues that remain open

The V4 matrix at `ad106...` remains a candidate draft:

- Nine proposed stationary Gaussian AR scenarios.
- 2,000 outer repetitions per scenario and 1,000 surrogates per outer attempt are candidates, not an approved design.
- Sample size 3,328; DGP burn-in 2,000.
- Candidate master seed 20261021 is not final.
- `acceptance_rule` is `null`.
- The historical 0.075 ceiling is explicitly not justified or approved for V4.
- Historical V1 two-sided 95% Wilson classifications must remain unchanged; do not select a new rule to turn a historical failure into a pass.

The primary-null capacity review reports selected AR order 20 at the declared maximum and a surrogate boundary fraction of 0.937. This is a model-capacity diagnostic requiring methodological review; it is neither a Type-I calibration pass nor evidence for or against HCM.

The V3 `null-type1-calibration.yml` workflow currently fails closed because its V3 matrix is not in an approved frozen state and the workflow explicitly blocks unreconciled execution. The V4 runtime-pilot workflow is exploratory-only. Neither workflow authorizes a formal V4 calibration.

## 5. Required independent reviewer disposition

The reviewer must be an attributable human with relevant statistical-methods expertise and must disclose:

- Full name and professional affiliation.
- Relevant expertise in Monte Carlo testing, time series, spectral methods, surrogate testing, and Type-I calibration.
- Prior involvement in the repository/project.
- Financial, professional, collaborative, supervisory, or personal conflicts; explicitly state `NONE` where applicable.
- Exact reviewed commit SHA `ad106...` and SHA-256 digests from the exact snapshot.
- Files, logs, tests, and artifact payloads actually inspected.
- A reasoned disposition on the estimand, nine DGPs, stationarity/root convention, implementation equivalence, invalid-attempt policy, acceptance rule, multiplicity, Monte Carlo precision, and computational feasibility.
- One disposition from the review request's permitted list, with explicit conditions and unresolved issues.

An AI-generated assessment, this addendum, CI success, or an automated report is not an attributable independent human statistical review.

## 6. Stop conditions

Until the exact ad106 inventory/snapshot is verified and an attributable independent human reviewer has issued a reasoned disposition:

```text
protocol_freeze = NOT_FROZEN
formal_calibration_authorized = false
confirmatory_execution_authorized = false
claim_support = false
promotion_authority = false
```

Do not run formal Type-I calibration, power analysis, or claim-promotion workflows. Do not change the historical acceptance rule or results. Do not merge the entire review branch into `main`; the branch comparison at this checkpoint is `diverged`, 330 commits ahead and 19 behind.
