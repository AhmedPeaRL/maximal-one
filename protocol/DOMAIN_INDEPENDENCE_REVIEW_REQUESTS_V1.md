# Independent Domain-Independence Review Requests V1

Status: REQUEST FOR INDEPENDENT HUMAN REVIEW
No replication eligibility or confirmatory authority is granted.

Repository:
https://github.com/AhmedPeaRL/maximal-one

Review context:
The primary series is the monthly sunspot-number series currently stored at
real-data/sunspots_full.csv.

The current file contains 3328 monthly rows from 1749-01 through 2026-04.
Its candidate source identity is WDC-SILSO SN_m_tot_V2.0.
Full raw-source prefix comparison is pending.

The climate and economic datasets are secondary candidates only.
Neither is currently approved as an independent replication domain.

## A. Climate-domain review

Dataset:
HadCET monthly mean Central England temperature

Path:
real-data/hadcet_monthly.csv

Window:
1659-01 through 2025-12

Rows:
4404

Raw SHA-256:
e19be737e1d7abcc0060fd93d315e5dc893ca99ccdc7188b7b60149f1addf7f1

Parsed SHA-256:
2024e93ad1aceb97b26ff67516c39abbe714b50c52b310c1c288e345ea46308a

The repository records monthly continuity and time-integrity checks as passed.
Replication eligibility remains false pending independent review.

Please assess:

1. Whether HadCET is sufficiently independent of the primary sunspot series.
2. Whether direct or indirect solar forcing creates shared physical dependence.
3. Whether regional climate dynamics, volcanic aerosols, ENSO, greenhouse forcing,
   aerosols, circulation regimes, station changes or urban effects are material.
4. Whether this regional temperature series is suitable for the intended
   cross-domain replication claim.
5. Whether the proposed stochastic null family is adequate for this climate series.
6. Whether the series should be classified ELIGIBLE, INELIGIBLE or CONDITIONAL.
7. If ineligible, what prospective alternative climate dataset would be suitable.

Do not infer independence merely from different file names or institutions.

## B. Economic-domain review

Dataset:
FRED INDPRO — Industrial Production: Total Index

Path:
real-data/fred_indpro_monthly.csv

Window:
1919-01 through 2025-12

Rows:
1284

Raw SHA-256:
9a07cd7f775a1783d5d2512d2b00014c8c5291fdb134ebc5998d8a8e567e007d

Parsed SHA-256:
4c45b3267e3c346a0c87a3c8c39467b86f2440ce6008fdb325b0c92dc5542560

The repository records monthly continuity and time-integrity checks as passed.
Replication eligibility remains false pending independent review.

Please assess:

1. Whether INDPRO represents an independent economic domain for this purpose.
2. Whether industrial cycles, energy use, climate shocks, policy, wars,
   financial shocks, global supply chains or shared time trends create
   important common causes.
3. Whether seasonal adjustment, index revisions, trend-cycle decomposition
   and structural breaks affect suitability.
4. Whether the proposed stochastic null family is adequate for this series.
5. Whether this series should be classified ELIGIBLE, INELIGIBLE or CONDITIONAL.
6. If ineligible, recommend a prospective alternative economic dataset.

## C. Prior exposure and confirmatory limitations

Endpoint-like historical values may have appeared in an earlier CI log,
run 38729766378. Whether the reviewer or project author personally inspected
those values is not established.

Please state whether this exposure compromises blindness or confirmatory
status and whether a new prospective data window or a different dataset is
necessary.

Do not silently exclude or replace a domain after seeing its result.

## D. Required report

Each report must include:

- Reviewer name, affiliation and relevant qualifications.
- Relevant publications or evidence of domain expertise.
- Explicit financial, professional, collaborative and intellectual
  conflict-of-interest disclosure.
- Exact dataset and source version reviewed.
- Independence assessment relative to the primary series and other domain.
- Measurement and sampling limitations.
- Null-model suitability assessment.
- Decision: ELIGIBLE, INELIGIBLE, CONDITIONAL or OUT OF SCOPE.
- Written rationale and any prospective requirements.
- Date and reviewer attribution.

No HCM endorsement is requested.

This request authorizes domain review only.
It does not authorize formal calibration, confirmatory execution,
protocol freeze, claim support or promotion.
