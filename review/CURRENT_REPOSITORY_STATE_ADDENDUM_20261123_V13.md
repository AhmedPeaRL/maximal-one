# HCM Current Repository and Evidence State Addendum --- V13

-   **Evidence date:** 2026-11-23
-   **Repository:** `AhmedPeaRL/maximal-one`
-   **Scope:** documentation-only state record; no scientific snapshot
-   **Disposition:**
    `REVIEW_ONLY / SECURITY_OPEN / HUMAN_REVIEW_PENDING / NO_WORKFLOW_AUTHORIZED`

## 1. Exact live repository state

The current GitHub connector/API comparison identifies:

-   `main`: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
-   `review/type1-v4-remediation`:
    `e98a7110465d615219b8f5c6acfe5f2e24b85547`
-   V12 parent/current-before-V1 commit:
    `5397113032232f2e5c9ddeb4b776509d9a4b5f86`
-   V12 → V1 documentation commit:
    `e98a7110465d615219b8f5c6acfe5f2e24b85547`
-   V12 → current Review comparison: exactly one commit ahead, zero
    behind.
-   Current Review vs `main`: Review is 734 commits ahead and 36 behind;
    the merge base remains `a9808bd999a7ad902daf15606272529ca9af4580`.

The V1 commit (`Add files via upload`, created 2026-11-23 14:40:56 UTC)
adds exactly two files:

1.  `review/ZENODO_PUBLISHED_BINARY_VERIFICATION_20261123_V1.md`
2.  `review/zenodo-published-papers-20261123.sha256`

No workflow YAML, Dockerfile, application code, scientific protocol,
dataset, DOI record, or `main` content was changed by that commit. The
Review branch currently points exactly to V1's commit. Preserve V12 and
V1 unchanged; this V13 file is a prospective follow-up record, not an
instruction to rewrite either historical file.

## 2. Uploaded ZIP archive identity and bounded alignment

### Main archive

-   Source: owner-uploaded `maximal-one-main(20261122-212012).zip`
-   SHA-256:
    `f59222d0eedd9073ea15ef51b1463c3926e7948fd0e8d417a536c78756634091`
-   ZIP integrity: pass (`testzip() == None`)
-   Entries: 1,166
-   Files: 1,051
-   Uncompressed bytes: 3,939,438

### Review archive

-   Source: owner-uploaded
    `maximal-one-review-type1-v4-remediation(20261123-145101).zip`
-   SHA-256:
    `88eb991eeedf8e85b6f09f54f3fe5e5e36cb11ff6f957fd8d491ce863fbf2061`
-   ZIP comment identifies commit
    `e98a7110465d615219b8f5c6acfe5f2e24b85547`
-   ZIP integrity: pass (`testzip() == None`)
-   Entries: 1,445
-   Files: 1,323
-   Uncompressed bytes: 22,634,728

Selected critical Git blob identities from the Review archive were
cross-checked against GitHub, including V12, V1, its SHA-256 manifest,
`Dockerfile`, `SECURITY.md`, `THREAT_MODEL.md`, and
`.github/workflows/build-image.yml`. These checks strongly corroborate
alignment to the current commit but are not a full byte-for-byte
comparison of every archive entry against the GitHub tree.

Static syntax checks on the Review archive:

-   52 root `.github/workflows/*.yml` definitions parsed with PyYAML;
    zero parse errors.
-   41 root workflow files contain `workflow_dispatch`.
-   572 Python files passed `ast.parse`.
-   157 JSON files parsed successfully.

These are syntax/inventory checks, not a complete security audit, full
semantic workflow validation, or proof that a workflow is
enabled/disabled.

## 3. Zenodo direct-verification transcript now preserved in Library

The combined source-and-transcript file is now stored at:

`Hybrid Consciousness Model - HCM/Current Evidence/ZENODO-TERMUX_VERIFICATION.txt`

-   File size: `11,910` bytes
-   File SHA-256:
    `26bd3599724af75733515dba9d897bceb9888f301d1a7a5e1fd2ef83565cab92`
-   It contains the `zenodo_verify.py` source followed by the Termux
    terminal output; it is not a separate `.py` file plus a separate
    `.txt` transcript.
-   Extracted script length: `4,476` bytes
-   Extracted script SHA-256:
    `9968f816895f4d2719f8fd30d37301e5bad0d3daee92c7eeb8edb7e9f9f83eae`
-   Extracted script passed Python AST parsing.

The transcript contains successful per-file output for all ten published
paper PDFs and Paper 01's additional `README.pdf`. For each of the ten
paper PDFs, the transcript reports:

-   downloaded byte count equal to Zenodo's declared size;
-   valid `%PDF-` signature;
-   actual MD5 equal to the Zenodo file checksum;
-   actual MD5 equal to the Registry paper MD5;
-   SHA-256 matching the assistant-side recomputation from the
    separately stored Library ZIP.

The README has a valid PDF signature, matching size and Zenodo MD5, and
its SHA-256 matches the Library archive. Its printed
`REGISTRY_MD5_MATCH: False` is expected because the Registry MD5 field
is a paper-PDF identity, not a README identity. Treat README Registry
comparison as `NOT_APPLICABLE`, not as a failed paper match.

**Scope limitation:** the direct downloads were executed by the
repository owner in Termux. The assistant environment could not
independently download the PDFs from Zenodo during this review. The
independent recomputation was performed against the separately stored
Library archive, and matched the supplied Termux output. This is
`PASS_SCOPE_LIMITED` for binary identity, not independent acquisition
from Zenodo, scientific validity, peer review, or empirical
confirmation.

**Script hardening note:** the supplied script catches per-record
exceptions and prints an error but does not aggregate failures into a
non-zero process exit status. The supplied transcript was manually
inspected and contains all ten paper results without a `RECORD_ERROR`
entry, but the script should be hardened before reuse: fail closed on
any record/file error, distinguish README from Registry paper MD5,
validate expected record IDs/DOIs and filenames, and validate the final
URL after redirects. Do not reinterpret this script-quality note as a
mismatch in the ten observed paper binaries.

The V1 addendum remains unchanged. Its statement that the
script/transcript were not yet separately uploaded accurately describes
the evidence available when V1 was authored; this later combined file is
a subsequent Library preservation action.

## 4. Library evidence organization completed

The following files are now in
`Hybrid Consciousness Model - HCM/Current Evidence/`:

-   `Zenodo_HCM_Published_Papers.zip`
-   `ZENODO-TERMUX_VERIFICATION.txt`
-   `trivy-image-report-44828421411.zip`
-   `trivy-image-report-44944152951.zip`
-   `osv-dependency-inventory-44944152951.zip`
-   `osv-dependency-inventory-44948856035.zip`
-   `exact-commit-software-assurance-44944152951.zip`
-   `exact-commit-software-assurance-44948856035.zip`
-   `CURRENT_SCORECARD_RESIDUAL_REVIEW_REGISTER_20261121_V6.csv`

The additional Trivy artifact for Run 44828421411 was downloaded and
verified before Library upload:

-   Artifact ID: `14674273098`
-   Artifact name: `trivy-image-report-44828421411`
-   GitHub artifact SHA-256:
    `42bf569c49c670c4423cce49b923ba8dc4ab0175f6cde074ae1b8a7d9b7d1a84`
-   Local ZIP integrity: pass
-   Report: 47 HIGH finding records, 11 unique CVEs, zero CRITICAL
    findings.
-   Image tag:
    `maximal-one-cli:aed3109b7a6ba28e956ef5d6db40efa06fb17dae`
-   Artifact expiry shown by GitHub: 2026-12-20 22:24:05 UTC.

No existing Library evidence was replaced or deleted. The transcript and
additional artifact were added/moved into the project-specific
`Current Evidence` folder.

## 5. Historical workflow-run evidence reviewed

The recent GitHub Actions failure notifications in Gmail refer to runs
before V12, not evidence of a post-V12 run. The most relevant inspected
runs are:

### Run 44944152951 --- 2026-11-21

-   Review commit: `48b223e8d5192ed133ba1f0e59493b6e36600950`
-   Exact-commit scanner and OSV jobs succeeded.
-   Container build and CLI smoke test succeeded.
-   Trivy gate failed.
-   Trivy report: 50 HIGH finding records, 12 unique CVEs, zero
    CRITICAL.
-   This is the previously preserved Run35 report.

### Run 44828421411 --- 2026-11-20

-   Review commit: `aed3109b7a6ba28e956ef5d6db40efa06fb17dae`
-   Exact-commit scanner and OSV jobs succeeded.
-   Container image build and CLI smoke test succeeded.
-   Trivy gate failed.
-   Trivy report: 47 HIGH finding records, 11 unique CVEs, zero
    CRITICAL.
-   Artifact preserved in the Library as described above.

### Run 44820794670 --- 2026-11-20

-   Review commit: `3a3d381a5bf5a74f8f7c08aae8d6b467f5d8288f`
-   Docker build failed before Trivy could run.
-   Root cause in that historical Dockerfile: `apt-get download` saved
    the Debian package with an epoch colon encoded as `%3a` in the
    filename, while the subsequent checksum/install commands expected a
    filename without that encoding.
-   The current Review Dockerfile uses a `find`-based filename discovery
    step, which appears to address that filename mismatch. It has not
    been revalidated by a later authorized build; do not call the build
    fix closed until a permitted future build verifies it.

### Run 44816950851 --- 2026-11-20

-   The manual exact-commit guard correctly rejected a supplied
    `scan_commit` (`d50c21cf60cbafacf282439e7bbff6200759a03c`) that did
    not equal the selected Review branch HEAD
    (`0fe95249512619b982065b8a076cee8e8fa9a110`).
-   OSV inventory succeeded.
-   A secondary workflow defect then occurred: the `if: always()`
    manifest step attempted to write `reports/assurance-manifest.json`
    when the earlier validation step had failed and the `reports/`
    directory had never been created. The manifest step failed with
    `FileNotFoundError`.
-   Future workflow remediation should create `reports/` inside the
    always-run manifest step before writing, and should record a
    structured preflight-blocked state. No workflow edit or run is
    authorized by this addendum.

### Run 44732932113 --- 2026-11-20

-   Review-branch guard and exact Review HEAD checks succeeded.
-   Dependency refresh and publish jobs were skipped.
-   The nested exact-assurance scanner failed its gate; OSV inventory
    succeeded.
-   No dependency lock publication occurred.

A prior Actions API query filtered after the V12 commit time returned
zero runs. The current Gmail search found no new GitHub Actions
notification after 2026-11-22. These are bounded checks; a complete
current Actions-run enumeration was not available in the current
connector surface. The owner also reports no post-V12 workflow
execution.

## 6. Current workflow inventory and authority boundary

The current Review archive contains 52 root workflow YAML files; 41
contain `workflow_dispatch`. YAML parsing succeeded, but workflow
enablement is a separate GitHub setting and was not independently
verified.

The owner's latest attestation names these 12 disabled workflows:

1.  Emergent Periodicity Analysis
2.  External Verification
3.  Reproducible Research Gate
4.  SOS Robustness Gate
5.  Build and Push Container --- current name on `main`
6.  Build and Publish Container --- current name on Review
7.  Cross Run Memory Verification
8.  Immutable Release Lock
9.  Evolution Engine
10. Canonical Sync
11. Cross Architecture Timing Test
12. Cross Architecture Timing

Classification: `OWNER_ATTESTATION_NOT_INDEPENDENTLY_VERIFIED`.

**Important omission to resolve:** the earlier V12 owner-attested list
also included `Validate Stress`, but the latest 12-item attestation does
not mention it. The current workflow file
`.github/workflows/validate-stress.yml` is schedule-only (`0 3 * * 0`)
and has no `workflow_dispatch`. If enabled on the default branch, its
next scheduled time after this evidence date is Sunday 2026-11-29 at
03:00 UTC (05:00 Egypt local time). Its current enabled/disabled state
remains unverified and must be reconfirmed.

The Review copy of `.github/workflows/build-image.yml` is named
`Build and Publish Container` and has an unfiltered `push` trigger. If
enabled, a Review-branch documentation push can start its build and
stability-check jobs. Its publish job is restricted to pushes on `main`.
The owner currently attests it is disabled; re-check this setting
immediately before any future Review push. This workflow has no
`workflow_dispatch`.

`replication.yml` is not part of the owner-listed disabled set. It has
`workflow_dispatch`, defaults `assurance_only=true`, and can invoke the
exact-assurance reusable workflow. Setting `assurance_only=false`
activates dependency refresh and a publish job with `contents: write`.
It is not an authorized workaround and must not be dispatched or
modified.

The four Review-only workflow definitions remain
non-manually-dispatchable in their current forms:

-   `container-cli-smoke-review.yml`: `workflow_call` only.
-   `dependency-vulnerability-inventory.yml`: `workflow_call` only.
-   `evaluation.yml`: `pull_request` only.
-   `scientific-evaluation.yml`: `pull_request` only.

`software-assurance-exact-commit-v1.yml` exists on both branches. The
Review version requires the selected Review branch and
`scan_commit == GITHUB_SHA`. Its `run_container_review` input is
declared under `workflow_call`, not `workflow_dispatch`; the manual UI
cannot turn on the container child job. The Main copy is an older
definition and must not be used as a substitute for the Review copy.

`type1-human-overlay-preflight-v5.yml` has divergent branch copies: Main
contains the older V5/V4 source pairing, while Review contains the V6
preflight-only version tied to Population Register V9.
`type1-target-batch-generation-v4.yml` also has divergent V4/V9 source
pairings. Neither is authorized to run.

**Current run authorization: NONE. No `.yml` file is authorized to run
after this documentation commit or at the current Review HEAD.** Do not
click Run workflow, enable a workflow, use `replication.yml`, or trigger
any push/PR/schedule workflow as a workaround.

For any future workflow that exists only on the Review branch: GitHub's
manual Run workflow UI requires the workflow file to exist on the
default branch. If the same workflow filename exists on `main` and
Review, select the Review branch in the UI; the run uses the workflow
definition on the selected ref. A workflow present only on Review and
absent from the default branch will not appear as a directly manually
runnable workflow in the UI. Do not copy a dispatcher to `main` merely
to bypass this rule. A `workflow_call`-only child is not directly
runnable from the UI; it requires an authorized caller workflow.

## 7. Container security and Debian Trixie status

The latest preserved Trivy report (Run 44944152951) records 50 HIGH
finding records across 12 unique CVEs and zero CRITICAL findings. Run
44828421411 records 47 HIGH findings across 11 unique CVEs and zero
CRITICAL findings.

As checked against the official Debian Security Tracker on 2026-11-23,
**all 12 CVEs from the latest Trivy report remain marked vulnerable for
the Trixie package versions present in the image**:

-   `util-linux` --- CVE-2026-76642, CVE-2026-78408, CVE-2026-78409,
    CVE-2026-78410; installed family version `2.41.5-0+deb13u1`.
-   `sqlite3` --- CVE-2026-119373, CVE-2026-119374, CVE-2026-119379;
    installed `3.46.1-7+deb13u2`.
-   `systemd` --- CVE-2026-16742; installed `257.13-1~deb13u1`.
-   `acl` --- CVE-2026-54369; installed `2.3.2-2+b1`.
-   `ncurses` --- CVE-2025-69720; installed `6.5+20250216-2`.
-   `openssl` --- CVE-2026-124709; installed `3.5.7-1~deb13u3`.
-   `perl` --- CVE-2026-9538; installed `5.40.1-6+deb13u1`.

Official tracker references:

-   `https://security-tracker.debian.org/tracker/source-package/util-linux`
-   `https://security-tracker.debian.org/tracker/source-package/sqlite3`
-   `https://security-tracker.debian.org/tracker/source-package/systemd`
-   `https://security-tracker.debian.org/tracker/source-package/acl`
-   `https://security-tracker.debian.org/tracker/source-package/ncurses`
-   `https://security-tracker.debian.org/tracker/source-package/openssl`
-   `https://security-tracker.debian.org/tracker/source-package/perl`

Do not suppress Trivy findings, substitute Forky/Sid packages into
Trixie, or edit the Dockerfile until official Trixie fixes and package
provenance/compatibility are reviewed. No post-V12 container rescan
exists. Container security remains `OPEN`.

## 8. Bounded source-code review findings

-   572 Python files parsed successfully; this is not a full code audit.
-   `env/fingerprint.py` uses `subprocess.check_output(..., shell=True)`
    with currently constant internal command strings. No direct
    user-input path was found in the reviewed call sites. Future
    hardening should use argument arrays and `shell=False`.
-   `api/public_reproduce_endpoint.py` claims zero-trust isolation but
    clones mutable `main`, installs `requirements-lock.txt` without
    `--require-hashes` and without an isolated virtual environment, then
    executes repository code. No in-repository caller was found in the
    inspected archive; deployment/external exposure is unknown. Treat as
    a latent high-priority risk before any exposure, not as proof of a
    currently deployed vulnerability.
-   The current Dockerfile is still based on a pinned
    `python:3.11.18-slim-trixie` image and a pinned `zlib1g` package.
    The pinned zlib download filename discovery has not been revalidated
    by a later authorized build. The `FROM --platform=linux/amd64` line
    also generated a BuildKit warning
    (`FromPlatformFlagConstDisallowed`) in the historical build log.

## 9. Human review and scientific status

Gmail review of the four reviewer threads found the latest outgoing
correction/scope messages but no substantive inbound independent review
reports. The four requested reports remain `PENDING`.

-   Type-I protocol freeze: `NOT_FROZEN`.
-   Formal calibration: `NOT_AUTHORIZED`.
-   Confirmatory execution: `NOT_AUTHORIZED`.
-   Replication: `NOT_AUTHORIZED`.
-   Scientific claim support/promotion: `NOT_ESTABLISHED / NONE`.
-   Independent peer review: `PENDING`.
-   Container security: `OPEN`.
-   Zenodo published-binary identity: `PASS_SCOPE_LIMITED`.
-   No new scientific snapshot is authorized or required by this
    addendum.

GitHub profile/repository HTML and GitHub Pages returned `Cache miss`
through the browser surface. This is not evidence that the Pages site is
down. Pages publication status remains unverified here. The `.git` URL
is a Git transport endpoint, not a normal HTML page; current state was
checked through GitHub API data and owner-provided archives instead.

## 10. Required next actions

1.  **Confirm whether `Validate Stress` remains disabled.** It appeared
    in the earlier 13-item attestation but not in the latest 12-item
    list. If enabled, disable it manually only through the owner's
    intended GitHub settings process; do not run it.
2.  Before any future Review push, manually re-check that
    `Build and Publish Container` is still disabled. Its unfiltered
    `push` trigger makes this a hard precondition.
3.  Preserve V12 and V1 unchanged. If this V13 file is adopted, add it
    only to `review/type1-v4-remediation` as a documentation-only
    change. Do not change `main`.
4.  Do not run any workflow after this documentation commit. No `.yml`
    is authorized.
5.  Do not modify workflow YAML, Dockerfile, application code,
    protocols, datasets, DOI records, or branch policies in this
    documentation-only step.
6.  Keep the Debian Trixie package/CVE remediation open until official
    Trixie fixes are available and a separately authorized build/scan
    verifies them.
7.  Correct the exact-assurance manifest step in a separately authorized
    workflow-only remediation by creating `reports/` before writing the
    manifest on early preflight failure.
8.  Harden `zenodo_verify.py` before reuse; retain the present combined
    transcript and all published PDF identities unchanged.
9.  Continue waiting for the four independent human review reports. Do
    not start Type-I calibration, confirmatory execution, replication,
    or scientific claim promotion before the relevant independent
    reviews and formal governance authorization.

No claim of 100% assurance, scientific truth, empirical confirmation,
security closure, or completed peer review is made.
