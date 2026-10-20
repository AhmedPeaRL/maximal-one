# Request for Attributable Independent Statistical Review — Type-I Calibration V4 Draft

**Requested review type:** independent human statistical-methods review, attributable by name, affiliation or professional profile, date, and explicit conflict-of-interest statement.

**Status:** Draft only; no protocol freeze or confirmatory execution is authorized.

Please review the exact commit and hashes supplied by the researcher at the time of review. This request must not be treated as fulfilled by an AI-only review.

## Decisions requested

1. **Estimand and scope.** Is the proposed per-DGP Type-I rejection probability the right target for this implemented test? What conclusions does it support, and what does it not support?
2. **Scenario coverage.** Are the nine proposed stationary Gaussian AR DGPs adequate for a first calibration layer? Specifically, are production-matched `n=3328` and two resonances at frequencies 0.02 and 0.04 appropriate? What additional DGPs are required before a formal run?
3. **Acceptance criterion.** Is a ceiling of 0.075 defensible given the consequences of false rejection? If yes, provide a prospective substantive rationale and recommend a complete decision rule. If no, propose an alternative before formal simulation. Do not infer that passing a ceiling alone means the rate equals 0.05.
4. **Monte Carlo precision.** Are 2,000 outer repetitions sufficient for the proposed decision rule? Please assess the chance of pass/fail around plausible true rejection rates, including 0.05, 0.065, 0.07, and 0.075.
5. **Invalid attempts.** Is the proposed no-silent-dropping rule appropriate? Recommend whether any invalid attempt must fail the scenario, or whether a predeclared invalid-rate bound and worst-case sensitivity analysis is defensible. Specify the rule before formal results exist.
6. **Behavioral equivalence.** Review a golden test that compares the exact production preprocessing/endpoint/null path and the calibration path on the same series and seed. State whether it demonstrates equivalence or only shared function calls.
7. **Feasibility.** Review pilot timing, sharding, deterministic merge, resume after interruption, artifact size, and workflow timeout. A checkpoint must never be mistaken for a completed pass.
8. **Reproducibility.** Review stable scenario IDs, seed construction, commit SHA, dependency-lock SHA-256, matrix SHA-256, workflow run/attempt IDs, and artifact retention.

## Required reviewer response

Please provide:
- Full name and a verifiable professional profile or institutional affiliation;
- Date and conflicts of interest;
- Exact commit SHA and protocol/matrix hashes reviewed;
- `APPROVE`, `APPROVE WITH CONDITIONS`, or `REQUEST REVISIONS` for each item above;
- Reasons and any required revisions;
- Explicit statement that the review is independent of the AI assistant and that the reviewer accepts attribution of the review.

Until an attributable human review is completed, keep the matrix status `DRAFT_PENDING_ATTRIBUTABLE_INDEPENDENT_STATISTICAL_REVIEW`, freeze state `NOT_FROZEN`, and confirmatory authorization `false`.
