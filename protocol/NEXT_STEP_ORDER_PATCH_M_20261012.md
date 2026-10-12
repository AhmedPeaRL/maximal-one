# Next-Step Order — Patch M — 2026-10-12

This order is designed to minimize accidental changes from a phone. It deliberately postpones endpoint computation.

## Step 1 — Add documentation only

Add the four Patch M files exactly as named in `README_AR.md`. Commit with:

`Add evidence-preserving live-state triage and audit plan`

Do not edit `core-scientific/strict_claim.json`, the eligibility gate, the AR order range, or Type-I acceptance thresholds in this commit.

## Step 2 — Audit the exact old Actions artifacts

Start with the runs/artifacts already referenced in project notes, including run `38088677966` (Type-I calibration outputs) and the run that generated the `0.947` boundary fraction (`38040221517`, as reported in the existing reconciliation record). Verify each exact artifact and commit; do not assume a run contains HadCET/INDPRO endpoint results merely because it is part of the same workflow family.

For HadCET and INDPRO, find every prior run that could have computed endpoint alpha/p-values or rendered endpoint plots. Fill the exposure audit table with exact IDs and evidence.

## Step 3 — Reconcile eligibility output

Download the eligibility artifact from the same commit/run as the pasted log. Determine whether the apparent name/reason mismatch comes from copied/interleaved logs, artifact revision mismatch, or code. Do not modify gate decisions during this check.

## Step 4 — Freeze the technical choices

Complete `protocol/SECONDARY_DOMAIN_PREANALYSIS_DECISION_TEMPLATE_V1.md` with one primary window for HadCET and one primary transformation for INDPRO, plus missingness, estimator, independence, multiplicity, and null-adequacy decisions. Use source/methodological criteria, not endpoint alpha. The current AR(p) null is explicitly not frozen; a confirmatory test cannot proceed until an appropriate null and its calibration/adequacy rule are prospectively resolved.

Record the real UTC decision time and commit SHA. Keep the researcher exposure statement distinct from machine audit findings. Do not backdate.

## Step 5 — Only after Steps 2–4

A fresh endpoint run may be considered only after the completed protocol and a suitable confirmatory null protocol are committed. Label it prospective only relative to those commitments. If the existing AR(p) null remains not frozen or fails calibration, do not call the output confirmatory and do not promote the claim.

## Current stop conditions

- Independent replication domains: `0/2`.
- Primary stochastic null: not rejected (`p = 0.999001` in the supplied current contract output).
- AR(2) and AR(10) calibration scenarios: failed the current Type-I acceptance rule.
- `0.937` versus `0.947`: unresolved reconciliation.
- Eligibility diagnostic log mismatch: review required.
- Claim status: `UNDER_INVESTIGATION`; promotion authority: `false`.
