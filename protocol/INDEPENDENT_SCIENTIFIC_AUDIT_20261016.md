# Independent Scientific Audit — 2026-10-16

## Scope and authority

This is an independent review of the supplied repository snapshot and recorded calibration artifacts.
It is not a claim-support report, a prospective registration, or evidence of successful fresh validation.
No acceptance threshold is changed by this document.

Scientific claim status remains UNDER INVESTIGATION.
Claim promotion is NOT AUTHORIZED.

---

## 1. Type-I calibration

The recorded calibration design uses four synthetic Gaussian AR scenarios, 1,000 outer repetitions per scenario, 200 surrogates per test, and sample length 1,024.
The recorded acceptance rule requires the two-sided Wilson 95% interval to contain 0.05 and its upper endpoint to be no greater than 0.075.

Recorded outcomes:

- AR(1), phi=0.4: 52/1000 rejections; rate 0.052; Wilson interval [0.039873, 0.067556]. Limited synthetic-scope pass.
- AR(5), low-order coefficients: 49/1000; rate 0.049; Wilson interval [0.037261, 0.064191]. Limited synthetic-scope pass.
- AR(2), phi=(0.45,-0.10): 60/1000; rate 0.060; Wilson interval [0.046896, 0.076471]. Fails the upper-bound criterion.
- AR(10), low-order coefficients: 73/1000; rate 0.073; Wilson interval [0.058459, 0.090809]. Fails both interval-containment and upper-bound criteria.

These results establish failure under the declared gate, not the root cause.
The two failed scenarios must remain recorded as failures.
Do not change the acceptance threshold, delete runs, or relabel failures as passes.

Required follow-up: independently audit p-value computation, surrogate generation, parameter estimation and refitting, invalid-run handling, random-number generation, and the outer-replicate sampling assumptions.
Reproduce the recorded artifacts from their exact source revision before attributing a root cause.

---

## 2. Acceptance-rule operating characteristics

The repository's operating-characteristics audit reports that, under its independent Bernoulli model with true rejection probability 0.05 and n=1000, the current rule accepts 86.83% of individual scenarios.
Its corresponding false-failure probability is 13.17% per scenario.
Under an additional independence assumption across four scenarios, the probability of at least one false failure is approximately 43.16%.

This is a property of the acceptance rule under the stated model, not proof that it caused either observed failure.
It does not authorize changing the gate after observing results.

---

## 3. Stochastic-null capacity

The recorded primary null audit reports 937/1000 surrogate refits selecting the maximum AR order 20, a boundary fraction of 0.937 against a review threshold of 0.50.
This triggers formal model-capacity and null-adequacy review.
It does not establish, reject, or falsify the scientific hypothesis.

The equal-effective-observation AIC comparison repair is a computational correction, not proof of model adequacy.

Required follow-up: document residual diagnostics, stationarity and fitting failures, observed-fit and surrogate boundary behavior, Type-I calibration across predeclared scenarios, and the scientific assumptions preserved by the surrogate generator.
Do not select a replacement null based on favorable endpoint results.

---

## 4. Prospective confirmation

The current AR(p)/AIC procedure remains exploratory.
The confirmatory null, selection rule, adequacy thresholds, surrogate generator, and replication registry are not frozen.
Historical results are not preregistered confirmation.

Before any new confirmatory analysis, freeze and independently timestamp the dataset identity and hash, primary endpoint, estimator, frequency band, normalization, direction, tail, null family, model-selection rule, adequacy criteria, calibration plan, exclusion policy, replication registry, multiplicity plan, and analysis code revision.

The timestamp and external record must establish that the protocol preceded access to confirmatory outcomes.
A Git commit timestamp alone does not prove that the outcomes were unobserved.

---

## 5. Secondary-domain eligibility

The supplied HadCET and FRED:INDPRO manifest records identify preserved snapshots but mark both sources as pending time and provenance audit.
They are not approved replication domains.

Assess source provenance, measured variable, cadence, time ordering, missingness, preprocessing, common confounders, dependence on the primary domain, and endpoint eligibility before examining confirmatory outcomes.
Do not select domains using alpha, p-values, or favorable results.

---

## 6. Clean-checkout reproduction

Reproduce the audit from a fresh public checkout at an exact commit.
Record the commit SHA, dependency installation outcome, commands, exit codes, artifact hashes, and differences from the preserved results.
Computational reproducibility is not independent scientific replication.

---

## Decision

- Claim status: UNDER INVESTIGATION.
- Claim promotion: BLOCKED.
- Type-I gate: unchanged.
- Failed calibration scenarios: preserved.
- Current AR(p)/AIC null: exploratory; capacity review required.
- Confirmatory protocol: not frozen.
- Secondary-domain replication: not approved pending provenance review.
- Fresh prospective confirmation: not completed.
- Independent scientific replication: not demonstrated.

No result in this report supports a causal HCM claim, universality, mechanism, or consciousness claim.

---

## Audit limitations

This report is based on the supplied repository archive and recorded artifact register.
It does not independently establish that the current live branch contains every archived file, that all linked workflow jobs passed, or that a fresh clean-checkout run has succeeded.
