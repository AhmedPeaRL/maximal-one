# Live Replication Blocker Review — 2026-10-17

**Repository:** `AhmedPeaRL/maximal-one`  
**Reviewed commit:** `345f3fe95af8c3da107d13f8390790082f589e7a`  
**Scientific status:** `UNDER_INVESTIGATION`  
**Claim support:** `false`  
**Promotion authority:** `false`  
**Review type:** independent review of the supplied repository ZIP plus the linked GitHub Actions job records available for this commit. This is not an external peer review or a new scientific replication.

## 1. Decision summary

The current promotion failure is scientifically consistent with the declared gate. The final decision for workflow run `39033172805` records `REPLICATION_ELIGIBILITY_INSUFFICIENT`, `0/2` eligible independent secondary domains, `claim_support_granted_by_this_job=false`, and `promotion_authority_granted_by_this_job=false`. Workflow run `39033344062` also fails at the dataset-eligibility contract. These are blocking scientific-eligibility outcomes, not evidence that the code should be weakened.

The core-proof jobs passing does not imply claim promotion. In run `39033172805`, the final claim/workflow gate failed after the supporting computational jobs completed. Preserve this distinction and retain the failure records.

## 2. Dataset decisions from the current record

| Candidate | Observed state | Required decision |
|---|---|---|
| `hadcet_monthly` | 4,404 rows; structurally measurement-valid; replication eligibility and provenance approval false | Keep unapproved. Source hashes reconcile to the committed snapshot, but independent-domain suitability, prior endpoint exposure classification, and confirmatory-null adequacy are unresolved. |
| `fred_indpro` | 1,284 rows; structurally measurement-valid; replication eligibility and provenance approval false | Keep unapproved. Source hashes reconcile to the committed snapshot, but independent-domain suitability, prior endpoint exposure classification, and confirmatory-null adequacy are unresolved. |
| `cosmic_rays` | 3,698 values; structural measurement validity does not establish regular sampling; source provenance fields are null/pending | Exclude from replication. The timestamp audit finds 321 non-hourly intervals and a longest contiguous hourly run of only 486, below the declared 1,024-observation minimum. |
| `solar_wind_speed` | Provenance/cadence pending and potential shared solar-cycle nuisance | Do not count as independent replication without a complete source, cadence, and nuisance review. |
| `co2` | 816 rows, below the 1,024-observation replication minimum | Do not count as replication. |
| `passengers`, `temperature`, `sp500` | Below current length/measurement eligibility rules | Do not count as replication. |
| `extended` | Derived/related to the primary sunspot domain | Do not count as an independent secondary domain. |

No metadata-only change can repair these blockers. Eligibility must remain outcome-independent and must not be changed to reach `2/2`.

## 3. Prior endpoint exposure: important correction

The repository's `protocol/PRIOR_ENDPOINT_EXPOSURE_AUDIT_HADCET_INDPRO_V1.md` records that workflow run `38729766378`, commit `3f0ccefbb1304fad1733a91c185c05aa3d619968`, generated and displayed endpoint-like estimates in CI logs on 2026-10-15:

- `hadcet_monthly.csv`: `0.150544`
- `fred_indpro_monthly.csv`: `2.530521`

The log establishes generation and display, but it does **not** establish whether the researcher personally inspected the values before the decision. Keep those questions separate. The researcher statement that the values were not personally viewed is not contradicted as a statement about personal viewing; it does not erase machine generation/display. These existing estimates must not be described as preregistered confirmation. Preserve the record and classify the exposed analyses conservatively as exploratory/post-observation unless a narrowly defined untouched confirmation dataset or period is prospectively established.

## 4. Null protocol and calibration

The current stationary Gaussian AR(p), AIC-selected over orders 1–20, remains exploratory and is not approved for confirmatory use. The recorded primary null p-value is `0.999001`; the current specified null was not rejected. The primary capacity audit reports maximum-order selection in `937/1000` surrogate refits (`0.937`), which triggers model-capacity review but does not establish or falsify the scientific hypothesis.

The existing Type-I acceptance rule must remain unchanged. Under that rule, the recorded AR(2) and AR(10) calibration scenarios fail. Do not tune thresholds, discard failures, or select a replacement null because it yields a preferred endpoint result. The prospective protocol remains `DRAFT_NOT_FROZEN` / `DO_NOT_RUN_CONFIRMATORY_ANALYSIS` until the null-family, calibration, failure-handling, and independent review prerequisites are resolved.

## 5. Fingerprint and execution identity

The reviewed commit contains `artifacts/fingerprint.txt` value:

`9f3a829033084e6b29d2849de59ce799c192a44cd8ca8eeaf28c1c6ddbddcdb5`

The associated workflow's fingerprint-publication and public-source sanity-check steps are recorded as successful. Do not manually replace this value with an invented or older value. Preserve the commit and run artifacts. A fingerprint is an identity/integrity aid; it is not evidence of scientific validity or claim support.

## 6. Required next actions

1. Preserve commit `345f3fe95af8c3da107d13f8390790082f589e7a`, workflow runs `39033172805` and `39033344062`, earlier exposure run `38729766378`, and their artifacts/logs.
2. Keep HadCET/INDPRO unapproved; complete the machine-exposure audit and an independent nuisance/independence review. Do not call their prior endpoint estimates preregistered confirmation.
3. Keep cosmic rays excluded: the current observed cadence/run-length result does not meet the declared replication requirements. Do not interpolate or silently drop timestamps to force eligibility.
4. Complete an independent methodological review and calibration plan for the null. Freeze the entire protocol and source/data identities before any fresh confirmatory endpoint calculation or inspection.
5. Select at least two eligible independent domains by predeclared source/scientific criteria—not alpha, p-value, or favorable outcome. Because current candidates have been examined by automated endpoint workflows or remain otherwise ineligible, identify genuinely untouched data/periods or newly acquired domains before confirmatory analysis.
6. Re-run the existing eligibility, provenance, time-integrity, null-calibration, and promotion gates unchanged. A failure must remain a failure.

## Final status

`BLOCKED — 0/2 eligible independent secondary domains; confirmatory null not frozen; fresh confirmatory validation not completed.`

This review grants no claim support or promotion authority and supports no inference of HCM causation, consciousness, mechanism, or universality.
