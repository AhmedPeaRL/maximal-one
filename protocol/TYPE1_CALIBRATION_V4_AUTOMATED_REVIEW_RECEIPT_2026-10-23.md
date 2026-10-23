Type-I Calibration V4 — Automated Review Receipt and Open Decisions

Record date: 2026-10-23
Repository: "AhmedPeaRL/maximal-one"
Branch: "review/type1-v4-remediation"
Review snapshot claimed by the automated reviewer: "905c085bbe2f197c7ef0f85258432203cdeffa8a"
Automated review disposition: "REVISE_AND_RESUBMIT"
Human independent statistical review: "NOT_ESTABLISHED"

1. Purpose and evidentiary status

This record preserves an automated methodological review attributed to Claude, an AI model made by Anthropic, and identifies the decisions and engineering issues that remain unresolved.

The received report is not an attributable independent human statistical review. It does not authorize protocol freeze, confirmatory execution, scientific claim support, or promotion.

The reviewer reported that it did not execute the repository calibration code, inspect workflow logs, or independently establish that the uploaded archive exactly matches the claimed Git commit. Its findings must therefore be interpreted within those stated limits.

The uploaded archive was reported to have:

- Size: 1,557,440 bytes
- Entry count: 1,158, including directories
- Archive SHA-256: "b92078c8384d7221811ec52500318a5ad851bb4ae2e29f85f23fef1c972f526d"
- Embedded commit identifier: "905c085bbe2f197c7ef0f85258432203cdeffa8a"

These are values reported by the automated reviewer. The archive-to-commit correspondence has not been independently established by this record.

2. Required status invariants

Until the acceptance rule, failure policy, implementation consistency, and independent review have been resolved prospectively:

- Protocol freeze: "NOT_FROZEN"
- Confirmatory execution: "NOT_AUTHORIZED"
- Claim support: "NOT_ESTABLISHED"
- Promotion authority: "false"
- Human independent statistical review: "NOT_ESTABLISHED"

No automated review, engineering CI result, pilot output, or documentation commit may change these states by itself.

3. Principal findings reported by the automated review

The following findings are preserved as reported observations or calculations, not as an assertion that every repository detail was independently reproduced here.

3.1 Snapshot and matrix identity

The report identified inconsistent commit references across the candidate matrix, the decision request, and the reviewed snapshot. It also identified two matrix files used by different execution paths:

- "protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_DRAFT.json"
- "protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json"

The report states that the scenario definitions match while their status fields and hashes differ.

Required resolution: designate one authoritative prospective design source, define how every runner and test binds to it, and record exact source hashes and the reviewed commit. Do not imply that a file can establish its own containing commit identity.

3.2 Acceptance rule and operating characteristics

The report confirms that the acceptance rule remains unresolved and that the current gate fails closed when the rule is unset.

It also reports that the probability of passing an upper-confidence-bound rule depends on the true rejection probability, the confidence-bound method, the proposed ceiling, and the number of outer repetitions.

The report specifically rejects the claim that a one-sided 95% Wilson upper-bound rule with "R = 2000" would pass with probability greater than 0.90 when the true rejection probability is 0.05 and the acceptance ceiling is 0.05.

Required resolution: define the scientific objective of the acceptance criterion before choosing its threshold. Produce a reproducible operating-characteristic table for the final proposed rule before formal execution.

No value of "delta", no confidence-bound method, and no final repetition count is approved by this receipt.

3.3 Estimand and interpretation

The intended calibration target must be defined for the complete implemented procedure, including data generation, endpoint estimation, null fitting, surrogate generation, model-order selection, and the operational rejection rule.

The conclusions must remain restricted to the declared synthetic scenarios and the exact implementation evaluated.

A successful synthetic calibration would not, by itself, establish adequacy of the null model for real data, independent real-domain replication, or support for any broader HCM claim.

3.4 Attempt preservation and failure handling

The report identified a potential information-loss issue: some invalid or shortfall attempts may not preserve all requested statistics, including exceedance counts and p-values.

Required resolution: preserve one auditable record for every requested attempt, including its seed identity, status, failure reason, observed statistic when available, exceedance count, valid-surrogate count, and relevant hashes.

The prospective policy must specify how invalid outer attempts and surrogate failures affect the scenario decision. No silent deletion, selective replacement, or outcome-dependent denominator changes are permitted.

Any change to the failure policy must be reviewed and versioned before confirmatory execution.

3.5 Surrogate count and numerical reliability

The report identifies a distinction between the minimum valid-surrogate count accepted by a lower-level function and the stricter requirement imposed by the runner.

Required resolution: state the operational rule once in the protocol and ensure that implementation, tests, output fields, and documentation agree.

The surrogate count must be justified for the intended procedure. Its numerical resolution alone does not establish calibration adequacy.

3.6 Joint decision across scenarios

The report recommends explicitly defining the aggregate rule across all nine scenarios and distinguishing a joint intersection-union decision from simultaneous confidence-interval coverage.

Required resolution: the independent reviewer must justify the chosen aggregate decision and any multiplicity treatment. The final rule must be implemented and tested as written before execution.

3.7 Scope of the conclusion

Any future calibration conclusion must state the exact scenarios, sample size, null-fitting procedure, endpoint, surrogate count, rejection rule, and uncertainty criterion to which it applies.

It must not be generalized to untested data-generating processes, other sample sizes, real-domain null adequacy, power, or HCM claim support without separate evidence.

4. Open decision register

ID| Decision required| Current status
D-01| Define the estimand and operational rejection rule| OPEN
D-02| Select and justify the acceptance objective and tolerated inflation "delta"| OPEN
D-03| Select the confidence-bound method and confidence level| OPEN
D-04| Determine "R" from prospective operating characteristics and a declared feasibility budget| OPEN
D-05| Set the surrogate count and shortfall policy| OPEN
D-06| Define invalid-attempt handling and any engineering-derived failure tolerance| OPEN
D-07| Establish one authoritative design matrix and consistent runner binding| OPEN
D-08| Define the aggregate decision across all nine scenarios| OPEN
D-09| Verify reproducibility, attempt preservation, checkpointing, and merge behavior| OPEN
D-10| Obtain an attributable independent human statistical review| OPEN
D-11| Re-review the exact amended snapshot and file hashes| OPEN

No open item is deemed resolved merely because this register records it.

5. Required next sequence

1. Preserve the current remediation branch and do not merge these changes into "main" as an approval.
2. Obtain a reasoned independent human statistical review, including the reviewer's relevant qualifications and the exact materials inspected.
3. Resolve the estimand, acceptance objective, operating characteristics, repetition count, aggregate decision, and failure policy prospectively.
4. Amend the protocol and implementation on the remediation branch only.
5. Test that the implementation, tests, output schema, and authoritative matrix agree.
6. Record exact commit identity, file-content SHA-256 digests, and relevant workflow evidence.
7. Submit the amended snapshot for independent review.
8. Freeze and authorize execution only through a separate, explicit, attributable decision after all prerequisites are satisfied.

6. Provenance and limits

This record documents receipt and triage of automated feedback. It does not certify that the repository code was executed, that the full archive was independently inspected, or that all reported computations were independently reproduced.

Any amended source, protocol, matrix, dependency lock, test, or workflow must be hashed and reviewed against the exact snapshot to which the subsequent decision applies.

Current disposition:

"AUTOMATED_REVIEW_RECEIVED"

"REVISE_AND_RESUBMIT"

"ACCEPTANCE_RULE_UNRESOLVED"

"PROTOCOL_NOT_FROZEN"

"CONFIRMATORY_EXECUTION_NOT_AUTHORIZED"

"HUMAN_INDEPENDENT_REVIEW_NOT_ESTABLISHED"

"CLAIM_NOT_ESTABLISHED"

"PROMOTION_AUTHORITY_FALSE"
