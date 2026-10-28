# Type-I V3/V4 Governance Inventory — 2026-10-27

Status: INITIAL INVENTORY; FULL BRANCH-BY-BRANCH AUDIT STILL REQUIRED

## 1. Purpose

Classify legacy V3 workflows, candidate V4 workflows, and references
to the 0.075 acceptance ceiling without deleting historical evidence
or transferring execution authority between protocol versions.

## 2. Classification rules

- HISTORICAL:
  Records the rule or result used at the time. Preserve unchanged.

- DIAGNOSTIC:
  Reports analyses, operating characteristics, tests, or audits that
  do not authorize confirmatory execution.

- PROPOSAL:
  Describes a candidate protocol or acceptance rule that has not
  received the required approval.

- EXECUTION-CAPABLE-BUT-GATED:
  Contains an execution path, but must refuse to execute unless its
  own matching protocol is approved, frozen, and explicitly authorized.

- GOVERNANCE:
  Enforces review, promotion, or eligibility conditions without
  itself constituting a calibration result.

## 3. Known V3 workflow

Path:
`.github/workflows/null-type1-calibration.yml`

Classification:
EXECUTION-CAPABLE-BUT-GATED

Required treatment:
- Preserve the workflow and historical runs.
- Preserve its V3 identity and V3 matrix reference.
- Require a fail-closed approval/freeze/authorization gate.
- Verify that the workflow invokes a runner matching the V3 schema.
- Never allow the workflow to invoke a V4 candidate runner under V3
  labels or metadata.
- Do not enable formal execution while approval is absent.

## 4. Other known workflows

Path:
`.github/workflows/scientific-validation.yml`

Classification:
GOVERNANCE / DIAGNOSTIC

Required treatment:
Inspect every step for indirect execution, promotion, or modification
of the calibration gate. Tests and compilation alone are not
calibration evidence.

Path:
`.github/workflows/scientific-claim-promotion.yml`

Classification:
GOVERNANCE / PROMOTION GATE

Required treatment:
Preserve the promotion guards. Verify that no engineering-only
artifact can be treated as a formal Type-I pass or claim support.

Path:
`.github/workflows/type1-v4-engineering-equivalence.yml`

Classification:
ENGINEERING-ONLY

Required treatment:
May test artifact integrity, CLI resume, sharding, merging, and
execution-path equivalence. Must not authorize formal calibration.

Path:
`.github/workflows/type1-v4-cross-runner-worker-order.yml`

Classification:
ENGINEERING-ONLY

Required treatment:
May compare separate runner jobs for a fixed bounded configuration.
Must not authorize formal calibration.

## 5. Known 0.075 references

- `protocol/TYPE1_CALIBRATION_SPEC_V3_CANDIDATE.md`
  Classification: PROPOSAL.

- `protocol/TYPE1_AUDIT_INTERPRETATION_20261011.md`
  Classification: HISTORICAL / DIAGNOSTIC.

- `protocol/TYPE1_CALIBRATION_DECISION_RECORD_V1.md`
  Classification: GOVERNANCE; threshold unresolved.

- `protocol/TYPE1_CALIBRATION_REVIEWER_REQUEST_V2.md`
  Classification: REVIEW REQUEST; not approval.

- `protocol/TYPE1_CALIBRATION_RUN_REVIEW_20261011.md`
  Classification: HISTORICAL RESULTS.

- `protocol/ACCEPTANCE_DECISION_RECORD_2026-10-19.md`
  Classification: HISTORICAL DECISION RECORD.

- `protocol/TYPE1_CALIBRATION_IMPLEMENTATION_GAP_V1.md`
  Classification: HISTORICAL / DIAGNOSTIC.

- `protocol/TYPE1_CALIBRATION_RESULT_REVIEW_20261010.md`
  Classification: HISTORICAL RESULTS.

- `protocol/TYPE1_CALIBRATION_TECHNICAL_REVIEW_20261020.md`
  Classification: TECHNICAL REVIEW; conflict documented.

- `protocol/TYPE1_ACCEPTANCE_RULE_OPERATING_CHARACTERISTICS_V1.md`
  Classification: DIAGNOSTIC; not acceptance-rule approval.

The list above is an initial inventory, not proof that every reference
in every branch has been found.

## 6. Mandatory branch-specific audit

For each branch, search all workflows, runner code, matrices,
tests, documentation, and scripts for:
- `0.075`
- `MAX_ACCEPTABLE_WILSON_UPPER`
- `ACCEPTANCE_RULE`
- `V3`
- `V4_APPROVED`
- `confirmatory_execution_authorized`
- `formal_calibration_pass`

For every match, record:
- path and line range;
- branch and exact commit SHA;
- whether the reference is historical, diagnostic, proposed,
  governance-related, or execution-capable;
- whether it can launch or authorize a calibration run;
- the specific fail-closed guard;
- the test that proves the guard works.

## 7. Governance decision

No historical result is deleted or reinterpreted.
No acceptance threshold is approved by this inventory.
No V3 workflow is disabled merely to hide a conflict.
No V3 workflow may execute V4 code under V3 identity.
No engineering workflow may grant confirmatory authorization.

Required state remains:

- V4 freeze state: NOT_FROZEN
- confirmatory_execution_authorized: false
- claim_support: false
- promotion_authority: false
- formal calibration: NOT AUTHORIZED

## Addendum — 2026-10-29 — Current engineering and governance controls

Status: PARTIAL INVENTORY; TWO-REF AUTOMATED AUDIT REQUIRED

### 1. Current CLI resume identity evidence

The workflow run `40778431846` on commit
`f88c7918c36f09953dd129cf45bddcadb75fde0c` completed the dedicated
CLI resume identity rejection test successfully.

This is engineering evidence only. The exact exit-code and diagnostic
assertions remain subject to the follow-up test remediation recorded
in the V4 acceptance ledger.

### 2. Known V3/V4 workflow classifications

- `.github/workflows/null-type1-calibration.yml`
  Classification: LEGACY V3 EXECUTION-CAPABLE-BUT-FAIL-CLOSED.
  Preserve historical runs. Do not repoint this workflow to the V4
  candidate matrix. Its V3 runner and matrix compatibility must be
  independently verified before any future authorization.

- `.github/workflows/type1-v4-cli-resume-identity.yml`
  Classification: ENGINEERING-ONLY CLI IDENTITY REJECTION.
  It tests bounded resume rejection. It does not authorize calibration.

- `.github/workflows/type1-v4-engineering-equivalence.yml`
  Classification: ENGINEERING-ONLY.
  It tests artifact integrity, merger behavior, resume identity,
  governance separation, worker ordering, and bounded path equivalence.
  It must not authorize formal calibration.

- `.github/workflows/type1-v4-cross-runner-worker-order.yml`
  Classification: ENGINEERING-ONLY CROSS-RUNNER COMPARISON.
  Its evidence is limited to the tested configuration and runner
  environments.

- `.github/workflows/type1-v4-assignment-matrix.yml`
  Classification: ENGINEERING-ONLY WORKER ASSIGNMENT AUDIT.
  Its output must remain separate from scientific acceptance.

- `.github/workflows/type1-full-path-equivalence.yml`
  Classification: ENGINEERING PATH-EQUIVALENCE EVIDENCE ONLY.

- `.github/workflows/type1-calibration-runtime-pilot.yml`
  Classification: EXPLORATORY RUNTIME DIAGNOSTIC ONLY.

- `.github/workflows/null-calibration-audit.yml`
  Classification: DIAGNOSTIC AUDIT ONLY; its reduced design is not
  the formal V4 calibration protocol.

- `.github/workflows/confirmatory-readiness-gate.yml`
  Classification: GOVERNANCE GATE; inspect its complete call path and
  verify that it cannot authorize V4 without the required signed
  decision and frozen protocol.

The above list is a known-workflow inventory, not a claim that every
relevant workflow, indirect runner, or reference on both branches has
already been exhaustively reviewed.

### 3. Required reference classification

The generated two-ref inventory must be reviewed for each occurrence
of `0.075`, V3, V4, acceptance-rule fields, and authorization fields.

Every relevant reference must be assigned one of these classes:

- HISTORICAL: immutable record of a prior rule or outcome.
- DIAGNOSTIC: analysis, audit, operating-characteristic study, or test.
- PROPOSAL: unapproved protocol, threshold, or design.
- GOVERNANCE: guard, readiness check, or promotion control.
- EXECUTION-CAPABLE-BUT-GATED: code or workflow that can attempt
  execution but must refuse unless the exact matching protocol is
  approved, frozen, and separately authorized.

For each execution-capable path, record the exact fail-closed guard
and the regression test that demonstrates the guard.

### 4. Non-retroactivity and authority

No historical record may be deleted, overwritten, or relabeled to
make a previously failed result pass.

No `0.075` reference is approval by itself.

No engineering workflow may set formal calibration success,
claim support, promotion authority, or confirmatory authorization.

Until the independent statistical review and prospective decision
are attributable and complete:

- `freeze_state = NOT_FROZEN`
- `confirmatory_execution_authorized = false`
- `claim_support = false`
- `promotion_authority = false`
- Formal calibration = NOT AUTHORIZED
