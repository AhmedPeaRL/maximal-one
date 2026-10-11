# Type-I Calibration Run Review — 2026-10-11

**Scope:** descriptive review of the completed GitHub Actions run, not a new statistical analysis and not a null-freezing decision.

- Repository: `AhmedPeaRL/maximal-one`
- Workflow run: `38088677966`
- Exact run commit: `179c2bb01167ed9f3d3deda6549c2b893faeabb5`
- Workflow: `.github/workflows/null-type1-calibration.yml`
- Requested repetitions per scenario: 1000
- Surrogates per test: 200
- Sample size: 1024
- Invalid repetitions reported in the inspected jobs: 0
- Artifacts expire on 2027-01-08 unless downloaded earlier.

## Observed scenario outcomes

| Scenario | Empirical Type-I rate | Wilson 95% interval | Workflow status | Interpretation under the current declared rule |
|---|---:|---|---|---|
| `gaussian_ar1_phi_0_4` | 0.052 | [0.0398730363, 0.0675557393] | `TYPE1_CALIBRATION_PASS_LIMITED_SYNTHETIC_SCOPE` | Pass for this one synthetic scenario only |
| `gaussian_ar5_low_order_coefficients` | 0.049 | [0.0372610346, 0.0641907015] | `TYPE1_CALIBRATION_PASS_LIMITED_SYNTHETIC_SCOPE` | Pass for this one synthetic scenario only |
| `gaussian_ar2_phi_0_45_minus_0_10` | 0.060 | [0.0468964727, 0.0764710748] | `TYPE1_CALIBRATION_FAILED` | Fails the current rule because the Wilson upper bound exceeds 0.075; the interval still contains 0.05 |
| `gaussian_ar10_low_order_coefficients` | 0.073 | [0.0584590262, 0.0908090255] | `TYPE1_CALIBRATION_FAILED` | Fails the current rule; interval excludes 0.05 and upper bound exceeds 0.075 |

Artifact records from the run:

- AR(1): [artifact 11687241416](https://github.com/AhmedPeaRL/maximal-one/actions/runs/38088677966/artifacts/11687241416)
- AR(5): [artifact 11687017681](https://github.com/AhmedPeaRL/maximal-one/actions/runs/38088677966/artifacts/11687017681)
- AR(2): [artifact 11687415527](https://github.com/AhmedPeaRL/maximal-one/actions/runs/38088677966/artifacts/11687415527)
- AR(10): [artifact 11685850751](https://github.com/AhmedPeaRL/maximal-one/actions/runs/38088677966/artifacts/11685850751)

## What this does and does not establish

1. The workflow completed all four scenario jobs; two passed the declared *limited synthetic-scope* criterion and two failed it. A successful upload step only means the report artifact was uploaded; it does not mean the calibration passed.
2. AR(2) is a rule failure because the upper Wilson bound is 0.07647, above 0.075. It is **not** accurate to say its interval excludes 0.05; it includes 0.05.
3. AR(10) is the stronger warning: the interval [0.05846, 0.09081] excludes 0.05 and exceeds the upper-bound limit.
4. These results are conditional on the declared synthetic AR scenarios, the chosen sample size, the test implementation, the surrogate count, and the fixed run configuration. They do not prove a universal Type-I error rate for all processes.
5. Passing AR(1) and AR(5) does not cancel the failures in AR(2) and AR(10). Do not average the four rates into a single pass/fail result unless a combined statistic and rule were specified in advance.
6. The current AR(p) null remains exploratory and unfrozen. Do not change the null family, acceptance threshold, or scenario selection to obtain a pass. Do not rerun the same expensive matrix merely to seek a favorable realization.
7. The prior primary result `p=0.999001` remains a non-rejection under the existing analysis; this calibration run does not convert it into positive evidence or change the result.

## Required next action

Download and preserve all four JSON artifacts with the exact run ID, commit SHA, artifact IDs, and their internal seeds. Review the full JSON (including boundary fractions and failure examples) before designing a **prospective** follow-up calibration protocol. Separate the following questions:

- calibration under each declared synthetic AR scenario;
- sensitivity to sample length and Welch segment coverage;
- null-model adequacy and order-selection saturation;
- prospective confirmatory inference on real data.

Do not merge those questions into one pass/fail label.
