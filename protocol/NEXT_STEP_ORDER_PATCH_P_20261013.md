# Next-Step Order — Patch P — 2026-10-13

**Purpose:** Safely sequence the next work from the currently supplied evidence. This is a workflow order, not a scientific result or preregistration.

## Step 0 — Freeze the current evidence

Do not edit scientific inputs or gates. Preserve the current workflow logs, JSON artifacts, repository ZIP, and their SHA-256 values. Do not reapply earlier patches that are already present.

## Step 1 — Reconcile the two reported commit identities

The supplied workflow excerpt reports commit `6f3430ce9368b956d0c2e35dff1f7bd9c9885ff7`; the reviewed archive's `LIVE_STATE_TRIAGE_20261012.md` records `3d649a34a6cdf63a05dd8b5aeed03ee4c4d94a5c`. These are different identifiers. Obtain the exact run ID and verify `GITHUB_SHA`, `git rev-parse HEAD`, and the artifact IDs from the same run. Do not treat files from the archive as if they are the same run's artifacts until this is resolved.

## Step 2 — Confirm the exact eligibility artifact

Download the `dataset_eligibility_gate.json` artifact from the same run that emitted the pasted eligibility log. Record run ID, commit SHA, artifact ID/name, download SHA-256, and test/command exit codes. The supplied excerpt is not enough to establish that a prior mismatched excerpt was a code defect. Change label code only if the discrepancy reproduces against one exact commit and artifact, with a regression test.

## Step 3 — Audit prior HadCET/INDPRO endpoint exposure

Search historical Actions runs and artifacts for outputs that could contain endpoint alpha, p-values, or plots. Record each run ID, commit SHA, timestamp, artifact ID, and whether the value was generated, exposed in logs/artifacts, or actually inspected by the researcher. Keep `UNKNOWN` where evidence is absent; absence of a search hit is not proof that no output was generated.

## Step 4 — Review null-model adequacy before any secondary endpoint

The primary capacity audit reports observed AR order 20 at the declared maximum and 937/1000 surrogate refits at that boundary. A diagnostic scan also reaches its order-40 scan boundary. The specified AR(2) and AR(10) Type-I calibration scenarios fail the current rule. Treat these as reasons to conduct a prospective methodological review, not reasons to tune the gate after seeing outcomes.

Before any confirmatory endpoint run, the research record must identify and justify a null family, fitting/order-selection procedure, calibration suite, acceptance criteria, and handling of failed calibration. Any change must be declared and committed before new confirmatory outputs are generated or inspected. If no adequate null protocol has passed, secondary outputs must not be called confirmatory and the claim must not be promoted.

## Step 5 — Complete source-grounded secondary-domain decisions

Only after the exposure audit and null-model decision are complete, fill `protocol/SECONDARY_DOMAIN_PREANALYSIS_DECISION_TEMPLATE_V1.md`. Use source/measurement criteria to choose a HadCET window and scientific-estimand criteria to choose one INDPRO transformation. Record missingness, estimator settings, multiplicity, provenance, independence, and the null-calibration prerequisite. Do not choose settings by endpoint alpha or p-value. Record the actual UTC time and commit SHA; do not backdate.

## Step 6 — Run in this order

1. Identity/artifact audit.
2. Eligibility artifact comparison and any justified label-only regression test.
3. Historical endpoint exposure audit.
4. Prospective null-family calibration/adequacy decision.
5. Completed and committed secondary-domain preanalysis protocol.
6. Only then consider a fresh candidate endpoint run, and label it confirmatory only if all prerequisites genuinely passed before outcome generation/inspection.

## Current stop conditions

- Independent real-domain replication: `0/2`.
- Primary stochastic null: not rejected in the supplied current contract output (`p = 0.999001`).
- Primary null capacity review: triggered; diagnostic-only.
- Type-I calibration: supplied AR(2) and AR(10) scenarios fail the current acceptance rule.
- HadCET and INDPRO: structurally measurable, not approved replications.
- Claim status: `UNDER_INVESTIGATION`; claim support and promotion authority remain `false`.

## Change boundary

This note authorizes documentation and audit work only. It authorizes no scientific-input changes, no gate relaxation, no threshold tuning, no endpoint computation before protocol completion, and no claim promotion.
