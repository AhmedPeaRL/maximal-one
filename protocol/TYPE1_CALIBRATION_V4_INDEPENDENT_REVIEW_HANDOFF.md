# Type-I Calibration V4 — Independent Statistical Review Handoff

## 1. Purpose

This document requests an attributable, independent human statistical-methods review of the proposed Type-I calibration protocol before any confirmatory execution is authorized.

This is a review handoff, not an approval, protocol freeze, calibration result, or claim-promotion record.

## 2. Exact review target

Repository: https://github.com/AhmedPeaRL/maximal-one

Review branch: `review/type1-v4-remediation`

Candidate commit:
`9fafec47afbaaed8dfbe31b4f4e53f2ff3a99b83`

Candidate matrix:
`protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json`

Design draft:
`protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_DRAFT.json`

The reviewer must independently verify the exact commit and file contents before issuing a decision. Any later change to the protocol, implementation, dependency lock, or workflow requires an explicit determination of whether the review remains applicable.

## 3. Current authorization state

- Protocol freeze state: `NOT_FROZEN`
- Confirmatory execution: `NOT_AUTHORIZED`
- Claim support: `NOT_ESTABLISHED`
- Promotion authority: `NOT_AUTHORIZED`
- Candidate approval status: `NOT_APPROVED`

These states must not be changed by an engineering workflow or pilot result.

## 4. Engineering evidence available

Full-path engineering workflow:
https://github.com/AhmedPeaRL/maximal-one/actions/runs/39871127641

Exploratory runtime pilot:
https://github.com/AhmedPeaRL/maximal-one/actions/runs/39871345141

The full-path workflow completed successfully, including the matrix gate tests, compilation checks, and full-path equivalence test.

The runtime pilot completed successfully for one declared scenario with two outer repetitions and 200 surrogates per repetition. Its output is diagnostic-only.

These results establish limited engineering execution evidence. They do not establish formal Type-I error control, protocol adequacy across the declared design space, real-domain replication, or HCM claim support.

The reviewer should inspect the actual workflow logs and retained artifacts rather than relying on this summary alone.

## 5. Required independent review questions

Please provide an explicit, reasoned decision on each item.

1. Are the nine declared data-generating scenarios correctly specified, sufficiently justified, and appropriate for the stated calibration objective?
2. Are the in-band resonance scenarios mathematically valid and correctly parameterized for their stated target frequencies and root radii?
3. Does the implemented endpoint match the declared scientific estimand and the intended production implementation?
4. Are the stationary Gaussian AR(p) null family, AIC order selection, stationarity requirements, hold-back, spectral estimation settings, and surrogate p-value calculation adequately justified?
5. Is the seed schedule reproducible, scenario-identity based, and invariant to sharding, merge order, and checkpoint/resume?
6. Are invalid attempts, failed fits, and surrogate shortfalls handled without silent deletion, replacement, or denominator changes?
7. Is the proposed design capable of estimating the relevant Type-I error operating characteristics with adequate precision under the declared scenarios?
8. What acceptance rule should be used, and what precision or uncertainty criterion justifies it?
9. Is the historical 0.075 ceiling justified for this objective? If not, explain the appropriate prospective alternative without silently changing the protocol.
10. Are the proposed repetition counts and computational plan adequate and feasible?
11. What limitations, untested assumptions, or additional scenarios must be addressed before protocol freeze?
12. Does any result support only an engineering conclusion, or does any result legitimately support a broader scientific conclusion? State the scope explicitly.

## 6. Required review deliverable

Please return a signed or otherwise attributable review containing:

- Reviewer name and relevant statistical-methods expertise
- Review date in UTC
- Exact commit SHA and reviewed file hashes
- Materials and artifacts actually inspected
- Decision for each question above
- Material concerns and required corrections
- Any proposed protocol amendments, with rationale
- Explicit disposition: `APPROVE_FOR_PROSPECTIVE_FREEZE`, `REVISE_AND_RESUBMIT`, or `NOT_APPROVED`
- A clear statement of what the review does and does not establish

Approval for prospective freeze is not authorization to execute a confirmatory run. Any approved amendments must first be incorporated, versioned, and reviewed against the resulting exact snapshot.

## 7. Non-negotiable safeguards

- Do not change acceptance thresholds after observing results.
- Do not infer approval from passing CI.
- Do not treat a pilot as formal calibration.
- Do not silently discard or replace invalid attempts.
- Preserve every requested replicate in the denominator and preserve its attempt record.
- Keep protocol, code, dependency, workflow, and artifact identities traceable.
- Do not describe synthetic calibration as real-domain replication.
- Do not promote the HCM claim from this calibration alone.
- Keep `main` unchanged during this remediation and review stage.

## 8. Current disposition

`ENGINEERING_PATH_PASSED_FOR_THE_RECORDED_SNAPSHOT; STATISTICAL_REVIEW_PENDING; PROTOCOL_NOT_FROZEN; CONFIRMATORY_EXECUTION_NOT_AUTHORIZED; CLAIM_NOT_ESTABLISHED`
