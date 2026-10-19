# Calibration Implementation Gap — Commit `9fcd54b`

**Review date:** 2026-10-19  
**Reviewed commit:** `9fcd54bbc56ccf4c13b7b2020aa5f02b5f2b7ce5`  
**Disposition:** `HOLD — DO NOT FREEZE OR PROMOTE`

## Historical results

Workflow [39155162528](https://github.com/AhmedPeaRL/maximal-one/actions/runs/39155162528) checked out the exact commit and completed all four scenarios. Historical rule: two-sided 95% Wilson interval must contain nominal 0.05 and its upper endpoint must be <= 0.075.

| Scenario | Valid outer reps | Rejections | Rate | 95% Wilson interval | Historical result |
|---|---:|---:|---:|---|---|
| AR(1), phi=[0.40] | 1000 | 52 | 0.052 | [0.039873, 0.067556] | Pass, limited synthetic scope |
| AR(2), phi=[0.45,-0.10] | 1000 | 60 | 0.060 | [0.046896, 0.076471] | Fail: upper endpoint > 0.075 |
| AR(5), low-order coefficients | 1000 | 49 | 0.049 | [0.037261, 0.064191] | Pass, limited synthetic scope |
| AR(10), low-order coefficients | 1000 | 73 | 0.073 | [0.058459, 0.090809] | Fail: interval excludes 0.05 and upper endpoint > 0.075 |

## Interpretation

**AR(2):** the interval contains 0.05, but its upper endpoint 0.076471 exceeds the committed 0.075 ceiling. This is a failure under the current rule, not proof that the true rate differs from 5%.

**AR(10):** the interval's lower endpoint is above 0.05 and its upper endpoint exceeds 0.075. This is a stronger warning of over-rejection under this DGP. It does not, by itself, identify the mechanism. Inspect AIC order selection, refitting, surrogate failures, selected-order distribution, and boundary diagnostics before assigning cause.

## Critical mismatch

`.github/workflows/null-type1-calibration.yml` runs `--surrogates 200`. `core-scientific/strict_claim.json` sets `stochastic_null_protocol.bootstrap_trials` to `1000`, and `scripts/generate_report.py` passes that value to `parametric_short_memory_null`.

Therefore these results are valid for the 200-surrogate calibration configuration but are **not exact calibration of the production configuration**. Preserve the historical results; do not relabel them as production-equivalent and do not change thresholds after seeing them.

## Required work before formal recalibration

1. Make calibration and production match on the 1000 surrogate draws, endpoint estimator, frequency band 0.01–0.05, AR order range 1–20, AIC, constant trend, stationarity/root constraints, fixed hold-back, refitting, upper-tail test, add-one p-value rule, and invalid-result semantics.
2. Record per outer replicate: p-value, requested/valid surrogate count, refit failures, alpha failures, selected order, and boundary indicator.
3. Add deterministic replicate-level seeds and tests proving results do not depend on shard order.
4. Commit the protocol and matrix before the next formal run.
5. Obtain attributable independent statistical review of the estimand, acceptance ceiling, matrix, failure policy, and power targets.

Other blockers: [raw acquisition/audit run 39155206532](https://github.com/AhmedPeaRL/maximal-one/actions/runs/39155206532) is structurally blocked; [claim-promotion run 39155182272](https://github.com/AhmedPeaRL/maximal-one/actions/runs/39155182272) reports 0/2 eligible independent secondary domains. Freeze remains `NOT_FROZEN`.
