# Scientific and Governance Status Addendum — 2026-11-17

- **Repository:** `AhmedPeaRL/maximal-one`  
- **Review branch:** `review/type1-v4-remediation`  
- **Current review-branch commit:** `1b57c9d5e6b411270ecc1c91ac8e26c1923b5ab2`  
- **Main commit:** `9749de9253f144eeda9e1b60cb219cfc5f201ecc`  
- **Pinned scientific/human-review target:** `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`

**Status:** `REVIEW_ONLY — SCIENTIFIC_GATES_OPEN — NO_NEW_SNAPSHOT`

## 1. Identity and governance

The pinned human-review target remains `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`.

The current review branch is 267 commits ahead of that target and has not diverged from it. The review branch and `main` have diverged; no merge, rebase, or main-branch modification is authorized by this addendum.

No newer human-review snapshot is issued.

The latest pinned-target inventory and snapshot evidence remains identity/coverage evidence only. The target population contains 1,800 occurrences. The manual adjudication overlay contains zero records. All unresolved classifications remain `UNKNOWN` or `PENDING`; automated tools and AI must not substitute for human adjudication.

## 2. Primary null-model adequacy

The current exploratory null is stationary Gaussian AR(p), AIC order selection over p=1..20, with common effective observations and surrogate refitting.

The primary capacity audit reported 1,000 valid surrogate refits and a boundary fraction of 0.937 at order 20. A separate source-scoped stream reported 0.947. These estimates remain tied to their respective runs and are not merged.

An exploratory order scan reported its best AIC at the maximum tested order, 40. This does not establish that AR(40) is the correct model or authorize increasing the production order cap.

**Decision:** AR(1..20) is not demonstrated adequate for confirmatory use. Its inadequacy is not conclusively established either. The null family and target-versus-nuisance boundary require attributable independent statistical review.

No production null change, order-cap increase, formal calibration, or confirmatory execution is authorized.

`protocol/AR20_PROSPECTIVE_DIAGNOSTIC_PLAN_DRAFT_20261112.md` remains a design draft only.

## 3. Cosmic-ray candidate

The existing `real-data/cosmic_rays.csv` contains 3,698 timestamped observations, 321 non-hourly intervals, and a longest uninterrupted hourly segment of 486 observations. The current clean file drops timestamps. The source provenance is incomplete.

The existing cosmic-ray candidate is not replication-eligible. No interpolation, concatenation of separated segments, or reduction of the 1,024-observation minimum is permitted.

The Oulu Cosmic Ray Station is a prospective source candidate because it provides hourly neutron-monitor data from 1964 onward. A specific raw 1,024-hour continuous segment has not yet been acquired and verified.

Cosmic-ray intensity is modulated by solar activity and is not automatically independent of the sunspot primary domain. Treat it as a possible mechanistic comparator, not an independent replication, unless an independent domain reviewer approves a defensible independence argument.

## 4. Historical HadCET and INDPRO endpoints

Historical endpoint-like estimates were generated and displayed in CI run `38729766378`:

- HadCET: approximately 0.150544
- FRED INDPRO: approximately 2.530521

Whether the researcher personally inspected those values before relevant decisions remains unknown.

Both historical results remain exploratory/post-observation and are not confirmatory replications. Source provenance, vintage, domain independence, shared nuisance, and null adequacy remain subject to independent review.

## 5. HadUKP candidate

The prospective raw audit recorded 1,356 monthly observations from 1913-01 through 2025-12, with no missing values or monthly gaps in the declared window.

Raw SHA-256: `75a10dcc597c4b0a452cdd8d22dcad6a0ef677bbe8f1a7d6065806123752882d`

Parsed SHA-256: `3c757cd2f7258944ba393906ea3fd7294b48a09782319381f91d9117652b87df`

Structural checks passed. Source-vintage interpretation, global prior-endpoint exposure, independence/shared-nuisance review, and confirmatory-null adequacy remain pending.

**Decision:** structurally valid candidate only; not approved for endpoint computation or replication.

## 6. CPIAUCNS candidate

The prospective raw audit recorded 1,356 monthly rows from 1913-01 through 2025-12, with 1,355 numeric observations and one missing observation at 2025-10-01.

The October 2025 all-items CPI observation is unavailable because BLS could not collect the relevant survey data during the 2025 lapse in appropriations and did not publish an October all-items CPI estimate.

No interpolation, carry-forward, or substitution with a Treasury TIPS contingency index is permitted.

A pre-gap window ending 2025-09-01 contains 1,353 monthly observations and may be evaluated as a separate prospective candidate. It is not approved by this addendum. The selected source vintage must be preserved through a dated ALFRED snapshot, with raw and parsed hashes.

Prior endpoint exposure and domain independence remain pending. No endpoint was computed by the raw-audit workflow.

**Decision:** candidate only; current 1913-01 through 2025-12 window fails the all-values-present requirement.

## 7. Replication status

Approved independent secondary domains: `0/2`.

HadUKP and a possible pre-gap CPIAUCNS window remain candidates only. Cosmic rays are not independent by default because of solar modulation. HadCET and INDPRO historical endpoints remain exploratory/post-observation.

No domain may be promoted based on structural validity alone.

## 8. Primary sunspot source discrepancy

The local primary analysis file and the current official WDC-SILSO source have a recorded version discrepancy. The analysis file must not be silently updated or extended. Resolve the four prefix value/flag mismatches and six newer official rows through a documented source-version decision before any new primary confirmatory analysis.

## 9. Software assurance

Run `43978201708` completed its guard job but the dependency-refresh job was cancelled before installation/testing completed. Publish and exact assurance were skipped. No verified dependency lock was published.

Run `43978295638` scanned review-branch commit `1b57c9d5e6b411270ecc1c91ac8e26c1923b5ab2`. It recorded 84 ShellCheck diagnostics, two low-severity `zizmor/self-repository` findings, and an OpenSSF Scorecard score of 7.5. The OSV inventory identified vulnerable package versions in the current dependency manifests.

These results are open software-assurance findings, not a clean security pass.

## 10. Independent human reviews

The four requested independent reviews remain pending:

1. Statistical-methods and null-model adequacy.
2. Climate-domain independence and HadUKP/HadCET suitability.
3. Econometric-domain independence and CPIAUCNS/INDPRO suitability.
4. GitHub Actions and CI security review.

No automated or AI-generated report substitutes for an attributable human decision.

## 11. Non-authorization

The following remain unchanged:

- `protocol_freeze = NOT_FROZEN`
- `formal_calibration_authorized = false`
- `confirmatory_execution_authorized = false`
- `claim_support = false`
- `promotion_authority = false`
- `approved_independent_secondary_domains = 0`
- `replication_status = 0/2`

This addendum records evidence and open decisions only. It does not authorize a new snapshot, protocol freeze, formal calibration, confirmatory execution, claim promotion, or a change to `main`.
