# Type-I Acceptance Threshold Reference Inventory — 2026-10-27

## Status

Disposition: HOLD — NO FORMAL V4 EXECUTION

This inventory is a governance and traceability record.
It does not approve the value 0.075, freeze V4, or authorize
confirmatory execution.

## 1. Historical evidence and interpretation

Preserve these records and their original classifications:

- protocol/TYPE1_CALIBRATION_RUN_REVIEW_20261011.md
- protocol/TYPE1_CALIBRATION_RESULT_REVIEW_20261010.md
- protocol/ACCEPTANCE_DECISION_RECORD_2026-10-19.md
- protocol/TYPE1_CALIBRATION_IMPLEMENTATION_GAP_V1.md
- protocol/TYPE1_AUDIT_INTERPRETATION_20261011.md
- protocol/INDEPENDENT_NULL_CALIBRATION_REVIEW_20261017.md
- protocol/INDEPENDENT_SCIENTIFIC_AUDIT_20261016.md
- protocol/INDEPENDENT_REVIEW_ADDENDUM_20261018.md
- protocol/INDEPENDENT_TECHNICAL_REVIEW_20261016.md
- protocol/LIVE_STATE_TRIAGE_20261012.md
- protocol/SCIENTIFIC_GATE_DIAGNOSTIC_FIX_PLAN_20261011.md
- protocol/CLOSURE_DECISION_AND_FREEZE_REASSESSMENT_20261018.md
- protocol/TYPE1_CALIBRATION_TECHNICAL_REVIEW_20261020.md
- docs/research/AR_P_NULL_ADEQUACY_REVIEW_2026-10-17.md
- docs/research/PROSPECTIVE_CONFIRMATORY_PROTOCOL_V1_DRAFT.md
- protocol/INDEPENDENT_TECHNICAL_REVIEW_20261016.md
- protocol/INDEPENDENT_REVIEW_ADDENDUM_20261018.md
- protocol/TYPE1_CALIBRATION_PREREGISTRATION_V2.md
- protocol/NULL_ADEQUACY_CALIBRATION_EXECUTION_PLAN_V3_DRAFT.md
- protocol/NEXT_STEP_ORDER_20261011.md

These records are not to be overwritten or reclassified
under a later acceptance rule.

## 2. Candidate or unresolved rule references

These are proposals, requests, templates, or decision records.
Their existence is not approval:

- protocol/TYPE1_CALIBRATION_SPEC_V3_CANDIDATE.md
- protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V3.json
- protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V2.json
- protocol/NULL_ADEQUACY_CALIBRATION_PLAN_V2.json
- protocol/TYPE1_CALIBRATION_REVIEWER_REQUEST_V2.md
- protocol/TYPE1_CALIBRATION_DECISION_RECORD_V1.md
- protocol/TYPE1_ACCEPTANCE_RULE_OPERATING_CHARACTERISTICS_V1.md
- protocol/TYPE1_ACCEPTANCE_RULE_DECISION_TEMPLATE_V1.md
- protocol/TYPE1_V4_ACCEPTANCE_RULE_DECISION_RECORD.md
- protocol/TYPE1_V4_DECISION_RECORD_2026-10-27.md
- protocol/V3_V4_GOVERNANCE_RECONCILIATION_2026-10-26.md

The historical two-sided rule and the candidate one-sided rule
are different decision rules. They must not be silently merged.

## 3. Diagnostic implementation and audit references

- analysis/type1_acceptance_operating_characteristics.py
- audit/type1_acceptance_operating_characteristics.json
- tests/test_type1_acceptance_operating_characteristics.py
- tests/test_type1_calibration_v3_candidate.py
- audit/downloaded-artifacts/null_type1_calibration_gaussian_ar1_phi_0_4.json
- audit/downloaded-artifacts/null_type1_calibration_gaussian_ar2_phi_0_45_minus_0_10.json
- audit/downloaded-artifacts/null_type1_calibration_gaussian_ar5_low_order_coefficients.json
- audit/downloaded-artifacts/null_type1_calibration_gaussian_ar10_low_order_coefficients.json

These are analytical helpers, tests, or historical evidence.
They do not independently approve a scientific threshold.

## 4. Workflow and runtime authority

- .github/workflows/null-type1-calibration.yml:
  legacy V3 path. Preserve it. Its current authorization gates
  must remain fail-closed while the V3 protocol is not approved
  and frozen. Never repoint it to the V4 candidate matrix.

- .github/workflows/type1-v4-engineering-equivalence.yml:
  engineering-only. It must never authorize formal calibration,
  claim support, or promotion.

- .github/workflows/type1-full-path-equivalence.yml:
  engineering path-equivalence evidence only.

- .github/workflows/type1-calibration-runtime-pilot.yml:
  exploratory runtime pilot only; its reduced dimensions do not
  constitute formal Type-I calibration.

- .github/workflows/null-calibration-audit.yml:
  diagnostic audit only.

- .github/workflows/scientific-claim-promotion.yml:
  runs separate null-adequacy and promotion checks. Its presence
  does not constitute approval of the V4 Type-I acceptance rule.

## 5. Prospective decision

No V4 acceptance rule is approved.

Before any formal V4 run, an attributable independent human
statistician must select and justify one complete prospective rule,
including interval sidedness, confidence level, numerical boundary,
outer repetition count, scenario aggregation, invalid-attempt
policy, and failure conditions.

The decision must bind to the exact reviewed commit and hashes.
AI-generated analysis and successful engineering CI are not
independent human statistical approval.

## 6. Non-retroactivity and authorization

Historical results retain the rule and classification that
actually applied to them. No threshold may be changed
retrospectively to turn a historical failure into a pass.

Until the independent review, protocol freeze, and separate
authorization decision are complete:

- freeze_state = NOT_FROZEN
- confirmatory_execution_authorized = false
- claim_support = false
- promotion_authority = false
- formal V4 calibration = NOT_AUTHORIZED
