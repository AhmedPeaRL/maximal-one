# Type-I Calibration Result Review — 2026-10-10

## Observed result supplied from GitHub Actions

- Scenario: `gaussian_ar10_low_order_coefficients`
- Valid repetitions: `1000/1000`
- Empirical Type-I rejection rate: `0.073`
- Wilson 95% interval: `[0.0584590262, 0.0908090255]`
- Declared nominal alpha: `0.05`
- Declared maximum acceptable Wilson upper bound: `0.075`
- Workflow outcome: `CALIBRATION_NOT_PASSED_OR_INCOMPLETE, exit code 1`

---

## Interpretation

This is a completed scenario-level calibration failure, not a runtime/import failure.

- The observed rejection rate is above 0.05, the reported interval does not contain 0.05, and the upper bound exceeds the protocol's 0.075 limit.
- For this declared synthetic Gaussian AR(10) scenario, the implemented test has not demonstrated acceptable Type-I behavior under the current acceptance rule.
- This result does not by itself establish that every scenario fails, that the scientific hypothesis is false, or that a different null should be chosen.
- It does mean the current null/test combination must not be frozen as confirmatory on the basis of this run.

---

## Required actions

1. Preserve the complete JSON artifact for this run, its artifact SHA-256, workflow run ID, commit SHA, and dependency/runner versions.
2. Retrieve the other three scenario artifacts from the same workflow matrix. Record each scenario's rate, interval, invalid count, and pass/fail status without pooling scenarios.
3. Keep the production null NOT_FROZEN; keep claim promotion blocked.
4. Diagnose the source of over-rejection prospectively: inspect null-fit validity, AR-order boundary saturation, residual behavior, stationarity, parameter stability, and the Monte Carlo p-value implementation. Do not alter thresholds or select a different null based on observed sunspot alpha.
5. If code or protocol changes are proposed, document them as a dated amendment and run fresh validation on fixed seeds and all declared scenarios. Retain this failed result in the historical record.
6. The roughly 3 h 15 min runtime is a performance concern, not evidence of validity or invalidity. Profile the expensive operations before optimizing; any optimization must be checked against an unchanged reference implementation for numerical equivalence and deterministic behavior.

---

## Claim-state snapshot from supplied logs

- Scientific status: `UNDER_INVESTIGATION`
- Primary stochastic null rejected: `false`
- Primary stochastic-null p-value: `0.999001`
- Independent secondary replication: `0/2`
- Claim support: `false`
- Promotion authority: `false`

A passing synthetic calibration would only validate limited operating characteristics under the tested synthetic scenarios; it would not establish HCM, scientific replication, or claim support.
