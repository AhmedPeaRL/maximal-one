# Type-I Main-Branch Execution Review — V3

Record status: NEGATIVE_TEST_OBSERVED_EXPECTED_BLOCK
Authority: Governance and execution-path evidence only
Scientific approval: NONE
Protocol freeze: NOT FROZEN
Confirmatory execution: NOT AUTHORIZED
Claim support: FALSE
Promotion authority: FALSE

## 1. Exact identities

Repository: AhmedPeaRL/maximal-one

Main branch:
- Branch: main
- Commit: 3899c6aa5a0d0f486bb3e78373d9b04d9ae155f6
- Workflow run: 41334991587
- Job: 124932813848
- Scenario matrix job: 124932872243
- Workflow:
  .github/workflows/null-type1-calibration.yml

Separate review branch:
- Branch: review/type1-v4-remediation
- Commit: e8e127259e475b06599d3f5fc550cd6a616a127f

Evidence from the review branch must not be treated as
evidence that the same implementation or guard exists on main.

## 2. Observed main-branch negative test

Run 41334991587 completed with GitHub conclusion FAILURE.

Observed job-level results:
- Preparation job 124932813848: FAILURE.
- Protocol validation step: FAILURE.
- Scenario matrix job 124932872243: SKIPPED.
- Run artifact listing: ZERO artifacts.

The exact V3 matrix at the tested commit declares:
- status: CANDIDATE_PENDING_ATTRIBUTABLE_INDEPENDENT_STATISTICAL_REVIEW
- freeze_state: NOT_FROZEN
- archive_git_identity_verified: false
- confirmatory_execution_authorized: false
- claim_support: false
- promotion_authority: false

The workflow checks APPROVED_FROZEN before emitting a matrix.

The expected rejection text from the checked-in workflow is:

BLOCKED: V3 protocol is not APPROVED_FROZEN.
No calibration simulations were started.

The step failure and skipped matrix job are directly observed.
The exact console text above is derived from the workflow source
and current matrix state; it must not be represented as raw-log
verification unless the raw log is separately archived.

Disposition:

EXPECTED_FAIL_CLOSED_BEHAVIOR_OBSERVED;
WORKFLOW_CONCLUSION_FAILURE;
NO_SCENARIO_JOB_STARTED;
NO_CALIBRATION_ARTIFACTS;
NO_CONFIRMATORY_AUTHORIZATION.

This is not a successful CI run and not a statistical
calibration result.

## 3. Main-branch execution-path finding

The observed run demonstrates blocking for this exact main
snapshot and current unfrozen V3 matrix.

It does not prove that every future workflow edit, direct CLI
invocation, alternate entry point, or modified matrix is safe.

Required follow-up:
1. Keep all approval, freeze, and authorization fields false.
2. Do not modify the matrix to make the workflow green.
3. Manually trace direct and indirect callers.
4. Review the direct Python runner separately from workflow gates.
5. Verify that every unauthorized entry point fails closed.
6. Retain exact run, job, commit, and artifact evidence.

## 4. Branch separation

The review branch at:

e8e127259e475b06599d3f5fc550cd6a616a127f

contains separate V4 candidate engineering and governance
changes.

Its inventory and snapshot workflows are not evidence that
the same guards exist on main.

No full-branch merge is authorized by this record.

## 5. Closure conditions

Do not close this review until:
- main direct and indirect execution paths are manually traced;
- authorization guard ordering is verified;
- every relevant unauthorized entry point has a negative test;
- V3/V4 separation tests pass on a pinned review commit;
- an attributable independent human statistical review
  resolves the protocol questions;
- a separate freeze decision and execution authorization
  are recorded.

## 6. Non-negotiable state

freeze_state = NOT_FROZEN
confirmatory_execution_authorized = false
claim_support = false
promotion_authority = false
formal_calibration_pass = false

No merge from review/type1-v4-remediation to main is
authorized by this record.
