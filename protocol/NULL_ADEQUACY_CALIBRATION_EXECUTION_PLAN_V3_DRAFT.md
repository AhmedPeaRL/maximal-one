# Null Adequacy, Type-I Error, Power, and Reference-Data Execution Plan — V3 Draft

**Record date:** 2026-10-18  
**Status:** `DRAFT_PENDING_ATTRIBUTABLE_INDEPENDENT_METHODS_REVIEW`  
**Confirmatory use:** `NOT_AUTHORIZED`  
**Claim support:** `false`  
**Promotion authority:** `false`

This plan organizes the next scientific work. It does not select a confirmatory null, approve any dataset, or authorize candidate endpoint computation.

## 1. Separation of workstreams

Keep three workstreams separate in code, artifacts, and interpretation.

### A. Known-truth simulation calibration
Purpose: estimate Type-I error under declared null-generating processes and power under prespecified alternatives. Because the data-generating process is known, this is the primary source of Type-I and power evidence.

### B. Empirical reference-series diagnostics
Purpose: check whether candidate methods preserve or misrepresent realistic temporal nuisance structures, including trends, gaps, seasonality, heteroskedasticity, heavy tails, and source revisions. Empirical series do not have known null truth and cannot alone establish Type-I calibration.

### C. Independent real-domain replication
Purpose: test the frozen endpoint/null in untouched real-world domains selected before endpoint observation. This workstream is blocked until the null, endpoint, acceptance rule, source snapshots, and independence review are approved. Do not reuse calibration outcomes as replication credit.

## 2. Gate 0 — preserve the historical record

Before any new run:
- preserve all historical scenario outputs and failed statuses;
- preserve the current primary dataset and all source snapshots byte-for-byte;
- record the current `main` commit SHA and the exact working-tree source hash;
- record SHA-256 for every input, script/config, dependency lockfile, and output;
- never overwrite artifacts from prior runs;
- label post-observation analyses exploratory.

## 3. Gate 1 — close the estimand and nuisance definition

An attributable independent statistical-methods reviewer must decide whether the target is:
- excess spectral persistence beyond a specified baseline; or
- long-memory/spectral persistence itself.

Do not proceed as though these are equivalent. The reviewer must approve the target-versus-nuisance table and document why each null family preserves nuisance structure without removing the target by construction.

## 4. Gate 2 — compare candidate null families without candidate endpoint selection

Permitted development comparators, subject to scientific justification:
- stationary Gaussian AR(p);
- ARMA(p,q);
- IAAFT surrogates;
- ARFIMA(p,d,q), only if long-memory treatment matches the estimand;
- block/residual bootstrap or another structured surrogate only with an explicit rationale.

For every family, declare in advance:
- scientific role and assumptions;
- parameters and candidate ranges;
- model-selection/fitting procedure;
- stationarity/invertibility and root constraints;
- residual diagnostics;
- surrogate generation and refitting procedure;
- minimum valid surrogates and invalid-fit handling;
- nuisance features preserved, modeled, or not preserved;
- boundary-saturation rule;
- known failure modes.

Do not select a family by smallest p-value, largest alpha, favorable candidate result, or post-observation endpoint behavior. A better in-sample fit alone is not proof of inferential adequacy.

## 5. Gate 3 — same-commit rerun of the four historical Type-I scenarios

First reproduce the existing declared suite without changing its historical rule:
- Gaussian AR(1), phi = 0.4;
- Gaussian AR(2), phi = 0.45, -0.10;
- Gaussian AR(5), declared low-order coefficients;
- Gaussian AR(10), declared low-order coefficients.

Current workflow configuration is 1,000 repetitions, 200 surrogates, n=1,024, with fixed scenario-specific seeds. Record exact commit SHA inside each job and verify that all four jobs used the same commit. Preserve checkpoints, invalid counts, fit failures, p-values, Wilson intervals, selected-order distributions, boundary fractions, and artifact SHA-256.

Apply the historical rule exactly as recorded: the two-sided 95% Wilson interval must contain 0.05 and its upper endpoint must be <= 0.075. Do not reinterpret or amend historical failures. A successful rerun establishes reproducibility of that run, not full null adequacy.

## 6. Gate 4 — predeclare and implement the expanded simulation matrix

Before launching the expanded matrix, the independent reviewer must approve the scenario list and acceptance rule. Include, where relevant:
- ARMA processes;
- non-Gaussian/heavy-tailed innovations;
- conditional heteroskedasticity;
- trend, level shifts, and regime changes;
- seasonal nuisance;
- declared missingness/gap patterns;
- long-memory diagnostics with explicit H0/H1 interpretation;
- prespecified alternatives across effect sizes, including weak effects and boundary cases.

For each scenario record: unique ID, DGP equation/parameters, sample length, burn-in, missingness, seed policy, number of outer replicates, number of inner surrogates, invalid-fit handling, expected artifact schema, and acceptance criterion.

The existing four-scenario acceptance rule does not automatically define a defensible suite-level rule for a larger matrix. Before any fresh expanded run, the reviewer must explicitly freeze:
- nominal Type-I target;
- tolerated deviation and interval method;
- per-scenario rule;
- overall suite rule (including whether all required scenarios must pass);
- treatment of dependent scenarios;
- Monte Carlo precision/stopping rule;
- invalid-run policy;
- power target and uncertainty reporting.

Do not fill these decisions after seeing results. Do not average away a failing scenario. Any amended rule must have a new version and must be frozen before the new run.

## 7. Gate 5 — power and false-negative audit

Use prespecified alternatives representing the operational target at multiple effect sizes and plausible nuisance conditions. Include the declared primary sample size and endpoint implementation. Report:
- empirical power and Monte Carlo uncertainty;
- false-negative behavior;
- p-value quantiles;
- Type-I rates under every required null DGP;
- invalid-fit and refit-failure rates;
- boundary saturation and model-selection stability;
- sensitivity to prespecified nuisance conditions.

Do not infer power from a current p-value, a Type-I-only simulation, or a successful code test. A failed power target blocks confirmation under the predeclared rule.

## 8. Gate 6 — register empirical reference series before use

Use `REFERENCE_DATA_REGISTRATION_TEMPLATE_V1.json`. Register a source before parsing or endpoint calculation. Required fields include publisher, stable source URL/citation, exact retrieval time, source vintage, raw and parsed SHA-256, immutable snapshot path, cadence/window, missingness policy, preprocessing, prior exposure, intended role, shared-driver assessment, and reviewer decision.

Candidate examples from the existing repository:
- HadUKP EWP: may be evaluated as an empirical climate reference series only after source-vintage, exposure, and shared-climate/solar nuisance review. It is not automatically independent confirmation.
- CPIAUCNS: current snapshot remains blocked by the recorded missing observation at 2025-10-01. Preserve it unchanged. A separately retrieved future snapshot must have a new timestamp/hash and a prospective, independent decision; it does not repair the old snapshot.
- HadCET and INDPRO: prior endpoint-like exposure means current outputs are exploratory/post-observation. They may inform method-development diagnostics but cannot be relabelled as untouched confirmation.
- Cosmic rays: do not use until the timestamp-aware raw-data audit, source provenance, and solar-cycle shared-nuisance assessment pass.

A dataset with realistic temporal structure can be a reference for diagnostics without being eligible as a replication domain.

## 9. Gate 7 — independent review and decision record

The reviewer must be attributable and must record:
- reviewer name or attributable identity, relevant expertise, affiliation if applicable, and conflicts/independence statement;
- exact reviewed commit;
- protocol and input/output SHA-256 hashes;
- methods reviewed and limitations;
- each criterion as `PASS`, `FAIL`, or `NOT_ASSESSED`;
- objections, responses, and any dissent;
- dated decision: `ACCEPT`, `REJECT`, or `HOLD`.

Do not invent or backdate reviewer information. An AI desk review or internal code review is not a substitute for the required external methodological signoff.

## 10. Final authorization

No candidate endpoint may be computed for confirmatory use until:
1. the estimand and nuisance boundary are closed;
2. a null family and fitting/refitting procedure are approved;
3. same-commit historical rerun and expanded calibration/power matrix meet the prospectively frozen rule;
4. empirical reference-series audits and their intended roles are documented;
5. the replication candidates have passed source, exposure, measurement, nuisance, and independence review;
6. all protocol components are frozen and hash-verified on a commit preceding the confirmatory run.

Until then: `NOT_FROZEN`; `DO_NOT_RUN_CONFIRMATORY_ANALYSIS`.
