# Scientific Gate Diagnostic Fix Plan — 2026-10-11

## Current exact evidence

The inspected Type-I Actions run is `38088677966`, on commit `179c2bb01167ed9f3d3deda6549c2b893faeabb5`. Two of four predeclared synthetic AR scenarios failed the current calibration rule; the other two passed only within their individual synthetic scope. The AR(p) null remains unfrozen.

The live provenance registry now records HadCET and INDPRO checksums and monthly integrity results, but both remain `replication_eligible: false`, `approved_for_replication: false`, and independence review pending. The current independent-domain gate reports `0/2`; this is the correct outcome until eligibility is established.

## Priority order

### P0 — Preserve the evidence

1. Download all four Type-I JSON artifacts from run `38088677966` and preserve the exact commit SHA, artifact IDs, hashes, internal seeds, requested repetitions, and software versions.
2. Keep the two failed scenarios marked failed. Do not change the 0.075 Wilson-upper limit or the nominal alpha to turn them green.
3. Preserve the discrepancy between the historical boundary fraction `0.937` in `strict_claim.json` and the later logged value `0.947`. Reconcile only after tying each value to exact run ID, commit, script/data hashes, seed, and surrogate definition. Do not overwrite either value by guess.

### P1 — Clarify the estimator design before more expensive runs

1. Complete `WELCH_SEGMENT_COVERAGE_REVIEW_V1.md` with a prospectively justified study design; do not treat overlapping segment count as independent sample size.
2. Run a planned synthetic calibration matrix across declared sample lengths and null scenarios, changing one factor at a time. Use fixed seeds and publish all scenarios, not only successful ones.
3. Diagnose the AR(10) failure and AR-order boundary saturation separately. Review fit diagnostics, stationarity, residual dependence, order-selection distribution, and model adequacy before deciding whether a new null family is scientifically appropriate.
4. Profile the current implementation before optimizing its runtime. Any optimization must be checked against a reference implementation and identical seeds/results. Runtime improvements are not statistical validation.

### P2 — Predeclare secondary-domain choices

1. Complete `SECONDARY_DOMAIN_PREANALYSIS_DECISION_TEMPLATE_V1.md` before endpoint computation. Record prior exposure honestly; the existing dataset-integrity audit is not a preregistration.
2. For HadCET, define the historical-window rule using source precision/provenance, not alpha. Preserve and report the full window and predeclared sensitivity windows where appropriate.
3. For INDPRO, choose a transformation from the estimand and time-series rationale, not the observed alpha. Raw level, log level, log difference, and detrended residuals answer different questions.
4. Review domain independence and shared nuisance structure; different file names or physical labels alone do not prove independent replication.
5. Keep the candidates unapproved until provenance, independence, estimator validity, and a confirmatory null protocol are all satisfied.

### P3 — Improve diagnostic clarity (non-scientific behavior change)

The current eligibility log labels sunspots `measurement=True` and also reports `missing_provenance_registry_entry`, while separately saying the primary domain is excluded from the secondary replication count. This is confusing but does not justify adding sunspots to the secondary count. A later reporting-only change may suppress the secondary-registry warning for the primary domain or explicitly label it `PRIMARY_DOMAIN_NOT_COUNTED_AS_SECONDARY`. Do not change the eligibility count or scientific gates to make the log look cleaner.

### P4 — Keep the scientific scope honest

- `unittest` success, compilation success, checksum matches, and clean-checkout reproduction are software/integrity evidence; they are not independent scientific replication.
- A failed calibration does not by itself falsify the broad HCM, but it blocks the present confirmatory use of this null/test combination until adequately reviewed.
- A non-rejected primary null (`p=0.999001`) is not positive support for the hypothesis.
- Current evidence does not establish HCM causation, universality, consciousness, market advantage, or a Nobel-level result. Recognition can only follow a defensible, independently scrutinized result; it cannot be guaranteed by a workflow or package.
