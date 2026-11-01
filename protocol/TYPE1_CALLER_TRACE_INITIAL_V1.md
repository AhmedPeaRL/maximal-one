# Type-I Caller Trace — Initial Evidence Record V1

Status: PARTIAL STATIC TRACE — HUMAN REVIEW OPEN  
Authority: REVIEW EVIDENCE ONLY  
Protocol freeze: NOT FROZEN  
Confirmatory execution: NOT AUTHORIZED  
Claim support: FALSE  
Promotion authority: FALSE

## A. Main V3 calibration workflow

1. Entry point: `.github/workflows/null-type1-calibration.yml`, event `workflow_dispatch`.
2. Preparation step reads `protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V3.json`.
3. Before writing the matrix output, the preparation step checks `status == APPROVED_FROZEN`, `freeze_state == FROZEN`, `confirmatory_execution_authorized is True`, and `archive_git_identity_verified is True`.
4. The `calibrate` job depends on `prepare-matrix`; therefore a failed preparation job causes the matrix job to be skipped.
5. The runner command is `python -m analysis.calibrate_null_type1_scenario`.
6. `analysis/calibrate_null_type1_scenario.py` independently checks matrix status, freeze state, and confirmatory authorization before creating the output directory or entering the replicate loop.
7. The scenario runner imports `generate_ar`, `replicate_rngs`, and Wilson helpers from `analysis/calibrate_null_type1.py`.
8. The scenario runner calls `estimate_alpha` from `analysis/numerical_spectral_verification.py` and `parametric_short_memory_null` from `analysis/appropriate_stochastic_null.py`.

## B. Main-branch negative execution evidence

Workflow run `41334991587`, job `124932813848`, checked out exact main commit `3899c6aa5a0d0f486bb3e78373d9b04d9ae155f6`.

Observed: preparation failed at the `APPROVED_FROZEN` check with the explicit message that no calibration simulations were started; the dependent scenario job was skipped. This is consistent with the intended fail-closed behavior for the current unfrozen matrix. The workflow conclusion remains `failure`; record it as a successful negative-control outcome only after independent log review, not as a successful calibration run.

## C. Separate exploratory runtime-pilot path

The review-branch `analysis/calibrate_null_type1_scenario.py` has two distinct dispatch paths:

- Without `--engineering-test`, `main()` dispatches to `formal_main()`. The first gate checks `V4_APPROVED` and exits before parsing the formal-run arguments or creating an output if V4 is not approved/frozen/authorized.
- With `--engineering-test`, `main()` dispatches to `engineering_main()`. That path requires the explicit flag, limits the scenario/repetitions/sample-size/seed/surrogate configuration, writes an artifact marked `V4_OFFICIAL_RUNNER_ENGINEERING_ONLY`, and hard-codes formal pass, claim support, promotion authority, and confirmatory authorization to false.
- Both paths can call `execute_attempt()`. The formal path is gated by `V4_APPROVED`; the engineering path is a separately constrained execution route and must be inventoried/traced as execution-capable-but-gated, not treated as formal calibration.

`.github/workflows/type1-calibration-runtime-pilot.yml` separately invokes `analysis/type1_calibration_pilot.py` and imports/uses `analysis/merge_type1_calibration_pilot_shards.py`. This is another distinct exploratory path and must be traced independently; do not infer that either the V3 or V4 formal gate automatically governs it.

## D. Static compile/test references are not runner invocations

`.github/workflows/scientific-validation.yml` and `.github/workflows/scientific-claim-promotion.yml` contain compile/compileall references to the scenario script. Those references must not be classified as execution-capable runner calls merely because the filename appears in the workflow.

## E. Still open

- Trace all direct and indirect callers of `parametric_short_memory_null` and `estimate_alpha`.
- Trace all V4 candidate runner entry points and their workflow branch/event restrictions.
- Verify authorization guard ordering independently in every execution-capable workflow, including the `--engineering-test` dispatch path and any direct `execute_attempt()` callers.
- Identify negative tests and exact run/job/artifact/commit evidence for each caller path.
- Review dynamic imports, subprocess invocations, CLI wrappers, and shard/resume entry points.
- Human adjudication remains required for every occurrence; automated suggestions do not close ledger records.
