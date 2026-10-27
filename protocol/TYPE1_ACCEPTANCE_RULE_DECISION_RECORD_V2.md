# Type-I Acceptance Rule Decision Record V2

Date opened: 2026-10-27

Status: UNRESOLVED — NO ACCEPTANCE RULE APPROVED

Repository:
`AhmedPeaRL/maximal-one`

Branch:
`review/type1-v4-remediation`

## 1. Purpose

This record prevents retrospective reinterpretation of historical
Type-I calibration results and requires a prospective decision before
any confirmatory execution.

## 2. Historical rule — preserve unchanged

The historical rule required both:

1. The two-sided 95% Wilson interval to contain nominal alpha 0.05.
2. The upper endpoint of that interval to be no greater than 0.075.

Historical results must retain their original classifications under
the rule used at the time. This record does not rewrite or replace
those classifications.

## 3. Proposed alternative — not approved

A later candidate proposed:

- One-sided 95% Wilson upper confidence bound.
- Upper-bound ceiling: 0.075.
- Every required scenario must satisfy the criterion.

This proposal is not approved by this record. The ceiling of 0.075
has not received the required attributable independent statistical
justification.

## 4. Current V4 state

- Protocol status: DRAFT_PENDING_REMEDIATION_AND_INDEPENDENT_REVIEW
- Freeze state: NOT_FROZEN
- Acceptance rule: UNRESOLVED
- Confirmatory execution authorized: false
- Claim support: false
- Promotion authority: false

## 5. Required prospective decision

Before any confirmatory run, an attributable independent human
statistical reviewer must document:

1. The target estimand and nominal error rate.
2. Whether the decision uses a two-sided interval, a one-sided
   upper bound, or another prospectively justified rule.
3. The substantive rationale for any tolerance above nominal alpha.
4. The confidence level and planned number of outer repetitions.
5. The treatment of invalid attempts and incomplete scenarios.
6. Multiplicity and the suite-level acceptance rule.
7. Monte Carlo precision and the consequences of false acceptance
   and false rejection.
8. The exact reviewed commit SHA and protocol content hashes.
9. The reviewer's expertise, conflicts of interest, decision, date,
   and rationale.

The reviewer must decide prospectively. No rule may be selected or
changed solely because it makes already observed results pass.

## 6. Decision record — intentionally pending

Reviewer name:
[NOT PROVIDED]

Relevant statistical expertise:
[PENDING]

Conflicts of interest:
[PENDING]

Reviewed commit SHA:
[PENDING]

Selected rule and rationale:
[PENDING]

Decision:
NOT DECIDED

Date:
[PENDING]

## 7. Execution gate

Until the decision is attributable, documented, accepted through
the project's governance process, and incorporated into a reviewed
protocol snapshot:

- Keep V4 NOT_FROZEN.
- Keep confirmatory_execution_authorized=false.
- Keep claim_support=false.
- Keep promotion_authority=false.
- Do not run formal confirmatory calibration.

This record does not authorize execution and does not alter any
historical result.
