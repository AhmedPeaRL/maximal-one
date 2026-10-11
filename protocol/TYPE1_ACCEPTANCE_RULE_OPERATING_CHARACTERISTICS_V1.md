# Type-I Acceptance Rule: Operating Characteristics — Corrected V1

**Review date:** 2026-10-11  
**Scope:** audit of the currently implemented synthetic-calibration acceptance rule. This correction changes the audit description/calculation only; it does not change the production gate.

## 1. Implemented rule

In `analysis/calibrate_null_type1_scenario.py`, a scenario passes only when all of the following hold:

1. The number of valid repetitions is at least 1,000.
2. The two-sided 95% Wilson interval contains the nominal rate 0.05: `lower <= 0.05 <= upper`.
3. The Wilson upper endpoint is no greater than 0.075.

The previous audit incorrectly modeled only condition 3. That omitted the lower-bound requirement and therefore described a different, more permissive rule. This document and its companion audit script now match the existing production code. The production gate itself is not modified.

## 2. Accepted counts and operating characteristics

For `n = 1000`, the accepted integer rejection counts are **37 through 58 inclusive**.

- At 36 rejections, the Wilson upper endpoint is approximately 0.0494357, below 0.05; the interval therefore fails to contain the nominal rate.
- At 37 rejections, the Wilson interval contains 0.05.
- At 58 rejections, the Wilson upper endpoint is approximately 0.0742496, within the 0.075 limit.
- At 59 rejections, the Wilson upper endpoint is approximately 0.0753609, above the limit.

Under the reference model `X ~ Binomial(1000, 0.05)` with independent Bernoulli repetitions:

- Probability one nominal scenario passes: approximately **0.8682836** (86.83%).
- Probability one nominal scenario falsely fails this screening rule: approximately **0.1317164** (13.17%).
- If four scenarios are independent and all are exactly nominal, probability all four pass: approximately **0.5683901** (56.84%).
- Under that same independence assumption, probability at least one of four falsely fails: approximately **0.4316099** (43.16%).

The four-scenario family values are conditional calculations, not guarantees. Independence between scenario outcomes must not be assumed as an empirical fact without justification.

## 3. Observed calibration results

- AR(1): 52/1000 = 0.052; Wilson interval approximately [0.039873, 0.067556]. Passes this scenario's rule only.
- AR(5): 49/1000 = 0.049; Wilson interval approximately [0.037261, 0.064191]. Passes this scenario's rule only.
- AR(2): 60/1000 = 0.060; interval approximately [0.046896, 0.076471]. Fails because its upper endpoint exceeds 0.075. The interval contains 0.05; the exact one-sided binomial tail `P(X >= 60 | n=1000, p=0.05)` is approximately 0.086732, so do not characterize this alone as strong evidence of inflation.
- AR(10): 73/1000 = 0.073; interval approximately [0.058459, 0.090809]. Fails the rule. Under the simple independent-binomial reference model, the exact one-sided tail `P(X >= 73 | n=1000, p=0.05)` is approximately 0.001006. This warrants targeted diagnosis of this declared scenario, but does not identify the cause or generalize to all data-generating processes.

The reported mean surrogate boundary fractions are low (about 0.001–0.00224) for these synthetic scenarios. This is a descriptive result for these artifacts only; it does not by itself diagnose the AR(10) discrepancy. Keep the primary-domain boundary-saturation issue (historical values 0.937 versus 0.947) separate until run identities and hashes are reconciled.

## 4. Limits and next steps

Synthetic Type-I calibration is a diagnostic check, not independent real-domain replication, not proof of general null adequacy, and not support for the scientific hypothesis. Preserve all four results. Do not rerun merely to seek a passing outcome, relax the acceptance rule, or change scenario membership after observing results.

Before any future calibration matrix, predefine its target operating characteristic, scenario family, repetition count, seeds, invalid-run handling, per-scenario rule, and family-level decision policy. Any change must be documented as a post-observation amendment with fresh validation.
