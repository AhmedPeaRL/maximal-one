# Prospective Raw Audit Runbook — 2026-10-17

**Status:** `RAW_AUDIT_PENDING` until the dedicated workflow completes and the artifact is independently reviewed.  
**Purpose:** Preserve source bytes and audit provenance/time/missingness/cadence/structural eligibility only.  
**Endpoint computation:** Not performed and not authorized by this workflow.  
**Claim support / promotion authority:** `false`.

## Candidate sources

1. HadUKP England & Wales monthly precipitation (EWP), direct text file: `https://hadleyserver.metoffice.gov.uk/hadobs/hadukp/data/monthly/HadEWP_monthly_totals.txt`; metadata/download page: `https://hadleyserver.metoffice.gov.uk/hadobs/hadukp/data/download.html`. The publisher notes that recent monthly values may change after quality control; preserve retrieval time and response metadata, and do not infer an immutable version when none is provided.
2. FRED CPIAUCNS, bounded CSV: `https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCNS&cosd=1913-01-01&coed=2025-12-01`; series metadata: `https://fred.stlouisfed.org/series/CPIAUCNS`. The series is BLS-produced, monthly, and not seasonally adjusted.

The audit window is predeclared as 1913-01 through 2025-12 inclusive for structural comparability. This is an acquisition/eligibility audit window only, not an approved confirmation window. No transformations for scientific analysis are selected by this audit.

## Files produced by the workflow

- `real-data/prospective-raw-snapshots/`: exact downloaded response bytes. The program refuses to overwrite an existing raw file.
- `real-data/prospective-parsed/`: newly generated `date,value` representations. These are derived and are not substitutes for the raw files.
- `real-data/prospective-raw-snapshots/prospective_raw_audit_manifest_v1.json`: source URLs, UTC retrieval time, response headers, raw SHA-256, parsed-data SHA-256, and status fields.
- `artifacts/prospective_raw_audit_report.json`: independent timestamp, duplicate, cadence/gap, missingness, length, and frequency-bin structural checks.

Raw-file SHA-256 is computed over the untouched response bytes. Parsed-data SHA-256 is computed separately over the exact derived CSV bytes. Missing sentinel `-99.9` in HadUKP is represented as missing in the parsed file; it is never silently converted into a measured value. No interpolation, padding, endpoint computation, alpha calculation, p-value calculation, or favorable-candidate selection occurs here.

## Status semantics

- `UNKNOWN` / `PENDING`: not verified; do not convert to `NO`, `PASS`, or `FAIL` without evidence.
- `STRUCTURAL_CHECKS_PASS_PENDING_INDEPENDENCE_AND_NULL_REVIEW`: only the listed mechanical data checks passed. This is not replication approval.
- `STRUCTURAL_ELIGIBILITY_NOT_ESTABLISHED`: at least one declared mechanical condition did not pass.
- `RAW_AUDIT_INCOMPLETE`: acquisition or parsing failed; inspect preserved raw bytes and error details before any retry.
- `prior_endpoint_exposure = NOT_VERIFIED_BY_GLOBAL_HISTORICAL_AUDIT`: this run does not prove that a candidate endpoint was never computed or displayed elsewhere.

## Required manual review after the run

1. Download and retain the workflow artifact; verify its SHA-256 digest from the artifact metadata where available.
2. Inspect each raw source and parsed representation; confirm raw bytes are unchanged and the hashes differ only because the parsed file is a distinct representation.
3. Resolve source-vintage/revision metadata. If the publisher does not provide a stable version identifier, keep the vintage status `UNKNOWN` and rely on the preserved raw bytes plus retrieval metadata.
4. Review candidate endpoint exposure globally; this script does not perform that historical audit.
5. Review independence and shared nuisance scientifically. Length and timestamp continuity do not establish independence.
6. Independently approve a suitable null family and calibration plan. The AR(p) AIC family remains exploratory and unapproved; prior Type-I calibration failures remain failures.
7. Freeze the complete confirmatory protocol before any endpoint is calculated or inspected. Do not use candidate endpoint values to choose the candidate, transformation, window, null family, tail, or acceptance rule.
8. Keep replication at `0/2` unless at least two independent real domains satisfy all required criteria.

## Safety invariant

This workflow is separate from the existing claim-promotion workflow. It has read-only repository permissions and uploads its results as an artifact. It does not edit `strict_claim.json`, acceptance thresholds, candidate registries, or promotion flags.
