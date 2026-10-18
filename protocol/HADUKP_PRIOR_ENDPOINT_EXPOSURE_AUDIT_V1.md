# HadUKP EWP Source-Vintage and Prior-Endpoint Exposure Audit — V1

**Record date:** 2026-10-18  
**Repository commit reviewed:** `047b84f2c78bdf19e28e283afc1a9800aca32287`  
**Candidate:** UK Met Office HadUKP, England & Wales Precipitation (EWP), monthly totals  
**Status:** `STRUCTURAL_AUDIT_PASS; SOURCE_VINTAGE_REVIEW_PENDING; GLOBAL_ENDPOINT_EXPOSURE_UNKNOWN; INDEPENDENCE_REVIEW_PENDING; NOT_APPROVED`  
**Claim support:** `false`  
**Promotion authority:** `false`  
**Endpoint computation authorized:** `false`

## 1. Purpose and scope

This record separates source identity and structural validity from source-vintage approval, prior endpoint exposure, scientific independence, shared-nuisance review, and confirmatory-null adequacy. It is an audit record, not a replication claim. It must not be interpreted as proof that no prior endpoint was ever computed, plotted, inspected, or discussed.

The prospective raw audit workflow explicitly reports `prior_endpoint_exposure = NOT_VERIFIED_BY_GLOBAL_HISTORICAL_AUDIT`. Preserve that status until the documented audit scope has actually been searched and reviewed. Missing evidence remains `UNKNOWN` or `PENDING`, never `NO` by default.

## 2. Source identity and format

- Publisher/source: UK Met Office Hadley Centre / National Climate Information Centre, HadUKP.
- Series: England & Wales Precipitation (EWP), monthly totals.
- Data URL: `https://hadleyserver.metoffice.gov.uk/hadobs/hadukp/data/monthly/HadEWP_monthly_totals.txt`
- Metadata/download page: `https://hadleyserver.metoffice.gov.uk/hadobs/hadukp/data/download.html`
- Data-format page: `https://www.metoffice.gov.uk/hadobs/hadukp/data/data_format.html`
- The published monthly file format uses year, monthly values, and an annual total; `-99.9` is the documented missing-value sentinel and must never be treated as a measurement.
- The publisher notes that recent monthly values may be revised after quality control and that the monthly/seasonal files are updated on a regular schedule. Therefore, the retrieved file must be treated as a dated snapshot, not as a timeless immutable “latest” dataset.

## 3. Snapshot evidence from workflow run `39066915519`

Workflow: `https://github.com/AhmedPeaRL/maximal-one/actions/runs/39066915519/workflow`  
Artifact: `https://github.com/AhmedPeaRL/maximal-one/actions/runs/39066915519/artifacts/12113581637`

The run log reports the following values for the raw source snapshot:

- Retrieval time (UTC): `2026-10-17T20:29:27.373716Z`
- HTTP status: `200`
- Content type: `text/plain; charset=UTF-8`
- Last-Modified header: `Mon, 05 Oct 2026 09:26:16 GMT`
- ETag: `"6653-65d14794bbe00"`
- Raw bytes: `26195`
- Raw SHA-256: `eb2a20081a4673211783b0fe442007921d0f23a4683065954373c6ce0fa96637`
- Parsed SHA-256: `3c757cd2f7258944ba393906ea3fd7294b48a09782319381f91d9117652b87df`
- Audit window: `1913-01-01` through `2025-12-01`, inclusive
- Parsed monthly observations in that window: `1356`
- First/last timestamps: `1913-01-01` / `2025-12-01`
- Duplicate timestamps: `0`
- Invalid timestamps: `0`
- Missing/non-finite values in the parsed audit window: `0`
- Missing monthly steps/gaps: `0`
- Structural status: `STRUCTURAL_CHECKS_PASS_PENDING_INDEPENDENCE_AND_NULL_REVIEW`

**Important limitations:** The ETag and Last-Modified header are response metadata, not by themselves a complete scientific version identifier or proof of homogeneity. The run artifact records the raw and parsed hashes, but its presence does not mean the raw file has been committed to the repository or permanently archived. Preserve the exact artifact and its hashes. If an archival repository copy is later made, use a new immutable path and verify the raw SHA-256 byte-for-byte before committing; never rewrite or normalize the raw snapshot.

## 4. Prior endpoint exposure: status remains UNKNOWN

The current audit output explicitly states `NOT_VERIFIED_BY_GLOBAL_HISTORICAL_AUDIT`. Therefore, do not write “no endpoint was previously computed,” “the candidate was never inspected,” or “this is preregistered” based solely on this workflow.

A global exposure review should search and record, at minimum:

1. All reachable repository commits, branches, tags, releases, and relevant deleted-file history for `HadUKP`, `HadEWP`, `EWP`, this source URL, and derived candidate identifiers.
2. GitHub Actions workflow logs, run artifacts, cached/generated reports, and prior endpoint or plot artifacts where accessible.
3. Public website/GitHub Pages content, public research notes, Zenodo records, and any linked publication supplements under the researcher's control.
4. Local analysis files and prior exported archives that are actually available to the researcher and can be enumerated.
5. The exact endpoint values, plots, alpha/p-values, transformations, windows, and frequency bands previously calculated or viewed, if any; record each known exposure without deleting it.
6. The search boundary: sources and dates that were searched, sources not accessible, and the reviewer who performed the audit.

Do not infer absence from a failed text search alone. A search of repository history cannot establish that no local, private, or external calculation ever occurred. Record `UNKNOWN` for inaccessible or unaudited areas.

Required fields for the completed audit:

- Auditor identity/attributable record: `PENDING`
- Audit date and exact commit: `PENDING`
- Repositories/branches/tags/releases searched: `PENDING`
- Actions runs/artifacts/logs searched: `PENDING`
- Publications/websites/local archives searched: `PENDING`
- Known prior endpoint computations or exposures: `PENDING`
- Inaccessible scope and limitations: `PENDING`
- Final exposure classification (`KNOWN_EXPOSED`, `NO_EXPOSURE_FOUND_WITHIN_DEFINED_SCOPE`, or `UNKNOWN`): `PENDING`
- Independent review/sign-off: `PENDING`

Even if no exposure is found within a declared search scope, use the bounded statement `NO_EXPOSURE_FOUND_WITHIN_DEFINED_SCOPE`, not an absolute claim that exposure never occurred.

## 5. Scientific independence and shared nuisance

HadUKP is a climate/precipitation series, while the primary domain is a sunspot series. Different measured variables or publishers do not automatically establish independent replication. Before any endpoint is computed, the reviewer must assess plausible shared temporal drivers, climate variability/teleconnections, possible solar-related forcing, trends/regime changes, and any other nuisance structure relevant to the exact hypothesis. This assessment must be based on scientific domain knowledge and prespecified covariates/diagnostics, not on whether the candidate endpoint is favorable.

The review must distinguish:

- source/data independence;
- independence of the scientific process or domain;
- independence from the primary endpoint-development history;
- adequacy of the null model for this domain;
- eligibility under the existing minimum-length and frequency-resolution rules.

No single one of these establishes the others.

## 6. Required decision before endpoint analysis

Until all applicable fields below are independently reviewed and resolved, HadUKP remains a candidate only:

- [ ] Source identity and exact source-vintage interpretation reviewed.
- [ ] Raw snapshot preserved byte-for-byte and SHA-256 independently verified.
- [ ] Timestamp, cadence, missingness, sentinel, and audit-window checks reviewed.
- [ ] Historical endpoint-exposure audit completed with explicit search boundaries.
- [ ] Shared-nuisance and domain-independence assessment completed.
- [ ] Confirmatory null family and its calibration approved for the scientific estimand.
- [ ] Endpoint, transformation, window, frequency band, tail/direction, surrogate count, seed policy, exclusions, and failure rules frozen prospectively.
- [ ] Independent reviewer record and exact commit/artifact hashes recorded.

Until then:

- `replication_approval = NOT_APPROVED`
- `endpoint_computation_authorized = false`
- `claim_support = false`
- `promotion_authority = false`

## 7. Decision

**Do not calculate a HadUKP candidate endpoint yet.** Preserve the existing raw audit artifact and its hashes. Complete the bounded historical exposure audit, source-vintage interpretation, and shared-nuisance/independence review first. Keep all unresolved facts as `UNKNOWN` or `PENDING`; do not retroactively label any prior analysis preregistered.
