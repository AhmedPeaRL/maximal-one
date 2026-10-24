Type-I Calibration V4 — Prospective Acceptance-Rule Decision Request

1. Purpose

This document requests a reasoned, prospective statistical decision on the acceptance rule for the proposed Type-I Calibration V4 protocol.

It does not approve, freeze, or authorize the protocol. It does not select an acceptance threshold.

2. Review target

Repository: "AhmedPeaRL/maximal-one"

Remediation branch: "review/type1-v4-remediation"

Candidate review base: "9fafec47afbaaed8dfbe31b4f4e53f2ff3a99b83"

Candidate matrix: "protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json"

Design draft: "protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_DRAFT.json"

Current status: "NOT_FROZEN"

Confirmatory execution: "NOT_AUTHORIZED"

Claim support: "NOT_ESTABLISHED"

The exact commit containing this request and the exact file hashes must be recorded before any review decision is treated as applicable.

3. Decisions requested before formal execution

The reviewer is asked to provide a reasoned recommendation for each item below.

A. Estimand and nominal level

1. Confirm the intended Type-I error estimand and the operational definition of a rejection.
2. Confirm whether the nominal level is alpha = 0.05 for every declared scenario.
3. Identify any ambiguity between the theoretical target, the implemented endpoint, and the reported empirical rejection proportion.

B. Confidence bound and acceptance criterion

1. Recommend a binomial confidence-bound method, such as a one-sided Wilson score bound or a one-sided Clopper-Pearson exact bound, and justify the choice.
2. State the confidence level and explain why it is suitable for the intended decision.
3. Specify the proposed per-scenario acceptance rule mathematically.
4. Explain whether the criterion is intended to demonstrate compatibility with nominal alpha, control inflation above a tolerance, or satisfy another explicitly defined objective.
5. Do not adopt 0.055 or the historical 0.075 ceiling without an explicit prospective rationale.
6. State whether and how the overall decision across all nine scenarios accounts for multiplicity or joint acceptance.

C. Number of outer repetitions

1. Evaluate whether the proposed 2,000 repetitions per scenario are adequate for the selected acceptance rule.
2. Calculate or otherwise justify the operating characteristics of the proposed decision rule, including its probability of passing when the true Type-I error equals the nominal level.
3. If more repetitions are needed, justify the number before any formal outcomes are observed.
4. Distinguish a Monte Carlo standard-error target from the probability of satisfying the chosen confidence-bound acceptance criterion.

D. Surrogate count and numerical failures

1. Assess whether 1,000 requested surrogates per outer replicate provide adequate resolution and precision for the implemented p-value rule.
2. Specify the prospective treatment of failed fits, non-convergent trials, numerical failures, and surrogate shortfalls.
3. Define which attempts constitute valid statistical outcomes and how each category affects the denominator, uncertainty calculation, and scenario-level decision.
4. Require preservation of every requested attempt and its status. No silent deletion, selective replacement, or outcome-dependent denominator changes are permitted.
5. Specify whether an invalid attempt blocks a scenario, triggers a separately defined recovery procedure, or leads to another prospectively justified disposition.

E. Scenario coverage and applicability

1. Assess the nine declared scenarios and their parameterizations, including the near-boundary AR(1) scenario and both in-band resonant AR(2) scenarios.
2. Identify any additional stress scenarios that are necessary, with reasons. Any addition must be prospectively versioned before formal execution.
3. State clearly what conclusions the resulting calibration could and could not support.

4. Required response format

For each decision, provide:

- The recommendation.
- The statistical rationale.
- Any assumptions or limitations.
- The exact candidate commit and file hashes reviewed.
- The source files, tests, workflow logs, and artifacts actually inspected.
- Whether the recommendation applies to the exact reviewed snapshot or requires further changes and re-review.

Distinguish verified observations from mathematical derivations, recommendations, and unresolved matters.

5. Authorization safeguards

Until the acceptance rule and invalid-attempt policy have been resolved prospectively and the required review has been completed:

- Protocol freeze remains "NOT_FROZEN".
- Confirmatory execution remains "NOT_AUTHORIZED".
- Claim support remains "NOT_ESTABLISHED".
- Promotion authority remains "false".
- Engineering CI success and exploratory pilot completion do not change these states.
- No threshold may be adjusted after observing formal calibration outcomes.

6. Current disposition

"ACCEPTANCE_RULE_UNRESOLVED; PROSPECTIVE_STATISTICAL_DECISION_REQUESTED; PROTOCOL_NOT_FROZEN; CONFIRMATORY_EXECUTION_NOT_AUTHORIZED; CLAIM_NOT_ESTABLISHED"

### Supplementary prospective operating-characteristic analysis — V4

## Status: ILLUSTRATIVE AUDIT ONLY — NO ACCEPTANCE RULE APPROVED

## Purpose

This section records a prospective operating-characteristic calculation to inform independent statistical review. It does not select an acceptance threshold, freeze the protocol, authorize confirmatory execution, or support the HCM claim.

## Illustrative calculation

For illustration only, consider a one-sided 95% Wilson upper confidence bound, 2,000 requested outer repetitions, and a true rejection probability of 0.05. Under an independent Bernoulli model, the approximate probability that one scenario satisfies the upper-bound criterion is:

Candidate upper limit| Maximum accepted rejection count| Pass probability when true p = 0.05
0.050| 83| 0.0423
0.055| 93| 0.2552
0.060| 102| 0.6067
0.075| 130| 0.9987

These values are illustrative calculations for the stated Wilson rule. They do not approve any listed limit. They do not establish operating characteristics for the final protocol until the confidence-bound method, acceptance objective, scenario-level rule, and repetition count have been prospectively selected and independently reviewed.

## Decisions still required

The independent reviewer must recommend and justify:

1. The estimand and operational rejection rule for each declared scenario.
2. The maximum tolerable Type-I error probability, including the scientific rationale for any tolerance above the nominal level of 0.05.
3. The confidence-bound method and confidence level.
4. The desired probability of accepting a suitably calibrated procedure and the probability of accepting a procedure whose rejection probability exceeds the chosen tolerance.
5. The outer repetition count required to achieve those operating characteristics, with computational feasibility documented.
6. The aggregate decision across the nine scenarios, including whether the intended conclusion is an intersection-union decision or requires simultaneous confidence coverage.
7. The treatment of invalid attempts, failed fits, and surrogate shortfalls, preserving all requested attempts and the requested denominator.

## Safeguards

- The historical 0.075 ceiling remains NOT_JUSTIFIED_OR_APPROVED.
- No listed illustrative threshold is adopted by this section.
- No threshold may be changed after formal calibration outcomes are observed.
- The V4 candidate remains NOT_FROZEN.
- Confirmatory execution remains NOT_AUTHORIZED.
- Claim support remains false and promotion authority remains false.

## Disposition:

PROSPECTIVE_OPERATING_CHARACTERISTICS_ILLUSTRATED; ACCEPTANCE_RULE_UNRESOLVED; INDEPENDENT_STATISTICAL_DECISION_REQUIRED.
