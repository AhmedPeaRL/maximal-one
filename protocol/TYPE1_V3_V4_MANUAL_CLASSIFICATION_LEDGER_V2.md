# Type-I V3/V4 Manual Occurrence Classification Ledger V2

Status: OPEN — NOT COMPLETE
Review branch: review/type1-v4-remediation
Target review commit: b9496c02f38770c57917fd06a5fdfb8016af9142
Inventory source commit: PENDING — MUST MATCH TARGET REVIEW COMMIT
Inventory artifact ID: PENDING
Inventory SHA-256: PENDING
Reviewer: PENDING
Review date: PENDING

## 1. Purpose and boundary

This ledger records manual review of every relevant occurrence
identified by the automated inventory and every additional occurrence
identified by manual call-graph inspection.

The automated inventory is a discovery aid only.
Its classifications are not accepted as final classifications.

This ledger does not approve the V4 protocol, freeze the protocol,
authorize confirmatory execution, establish Type-I error control,
or support the broader HCM claim.

## 2. Mandatory occurrence-level classification

Every occurrence must receive exactly one primary classification:

- HISTORICAL
- DIAGNOSTIC
- PROPOSAL
- GOVERNANCE
- EXECUTION-CAPABLE-BUT-GATED
- EXECUTION-CAPABLE-UNRESOLVED
- AUTHORIZATION-CONTROL
- TEST-OR-REGRESSION-GUARD
- DOCUMENTATION-ONLY
- UNKNOWN

UNKNOWN is a valid and mandatory disposition whenever evidence is
insufficient. UNKNOWN must remain OPEN; it must never be converted
to a negative finding by assumption.

## 3. Required fields for every occurrence

Each row must identify:

1. Stable occurrence ID.
2. Branch/ref name.
3. Exact 40-character commit SHA.
4. File path.
5. Line number or line range.
6. Exact matched text.
7. Primary classification.
8. Whether the occurrence can influence execution.
9. Direct caller or workflow step.
10. Indirect call path, if any.
11. Runner or entry-point reached.
12. Trigger conditions.
13. Matrix/protocol consumed.
14. Authorization guard and its ordering.
15. Negative test proving unauthorized execution is blocked.
16. Evidence URL, artifact, log, or test result.
17. Reviewer disposition.
18. OPEN/CLOSED state and rationale.

A file name or a keyword match is never sufficient evidence
for an execution-path conclusion.

## 4. Occurrence ledger

The complete occurrence table must be generated from the fresh
inventory for both the review commit and the main comparison commit.

No occurrence may be silently omitted, merged, or summarized.

| ID | Ref | Commit SHA | File | Line | Exact occurrence | Class | Call path / caller | Guard evidence | Test evidence | Disposition | State |
|---|---|---|---|---:|---|---|---|---|---|---|---|
| PENDING | PENDING | PENDING | PENDING | PENDING | PENDING | UNKNOWN | PENDING | PENDING | PENDING | UNRESOLVED | OPEN |

## 5. Required call-path investigation

Inspect all relevant direct and indirect references, including
but not limited to:

- analysis/calibrate_null_type1.py
- analysis/calibrate_null_type1_scenario.py
- analysis/appropriate_stochastic_null.py
- analysis/null_protocol.py
- analysis/type1_calibration_pilot.py
- analysis/type1_execution_artifacts.py
- analysis/merge_type1_execution_shards.py
- analysis/merge_type1_calibration_pilot_shards.py
- analysis/compare_type1_cross_runner.py
- analysis/type1_acceptance_operating_characteristics.py
- scripts/audit_type1_governance_refs.py
- scripts/create_type1_review_snapshot.py

Inspect the complete current versions of all relevant workflows,
including:

- null-type1-calibration.yml
- type1-calibration-runtime-pilot.yml
- type1-full-path-equivalence.yml
- type1-v3-v4-governance-audit.yml
- type1-v4-assignment-matrix.yml
- type1-v4-cli-resume-identity.yml
- type1-v4-cross-runner-worker-order.yml
- type1-v4-engineering-equivalence.yml
- scientific-validation.yml
- scientific-claim-promotion.yml
- confirmatory-readiness-gate.yml

This list is a minimum, not proof of exhaustive coverage.
Add every other workflow, script, module, or indirect caller
identified by repository-wide inspection.

For every workflow, record:
- Every trigger and branch/path filter.
- Every job dependency and conditional.
- Every direct and indirect runner invocation.
- The exact matrix and protocol file consumed.
- All authorization checks and their execution order.
- Every route that can set or influence formal-pass,
  confirmatory authorization, claim support, or promotion authority.
- A negative test demonstrating that an unauthorized state
  cannot reach formal execution.

## 6. Historical acceptance-rule conflict

Preserve the historical acceptance rule and all historical outcomes.

Historical rule:
- Two-sided 95% Wilson interval must contain nominal alpha = 0.05.
- Upper endpoint must be <= 0.075.

Alternative candidate rule:
- One-sided 95% Wilson upper bound <= 0.075.

These are different statistical decision rules.
Do not silently substitute one for the other.
Do not change the threshold or confidence-bound rule after
observing results to obtain a passing outcome.

V4 acceptance rule: UNRESOLVED
Independent human recommendation: NOT RECEIVED
Prospective governance decision: NOT APPROVED

## 7. Required status safeguards

Until all required independent review and governance decisions
are complete:

- freeze_state = NOT_FROZEN
- confirmatory_execution_authorized = false
- claim_support = false
- promotion_authority = false
- formal calibration = NOT AUTHORIZED

Engineering equivalence is not formal Type-I calibration.
A pilot is not a confirmatory calibration.
An inventory is not a manual classification.
A passing workflow is not scientific approval.

## 8. Closure criteria

This ledger may be marked COMPLETE only when:

- The inventory is tied to the exact target commit.
- Every inventory occurrence has an individual disposition.
- Every additional manually discovered occurrence is included.
- Every execution-capable path has a documented call path.
- Every authorization path and guard ordering is verified.
- Every unresolved path remains explicitly OPEN.
- Relevant negative tests have actually passed.
- Evidence URLs, run IDs, artifact IDs, and hashes are recorded.
- The reviewer and review date are attributable.
- The ledger itself is committed and hashed.

Completion means complete coverage of the declared review scope.
It does not mean universal proof, protocol approval, or scientific
validation.
