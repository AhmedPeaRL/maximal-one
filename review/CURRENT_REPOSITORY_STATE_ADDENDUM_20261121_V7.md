# Current Repository State Addendum — 2026-11-21 V7

**Disposition:** `REVIEW_ONLY — RUN_36_REMAINS_LAST_SOFTWARE_ASSURANCE — POST_RUN_COMMITS_DOCUMENTATION_ONLY — OWNER_SUPPLIED_ZENODO_METADATA_CAPTURED — DIRECT_ZENODO_BINARY_VERIFICATION_PENDING — CONTAINER_SECURITY_GATE_OPEN — HUMAN_REVIEWS_PENDING — NO_WORKFLOW_AUTHORIZED`

## 1. Current repository identity

Repository: `AhmedPeaRL/maximal-one`

Observed `main` HEAD:

`9749de9253f144eeda9e1b60cb219cfc5f201ecc`

Observed `review/type1-v4-remediation` HEAD:

`77400bfcd18974a49711138d7061bc93ee9b0040`

The review branch remains divergent from main:

- Status: `diverged`
- Review branch ahead: `722`
- Review branch behind: `36`
- Merge base: `a9808bd999a7ad902daf15606272529ca9af4580`

The comparison returned the same main HEAD shown above. Both `main` and `review/type1-v4-remediation` are reported as protected branches.

No merge, rebase, cherry-pick, pull request, promotion, or change to `main` is authorized.

## 2. Documentation commits after Run 36

Run 36 targeted commit:

`99dd702ce4f7569e19b55503506b3bbfe8c920fa`

The current review branch is two commits ahead of that target. The comparison identifies exactly these two added files:

1. `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261121_V6.md`
2. `evidence/EXACT_ASSURANCE_RUN_44948856035_REVIEW.csv`

These are documentation/evidence-register additions. No workflow file, application code, Dockerfile, scientific protocol, or scientific dataset was changed by those two commits.

Current review-branch HEAD is therefore newer than the exact commit tested by Run 36. Run 36 remains valid evidence for `99dd702...`, not a scan of `77400bf...`.

## 3. Latest workflow-run state

Latest observed run remains:

- Workflow: `Exact Commit Software Assurance`
- Run: `44948856035` / #36
- Branch: `review/type1-v4-remediation`
- Run head and scan target: `99dd702ce4f7569e19b55503506b3bbfe8c920fa`
- Conclusion: `success`
- Exact-commit software assurance job: `success`
- OSV inventory job: `success`
- Container CLI build and image security job: `skipped`

The latest repository run listing returned Run 36 as the newest run. The V6 and CSV documentation commits occurred after Run 36; no later workflow run was observed.

Run 36's two artifacts remain:

- Software assurance artifact `14724383591`, SHA-256 `9802a450328b3174047062496c21e10af21a340256764215f013135c804390fd`
- OSV artifact `14725360055`, SHA-256 `1d3aaa89287d26325e2810b6ad6fc7567cc5a418b759f52cc31c7a883eb6a604`

Run 36 did not build or scan a container. The last measured V4 container result remains Run `44944152951`: 50 HIGH finding records, 12 distinct CVEs, 0 CRITICAL records. The container security gate remains open.

## 4. New owner-supplied Zenodo API metadata evidence

The user supplied API-shaped Zenodo record JSON for Papers 02–10 in `Pasted text(6).txt` on 2026-11-21. The capture/retrieval timestamp of the original API requests was not supplied. The extracted fields are preserved separately in:

`docs/publications/ZENODO_API_METADATA_CAPTURE_20261121_V1.csv`

- Rows: `9` (Papers 02–10)
- SHA-256: `0151169193095e2ec00c828c8439d31ae4160d22e9fe1deb09b7ed9a0b08503c`

For all nine supplied records, the payload states:

- `is_published=true`
- `is_draft=false`
- record access `public`
- file access `public`
- access status `open`
- embargo `active=false`
- deletion status `is_deleted=false`

The payload supplies the record IDs, version DOIs, parent concept DOIs, revision IDs, created/updated timestamps, PDF filenames, byte sizes, and MD5 checksums. Those supplied filenames, byte sizes, and MD5 values reconcile with the current repository publication registry and the local candidate archive inventory for Papers 02–10.

**Evidence classification:** `OWNER_SUPPLIED_API_JSON_REVIEWED_AND_INTERNALLY_RECONCILED`.

This is stronger than a DOI-only registry entry, but it is not independent retrieval from Zenodo. Direct API retrieval attempts through the available web surface returned `Cache miss`; that failure is not evidence that a record is absent or deleted. No published PDF binary for Papers 02–10 was directly downloaded and hashed in this review.

Do not upgrade any of Papers 02–10 to `VERIFIED_BINARY_MATCH`. Keep the distinction between:

1. user-supplied API metadata;
2. repository registry values;
3. local archive candidate PDF bytes;
4. uploaded working PDFs;
5. the actual published Zenodo PDF binary;
6. the corresponding Markdown source.

The current candidate archive MD5 agreement establishes local candidate-to-registry consistency, not direct Zenodo binary identity. The working PDFs for Papers 08 and 10 remain byte/MD5-distinct from the archive candidates despite normalized extracted-text equality. Paper 04's Markdown association remains unresolved because the source Markdown is titled `The Silent Assumption of Action`, while the Zenodo metadata title is `When Capability Does Not Become Action: Stabilized Potential and the Absence of Internal Gradient`. Papers 07 and 09 share a title but have distinct record IDs, version DOIs, concept DOIs, filenames, sizes, and MD5 values; preserve both records. Paper 08's metadata title and filename/PDF heading arrangement remain a separate title-association review item.

Paper 01 is not part of the newly supplied JSON capture and retains its earlier evidence status.

No existing publication registry value, DOI, title, file, or verification status is silently changed by this addendum.

## 5. Workflow authorization and branch-only workflow policy

**No GitHub Actions workflow is authorized to run after the next documentation-only commit.** This includes software assurance, container review, WDC-SILSO source audit, dependency refresh, replication, calibration, confirmatory, validation, or promotion workflows. Do not click `Run workflow` or dispatch through API/CLI.

The current `software-assurance-exact-commit-v1.yml` on the review branch exposes only `scan_commit` as a manual `workflow_dispatch` input. `run_container_review` remains a `workflow_call` input only. The container child remains reusable-only. This configuration does not authorize another run.

The review-branch WDC-SILSO workflow and `scripts/acquire_wdc_silso_source.py` were inspected read-only. The script downloads the official SILSO CSV and TXT snapshots, compares the official CSV against the existing `real-data/sunspots_full.csv`, writes source snapshots and a comparison report, and does not append official rows to the analysis file. The review-branch workflow adds checks for a complete official-prefix match, chronological/duplicate/gap checks, and `analysis_file_modified=false`; the report explicitly sets `replication_eligible=false`. This is a possible future provenance-only evidence task, not an authorization to run it now. The WDC-SILSO workflow versions on `main` and the review branch differ; do not treat one branch's workflow definition as the other's.

`replication.yml` remains unauthorized for dispatch or modification. It is not one of the 12 owner-listed disabled workflows.

### If a workflow exists only on the review branch

GitHub documents that `workflow_dispatch` events are received only when the workflow file exists on the repository's default branch. The Actions UI's `Run workflow` control therefore cannot be assumed to appear for a workflow that exists only on `review/type1-v4-remediation` and not on `main`.

Do not copy a review-only workflow into `main` merely to expose a Run workflow button. Do not use API/CLI dispatch as a workaround without checking GitHub's eligibility requirements and receiving explicit authorization for the exact workflow, branch, commit, and inputs. If a future review-only workflow genuinely needs execution, first design and review a legitimate caller/dispatcher path; do not change `main` or create a dispatch shim by assumption.

## 6. Disabled workflows and human reviews

The owner continues to attest that these 12 workflows are disabled:

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

Status remains `OWNER_ATTESTATION_NOT_INDEPENDENTLY_VERIFIED`. The available GitHub connector did not expose the server-side Actions workflow-state listing endpoint. Keep all 12 disabled; do not re-enable them.

The four substantive independent human reviews remain pending: Dimitris Politis, Anil Machiry, Annika Seppälä, and Benjamin Wong.

## 7. Scientific governance

Pinned scientific target:

`ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`

- `alpha_max=NOT_SET`
- `protocol_freeze=NOT_FROZEN`
- formal calibration: `false`
- confirmatory execution: `false`
- claim support: `false`
- promotion authority: `false`
- independent domains: `0/2`
- replication: `0/2`

No new scientific snapshot, calibration, confirmatory execution, endpoint computation, replication promotion, claim support, or scientific promotion is authorized. Conceptual papers and software/security checks do not establish consciousness, HCM causation, a universal mechanism, or empirical validation.

## 8. Next actions

1. Add this V7 addendum and the Zenodo metadata capture CSV as documentation-only files on `review/type1-v4-remediation`.
2. Do not edit `main`.
3. Do not run any workflow after this documentation-only commit.
4. Preserve the Run 35/36 artifacts and prior state records; do not delete historical Library evidence without a verified identity/duplication check.
5. Continue direct Zenodo API and published-PDF retrieval when the source is accessible; compare downloaded bytes, size, MD5, SHA-256, metadata, and Markdown relationship before changing publication status.
6. Continue the three Scorecard `contents: write` manual reviews and container package provenance review without dispatching the affected workflows.
7. Await the four attributable independent human review reports.

**Final status:** the repository's latest review-branch changes are documentation-only and remain isolated from `main`. Run 36 remains the last successful software-assurance run on its exact target commit. The supplied Zenodo JSON materially improves the metadata evidence for Papers 02–10 but does not close published-binary verification. No workflow or scientific authority is granted by this addendum.
