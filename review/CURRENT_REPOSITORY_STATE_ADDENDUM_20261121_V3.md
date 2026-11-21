# Current Repository State Addendum — 2026-11-21 V3

**Disposition:** `REVIEW_ONLY — SECURITY_GATE_OPEN — HUMAN_REVIEWS_PENDING — NO_NEW_SNAPSHOT — NO_WORKFLOW_RUN_AUTHORIZED — NO_PROMOTION_AUTHORITY`

**Observation time:** 2026-11-21, approximately 20:55 Africa/Cairo.

**Important identity rule:** This document records the exact GitHub state observed immediately before this documentation file is committed. Its recorded review-branch SHA is an observation point, not a claim about the branch HEAD after this file is committed.

## 1. Exact GitHub state at observation time

Repository: `AhmedPeaRL/maximal-one`

Default branch (`main`) HEAD:

`9749de9253f144eeda9e1b60cb219cfc5f201ecc`

Review branch (`review/type1-v4-remediation`) HEAD:

`cfe37ddbd6bfd049faef18729b5052e6d51ad73f`

Comparison (`main` → `review/type1-v4-remediation`):

- Status: `diverged`
- Review ahead: `716`
- Review behind: `36`
- Merge base: `a9808bd999a7ad902daf15606272529ca9af4580`

The review branch advanced by two commits after the previously recorded `650c57c6286acaa018a6dfc5ca81b2418399f6aa`. The latest observed commit is:

`cfe37ddbd6bfd049faef18729b5052e6d51ad73f`

Commit message:

`Record current repository state and HCM PDF candidate identities`

No merge, rebase, cherry-pick, or promotion is authorized.

## 2. Reconciliation of prior state reports

The following records are preserved as historical evidence and must not be silently overwritten:

- `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261121_V2.md` records review HEAD `650c57...` and 714 commits ahead. It is superseded for live branch identity by this V3 observation.
- `review/CONTAINER_IMAGE_SECURITY_TRIAGE_20261121_V4.md` records review HEAD `a6ec526...` and 707 commits ahead. It remains the historical security audit for its stated scan and evidence.
- `evidence/CURRENT_SCORECARD_RESIDUAL_REVIEW_REGISTER_20261121_V6.csv` also records the earlier `a6ec526...` branch identity. Preserve V6 as the register for that audit point.
- `protocol/INDEPENDENT_REVIEW_STATUS_AND_EVIDENCE_ADDENDUM_20261119.md` records an earlier moving review-branch identity. Its pinned scientific target remains a separate identity.
- `evidence/CURRENT_EVIDENCE_REGISTER.json` contains target commit `e41fb7392b58198e8a4d8fa28b470b12b6ad2c31` and main commit `fe0daded51229ed88d449c2eb68252455fd4ad7c`, with older run and artifact identities. Despite its filename, it is not the current live-state register for the November 21 review HEAD. Preserve it as historical evidence; do not use it to replace the current pinned scientific target.

The current pinned scientific target remains:

`ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`

A moving review-branch HEAD must not be substituted for this pinned target.

## 3. Changes since the exact container scan

Previously scanned code commit:

`aed3109b7a6ba28e956ef5d6db40efa06fb17dae`

GitHub comparison from that commit to the observed review HEAD reports 10 commits ahead. The changed paths are documentation and evidence-register files, including:

- `README.md`
- `docs/publications/README.md`
- `docs/publications/BINARY_IDENTITY_AND_PROVENANCE.md`
- `docs/publications/LOCAL_PDF_CANDIDATE_IDENTITY_MANIFEST_20261121_V1.csv`
- `evidence/CURRENT_SCORECARD_RESIDUAL_REVIEW_REGISTER_20261121_V6.csv`
- `review/CONTAINER_IMAGE_SECURITY_TRIAGE_20261121_V3.md`
- `review/CONTAINER_IMAGE_SECURITY_TRIAGE_20261121_V4.md`
- `review/CONTAINER_PACKAGE_NECESSITY_AUDIT_V1.md`
- `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261121_V1.md`
- `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261121_V2.md`

No `Dockerfile` or `.github/workflows` path appears in this comparison.

Therefore:

- The prior container scan remains relevant to the unchanged Dockerfile definition.
- It is not a scan of a newly built image at the current review HEAD.
- The recent documentation commits do not close any Trivy finding.
- No new scientific execution or snapshot is implied by these documentation commits.

## 4. Workflow governance and manual-run boundary

The repository owner attests that the following 12 workflows remain disabled in GitHub Actions settings:

1. Emergent Periodicity Analysis
2. External Verification
3. Reproducible Research Gate
4. SOS Robustness Gate
5. Build and Push Container — main name
6. Build and Publish Container — review-branch name
7. Cross Run Memory Verification
8. Immutable Release Lock
9. Evolution Engine
10. Canonical Sync
11. Cross Architecture Timing Test
12. Cross Architecture Timing

This is an owner attestation. It is not independent server-side verification of each workflow's enabled/disabled setting.

Some workflow YAML files remain in `.github/workflows`. On the review branch, Evolution Engine and Immutable Release Lock have been moved outside `.github/workflows` into `docs/disabled-workflows/`. The corresponding files under `docs/disabled-workflows/` are documentation/archive files, not active GitHub Actions workflow locations. The main branch still has its own workflow files.

`replication.yml` is not one of the 12 owner-listed disabled workflows. Do not dispatch it or change its `assurance_only` behavior.

### Future manual software-assurance candidate — not currently authorized

The only future candidate for a separately authorized software-assurance run is:

`.github/workflows/software-assurance-exact-commit-v1.yml`

Target branch:

`review/type1-v4-remediation`

The review-branch version includes:

- A review-branch-only guard.
- Exact full-SHA validation.
- `scan_commit` validation against the selected review-branch HEAD.
- Optional `run_container_review`, defaulting to `false`.
- Read-only software assurance and an OSV dependency inventory.
- No scientific claim or promotion authority.

The main-branch copy is older and has a stale default `scan_commit`; it does not include the review copy's `run_container_review` input.

The review-only child workflow:

`.github/workflows/container-cli-smoke-review.yml`

exists only on the review branch and is `workflow_call` only. It is not a direct manual Run workflow target. It is invoked by the parent workflow when the optional container-review input is enabled.

GitHub's documented same-repository reusable-workflow syntax supports `$/.github/workflows/{filename}`. The parent-to-child reference is therefore not itself a syntax defect.

**No workflow is authorized by this addendum.**

For a future run, GitHub's Actions UI requires the `workflow_dispatch` workflow to exist on the default branch. The existing parent is present on `main`, so a future, separately authorized run can select `review/type1-v4-remediation` in the branch dropdown and use the review-branch version. The child workflow must be called by the parent; it cannot be dispatched directly.

Do not add a new dispatcher to `main` merely for convenience. If the selected review branch does not expose the expected inputs, stop and inspect the UI rather than guessing.

## 5. Container security status

The previous exact-commit software-assurance and container-review run was:

- Workflow run: `44828421411`
- Scanned code commit: `aed3109b7a6ba28e956ef5d6db40efa06fb17dae`

The scan recorded:

- 47 HIGH finding records.
- 11 distinct CVEs.
- 6 Debian Trixie source-package families.
- 0 CRITICAL finding records.
- 87 OS packages inventoried.

The 47 finding records are not 47 distinct CVEs.

The zlib remediation was verified for the scanned image only. The remaining Trixie package families remain open pending verified Trixie security fixes or a separate evidence-based applicability assessment.

No package removal, unsupported false-positive classification, scanner suppression, Forky/Sid package mixing, or Dockerfile modification is authorized.

A zero exit code from actionlint, zizmor, Scorecard, or OSV is not a security certification and does not override the Trivy image result.

## 6. Scientific status and authority

The pinned scientific target remains:

`ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`

The current scientific disposition remains:

- `alpha_max=NOT_SET`
- V4 candidate: `REVISE_AND_RESUBMIT`
- Historical V1: `NOT_PASSED`
- `protocol_freeze=NOT_FROZEN`
- `formal_calibration_authorized=false`
- `confirmatory_execution_authorized=false`
- `claim_support=false`
- `promotion_authority=false`
- Approved independent secondary domains: `0/2`
- Independent replication: `0/2`
- Manual adjudication overlay records: `0`

No formal Type-I calibration, confirmatory execution, new scientific snapshot, claim support, or promotion is authorized.

The conceptual HCM publications do not establish empirical validity of the repository's computational hypothesis, consciousness, HCM causation, a causal mechanism, or universality.

## 7. Independent human-review status — checked 2026-11-21

Four independent review tracks remain pending.

### Politis — statistical methods and Type-I calibration

The November 15 review request and November 19 correction were found in Gmail. No attributable substantive review report was found in the current search.

The V4 acceptance rule remains unresolved. `alpha_max` remains `NOT_SET`. Historical V1 failures and its original two-sided Wilson rule must remain unchanged.

No calibration or confirmatory execution is authorized.

### Machiry — GitHub Actions and CI/CD security

The November 19 updated V9 snapshot and software-assurance review request were found. No attributable substantive review report was found in the current search.

The requested review remains limited to the pinned V9 target and its exact evidence. Later remediation-context scanner results must not be represented as an independent review of the pinned target.

### Seppälä — climate-domain review

The November 19 correction supersedes the earlier HadCET candidate framing.

The current candidate for independent assessment is HadUKP England and Wales monthly precipitation totals (EWP), January 1913 through December 2025, with 1,356 monthly rows.

Structural cadence and missingness checks are reported as passed. Independence, shared nuisance, source-vintage interpretation, prior endpoint exposure, and confirmatory-null adequacy remain unresolved.

A raw-source SHA-256 discrepancy remains open:

- Status addendum value: `75a10dcc597c4b0a452cdd8d22dcad6a0ef677bbe8f1a7d6065806123752882d`
- Raw-audit artifact value: `eb2a20081a4673211783b0fe442007921d0f23a4683065954373c6ce0fa96637`
- Parsed SHA-256 in both records: `3c757cd2f7258944ba393906ea3fd7294b48a09782319381f91d9117652b87df`

No HadUKP endpoint computation or confirmatory analysis is authorized. HadCET is not an approved independent replication domain.

### Wong — econometric review

The November 19 correction supersedes the earlier INDPRO candidate framing.

The current candidate for independent assessment is CPIAUCNS using a separately defined pre-gap window ending September 2025.

- Full audited window: January 1913 through December 2025.
- Full-window rows: 1,356.
- Missing observation: `2025-10-01`.
- Valid numeric observations in the full window: 1,355.
- Separate pre-gap window ending September 2025: 1,353 observations.

The missing October 2025 observation must not be imputed, interpolated, carried forward, or silently dropped. The pre-gap window is a separate candidate definition, not a repair of the full-window series.

Source-vintage, prior exposure, independence, shared nuisance, and confirmatory-null adequacy remain unresolved.

Wong's automatic out-of-office reply states that conference commitments may delay responses through November 29. No substantive review report was found in the current search.

No CPIAUCNS or INDPRO endpoint computation is authorized. Neither is approved as an independent replication domain.

No reviewer disposition is inferred from silence or an automatic reply.

## 8. HCM publication and PDF identity status

The review branch contains:

- `docs/publications/README.md`
- `docs/publications/HCM_ZENODO_PUBLICATIONS.csv`
- `docs/publications/BINARY_IDENTITY_AND_PROVENANCE.md`
- `docs/publications/LOCAL_PDF_CANDIDATE_IDENTITY_MANIFEST_20261121_V1.csv`
- Ten Markdown manuscript sources under `docs/concept/core-scientific/papers/`

The ten individually available local PDF candidates were inspected and hashed. Each candidate's byte size and MD5 match the corresponding values in the repository publication registry. Their SHA-256 values are recorded in the local identity manifest.

This establishes a local candidate-to-registry match. It does not, by itself, establish that each file was independently downloaded from its exact Zenodo record during this review.

### Paper 01 — partial direct record verification

The Zenodo version record page for `10.5281/zenodo.18148140` was accessible.

The page reports:

- Title: `Hybrid Consciousness Model (HCM): Presence Without Demand`
- Creator: Ahmed Salahuddin
- Published: January 4, 2026
- Version: v1
- Version DOI: `10.5281/zenodo.18148140`
- License: CC BY 4.0
- PDF filename: `HCM_Paper_01_Presence_Without_Demand.pdf`
- PDF size: 70.8 kB
- PDF MD5: `a240e99737d9d29c44c7f2fc161ca8b1`

The retained local candidate has size 70,764 bytes and the same MD5. This is a direct Zenodo-record metadata match to the retained candidate.

The direct PDF download could not be retrieved through the available browser path. The supplementary `README.pdf` is also listed on the record page with MD5 `adaa0b0a00581ec5eee46e55cc73f0ca`; its direct download was not retrieved.

The concept DOI `10.5281/zenodo.18148139` remains sourced from the repository registry and has not been independently confirmed through the inaccessible concept record page.

### Papers 02–10

The nine remaining version-record pages and direct PDF links could not be retrieved through the available browser path; the attempts returned cache/access errors. This is a retrieval limitation, not evidence that the records or files are absent.

Their local candidates match the repository registry's recorded sizes and MD5 values. Direct Zenodo record metadata and direct-download identity remain pending for these nine records.

### Paper 04 — title discrepancy remains open

The repository registry records:

`When Capability Does Not Become Action: Stabilized Potential and the Absence of Internal Gradient`

The retained PDF and corresponding Markdown manuscript identify the work as:

`The Silent Assumption of Action`

The local PDF content and Markdown source are closely aligned, but the Zenodo record page could not be retrieved to resolve the record-title discrepancy. Preserve the existing title values and the `TITLE_MISMATCH_REVIEW_REQUIRED` status. Do not rename, merge, or silently reassign the record.

### Papers 07 and 09

Both records use the title:

`When the System Does Not Answer: Observer Drift in Hybrid Conscious Architectures`

They have different version DOIs, concept DOIs, file sizes, and file hashes. They must remain separate publication records unless direct Zenodo metadata proves otherwise.

### Three newly supplied working PDFs

The newly supplied working PDFs for Papers 01, 08, and 10 differ from the retained registry-matching candidates:

- Paper 01 working copy: 70,356 bytes; MD5 `24a27ca6b33a0ada641c1f96ed50ab63`
- Paper 08 working copy: 340,399 bytes; MD5 `a69b11345fb4d83abe5bf3e58d9d10ff`
- Paper 10 working copy: 196,618 bytes; MD5 `62ef82c7c2efeea2dc10a20366dfadf5`

Preserve these as distinct working copies. Do not replace the retained candidate PDFs or label the working copies as published binaries.

The Markdown manuscript sources are editable research-source representations. Textual similarity, title agreement, or extracted-text coverage does not establish binary identity. The conceptual publications do not establish empirical validation of the computational hypothesis.

## 9. ZIP and Library evidence boundary

The supplied `maximal-one-main.zip` was inspected as a main-branch snapshot:

- 1,166 archive entries.
- SHA-256: `f59222d0eedd9073ea15ef51b1463c3926e7948fd0e8d417a536c78756634091`
- It corresponds to the observed main HEAD `9749de9253f144eeda9e1b60cb219cfc5f201ecc`.

This ZIP is not a snapshot of the moving review branch. The review branch was checked separately through GitHub.

The Library entry `HCM_Zenodo_10_Papers.zip` is present, with reported size 1,115,283 bytes. Its raw bytes could not be materialized through the available Library path. The ten individual PDF candidates were available separately and were inspected.

The retained candidate PDFs remain organized under:

`Hybrid Consciousness Model - HCM/Zenodo PDF Candidates - Registry MD5 Match/`

No historical archive or non-identical evidence file was deleted as part of this review.

## 10. Authorization boundary and next action

This addendum authorizes no:

- `main` branch modification
- Dockerfile modification
- workflow dispatch or re-enablement
- image publication
- scientific execution
- Type-I calibration
- confirmatory execution
- new scientific snapshot
- claim support
- promotion
- merge, rebase, or cherry-pick

The only next repository action is to add this V3 documentation file on:

`review/type1-v4-remediation`

After the documentation-only commit, do not run any `.yml` workflow.

The next review round must preserve the four pending independent-review tracks, the open container security findings, the current pinned scientific target, and the unresolved Zenodo metadata checks.

**Final disposition:** `REVIEW_ONLY — SECURITY_GATE_OPEN — HUMAN_REVIEWS_PENDING — NO_NEW_SNAPSHOT — NO_WORKFLOW_RUN_AUTHORIZED — NO_PROMOTION_AUTHORITY`
