# Eligibility Diagnostic Log Discrepancy Review — 2026-10-12

**Status:** REVIEW REQUIRED — no gate change authorized.

## Why this review is required

In the supplied `REPLICATION ELIGIBILITY DIAGNOSTICS` log excerpt, some printed dataset names/statuses/reasons appear inconsistent with the dataset fields in the committed `artifacts/dataset_eligibility_gate.json` and with the current `analysis/eligibility_diagnostic_labels.py` transformation when applied to that JSON.

Examples to verify against the exact uploaded artifact and complete step log:

- The JSON reports `fred_indpro` has 1284 rows and its base reason is `eligible`; the excerpt appears to print a `series_shorter_than_canonical_nperseg` reason near this domain.
- The JSON reports `co2` has 816 rows, measurement validity true under the 256-row/20-bin measurement rule, but replication eligibility false because it is below the canonical 1024-row segmentation; the excerpt appears to label it `MEASUREMENT_INVALID`.
- The JSON reports `passengers` has 144 rows and measurement validity false; the excerpt appears to show it as measurement-valid with a cosmic-ray timestamp reason.
- The JSON reports `cosmic_rays` is not marked as a derived domain; the excerpt appears to label it `EXCLUDED_DERIVED_DOMAIN`.
- The JSON reports `extended` has 3327 rows and is derived; the excerpt appears to label it structurally invalid.

These observations may reflect interleaved/truncated output, a different artifact revision, or a real presentation/mapping issue. The pasted excerpt alone cannot decide which explanation is correct.

## Required investigation

1. Download the exact `dataset-eligibility-gate` artifact from the same workflow run and retain its original ZIP and SHA-256.
2. Compare the artifact's JSON to the JSON uploaded/committed for that exact commit. Do not compare artifacts from different runs or commits as if they were one run.
3. Read the complete log for the single step that emits `REPLICATION ELIGIBILITY DIAGNOSTICS`; verify whether lines from concurrent steps or separate runs were combined in the copied text.
4. Run the existing diagnostic-label unit tests against the exact commit/artifact. Record command, commit SHA, artifact SHA-256, exit code, and output.
5. If a reproducible code defect is confirmed, prepare a minimal follow-up patch with a regression test. Keep changes to explanatory labels/output only unless a separately reviewed protocol amendment authorizes a gate change.

## Prohibited shortcuts

- Do not change eligibility booleans, thresholds, row counts, domain names, or gate status to make the log look consistent.
- Do not mark HadCET or INDPRO as replication-eligible based only on row count or time-integrity pass.
- Do not use the log discrepancy to infer endpoint values or scientific support.

## Current decision

Until reconciled, retain `REPLICATION_ELIGIBILITY_INSUFFICIENT`, eligible independent replication domains `0/2`, and claim-promotion authority `false`.
