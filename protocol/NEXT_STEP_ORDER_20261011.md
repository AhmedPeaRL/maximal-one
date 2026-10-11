# Next-Step Order — maximal-one — 2026-10-11

This is an ordered, conservative plan based on the reviewed repository snapshot and the reported live logs. It is not a claim that every live GitHub file was independently re-fetched.

## Priority 1 — Correct the audit/code rule mismatch

Apply this patch's three replacements/additions:
- `analysis/type1_acceptance_operating_characteristics.py`
- `tests/test_type1_acceptance_operating_characteristics.py`
- `audit/type1_acceptance_operating_characteristics.json`
- `protocol/TYPE1_ACCEPTANCE_RULE_OPERATING_CHARACTERISTICS_V1.md`
- add `audit/DOWNLOADED_JSON_SHA256_MANIFEST.txt`

The production calibration rule stays unchanged. The audit now represents both conditions already enforced in `analysis/calibrate_null_type1_scenario.py`: the Wilson interval must contain 0.05, and its upper endpoint must be <= 0.075. Expected accepted counts for n=1000: 37..58. Four local unit tests passed against the patch files in the packaging environment; this is not a claim that GitHub Actions has passed.

Suggested commit message: `Align Type-I operating-characteristics audit with implemented gate`

## Priority 2 — Do not guess at unresolved scientific decisions

Do not fill `SECONDARY_DOMAIN_PREANALYSIS_DECISION_TEMPLATE_V1.md` by inventing answers. The author must honestly record whether endpoints or outcomes were previously viewed. If they were, label the analysis post-observation/exploratory. Choose the HadCET start rule and INDPRO transformation from source-backed scientific reasoning, not from the alpha or p-value.

## Priority 3 — Reconcile primary null boundary saturation

Keep `0.937` in `strict_claim.json` and the reported `0.947` in the latest audit as conflicting historical records until each is tied to its exact run ID, commit SHA, code/data hashes, seed, and output artifact. Do not overwrite one with the other by inference. Keep confirmatory status unfrozen.

## Priority 4 — Implement diagnostic clarity only after tests are added

The primary-provenance diagnostic issue is suitable for a code fix, but the change must preserve all eligibility booleans, gate outcomes, exit codes, and claim-promotion authority. Add tests that prove the reason labels are role-aware and that final replication counts do not change. Do not merge a diagnostic change that changes eligibility semantics.

## Priority 5 — Separate software health from scientific promotion status

Consider splitting CI into:
- a software/integrity workflow that must pass tests, schema checks, checksums, and audit calculations; and
- a scientific claim-promotion workflow whose blocked result is reported as a scientific status, not disguised as a software defect.

Before editing workflows, inspect all existing triggers, required checks, downstream dependencies, and branch protection behavior. Do not make a blocked scientific gate green by weakening the scientific criteria.

## Priority 6 — Reproducibility and provenance

The current lock file already contains multiple hashes for many distributions, so the phrase “only two hashes” should be checked against the exact current file rather than repeated generically. Audit the complete transitive dependency closure and platform-specific wheels before changing it. Preserve the currently working environment; regenerate hashes only in a controlled, reproducible process and verify `pip install --require-hashes`.

The JSON hash manifest in this patch records the exact JSON bytes present in the reviewed ZIP snapshot. Recompute hashes from the actual live committed JSON files before treating it as a live-repository manifest. The ZIP-artifact manifest and JSON-payload manifest are deliberately separate.

## Scientific status boundary

The current evidence described in the logs does not establish the hypothesis: the primary null is not rejected (reported p=0.999001), zero of two candidate secondary domains are eligible for independent replication, and the AR(p) null remains exploratory/unfrozen. Clean-checkout reproducibility and passing software tests are valuable but are not independent scientific replication. No market edge, HCM causation, universality, or award outcome is established by these records.
