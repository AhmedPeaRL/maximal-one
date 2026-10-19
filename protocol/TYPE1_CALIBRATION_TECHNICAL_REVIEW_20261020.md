# Type-I Calibration Technical Pre-Review — 2026-10-20

**Disposition:** `REVISE AND REVIEW AGAIN`  
**Reviewer status:** `AI-ASSISTED TECHNICAL PRE-REVIEW; NOT AN ATTRIBUTABLE INDEPENDENT HUMAN REVIEW`  
**Freeze state:** `NOT_FROZEN`  
**Claim support:** `false`  
**Promotion authority:** `false`

## Identity and scope

The supplied report names snapshot `71d331a5c6446f86ab76c7bd94f68feff73813ae`. The attached ZIP does not include `.git` metadata, and its calibration matrix identifies reference commit `9fcd54bbc56ccf4c13b7b2020aa5f02b5f2b7ce5`. Therefore the ZIP's exact Git commit identity cannot be independently verified from the archive alone. This pre-review is tied to the supplied archive contents, not a claim that its bytes are proven identical to either commit.

## Findings

1. **Acceptance-rule conflict:** the historical implementation uses a two-sided 95% Wilson interval and requires it to contain 0.05 while its upper endpoint is at most 0.075. The proposed matrix specifies a one-sided 95% Wilson upper bound at most 0.075. These are different decision rules. V3 candidate files make the one-sided rule explicit and keep the two-sided interval report-only. This rule still requires attributable independent statistical approval; 0.075 is a tolerance above nominal alpha 0.05 and must not be represented as 5% Type-I control.
2. **Scenario/run mismatch:** the archive matrix declares nine scenarios, 2,000 outer attempts per scenario, and 1,000 surrogates per attempt. The existing workflow launches four scenarios with 1,000 attempts and 200 surrogates. Historical results remain historical and are not relabeled as production-equivalent.
3. **Seed dependence:** the existing runner carries one RNG stream through series generation and null generation. V3 candidate code uses stable per-scenario/per-replicate SeedSequence identities with separate DGP and null streams and includes an order-invariance test.
4. **Invalid attempts:** the old runner calculates the rejection rate among valid attempts while allowing invalid attempts to be excluded. V3 candidate policy preserves every attempted record and blocks a scenario pass if any outer attempt is invalid or a requested surrogate is missing.
5. **Production equivalence:** source inspection shows the production configuration declares 1,000 bootstrap trials, canonical open band `(0.01, 0.05)`, Welch `nperseg=1024`, AR order 1–20, AIC, constant trend, stationarity, common effective observations via hold-back, refitting, upper tail, and add-one p-value. Candidate tests check these declared settings. This static check is necessary but is not proof that all runtime behavior is equivalent; independent review and a successful exact-commit test run remain required.
6. **Computational feasibility:** the candidate design requests 9 × 2,000 × 1,000 = 18,000,000 surrogate generations/refits. An independent reviewer should assess runtime and whether the timeout/artifact plan can retain every scenario and failure without partial runs being mistaken for passes.
7. **Primary-domain null adequacy:** the prior boundary-saturation result (937/1,000 valid surrogate refits selecting AR(20)) remains a capacity warning. Synthetic Type-I calibration cannot close this real-data adequacy question. Do not raise the order cap or change the model after observing results without a new prospective protocol.

## Candidate implementation checks

On a local overlay of the supplied ZIP plus the candidate patch, the nine focused unit tests passed and Python compile checks passed. These tests cover the candidate matrix dimensions, stationarity of the nine declared AR DGPs, deterministic shard-order-invariant seed identities, one-sided Wilson acceptance calculation, invalid/incomplete run blocking, and consistency with the declared production settings. They do **not** run the full 18-million-surrogate study, validate every runtime failure path, or constitute independent statistical approval.

## Decision

- `ACCEPTANCE_RULE_CONFLICT`: resolved in the candidate text only; independent approval pending.
- `IMPLEMENTATION_EQUIVALENCE`: static configuration checks pass locally; runtime equivalence and frozen-commit validation pending.
- `NINE_SCENARIO_CALIBRATION`: `NOT_RUN; NOT_DEMONSTRATED`.
- `PRODUCTION_NULL_ADEQUACY`: `NOT_ESTABLISHED`.
- `FREEZE_STATE`: `NOT_FROZEN`.
- `CLAIM_SUPPORT`: `false`.
- `PROMOTION_AUTHORITY`: `false`.

Do not change the candidate matrix to `APPROVED_FROZEN` until an attributable independent statistical reviewer has approved the target, acceptance ceiling, scenario matrix, invalid-attempt policy, runtime feasibility, and production-equivalence plan. Only the resulting freeze commit may trigger the formal calibration workflow.
