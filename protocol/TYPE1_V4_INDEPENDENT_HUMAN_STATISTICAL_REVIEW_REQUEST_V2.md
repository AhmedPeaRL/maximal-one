# Independent Human Statistical Review Request — Type-I Calibration V4

Status: DRAFT — AWAITING ATTRIBUTABLE INDEPENDENT REVIEW
No protocol freeze or execution authority is granted.

## 1. Repository and exact review identity

Repository:
https://github.com/AhmedPeaRL/maximal-one

Scientific target commit:
ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876

Review workflow-definition commit:
3a158e8f902179cdd543e92153032ae409faaea0

Latest inventory artifact:
Run 43724022202
Artifact 14165228673
Inventory SHA-256:
f528652046f4d855e4dd1abd303a2d85ec06740667d90f42ae206451d60ed5e5

Latest snapshot artifact:
Run 43724143560
Artifact 14166116356
Archive SHA-256:
63e8a0d3b5107da4ec3d30bda0e0cf79e9c58c59a508bf31df87c2ebe2177c72

Snapshot manifest SHA-256:
849c12ea44645264e9c0cbff08f78686dffb33450c3988dee289040f1f26ceba

Snapshot inner ZIP SHA-256:
ed5751c966aa874d2d4d3fc2ee2f4b657579281e192aaf0381afe1453768aeb8

Snapshot certificate SHA-256:
4ea720b134cd8cc09304300e2037ba2871bb9709bcea7fbf6f2b19b5b131ccd8

Snapshot scope:
289 selected files; 289 present; extraction verification passed.

Inventory artifact:
https://github.com/AhmedPeaRL/maximal-one/actions/runs/43724022202/artifacts/14165228673

Snapshot artifact:
https://github.com/AhmedPeaRL/maximal-one/actions/runs/43724143560/artifacts/14166116356

## 2. Exact statistical materials

Primary V4 draft matrix:
protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_DRAFT.json

SHA-256:
b6c6354558ca6a0685f5731da11da656268c1c3e44599f84f5540ad9725f11af

Scenario runner:
analysis/calibrate_null_type1_scenario.py

SHA-256:
a8e5e7d1730eb7cc1650a9c4934f472f37b85829f4b713e9d048ee30f054705f

Calibration implementation:
analysis/calibrate_null_type1.py

SHA-256:
faf96a9e969f1060d51142503521e2857ff0b4c11cfa53fbe4fab6f0c318b86a

Acceptance decision record:
protocol/TYPE1_V4_ACCEPTANCE_RULE_DECISION_RECORD.md

SHA-256:
3c87b27a3512d89bba362c7ed9e99bc22388d2372471ec14d80db2e736d040ac

Calibration workflow:
.github/workflows/null-type1-calibration.yml

SHA-256:
e239fe886475a0c716def6a06da5c1bff45a1f1b3fac50e272567a116c79aa72

Runtime pilot workflow:
.github/workflows/type1-calibration-runtime-pilot.yml

SHA-256:
43e83a217f2a0aa8faf615cb8f89b7484e98c2300d729a9225c9f9578027f76b

The separate V4 candidate matrix has a prior outcome of REVISE_AND_RESUBMIT. It is not the active V4 draft design and must not be silently substituted for it.

## 3. Candidate design under review

The V4 draft specifies:

- Nine stationary Gaussian AR data-generating scenarios.
- Sample size n = 3328.
- DGP burn-in = 2000.
- 2000 outer repetitions per scenario.
- 1000 surrogate replications per outer repetition.
- 18,000,000 total surrogate fits.
- Candidate master seed = 20261021.
- AR model-order selection by AIC over orders 1 through 20.
- Two near-boundary resonant AR(2) scenarios, with candidate frequencies 0.02 and 0.04 and root radii 0.90 and 0.97.

The exact matrix file, rather than this summary, is the authoritative parameter specification.

## 4. Historical results and governance boundary

Historical Type-I calibration V1 remains NOT_PASSED.

The historical two-sided 95% Wilson procedure and its results must not be changed retrospectively.

The historical 0.075 upper-bound ceiling is not approved for V4 merely because it appeared in an earlier draft.

The V4 acceptance-rule decision record remains OPEN. No complete executable acceptance rule has been approved. No numeric alpha_max has been authorized.

Formal calibration, confirmatory execution, protocol freeze, claim support and promotion authority remain false.

## 5. Questions requiring independent statistical judgment

Please independently assess:

1. Whether the nine DGP scenarios adequately represent the intended stationary-null family.
2. Whether the near-boundary AR(2) parameterizations are correctly specified, stationary and numerically stable.
3. Whether n=3328, burn-in 2000, 2000 outer repetitions and 1000 surrogates per repetition are adequate.
4. Whether AIC order selection over AR(1) through AR(20) is appropriate, including selection bias and boundary behavior.
5. Whether the proposed Type-I acceptance family should use:
   - a one-sided confidence upper bound per scenario;
   - a two-sided interval with a justified upper tolerance;
   - or another procedure.
6. If a maximum Type-I tolerance is appropriate, what numeric alpha_max is justified and why.
7. Whether every required scenario must pass individually, and the correct global interpretation of that rule.
8. Whether simultaneous coverage or multiplicity adjustment is required for the intended claim.
9. How invalid, failed, non-convergent or numerically unstable repetitions must be counted. Silent deletion or replacement is not acceptable.
10. Whether the Monte Carlo precision is adequate to distinguish a calibrated procedure from meaningful inflation.
11. Whether power simulations and alternative DGPs are sufficient, and what additional scenarios are necessary.
12. Whether any part of the proposed procedure should be rejected or redesigned before formal execution.

Please distinguish mathematical correctness, statistical adequacy, computational reproducibility and scientific interpretation.

## 6. Required reviewer attribution

Please provide:

- Full name and current institutional affiliation.
- Relevant qualifications and publications.
- Specific expertise relevant to Type-I error calibration, dependent time series, resampling and Monte Carlo methods.
- Any financial, professional, collaborative, supervisory or intellectual conflicts of interest.
- Whether you have previously interacted with this repository, author or project.
- Whether you have seen any historical endpoint-like results.
- A dated written report with a clear decision: ACCEPT, REVISE, REJECT or OUT OF SCOPE.
- Explicit limitations and any conditions for reconsideration.

A report must be attributable to the named reviewer. An automated scanner output or AI-generated summary is not an independent human statistical review.

## 7. Decision boundary

This request authorizes review only.

It does not authorize formal calibration, confirmatory execution, protocol freeze, claim support, or promotion.

No HCM endorsement is requested.
