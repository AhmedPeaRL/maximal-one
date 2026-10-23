Type-I Calibration V4 — Automated Report Technical Adjudication

1. Purpose and status

This record evaluates the methodological recommendations received on 2026-10-23 concerning the proposed Type-I Calibration V4 protocol.

This is an automated technical adjudication, not an attributable independent human statistical review. It does not approve, freeze, or authorize the protocol.

Repository: "AhmedPeaRL/maximal-one"

Remediation branch: "review/type1-v4-remediation"

Candidate review base cited in the received report: "9fafec47afbaaed8dfbe31b4f4e53f2ff3a99b83"

Current protocol status: "NOT_FROZEN"

Confirmatory execution: "NOT_AUTHORIZED"

Claim support: "NOT_ESTABLISHED"

Promotion authority: "false"

2. Materials considered

The following repository records were inspected on the remediation branch:

- "protocol/TYPE1_CALIBRATION_V4_ACCEPTANCE_RULE_DECISION_REQUEST.md"
- "protocol/TYPE1_CALIBRATION_V4_REVIEW_RECEIPT_AND_REMEDIATION.md"
- "protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json"
- "protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_DRAFT.json"

The candidate matrix and design draft remain unapproved. The acceptance rule is unresolved. The cited workflow and pilot identifiers are traceability references; their existence or success does not establish statistical calibration.

The file-level Git blob identifiers observed during this inspection are not SHA-256 file-content digests. No independent claim is made here that the full workflow artifacts or every underlying implementation detail have been exhaustively inspected.

3. Findings requiring correction or clarification

A. Operating characteristic of the proposed acceptance rule

The received report states that, when the true Type-I error equals 0.05, the probability of passing the proposed upper-confidence-bound acceptance rule would be high, for example greater than 0.90.

That statement is unsupported and is incorrect for the proposed one-sided 95% Wilson upper-bound rule with the candidate repetition count.

For a fixed sample size of R = 2000 independent Bernoulli rejection outcomes and a true rejection probability of 0.05:

- The Monte Carlo standard error of the empirical rejection proportion is approximately 0.00487.
- Under the one-sided 95% Wilson rule, the probability that the upper bound is at most 0.05 is approximately 4.2%.
- Under the one-sided 95% Wilson rule, the probability that the upper bound is at most 0.055 is approximately 25.5%.

These are binomial operating-characteristic calculations for the specified rules, not results from running the repository's calibration implementation.

The report must not equate a Monte Carlo standard-error target with a high probability of passing a confidence-bound acceptance rule. Before formal execution, the selected acceptance rule must have its operating characteristics evaluated under relevant true rejection probabilities, including the nominal value and scientifically justified inflation values.

B. Acceptance ceiling and inferential objective

Neither 0.055 nor the historical 0.075 ceiling is adopted by this record.

Before freeze, the protocol must explicitly state whether its objective is:

1. Demonstrating that the upper confidence bound is no greater than the nominal level;
2. Demonstrating that the rejection probability is below a prospectively justified tolerance above the nominal level; or
3. Satisfying another explicitly defined statistical decision objective.

The selected objective, tolerance, confidence level, confidence-bound method, repetition count, and pass/fail rule must be justified and versioned before formal outcomes are observed.

C. Multiple scenarios and the aggregate decision

The report recommends a multiplicity adjustment for the nine scenarios but does not fully specify the inferential target.

Before selecting an adjustment, the protocol must define whether it requires simultaneous confidence coverage across scenarios, a joint acceptance decision, or another aggregate property. If simultaneous confidence coverage is required, a prospective method such as Bonferroni may be considered; any chosen method must be justified and implemented consistently.

The scenarios must not be described as statistically independent unless that property has been established for the relevant simulation design and decision procedure.

D. Invalid attempts and denominator integrity

Every requested outer replicate and surrogate attempt must remain auditable, including its identity, status, and failure reason.

The protocol must distinguish at least:

- Valid statistical rejection;
- Valid statistical non-rejection;
- Invalid or non-convergent outer replicate;
- Surrogate generation, fitting, or numerical failure;
- Unresolved surrogate shortfall.

A failed attempt must not automatically be classified as an ordinary rejection or non-rejection. Its effect on denominators, uncertainty estimates, scenario validity, and the overall decision must be specified prospectively.

No silent deletion, selective replacement, or outcome-dependent denominator change is permitted. Any recovery procedure must be defined and tested before formal execution.

E. Surrogate count and endpoint validity

A requested surrogate count of 1000 offers nominal p-value resolution on the order of 0.001 under the candidate plus-one p-value rule. That resolution alone does not establish that the count is adequate for the full calibration objective.

Adequacy depends on the implemented p-value rule, null-model fitting and selection, numerical stability, valid surrogate count, and the desired operating characteristics of the complete procedure. These must be assessed before freeze.

F. Scenario coverage

The nine current scenarios must remain unchanged unless a separately documented prospective amendment is reviewed and approved.

Heavy-tailed innovations, heteroskedasticity, structural breaks, irregular sampling, and other stress conditions may be useful extensions, but they are not automatically required additions to the current primary matrix. Their inclusion and intended inferential scope must be justified before execution.

4. Required next review

An attributable independent human statistical reviewer should receive the exact candidate snapshot and the relevant source files, implementation, tests, workflow logs, and retained artifacts.

The reviewer should provide:

- Verifiable identity and relevant qualifications;
- Review date in UTC;
- Exact reviewed commit and file-level SHA-256 digests;
- An explicit inventory of the materials actually inspected;
- A reasoned decision on the acceptance rule and its operating characteristics;
- A decision on the aggregate scenario criterion and multiplicity, if applicable;
- A prospective policy for invalid attempts and surrogate shortfalls;
- A clear statement of whether the recommendations apply to the exact reviewed snapshot or require another revision.

Automated feedback may inform this process but must not be represented as human independent review.

5. Authorization safeguards

Until the statistical decision rule and invalid-attempt policy are resolved prospectively and the required review is completed:

- Protocol freeze remains "NOT_FROZEN".
- Confirmatory execution remains "NOT_AUTHORIZED".
- Claim support remains "NOT_ESTABLISHED".
- Promotion authority remains "false".
- Engineering workflow success and exploratory pilot completion do not alter these states.
- Acceptance thresholds must not be changed after formal outcomes are observed.
- "main" remains unchanged during this remediation stage.

6. Disposition

"AUTOMATED_REPORT_TECHNICAL_ADJUDICATION_RECORDED; OPERATING_CHARACTERISTIC_CLAIM_REQUIRES_CORRECTION; ACCEPTANCE_RULE_UNRESOLVED; HUMAN_INDEPENDENT_REVIEW_NOT_ESTABLISHED; PROTOCOL_NOT_FROZEN; CONFIRMATORY_EXECUTION_NOT_AUTHORIZED; CLAIM_NOT_ESTABLISHED"
