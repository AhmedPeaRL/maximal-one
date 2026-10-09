# Secondary Domain Acquisition and Null Calibration V1

## Status

- Protocol status: `CANDIDATE_ACQUISITION_AND_EXPLORATORY_CALIBRATION`
- Scientific claim: `UNDER_INVESTIGATION`
- Confirmatory null: `NOT_FROZEN`
- Eligible secondary domains at protocol creation: `0`
- Claim-promotion authority: `NONE`

---

## Candidate selection before endpoint inspection

1. hadcet_monthly: official Met Office monthly mean Central England temperature series. Source: `https://www.metoffice.gov.uk/hadobs/hadcet/data/meantemp_monthly_totals.txt`
2. fred_indpro: Federal Reserve Industrial Production: Total Index distributed by FRED. Source: `https://fred.stlouisfed.org/series/INDPRO`
3. fred_dexuseu remains a negative-control candidate only, not a replication domain under this plan, until a separate protocol justifies its endpoint and sampling semantics.

Selection is based on source availability, monthly cadence, and expected record length---not on alpha, p-values, or observed agreement. Candidate status does not establish independence or replication.

---

## Temporal interpretation

- The primary and these two candidates are monthly series.
- Under the current frequency band `[0.01, 0.05]` cycles per observation, the nominal period is approximately 20 to 100 monthly observations.
- This interpretation must be stated explicitly in the claim protocol and is not transferable unchanged to daily data.
- Do not change the band after seeing any candidate endpoint.

Any change to the canonical band requires an explicit amendment and fresh validation.

---

## Acquisition and immutable snapshots

• Run python `analysis/acquire_secondary_domain_snapshots.py` once from the repository root.
The script preserves raw source bytes under `real-data/source-snapshots/`, records retrieval metadata and SHA-256 checksums in `secondary_source_manifest_v1.json`, and generates separate date,value analysis files.
It reuses a previously manifested snapshot rather than silently overwriting it.

A new data vintage must be archived as a new snapshot and separately documented.

• Raw snapshots, manifest, and generated analysis files must be committed together.
Do not hand-edit any of these files.
Do not fill missing values, interpolate months, or concatenate across gaps.

---

## Integrity audit

Run python `analysis/audit_secondary_monthly_domains.py`.

A passing result verifies only that the recorded raw and parsed checksums match, dates are sorted and unique, every month in the represented window is present, values are finite, and at least 1024 monthly observations are available.
It does not approve provenance, independence, null adequacy, or replication.

---

## Null Type-I calibration

`analysis/calibrate_null_type1.py` evaluates the existing implemented test on fixed synthetic Gaussian AR(1), AR(2), AR(5), and AR(10) scenarios.

The default run is a pilot and is never sufficient to freeze the null.
A calibration assessment requires at least 1000 valid outer repetitions per scenario and at least 200 inner surrogate draws per test.
The report remains limited to the tested synthetic families and never freezes the null automatically.

A pilot can be run with:
`python analysis/calibrate_null_type1.py --repetitions 10 --surrogates 200`

A full assessment can be requested with:
`python analysis/calibrate_null_type1.py --repetitions 1000 --surrogates 200`

- The full run may be computationally expensive.
- Preserve its artifact even if it fails.
- Do not increase the AR order limit, alter the endpoint, or choose a model based on a favorable p-value.

A Type-I calibration pass is necessary but not sufficient: residual ACF/PACF, stationarity, parameter stability, surrogate validity, boundary saturation, effective sample size, and nuisance preservation still require documented review.

---

## Promotion remains blocked until all conditions are met

- Exact source snapshot and checksum are committed.
- Monthly integrity audit passes.
- Provenance fields are complete and reviewed.
- Independence and shared nuisance review is documented before endpoint analysis.
- The null model and thresholds are reviewed and prospectively frozen; no result-dependent selection is allowed.
- Fresh primary reanalysis and fresh candidate analysis occur after the freeze.
- Each domain independently meets the same declared endpoint, estimator, frequency band, direction, null family, and testing rule.
- At least two secondary real domains pass all eligibility and replication criteria.
- All existing consistency, adversarial-control, and clean-checkout reproducibility gates pass.

Never set `replication_eligible` or `approved_for_replication` to true merely because an acquisition or integrity audit passed. Never mark `NULL_CONFIRMATORY_READINESS_V1.json` ready automatically from this calibration script.
