# AR(10) Null-Capacity Diagnostic Plan — V1

**Status:** proposed diagnostic plan; not a frozen confirmatory protocol and not authorization to alter the production null.

## Motivation

The current synthetic calibration scenario `gaussian_ar10_low_order_coefficients` recorded 73 rejections in 1000 repetitions (0.073), with Wilson 95% interval [0.058459, 0.090809]. Under the idealized binomial reference p=0.05, the exact one-sided tail is approximately 0.001006. This is a material diagnostic discrepancy in the declared scenario. It does not establish why it occurs, and must not be generalized to all time series or used as support for the HCM hypothesis.

The separate primary-domain AR(p) audit previously reported boundary saturation at max order 20 in 937/1000 surrogate refits. A diagnostic scan that selected order 40 is a separate result and must not be conflated with the production null max order 20.

## Freeze existing evidence first

Keep run `38088677966`, commit `179c2bb01167ed9f3d3deda6549c2b893faeabb5`, its four artifacts, exact scenario seeds, logs, JSON outputs, and their SHA-256 digests. Do not rerun only in pursuit of a favorable result.

## Diagnostic work to record before running

1. Identify and cite the exact run/commit/artifact for the primary-domain result `0.937` and for the later `0.947` value. Until both are tied to exact code, data, seed and output hashes, record the discrepancy as unresolved; do not pick one.
2. Inspect the full empirical distribution of selected AR order per outer replicate and per surrogate, not only the mean/boundary fraction. Report frequency at each order, convergence failures, stationarity checks, residual diagnostics, and whether order selection piles up at candidate boundaries.
3. Audit whether the outer simulation generator matches the assumptions and parameterization of the surrogate-fitting routine. Record parameterization, initialization/burn-in, coefficient stability, innovation variance, handling of fitted model failures, and whether the replicate-level rejection indicator is generated independently as assumed by the binomial operating-characteristic calculation.
4. Check each component of the implemented test in isolation with small, deterministic unit cases; then use a locked, predeclared diagnostic grid. Change only one factor at a time and preserve all earlier outputs.
5. Separate the model-order diagnostic scan that reached 40 from the production order-selection cap of 20. Report the candidate set, objective values, tie-breaking, convergence and boundary behavior; never silently raise the cap just because the current result hits it.
6. Preserve the current upper-tail endpoint, p-value formula, and existing pass threshold while diagnosing. Any future proposed change to model family, order range, burn-in, surrogate generation or acceptance criteria must be a post-observation protocol amendment followed by a new commit and fresh prospective validation.

## Deliverable before any new expensive run

Commit a diagnostic specification that lists the exact hypotheses to investigate, the single changed factor for each diagnostic, outputs/logging, stopping rules, compute budget, seeds, and interpretation of outcomes. It must state explicitly that results are diagnostic-only and cannot promote the scientific claim.

## Non-claims

Neither the AR(10) calibration failure nor primary-domain boundary saturation alone proves the scientific hypothesis true or false, and neither establishes HCM causation, consciousness, universality, or market advantage. Until null adequacy is formally resolved, the confirmatory null remains unfrozen and claim promotion remains blocked.
