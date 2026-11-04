# Type-I V4 — AI Static Execution-Path Triage

## Review identity

- Repository: AhmedPeaRL/maximal-one
- Branch: review/type1-v4-remediation
- Exact commit: 0de129986f95282bcc34a00a5628f3507bafcb10
- Inventory artifact: 13303605715
- Inventory SHA-256: 451e83fece077884ec267ba2f31462436655ec3abc42cb66af22effa3f2e3c3d
- Review type: AI-assisted static technical triage
- Human adjudication: NOT PERFORMED
- Protocol freeze: NOT_FROZEN
- Formal calibration: NOT_AUTHORIZED
- Confirmatory execution: NOT_AUTHORIZED

## Scope and limitation

This document records technical observations from the exact source snapshot.
It is not an independent human review, statistical approval, protocol freeze,
execution authorization, or scientific adjudication.

Automated classifications remain provisional.
All three execution-capable workflow candidates remain UNKNOWN / OPEN / PENDING
until an attributable qualified human reviewer records a decision.

## Candidate 1

- Occurrence ID: HEAD/2f8523fcf7c5/73/4
- Path: .github/workflows/type1-calibration-runtime-pilot.yml
- Line: 73
- Technical nature: exploratory runtime-pilot invocation
- Runner: analysis.type1_calibration_pilot
- Candidate scenario: gaussian_ar2_inband_f_0_02_radius_0_90_n3328
- Requested outer replicates: 2
- Requested surrogates per replicate: 200
- Matrix consumed by runner: TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_DRAFT.json

### Observed controls

- Runtime-pilot branch guard is invoked before output creation and runner invocation.
- The guard permits refs/heads/review/type1-v4-remediation.
- The guard rejects refs/heads/main.
- The runner entry point calls require_authorized_branch() before argument processing.
- Existing tests inspect the guard ordering and unauthorized-main rejection.

### Technical interpretation

This is an execution-capable exploratory pilot path.
The observed branch restriction does not constitute formal protocol approval.
The pilot is not formal Type-I calibration and does not establish claim support.

### Human review still required

- Confirm complete direct and indirect call path.
- Verify all trigger conditions and branch restrictions.
- Verify the negative test against the exact workflow and runner.
- Confirm that no alternate invocation bypasses the branch guard.
- Record source and test evidence hashes.

## Candidate 2

- Occurrence ID: HEAD/40d0253a5dd6/60/6
- Path: .github/workflows/type1-v4-cross-runner-worker-order.yml
- Line: 60
- Job: connected-reference
- Runner: analysis.calibrate_null_type1_scenario
- Mode: --engineering-test
- Scenario: gaussian_ar2_phi_0_45_minus_0_10_n3328
- Requested repetitions: 6
- Requested surrogates: 1000
- Sample size: 3328

### Observed controls

- Review-branch identity is checked before Python setup and runner invocation.
- Checkout HEAD is compared with GITHUB_SHA.
- The invocation explicitly uses --engineering-test.
- The engineering runner restricts scenario and execution dimensions.
- The engineering output declares formal_calibration_pass=false,
  claim_support=false, promotion_authority=false, and
  confirmatory_execution_authorized=false.

### Technical interpretation

This is an execution-capable engineering reference path.
It is not formal Type-I calibration.
Branch restriction and engineering-mode restrictions are not protocol approval.

### Human review still required

- Inspect all callers and entry points.
- Verify the engineering-mode restrictions fail closed.
- Verify the connected reference cannot be interpreted as a formal result.
- Record exact negative-test and artifact evidence.

## Candidate 3

- Occurrence ID: HEAD/40d0253a5dd6/60/6
- Path: .github/workflows/type1-v4-cross-runner-worker-order.yml
- Line: 123
- Job: independent-workers
- Runner: analysis.calibrate_null_type1_scenario
- Mode: --engineering-test
- Scenario: gaussian_ar2_phi_0_45_minus_0_10_n3328
- Requested repetitions: 6
- Requested surrogates: 1000
- Sample size: 3328
- Worker assignment: one replicate index per matrix worker

### Observed controls

- Review-branch identity is checked before Python setup and runner invocation.
- Checkout HEAD is compared with GITHUB_SHA.
- The invocation explicitly uses --engineering-test.
- Each worker receives a bounded replicate index.
- The workflow's comparison job checks worker outputs against the connected reference.

### Technical interpretation

This is an execution-capable distributed engineering path.
It is not formal Type-I calibration.
Static workflow tests do not by themselves prove all runtime failure modes.

### Human review still required

- Verify worker assignment and range boundaries.
- Verify duplicate, missing, overlapping, and out-of-range replicate rejection.
- Verify every worker fails closed on identity mismatch.
- Verify comparison failure cannot be converted into a pass.
- Record exact source, test, workflow-log, and artifact hashes.

## Current decision state

All three candidates remain:

- manual_classification: UNKNOWN
- status: OPEN
- reviewer_disposition: PENDING
- guard_fails_closed: UNKNOWN pending occurrence-specific adjudication
- execution authority: NONE

This document must never be merged as a human adjudication.
A qualified independent reviewer must inspect the exact snapshot and issue
attributable decisions with evidence.

## Explicit non-claims

This triage does not establish:

- V4 statistical validity
- Type-I calibration pass
- protocol freeze
- confirmatory execution authorization
- independent human review
- HCM claim support
- promotion authority
