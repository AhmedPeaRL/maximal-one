# Prospective Confirmatory Freeze Gate — 2026-10-17

**Status:** `NOT_FROZEN`  
**Authorization:** `DO_NOT_RUN_CONFIRMATORY_ANALYSIS`  
**Claim status:** `UNDER_INVESTIGATION`

## Purpose

This file records a mandatory stop condition before any future confirmatory analysis. It does not replace the existing protocol draft or alter any scientific threshold. It exists to prevent a new workflow run from being mistaken for confirmation merely because it is reproducible.

## Unresolved mandatory conditions

A confirmatory run is not authorized until every item below is completed, versioned, reviewed, and durably timestamped before the confirmatory endpoint is calculated or inspected:

- [ ] Primary hypothesis, estimand, and endpoint implementation
- [ ] Dataset/source identity, exact source-data hashes, and a documented untouched confirmation dataset/period
- [ ] Prior endpoint exposure audit distinguishing generated, displayed, and personally viewed results
- [ ] Sampling cadence, timestamp, missingness, preprocessing, and exclusion rules
- [ ] Estimator, normalization, frequency band, direction, tail, and multiplicity plan
- [ ] Scientifically justified null family and parameter-estimation/model-selection procedure
- [ ] Surrogate-generation method, burn-in, number of draws, seed policy, invalid-fit policy, and Monte Carlo p-value rule
- [ ] Model adequacy criteria, residual diagnostics, stationarity checks, boundary-saturation policy, and calibration suite
- [ ] Type-I calibration plan and unchanged, prospectively justified acceptance rule
- [ ] At least two secondary domains selected by source/scientific criteria before endpoint observation; provenance and independence reviewed
- [ ] Exclusion and stopping rules, including the consequences of every failed mandatory diagnostic
- [ ] Locked code revision, dependencies, reproducibility commands, artifact schema, and expected hashes
- [ ] Independent methodological review and durable timestamp/registration record

## Current null decision

The stationary Gaussian AR(p) family selected by AIC over orders 1–20 remains exploratory. The recorded capacity diagnostic reaches the maximum order in `937/1000` surrogate refits. Two recorded Type-I calibration scenarios fail the current rule. These results require methodological review; they do not authorize retrospective threshold changes or selection of a null family based on favorable endpoint results.

## Replication decision

Current gate result: `0/2` eligible independent secondary domains. HadCET and INDPRO are structurally measurement-valid but remain unapproved; their endpoint-like estimates were generated and displayed in workflow run `38729766378` before the relevant pre-analysis decisions were completed. Cosmic rays fail the timestamp continuity/run-length check and have unresolved source provenance. Solar-wind data have unresolved cadence/provenance and potential shared solar-cycle nuisance. None may be counted as approved confirmation by changing metadata alone.

## Authorization rule

If any checkbox above remains unchecked, the status must remain `NOT_FROZEN` and confirmatory analysis must not run. Existing exploratory runs may be retained and analyzed as exploratory, but they must not be relabeled as preregistered confirmation. Any post-observation amendment must be explicitly recorded and requires a fresh prospective confirmation design.

**Current decision:** `NOT_READY — DO_NOT_RUN_CONFIRMATORY_ANALYSIS`.

This gate grants no claim support or promotion authority and makes no claim about HCM causation, consciousness, mechanism, or universality.
