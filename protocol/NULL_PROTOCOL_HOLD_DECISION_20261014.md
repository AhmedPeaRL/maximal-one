# Null Protocol Decision — Hold Pending Independent Methodological Review

Protocol ID: `NULL_PROTOCOL_HOLD_DECISION_20261014_V1`

Decision date: 2026-10-14

Status: `EXPLORATORY_NULL_NOT_FROZEN_FOR_CONFIRMATORY_INFERENCE`

## Decision

Do not freeze or replace the current null family in this change. Retain the existing stationary Gaussian AR(p), AIC-selected over p = 1..20, as an explicitly exploratory diagnostic protocol only. Do not use it for confirmatory endpoint interpretation until an independent methodological review has assessed its adequacy and a prospective calibration protocol has passed.

This is a stop/hold decision, not a claim that AR(p) is universally invalid and not a selection of a more favorable alternative.

## Evidence motivating the hold

- The current reported primary stochastic-null p-value is `0.999001`; the null was not rejected under the reported contract.
- The capacity diagnostic reports 937/1000 surrogate refits selecting the maximum AR order 20. A separate recorded stream reports 0.947; these are source-scoped estimates and should not be forced to match across different random streams.
- A diagnostic scan through order 40 also reached its scan boundary.
- The reported Type-I scenarios include AR(2) at 60/1000 and AR(10) at 73/1000 under nominal 0.05. The current acceptance rule rejects both, for different reasons; the AR(2) result alone is not evidence of over-rejection at the conventional 0.05 level, whereas the AR(10) result is a stronger calibration warning. Neither result licenses changing thresholds after observing outcomes.
- Independent eligible secondary real-domain replications remain `0/2`.

These observations motivate review. They do not identify a uniquely correct replacement null family.

## Required review before freezing a confirmatory protocol

An independent reviewer should document:

1. The scientific estimand and the temporal structure the null must preserve.
2. Why the selected null family follows from scientific assumptions rather than the observed endpoint result.
3. Parameter estimation, model-order selection, model-selection uncertainty, fit failures, boundary-selected fits, and invalid surrogate handling.
4. Calibration scenarios spanning relevant short-memory orders, plausible long-memory behavior, periodic structure, nonstationarity, nuisance structure, and finite-sample effects, with each scenario justified before outcomes are examined.
5. Type-I error and power evaluation, Monte Carlo uncertainty, and a predeclared rule for evaluating the calibration suite as a whole, including the risk of falsely failing one of many scenarios.
6. Reproducible seeds, software versions, protocol ID, acceptance criteria, and a fresh-validation plan.
7. Whether the protocol is adequate for the intended scientific question, not merely whether it avoids boundary saturation.

## Prospective change control

- Commit the approved protocol and calibration plan before generating or inspecting new confirmatory endpoint results.
- Use fresh validation runs after any protocol amendment.
- Label already exposed or previously computed endpoint analyses exploratory/post-observation; do not retroactively call them preregistered.
- Do not choose HadCET windows or INDPRO transformations based on alpha, p-values, plots, or other endpoint outcomes.
- Keep HadCET and INDPRO unapproved until provenance, independence, eligibility, and the null prerequisite are resolved.
- Keep cosmic-ray data excluded from replication unless its continuity, missingness, provenance, and eligibility criteria are met prospectively.

## Authority

This document grants no scientific claim support, no replication credit, and no claim-promotion authority. The claim remains `UNDER_INVESTIGATION`.
