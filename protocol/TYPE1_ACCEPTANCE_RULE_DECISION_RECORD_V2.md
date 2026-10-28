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


## Addendum — 2026-10-29 — Prospective decision after engineering evidence

Decision ID: `HCM-TYPE1-V4-HOLD-2026-10-29`

Disposition: `HOLD_NO_ACCEPTANCE_RULE_APPROVED`

### Evidence considered

The CLI resume identity workflow run `40778431846` succeeded for
its recorded bounded engineering test.

This result concerns resume identity rejection and preservation of
checkpoint and manifest bytes. It does not determine the statistical
acceptance rule.

### Prospective governance decision

1. Preserve the historical two-sided Wilson rule and all historical
   result classifications unchanged.
2. Do not approve the candidate one-sided Wilson rule merely because
   it appears in a V3 or V4 draft.
3. Do not treat the historical `0.075` ceiling as scientifically
   justified without a prospective substantive rationale.
4. Require an attributable independent human statistical reviewer
   to select and justify one complete rule before formal execution.
5. Bind the future decision to the exact reviewed commit and hashes.
6. Require a separate authorization record after the approved
   protocol is frozen.
7. Do not backdate the decision or reclassify historical failures
   under the future rule.

### Required content of the independent review

The reviewer must document:

- target estimand and nominal Type-I error rate;
- interval sidedness and confidence level;
- numerical acceptance boundary and substantive rationale;
- outer repetition count and Monte Carlo operating characteristics;
- scenario-level and suite-level acceptance requirements;
- invalid-attempt policy and preservation of the requested denominator;
- treatment of missing results and surrogate shortfalls;
- reviewer identity, relevant expertise, independence, conflicts,
  date, reviewed commit, and protocol hashes;
- explicit recommendation, rationale, limitations, and disposition.

### Current authorization state

- Approved V4 acceptance rule: `NONE`
- V4 freeze state: `NOT_FROZEN`
- Confirmatory execution authorized: `false`
- Claim support: `false`
- Promotion authority: `false`
- Formal calibration: `NOT AUTHORIZED`

This addendum is a governance hold, not a substitute for the
independent statistical review and not an authorization to execute.
