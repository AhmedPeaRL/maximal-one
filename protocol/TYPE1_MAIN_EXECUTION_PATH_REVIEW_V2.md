# Type-I Main-Branch Review Status V2

- Status: OPEN — NEGATIVE EXECUTION TEST PENDING  
- Authority: GOVERNANCE AND REVIEW EVIDENCE ONLY  
- Scientific approval: NONE  
- Protocol freeze: NOT FROZEN  
- Confirmatory execution: NOT AUTHORIZED  
- Claim support: FALSE  
- Promotion authority: FALSE

## 1. Exact source identities

- Repository: AhmedPeaRL/maximal-one
- Current main branch commit:
`ab4170645d6e902a065a3235d0c31136bcbee77c`
- Review branch:
`review/type1-v4-remediation`
- Review branch commit:
`5f32741701a26436e326e915b619394500378f0c`

The two branches are divergent and must be reviewed independently.

## 2. Governance inventory evidence
- Inventory workflow run:
`41302926740`
- Inventory artifact:
`13081704496`
- Inventory ZIP SHA-256:
`254acb2f0c2c5e901f215635d006a26ad430a0b47037844d6f718cda85c78e4a`
- Main-branch occurrence count: 208  
- Review-branch occurrence count: 2249
- Main reconciliation:
`RECONCILED`
- Review-branch reconciliation:
`RECONCILED`

Reconciliation verifies occurrence identity and coverage only.
It does not establish human classification, execution-path safety, statistical validity, or scientific approval.

## 3. Exact review snapshot evidence

- Snapshot workflow run:
`41303166843`
- Snapshot artifact:
`13081899278`
- Snapshot ZIP SHA-256:
`b6c1bcd9ef3c9d9f13f0bb9700507dbbc1d9773eba51503a67c9edcd506e767b`
- Review commit:
`5f32741701a26436e326e915b619394500378f0c`

Snapshot scope:
- Inventory paths: 133
- Mandatory anchors: 40
- Selected unique paths: 140
- Present files: 140
- Missing required paths: 0
- Missing scope paths: 0
- Excluded paths: 0
- Occurrence records: 2249

The artifact contains a manifest and SHA-256 checksum list. It is an identity-and-integrity record, not a bundled copy of all source files. The immutable Git commit remains the source reference.

## 4. Branch separation

The review branch and main branch contain materially different Type-I execution paths.

The current main branch uses the V3 matrix path in:
- `.github/workflows/null-type1-calibration.yml`
- `analysis/calibrate_null_type1.py`
- `analysis/calibrate_null_type1_scenario.py`

The review branch introduces V4 candidate execution-path changes and an explicit fail-closed workflow step.

Evidence from the review branch must not be treated as proof that the same guard is present on main.

No full-branch merge is authorized by this review record.

## 5. Current V3 protocol state

The current main-branch V3 matrix declares:
- status: `CANDIDATE_PENDING_ATTRIBUTABLE_INDEPENDENT_STATISTICAL_REVIEW`
- freeze_state: `NOT_FROZEN`
- archive_git_identity_verified: false
- confirmatory_execution_authorized: false
- claim_support: false
- promotion_authority: false

The V3 candidate acceptance rule is recorded as a one-sided 95% Wilson upper confidence bound no greater than 0.075 for every required scenario. The two-sided interval is report-only in this candidate matrix.

This rule remains a candidate specification and requires attributable independent statistical review before any freeze or confirmatory authorization.

## 6. Mandatory next test

Run the exact main-branch workflow:

`.github/workflows/null-type1-calibration.yml`

Expected source commit:
`ab4170645d6e902a065a3235d0c31136bcbee77c`

Expected negative-test outcome:
- The preparation step rejects the current unfrozen V3 matrix.
- No calibration scenario job begins.
- No formal calibration result is produced.
- No confirmatory execution is authorized.

Required evidence:
- Exact workflow run ID.
- Exact commit SHA.
- Preparation job conclusion.
- Rejection message and exit status.
- Confirmation that no scenario calibration jobs ran.
- Confirmation that no scenario calibration artifacts were produced.

If the workflow proceeds beyond the preparation gate, stop further work and open an execution-path defect review.

## 7. Review closure conditions

Do not close the main-branch execution review because:
- a governance inventory reconciles;
- a snapshot manifest is complete;
- a review-branch workflow succeeds;
- a source-code test finds a guard string;
- a documentation statement says execution is blocked.

Closure requires the exact main-branch negative test and inspection of its job-level evidence.

## 8. Current disposition

MAIN_INVENTORY_RECONCILED  
REVIEW_BRANCH_INVENTORY_RECONCILED  
REVIEW_SNAPSHOT_MANIFEST_COMPLETE  
HUMAN_CLASSIFICATION_OPEN  
CALL_GRAPH_REVIEW_OPEN  
MAIN_NEGATIVE_TEST_PENDING  
PROTOCOL_NOT_FROZEN  
CONFIRMATORY_EXECUTION_NOT_AUTHORIZED  
CLAIM_SUPPORT_FALSE  
PROMOTION_AUTHORITY_FALSE
