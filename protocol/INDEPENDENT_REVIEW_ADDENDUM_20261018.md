# Independent Review Addendum — 2026-10-18

**Repository:** `AhmedPeaRL/maximal-one`  
**Reviewed commit:** `047b84f2c78bdf19e28e283afc1a9800aca32287`  
**Review type:** Independent desk review of the supplied repository snapshot, workflow records, and official source documentation. This is not a substitute for an attributable external statistical-methods reviewer.  
**Scientific claim status:** `UNDER_INVESTIGATION`  
**Claim support:** `false`  
**Promotion authority:** `false`  
**Confirmatory protocol:** `NOT_FROZEN`  
**Approved independent secondary domains:** `0/2`

## 1. Decision

**HOLD CONFIRMATORY ANALYSIS. Do not change the scientific claim, acceptance thresholds, endpoint, or raw candidate snapshots to make a gate pass.** Continue outcome-blind methods review, calibration, source-provenance work, and documentation only. Do not compute new HadUKP or CPIAUCNS candidate endpoints under the current state.

This addendum records the evidence visible on 2026-10-18. It does not claim that the hypothesis is supported or falsified, and it does not grant replication credit or promotion authority.

## 2. Workflow evidence reviewed

### Main workflow — run `39066662709`

- Commit: `047b84f2c78bdf19e28e283afc1a9800aca32287`.
- The `core-proof` job completed successfully, including the canonical computation and reproducibility-related steps.
- The final claim gate produced `status = BLOCKED`, `eligible_replication_domain_count = 0`, and `minimum_replication_domains = 2`.
- `claim_support_granted_by_this_job = false` and `promotion_authority_granted_by_this_job = false`.
- Interpretation: successful computational/reproducibility jobs are not evidence of independent scientific replication or claim support.

Workflow: https://github.com/AhmedPeaRL/maximal-one/actions/runs/39066662709/workflow

### Type-I calibration — run `39064443602`

Recorded results under the currently declared scenario-wise rule:

| Scenario | Rejections / trials | Rate | Wilson 95% interval | Result under current rule |
|---|---:|---:|---|---|
| Gaussian AR(1), phi = 0.4 | 52 / 1,000 | 0.052 | [0.039873, 0.067556] | Passes this scenario only |
| Gaussian AR(2), phi = 0.45, -0.10 | 60 / 1,000 | 0.060 | [0.046896, 0.076471] | Fails: upper endpoint exceeds 0.075 |
| Gaussian AR(5), low-order coefficients | 49 / 1,000 | 0.049 | [0.037261, 0.064191] | Passes this scenario only |
| Gaussian AR(10), low-order coefficients | 73 / 1,000 | 0.073 | [0.058459, 0.090809] | Fails: interval excludes 0.05 and upper endpoint exceeds 0.075 |

Two passing scenarios do not make the suite pass. Preserve the two failures and the current rule. The separate `null-calibration` workflow run `39067017810` succeeding means its audit/contract checks succeeded; it must not be described as evidence that all four scenario calibrations passed. Before treating the four-scenario suite as one same-commit result, record and verify the exact checkout SHA for every scenario job and rerun all declared scenarios on one identified commit if needed.

Calibration workflow: https://github.com/AhmedPeaRL/maximal-one/actions/runs/39064443602/workflow

### Prospective raw-source audit — run `39066915519`

- The source-audit code tests passed.
- HadUKP EWP passed the structural checks in the reported window but remains unapproved for replication.
- CPIAUCNS failed the completeness check because one value is missing at `2025-10-01`.
- Both candidates remain `NOT_APPROVED`; endpoint computation was not performed; claim support and promotion authority remain false.
- The workflow correctly preserved the audit artifact and failed closed because the audit was incomplete/blocked.

Workflow: https://github.com/AhmedPeaRL/maximal-one/actions/runs/39066915519/workflow

### Claim-promotion workflow — run `39066935038`

The eligibility contract failed because no two independent, eligible real-domain replications have been approved. Keep this failure visible. Do not weaken the eligibility gate.

Workflow: https://github.com/AhmedPeaRL/maximal-one/actions/runs/39066935038/workflow

## 3. AR(p), AIC, p = 1..20: decision

**The current AR(p) specification is not approved for confirmatory use.** The repository's primary capacity audit reports 937/1,000 surrogate refits selecting the maximum order 20 (boundary fraction 0.937; declared review threshold 0.50). A separate recorded stream reports 0.947. These are source-scoped estimates and are not required to match across different seeds/streams. Both indicate boundary saturation and require review; neither identifies the correct replacement family by itself.

Boundary saturation can reflect an insufficient candidate range, model-family mismatch, order-selection behavior, or other fitting/data properties. It is not proof that simply increasing the maximum order is correct. Do not extend the cap to 40, select a new family, or tune model settings in response to candidate endpoint values.

The existing reported stochastic-null p-value of `0.999001` is not a rejection of the current null. Historical results after protocol amendments are exploratory/post-observation and must not be relabelled as confirmatory.

## 4. What a defensible null must preserve

The null family must follow the scientific estimand and the null hypothesis, not the most favorable p-value. Before choosing a family, the methods review must state whether the target phenomenon is itself long-memory/spectral persistence or an excess feature beyond ordinary temporal structure. This distinction is critical: a null that preserves the target feature can make a test conservative or test a different question; a null that removes it by construction can make rejection uninformative.

At minimum, the review must identify and justify treatment of:

- the actual monthly/daily sampling cadence and gaps;
- trend, level shifts, nonstationarity, and known regime changes;
- seasonality and periodic components;
- short-lag linear dependence and spectral/autocorrelation structure;
- marginal distribution, heavy tails, and outliers;
- conditional heteroskedasticity or time-varying variance;
- possible long-memory behavior and uncertainty in estimating it;
- known domain-specific nuisance structure and measurement/source revisions.

No single surrogate family preserves all of these features exactly. A model is adequate only relative to a specified scientific null, data-generating assumptions, endpoint, and calibrated decision rule.

## 5. Candidate-family comparison — development only, not a selection by p-value

| Family | What it can represent/preserve | Important limitations and review questions | Current decision |
|---|---|---|---|
| Stationary Gaussian AR(p) | Short-memory linear dependence through an autoregressive spectrum; Gaussian innovations | Current p=1..20 fit saturates at the upper boundary; Type-I calibration has two recorded failures; may miss non-Gaussian innovations, heteroskedasticity, nonstationarity, or long memory | Not approved for confirmation in current form |
| ARMA(p,q) | More flexible short-memory linear dependence than AR-only models | Requires a prespecified order-selection and fitting rule; can still miss long memory, regime changes, and non-Gaussian/heteroskedastic structure; better fit alone does not establish null adequacy | Candidate for outcome-blind development comparison only |
| IAAFT surrogates | Preserves the empirical amplitude distribution and approximates the observed power spectrum | Spectrum and amplitude distribution are not both preserved exactly; if the endpoint is spectral persistence, preserving the spectrum may preserve the very feature under test and change the scientific question | Diagnostic/comparator only; not a replacement chosen because it yields a smaller p-value |
| ARFIMA(p,d,q) | Can represent fractional/long-memory dependence under explicit assumptions on d and the ARMA terms | Estimation of d and model orders is uncertain; finite-sample calibration and stationarity/invertibility conditions matter; if long memory is the target, conditioning on it may remove the target from the test | Candidate only if the scientific null requires long memory as nuisance; not approved |
| Block/residual bootstrap or other structured surrogates | May preserve selected local dependence or fitted residual properties | Block length, residual assumptions, boundary behavior, and target preservation must be justified and calibrated; no universal default | Candidate only if justified prospectively |

A family comparison is permitted only as a clearly labelled method-development study with declared assumptions, fixed scenarios, and no inspection of fresh confirmatory endpoint outcomes. The comparison report must include failures and must not select a family on observed candidate alpha/p-values.

## 6. Required fit, calibration, and power audit

Before any confirmatory protocol can be frozen, an independent methods reviewer must approve a versioned plan that includes all of the following:

1. **Fit diagnostics:** selected-order distribution, boundary-hit rate, convergence failures, nonstationary/invalid fits, parameter estimates, near-boundary roots, and the disposition of every failed fit.
2. **Residual diagnostics:** prespecified residual autocorrelation checks with parameter-estimation degrees of freedom considered; conditional heteroskedasticity checks; innovation-distribution checks; and parameter stability across prespecified segments where scientifically justified. A non-significant diagnostic is not proof of adequacy.
3. **Type-I calibration:** the four existing scenarios, exact seeds/code/dependencies, trial counts, invalid-fit handling, Wilson intervals, scenario-wise acceptance, and an overall rule for the family of scenarios. Preserve every failure. Do not change the present acceptance rule after observing outcomes merely to get a pass.
4. **Power:** simulations under explicitly defined alternatives representing the target effect and realistic nuisance processes, at the primary sample size and declared estimator/window/band. Report power with Monte Carlo uncertainty and include plausible weak effects, boundary cases, model misspecification, and nonstationarity where relevant. Do not infer power from the current p-value or from Type-I calibration alone.
5. **Multiplicity and Monte Carlo uncertainty:** define before fresh runs how the suite-level false-positive risk is controlled and how Monte Carlo precision affects decisions.
6. **Clean confirmation:** freeze the null, estimator, endpoint, transformation, window, frequency band, direction/tail, surrogate count, seed policy, missingness/exclusion rules, source snapshots, software versions, and acceptance rule before calculating any fresh candidate endpoint.
7. **Independent review record:** reviewer identity/affiliation or attributable record, expertise, exact commit and artifact hashes, date, objections, responses, and signed/otherwise attributable disposition. Do not fill reviewer fields by inference or backdate them.

## 7. HadUKP and CPIAUCNS decisions

### HadUKP EWP

Treat it as a candidate only. Structural checks in run `39066915519` passed for the predeclared 1913-01 through 2025-12 window (1,356 monthly observations; no missing/non-finite values or cadence gaps reported). This does not establish independence from the primary sunspot domain, exclude shared climate/solar-related nuisance, validate source homogeneity/vintage, or prove absence of prior endpoint exposure.

### CPIAUCNS

Keep excluded under the current completeness rule. The run reported 1,356 monthly rows and one missing/non-finite observation at `2025-10-01` (1,355 valid numeric values). Preserve the raw snapshot byte-for-byte. Do not impute, interpolate, silently drop the month, or change the rule post hoc. If a future source retrieval is scientifically justified, store it as a separate dated immutable snapshot with its own raw hash and a prospective decision made before endpoint analysis; it does not retroactively repair the current snapshot.

## 8. Mandatory next gate, in order

1. Preserve the current commit, artifacts, hashes, and failures.
2. Complete a source-independent, outcome-blind null-family review using development simulations and the scientific estimand; do not use candidate endpoint results to choose the family.
3. Complete same-commit calibration and the full fit/power/failure audit under the declared plan.
4. Record an attributable independent methods review and freeze the complete confirmatory protocol only if accepted.
5. Complete HadUKP source-vintage and historical endpoint-exposure review, plus shared-nuisance/independence review.
6. Keep CPIAUCNS excluded unless a scientifically justified and prospectively specified completeness treatment is independently approved; preserve the current raw snapshot unchanged.
7. Only after steps 2–6, and only on the frozen protocol, consider fresh candidate endpoint analysis and the two-domain replication gate.

## 9. Non-negotiable interpretation boundary

A green engineering workflow establishes that particular code/checks completed, not that the scientific hypothesis is true. A failed gate must remain failed until the underlying criterion is met for a scientifically justified reason. Even a future rejection of one adequate, prespecified stochastic null is evidence against that null under that protocol; it does not alone establish HCM causation, consciousness, universality, mechanism, or a new physical law.
