# Current Repository State Addendum — 2026-11-21 V2

**Disposition:** REVIEW_ONLY — SECURITY_GATE_OPEN — HUMAN_REVIEWS_PENDING — NO_NEW_SNAPSHOT — NO_WORKFLOW_RUN_AUTHORIZED — NO_PROMOTION_AUTHORITY

## 1. Exact live GitHub identities

Repository: `AhmedPeaRL/maximal-one`

Default branch (`main`) HEAD:
`9749de9253f144eeda9e1b60cb219cfc5f201ecc`

Review branch (`review/type1-v4-remediation`) HEAD:
`650c57c6286acaa018a6dfc5ca81b2418399f6aa`

Comparison:
- Status: `diverged`
- Review ahead of main: `714`
- Review behind main: `36`
- Merge base: `a9808bd999a7ad902daf15606272529ca9af4580`

No merge, rebase, cherry-pick, or promotion is authorized.

## 2. Changes since the exact container scan target

Previously scanned commit:
`aed3109b7a6ba28e956ef5d6db40efa06fb17dae`

The comparison from that commit to the current review HEAD contains eight documentation-only commits.

Changed paths include:

- `README.md`
- `docs/publications/README.md`
- `docs/publications/BINARY_IDENTITY_AND_PROVENANCE.md`
- `evidence/CURRENT_SCORECARD_RESIDUAL_REVIEW_REGISTER_20261121_V6.csv`
- `review/CONTAINER_IMAGE_SECURITY_TRIAGE_20261121_V3.md`
- `review/CONTAINER_IMAGE_SECURITY_TRIAGE_20261121_V4.md`
- `review/CONTAINER_PACKAGE_NECESSITY_AUDIT_V1.md`
- `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261121_V1.md`

No Dockerfile or workflow file changed in this interval.

The previous container scan therefore remains relevant to the unchanged Dockerfile definition. It is not a scan of a newly built image.

## 3. Recent documentation commits

`2367649e825ea4f15038273814d21a559547acd8`

Added:
`review/CONTAINER_PACKAGE_NECESSITY_AUDIT_V1.md`

This is an analysis-only procedure. It does not authorize package removal, Dockerfile changes, workflow execution, image publication, or scientific execution.

`650c57c6286acaa018a6dfc5ca81b2418399f6aa`

Updated:
`README.md`

Added links to the HCM publication index, registry, and binary identity policy.

The publication index and provenance policy are present on the review branch. They are not present on `main`.

## 4. Workflow governance

The repository owner attests that these 12 workflows remain disabled:

1. Emergent Periodicity Analysis
2. External Verification
3. Reproducible Research Gate
4. SOS Robustness Gate
5. Build and Push Container — main name
6. Build and Publish Container — review name
7. Cross Run Memory Verification
8. Immutable Release Lock
9. Evolution Engine
10. Canonical Sync
11. Cross Architecture Timing Test
12. Cross Architecture Timing

This is an owner attestation, not independent server-side verification of each workflow's enabled/disabled setting.

`replication.yml` is not among these 12 workflows. On the review branch it is a Python dependency-refresh workflow, not the main-branch Cross-Architecture Replication workflow. Do not dispatch it.

No workflow is authorized by this addendum.

## 5. Future workflow boundary

The only future candidate for a specifically authorized software-assurance or container-review run is:

`.github/workflows/software-assurance-exact-commit-v1.yml`

Target branch:
`review/type1-v4-remediation`

Any future dispatch must use the exact full HEAD SHA of that branch.

The optional `run_container_review` input must remain false unless an actual Trixie security fix and a reviewed Dockerfile change justify a new container build and Trivy scan.

This is a future candidate only, not current authorization.

## 6. Container security status

The previous scan reported:

- 47 HIGH finding records
- 11 distinct CVEs
- 6 Debian source-package families
- 0 CRITICAL records

The 47 finding records must not be represented as 47 distinct CVEs.

The zlib remediation applies only to the scanned image. The six remaining Trixie package families remain open pending verified Trixie fixes or a separate evidence-based applicability assessment.

No package removal, non-Trixie package mixing, scanner suppression, or unsupported false-positive classification is authorized.

## 7. Scientific status

The pinned scientific target remains:

`ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`

Current status remains:

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

No newer scientific snapshot is authorized.

## 8. Independent human reviews

Four review tracks remain pending:

- Politis — statistical methods and Type-I calibration
- Machiry — GitHub Actions and CI/CD security
- Seppälä — climate-domain independence
- Wong — econometric-domain review

The current Gmail search found no substantive review report from these reviewers. Wong's out-of-office message reports possible response delays through November 29.

No reviewer disposition is inferred from silence or an automatic reply.

## 9. HCM publications and binary identity

Ten repository manuscript sources are present under:

`docs/concept/core-scientific/papers/`

All ten manuscript files in the review branch match the corresponding Markdown files in the supplied main-branch ZIP by Git blob identity.

Ten local PDF candidates have been retained in the Library under:

`Hybrid Consciousness Model - HCM/Zenodo PDF Candidates - Registry MD5 Match/`

Their sizes and MD5 values match the repository publication registry. SHA-256 values are recorded separately in:

`docs/publications/LOCAL_PDF_CANDIDATE_IDENTITY_MANIFEST_20261121_V1.csv`

This is a repository-registry match, not independent live verification against Zenodo.

Paper 04 remains `TITLE_MISMATCH_REVIEW_REQUIRED`.

Papers 07 and 09 retain separate DOI identities despite sharing a title.

The three newly supplied working PDFs for Papers 01, 08, and 10 differ from the corresponding registry-matching PDF candidates. They must not replace the candidate files as published binaries.

## 10. Library cleanup

Ten byte-for-byte duplicate PDF copies were moved to trash after exact hash comparison. One retained copy of each paper was moved into the dedicated candidate folder.

No historical ZIP archive or non-identical evidence file was deleted.

Uploads of the newer working copies for Papers 08 and 10 were rate-limited and remain pending.

## 11. Authorization boundary

This addendum authorizes no:

- `main` branch modification
- Dockerfile modification
- workflow dispatch
- workflow re-enablement
- image publication
- scientific execution
- Type-I calibration
- confirmatory execution
- snapshot creation
- merge or promotion

All future actions require separate evidence review and explicit authorization.
