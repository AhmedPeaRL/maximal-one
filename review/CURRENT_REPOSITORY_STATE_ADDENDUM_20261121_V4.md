# Current Repository State Addendum — 2026-11-21 V4

**Disposition:** `REVIEW_ONLY — SECURITY_GATE_OPEN — WORKFLOW_STATE_VERIFICATION_PENDING — HUMAN_REVIEWS_PENDING — ZENODO_RECORD_VERIFICATION_INCOMPLETE — NO_NEW_SCIENTIFIC_SNAPSHOT`

## 1. Observation and exact repository identity

Repository: `AhmedPeaRL/maximal-one`

Default branch (`main`) HEAD:

`9749de9253f144eeda9e1b60cb219cfc5f201ecc`

Review branch (`review/type1-v4-remediation`) HEAD observed after V3:

`dac3c4a1f2fae2afcfe6634171a2a21fb4f8c476`

Latest review-branch commit:

`Record current repository and review status V3`

Commit URL:

`https://github.com/AhmedPeaRL/maximal-one/commit/dac3c4a1f2fae2afcfe6634171a2a21fb4f8c476`

The V3 commit is GitHub-verified as signed and adds only:

`review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261121_V3.md`

Current comparison (`main` → `review/type1-v4-remediation`):

- Status: `diverged`
- Review ahead: `717`
- Review behind: `36`
- Merge base: `a9808bd999a7ad902daf15606272529ca9af4580`

No merge, rebase, cherry-pick, or promotion is authorized.

## 2. Changes since the container scan

Previously scanned code commit:

`aed3109b7a6ba28e956ef5d6db40efa06fb17dae`

Comparison from that commit to the current review HEAD reports 11 commits ahead and no commits behind.

The changed paths are documentation and evidence records:

- `README.md`
- `docs/publications/BINARY_IDENTITY_AND_PROVENANCE.md`
- `docs/publications/LOCAL_PDF_CANDIDATE_IDENTITY_MANIFEST_20261121_V1.csv`
- `docs/publications/README.md`
- `evidence/CURRENT_SCORECARD_RESIDUAL_REVIEW_REGISTER_20261121_V6.csv`
- `review/CONTAINER_IMAGE_SECURITY_TRIAGE_20261121_V3.md`
- `review/CONTAINER_IMAGE_SECURITY_TRIAGE_20261121_V4.md`
- `review/CONTAINER_PACKAGE_NECESSITY_AUDIT_V1.md`
- `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261121_V1.md`
- `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261121_V2.md`
- `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261121_V3.md`

No `.github/workflows` path or `Dockerfile` path appears in this comparison.

The previous container scan remains relevant to the unchanged Dockerfile definition. It is not a newly built image scan at the current review HEAD. Documentation-only commits do not close Trivy findings.

## 3. Main-branch Actions history — independently inspected

A live GitHub Actions run-history query filtered to `branch=main` returned 2,500 historical runs, with the newest 100 returned for inspection.

The newest run in that result was:

- Workflow: `Reproducible Research Gate`
- Run ID: `44513785360`
- Created: `2026-11-19T11:19:30Z`
- Event: `schedule`
- Branch: `main`
- SHA: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- Conclusion: `success`

Other recent scheduled or push-triggered runs relevant to the owner-listed workflow set include:

| Workflow | Run ID | Created (UTC) | Event | Conclusion |
|---|---:|---|---|---|
| Emergent Periodicity Analysis | 44333793697 | 2026-11-18 15:16:52 | schedule | success |
| External Verification | 44275083285 | 2026-11-18 09:21:02 | schedule | success |
| Cross Architecture Timing Test | 43849590365 | 2026-11-16 10:31:16 | schedule | success |
| Build and Push Container | 43730704220 | 2026-11-15 15:35:10 | push | success |
| SOS Robustness Gate | 43730704181 | 2026-11-15 15:35:10 | push | failure |
| Cross Run Memory Verification | 43704387396 | 2026-11-15 10:30:21 | schedule | success |

Additional scheduled runs of `External Verification`, `Emergent Periodicity Analysis`, and `Reproducible Research Gate` occurred on November 17–18.

These records establish that the relevant workflows executed historically. They do not establish their current enabled/disabled state.

The owner reports that the 12 listed workflows are currently disabled. Current state remains `OWNER_ATTESTED — INDEPENDENT_STATE_CONFIRMATION_PENDING` because the connected GitHub read interface used in this review did not expose the repository Actions workflow-state listing endpoint.

The owner can independently provide the current state by opening:

`https://api.github.com/repos/AhmedPeaRL/maximal-one/actions/workflows?per_page=100`

For each relevant workflow, preserve the exact `name`, `path`, `id`, and `state` fields. A current `disabled_manually` state must not be used to rewrite or erase historical run records.

No claim is made that the workflows were disabled before their November 15–19 executions. The current owner attestation may describe a later disabling action.

## 4. Workflow inventory and authorization boundary

The owner-listed disabled workflow set remains:

1. Emergent Periodicity Analysis
2. External Verification
3. Reproducible Research Gate
4. SOS Robustness Gate
5. Build and Push Container — main-branch name
6. Build and Publish Container — review-branch name
7. Cross Run Memory Verification
8. Immutable Release Lock
9. Evolution Engine
10. Canonical Sync
11. Cross Architecture Timing Test
12. Cross Architecture Timing

Workflow YAML files remain present in the repository where applicable. Their presence does not prove that a workflow is enabled.

On the review branch, `evolution.yml` and `release-lock.yml` are archived under `docs/disabled-workflows/`; those archived files are not active workflow paths. The corresponding workflow files remain under `.github/workflows` on `main`.

`replication.yml` is not part of the 12 owner-listed workflows. It remains outside the authorization below and must not be dispatched.

### One narrowly scoped future software-assurance run

After this V4 addendum is committed, one software-only run may be manually dispatched, subject to the checks below:

Workflow:

`.github/workflows/software-assurance-exact-commit-v1.yml`

Target branch:

`review/type1-v4-remediation`

Required target:

The exact full 40-character SHA of the V4 documentation commit, which must equal the selected review-branch HEAD at dispatch time.

Input:

`run_container_review=false`

This parent workflow has a review-branch-only guard and exact-HEAD validation. Its software-only path runs actionlint, zizmor, Scorecard, and the OSV dependency inventory. Its permissions are read-only.

The OSV child workflow is `workflow_call` only and is not a direct manual-dispatch target.

The container child workflow is also `workflow_call` only. It builds a local image, runs a CLI smoke test, and scans with Trivy. It is not authorized by this addendum. The `run_container_review` input must remain `false`.

If the Actions UI does not show the expected review branch, exact SHA input, or `run_container_review=false`, stop and request review. Do not guess, enable a disabled workflow, or select `main`.

This software-only run does not authorize scientific execution, Type-I calibration, confirmatory execution, container publication, claim support, or promotion.

No other `.yml` workflow is authorized.

## 5. Container security status

The previous container run remains:

- Workflow run: `44828421411`
- Scanned commit: `aed3109b7a6ba28e956ef5d6db40efa06fb17dae`

Recorded findings:

- 47 HIGH finding records
- 11 distinct CVEs
- 6 Debian Trixie source-package families
- 0 CRITICAL finding records
- 87 OS packages inventoried

The zlib remediation was verified for that scanned image only. The remaining Trixie package families remain open pending verified Trixie security fixes or a separate evidence-based applicability assessment.

No Dockerfile modification, package removal, scanner suppression, unsupported false-positive classification, Forky/Sid package mixing, or image publication is authorized.

A zero exit code from an individual scanner is not a security certification and does not override the Trivy image findings.

## 6. Scientific status and authority

The pinned scientific target remains:

`ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`

The moving review HEAD must not replace the pinned scientific target.

Current disposition remains:

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

No new scientific snapshot, formal Type-I calibration, confirmatory execution, claim support, or promotion is authorized.

The conceptual HCM publications do not establish empirical validity of the computational hypothesis, HCM causation, consciousness, a causal mechanism, or universality.

## 7. Independent human-review status

Four independent review tracks remain pending:

- Politis — statistical methods and Type-I calibration
- Machiry — GitHub Actions and CI/CD security
- Seppälä — climate-domain review
- Wong — econometric review

No reviewer disposition may be inferred from silence or an automatic out-of-office reply.

The existing unresolved issues remain open, including the V4 acceptance rule, independent-domain eligibility, HadUKP raw-source SHA discrepancy, and the CPIAUCNS October 2025 missing observation.

No endpoint computation or confirmatory analysis for the pending secondary domains is authorized.

## 8. Zenodo archive received and inspected

The user-supplied archive:

`HCM_Zenodo_10_Papers(1).zip`

was opened and passed the ZIP integrity test.

- Archive size: `1,115,283` bytes
- Non-directory entries: `11`
- `testzip()`: no corrupt member reported
- Archive SHA-256: `b75f37026ee3cdc04ea79a671d166dfc7ac1b1227a7ee4a72a7f29a98b075562`
- Archive MD5: `81180bdde460c1171e622aa80863af48`

The archive contains ten PDFs and `README.pdf`.

### PDF candidate identities

| Paper | Size (bytes) | MD5 | SHA-256 |
|---|---:|---|---|
| 01 | 70764 | `a240e99737d9d29c44c7f2fc161ca8b1` | `0afdc65873debb2f50fc9a20864957ae8cc541e6d4926a8ae86d2cf340e75162` |
| 02 | 99264 | `045ce4aec6077eb238fdff0c4a1bc8f3` | `85528a4977effdd3a82b7e051b02992563e33a3fc830f27294a46890b301bb9e` |
| 03 | 101190 | `2772be59d4f02e4e64f6055ec69f4673` | `a7ca8c87cd9ebcf8640e4113f3fd7835ff351d8049cfa8b10c30b53843d14f7d` |
| 04 | 80328 | `e8c9ab7dc6c2ce315562c3948b47c506` | `2f6e63e837c49ea2943b199be927c7abfc7387b08183962551a42cca5fa6101a` |
| 05 | 172876 | `86f0cb907abe28f36070492a351fb0fd` | `b1f1964a410566befa7fe3a6601bb6706bee3776280a56c7f46bc273136bc905` |
| 06 | 233504 | `7a889f75d727165437e5e7797d372f83` | `9bb802f6c839ebb94364ca451b7a1c425131e34fd6741e3413fe83149cdc8406` |
| 07 | 117951 | `197714d5b6e5548fac66fb1b4e41fc8d` | `9b61ac0996cede283c9c4fdec0faed052e94a4177be0f2909e1609bda5ba0e73` |
| 08 | 353625 | `93821672f0ce53bd98f9060c1909da4c` | `07bf4d86d6e1e4f0a447f3c9f947d1128fcd271ccd7e171d709fe9b188b167eb` |
| 09 | 124010 | `73b9f42974b4a6190a4f97486ebe5cae` | `fc46df04cc95ddd8187acde93113a2ff132f9762a0b0aef4e4bbb558dc0e0ca1` |
| 10 | 208622 | `cb6cf6515cc37f4d83c9e13ae21a0cb5` | `63e541a3ab3872989745e622fefb33f99ac11c9032c36a924e551d003e20196e` |

All ten candidate PDFs match the byte sizes and MD5 values in the repository publication registry and local candidate identity manifest.

This establishes a candidate-to-registry match for the ZIP contents. It does not establish direct Zenodo download identity for records whose Zenodo pages could not be retrieved.

### README.pdf

- Size: `58677` bytes
- MD5: `adaa0b0a00581ec5eee46e55cc73f0ca`
- SHA-256: `e826ff0e3a64994470181f3ba4ef8fed604ee3d708a6f6158cecf3ba6e8e8d1e`

Paper 01's Zenodo record page lists this supplementary file and the same MD5.

## 9. Zenodo record identity status

The version DOI and concept DOI pairs below are reproduced from the repository registry. Only Paper 01's version-record page was directly accessible in this review.

| Paper | Version DOI | Concept DOI | Direct record verification |
|---|---|---|---|
| 01 | `10.5281/zenodo.18148140` | `10.5281/zenodo.18148139` | Version record and PDF MD5 verified; concept DOI still registry-sourced |
| 02 | `10.5281/zenodo.18168287` | `10.5281/zenodo.18168286` | Pending |
| 03 | `10.5281/zenodo.18168932` | `10.5281/zenodo.18168931` | Pending |
| 04 | `10.5281/zenodo.18169421` | `10.5281/zenodo.18169420` | Pending; title mismatch open |
| 05 | `10.5281/zenodo.18177283` | `10.5281/zenodo.18177282` | Pending |
| 06 | `10.5281/zenodo.18181050` | `10.5281/zenodo.18181049` | Pending |
| 07 | `10.5281/zenodo.18182089` | `10.5281/zenodo.18182088` | Pending; same title as Paper 09 |
| 08 | `10.5281/zenodo.18190317` | `10.5281/zenodo.18190316` | Pending; title and filename presentation require confirmation |
| 09 | `10.5281/zenodo.18193434` | `10.5281/zenodo.18193433` | Pending; same title as Paper 07 |
| 10 | `10.5281/zenodo.18214787` | `10.5281/zenodo.18214786` | Pending |

Paper 01's accessible Zenodo page reports:

- Title: `Hybrid Consciousness Model (HCM): Presence Without Demand`
- Creator: Ahmed Salahuddin
- Published: January 4, 2026
- Version: v1
- Version DOI: `10.5281/zenodo.18148140`
- License: CC BY 4.0
- PDF filename: `HCM_Paper_01_Presence_Without_Demand.pdf`
- PDF size: 70.8 kB
- PDF MD5: `a240e99737d9d29c44c7f2fc161ca8b1`

The local ZIP candidate matches this MD5 and byte size.

The concept DOI `10.5281/zenodo.18148139` remains registry-sourced and was not independently confirmed through its concept record page.

### Unresolved title and association issues

Paper 04:

- Registry title: `When Capability Does Not Become Action: Stabilized Potential and the Absence of Internal Gradient`
- PDF title: `The Silent Assumption of Action`
- Markdown source: `docs/concept/core-scientific/papers/HCM_Paper_04_The_Silent_Assumption_of_Action.md`

Keep `TITLE_MISMATCH_REVIEW_REQUIRED`. Do not rename, merge, or silently reassign the record.

Paper 08:

- Registry title: `When Measurement Approaches the Threshold: Formalism Without Control in Hybrid Conscious Architectures`
- PDF title: `Formalism Without Control in Hybrid Conscious Architectures`
- PDF subtitle: `When Measurement Becomes Pressure: Limits of Quantification in Hybrid Conscious Fields`
- Filename: `HCM_Paper_08_When_Measurement_Approaches_the_Thresholdes.pdf`

The exact Zenodo record title and file metadata remain unverified.

Papers 07 and 09 share the displayed title `When the System Does Not Answer: Observer Drift in Hybrid Conscious Architectures`, but have distinct version DOIs, concept DOIs, sizes, and MD5 values. Keep them as separate records.

### Registry-status inconsistency

The current `HCM_ZENODO_PUBLICATIONS.csv` marks Papers 01, 08, and 10 as `MD5_MISMATCH_LOCAL_PDF`.

The current local candidate manifest marks all ten candidate PDFs as `repository_registry_md5_match=YES`.

The newly received ZIP confirms that its Paper 01, Paper 08, and Paper 10 candidates match the registry MD5 values. Separate working copies for those three papers have different MD5 values.

This discrepancy requires a controlled registry clarification. Do not silently overwrite the CSV or manifest until direct Zenodo record metadata has been collected.

The manifest's `zenodo_direct_verification=NO` remains the conservative status for all ten until the direct record-level verification is completed and updated.

## 10. Separate working copies — preserve without substitution

Three separately supplied working PDFs were inspected.

| Paper | Working-copy size | Working-copy MD5 | Extracted text compared with ZIP candidate |
|---|---:|---|---|
| 01 | 70356 | `24a27ca6b33a0ada641c1f96ed50ab63` | Exact extracted-text match; 7 pages |
| 08 | 340399 | `a69b11345fb4d83abe5bf3e58d9d10ff` | Exact extracted-text match; 33 pages |
| 10 | 196618 | `62ef82c7c2efeea2dc10a20366dfadf5` | Exact extracted-text match; 16 pages |

The extracted text and page counts match the corresponding ZIP candidates, while the binary hashes differ.

Preserve the working copies as distinct files. Do not replace the registry-matching candidates or label the working copies as the published Zenodo binaries.

## 11. Library evidence and mutation limitation

The ten candidate PDFs remain in:

`Hybrid Consciousness Model - HCM/Zenodo PDF Candidates - Registry MD5 Match/`

The newly uploaded ZIP is visible in the Project Library collection.

A move into a newly created archive folder was attempted, but the Library tool returned:

`project_library_mutation_unsupported`

The empty folder was removed afterward. No file was deleted, replaced, or moved during this attempt.

An older `HCM_Zenodo_10_Papers.zip` entry remains in the Library. Its raw bytes could not be materialized for an exact hash comparison with the newly inspected ZIP. Do not delete either archive until byte identity is established.

## 12. Required next actions

1. Commit this V4 addendum only to `review/type1-v4-remediation`.
2. Do not modify `main`.
3. After the V4 commit, the only authorized manual workflow candidate is `software-assurance-exact-commit-v1.yml` on `review/type1-v4-remediation`, with the exact V4 commit SHA and `run_container_review=false`.
4. Do not dispatch the container child workflow, `replication.yml`, any of the 12 owner-listed workflows, or any scientific workflow.
5. Obtain the current GitHub Actions workflow-state JSON and preserve the `name`, `path`, `id`, and `state` fields.
6. Obtain direct Zenodo metadata for Papers 02–10, including version DOI, concept DOI, title, creators, version/date, filename, byte size, and MD5.
7. Resolve Paper 04's title discrepancy and Paper 08's title/filename discrepancy before changing the publication registry.
8. Keep all four independent human-review tracks pending until substantive attributable reports are received.
9. Keep container security findings open until fixed by verified Debian Trixie packages or a separate evidence-based applicability assessment.
10. Do not create a new scientific snapshot, freeze the protocol, authorize calibration, run confirmatory analysis, or promote a claim.

**Final disposition:** `REVIEW_ONLY — SECURITY_GATE_OPEN — WORKFLOW_STATE_VERIFICATION_PENDING — HUMAN_REVIEWS_PENDING — ZENODO_RECORD_VERIFICATION_INCOMPLETE — NO_NEW_SCIENTIFIC_SNAPSHOT`
