## Secondary Domain Selection Plan V1

# Status

- Protocol status: `PRE_CONFIRMATORY_CANDIDATE_REVIEW`
- Scientific claim status: `UNDER_INVESTIGATION`
- Confirmatory status: `NOT_READY`
- Required independent secondary real domains: `2`
- Currently confirmed eligible secondary domains: `0`
- Claim-promotion authority: `NONE`

### This document records candidate selection and eligibility rules. It does not approve any candidate dataset or establish scientific replication.

1. Non-negotiable selection rules

1. Candidate eligibility must be evaluated without using the candidate's spectral exponent, p-value, or apparent agreement with the hypothesis.
2. No missing observations may be silently interpolated, synthetically generated, or concatenated across temporal gaps.
3. Every candidate must retain an auditable raw source snapshot and a SHA-256 checksum.
4. Timestamps, units, sampling cadence, time ordering, missingness, and preprocessing must be documented.
5. The analysis must use the declared endpoint, estimator, frequency band, direction, and null-testing protocol without candidate-specific optimization.
6. A candidate that fails a declared eligibility criterion remains excluded. The criterion must not be weakened after its result is observed.
7. The primary sunspot domain and derived sunspot datasets do not count as secondary independent domains.
8. Measurement validity, estimator validity, and scientific replication are separate decisions.

2. Candidate A: Daily foreign-exchange observations

- Candidate identifier: `fred_dexuseu`
- Source: Federal Reserve Board, published through FRED
- Series identifier: DEXUSEU
- Source URL: `https://fred.stlouisfed.org/series/DEXUSEU`
- Candidate physical domain: Foreign-exchange market
- Proposed observation: Published daily USD-per-EUR exchange rate
- Candidate status: NOT_YET_AUDITED
- Replication eligibility: FALSE

Required checks before eligibility review:

- Preserve the original downloaded file and retrieval date.
- Record the source citation, units, date range, and SHA-256 checksum.
- Define the market-day sampling convention before spectral analysis.
- Verify date ordering, duplicate dates, missing trading sessions, and source revisions.
- Do not fabricate weekend or holiday observations.
- Assess whether the sampling convention is compatible with the declared spectral estimator and frequency interpretation.
- Document relevant market-specific nuisance structure.
- Evaluate eligibility before computing or reviewing the candidate endpoint.

3. Candidate B: Daily streamflow observations

- Candidate identifier: `usgs_daily_streamflow`
- Source: United States Geological Survey
- Source URL: `https://waterservices.usgs.gov/docs/dv-service/`
- Candidate physical domain: Hydrology
- Proposed observation: Daily mean streamflow from one explicitly identified monitoring site
- Candidate status: NOT_YET_AUDITED
- Replication eligibility: FALSE

Required checks before eligibility review:

- Select and record a site identifier using source availability and data-quality criteria, not the spectral endpoint.
- Preserve the original source response and retrieval metadata.
- Record the site identifier, parameter code, units, date range, and SHA-256 checksum.
- Verify timestamp ordering, duplicate dates, missing days, quality flags, and measurement units.
- Confirm whether at least 1024 observations satisfy the declared temporal sampling requirements without synthetic filling.
- Document preprocessing, missingness, and relevant hydrological or climatic nuisance structure.
- Evaluate eligibility before computing or reviewing the candidate endpoint.

4. Shared protocol requirements

Both candidates must be assessed using the same declared:

- Primary spectral endpoint definition
- Welch estimator and canonical segmentation
- Frequency band and normalization rules
- Stochastic-null family and selection criteria
- Alternative direction and statistical tail
- Minimum valid surrogate count and p-value rule
- Internal consistency and adversarial-control requirements
- Computational reproduction and fingerprint requirements

The same null family does not imply identical fitted parameters across datasets. Model adequacy must be demonstrated for each domain under the frozen selection rules.

If the declared null protocol is not adequately calibrated, candidate analyses remain exploratory and cannot establish confirmatory replication.

5. Independence review

Before either candidate can count toward replication, document:

- Whether the domain is physically distinct from the primary domain
- Known shared drivers and nuisance structures
- Whether the measurement process creates a dependence that undermines the intended replication
- Whether the candidate is derived from, transformed from, or reused from another dataset
- Why the candidate provides an independent test of the same operational endpoint

Different dataset names alone do not establish independence.

6. Decision states

Each candidate must receive exactly one evidence-based decision:

- NOT_YET_AUDITED
- INELIGIBLE_DATA_INTEGRITY
- INELIGIBLE_PROVENANCE
- INELIGIBLE_SAMPLING
- INELIGIBLE_NULL_ADEQUACY
- ELIGIBLE_FOR_PROSPECTIVE_REPLICATION_REVIEW

Eligibility does not mean replication succeeded. Replication success additionally requires the declared endpoint result, null rejection, direction agreement, and all other protocol requirements.

7. Prospective validation

Any changes made after examining endpoint results must be recorded as exploratory amendments.

After the null family, candidate eligibility rules, endpoint, and analysis protocol are frozen, run a fresh validation using data not used to optimize those choices. Record the exact commit, source checksums, environment, generated artifacts, and all failed as well as passed gates.

8. Current conclusion

No candidate in this plan is approved for replication at the time this document is created.

The scientific claim remains UNDER_INVESTIGATION. This plan grants no authority to promote the claim and does not establish causation, universality, a consciousness mechanism, or HCM validity.
