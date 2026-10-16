# Prospective Confirmatory Protocol Freeze — Checklist

## Status

`NOT_FROZEN — DO_NOT_RUN_CONFIRMATORY_ANALYSIS`

This checklist is a freeze gate, not a frozen protocol. Do not describe the protocol as preregistered or confirmatory until every mandatory item is resolved, the document is versioned and independently timestamped, and confirmation outcomes have not been inspected.

---

## Gate A — Null-family adequacy

* [ ] Common-sample AR(p) capacity audit completed; artifact preserved.
* [ ] Residual diagnostics use model-adjusted degrees of freedom.
* [ ] Stationarity, parameter stability, and surrogate refitting reviewed.
* [ ] Type-I calibration passes the existing declared acceptance rule in every required scenario.
* [ ] Failed calibration scenarios remain visible.
* [ ] Null-family selection rule is specified without using future confirmation outcomes.
* [ ] Independent technical review is recorded.
* [ ] The candidate null family is explicitly approved or rejected, with reasons.

If any item is open, the protocol remains `NOT_FROZEN`.

---

## Gate B — Frozen scientific specification

Before confirmation, the versioned protocol must specify:

1. **Hypothesis and estimand:** exact claim, operational endpoint, and effect direction.
2. **Primary endpoint:** estimator, frequency band, Welch/FFT settings, preprocessing, missing-data rules, and provenance.
3. **Primary null:** model family, parameters, estimation method, order-selection rule, burn-in, surrogate count, refitting rule, and failure handling.
4. **Test definition:** alternative, tail, statistic, p-value formula, alpha level, and Monte Carlo precision rule.
5. **Calibration:** scenarios, repetition counts, seed policy, interval method, acceptance rule, and failure action.
6. **Eligibility:** inclusion/exclusion rules, minimum length, cadence/timestamp rules, frequency-bin requirements, and non-finite-value handling.
7. **Replication:** at least two independent secondary real domains; same endpoint, null family, direction, tail, and domain-level rejection requirement.
8. **Multiplicity:** declared multiple endpoints, datasets, subgroup tests, and the prespecified control strategy.
9. **Stopping rule:** fixed sample and surrogate counts; no outcome-dependent extension or optional stopping.
10. **Failure policy:** actions for fitting failures, failed residual checks, failed calibration, ineligible domains, and non-rejection of the null.
11. **Reproducibility:** exact commit, dependency lock, source-data hashes, protocol hash, and clean-checkout instructions.
12. **Data separation:** distinguish method-development data from untouched confirmation data.
13. **Amendments:** record each amendment and date; do not call post-observation amendments preregistered.
14. **Review and timestamp:** independent review and durable timestamp before confirmation data are inspected.

---

## Gate C — Claim promotion remains blocked

* [ ] Appropriate primary stochastic null rejected under the frozen test.
* [ ] Calibration and internal-consistency gates pass.
* [ ] Two independent secondary real domains meet eligibility and show the required domain-level result.
* [ ] Clean-checkout computational reproduction and fingerprint match pass.
* [ ] Adversarial controls and exclusions pass.
* [ ] Final report distinguishes computational reproducibility from scientific replication.
* [ ] No diagnostic-only result is substituted for a primary confirmatory result.

---

## Non-negotiable safeguards

* Do not change the null, order range, endpoint, tail, alpha level, minimum sample size, replication count, or acceptance thresholds after seeing confirmation results to improve the outcome.
* Do not count synthetic, shuffled, derived, or null datasets as independent real-domain replications.
* Do not use a permutation-null p-value as a substitute for the primary temporal stochastic-null p-value.
* A successful workflow is not itself evidence that the scientific claim is true.
* Until all gates are satisfied, keep claim support and promotion authority false.
