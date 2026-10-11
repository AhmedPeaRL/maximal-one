# Type-I Acceptance Rule: Operating Characteristics — V1

**Review date:** 2026-10-11  
**Scope:** mathematical review of the current synthetic-calibration scenario rule only. This is not a replacement rule and does not amend the workflow.

## 1. Current declared rule

The current calibration JSON records `nominal_alpha = 0.05`, `maximum_acceptable_95pct_wilson_upper_bound = 0.075`, and `minimum_valid_repetitions_per_scenario = 1000`. For a scenario with `n = 1000` valid repetitions and `x` rejections, the scenario is accepted if the two-sided 95% Wilson upper confidence bound for the binomial rejection proportion is no greater than 0.075.

The rule is a confidence-bound screening rule. It is not equivalent to a hypothesis test whose null is exactly `p = 0.05`, and its `TYPE1_CALIBRATION_FAILED` status is a failure of the declared acceptance criterion, not automatically a formal statistical finding that true Type-I error exceeds a specified value.

## 2. Exact binomial operating characteristics

Using the standard two-sided 95% Wilson bound (z = 1.959963984540054), for `n = 1000` the acceptable integer rejection counts are **0 through 58**. At x=58 the Wilson upper bound is about 0.0742496; at x=59 it is about 0.0753609.

Under the idealized independent-repetition model `X ~ Binomial(1000, 0.05)`:

- Probability the current criterion passes one truly nominal scenario: approximately **0.8894385**.
- Probability it fails one truly nominal scenario (false-fail probability): approximately **0.1105615**, or **11.06%**.
- If four scenarios were independent and each exactly nominal, probability all four pass: approximately **0.6258405**, or **62.58%**.
- Under that same independence assumption, probability at least one of four fails: approximately **0.3741595**, or **37.42%**.

These values supersede the previously circulated figures 13.2%, 57%, and 43% for this exact stated rule. The four scenario outcomes are not guaranteed to be independent in every possible implementation, so the four-scenario calculation is a reference calculation under independence, not a universal guarantee.

## 3. Interpretation of the observed scenarios

- AR(1): 52/1000 = 0.052; Wilson 95% CI approximately [0.039873, 0.067556]; passes the declared criterion in this scenario only.
- AR(5): 49/1000 = 0.049; Wilson 95% CI approximately [0.037261, 0.064191]; passes the declared criterion in this scenario only.
- AR(2): 60/1000 = 0.060; Wilson 95% CI approximately [0.046896, 0.076471]; fails because the upper bound exceeds 0.075. The interval includes 0.05. The exact one-sided binomial tail `P(X >= 60 | n=1000, p=0.05)` is approximately **0.086732**. This is weak evidence against the exact p=0.05 model by common conventional standards; do not call it a strong standalone finding of inflation.
- AR(10): 73/1000 = 0.073; Wilson 95% CI approximately [0.058459, 0.090809]; fails the criterion. The exact one-sided binomial tail `P(X >= 73 | n=1000, p=0.05)` is approximately **0.001006**. This is a clear discrepancy under the simple independent-binomial reference model and warrants targeted diagnosis; it does not by itself establish the cause or generalize to all data-generating processes.

The exact binomial calculations treat the 1000 repetitions as independent Bernoulli trials with a common rejection probability. This assumption itself should be checked against the implementation and seed/replicate construction before the values are used inferentially.

## 4. Monte Carlo surrogates

With 200 surrogates and the plus-one p-value rule `(exceedances + 1)/(valid_surrogates + 1)`, the p-value increments are `1/201 ≈ 0.004975`. A zero-exceedance minimum is 1/201 ≈ 0.004975; a rejection threshold of p <= 0.05 corresponds to at most 9 exceedances, since 10/201 ≈ 0.049751 and 11/201 ≈ 0.054726. This discretization is a resolution property. It is not, by itself, evidence that Monte Carlo discreteness cannot affect calibration. The whole simulation-and-surrogate procedure must be calibrated as implemented.

## 5. Prospective redesign requirements (not a current rule)

Before any future calibration matrix is run, write and commit a protocol that predefines:

1. The scientific purpose of calibration and the target operating characteristic (e.g., upper confidence bound, tolerance, or formal test), rather than choosing a convenient fixed upper limit after seeing outputs.
2. The per-scenario pass/fail rule and how multiple scenarios will be summarized; do not average away an adverse scenario unless an aggregate statistic and rationale were specified in advance.
3. The number of outer repetitions with a calculation or simulation demonstrating the desired precision and false-fail probability under p=0.05.
4. The scenario family, coefficients, initialization/burn-in, estimator, null fit, surrogate count, random seeds, failed-repetition handling, and software commit.
5. Whether the target is per-scenario error control or family-level control over the entire matrix. If family-level claims are intended, predefine the multiplicity/decision policy.
6. A rule that no thresholds, null families, or scenario exclusions are changed after looking at current or future outcomes without a transparently labeled post-observation amendment and fresh validation.

Do not rerun solely to seek a passing outcome. Preserve existing results and failures.

## 6. Limits

Synthetic type-I calibration at N=1024 is necessary diagnostic evidence, not general null adequacy, not real-domain replication, and not claim support. `strict_claim.json` remains the authority for the currently blocked confirmatory status until a formally reviewed prospective protocol and fresh evidence satisfy the repository gates.
