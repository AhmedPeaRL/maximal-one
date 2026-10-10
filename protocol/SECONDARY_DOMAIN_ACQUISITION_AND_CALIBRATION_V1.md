# Secondary Domain Acquisition and Null Calibration V1.1 — Remediation Amendment

## Status

- Claim: `UNDER_INVESTIGATION`.
- Confirmatory null: `NOT_FROZEN`.
- Eligible secondary domains: `0` until separate provenance, independence, null and endpoint reviews pass.
- Claim/promotion authority from this amendment: `NONE`.

---

## Fixed candidate window

The candidate analysis window ends inclusively at 2025-12-01 (December 2025 monthly observation).

This cutoff is fixed before analysis of either candidate's alpha.
Data after the cutoff remain in the raw snapshot but are excluded from the parsed analysis CSV.

Do not change the cutoff after examining endpoint values; any change requires a dated protocol amendment and fresh validation.

---

## Source endpoint and HadCET missing-value rule

The HadCET raw snapshot is requested from the `hadleyserver.metoffice.gov.uk` data host named in the publisher download page, rather than the alternate `www.metoffice.gov.uk` path.

The exact URL and bytes are captured in the manifest; if the publisher changes the endpoint, stop and record a protocol/source update rather than silently substituting a mirror.

The documented Met Office sentinel -99.9 is parsed as missing, never as a temperature. 

Missing observations remain explicit blank value cells and are reported by the audit.
They are not imputed, interpolated, or silently dropped.
Any missing value in the fixed analysis window blocks the monthly integrity audit.
Broad plausibility bounds are used only as error checks: `HadCET [-20, 40] degrees C` and `INDPRO [0, 1000]`; they are not scientific selection criteria.

---

## Acquisition and retries

The acquisition script requests the bounded FRED INDPRO window first (1919-01-01 through 2025-12-01), then tries the canonical FRED CSV URL as a fallback. Each URL receives two attempts with a 90-second socket timeout.
The exact successful URL, candidate URL list, retrieval time and SHA-256 are recorded after a complete response.
It processes the second source even if the first fails and preserves a partial manifest.

This is retry/fallback handling, not a guarantee that FRED is reachable from GitHub Actions.
The artifact should be uploaded even on failure.
A failed or partial acquisition must not be committed as an eligible dataset.

After a successful workflow, inspect the audit JSON first.
Then commit the raw snapshots, manifest, and parsed CSVs together.
Do not edit them by hand.

For a stable citation, prefer an archived source vintage with a durable identifier when available; the recorded live URL snapshot is still the byte-level reproducibility anchor for this run.

---

## Offline safety tests

Run from the repository root:
`python -m unittest discover -s tests -p 'test_secondary_acquisition_safety.py'`

These tests verify that -99.9 becomes missing, the fixed cutoff excludes 2026 rows, and the FRED parser respects the same cutoff.
They do not test live source availability or approve data.

---

## Type-I calibration sequence

Run Null Type-I Calibration (Synthetic Scenarios) with repetitions=10 first.
A completed pilot is labeled `PILOT_COMPLETED_NOT_CONFIRMATORY`; it is not a calibration pass and does not freeze the null. 

Review run time, valid/invalid replicate counts, p-value behavior, Wilson interval, and AR-order boundary diagnostics before considering 1000.

The workflow invokes the module with `python -m analysis.calibrate_null_type1_scenario`, avoiding the import-path failure from executing the file as a script.
A 1000-repetition run remains limited to the four synthetic Gaussian AR scenarios.
Before any confirmatory null freeze, a separately reviewed protocol must add relevant nuisance scenarios (including quasi-periodic structure, long-memory alternatives/controls, larger sample size such as N=3328, residual/stationarity/parameter-stability checks, surrogate adequacy, and effective sample-size accounting).

Do not add or tune these scenarios after looking at candidate alpha and then call them preregistered.

---

## Domain independence and transformations

Before computing candidate alpha, document why HadCET and INDPRO are independent enough for the intended replication claim and assess shared temporal confounders.
For INDPRO, the analysis scale (raw level, log level, growth rate, or a predeclared anomaly series) must be chosen from domain semantics and a prospective protocol before endpoint inspection.
A raw index with trend can produce spectral behavior dominated by nonstationarity.
The same numeric frequency band corresponds to 20–100 monthly observations here; do not transfer that interpretation to daily data.

---

## Promotion remains blocked until

- Raw source snapshots, retrieval metadata, SHA-256, parsed files, and exact analysis window are committed together.
- Monthly integrity audit passes with no gaps, missing values, checksum mismatch, or implausible values.
- Provenance and source-vintage review passes.
- Independence/shared-nuisance review is documented before endpoint analysis.
- Transformation and endpoint are fixed before candidate alpha is viewed.
- Null adequacy, Type-I calibration, residual/stationarity/parameter stability, model-capacity saturation, surrogate validity and effective sample size are reviewed; the null is frozen prospectively only after approval.
- Fresh primary reanalysis and candidate analyses run on the frozen protocol.
- At least two secondary real domains pass the same declared endpoint, direction, null family and testing rule independently.
- Adversarial controls and clean-checkout computational reproduction pass.

Never infer HCM causation, consciousness, universality, or market advantage from a spectral result alone.
