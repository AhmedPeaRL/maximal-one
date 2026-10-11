# Welch Segment Coverage Review — V1

**Purpose:** document the number of complete Welch segments implied by the currently declared estimator configuration. This is a design diagnostic, not an endpoint result and not a replication decision.

## Frozen estimator configuration currently reported

- `nperseg = 1024`
- `noverlap = 512` (50% overlap)
- step between segment starts = `1024 - 512 = 512`
- only complete segments count; no padding or adaptive `nperseg` is assumed.

For a finite series of length `N >= 1024`, the number of complete segments is:

`K = floor((N - 1024) / 512) + 1`

For `N < 1024`, `K = 0` under this fixed configuration.

## Current lengths and implied segments

| Series | N | Complete Welch segments K | Notes |
|---|---:|---:|---|
| Synthetic calibration series | 1024 | 1 | Same nominal length as one segment |
| FRED INDPRO | 1284 | 1 | The second 512-shifted segment would be incomplete and is not counted |
| Sunspots primary | 3328 | 5 | Five complete overlapping segments |
| HadCET monthly | 4404 | 7 | Seven complete overlapping segments |

## Interpretation limits

- Overlapping Welch segments are not independent observations. `K` is not the effective degrees of freedom and must not be used as if it were an independent sample size.
- A calibration at `N=1024` does not by itself validate the estimator's finite-sample behavior at `N=3328`, `N=4404`, or for a one-segment INDPRO estimate. The AR(2)/AR(10) calibration failures remain failures regardless of this design mismatch.
- Conversely, different `K` values do not automatically invalidate a domain. They identify a finite-sample comparability issue that needs a prospective, justified protocol.
- Do not simply raise the replication minimum or require an arbitrary number of segments after seeing domain alpha. A new minimum, if needed, must be justified from estimator precision/power and fixed before confirmatory endpoint inspection.

## Required prospective study design

1. Keep the existing canonical estimator unchanged for the historical analysis; label it exploratory where required.
2. Define a finite set of sample lengths *before* running outcomes, including at minimum `N=1024`, `N=1284`, `N=3328`, and `N=4404`, plus any scientifically justified longer/shorter lengths.
3. For each length, simulate each predeclared null scenario with fixed seeds and record Type-I rate, Wilson interval, invalid-fit rate, selected AR-order distribution, boundary fraction, and runtime.
4. Change one design factor per comparison: length, null scenario, estimator segmentation, or order-selection rule. Do not simultaneously alter several factors and attribute the result to one of them.
5. Because changing `nperseg` changes frequency resolution and the estimator itself, treat it as a separate estimator version with its own protocol ID, not as a silent tuning knob.
6. Before any confirmatory use, define how the final null adequacy decision is made across scenarios and lengths, including treatment of multiple scenarios and failures. Do not infer a confirmatory pass from one successful scenario.

No numerical acceptance thresholds are proposed here. The point of this review is to require that those thresholds be justified and frozen prospectively rather than invented after observing the calibration outcomes.
