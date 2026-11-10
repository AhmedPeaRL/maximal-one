# First-three occurrence evidence dossier — no adjudication

**Scope:** target snapshot `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`.

**Rule:** this dossier records source and execution evidence only. It does not set `manual_classification`, close a record, or replace an independent human reviewer. Keep all three CSV rows `UNKNOWN / OPEN / PENDING` until an actual human review is completed.

## Occurrence 1

- ID: `refs/audit/target/2f8523fcf7c5/73/4`
- Target file and line: `.github/workflows/type1-calibration-runtime-pilot.yml:73`
- Target source command: `python -m analysis.type1_calibration_pilot` with scenario `gaussian_ar2_inband_f_0_02_radius_0_90_n3328`, start index 0, stop index 2, total repetitions 2, 200 surrogates, master seed 20261021.
- Target workflow is `workflow_dispatch` only. The branch guard is called at line 26 before output-directory creation and the runner call. A separate checkout-identity step at lines 28–34 checks `git rev-parse HEAD == GITHUB_SHA` before the run.
- Important version distinction: the guard script inside target snapshot `ad106...` checks only `GITHUB_REF`. The later review-branch implementation at `4d0fe317...` strengthens the guard to require `GITHUB_ACTIONS=true`, a full 40-character `GITHUB_SHA`, and exact `HEAD` equality. Do not backdate that later hardening into the target snapshot.
- Later implementation execution: run `42870135490`, job `130018881819`, artifact `13789261860`, commit `4d0fe317...`. Two valid pilot attempts, 200 surrogates each, zero invalid attempts; Monte Carlo p-values `0.1890547263681592` and `0.024875621890547265`. Artifact status `PILOT_COMPLETE_DIAGNOSTIC_ONLY`; formal calibration false, confirmatory null not frozen, claim support false, promotion authority false.
- Human question left open: determine the exact historical governance classification of this invocation and the effect of its branch/checkout guards. The later implementation run is supporting evidence about the remediation, not a substitute for inspecting target `ad106...`.

## Occurrence 2

- ID: `refs/audit/target/40d0253a5dd6/60/6`
- Target file and line: `.github/workflows/type1-v4-cross-runner-worker-order.yml:60`
- Target source command: `python -m analysis.calibrate_null_type1_scenario --engineering-test` for `gaussian_ar2_phi_0_45_minus_0_10_n3328`, six repetitions, 1,000 surrogates per repetition, n=3328, seed 20261021.
- Workflow guard and checkout identity checks occur before the connected-reference command.
- Execution evidence: run `42870239737`, connected-reference job `130019260827`, artifact `13789098160`; comparison job `130023691405`, artifact `13788489214`. Six of six worker records matched the connected reference.
- All seven recorded platform identities were `Linux-7.0.0-1017-azure-x86_64-with-glibc2.39`. This demonstrates worker/run equivalence on the same platform identity; it does not demonstrate cross-platform replication or independent scientific replication.
- Human question left open: determine whether the occurrence should be classified as a connected engineering reference, and what authority it does or does not have under the target protocol. The command explicitly uses `--engineering-test`.

## Occurrence 3

- ID: `refs/audit/target/40d0253a5dd6/123/9`
- Target file and line: `.github/workflows/type1-v4-cross-runner-worker-order.yml:123`
- Target source command: same engineering-test scenario and parameters as occurrence 2, but this is the worker-matrix invocation; each matrix job executes one replicate index.
- Execution evidence: same run `42870239737`; six worker jobs `130019260740`, `130019260845`, `130019260657`, `130019260425`, `130019260759`, and `130019260796`; worker artifacts `13790460003`, `13788219997`, `13789801310`, `13789491564`, `13788962393`, and `13789032373`. Comparison job `130023691405`, artifact `13788489214`; six of six matches.
- Same-platform limitation applies: all workers and the connected reference reported the same Linux platform identity. Distinct jobs/runner instances are not cross-platform independence.
- Human question left open: determine whether the worker invocation is a separate execution-path occurrence from the connected reference, and whether any governance distinction follows from its matrix role. Do not collapse occurrence 2 and 3 merely because they share a workflow.

## Shared constraints

- The three rows remain `manual_classification` blank / `status=OPEN` / `reviewer_disposition=PENDING` until reviewed.
- The repository author may act as primary reviewer only with authorship/intellectual-interest conflict disclosed. High-impact classifications require a distinct second human reviewer. An AI system is not a human second reviewer.
- No formal Type-I calibration pass, confirmatory authorization, claim support, promotion authority, or protocol freeze follows from these engineering artifacts.
