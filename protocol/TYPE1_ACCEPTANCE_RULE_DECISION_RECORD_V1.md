# Type-I Acceptance Rule Decision Record V1

**Record status:** OPEN — PROSPECTIVE DECISION REQUIRED  
**Protocol:** HCM_TYPE1_CALIBRATION_V4_CANDIDATE  
**Branch:** review/type1-v4-remediation  
**Freeze state:** NOT_FROZEN  
**Confirmatory execution authorized:** false  
**Claim support:** false  
**Promotion authority:** false  

## 1. Purpose

This record prevents retrospective reinterpretation of historical
Type-I calibration results and establishes the mandatory decision gate
for any future confirmatory V4 execution.

This document is a governance record. It is not an independent
statistical approval and does not authorize execution.

## 2. Historical rule — preserve as recorded

The previously recorded historical rule required both:

1. The two-sided 95% Wilson confidence interval to contain nominal
   Type-I error 0.05.
2. The upper endpoint of that interval to be no greater than 0.075.

Historical results and their original pass/fail labels must remain
preserved under the rule that was applied when those results were
reported.

No historical result may be relabelled as a pass by applying a new
rule retrospectively. Any later sensitivity analysis must be labelled
as a separate re-analysis and must retain the original decision.

## 3. Alternative V4 proposal — not approved

A different proposal has been discussed:

- Use the one-sided 95% Wilson upper confidence bound.
- Require that bound to be no greater than 0.075.

This is not equivalent to the historical two-sided rule. The numerical
boundary, confidence-tail convention, and decision logic must not be
treated as interchangeable.

The value 0.075 has not been justified or approved in the current V4
candidate matrix. It must not become an operative acceptance boundary
merely because it appears in prior draft code or documentation.

## 4. Required prospective human review

Before protocol freeze, an attributable independent human statistical
reviewer must provide a dated, signed or otherwise attributable
decision that records:

1. The target estimand and the meaning of a Type-I error in this design.
2. The selected confidence-bound convention and exact acceptance rule.
3. The scientific rationale for the numerical acceptance boundary.
4. The planned outer-repetition count and expected Monte Carlo precision.
5. The treatment of invalid attempts and the denominator used.
6. The multiplicity policy across the required scenario family.
7. Whether any historical results are being re-analysed, clearly
   separated from the original historical decisions.
8. The exact reviewed commit and SHA-256 hashes of the reviewed
   protocol, matrix, runner, dependency lock, and workflow.
9. The reviewer's relevant expertise, conflicts of interest, date,
   and explicit approval or rejection.

AI-assisted analysis may support the review but must not be represented
as independent human approval.

## 5. Prospective decision options for reviewer disposition

The reviewer must select and justify one option. No option is selected
or approved by this draft.

- OPTION A: Retain the historical two-part Wilson rule for the future
  V4 protocol, subject to explicit scientific justification and review.
- OPTION B: Adopt a one-sided upper-bound rule for future V4 execution,
  with a prospectively justified boundary and confidence level.
- OPTION C: Reject both candidates and specify a different rule with
  a complete rationale.

The reviewer must state why the chosen rule controls the intended
error-rate risk and why the rejected alternatives are unsuitable.

## 6. Freeze and execution gate

The decision becomes operative only after all of the following:

- Attributable independent human review is recorded.
- The chosen rule is encoded consistently in the protocol, matrix,
  implementation, tests, and workflow.
- The historical-results record is preserved unchanged.
- Tests verify that the implementation follows the selected rule.
- The reviewed files and exact commit are identified.
- A separate, explicit authorization is recorded for confirmatory
  execution.

Until then:

- `acceptance_rule = null` in the candidate matrix remains unresolved.
- `freeze_state = NOT_FROZEN`.
- `confirmatory_execution_authorized = false`.
- `claim_support = false`.
- `promotion_authority = false`.
- Formal Type-I calibration remains NOT AUTHORIZED.

## 7. Prohibited actions

- No retrospective threshold change to obtain a pass.
- No silent replacement of historical results or pass/fail labels.
- No conversion of missing or invalid attempts into successful attempts.
- No protocol freeze or confirmatory execution based solely on a
  successful engineering workflow.
- No representation of AI output as independent human approval.

## 8. Decision record — intentionally pending

**Selected option:** NONE — PENDING INDEPENDENT HUMAN REVIEW  
**Reviewer:** NOT YET RECORDED  
**Review date (UTC):** NOT YET RECORDED  
**Reviewed commit:** NOT YET RECORDED  
**Reviewed file hashes:** NOT YET RECORDED  
**Approval status:** NOT APPROVED  
**Effective date:** NONE  

This record documents the conflict and blocks premature execution.
It does not claim that the scientific acceptance-rule question has
already been resolved.
