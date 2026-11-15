# Prospective Type-I Acceptance Rule — Decision V1

- **Decision ID:** `HCM_TYPE1_CONTROL_UCB_IUT_V1`  
- **Status:** `RULE_FAMILY_SELECTED_PENDING_INDEPENDENT_STATISTICAL_REVIEW`  
- **Protocol freeze:** `NOT_FROZEN`  
- **Formal calibration:** `NOT_AUTHORIZED`

## 1. Selected objective

The future calibration objective is control of Type-I error inflation, not equivalence to exactly 0.05.

## 2. Estimand

For each required null scenario `s`:

`p_s = Pr(the complete production-equivalent test rejects | data generated under null scenario s)`

The rejection event must be the actual production decision, including endpoint estimation, fitting, surrogate generation and refitting, invalid-fit handling, denominator, and p-value rule.

## 3. Per-scenario candidate acceptance rule

For every required scenario:

`U_s(0.95) <= alpha_max`

where `U_s(0.95)` is a one-sided 95% upper confidence bound for the scenario's Type-I error probability.

The one-sided 95% Wilson upper bound is the current candidate method. The independent statistical reviewer must assess it and may recommend an exact binomial bound or another justified procedure.

## 4. Suite decision

All nine required scenarios must pass. No averaging, majority vote, or compensation between scenarios is permitted. One failed, incomplete, invalid, or unresolved scenario blocks the suite.

This is an intersection-union decision for the single global claim that all required scenarios satisfy the ceiling. Under that all-must-pass formulation, a 5% one-sided test per scenario controls the global false-acceptance probability at no more than 5% without Bonferroni adjustment. This does not provide simultaneous 95% confidence coverage for separate per-scenario claims.

## 5. Numerical tolerance

`alpha_max = NOT_SET`

The historical `0.075` ceiling is not adopted. It permits a 50% relative increase over nominal 0.05 and currently lacks a documented scientific risk justification.

The independent reviewer must justify the numerical tolerance and evaluate the probability of passing the entire nine-scenario suite under nominal and inflated Type-I rates.

## 6. Repetition count and invalid attempts

The proposed 2,000 outer repetitions and 1,000 surrogates per outer replicate remain candidate dimensions only.

Every requested outer attempt must be preserved. Invalid attempts are not non-rejections. Missing attempts, duplicates, unresolved surrogate shortfalls, or corrupted artifacts block a pass unless a separately justified recovery policy is prospectively approved.

No silent dropping, replacement, outcome-dependent stopping, or denominator changes are allowed.

## 7. Historical protection

Historical V1 remains `NOT_PASSED` under the rule used at that time:

- AR1: 52/1000; [0.039873, 0.067556]
- AR2: 60/1000; [0.046896, 0.076471], failed
- AR5: 49/1000; [0.0372610346, 0.0641907015]
- AR10: 73/1000; [0.058459, 0.090809], failed

No retrospective reclassification is permitted.

## 8. Approval boundary

This decision selects the objective and suite logic only. It does not approve a numerical acceptance rule, freeze V4, or authorize execution.

Before freeze, an attributable independent human statistical report must approve or replace the confidence-bound method, numerical tolerance, repetition count, suite-level operating characteristics, scenario coverage, and invalid-attempt policy.

Until then:
- `acceptance_rule_approved = false`
- `freeze_state = NOT_FROZEN`
- `confirmatory_execution_authorized = false`
- `claim_support = false`
- `promotion_authority = false`
