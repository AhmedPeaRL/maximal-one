# Independent Statistical Review Request — HCM Type-I Calibration V4

## 1. Purpose

This request seeks an attributable, independent statistical-methods review of the proposed V4 calibration protocol before any confirmatory execution.

This is a review request, not an assertion that the protocol is valid, approved, frozen, or authorized.

## 2. Repository and review identity

- Repository: https://github.com/AhmedPeaRL/maximal-one
- Review branch: `review/type1-v4-remediation`
- Candidate matrix: `protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json`
- Candidate protocol status: `DRAFT_PENDING_REMEDIATION_AND_INDEPENDENT_REVIEW`
- Freeze state: `NOT_FROZEN`
- Confirmatory execution authorized: `false`
- Claim support: `false`
- Promotion authority: `false`

The reviewer must record the exact commit SHA and the SHA-256 digest of the candidate matrix and any other reviewed protocol inputs. A branch name alone is not an adequate immutable review identity.

## 3. Engineering evidence available

The following engineering records are available for inspection:

- Official-runner engineering workflow:  
  https://github.com/AhmedPeaRL/maximal-one/actions/runs/40802655822
- Governance inventory workflow:  
  https://github.com/AhmedPeaRL/maximal-one/actions/runs/40802782354
- Worker-assignment matrix audit:  
  https://github.com/AhmedPeaRL/maximal-one/actions/runs/40768558101
- Cross-runner worker-order comparison:  
  https://github.com/AhmedPeaRL/maximal-one/actions/runs/40585881668
- CLI resume identity rejection tests:  
  https://github.com/AhmedPeaRL/maximal-one/actions/runs/40783850430

These records concern engineering behavior and reproducibility. They are not evidence that the scientific acceptance rule is correct or that Type-I calibration passed.

The reviewer should inspect the exact logs, manifests, relevant artifact payloads, and source files rather than relying only on workflow-level success labels.

## 4. Historical results and non-retroactivity

The historical V1 review used a two-sided 95% Wilson interval criterion: the interval had to contain nominal 0.05 and its upper endpoint had to be no greater than 0.075.

Historical recorded outcomes included:

- AR1: 52/1000; interval [0.039873, 0.067556]; pass under the historical rule.
- AR2: 60/1000; interval [0.046896, 0.076471]; fail under the historical rule.
- AR5: 49/1000; interval [0.036..., 0.0...]; consult the original archived report for the exact interval before citing it.
- AR10: 73/1000; interval [0.058459, 0.090809]; fail under the historical rule.

The original archived reports and exact recorded values are authoritative for historical reporting. Do not recalculate, relabel, omit, or reinterpret historical outcomes merely to make a later protocol pass.

If any historical value in this summary is incomplete, use the original archived report and record the correction as a transparent transcription correction without changing the historical decision.

## 5. Unresolved acceptance-rule conflict

The V4 draft has considered a one-sided 95% Wilson upper-bound rule of `<= 0.075`. This differs from the historical two-sided interval rule.

The `0.075` ceiling has not been established as independently justified or approved.

The reviewer must explicitly answer:

1. What is the exact primary estimand and what constitutes a Type-I error for this procedure?
2. Is the intended criterion a one-sided upper confidence bound, a two-sided interval criterion, or another prespecified criterion? Why?
3. What coverage level and numerical acceptance bound are justified by the scientific objective and operating characteristics?
4. How should multiplicity across required scenarios be handled?
5. Must every required scenario pass, and what is the justification?
6. How should Monte Carlo uncertainty and invalid or failed attempts affect the denominator and decision?
7. What operating-characteristic evidence supports the proposed rule before the confirmatory run?
8. What exact rule should govern future V4 execution, and how will it be frozen before any confirmatory result is observed?

No threshold or rule may be changed retrospectively to convert a historical failure into a pass.

## 6. Scenario and implementation review

The reviewer should examine:

- The statistical validity and stability of every declared scenario, including the proposed AR(2) coefficient combinations.
- The data-generating process, burn-in, sample size, and seed schedule.
- The endpoint estimator and the surrogate/null-generation implementation.
- The interpretation of valid surrogates, exceedances, Monte Carlo p-values, and failed attempts.
- Whether all nine candidate scenarios are justified and sufficient for the intended claim.
- Whether the design covers relevant failure modes, dependence structures, and boundary cases.
- Whether the proposed power scenarios and targets are adequate and prespecified.
- Whether any simulation or implementation choice could bias the acceptance decision.

The reviewer should distinguish mathematical/statistical objections from software engineering defects and specify a reproducible test or argument for each material finding.

## 7. Governance and execution safeguards

Before any confirmatory execution:

- The acceptance rule must be explicitly resolved and documented.
- The exact protocol and matrix must be versioned and frozen.
- The reviewed commit and all input digests must be recorded.
- The authorized runner must be bound to the approved protocol identity.
- Legacy V3 workflows and all execution-capable paths must be reviewed.
- No engineering-only flag or workflow may authorize formal calibration.
- No missing, invalid, duplicate, or failed attempt may be silently discarded or replaced.
- Claim-support and promotion-authority flags must remain false until their separately defined gates are met.

A successful CI run is not a substitute for independent statistical review.

## 8. Required reviewer disposition

The reviewer must select one:

- `APPROVE_WITH_EXPLICIT_RATIONALE`
- `REVISE_AND_RESUBMIT`
- `REJECT`
- `INSUFFICIENT_INFORMATION`

The reviewer must provide:

- Full name and professional affiliation.
- Relevant statistical-methods expertise.
- Conflict-of-interest declaration.
- Exact reviewed commit SHA.
- Exact reviewed matrix and protocol digests.
- Findings with file/line or evidence references.
- Decision on the acceptance-rule conflict.
- Required changes, if any.
- Explicit statement on whether the reviewed protocol is ready to be frozen.

An AI-generated assessment is not an attributable independent human statistical review.

## 9. Current decision

Until an attributable independent reviewer has issued a documented disposition and the resulting protocol changes have been reconciled:

- V4 remains `NOT_FROZEN`.
- Confirmatory execution remains `NOT_AUTHORIZED`.
- Claim support remains `false`.
- Promotion authority remains `false`.

No formal calibration run is requested or authorized by this document.
