# Type-I Calibration V3/V4 Status Addendum

**Record date:** 2026-11-12  
**Status:** `CANDIDATE_ONLY — ACCEPTANCE_RULE_UNRESOLVED — NO_FORMAL_EXECUTION_AUTHORITY`

## 1. Keep the two V3 meanings separate

The repository contains two different V3 documents:

1. `TYPE1_MANUAL_OCCURRENCE_ADJUDICATION_PROTOCOL_V3.md` — governance rules for human review of code/governance occurrences.
2. `TYPE1_CALIBRATION_SPEC_V3_CANDIDATE.md` and `TYPE1_CALIBRATION_SCENARIO_MATRIX_V3.json` — a candidate statistical Type-I calibration design.

A successful manual-adjudication governance workflow does not approve the statistical calibration protocol.

## 2. V3 statistical candidate

The V3 statistical candidate describes nine stationary Gaussian AR DGPs, sample size 1,024, burn-in 2,000, 2,000 outer attempts per scenario, and 1,000 surrogates per attempt. It proposes a one-sided 95% Wilson upper bound no greater than 0.075 for every scenario. These are candidate settings, not an approved or frozen protocol.

The V3 validation run `43073483541`, job `130707223619`, stopped before simulation because the V3 protocol was not `APPROVED_FROZEN`. The log explicitly states that no calibration simulations were started. Preserve this failure as a valid fail-closed outcome.

## 3. V4 candidate is not a V3 amendment

The V4 candidate matrix SHA-256 is:

`f8b8dfaf97282ca24378b8929939d8fffd1fe72064a2fe662198422a11b1bc2f`

The V4 review request SHA-256 is:

`616da863703ff157d3d95e2261308bf358e9ee16923695f6d6676db25937bb25`

V4 uses a different candidate design, including sample size 3,328 and in-band resonant AR(2) scenarios. Its `acceptance_rule` remains `null`; the inherited 0.075 ceiling is not approved. Do not combine V3 sample size/scenarios with V4 scenarios or seed identities.

## 4. Pilot and engineering evidence are not calibration

- Runtime pilot run `43073211742`, artifact `13878079293`: two outer attempts, 200 surrogates per attempt, one V4 resonant AR(2) scenario. Explicitly exploratory; not formal calibration.
- Cross-runner engineering run `43073152996`, artifact `13882575040`: six engineering-only replicate records with 1,000 surrogates each across distinct runner instances. This tests runner behavior and identity, not the nine-scenario Type-I acceptance rule.
- CLI resume identity and negative-gate tests are engineering controls, not statistical evidence.

## 5. Preserve historical Type-I results

The historical two-sided 95% Wilson classifications remain unchanged. Do not reclassify any historical pass/failure using the proposed V3 one-sided rule or the unresolved V4 rule. Any future acceptance rule must be justified and frozen prospectively by an attributable independent human statistician before formal calibration.

## 6. AR(20) is a separate prospective diagnostic

An AR(20) data-generating process is not the same thing as silently increasing the production surrogate order cap. The AR(20) study must have its own prospective specification, coefficient grid, stationarity checks, seed schedule, invalid-attempt policy, compute budget, and interpretation before execution. It must not alter the production null or the V4 candidate matrix after observing outcomes.

## 7. Current authority

```text
V3 statistical protocol = CANDIDATE_PENDING_REVIEW
V4 statistical protocol = DRAFT_PENDING_REVIEW
acceptance_rule = UNRESOLVED
protocol_freeze = NOT_FROZEN
formal_calibration_authorized = false
confirmatory_execution_authorized = false
claim_support = false
promotion_authority = false
```
