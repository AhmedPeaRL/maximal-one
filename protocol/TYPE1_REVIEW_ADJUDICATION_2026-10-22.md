# Type-I V4 Review Adjudication — 2026-10-22

- **Repository:** `AhmedPeaRL/maximal-one`
- **Working branch:** `review/type1-v4-remediation`
- **Adjudication reference commit:** `2ea541207c7c8be0046327399eac2f146d576ab7`
- **Protocol:** `HCM_TYPE1_CALIBRATION_V4_CANDIDATE`
- **Decision:** `CONTINUE_REMEDIATION`
- **Freeze state:** `NOT_FROZEN`
- **Formal calibration:** `NOT_AUTHORIZED`

## 1. Purpose and decision boundary

This record adjudicates the two Type-I review texts received on 2026-10-22, designated Report A and Report B, against the available repository records and engineering evidence.

It is a repository-side technical adjudication. It is not a substitute for an attributable independent human statistical review, does not establish that either submitted report was authored or approved by a named human, and does not authorize formal calibration.

The submitted reports are retained as review inputs. Their claims are not treated as verified findings solely because they appear in a report.

## 2. Evidence reviewed

The following repository materials and records were inspected:

* `protocol/TYPE1_V4_FREEZE_DECISION.md`
* `protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json`
* `protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_DRAFT.json`
* `protocol/TYPE1_CALIBRATION_SPEC_V3_CANDIDATE.md`
* `protocol/TYPE1_V4_ACCEPTANCE_LEDGER.md`
* `protocol/TYPE1_FORMAL_CALIBRATION_AUTHORIZATION.md`
* `protocol/TYPE1_ACCEPTANCE_RULE_OPERATING_CHARACTERISTICS_V1.md`
* `analysis/calibrate_null_type1.py`
* `analysis/calibrate_null_type1_scenario.py`
* `protocol/TYPE1_REVIEW_REPORT_TRIAGE_2026-10-21.md`

Engineering evidence:

* Latest recorded full-path workflow run: `39683638768`
* Job: `119512096300`
* Tested commit: `2ea541207c7c8be0046327399eac2f146d576ab7`
* Artifact ID: `12384249797`
* Artifact name: `type1-full-path-equivalence-evidence`
* Artifact ZIP SHA-256 as reported by GitHub: `156e6ffa90b7b655f85f208c85e885db45a7f213789e25df30fb7e7fdf9cfd18`
* Workflow result: `success`

This evidence establishes successful completion of the recorded engineering job for its tested configuration. It does not establish formal Type-I calibration, adequacy of every scientific null model, or support for the broader research claim. The artifact ZIP digest is not a digest of any individual JSON payload.

## 3. Report A — disposition

**Disposition:** `REVISE_AND_RESUBMIT_FOR_GATE_CLOSURE`

Report A names Dr. Ibrahim Abdullah and states relevant expertise. The submitted text alone does not provide enough independently verifiable attribution and version identity to close the independent-review gate.

The following items remain unresolved:

1. The exact reviewed commit SHA is not stated.
2. SHA-256 hashes for the reviewed protocol and implementation files are not supplied.
3. The identity, independence, and final disposition have not been independently verified from an attributable review record.
4. Report A proposes `N = 10000`, burn-in `1000`, and five outer seeds. These values conflict with the current V4 candidate dimensions, which specify `N = 3328`, DGP burn-in `2000`, and `2000` outer repetitions per scenario.
5. Report A proposes several null-model families and surrogate types without establishing that they are implemented by, or prospectively approved for, the exact candidate V4 execution path.
6. The recommendation to proceed to confirmatory execution conflicts with the currently open acceptance criteria and the separate authorization gate.

No parameter change is approved by this adjudication.

## 4. Report B — disposition

**Disposition:** `REVISE_AND_RESUBMIT_FOR_GATE_CLOSURE`

Report B appropriately distinguishes a review step from protocol freeze and formal execution authorization. However, it does not close the gate.

The following items remain unresolved:

1. The record attributes the review to a committee but does not provide an individually attributable human reviewer record with an exact reviewed commit and file-level SHA-256 manifest.
2. It describes the historical Wilson upper-bound ceiling of `0.075` as conditionally acceptable, whereas the current V4 candidate matrix records the acceptance rule as unresolved and the historical ceiling as not justified or approved.
3. The report's approvals do not constitute a completed authorization record.
4. The production implementation and the V4 candidate specification have not been demonstrated to be the same frozen configuration.
5. The report does not provide sufficient evidence to authorize formal calibration.

No `APPROVE` disposition in the submitted text is treated as repository authorization.

## 5. Critical specification-to-implementation discrepancy

The inspected files `analysis/calibrate_null_type1.py` and `analysis/calibrate_null_type1_scenario.py` reference:

`protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V3.json`

The V4 candidate matrix is a separate file:

`protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json`

Before freeze, the project must identify the exact intended production entry point and demonstrate that its runtime configuration, endpoint, null generator, scenario definitions, seeds, and decision rule are the ones specified by the reviewed candidate.

A successful engineering test does not by itself close this discrepancy.

Required disposition:

* Identify the exact formal runner and all modules it imports.
* Trace the runtime configuration to the intended frozen matrix.
* Add tests that fail if the runner silently loads an unintended matrix or configuration.
* Record the reviewed source hashes and the test evidence.
* Obtain independent reviewer disposition on the resulting exact snapshot.

## 6. Prospective parameter reconciliation

The following values are not interchangeable and must not be silently combined across reports or protocol versions.

| Parameter                      |       Current V4 candidate |                         Report A | Adjudication                                                          |
| ------------------------------ | -------------------------: | -------------------------------: | --------------------------------------------------------------------- |
| Sample size `N`                |                       3328 |                            10000 | Unresolved; no change authorized                                      |
| DGP burn-in                    |                       2000 |                             1000 | Unresolved; no change authorized                                      |
| Outer repetitions per scenario |                       2000 |                Five seeds stated | Not equivalent specifications                                         |
| Surrogates per outer test      |             1000 requested |                             1000 | Candidate requirement only; production path still requires validation |
| Nominal alpha                  |                       0.05 |                             0.05 | Common target, not proof of calibration                               |
| Acceptance rule                | `null` in candidate matrix | Historical 0.075 ceiling implied | Unresolved; no acceptance rule approved                               |

The candidate master seed is `20261021`, but its final approval status is false. No seed, scenario, threshold, sample size, burn-in, or null-model amendment may be made after inspecting formal calibration outcomes to obtain a passing result.

Any proposed amendment must be justified prospectively, reviewed, versioned, tested, and hashed before formal outcomes are generated.

## 7. Type-I estimand and Monte Carlo design

The protocol must distinguish:

* **Outer repetitions (`R`):** independent executions of the complete test under each declared null data-generating process. These outcomes estimate the empirical Type-I rejection rate for that scenario.
* **Inner surrogates (`M`):** surrogate realizations used to calculate a Monte Carlo p-value for one outer test.
* **Invalid outer attempts:** failures of the complete test or required evidence that remain visible and block a scenario pass under the current candidate policy.
* **Invalid or missing surrogates:** failures that must not be silently dropped, replaced, or counted as valid. The approved policy must specify the consequence and record every attempt.

The add-one Monte Carlo p-value formula may be used only where its implementation and assumptions are verified:

`p = (exceedances + 1) / (valid_surrogates + 1)`

The production requirement for 1000 valid surrogates per outer test must be verified in the actual authorized execution path. The exploratory pilot is not a substitute for that verification.

## 8. Acceptance rule and multiplicity

The historical Wilson upper-bound ceiling of `0.075` is not approved by this adjudication.

Before freeze, an attributable independent statistical reviewer must assess and document:

1. The exact Type-I estimand and per-scenario decision rule.
2. The rationale for the nominal level and the selected confidence-bound criterion.
3. The planned outer repetition count and resulting operating characteristics.
4. The risk of falsely failing a nominal scenario and the risk of passing a materially inflated scenario.
5. The decision policy across all nine scenarios, including the scope of any aggregate statement.
6. The handling of invalid attempts, missing results, and incomplete scenarios.
7. The Monte Carlo precision required for the intended scientific interpretation.

The rule must be selected prospectively and must not be altered after formal outcomes are examined.

## 9. Resonance near the tested frequency-band boundaries

An AR(p) null may reproduce some linear dependence and spectral characteristics, but it must not be presumed adequate for every near-boundary resonance or nonlinear structure.

Before freeze, the reviewer must decide whether the declared nine scenarios adequately test the intended boundary and resonance behavior. Any new scenario or surrogate family must be added by a prospective, versioned amendment before confirmatory outcomes are inspected.

Required evidence includes:

* Exact frequency-band limits and endpoint behavior at and near those limits.
* The declared null-generation and model-fitting procedure.
* Stationarity and fit-validity checks.
* The surrogate refitting policy and failure accounting.
* Scenario-specific Type-I operating characteristics and uncertainty.
* Evidence that boundary-related failure modes cannot silently become passes.

This adjudication does not add spectral or block-shuffle surrogates to the approved design; no approved design exists yet.

## 10. Freeze gate

V4 remains `NOT_FROZEN` until all of the following are complete:

* An attributable independent human statistical review identifies the exact commit and file hashes.
* The reviewer explicitly disposes of each critical review item.
* The V4 matrix and the actual production execution path are reconciled.
* The endpoint, null family, scenarios, sample size, burn-in, surrogate count, outer repetitions, seeds, and acceptance rule are frozen as one coherent design.
* Invalid-attempt and missing-evidence rules are executable and tested.
* Required production-configuration equivalence tests pass.
* Runtime and artifact-retention feasibility are assessed.
* The completed freeze decision records the exact commit, file hashes, evidence identifiers, limitations, and decision owner.

A successful CI run or an AI-assisted report does not substitute for these requirements.

## 11. Separate formal-execution authorization

Even after a valid freeze decision, formal calibration remains unauthorized until a separate authorization record explicitly approves:

* The frozen commit and file hashes.
* The exact scenario matrix and execution entry point.
* Outer repetitions and required valid surrogates.
* Master seed and deterministic seed schedule.
* The Type-I rejection and acceptance rules.
* Invalid-attempt, rerun, interruption, and artifact-integrity policies.
* Stop conditions and retained evidence.
* The authorized decision-maker and date.

## 12. Current decision

* `review_gate = NOT_CLOSED`
* `freeze_state = NOT_FROZEN`
* `confirmatory_execution_authorized = false`
* `claim_support = false`
* `promotion_authority = false`
* `formal_calibration = NOT_AUTHORIZED`
* `next_action = RECONCILE_IMPLEMENTATION_AND_OBTAIN_ATTRIBUTABLE_VERSION_SPECIFIC_REVIEW`

This decision preserves the engineering evidence without promoting it into a scientific conclusion. It does not reject the research hypothesis; it records what the current evidence does and does not establish.

## Addendum — V4 Runner Remediation Status — 2026-10-22

- **Working branch:** `review/type1-v4-remediation`
- **Disposition:** `CONTINUE_REMEDIATION`
- **Freeze state:** `NOT_FROZEN`
- **Formal calibration:** `NOT_AUTHORIZED`
- **Confirmatory execution:** `BLOCKED`
- **Claim support:** `false`
- **Promotion authority:** `false`

### Current engineering status

The primary candidate runner reads the V4 candidate matrix and
keeps formal execution disabled. Candidate dimensions are treated
as diagnostic configuration only. The acceptance rule remains
unresolved; no historical Wilson upper-bound ceiling is approved.

The scenario runner requires reconciliation with the V4 schema.
All references to the legacy V3 matrix and legacy `primary_design`
configuration must be removed from its runtime and artifact metadata.
Seed identity must be based on the stable scenario identifier rather
than scenario list position.

The existing small-configuration full-path test is engineering
evidence only. Production-path equivalence at M=1000 has not been
established by this addendum.

### Independent review status

No attributable independent human statistical review is recorded
as closed by this addendum. AI-assisted analysis and repository
engineering checks are not treated as independent human approval.

### Required next evidence

1. Record the exact remediation commit SHA after the changes are
   committed.
2. Record SHA-256 hashes of the reviewed matrix, runner, null
   implementation, endpoint implementation, tests, dependency lock,
   and relevant workflow files.
3. Run and preserve the V4 schema and fail-closed gate tests.
4. Demonstrate connected, sharded, and resumed equivalence at
   M=1000 through the actual shared execution path.
5. Obtain an attributable independent human statistical review
   against the exact commit and file hashes.
6. Record any freeze decision separately from execution authorization.

This addendum does not approve a parameter, acceptance threshold,
formal calibration, scientific claim, or promotion.
