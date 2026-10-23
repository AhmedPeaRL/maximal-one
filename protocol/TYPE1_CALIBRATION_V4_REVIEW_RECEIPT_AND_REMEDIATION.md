# Type-I Calibration V4 — Review Receipt and Remediation Record

## 1. Purpose and scope

This record documents receipt of a statistical review report dated 2026-10-23 concerning the proposed Type-I Calibration V4 protocol.

It distinguishes the conclusions stated in the received report from facts independently verifiable from repository records.

This record is not a statistical approval, protocol freeze, calibration result, or authorization for confirmatory execution.

## 2. Review target

Repository: https://github.com/AhmedPeaRL/maximal-one

Review branch: `review/type1-v4-remediation`

Candidate commit:
`9fafec47afbaaed8dfbe31b4f4e53f2ff3a99b83`

Candidate matrix:
`protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json`

Design draft:
`protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_DRAFT.json`

Full-path engineering workflow:
https://github.com/AhmedPeaRL/maximal-one/actions/runs/39871127641

Exploratory runtime pilot:
https://github.com/AhmedPeaRL/maximal-one/actions/runs/39871345141

## 3. Attribution and evidence limitations

The received report states that it was prepared by an independent statistical-methods expert and gives a review date of 2026-10-23 UTC.

In the copy received for this record, the following items are not sufficiently documented to permit independent verification of reviewer attribution:

- The reviewer's name and verifiable professional identity.
- Specific qualifications or relevant statistical-methods experience.
- A signature or other verifiable attribution.
- SHA-256 hashes of the reviewed files.
- A sufficiently detailed inventory of the exact source files, logs, and artifact contents actually inspected.

The report identifies a candidate commit and workflow run identifiers. These identifiers aid traceability but do not, by themselves, establish reviewer identity or prove that every stated technical conclusion was independently verified.

This limitation does not establish that the report is false. It means that the report must not yet be represented as a fully attributable, independently verified approval.

## 4. Reported disposition

The received report states:

`REVISE_AND_RESUBMIT`

Its stated scope is limited to engineering and methodological observations. It explicitly does not establish final Type-I error control, real-domain replication, HCM claim support, or authorization for confirmatory execution.

The disposition is recorded as received, not as an independently validated scientific conclusion.

## 5. Current authorization state

- Protocol freeze state: `NOT_FROZEN`
- Candidate approval status: `NOT_APPROVED`
- Confirmatory execution: `NOT_AUTHORIZED`
- Claim status: `NOT_ESTABLISHED`
- Claim support: `false`
- Promotion authority: `false`

No workflow success, pilot completion, or review-receipt record may automatically change these states.

## 6. Required remediation before prospective freeze

### A. Attributable independent review

Obtain a review that identifies the reviewer and relevant expertise, states the UTC review date, identifies the exact reviewed commit and file hashes, lists the materials actually inspected, and provides reasoned responses to the required review questions.

The reviewer must explicitly address whether the existing review remains applicable to the exact snapshot being considered.

### B. Prespecified Type-I acceptance rule

Before formal execution, document and justify:

- The nominal Type-I error level.
- The confidence-interval method and confidence level.
- Whether the acceptance bound is one-sided or two-sided.
- The per-scenario acceptance rule and its statistical rationale.
- The precision objective and justification for the number of outer repetitions.
- The treatment of any multiplicity or aggregate decision across scenarios, if applicable.

No threshold may be changed after observing calibration outcomes.

The historical `0.075` ceiling remains `NOT_JUSTIFIED_OR_APPROVED` unless a prospective, attributable review explicitly justifies and approves its intended role.

A proposed alternative such as `0.055` is not adopted by this record.

### C. Invalid attempts and denominator integrity

The protocol and implementation must preserve an auditable record for every requested outer replicate and every requested surrogate attempt, including failures and reasons.

Before execution, explicitly define how invalid attempts, failed model fits, and surrogate shortfalls affect validity, denominators, uncertainty calculations, and pass/fail decisions.

An invalid attempt must not be silently deleted, replaced, or reclassified as an ordinary statistical rejection or non-rejection.

The rule for blocking a scenario or the entire calibration must be specified prospectively and tested.

### D. Scenario coverage and implementation validity

The reviewer must assess the mathematical parameterization and stability of all declared scenarios, the intended endpoint, the surrogate p-value calculation, the null-model fitting procedure, and the reproducibility requirements.

Any additional scenarios, including heavy-tailed innovations or other stress conditions, must be separately justified and prospectively versioned before inclusion. They must not be added silently to the existing matrix.

### E. Engineering evidence

Inspect the actual workflow logs and retained artifacts for the exact snapshot under review. Passing engineering tests is evidence only for the checks those tests actually perform; it is not a substitute for statistical calibration or independent review.

## 7. Change-control safeguards

- Keep `main` unchanged during this remediation stage.
- Make remediation changes on `review/type1-v4-remediation` only.
- Do not freeze the protocol based solely on this received report.
- Do not authorize confirmatory execution based solely on CI success or a pilot.
- Do not change acceptance criteria after observing results.
- Preserve exact commit, source, dependency, workflow, and artifact identities.
- Re-review any material protocol or implementation change against its exact resulting snapshot.
- Do not promote the HCM claim from synthetic calibration alone.

## 8. Current disposition

`REVIEW_REPORT_RECEIVED; ATTRIBUTION_NOT_YET_VERIFIED; REVISE_AND_RESUBMIT; PROTOCOL_NOT_FROZEN; CONFIRMATORY_EXECUTION_NOT_AUTHORIZED; CLAIM_NOT_ESTABLISHED`
