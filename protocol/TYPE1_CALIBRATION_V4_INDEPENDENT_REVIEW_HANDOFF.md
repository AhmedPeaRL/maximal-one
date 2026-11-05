# Type-I Calibration V4 — Independent Statistical Review Handoff

## 1. Purpose and current decision

This handoff requests an attributable, independent human statistical-methods review of the proposed V4 Type-I calibration protocol before any confirmatory execution.

This is a review request only. It is not protocol approval, a freeze decision, a calibration result, real-domain replication, claim support, or promotion authority.

At the reviewed snapshot:
- V4 status: `DRAFT_PENDING_REMEDIATION_AND_INDEPENDENT_REVIEW`
- Freeze state: `NOT_FROZEN`
- Confirmatory execution: `NOT_AUTHORIZED`
- Formal calibration: `NOT_STARTED`
- Claim support: `false`
- Promotion authority: `false`

These states must remain unchanged until the independent review, prospective protocol resolution, freeze decision, and separate execution authorization have each been completed.

## 2. Exact immutable review target

- Repository: https://github.com/AhmedPeaRL/maximal-one
- Review branch: `review/type1-v4-remediation`
- Exact review commit: `5b814ddf529b04b3ea9fda908373c3676eb647c1`
- Main branch at snapshot time: `fe0daded51229ed88d449c2eb68252455fd4ad7c`
- V4 candidate matrix: `protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json`
- V4 design draft: `protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_DRAFT.json`

The review branch pointed to the exact review commit when this handoff was prepared. Any later commit changes the review identity and requires a new snapshot and digest register.

### SHA-256 digests at the reviewed snapshot

| File | SHA-256 |
|---|---|
| `protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json` | `f8b8dfaf97282ca24378b8929939d8fffd1fe72064a2fe662198422a11b1bc2f` |
| `protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_DRAFT.json` | `b6c6354558ca6a0685f5731da11da656268c1c3e44599f84f5540ad9725f11af` |
| `protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V3.json` | `ea811a949f1b12bf87a96e47ac8c04bec5e99637af728d458a975c0213a4d7df` |
| `.github/workflows/null-type1-calibration.yml` | `e239fe886475a0c716def6a06da5c1bff45a1f1b3fac50e272567a116c79aa72` |
| `.github/workflows/type1-v4-cross-runner-worker-order.yml` | `2b185f17e9a93c6de1e36dfee35b5e313758c2c8e54cc20bcf0126d1227ef4f6` |
| `.github/workflows/type1-calibration-runtime-pilot.yml` | `43e83a217f2a0aa8faf615cb8f89b7484e98c2300d729a9225c9f9578027f76b` |
| `analysis/calibrate_null_type1.py` | `faf96a9e969f1060d51142503521e2857ff0b4c11cfa53fbe4fab6f0c318b86a` |
| `analysis/calibrate_null_type1_scenario.py` | `a8e5e7d1730eb7cc1650a9c4934f472f37b85829f4b713e9d048ee30f054705f` |
| `analysis/type1_calibration_pilot.py` | `0a578be55c68bcf90a9c56c112f1d5a6aa0bb175a72b6ba48b1a1ffb17bb1228` |
| `scripts/type1_runtime_pilot_branch_guard.py` | `69e8c6f68b8da21880dc7bed5c3089417fa6611ff72d09315a447394a7956fc1` |
| `tests/test_type1_runtime_pilot_branch_guard.py` | `11dc8e14085c6dfe649434330e9b34a0914a99a1d28b54c3fdd3817f1b38148d` |
| `analysis/null_calibration_gate.py` | `48a2ac28c1d030fa6022372036f8a6318507ee204035bc836bd45b333b2d1ee8` |
| `core-scientific/strict_claim.json` | `a2b5f0a53152d986fcb3d53dc73861aee350512bca3eaa16e7ad9ebd5912bc0c` |
| `protocol/TYPE1_CALIBRATION_FREEZE_DECISION.json` | `836151280228e1490d188f0daee9f1952f8942cfd07273eb212f6837e53a6b95` |
| `protocol/TYPE1_CALIBRATION_EXECUTION_AUTHORIZATION.json` | `2ec8486284f96199771d0f14607bfe7253217fa24a8d245f3e0f293b984707c3` |
| `requirements-lock.txt` | `e723a80e054797d4d555df117f5bcbcaa4a5e17435eec159a006892383038ec8` |

## 3. Exact review snapshot and inventory

The exact-review-snapshot workflow produced:
- Workflow run: https://github.com/AhmedPeaRL/maximal-one/actions/runs/42106395007
- Job: https://github.com/AhmedPeaRL/maximal-one/actions/runs/42106395007/job/127522248383
- Artifact: https://github.com/AhmedPeaRL/maximal-one/actions/runs/42106395007/artifacts/13451792355
- Artifact ZIP SHA-256: `58c152e6e7c9caa7078b0c0c46f674b7fb8b654e5826f74ea69ca68983ec69fa`
- Nested self-contained snapshot ZIP SHA-256: `715f65cdeb51ba646e83c59682ae3897168dd0d044ccf411d05b55965461908d`
- Inventory JSON SHA-256: `cf3d05b060edbc1a813b5cfc3b96ef1ee52ccb4fc40dab60629e228a8aba0c74`
- Selected files: 262
- Inventory paths: 254
- Required anchors: 40
- Missing required paths: 0
- Missing scope paths: 0

All 262 file hashes in the snapshot manifest were checked against the contents of the nested snapshot ZIP; all 262 matched. The nested ZIP passed integrity testing.

The snapshot's `manual_adjudication_overlay.json` contains zero records. The snapshot is complete for its declared selection scope, but it is not a completed human review.

## 4. Engineering evidence — bounded scope only

### E1 — Official runner / 1000-surrogate engineering equivalence

- Workflow run: https://github.com/AhmedPeaRL/maximal-one/actions/runs/42106008752
- Job: https://github.com/AhmedPeaRL/maximal-one/actions/runs/42106008752/job/127520893897
- Artifact: https://github.com/AhmedPeaRL/maximal-one/actions/runs/42106008752/artifacts/13454677834
- Artifact ZIP SHA-256: `9c6a328574542f17b2605c3ec8f7edfea0a2b400d7edd8d0325350620d29acdb`

Recorded result:
- `ENGINEERING_EQUIVALENCE_PASS`
- One declared scenario: `gaussian_ar2_phi_0_45_minus_0_10_n3328`
- Six outer replicate indices
- 1,000 requested surrogates per attempt
- Connected, sharded, alternative partition, reverse merge, worker-order, and interrupted/resumed paths were exercised.
- All 19 recorded execution paths returned code 0.
- `invalid_attempts_observed = 0`
- `formal_calibration_pass = false`
- `confirmatory_execution_authorized = false`
- `claim_support = false`
- `promotion_authority = false`

Interpretation: this is bounded path/engineering equivalence for one scenario and six replicates. It is not a nine-scenario Type-I calibration, does not establish the acceptance rule, and does not establish full production equivalence for the entire V4 design.

### E2 — CLI resume identity rejection

- Workflow run: https://github.com/AhmedPeaRL/maximal-one/actions/runs/42108047580
- Job: https://github.com/AhmedPeaRL/maximal-one/actions/runs/42108047580/job/127528006935
- Artifact: https://github.com/AhmedPeaRL/maximal-one/actions/runs/42108047580/artifacts/13452328826
- Artifact ZIP SHA-256: `36b11f08289e3d38bff53178f92c3f42413e0f1076084e021a4a72e80fd9e5dc`

Recorded result:
- `PASS`
- 23 identity fields tested.
- Every injected mismatch was rejected with exit code 1 and the expected diagnostic.
- Original checkpoint and manifest hashes remained byte-identical before and after every rejected resume.
- Formal calibration, claim support, and promotion authority remained false.

Interpretation: this validates the tested CLI resume-identity rejection path and declared fields only. It is not a statistical calibration result or a proof of every possible storage/runtime configuration.

### E3 — V3/V4 governance inventory

- Workflow run: https://github.com/AhmedPeaRL/maximal-one/actions/runs/42106008761
- Job: https://github.com/AhmedPeaRL/maximal-one/actions/runs/42106008761/job/127520893529
- Artifact: https://github.com/AhmedPeaRL/maximal-one/actions/runs/42106008761/artifacts/13451387326
- Artifact ZIP SHA-256: `d786f9c7503bd1601547a030d28eaf7a0b04b7f925a3d2ba9d41d8ac6fe38a71`

The review-branch ledger contains 1,649 occurrences. All 1,649 remain:
- `status = OPEN`
- `manual_classification = UNKNOWN`
- `reviewer_disposition = PENDING`
- `can_influence_execution = UNKNOWN`
- `guard_fails_closed = UNKNOWN`

The main-branch ledger contains 583 occurrences; all 583 remain open/unknown/pending.

Both reconciliation records report `RECONCILED`, but reconciliation establishes identity/count coverage only. It does not establish manual classification, call-path closure, authorization ordering, or scientific validity.

Three occurrences were automatically flagged as execution-capable workflow candidates. Their manual classifications remain `UNKNOWN`; see the separate manual-governance review plan.

### E4 — Final review snapshot

See Section 3 and the snapshot artifact. The inventory and snapshot are identity-complete for the declared scope; manual adjudication is still empty.

## 5. Scientific and replication blockers

### 5.1 Primary stochastic-null capacity warning

The supplied evidence contains two related boundary-saturation diagnostics:

- `primary_null_capacity_audit.json` (artifact 13451547965): selected AR order 20 of 20; 937/1,000 surrogate refits selected the boundary (93.7%); seed 90210; no alpha-estimation or refit failures.
- `null_calibration_gate.json` (artifact 13452756579): selected AR order 20 of 20; boundary fraction 0.947 (94.7%); `fresh_calibration_required = true`; status `CALIBRATION_REQUIRED`.

The canonical primary stochastic-null report records:
- observed primary alpha: approximately 2.525347
- 999 exceedances among 1,000 valid surrogates
- Monte Carlo add-one p-value: 0.999001
- no rejection at 0.05 under the declared fitted stationary Gaussian AR(p) procedure
- boundary selection and high boundary saturation diagnostics

The gate explicitly states that boundary saturation requires calibration and is not evidence against the scientific hypothesis. The primary null's adequacy is unresolved. Do not interpret this p-value as a validated positive result; do not treat the boundary warning as falsification.

The audit also records `post_observation_amendment = true`. This must remain visible and be explained prospectively; it must not be backdated or silently removed.

### 5.2 Independent real-domain replication

The final gates report:
- eligible independent secondary domains: `0`
- minimum required: `2`
- status: `REPLICATION_ELIGIBILITY_INSUFFICIENT`

Specific evidence:
- `hadcet_monthly` (4,404 observations) and `fred_indpro` (1,284) are structurally measurement-valid, but not approved for replication. Source independence and shared-nuisance assessment remain pending.
- `cosmic_rays` has 3,698 observations and increasing unique timestamps, but is not continuously hourly: 321 non-hourly intervals/gaps; longest hourly-contiguous run 486; no contiguous run of 1,024. It is not replication-eligible.
- `co2` has 816 observations, below canonical `nperseg = 1024`; it cannot establish replication eligibility under the current rule.
- `passengers`, `temperature`, and `sp500` are below the declared measurement minimum.
- `extended` is derived/related and excluded from independent-domain counting.
- The primary sunspot domain is not counted as a secondary replication domain and has a missing provenance-registry entry.

The independent-domain gate skipped computations because the protocol is not frozen, explicit approval is missing, and provenance is not approved. A dataset name or distinct file is not proof of independent scientific replication.

### 5.3 Computational replay is not independent scientific replication

The external replay artifact reports clean-checkout computational reproducibility for the same repository snapshot, but:
- same workflow runner
- no independent execution environment
- no independent implementation
- no external laboratory replication
- no independent scientific replication

This must be described as computational reproducibility only.

## 6. Current workflow outcomes

All six supplied workflow runs used the exact review commit `5b814ddf529b04b3ea9fda908373c3676eb647c1` on `review/type1-v4-remediation`.

1. `42106008752` — Type-I V4 Official Runner Engineering Equivalence: workflow success; bounded engineering equivalence pass.
2. `42108047580` — Type-I Priority Occurrence Guard and Negative-Gate Tests: success; 23 resume-identity rejection fields.
3. `42106008761` — Type-I V3/V4 Governance Inventory Audit: success; inventory/ledger generated, but manual review remains open.
4. `42106395007` — Type-I Exact Review Snapshot and SHA-256: success; exact 262-file snapshot generated and hashes verified.
5. `42106629892` — SOS Robustness Gate: workflow failure at final claim gate because eligible independent replication domains were 0/2. Final decision artifact says `BLOCKED`, claim remains `under_investigation`, claim support false, promotion authority false, scientific inputs not modified.
6. `42106684822` — Scientific Claim Promotion Gate: failure at the dataset-eligibility contract because eligible independent replication domains were 0/2. This is an eligibility failure, not a Type-I calibration result.

No supplied run is a formal V4 Type-I calibration.

## 7. V3/V4 separation and the proposed manual run

The V3 workflow `.github/workflows/null-type1-calibration.yml`:
- consumes `TYPE1_CALIBRATION_SCENARIO_MATRIX_V3.json`;
- requires V3 `APPROVED_FROZEN`, `FROZEN`, authorized execution, and verified archived Git identity;
- then contains an explicit fail-closed step stating that the V3 runner is not reconciled and exiting with code 1 before simulation.

At the reviewed snapshot, the V3 matrix is still a candidate and is not frozen or authorized. Therefore, a manual `workflow_dispatch` cannot legitimately activate V4. It will be blocked at the V3 preparation guard; even if that guard were changed, the execution job itself is explicitly fail-closed. Do not remove either guard to obtain a green run.

V4 uses a different schema and a separate candidate runner. Do not add V3 fields to V4, do not route V4 through the V3 matrix, and do not copy a historical 0.075 ceiling into V4.

The V4 cross-runner workflow uses `--engineering-test` and is limited to six replicates in one scenario. The V4 runtime-pilot workflow is explicitly exploratory, branch-restricted, and runs only two replicates with 200 surrogates for one scenario. Neither is formal calibration.

## 8. Post-observation eligibility amendment — separate governance issue

`core-scientific/strict_claim.json` records an explicit post-observation eligibility amendment:
- `preregistered_confirmation = false`
- the 512-sample estimator minimum is made explicit because the canonical frequency-bin requirement implies that minimum;
- claim promotion is blocked until fresh validation.

The reviewer must assess this amendment as a separate governance/measurement-validity issue. Preserve its post-observation status and require fresh validation. Do not present it as preregistered or backdate it.

## 9. Required independent reviewer decisions

The reviewer must inspect the exact snapshot, source, tests, workflow YAML, logs, artifact payloads, and relevant call paths, and must provide an attributable written report.

The reviewer must explicitly decide:
1. the Type-I estimand and operational rejection definition;
2. the appropriate confidence-bound/test procedure and confidence level;
3. the numerical acceptance boundary, with rationale;
4. scenario-level versus suite-level acceptance and multiplicity handling;
5. whether all nine scenarios are appropriate and sufficient;
6. whether the two in-band resonant AR(2) scenarios are valid and correctly parameterized;
7. whether the endpoint and null implementation match the scientific estimand and production implementation;
8. whether 2,000 outer repetitions and 1,000 surrogates are adequate;
9. invalid-attempt, failed-fit, shortfall, denominator, restart, and resume policies;
10. the high AR-order boundary-saturation finding and the required null-family calibration/remediation;
11. the post-observation 512-sample eligibility amendment;
12. the manual execution-path inventory and the three flagged workflow candidates;
13. the limitations on what synthetic calibration can support;
14. the separate evidence required for independent real-domain replication.

Required attribution:
- full name and affiliation;
- relevant statistical-methods expertise;
- conflict-of-interest declaration;
- review date in UTC;
- exact commit SHA;
- exact reviewed file SHA-256 values;
- actual files, logs, and artifacts inspected;
- explicit disposition: `APPROVE_WITH_EXPLICIT_RATIONALE`, `REVISE_AND_RESUBMIT`, `REJECT`, or `INSUFFICIENT_INFORMATION`;
- whether the exact reviewed protocol is ready for prospective freeze.

An AI-generated assessment is not an attributable independent human review.

## 10. Historical result protection

The historical V1 rule remains the two-sided 95% Wilson interval rule: the interval must contain 0.05 and its upper endpoint must not exceed 0.075. Historical decisions remain unchanged.

The exact AR5 interval is `[0.0372610346, 0.0641907015]`; it passed its historical per-scenario rule. The overall historical V1 suite remains `NOT_PASSED` because AR2 and AR10 failed.

The later V3 one-sided candidate rule and the V4 unresolved rule are not interchangeable with the historical rule. No threshold may be changed retrospectively to convert a historical failure into a pass.

## 11. Required sequence after review

1. Obtain the attributable independent human statistical review of the exact snapshot.
2. Resolve every material statistical objection prospectively; version any changes.
3. Complete manual adjudication of execution-capable workflow paths and the required governance-control paths.
4. Reconcile the V4 matrix, runner, dependency lock, workflow, and source hashes.
5. Update the freeze-decision file only after the reviewer has issued a reasoned disposition and the exact reviewed snapshot is fixed.
6. Obtain a separate explicit execution-authorization decision bound to the frozen commit and exact hashes.
7. Only then run the separately authorized V4 formal calibration workflow.
8. Review all attempts, failures, denominators, hashes, and scenario decisions before reporting a calibration outcome.
9. Independently establish at least two eligible secondary real domains under a frozen protocol and the same endpoint/null procedure.
10. Keep claim support and promotion authority false until their separate gates are met.

No step in this handoff grants execution authorization.

## 12. Current disposition

`ENGINEERING_EQUIVALENCE_LIMITED_PASS; GOVERNANCE_INVENTORY_RECONCILED_BUT_MANUAL_REVIEW_OPEN; PRIMARY_NULL_CAPACITY_REVIEW_REQUIRED; V4_ACCEPTANCE_RULE_UNRESOLVED; V4_NOT_FROZEN; CONFIRMATORY_EXECUTION_NOT_AUTHORIZED; INDEPENDENT_REPLICATION_0_OF_2; CLAIM_UNDER_INVESTIGATION; NO_CLAIM_SUPPORT; NO_PROMOTION_AUTHORITY`
