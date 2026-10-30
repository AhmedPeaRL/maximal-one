Type-I Review Snapshot Policy V1

Status: REQUIRED_BEFORE_INDEPENDENT_REVIEW
Protocol: HCM_TYPE1_CALIBRATION_V4_CANDIDATE
Freeze state: NOT_FROZEN
Formal calibration: NOT_AUTHORIZED

1. Review identity

The review identity consists of:

- Repository: "AhmedPeaRL/maximal-one"
- Review branch: "review/type1-v4-remediation"
- Exact commit SHA: required; branch name alone is insufficient
- SHA-256 digest for every file in the declared review scope
- Inventory artifact ID and its source commit
- Snapshot manifest and SHA256SUMS file

2. Required file scope

The snapshot must include, when present:

Protocol and governance

- "protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V3.json"
- "protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json"
- "protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_DRAFT.json"
- "protocol/TYPE1_CALIBRATION_SPEC_V3_CANDIDATE.md"
- "protocol/TYPE1_CALIBRATION_V4_ACCEPTANCE_RULE_DECISION_REQUEST.md"
- "protocol/TYPE1_CALIBRATION_EXECUTION_AUTHORIZATION.json"
- "protocol/TYPE1_CALIBRATION_FREEZE_DECISION.json"
- "protocol/TYPE1_V3_V4_GOVERNANCE_INVENTORY_2026-10-27.md"
- "protocol/TYPE1_V3_V4_MANUAL_CLASSIFICATION_LEDGER_2026-10-29.md"
- "protocol/TYPE1_ENGINEERING_EVIDENCE_ADDENDUM_2026-10-30.md"

Statistical implementation

- "analysis/calibrate_null_type1.py"
- "analysis/calibrate_null_type1_scenario.py"
- "analysis/appropriate_stochastic_null.py"
- "analysis/numerical_spectral_verification.py"
- "analysis/null_protocol.py"
- "analysis/type1_calibration_pilot.py"
- "analysis/type1_execution_artifacts.py"
- "analysis/merge_type1_execution_shards.py"
- "analysis/merge_type1_calibration_pilot_shards.py"
- "analysis/compare_type1_cross_runner.py"
- "analysis/type1_acceptance_operating_characteristics.py"

Dependencies

- "requirements-lock.txt"
- "requirements.in"

Relevant workflows

- ".github/workflows/null-type1-calibration.yml"
- ".github/workflows/scientific-claim-promotion.yml"
- ".github/workflows/scientific-validation.yml"
- ".github/workflows/confirmatory-readiness-gate.yml"
- ".github/workflows/type1-calibration-runtime-pilot.yml"
- ".github/workflows/type1-full-path-equivalence.yml"
- ".github/workflows/type1-v3-v4-governance-audit.yml"
- ".github/workflows/type1-v4-engineering-equivalence.yml"
- ".github/workflows/type1-v4-cli-resume-identity.yml"
- ".github/workflows/type1-v4-assignment-matrix.yml"
- ".github/workflows/type1-v4-cross-runner-worker-order.yml"

Relevant tests

- "tests/test_v3_v4_governance_separation.py"
- "tests/test_type1_full_path_equivalence.py"
- "tests/test_type1_production_equivalence.py"
- "tests/test_type1_resume_cli_identity_rejections.py"
- "tests/test_type1_worker_assignment_matrix_invariance.py"
- "tests/test_type1_parallel_worker_order_equivalence.py"

3. Integrity requirements

For each existing file in scope, record:

- Exact repository-relative path
- Exact SHA-256 of file bytes
- Exact review commit SHA
- File existence status

Missing files must be recorded as missing. They must not be silently omitted.

The manifest must fail if the checked-out commit differs from the requested review commit or if the branch is not the designated remediation branch.

4. Non-retroactivity

A later commit creates a new review snapshot. It does not modify the identity of an earlier snapshot.

No protocol freeze, acceptance-rule approval, or confirmatory execution authorization is implied by producing this manifest.

5. Current authority

- Independent human statistical review: PENDING
- Acceptance rule: UNRESOLVED
- Protocol freeze: NOT_FROZEN
- Confirmatory execution: NOT_AUTHORIZED
- Claim support: false
- Promotion authority: false
