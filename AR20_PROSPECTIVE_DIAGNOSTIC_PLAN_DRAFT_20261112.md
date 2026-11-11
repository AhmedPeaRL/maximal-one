# AR(20) Prospective Diagnostic Plan — Draft Only

**Record date:** 2026-11-12  
**Status:** `DESIGN_DRAFT — NOT_REVIEWED — NOT_FROZEN — NOT_AUTHORIZED`

## 1. Purpose and distinction

This study would evaluate the operating behavior of the complete declared test under explicitly specified stationary Gaussian AR(20) data-generating processes.

An AR(20) DGP means:

`X_t = phi_1 X_(t-1) + ... + phi_20 X_(t-20) + epsilon_t`

It is not permission to increase the production surrogate model-order cap, alter the production null, or reinterpret the earlier AR(10) and AR(p) diagnostics.

The study is diagnostic-only. It cannot support or falsify HCM by itself and cannot grant claim-promotion authority.

## 2. Decisions required before execution

An attributable independent time-series statistician must review and decide:

1. The target Type-I estimand and exact rejection event for the full production endpoint/null procedure.
2. The predeclared AR(20) coefficient vectors or parameter-generation design.
3. Stationarity validation for every coefficient vector, including a documented root/companion-matrix criterion.
4. Innovation distribution and variance; any non-Gaussian extension must be a separate declared scenario family.
5. Sample size, burn-in, frequency band, Welch settings, null refitting, requested surrogate count, and outer repetitions.
6. Seed derivation keyed to stable scenario identity and replicate index.
7. Invalid-attempt, failed-fit, surrogate-shortfall, and missing-artifact handling.
8. Monte Carlo precision and a prospectively justified acceptance rule. The V4 acceptance rule is currently unresolved; do not inherit 0.075 without independent justification.
9. Production-equivalence tests and exact implementation hashes.
10. Compute budget, stopping rules, output schema, and artifact-retention plan.

No coefficient vector or threshold may be chosen after inspecting candidate outcomes.

## 3. Proposed scenario coverage for reviewer consideration

The reviewer should determine whether the prospective grid needs distinct predeclared AR(20) families covering:

- low-persistence stable coefficients;
- mixed-sign or alternating coefficients;
- dense nonzero coefficients;
- near-stability-boundary but strictly stationary coefficients;
- resonant roots with peaks inside the declared frequency band;
- coefficients producing peaks outside the declared band as negative controls.

These are design categories only. No coefficient vectors are approved by this draft.

## 4. Required records per attempt

Preserve one record for every requested replicate, including:

- exact commit, protocol version/hash, matrix hash, runner hash, dependency lock hash;
- scenario ID, exact coefficient vector, stationarity evidence;
- DGP and null seed identities;
- generated-series hash;
- requested and valid surrogate counts;
- all fit/estimation failures and reasons;
- selected AR order and boundary diagnostics;
- exceedances, Monte Carlo p-value, and rejection indicator when valid;
- workflow run/job/attempt and artifact IDs;
- runtime/platform/Python versions;
- final attempt status.

No failed attempt may be silently dropped or replaced. An incomplete run is not a pass.

## 5. Prospective sequence

1. Publish this draft as a design request only.
2. Obtain attributable independent statistical review.
3. Resolve the acceptance rule prospectively.
4. Amend the plan with exact coefficient vectors, seed schedule, sample size, repetition counts, surrogate counts, and hashes.
5. Freeze the approved plan in a new exact commit before any formal run.
6. Pass production-equivalence and negative-gate tests.
7. Execute the predeclared diagnostic and preserve all outputs.
8. Publish a report that labels the scope as synthetic operating-characteristic evidence only.

## 6. Non-authorization

```text
AR20 execution = NOT_AUTHORIZED
production null change = NOT_AUTHORIZED
formal Type-I calibration = NOT_AUTHORIZED
confirmatory execution = NOT_AUTHORIZED
claim_support = false
promotion_authority = false
```
