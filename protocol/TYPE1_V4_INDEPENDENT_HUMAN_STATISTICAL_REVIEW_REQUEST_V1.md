# Independent Human Statistical Review Request
## HCM Type-I Calibration V4 Candidate

Status: REQUEST FOR REVIEW — NOT AN APPROVAL
Protocol freeze: NOT_FROZEN
Confirmatory execution: NOT_AUTHORIZED
Claim support: false
Promotion authority: false

## 1. Purpose

An independent human statistical review is requested before any
confirmatory Type-I calibration or power analysis is authorized.

The reviewer is asked to evaluate the statistical estimand,
data-generating processes, null procedure, implementation
equivalence, acceptance-rule design, Monte Carlo precision,
invalid-attempt policy, and reproducibility controls.

This request does not approve or freeze the protocol.
It does not authorize execution.
It does not ask the reviewer to endorse HCM as a theory of
consciousness or as a general theory of reality.

## 2. Repository and review identity

Repository:
https://github.com/AhmedPeaRL/maximal-one

Review branch:
review/type1-v4-remediation

Candidate review commit:
MUST BE FILLED WITH THE FINAL REVIEW SNAPSHOT COMMIT SHA

Review snapshot artifact:
MUST BE FILLED AFTER SNAPSHOT GENERATION

Governance inventory artifact:
MUST BE FILLED WITH THE FINAL INVENTORY ARTIFACT ID

Governance inventory source commit:
MUST MATCH THE REVIEW COMMIT

Protocol matrix:
protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json

V4 acceptance-rule record:
protocol/TYPE1_V4_ACCEPTANCE_RULE_DECISION_RECORD.md

Historical acceptance-rule record:
protocol/TYPE1_ACCEPTANCE_RULE_DECISION_RECORD_V2.md

The reviewer must receive the exact snapshot manifest and
SHA256SUMS file. A branch name or mutable URL alone is not
a sufficient review identity.

## 3. Reviewer attribution and independence

Reviewer name:
[REQUIRED]

Academic / professional affiliation:
[REQUIRED]

Relevant statistical qualifications:
[REQUIRED]

Relevant publications or methodological work:
[REQUIRED]

Experience with Monte Carlo testing, time series, spectral
methods, surrogate testing, or Type-I error calibration:
[REQUIRED]

Prior involvement in this repository or project:
[REQUIRED — state NONE if none]

Financial, professional, collaborative, or personal conflicts:
[REQUIRED — state NONE if none]

Date of review:
[REQUIRED]

Attributable written confirmation or signature:
[REQUIRED]

The reviewer must disclose any prior involvement.
The project authors must not describe a reviewer as independent
without a documented basis for that description.

AI-generated analysis is not an independent human review.

## 4. V4 candidate design under review

The V4 candidate currently declares:

- Nine stationary Gaussian AR scenarios.
- 2,000 requested outer repetitions per scenario.
- 1,000 requested surrogate fits per outer repetition.
- Sample size: 3,328.
- DGP burn-in: 2,000.
- Nominal test level: 0.05.
- Candidate master seed: 20261021.
- Seed schedule intended to be invariant to shard order.
- Invalid attempts are preserved and block a scenario pass.
- Missing requested attempts cannot be silently dropped.
- Unresolved surrogate shortfalls block a pass.
- Acceptance rule: null / unresolved.
- Historical 0.075 ceiling: not justified or approved.
- Freeze state: NOT_FROZEN.

The candidate matrix is a governance and consistency record.
It is not an approved confirmatory protocol.

The reviewer must inspect the exact JSON file in the snapshot,
not rely solely on this summary.

## 5. Scenario design

The V4 candidate includes the following nine scenarios:

1. AR(1), phi = [0.4]
2. AR(2), phi = [0.45, -0.10]
3. AR(5), phi = [0.2, 0.1, 0.05, 0.025, 0.0125]
4. AR(10), phi = [0.15, 0.08, 0.05, 0.03, 0.02,
   0.015, 0.01, 0.008, 0.006, 0.004]
5. AR(1), phi = [0.7]
6. AR(1), phi = [0.9]
7. AR(1), phi = [0.97]
8. In-band resonant AR(2), phi =
   [1.78580646236606, -0.81],
   target peak frequency 0.02 cycles/sample,
   root radius 0.90.
9. In-band resonant AR(2), phi =
   [1.8790513325895442, -0.9409],
   target peak frequency 0.04 cycles/sample,
   root radius 0.97.

The reviewer must independently assess:
- stationarity of every specified process;
- parameterization and root convention;
- numerical correctness of the resonant scenarios;
- adequacy and rationale of the scenario coverage;
- whether additional scenarios are necessary;
- whether the scenarios represent the intended null family;
- whether the sample size and burn-in are appropriate.

Any proposed amendment must be prospective, reasoned, and
recorded before confirmatory execution.

## 6. Estimand and test definition

Please define and assess the precise Type-I error estimand.

The intended operational quantity is the probability that the
complete implemented test rejects under each declared null DGP.

Please determine whether:
- the rejection event is defined unambiguously;
- the empirical rejection proportion estimates the intended quantity;
- the nominal alpha = 0.05 is appropriate;
- the endpoint and null procedure are mathematically specified;
- the estimand is per-scenario or suite-level;
- the proposed interpretation is statistically defensible.

Please distinguish calibration under the nine synthetic DGPs
from adequacy of the stochastic null for any real-world series.

## 7. Production-equivalence review

The declared production-equivalence target includes:

- endpoint: canonical_primary_alpha;
- frequency band: open interval (0.01, 0.05);
- Welch nperseg: 1024;
- Welch window: Hann;
- Welch detrend: linear;
- Welch scaling: density;
- Welch average: mean;
- null family: stationary Gaussian AR(p);
- candidate AR order range: 1 through 20;
- model selection: AIC;
- trend: constant;
- stationarity required;
- common effective observations using maximum candidate-order hold-back;
- refitting each surrogate;
- alternative direction: observed alpha greater than null;
- upper-tail test;
- add-one Monte Carlo p-value:
  (exceedances + 1) / (valid_surrogates + 1);
- rejection when p-value <= 0.05;
- requested surrogates: 1,000;
- surrogate-generation burn-in: 1,000.

Please determine whether the calibration runner is equivalent
to the actual production implementation for all scientifically
relevant steps, including:
- preprocessing and endpoint calculation;
- model fitting and order selection;
- stationarity enforcement;
- surrogate generation;
- refitting;
- invalid-fit behavior;
- valid-surrogate denominator;
- p-value calculation;
- rejection decision.

Please identify any differences that could change the Type-I
operating characteristics.

Engineering equivalence tests are evidence for the tested paths
and configurations only. They do not replace this methodological
review.

## 8. Acceptance-rule decision

The acceptance rule is deliberately unresolved.

Historical rule:
- two-sided 95% Wilson interval must contain 0.05;
- upper endpoint must be <= 0.075.

Candidate alternative:
- one-sided 95% Wilson upper confidence bound <= 0.075.

These are not equivalent.

The historical classifications must remain unchanged.
The 0.075 ceiling is not approved merely because it appeared
in a historical or candidate document.

Please recommend a complete prospective rule, including:

1. Confidence-bound or test procedure.
2. Confidence level and sidedness.
3. Numerical acceptance boundary.
4. Scientific rationale for any tolerance above nominal alpha.
5. Per-scenario acceptance.
6. Suite-level acceptance and multiplicity implications.
7. Planned number of outer repetitions.
8. Monte Carlo precision and uncertainty.
9. Consequences of false acceptance and false rejection.
10. Treatment of incomplete scenarios and invalid attempts.

Do not choose a rule solely because it makes previous results pass.

The recommendation must be mathematically explicit and
applicable to the exact reviewed snapshot.

## 9. Invalid attempts and denominator policy

The candidate protocol requires:
- every requested outer attempt to remain represented;
- invalid attempts to retain their failure reasons;
- no silent dropping or replacement;
- no conversion of invalid attempts into non-rejections;
- unresolved requested-surrogate shortfalls to block a pass;
- missing indices and duplicate indices to block a pass.

Please evaluate whether this policy is statistically appropriate
and whether the implementation enforces it correctly.

Please identify any additional failure modes that require
pre-registration or explicit handling.

## 10. Monte Carlo feasibility and precision

The candidate design requests 2,000 outer attempts per scenario
and 1,000 surrogates per outer attempt.

Please assess:
- whether the number of outer attempts is adequate;
- whether the planned confidence-bound precision is adequate;
- the computational burden and feasibility;
- whether a pilot can estimate runtime without contaminating
  confirmatory results;
- whether the seed schedule is suitable;
- whether the planned stopping and invalid-attempt rules
  are coherent.

A pilot or engineering run must not be represented as
confirmatory calibration.

## 11. Historical evidence — preserve as historical

The earlier historical V1 results were recorded under the
historical two-sided Wilson rule:

- AR(1): 52/1000; interval [0.039873, 0.067556].
- AR(2): 60/1000; interval [0.046896, 0.076471].
- AR(5): 49/1000; exact interval must be retrieved from the
  original immutable historical artifact.
- AR(10): 73/1000; interval [0.058459, 0.090809].

Historical overall outcome: NOT_PASSED.

Do not reconstruct or invent the AR(5) interval.
Do not alter historical files or classifications.
Any reanalysis under a different rule must be labeled as
a new analysis and must preserve the original record.

## 12. Scope limitations

A successful synthetic Type-I calibration would support only
the operating characteristics of the tested implementation
under the explicitly declared DGPs and protocol.

It would not by itself establish:
- universal stochastic-null adequacy;
- real-domain replication;
- a general theory of consciousness;
- the truth of HCM as a Model of Everything;
- claim support or promotion authority.

The reviewer is not being asked to validate claims beyond
the statistical scope of this protocol.

## 13. Required reviewer disposition

Select exactly one:

- ACCEPT
- ACCEPT WITH CONDITIONS
- REVISE AND RESUBMIT
- REJECT

Decision:
[REQUIRED]

Detailed rationale:
[REQUIRED]

Required amendments:
[REQUIRED]

Limitations:
[REQUIRED]

Unresolved issues:
[REQUIRED]

Reviewed commit SHA:
[REQUIRED]

Reviewed protocol file SHA-256:
[REQUIRED]

Reviewed matrix SHA-256:
[REQUIRED]

Reviewed runner SHA-256:
[REQUIRED]

Review date:
[REQUIRED]

Reviewer signature or attributable confirmation:
[REQUIRED]

## 14. Explicit non-authorization

This review request does not authorize:
- protocol freeze;
- confirmatory Type-I calibration;
- power analysis;
- production-null freeze;
- claim support;
- promotion authority.

Any later protocol freeze and execution authorization must be
separate, explicit, attributable, and bound to the exact
reviewed commit and file hashes.
