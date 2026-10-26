# V3/V4 Governance Reconciliation — 2026-10-26

## Status

Disposition: HOLD — NO FORMAL V4 EXECUTION

V4 remains NOT_FROZEN.
Confirmatory execution remains NOT_AUTHORIZED.
claim_support remains false.
promotion_authority remains false.

This record classifies existing controls and historical references.
It does not approve an acceptance rule, alter historical results,
or authorize a calibration run.

## 1. Legacy V3 workflow

Workflow:
`.github/workflows/null-type1-calibration.yml`

Referenced matrix:
`protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V3.json`

Referenced runner:
`analysis/calibrate_null_type1_scenario.py`
and `analysis/calibrate_null_type1.py`

Classification:
LEGACY V3 WORKFLOW — CURRENTLY FAIL-CLOSED, BUT CAPABLE OF
ATTEMPTING V3 FORMAL EXECUTION IF ITS V3 AUTHORIZATION GATES
WERE TO BE CHANGED.

Observed safeguards include checks for:
- status == APPROVED_FROZEN
- freeze_state == FROZEN
- confirmatory_execution_authorized == true
- archive_git_identity_verified == true
- exactly nine declared scenarios
- expected V3 dimensions

The current V3 matrix records confirmatory authorization as false.
The workflow must not be treated as a V4 execution or approval path.

Required control:
Preserve the workflow and its historical evidence. Do not delete it
or silently repoint it to V4. Add an explicit regression test proving
that the V3 workflow and V3 runner cannot authorize or consume the
V4 candidate matrix as an approved V4 protocol.

## 2. V4 engineering workflow

Workflow:
`.github/workflows/type1-v4-engineering-equivalence.yml`

Classification:
ENGINEERING-ONLY WORKFLOW.

It may test artifacts, identity rejection, shard merging, resume,
and path equivalence. It must not run formal V4 calibration or
set claim_support, promotion_authority, or
confirmatory_execution_authorized to true.

The bounded CLI mode must continue to emit
formal_calibration_pass=false.

## 3. Acceptance-rule references

The repository contains materially different rule descriptions:

A. Historical rule:
The two-sided 95% Wilson interval must contain nominal alpha 0.05,
and its upper endpoint must be <= 0.075.

B. V3 candidate rule:
The one-sided 95% Wilson upper bound must be <= 0.075;
the two-sided interval is reported but does not decide acceptance.

These are different decision rules. They must not be silently merged.

The historical 0.075 ceiling is not approved for V4.
No prospective V4 acceptance rule is approved by this record.

## 4. Classification of 0.075 references

Historical evidence / interpretation:
- `protocol/TYPE1_CALIBRATION_RUN_REVIEW_20261011.md`
- `protocol/TYPE1_CALIBRATION_RESULT_REVIEW_20261010.md`
- `protocol/ACCEPTANCE_DECISION_RECORD_2026-10-19.md`
- `protocol/TYPE1_CALIBRATION_IMPLEMENTATION_GAP_V1.md`

These files document historical outcomes and the rule applied at
the time. Preserve their original interpretations.

Candidate specification / not approved:
- `protocol/TYPE1_CALIBRATION_SPEC_V3_CANDIDATE.md`
- `protocol/TYPE1_CALIBRATION_REVIEWER_REQUEST_V2.md`
- `protocol/TYPE1_ACCEPTANCE_RULE_OPERATING_CHARACTERISTICS_V1.md`
- `protocol/TYPE1_CALIBRATION_DECISION_RECORD_V1.md`
- `protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json`

These documents describe candidate rules, operating characteristics,
or unresolved decisions. They do not authorize formal V4 execution.

Implementation reference:
- `analysis/calibrate_null_type1.py`

The implementation constant is not independent scientific approval.
Its presence must not be interpreted as a signed decision.

Audit-only reference:
- `protocol/TYPE1_AUDIT_INTERPRETATION_20261011.md`

The audit-only document must remain diagnostic and must not change
the production gate.

## 5. Prospective decision required

Before any formal V4 run, an attributable independent human
statistician must review and document:

1. The target estimand and intended interpretation.
2. The complete acceptance rule, including interval sidedness.
3. The substantive consequences that justify any tolerance above 0.05,
   or a prospective alternative to the historical 0.075 ceiling.
4. Operating characteristics at relevant true rejection probabilities.
5. The treatment of invalid attempts and the fixed requested denominator N.
6. Scenario coverage, null adequacy, runtime feasibility, and replication.

The decision must identify the exact reviewed commit, matrix digest,
date, reviewer identity, relevant expertise, conflicts of interest,
rationale, and explicit disposition.

An AI-generated draft or successful CI run is not an independent
human statistical approval.

## 6. Historical integrity

Do not delete, overwrite, or relabel historical results.
Do not change a threshold retrospectively to make a failed result pass.
A future prospective rule applies only to the protocol and runs
explicitly covered by its approval.

## 7. Authorization gate

No formal run is permitted until all of the following are true:

- V4 matrix reviewed and frozen prospectively.
- Acceptance rule approved and machine-readable.
- Independent human review attributable and recorded.
- CLI resume and shard invariance gates passed.
- V3/V4 workflow separation tested.
- Exact commit, dependency lock, matrix, runner, and environment
  identities recorded.
- A separate explicit authorization decision is committed.

Until then:
NOT_FROZEN; NOT_AUTHORIZED; claim_support=false;
promotion_authority=false.
