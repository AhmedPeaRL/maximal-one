# Independent Human Statistical Review Request — Type-I V4

Status: REQUEST FOR REVIEW — NOT AN APPROVAL
Repository: AhmedPeaRL/maximal-one
Review branch: review/type1-v4-remediation

## 1. Purpose

An independent human statistical-methods review is requested
before any prospective protocol freeze or confirmatory
Type-I calibration execution.

The reviewer is asked to assess the statistical design,
acceptance rule, operating-characteristic plan, invalid-run
policy, and adequacy of the proposed evidence.

This request does not presume that the V4 proposal is valid
or that any previous engineering result establishes Type-I
error control.

## 2. Exact review materials

Target review commit:
PENDING — INSERT FINAL SNAPSHOT COMMIT

Snapshot artifact ID:
PENDING

Snapshot manifest SHA-256:
PENDING

SHA256SUMS file SHA-256:
PENDING

Governance inventory artifact ID:
PENDING

Governance inventory source commit:
PENDING

Manual classification ledger commit:
PENDING

V4 matrix path:
protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json

V4 matrix SHA-256:
PENDING

Acceptance-rule decision record:
PENDING — INSERT EXACT PATH AND HASH

Engineering evidence addendum:
protocol/TYPE1_ENGINEERING_EVIDENCE_ADDENDUM_2026-10-30.md

## 3. Reviewer identity and qualifications

Reviewer full name:
REQUIRED

Institution / independent affiliation:
REQUIRED

Highest relevant qualification:
REQUIRED

Relevant statistical expertise:
REQUIRED

Relevant publications or professional work:
REQUIRED

Experience with Monte Carlo calibration, surrogate testing,
time-series null models, or Type-I error control:
REQUIRED

Conflict-of-interest declaration:
REQUIRED

Prior involvement in this project:
REQUIRED

Financial, professional, personal, or intellectual conflicts:
REQUIRED

The reviewer must explicitly state whether they are independent
of the authors and the design decisions under review.

AI-generated analysis is not a substitute for this human review.

## 4. Questions requiring a documented decision

1. Is the estimand clearly defined?
2. Are all nine proposed null data-generating processes appropriate?
3. Are the AR parameterizations and stationarity conditions correct?
4. Is the proposed sample length and burn-in adequate?
5. Is the surrogate-generation and refitting procedure valid?
6. Is the add-one p-value definition appropriate?
7. Is the rejection rule correctly implemented?
8. Are invalid attempts and incomplete surrogate sets handled
   without bias or silent exclusion?
9. Is the proposed Monte Carlo precision adequate?
10. Is the acceptance rule justified prospectively?
11. Is the inherited 0.075 ceiling defensible?
12. Is the one-sided Wilson upper-bound proposal justified,
    or should the historical two-sided interval rule remain?
13. Are the power alternatives and targets scientifically justified?
14. What additional stress scenarios are required?
15. What evidence is still missing before confirmatory execution?

## 5. Historical results must remain visible

The historical two-sided Wilson assessment reported:

- AR1: 52/1000; interval [0.039873, 0.067556]
- AR2: 60/1000; interval [0.046896, 0.076471]
- AR5: 49/1000; interval [0.038..., 0.064...] 
- AR10: 73/1000; interval [0.058459, 0.090809]

The historical suite was NOT_PASSED.

The exact original result artifacts and full precision values
must be included in the review package. The abbreviated values
above are not a replacement for those artifacts.

No historical failure may be deleted or reclassified to make
the candidate protocol pass.

## 6. Required reviewer output

The reviewer must provide:

- Identity and qualifications.
- Independence and conflict declaration.
- Exact commit SHA reviewed.
- Exact matrix and protocol hashes reviewed.
- Exact evidence package and artifact IDs reviewed.
- Methods assessment.
- Acceptance-rule recommendation.
- Explicit limitations and unresolved issues.
- A reasoned decision:
  ACCEPT / ACCEPT WITH CONDITIONS / REVISE / REJECT.
- Whether any future confirmatory execution may be considered,
  and under which explicit conditions.
- Signature or other attributable confirmation.
- Review date.

A recommendation is not itself execution authorization.
A separate prospective governance decision is required.

## 7. Current authorization state

freeze_state = NOT_FROZEN
confirmatory_execution_authorized = false
claim_support = false
promotion_authority = false

No formal calibration is authorized by this request.
No scientific claim is approved by this request.
