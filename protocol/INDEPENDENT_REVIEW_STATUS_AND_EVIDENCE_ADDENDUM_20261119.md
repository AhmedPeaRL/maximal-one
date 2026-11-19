# Independent Review Status and Evidence Addendum — 2026-11-19

**Status:** `REVIEW_ONLY — EXISTING SNAPSHOT PRESERVED — NO NEW SNAPSHOT`

**Repository:** `AhmedPeaRL/maximal-one`

**Current main commit:** `9749de9253f144eeda9e1b60cb219cfc5f201ecc`

**Current review branch commit:** `1792d735c96622202c3c115701e53bbe49bc99e1`

**Pinned scientific and software-review target:** `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`

This addendum updates the evidence identity and review scope. It does not replace historical records, modify the pinned target, or authorize a new snapshot.

## 1. Exact V9 inventory and snapshot identity

### Inventory

- Workflow run: `43757949244`
- Artifact: `14178549418`
- Artifact SHA-256: `dcb0dd3283689e171c938bce02409b937c431b96ef5a86f44ca9e47fc2413eb4`
- Inventory SHA-256: `4ee4335d5807c0a90ac668637a2bd55277ae9b6ce442af316f65f22a24f17a89`
- Target ledger SHA-256: `ad18beccc8e5e9e9934838afe0e176b9e25658bea24e93c5dd3d2ec9ef119c67`
- Main ledger SHA-256: `e2a9aa2b2da293c2c68f0a518ca1d76c5ffc85c8f7304ed17d3e312e1beec650`

### Exact target snapshot

- Workflow run: `43762349962`
- Artifact: `14180143511`
- Artifact archive SHA-256: `caa75810be3463ddf09c6d379bd6685337bbee6be62284bf8fc877768b43364e`
- Manifest SHA-256: `2ff2e9b8c9aa2aea520ca1612e76a92703af9d479d6742e6ea211627862d9426`
- Inner snapshot ZIP SHA-256: `6a399450a2e69d3e069363a957200203c84025754cb5b333dc90786e64494842`
- Three-way identity certificate SHA-256: `33ed699ddb23ec454c66951fd08704c4248f6709699f805b0ffe689481b32567`
- Extraction verification SHA-256: `2e1f6c1134dd01d1cb39ce184865212f621bab3bf250aee0d6376f71971a31ef`
- Selected/present files: `289/289`
- Extraction checks: `292`
- Missing required paths: `0`
- Missing scope paths: `0`
- Manual adjudication overlay records: `0`

These are identity and packaging results only. They do not establish execution safety, scientific validity, or human approval.

## 2. Post-V9 workflow evidence

The following workflows were already executed on `review/type1-v4-remediation`.

### Navigation-only target batches

- Run: `44182819734`
- Artifact: `14371289914`
- Artifact SHA-256: `c63e19804f877a52f14230964ed4acddabf91dfdfee6d731d3470e371c4c93ab`
- Output: 72 batches, 25 occurrences per batch, 1,800 unique occurrence IDs.
- Status: `NAVIGATION_ONLY_NOT_ADJUDICATED`
- Authority: `NONE`

### Read-only human-overlay preflight

- Run: `44182878546`
- Artifact: `14373670597`
- Verified artifact SHA-256: `8dc10de19d292803e3582b1660cc7f5eb675bc33ed0bf3b782e1decab98be67d`
- CSV: `adjudication/incoming/first-three-occurrences-v6.csv`
- CSV SHA-256: `60ddb17002a5e6ccdd82b2680fdb4efcc3ce94724e1c7d48a5fa9e6040fb1c05`
- Rows: `3`
- All rows open and pending: `true`
- Adjudications applied: `0`
- Status: `CURRENT_SOURCE_PAIR_VERIFIED_PENDING_INDEPENDENT_HUMAN_ADJUDICATION`
- Authority: `NONE`

### Exact-target Software Assurance V3

- Run: `44182949661`
- Artifact: `14372144011`
- Verified artifact SHA-256: `f88d5f18b91b0c6b97aa63aef8dc3f9cc4c7f3b1de83abce4f07addea72b182c`
- Scan commit: `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`
- Inventory run: `43757949244`
- Snapshot run: `43762349962`

Recorded scanner results:

- actionlint exit code: `123`; 97 diagnostic headers, comprising 92 ShellCheck diagnostics and 5 other actionlint diagnostics.
- zizmor exit code: `14`; 205 findings: 164 High, 37 Medium, 4 Informational.
- Scorecard exit code: `0`; score `5.7/10`; 73 reported vulnerabilities.

These findings remain open for occurrence-specific triage and independent human review. The workflow's successful artifact production does not mean the scan was clean.

## 3. Later engineering assurance on review-branch HEAD

### Exact-commit software assurance

- Run: `44408732399`
- Review branch commit: `1792d735c96622202c3c115701e53bbe49bc99e1`
- Main scan job: `135170861637`
- OSV job: `135170862529`
- Exact assurance artifact: `14475467384`
- Exact assurance artifact SHA-256: `bf5b299477b13f39929cc04a97e5c46ba5f812536fd7bd987380c2db05a080e5`
- OSV artifact: `14475298142`
- OSV artifact SHA-256: `d6e16a021dafc992faaa368834c56fc6967dbc604154a8ec13db916b8a327aaf`

Results on review-branch commit `1792...`:

- actionlint exit code: `0`; empty output.
- zizmor exit code: `0`; JSON findings array empty.
- Scorecard: `8.6/10`.
- OSV Scanner 2.7.1 exit code: `0`; valid JSON with `results: []` across the six supported manifests/lockfiles.

Scorecard still reports improvement areas, including Fuzzing, Security Policy, Pinned Dependencies, and Token Permissions.

**Scope limitation:** this scan concerns the review-branch HEAD `1792...`. It does not replace the separate exact-target scan of `ad106...`, and it does not automatically close any finding from that target scan. Automated results are not an independent human security review.

### Priority guard and negative-gate tests

- Run: `44418604254`
- Job: `135205340384`
- Artifact: `14481106755`
- Artifact SHA-256: `e1459d4dcaf5bdaf2c42a0bd062d251513919028702e664e1b395f5b9a8e35de`

Results:

- 25 tests passed.
- 23 injected identity mismatches were rejected.
- Original checkpoint and manifest hashes remained unchanged after rejected resume attempts.
- `formal_calibration_pass=false`
- `confirmatory_execution_authorized=false`
- `claim_support=false`
- `promotion_authority=false`

This is bounded engineering integrity evidence only.

## 4. Corrections to existing independent-review handoffs

### A. Statistical-methods review

Some existing statistical-review request files refer to an older inventory/snapshot lineage. Use the V9 identities in Section 1 for the current source and snapshot context.

The current review-branch protocol inputs include:

- `protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_DRAFT.json`  
  SHA-256: `b6c6354558ca6a0685f5731da11da656268c1c3e44599f84f5540ad9725f11af`

- `protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json`  
  SHA-256: `f8b8dfaf97282ca24378b8929939d8fffd1fe72064a2fe662198422a11b1bc2f`

- `analysis/calibrate_null_type1_scenario.py`  
  SHA-256: `d367d3ba0ed3910196cd639b1f2284b84ab7b066fad08806791a1a6406fa9472`

- `analysis/calibrate_null_type1.py`  
  SHA-256: `faf96a9e969f1060d51142503521e2857ff0b4c11cfa53fbe4fab6f0c318b86a`

- `protocol/PROSPECTIVE_TYPE1_ACCEPTANCE_RULE_DECISION_V1.md`  
  SHA-256: `3da64533381da10af667771c9bfe72399495ba24472d4e808f4e9c11051d2644`

The V4 candidate matrix remains `DRAFT_PENDING_REMEDIATION_AND_INDEPENDENT_REVIEW` with prior disposition `REVISE_AND_RESUBMIT`.

The prospective rule family remains pending independent statistical review. `alpha_max` remains `NOT_SET`. The historical two-sided Wilson rule and all historical outcomes must remain unchanged. The historical `0.075` ceiling is not approved for V4.

The reviewer must provide an attributable decision on the estimand, confidence-bound method, numerical tolerance, scenario coverage, multiplicity, Monte Carlo precision, invalid-attempt policy, and whether the protocol is ready to freeze.

No formal calibration is requested or authorized.

### B. Software-assurance review

The existing `review/TYPE1_SOFTWARE_ASSURANCE_INDEPENDENT_REVIEW_REQUEST_V1.md` points to an older snapshot and inventory pair. Do not treat those old IDs as the current V9 source lineage.

Use:

- Target commit: `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`
- Inventory run/artifact: `43757949244` / `14178549418`
- Snapshot run/artifact: `43762349962` / `14180143511`
- Exact-target assurance V3 run/artifact: `44182949661` / `14372144011`

The reviewer should examine the exact 289-file target snapshot, relevant workflow and script call paths, effective token permissions, secrets/OIDC boundaries, artifact trust, guard ordering, and occurrence-specific evidence.

The later scan of review-branch HEAD `1792...` may be considered remediation-context evidence only. It does not substitute for review of the pinned target or independently adjudicate its findings.

### C. Climate-domain review

The older domain-independence request requires an update to reflect the current scientific status.

- HadUKP EWP is a candidate only. Structural checks were reported as passing for 1,356 monthly observations from 1913-01 through 2025-12. Source vintage, historical endpoint exposure, shared nuisance, and independence remain unresolved.
- HadCET historical endpoint-like output remains exploratory/post-observation and is not an approved confirmatory replication.

A raw-source identity discrepancy remains open: the 2026-11-17 status addendum lists HadUKP raw SHA-256 `75a10dcc597c4b0a452cdd8d22dcad6a0ef677bbe8f1a7d6065806123752882d`, while the available raw-audit artifact from run `39066915519`, artifact `12113581637`, has raw SHA-256 `eb2a20081a4673211783b0fe442007921d0f23a4683065954373c6ce0fa96637`. Both records list parsed SHA-256 `3c757cd2f7258944ba393906ea3fd7294b48a09782319381f91d9117652b87df`.

The artifact matching the newer raw hash has not been identified in the available repository evidence. Preserve this discrepancy as unresolved; do not choose a raw source version by inference.

No HadUKP endpoint computation is authorized.

### D. Econometric-domain review

- CPIAUCNS has 1,356 monthly rows in the 1913-01 through 2025-12 audit window, with one missing observation at `2025-10-01` and 1,355 valid numeric observations.
- Do not impute, interpolate, carry forward, or silently remove the missing observation.
- A separate pre-gap window ending `2025-09-01` contains 1,353 observations and may be assessed as a separate prospective candidate. It is not approved by this addendum.
- INDPRO historical endpoint-like output remains exploratory/post-observation and is not an approved confirmatory replication.

No CPIAUCNS or INDPRO endpoint computation is authorized by this addendum.

## 5. Current scientific and governance status

- `protocol_freeze = NOT_FROZEN`
- `formal_calibration_authorized = false`
- `confirmatory_execution_authorized = false`
- `claim_support = false`
- `promotion_authority = false`
- `approved_independent_secondary_domains = 0`
- `replication_status = 0/2`
- Manual adjudication overlay records: `0`

The four requested independent human reviews remain pending:

1. Statistical methods and null-model adequacy.
2. Climate-domain independence and HadUKP/HadCET suitability.
3. Econometric-domain independence and CPIAUCNS/INDPRO suitability.
4. GitHub Actions and CI security.

Each reviewer must provide identity, relevant expertise, conflicts of interest, exact reviewed commit and file/artifact hashes, reviewed and excluded scope, limitations, and an attributable written disposition.

An email acknowledgement, out-of-office reply, automated scanner, or AI-generated assessment is not an independent human review.

## 6. Non-authorization and preservation

This addendum:

- does not modify `main`;
- does not modify Population Register V9;
- does not modify the pinned target commit;
- does not create or authorize a new snapshot;
- does not adjudicate any occurrence;
- does not close any software finding;
- does not approve a statistical acceptance rule;
- does not authorize formal calibration, confirmatory execution, claim support, or promotion.

All historical outcomes, failed gates, unresolved classifications, source discrepancies, and prior review records must remain preserved.

**Final status:** `REVIEW_ONLY — HUMAN_REVIEWS_PENDING — SCIENTIFIC_GATES_OPEN — NO_NEW_SNAPSHOT`
