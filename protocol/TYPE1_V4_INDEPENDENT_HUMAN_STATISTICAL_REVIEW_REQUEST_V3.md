# Independent Human Statistical Review Request — Type-I Calibration V4 (V3)

Status: DRAFT — AWAITING ATTRIBUTABLE INDEPENDENT REVIEW
This is a review-only request. No protocol freeze or execution authority is granted.

## 1. Repository and exact review identity

Repository:
https://github.com/AhmedPeaRL/maximal-one

Scientific target commit:
`ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`

Current review branch commit:
`ff640e54e6996dd2a4ab0af061fa43e2151c14a2`

Current main commit:
`9749de9253f144eeda9e1b60cb219cfc5f201ecc`

Latest inventory:
- Run `43739431060`
- Artifact `14172180461`
- Inventory SHA-256 `4ee4335d5807c0a90ac668637a2bd55277ae9b6ce442af316f65f22a24f17a89`

Latest self-contained snapshot:
- Run `43739541831`
- Artifact `14172275278`
- Snapshot manifest SHA-256 `b90f926eb4273284a34e660911485b42105fc0eab2f0174b101a3b359d506462`
- Inner snapshot archive SHA-256 `b0ad0fd5e5c54f0b63d95a193afb12c4d60c582ee2127c7412eeade7f0bb866f`
- Snapshot identity certificate confirms target `ad106...`, main `9749de...`, and 289/289 files present with extraction verification passed.

Inventory artifact:
https://github.com/AhmedPeaRL/maximal-one/actions/runs/43739431060/artifacts/14172180461

Snapshot artifact:
https://github.com/AhmedPeaRL/maximal-one/actions/runs/43739541831/artifacts/14172275278

The scientific target is intentionally distinct from the later review-branch workflow commits. Please review the exact target snapshot and the exact files/hashes below, not an unspecified moving branch head.

## 2. Exact statistical materials

Primary V4 draft matrix:
`protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_DRAFT.json`

SHA-256:
`b6c6354558ca6a0685f5731da11da656268c1c3e44599f84f5540ad9725f11af`

Scenario runner:
`analysis/calibrate_null_type1_scenario.py`

SHA-256:
`a8e5e7d1730eb7cc1650a9c4934f472f37b85829f4b713e9d048ee30f054705f`

Calibration implementation:
`analysis/calibrate_null_type1.py`

SHA-256:
`faf96a9e969f1060d51142503521e2857ff0b4c11cfa53fbe4fab6f0c318b86a`

Acceptance decision record:
`protocol/TYPE1_V4_ACCEPTANCE_RULE_DECISION_RECORD.md`

SHA-256:
`3c87b27a3512d89bba362c7ed9e99bc22388d2372471ec14d80db2e736d040ac`

Calibration workflow:
`.github/workflows/null-type1-calibration.yml`

SHA-256:
`e239fe886475a0c716def6a06da5c1bff45a1f1b3fac50e272567a116c79aa72`

Runtime pilot workflow:
`.github/workflows/type1-calibration-runtime-pilot.yml`

SHA-256:
`43e83a217f2a0aa8faf615cb8f89b7484e98c2300d729a9225c9f9578027f76b`

The separate V4 candidate matrix previously received `REVISE_AND_RESUBMIT`. It is not the active V4 draft and must not be silently substituted.

## 3. Candidate design under review

The V4 draft specifies:
- Nine stationary Gaussian AR data-generating scenarios.
- Sample size n = 3328.
- DGP burn-in = 2000.
- 2,000 outer repetitions per scenario.
- 1,000 surrogate replications per outer repetition.
- 18,000,000 total surrogate fits.
- Candidate master seed = 20261021.
- AR model-order selection by AIC over orders 1 through 20.
- Two in-band resonant AR(2) scenarios, with candidate frequencies 0.02 and 0.04 and root radii 0.90 and 0.97.

The exact matrix file, not this summary, is authoritative for parameters.

## 4. Historical results and governance boundary

Historical Type-I calibration V1 remains `NOT_PASSED`.

The historical two-sided 95% Wilson procedure and its results must not be changed retrospectively. The historical 0.075 upper-bound ceiling is not approved for V4 merely because it appeared in an earlier draft.

The V4 acceptance-rule decision record remains OPEN. No complete executable acceptance rule has been approved. No numeric `alpha_max` has been authorized.

Formal calibration, confirmatory execution, protocol freeze, claim support and promotion authority remain false.

## 5. Independent statistical questions

Please independently assess:
1. Whether the nine DGP scenarios adequately represent the intended stationary-null family.
2. Whether the near-boundary AR(2) parameterizations are correctly specified, stationary and numerically stable.
3. Whether n=3328, burn-in 2000, 2,000 outer repetitions and 1,000 surrogates per repetition are adequate.
4. Whether AIC order selection over AR(1) through AR(20) is appropriate, including selection bias and boundary behavior.
5. Whether the acceptance family should use a one-sided confidence upper bound per scenario, a two-sided interval with a justified upper tolerance, or another procedure.
6. If a maximum Type-I tolerance is appropriate, what numeric `alpha_max` is justified and why.
7. Whether every required scenario must pass individually and the correct global interpretation.
8. Whether simultaneous coverage or multiplicity adjustment is required.
9. How invalid, failed, non-convergent or numerically unstable repetitions must be counted. Silent deletion/replacement is not acceptable.
10. Whether Monte Carlo precision is adequate to distinguish calibration from meaningful inflation.
11. Whether power simulations and alternative DGPs are sufficient.
12. Whether any part should be rejected or redesigned before formal execution.

Please distinguish mathematical correctness, statistical adequacy, computational reproducibility and scientific interpretation.

## 6. Attribution and prior exposure

Please provide:
- Full name and current institutional affiliation.
- Relevant qualifications/publications.
- Specific expertise in Type-I calibration, dependent time series, resampling and Monte Carlo methods.
- Financial, professional, collaborative, supervisory or intellectual conflicts.
- Whether you have previously interacted with this repository, author or project.
- Whether you have seen historical endpoint-like results.
- A dated attributable written report with decision `ACCEPT`, `REVISE`, `REJECT` or `OUT OF SCOPE`.
- Explicit limitations and conditions for reconsideration.

Historical endpoint-like values appeared in an earlier CI log, run `38729766378`. Whether the reviewer personally inspected those values is unknown. Please state whether this affects blindness or confirmatory status.

An automated scanner or AI-generated summary is not an independent human statistical review.

## 7. Decision boundary

This request authorizes review only. It does not authorize formal calibration, confirmatory execution, protocol freeze, claim support or promotion. No HCM endorsement is requested.
