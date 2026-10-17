
# Independent Null Calibration Review — 2026-10-17

**Review ID:** `INDEPENDENT_NULL_CALIBRATION_REVIEW_20261017_V1`

**Scientific status:** `UNDER_INVESTIGATION`

**Confirmatory protocol:** `NOT_FROZEN`

**Claim support:** `false`

**Promotion authority:** `false`

## Scope

This review independently recalculates the reported two-sided Wilson 95% intervals from the four published 1,000-repetition calibration counts. It does not claim that the complete Monte Carlo experiments were independently rerun.

## Recalculated results

| Scenario | Rejections / repetitions | Rate | Wilson 95% interval | Decision |
|---|---:|---:|---|---|
| gaussian_ar1_phi_0_4 | 52 / 1000 | 0.052 | [0.0398730363, 0.0675557393] | PASS for this scenario |
| gaussian_ar2_phi_0_45_minus_0_10 | 60 / 1000 | 0.060 | [0.0468964727, 0.0764710748] | FAIL |
| gaussian_ar5_low_order_coefficients | 49 / 1000 | 0.049 | [0.0372610346, 0.0641907015] | PASS for this scenario |
| gaussian_ar10_low_order_coefficients | 73 / 1000 | 0.073 | [0.0584590262, 0.0908090255] | FAIL |

## Acceptance rule

The declared rule requires the two-sided Wilson 95% interval to contain the nominal Type-I rate 0.05 AND its upper endpoint to be no greater than 0.075.

The AR(2) scenario fails the upper-endpoint requirement. The AR(10) scenario fails both requirements.

Passing two scenarios does not cancel the failures in the other two scenarios.

## Reproducibility boundary

The four scenario-specific jobs supplied for review belong to commit:

`9588084063ed02c456126a51a26fbd1ae992d82d`

The current candidate-selection commit is:

`598bfb5d1a47933de7c460df85f7c94cd1863cc4`

A same-commit rerun of all four scenario-specific simulations has not been established by the supplied run records. The current commit's calibration audit and passing unit tests do not substitute for that rerun.

## Decision

- Overall calibration acceptance: `NOT_PASSED`
- Confirmatory null protocol: `NOT_FROZEN`
- New candidate endpoint computation: `NOT_AUTHORIZED`
- Independent secondary replication count: `0/2`
- Claim support: `false`
- Promotion authority: `false`

## Required next actions

1. Preserve the current acceptance rule and all failed outputs.
2. Independently review whether the null family preserves the relevant temporal structure and whether the calibration scenarios cover the intended operating conditions.
3. Rerun all declared calibration scenarios on one exact, identified commit with locked dependencies and preserved outputs.
4. Record the code commit, environment, scenario definitions, seeds, repetition counts, and artifact hashes.
5. Do not compute candidate endpoints unless the methods review approves the null protocol and all required gates pass.

A passing engineering workflow is not, by itself, evidence that the scientific hypothesis is supported.
