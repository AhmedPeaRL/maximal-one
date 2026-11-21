# Current Repository State Addendum — 2026-11-21 V6

**Disposition:** `REVIEW_ONLY — MANUAL_CONTAINER_INPUT_GUARD_VERIFIED — SOFTWARE_ASSURANCE_RUN_36_SUCCESS — CONTAINER_JOB_SKIPPED — CONTAINER_SECURITY_GATE_OPEN — HUMAN_REVIEWS_PENDING — ZENODO_RECORDS_02_10_DIRECT_VERIFICATION_PENDING — NO_NEW_SCIENTIFIC_SNAPSHOT`

## 1. Repository identity and branch isolation

Repository: `AhmedPeaRL/maximal-one`

Main commit observed in the GitHub comparison:

`9749de9253f144eeda9e1b60cb219cfc5f201ecc`

Review branch: `review/type1-v4-remediation`

Latest assurance run observed on the review branch:

`99dd702ce4f7569e19b55503506b3bbfe8c920fa`

GitHub comparison `main` → `review/type1-v4-remediation`:

- Status: `diverged`
- Review ahead: `720`
- Review behind: `36`
- Merge base: `a9808bd999a7ad902daf15606272529ca9af4580`
- Base/main commit returned by comparison: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`

No merge, rebase, cherry-pick, pull request, or promotion is authorized. No change to `main` is authorized.

The user reports no recent manual changes or workflow runs on `main`. The current comparison is consistent with the previously observed main commit; this is not a claim that every repository setting or deployment surface has been independently inspected.

## 2. Guard commit and exact workflow change

Commit:

`99dd702ce4f7569e19b55503506b3bbfe8c920fa`

Message: `Record V4 assurance deviation and guard manual dispatch`

The commit changes only:

`.github/workflows/software-assurance-exact-commit-v1.yml`

Exact change: it removes the `run_container_review` input from `workflow_dispatch.inputs` while retaining that input under `workflow_call.inputs`.

The current file therefore exposes only `scan_commit` as a manual dispatch input. The reusable-workflow interface still supports `run_container_review`, so callers retain that parameter, defaulting to false where omitted.

The child workflow `container-cli-smoke-review.yml` was not changed. `replication.yml` was not changed. The Dockerfile was not changed.

## 3. Exact Commit Software Assurance run 36

Workflow: `Exact Commit Software Assurance`

Run ID: `44948856035`

Run number: `36`

Event: `workflow_dispatch`

Branch: `review/type1-v4-remediation`

Run head SHA: `99dd702ce4f7569e19b55503506b3bbfe8c920fa`

Target `scan_commit` recorded in the job log and assurance manifest:

`99dd702ce4f7569e19b55503506b3bbfe8c920fa`

Workflow definition commit recorded in the manifest:

`99dd702ce4f7569e19b55503506b3bbfe8c920fa`

Workflow ref: `refs/heads/review/type1-v4-remediation`

Run conclusion: `success`

Jobs:

- `Scan exact commit without promotion authority` — job `136982108490`: `success`
- `OSV inventory for the exact target commit / osv-inventory` — job `136982108655`: `success`
- `Container CLI build and image security (review only)` — job `136982200029`: `skipped`

The container child did not run. No Trivy image scan, container build, or scientific analysis occurred in run 36.

## 4. Software-assurance findings

### actionlint

- Version: `1.7.12`
- Exit code: `0`
- Diagnostic output: empty

The command contains three explicit ignore patterns for same-repository reusable-workflow references using GitHub's `$/.github/workflows/...` syntax. GitHub's current workflow syntax documentation explicitly supports `$/.github/workflows/{filename}` for a reusable workflow in the same repository. The ignores are retained as a linter-compatibility exception and must not be misrepresented as a general suppression of unrelated diagnostics.

### zizmor

- Version: `1.30.1`
- Mode: `--offline`
- Exit code: `0`
- JSON findings: `[]`

The tool logged completion for the repository workflow files. Offline mode is a scope limitation; this is not a complete external threat assessment.

### OpenSSF Scorecard

- Version: `5.6.0`
- Exit code: `0`
- Overall score: `9.2/10`

Checks include:

- Fuzzing: `0/10` — no fuzzer integration detected.
- License: `9/10` — `LICENSE` detected, but Scorecard did not recognize an FSF/OSI license identifier.
- Token-Permissions: `10/10`, with warnings that `contents: write` is present at:
  - `.github/workflows/canonical-sync.yml:51`
  - `.github/workflows/cross-run-memory-verification.yml:57`
  - `.github/workflows/replication.yml:232`
- Vulnerabilities: `10/10` in Scorecard's own repository/check scope.

The Scorecard JSON reports the local worktree URI and `repo.commit=unknown`. Exact target identity is independently bound by the workflow checkout check and assurance manifest; Scorecard's own JSON is not independent commit-identity evidence.

The three `contents: write` warnings remain a manual review item even though the numeric check score is 10. The inspected workflow context shows:

- `canonical-sync.yml`: manual dispatch; its write job is restricted to `review/type1-v4-remediation` and updates only the review-branch protocol lock.
- `cross-run-memory-verification.yml`: manual and weekly schedule; its write job is restricted to `review/type1-v4-remediation` and appends the computed hash to review-branch history.
- `replication.yml`: manual dispatch with `assurance_only` defaulting to true; the `publish` job with `contents: write` is conditional on `!inputs.assurance_only`. This workflow is not one of the 12 owner-listed disabled workflows and remains unauthorized for dispatch or modification.

These controls reduce apparent reachability but do not replace a full trigger, caller, effective-permission, and server-side workflow-state review. No permission change is authorized in this addendum.

### OSV-Scanner

- Version: `2.7.1` (osv-scalibr `0.5.3`)
- Exit code: `0`
- JSON validity: `true`
- Results: `[]`
- Six supported manifest/lock files scanned: five Python requirements files with 48 package entries each, and `package-lock.json` with zero packages.

This is a source-manifest/lockfile inventory only. It does not scan Debian OS packages in a container image and must not be described as a clean image scan or a security certification.

### Assurance manifest

The run manifest binds the exact scan commit and run ID and retains:

- `protocol_freeze=NOT_FROZEN`
- `formal_calibration_authorized=false`
- `confirmatory_execution_authorized=false`
- `claim_support=false`
- `promotion_authority=false`
- `authority=NONE`

All scanner exit codes being zero means the required manual finding review remains necessary. It does not certify the repository as secure.

## 5. Run 36 artifact identities

### Exact-commit software assurance

- Artifact ID: `14724383591`
- Name: `exact-commit-software-assurance-44948856035`
- Size: `5,906` bytes
- SHA-256: `9802a450328b3174047062496c21e10af21a340256764215f013135c804390fd`
- Retention expiry reported by GitHub: `2027-02-19T20:55:57Z`

### OSV dependency inventory

- Artifact ID: `14725360055`
- Name: `osv-dependency-inventory-44948856035`
- Size: `1,271` bytes
- SHA-256: `1d3aaa89287d26325e2810b6ad6fc7567cc5a418b759f52cc31c7a883eb6a604`
- Retention expiry reported by GitHub: `2027-02-19T20:55:57Z`

Both artifacts were downloaded, ZIP-tested, and inspected. Their local SHA-256 values match GitHub's artifact digests.

## 6. Container security remains open

Run 36 skipped the container child and did not create a new image or Trivy report.

The last completed container scan remains run `44944152951` (V4): 50 HIGH finding records, 12 distinct CVEs, and 0 CRITICAL finding records across the Debian 13.7 image inventory. These are the last measured findings, not a new run-36 measurement. The image security gate remains open.

No vulnerability suppression, package removal, Dockerfile edit, Debian suite mixing, container workflow dispatch, or replacement image is authorized. Continue the package provenance/necessity/reverse-dependency/runtime-use audit before any Dockerfile remediation.

## 7. Workflow disabled-state evidence

The repository owner reports that these 12 workflows remain disabled in the live repository:

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

Status classification: `OWNER_ATTESTATION_NOT_INDEPENDENTLY_VERIFIED`.

The available GitHub connector did not expose the repository Actions workflow-state listing endpoint, so this addendum does not claim independent server-side verification. The source YAML files may remain in the repository while the corresponding Actions workflows are disabled in repository settings.

`replication.yml` is not one of the 12 and remains unauthorized for dispatch or modification. Do not re-enable any listed workflow.

## 8. Independent human reviews

A fresh Gmail search for inbound messages from the four reviewer addresses over the last 30 days returned no messages. The latest known correction/follow-up emails remain the ones sent on 2026-11-19.

Reviewers:

- Dimitris Politis
- Anil Machiry
- Annika Seppälä
- Benjamin Wong

All four substantive independent review reports remain pending. The known Wong out-of-office response covered 2026-11-15 through 2026-11-29. Automated scanners do not substitute for the requested independent reviews.

## 9. Main archive and HCM publication archive

### Main archive

`maximal-one-main.zip`

- SHA-256: `f59222d0eedd9073ea15ef51b1463c3926e7948fd0e8d417a536c78756634091`
- ZIP comment: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- Entries: `1,166` total, comprising `1,051` files and `115` directory entries
- Uncompressed file bytes: `3,939,438`
- ZIP integrity test: passed

The archive comment matches the main commit returned by the GitHub comparison. This is a main-branch archive, not a review-branch snapshot.

### Ten-paper HCM archive

`HCM_Zenodo_10_Papers(1).zip`

- Size: `1,115,283` bytes
- SHA-256: `b75f37026ee3cdc04ea79a671d166dfc7ac1b1227a7ee4a72a7f29a98b075562`
- Contents: ten candidate PDFs plus `README.pdf`
- ZIP integrity test: passed

The ten candidate PDFs' local MD5 values match the repository publication registry. This establishes candidate-to-registry consistency only; it does not establish that the candidate bytes are the bytes currently downloadable from Zenodo.

## 10. Publication registry and Markdown-source mapping

The review-branch registry is:

`docs/publications/HCM_ZENODO_PUBLICATIONS.csv`

The provenance policy is:

`docs/publications/BINARY_IDENTITY_AND_PROVENANCE.md`

The policy correctly separates Zenodo record metadata, version PDF, concept DOI, Markdown source, working PDF, and extracted text. No status may be upgraded from title or text similarity alone.

The repository Markdown source paths for all ten papers resolve on `review/type1-v4-remediation`. Blob identities:

- Paper 01: `docs/concept/core-scientific/papers/HCM_Paper_01_Presence_Without_Demand.md` — `b989be7dcb039196796095a7b7a3598660c87332`
- Paper 02: `docs/concept/core-scientific/papers/HCM_Paper_02_Autonomy_Without_Demand.md` — `fbcb182eb30194bdb17db5681f0be9c40b7bea66`
- Paper 03: `docs/concept/core-scientific/papers/HCM_Paper_03_When_Capability_Does_Not_Become_Action.md` — `d8773bc365618fc94873f52334b48a69f3cc1c84`
- Paper 04: `docs/concept/core-scientific/papers/HCM_Paper_04_The_Silent_Assumption_of_Action.md` — `511b8c699f0a4c088af4b328361addd292d46691`
- Paper 05: `docs/concept/core-scientific/papers/HCM_Paper_05_The_Field_That_Does_Not_Ask_to_Operate.md` — `d13ddb7fa31d4aa4350709ff0576a05bf1cee3a5`
- Paper 06: `docs/concept/core-scientific/papers/HCM_Paper_06_Systems_That_Survive_Being_Left_Alone.md` — `55a22454ed732878ff6d0f8e2cd39d11ee7c8158`
- Paper 07: `docs/concept/core-scientific/papers/HCM_Paper_07_When_the_System_Does_Not_Answer.md` — `fedf99d44f621baa8e2aec8cb045f0e8fbd32ff7`
- Paper 08: `docs/concept/core-scientific/papers/HCM_Paper_08_Formalism_Without_Control_in_Hybrid_Conscious_Architectures.md` — `cd9a2341146a6bf0db25d6f5ee3daf504db4017a`
- Paper 09: `docs/concept/core-scientific/papers/HCM_Paper_09_When_the_System_Does_Not_Answer.md` — `b72126002795e421ccb950dcb0d97cffe4122599`
- Paper 10: `docs/concept/core-scientific/papers/HCM_Paper_10_Application_Without_Extraction.md` — `f99029a9f3f5a21d78baa74caa45f9a38b8dc734`

The repository Markdown files are editable manuscript/source representations. They are not byte-identical to the published PDF files; the Markdown sources also carry explicit conceptual/non-empirical status notes. A source-path or title association is not proof that the published PDF was generated from that exact Markdown revision.

### Version DOI / concept DOI pairs from the repository registry

| Paper | Version DOI | Concept DOI | Registry title |
|---|---|---|---|
| 01 | `10.5281/zenodo.18148140` | `10.5281/zenodo.18148139` | Hybrid Consciousness Model (HCM): Presence Without Demand |
| 02 | `10.5281/zenodo.18168287` | `10.5281/zenodo.18168286` | Autonomy Without Demand: Observations from a Permission-Based System Architecture |
| 03 | `10.5281/zenodo.18168932` | `10.5281/zenodo.18168931` | When Capability Does Not Become Action: On Silent Presence in Technically Complete Systems |
| 04 | `10.5281/zenodo.18169421` | `10.5281/zenodo.18169420` | When Capability Does Not Become Action: Stabilized Potential and the Absence of Internal Gradient |
| 05 | `10.5281/zenodo.18177283` | `10.5281/zenodo.18177282` | The Field That Does Not Ask to Operate: Pre-Operational Coherence as a Structural Property of Hybrid Conscious Systems |
| 06 | `10.5281/zenodo.18181050` | `10.5281/zenodo.18181049` | Systems That Survive Being Left Alone: Structural Longevity Through Non-Dependence in Hybrid Conscious Architectures |
| 07 | `10.5281/zenodo.18182089` | `10.5281/zenodo.18182088` | When the System Does Not Answer: Observer Drift in Hybrid Conscious Architectures |
| 08 | `10.5281/zenodo.18190317` | `10.5281/zenodo.18190316` | When Measurement Approaches the Threshold: Formalism Without Control in Hybrid Conscious Architectures |
| 09 | `10.5281/zenodo.18193434` | `10.5281/zenodo.18193433` | When the System Does Not Answer: Observer Drift in Hybrid Conscious Architectures |
| 10 | `10.5281/zenodo.18214787` | `10.5281/zenodo.18214786` | Application Without Extraction: Reframing Application as Presence Within the Hybrid Consciousness Model |

These DOI pairs and titles above are registry-derived, not newly verified Zenodo metadata for records 02–10.

### Direct Zenodo access limitation

The nine supplied record API endpoints for records `18168287`, `18168932`, `18169421`, `18177283`, `18181050`, `18182089`, `18190317`, `18193434`, and `18214787` returned `Cache miss` to the available web retrieval surface. The corresponding landing pages were also inaccessible through that surface. A cache miss or access failure is not evidence that a record is absent or deleted.

Record 01 (`18148140`) had its metadata reviewed in the earlier audit; its recorded filename, byte size, and MD5 matched the local candidate archive entry. The concept DOI was registry-sourced. The direct Zenodo download of the published binary was not established in this review.

Records 02–10 remain `RECORD_METADATA_UNVERIFIED / PUBLISHED_BINARY_DIRECT_DOWNLOAD_PENDING` until their public record JSON and file downloads are retrieved successfully.

### Working PDFs for Papers 01, 08, and 10

The three uploaded working PDFs were opened and checked as PDFs. Their normalized extracted text is exactly equal to the corresponding candidate PDFs inside the ten-paper archive, but their bytes and MD5 values differ:

| Paper | Candidate archive bytes / MD5 | Working PDF bytes / MD5 | Extracted text |
|---|---|---|---|
| 01 | `70,764` / `a240e99737d9d29c44c7f2fc161ca8b1` | `70,356` / `24a27ca6b33a0ada641c1f96ed50ab63` | normalized text equal |
| 08 | `353,625` / `93821672f0ce53bd98f9060c1909da4c` | `340,399` / `a69b11345fb4d83abe5bf3e58d9d10ff` | normalized text equal |
| 10 | `208,622` / `cb6cf6515cc37f4d83c9e13ae21a0cb5` | `196,618` / `62ef82c7c2efeea2dc10a20366dfadf5` | normalized text equal |

The working PDFs are not byte-identical to the candidate PDFs and neither set is treated as directly downloaded Zenodo binaries.

### Publication-specific unresolved items

- Paper 04: registry title differs from the PDF/Markdown title (`The Silent Assumption of Action`); `TITLE_MISMATCH_REVIEW_REQUIRED`.
- Paper 08: registry title differs from the PDF heading/subtitle arrangement; the PDF heading is `Formalism Without Control in Hybrid Conscious Architectures`, with a former working subtitle about measurement becoming pressure.
- Papers 07 and 09 share the same registry title but have distinct version DOIs, concept DOIs, file sizes, and MD5 values. They remain distinct records and must not be merged.
- Papers 01, 08, and 10 working PDFs differ in binary identity from the local candidate archive PDFs despite equal normalized extracted text.

No DOI, title, file, registry hash, or manuscript association is silently changed.

## 11. Project Library update

The following run artifacts were successfully added to:

`/Hybrid Consciousness Model - HCM/Current Evidence/`

Run 36:

- `exact-commit-software-assurance-44948856035.zip`
- `osv-dependency-inventory-44948856035.zip`

Run 35 / V4 container review:

- `exact-commit-software-assurance-44944152951.zip`
- `osv-dependency-inventory-44944152951.zip`
- `trivy-image-report-44944152951.zip`

The V6 state addendum and run-36 CSV review register were also stored in the same folder.

No Library files were deleted, renamed, or moved. The old and new `HCM_Zenodo_10_Papers.zip` archives have the same recorded size, but the old archive's raw bytes could not be materialized for a binary comparison. Historical repository ZIP variants also require commit/hash verification before deletion. Preserve them pending identity checks.

## 12. Scientific governance remains unchanged

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

No new scientific snapshot, Type-I calibration, confirmatory execution, endpoint computation, independent replication promotion, claim support, or scientific promotion is authorized. HCM conceptual papers and software/security checks do not establish consciousness, HCM causation, a universal mechanism, or empirical validation.

## 13. Next authorized actions

1. Preserve this V6 state record and the five run artifacts in `Current Evidence`.
2. If updating the repository, create a documentation-only commit on `review/type1-v4-remediation` containing this V6 addendum and a separate append-only run-36 evidence row/register update. Do not touch `main`.
3. **No GitHub Actions workflow is authorized to run after that documentation-only commit.** The one permitted software-only run (run 36) is complete. No further run is needed merely to validate a Markdown/CSV documentation update.
4. Continue read-only review of the three Scorecard `contents: write` warnings and package provenance. Do not dispatch `replication.yml`, `canonical-sync.yml`, `cross-run-memory-verification.yml`, any scientific workflow, or the container child workflow.
5. Keep the 12 owner-listed workflows disabled. Do not re-enable them.
6. Obtain direct Zenodo record JSON and published PDF downloads for records 02–10; then compare record metadata, file size, MD5, SHA-256, and Markdown-source relationship before changing any publication status.
7. Await the four attributable independent human review reports.

**Final status:** run 36 provides successful, exact-commit software-assurance evidence on the review branch, with the container job skipped. The manual container-input guard is present and behaved as intended in this run. Container sec
