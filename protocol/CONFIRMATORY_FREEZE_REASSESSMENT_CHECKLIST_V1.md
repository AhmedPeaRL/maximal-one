# Confirmatory Freeze Reassessment Checklist — V1

**Default state:** `NOT_FROZEN`  
**Confirmatory endpoint authorization:** `false`  
**Claim promotion authority:** `false`

A checked box requires a committed artifact or attributable review record. A passing code test alone does not satisfy a scientific review item.

## A. Phenomenon and estimand
- [ ] Independent reviewer confirms that “excess spectral persistence” matches the intended scientific question.
- [ ] H0 and H1 are stated in operational terms.
- [ ] Target-versus-nuisance table is complete and approved.
- [ ] Treatment of trend, regimes, seasonality, cadence/gaps, autocorrelation, tails/outliers, heteroskedasticity, possible long-memory, measurement error, and source revisions is justified.

## B. Null and fitting procedure
- [ ] Candidate-family comparison used development/calibration data only and did not use candidate endpoint values or p-values for selection.
- [ ] Null family, parameter fitting, model-selection rule, candidate range, root/stationarity constraints, surrogate generation, refitting, burn-in, and minimum valid surrogate count are specified.
- [ ] Boundary saturation and all fit/refit failures have a prespecified disposition.
- [ ] Null preserves relevant nuisance structure without removing the target by construction.

## C. Type-I and power calibration
- [ ] Historical four-scenario results and failures preserved unchanged.
- [ ] All four historical scenarios rerun on one exact commit, with the checked-out SHA recorded in each job.
- [ ] The existing historical rule applied without retroactive amendment.
- [ ] Expanded DGP matrix and scenario membership frozen before execution.
- [ ] Per-scenario and suite-level acceptance rules, interval method, Monte Carlo precision/stopping rule, dependence handling, and invalid-fit policy approved before fresh runs.
- [ ] Type-I calibration passes all required predeclared criteria.
- [ ] Power and false-negative criteria pass at the declared sample size/effect sizes, with Monte Carlo uncertainty.
- [ ] Artifact hashes, seeds, environment and dependencies recorded.

## D. Empirical reference series
- [ ] Each series registered before parsing/endpoint computation.
- [ ] Raw snapshots preserved byte-for-byte with retrieval timestamps and SHA-256.
- [ ] Parsed hashes, cadence, timestamps, gaps, missingness, preprocessing and source-vintage checks verified.
- [ ] Prior exposure is recorded honestly as `YES`, `NO`, or `UNKNOWN`; `UNKNOWN` is not changed to `NO`.
- [ ] Empirical series are interpreted as nuisance diagnostics, not as known-truth Type-I evidence.
- [ ] No empirical reference series is automatically counted as a replication domain.

## E. Replication eligibility
- [ ] At least two secondary real domains pass measurement, provenance, source-vintage, independence/shared-nuisance, exposure, and protocol-compatibility review.
- [ ] Selection and all analysis decisions precede endpoint observation on untouched confirmation data.
- [ ] Missing data are handled under a prospectively approved rule; no silent imputation/drop.
- [ ] Same endpoint, direction, tail, estimator, null, and decision rule are used.

## F. Exact freeze and decision
- [ ] Full protocol committed before confirmation endpoint calculation/inspection.
- [ ] Freeze commit SHA is a full 40-character SHA and is an ancestor of the confirmation run commit.
- [ ] SHA-256 of frozen registry/config matches the freeze lock and the bytes at the freeze commit.
- [ ] Clean-checkout run reproduces protocol identity and dependencies.
- [ ] Attributable independent reviewer signs or otherwise records a dated decision with expertise, conflicts, exact commit and artifact hashes.
- [ ] A new acceptance decision record is committed.
- [ ] Only after all prior items pass may the freeze status be reconsidered.

## Decision rule

If any mandatory item is unchecked, retain:
- `confirmatory_protocol_frozen = false`;
- `confirmatory_inference_available = false`;
- `claim_promotion_allowed = false`;
- `approved_independent_secondary_domains = 0/2` unless separately verified evidence proves otherwise.

A freeze is a protocol-control decision, not a scientific result. It does not establish HCM causation, consciousness, universality, mechanism, or new physics.
