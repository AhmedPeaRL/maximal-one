# V4 Type-I Acceptance Rule — Prospective Decision Record

Status: "OPEN — NO ACCEPTANCE RULE APPROVED"

Protocol: "HCM_TYPE1_CALIBRATION_V4_CANDIDATE"

Branch: "review/type1-v4-remediation"

1. Purpose

This record resolves the acceptance-rule specification prospectively, before any authorized confirmatory execution.

It does not reinterpret, overwrite, or retroactively reclassify historical results.

A successful engineering workflow is not a statistical acceptance decision.

2. Historical rule — preserved, not silently amended

The historical review record used a two-sided 95% Wilson interval and required:

1. The interval to contain the nominal rate 0.05.
2. The upper endpoint not to exceed 0.075.
3. Every required scenario to satisfy the stated suite-level rule.

The historical V1 result was recorded as "NOT_PASSED":

- AR1: 52/1000; interval [0.039873, 0.067556]; passed the historical per-scenario rule.
- AR2: 60/1000; interval [0.046896, 0.076471]; failed the historical per-scenario rule.
- AR5: 49/1000; interval [0.030..., 0.064...] — verify exact endpoints from the original immutable result record before reproducing this interval.
- AR10: 73/1000; interval [0.058459, 0.090809]; failed the historical per-scenario rule.

The overall historical outcome remains "NOT_PASSED". Do not replace original result files or change the historical rule retrospectively.

3. Conflicting candidate rule

A later candidate proposed a one-sided 95% Wilson upper bound no greater than 0.075.

This is not equivalent to the historical two-sided rule. The 0.075 ceiling is not approved merely because it appears in a draft.

No candidate rule is approved by this record.

4. Decision options for prospective review

The independent reviewer must assess the options below and may recommend another explicitly specified rule with justification.

Option A — Retain the historical rule for future confirmatory work

Require a two-sided 95% Wilson interval to contain 0.05 and its upper endpoint to be no greater than a justified boundary.

The reviewer must determine whether 0.075 is statistically and scientifically justified; its historical presence alone is not sufficient.

Option B — Adopt a one-sided upper-bound rule

Specify a one-sided confidence level and a justified upper acceptance boundary prospectively. Explain why the nominal rate, confidence level, boundary, outer repetition count, and Monte Carlo precision are appropriate.

Do not assume that 0.075 is justified.

Option C — Recommend a different rule

Define the estimand, interval or test, confidence level, numerical boundary, suite-level decision, invalid-attempt treatment, and multiplicity handling in full. Provide a rationale before confirmatory execution.

5. Mandatory statistical questions

The reviewer must document:

- The estimand and precise definition of a Type-I error for this pipeline.
- Whether the criterion targets calibration per scenario or a suite-level guarantee.
- Why the selected confidence procedure and boundary are justified.
- Expected Monte Carlo precision at the planned number of outer repetitions.
- The effect of invalid attempts, missing outputs, and unresolved surrogate shortfalls.
- The denominator policy, including whether every requested outer attempt remains in N.
- How multiple required scenarios jointly determine the suite result.
- Whether the proposed null models and endpoint implementation are appropriate for the stated claim.
- Any limitations, sensitivities, or conditions that prevent approval.

6. Historical-result protection

The decision applies prospectively only to a protocol snapshot identified by commit SHA and content hashes.

Historical results retain the acceptance rule, data, code, and interpretation that were actually used at the time.

Any retrospective re-analysis must be labeled as a new analysis, preserve the original results, identify its new rule and rationale, and must not be presented as the original predeclared test.

No backdating is permitted.

7. Required reviewer attribution

Reviewer name: "NOT PROVIDED"

Relevant statistical expertise: "NOT PROVIDED"

Affiliation or independent status: "NOT PROVIDED"

Conflicts of interest: "NOT PROVIDED"

Reviewed protocol commit SHA: "NOT PROVIDED"

Review date: "NOT PROVIDED"

Recommendation: "PENDING"

Rationale and limitations: "PENDING"

Signature or attributable written confirmation: "PENDING"

AI-generated analysis is not independent human statistical approval.

8. Decision and authorization

Approved prospective acceptance rule: "NONE"

Effective protocol commit SHA: "NONE"

Effective matrix SHA-256: "NONE"

Effective runner SHA-256: "NONE"

Formal execution authorization: "NOT GRANTED"

Protocol freeze: "NOT APPROVED"

"confirmatory_execution_authorized = false"

"claim_support = false"

"promotion_authority = false"

This record may be marked approved only after an attributable independent statistical review and explicit governance decision. A subsequent formal execution requires its own separate authorization record.
