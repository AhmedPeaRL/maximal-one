# HCM Current Repository and Evidence State Addendum — V15

- Evidence date: 2026-11-23
- Repository: `AhmedPeaRL/maximal-one`
- Scope: post-V14 repository identity, bounded Actions audit, evidence archive review, container security status, and one conditional read-only software-assurance dispatch
- Disposition: `REVIEW_ONLY / SECURITY_OPEN / HUMAN_REVIEW_PENDING / ONE_CONDITIONAL_SOFTWARE_ASSURANCE_DISPATCH / SCIENTIFIC_NO_GO`

## 1. Exact repository state

The current GitHub comparison reports:

- Default branch `main`: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`.
- Review branch `review/type1-v4-remediation`: `a647a806d228d98d9860b7802ada0a47e321f2f5`.
- Review is 736 commits ahead of `main` and 36 commits behind it.
- Merge base: `a9808bd999a7ad902daf15606272529ca9af4580`.
- Review HEAD is confirmed identical to `a647a806d228d98d9860b7802ada0a47e321f2f5`.

No merge, rebase, cherry-pick, pull request, promotion, or change to `main` is authorized.

## 2. V14 identity and exact delta

V14 commit:

`a647a806d228d98d9860b7802ada0a47e321f2f5`

Parent:

`abc08a203d8649ead0f30ac23c226a6ad91db535`

The compare between the parent and V14 reports exactly two added files:

- `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261123_V14.md`
- `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261123_V14.sha256`

No code, workflow, Dockerfile, protocol, dataset, or DOI file was changed by V14.

V14 Markdown SHA-256:

`8ece53836fdb4685457bcf63de8f458491436206585a8e2e446ba09e4fecf44e`

V14 manifest SHA-256:

`1abad483371bd54790899277762defa6ef87d74601935cd9f7da400c69cf3a49`

Git blob identities:

- Markdown: `7aecae367316e6c5d303934565fef72dcfe0bff3`
- Manifest: `acecd76beaf455e9bb35774f16b7a41a874e754b`

## 3. Archive and Library identity

Main archive:

- `maximal-one-main-9749de9-20261122.zip`
- 1,522,641 bytes
- SHA-256: `f59222d0eedd9073ea15ef51b1463c3926e7948fd0e8d417a536c78756634091`
- ZIP integrity passed.
- ZIP comment identifies main commit `9749de9253f144eeda9e1b60cb219cfc5f201ecc`.

Review archive currently in Library:

- `maximal-one-review-type1-v4-remediation-abc08a2-20261123.zip`
- 3,484,681 bytes
- SHA-256: `02d43033ff274d3278f49a9119e99fd0a4b3c8fe1338b4b95c75accccb35fbfb`
- ZIP integrity passed.
- ZIP comment identifies `abc08a203d8649ead0f30ac23c226a6ad91db535`.
- This archive is one documentation-only commit behind current Review HEAD `a647a806d228d98d9860b7802ada0a47e321f2f5`.
- It must not be described as an exact archive of current Review HEAD.

Historical V13 package:

- `HCM_Review_State_V13_Package_20261123.zip`
- 8,570 bytes
- SHA-256: `7f21fc0356afcb44a01e3f89cb46fe7706c0f2a2741add5647a24e054d77d77b`
- Contains only the V13 Markdown and its SHA-256 manifest.
- V14 is committed to GitHub Review but was not present as a separate package in the inspected Library listing.

Zenodo Library archive:

- `Zenodo_HCM_Published_Papers.zip`
- 1,115,283 bytes
- SHA-256: `c025b132da7f9c0727e9646cefb0ba0c2aabca096955b4cbbf51875579a0adf3`
- Contains ten paper PDFs and README.pdf.
- Local file sizes and MD5 values for the ten PDFs and README were independently recomputed and matched the metadata snapshots stored in `evidence/HCM-Papers_Zenodo.zip` in the Review archive.
- This is local archive-to-metadata identity evidence, not a fresh direct download from Zenodo during this review.

Zenodo verification transcript:

- `ZENODO-TERMUX_VERIFICATION.txt`
- 11,910 bytes
- SHA-256: `26bd3599724af75733515dba9d897bceb9888f301d1a7a5e1fd2ef83565cab92`

No V15 ZIP package has been created.

## 4. Bounded GitHub Actions history

V12 commit:

`5397113032232f2e5c9ddeb4b776509d9a4b5f86`

V12 commit timestamp:

`2026-11-22T17:11:22Z`

A branch-filtered GitHub Actions API query using `created > 2026-11-22T17:11:22Z` returned:

- `main`: `total_count = 0`
- `review/type1-v4-remediation`: `total_count = 0`

Run `45013476170` (`Validate Stress`) was created at `2026-11-22T10:39:08Z`, before the V12 cutoff. It is not a post-V12 run.

Latest Review run observed in the queried run list:

- Run `44948856035`
- `Exact Commit Software Assurance`
- Created `2026-11-21T20:55:56Z`
- Target commit `99dd702ce4f7569e19b55503506b3bbfe8c920fa`

This is bounded API evidence for the two named branches and the specified cutoff. It is not a complete all-time Actions audit.

## 5. Disabled workflow state

The repository owner attests that all thirteen workflows below remain disabled in the live GitHub settings:

1. Emergent Periodicity Analysis
2. External Verification
3. Reproducible Research Gate
4. SOS Robustness Gate
5. Build and Push Container — `main` name
6. Build and Publish Container — Review name
7. Cross Run Memory Verification
8. Immutable Release Lock
9. Evolution Engine
10. Canonical Sync
11. Cross Architecture Timing Test
12. Cross Architecture Timing
13. Validate Stress

Classification:

`OWNER_ATTESTATION_NOT_INDEPENDENTLY_VERIFIED`

The available repository inspection does not independently establish the server-side enabled/disabled state of every workflow. Workflow presence, absence of recent runs, or YAML triggers do not prove disabled status.

The Review `.github/workflows/build-image.yml` (`Build and Publish Container`) has an unfiltered `push` trigger. Its disabled state must be visually rechecked immediately before any Review push. If that state cannot be confirmed, do not push.

The `main` Build and Push Container workflow is a separate definition with different permissions and triggers. No changes to `main` are authorized.

## 6. Existing exact-commit assurance evidence

Latest completed exact-assurance run inspected:

`44948856035`

Target and workflow-definition commit:

`99dd702ce4f7569e19b55503506b3bbfe8c920fa`

Artifact identities:

- Exact assurance ZIP SHA-256: `9802a450328b3174047062496c21e10af21a340256764215f013135c804390fd`
- OSV ZIP SHA-256: `1d3aaa89287d26325e2810b6ad6fc7567cc5a418b759f52cc31c7a883eb6a604`

Observed results:

- actionlint 1.7.12: exit code 0, empty output.
- zizmor 1.30.1 offline: exit code 0, findings array empty.
- OpenSSF Scorecard 5.6.0: 9.2/10.
- Scorecard Fuzzing: 0/10.
- Scorecard License: 9/10.
- Scorecard Token-Permissions: numeric score 10/10, but manual warnings remain for `contents:write` in canonical-sync, cross-run-memory-verification, and replication workflows.
- OSV-Scanner v2.7.1: valid JSON, `results=[]`, scoped to supported source manifests and lockfiles.
- Container child job: skipped.

This run did not scan current Review HEAD `a647a806d228d98d9860b7802ada0a47e321f2f5`. Its zero scanner exit codes are not proof of zero risk, complete security closure, or scientific validity.

## 7. Container build and Debian Trixie status

Latest container build and image scan inspected:

- Run `44944152951`
- Image target commit `48b223e8d5192ed133ba1f0e59493b6e36600950`
- Trivy artifact SHA-256: `657ba2a2f687611c3ea5643ec128ab2fc1badd3cf0783dd8acba645415f791d7`
- Trivy artifact ID: `14723121334`

The Docker build succeeded. The CLI smoke test succeeded. Python `3.11.18` and non-root runtime identity were verified.

The zlib1g package download, SHA-256 check, installation, and `dpkg-query` verification succeeded for:

`1:1.3.dfsg+really1.3.1-1+deb13u1`

The report does not contain CVE-2026-85091. This is a scoped closure for that scanned image, not closure of the remaining image vulnerabilities.

Trivy reported 50 HIGH records, zero CRITICAL records, and twelve unique CVEs:

- util-linux: CVE-2026-76642, CVE-2026-78408, CVE-2026-78409, CVE-2026-78410
- SQLite: CVE-2026-119373, CVE-2026-119374, CVE-2026-119379
- OpenSSL: CVE-2026-124709
- systemd: CVE-2026-16742
- acl: CVE-2026-54369
- ncurses: CVE-2025-69720
- Perl: CVE-2026-9538

The Trivy step failed on the configured HIGH/CRITICAL policy. The build itself did not fail.

The official Debian Security Tracker currently lists the affected Trixie source package versions as vulnerable for these findings. No official Trixie package fix was established for the listed CVEs during this review.

Official tracker references:

- `https://security-tracker.debian.org/tracker/source-package/util-linux`
- `https://security-tracker.debian.org/tracker/source-package/sqlite3`
- `https://security-tracker.debian.org/tracker/source-package/openssl`
- `https://security-tracker.debian.org/tracker/source-package/systemd`
- `https://security-tracker.debian.org/tracker/source-package/acl`
- `https://security-tracker.debian.org/tracker/source-package/ncurses`
- `https://security-tracker.debian.org/tracker/source-package/perl`

The Dockerfile and requirements lockfile are unchanged between the container target commit and current Review HEAD. However, the Dockerfile uses `COPY . .`; later documentation changes can alter the build context. Therefore no byte-identical current-HEAD image claim is made.

Open build warnings include BuildKit's constant `FROM --platform=linux/amd64` warning and pip's root-install warning during the build stage. The runtime user is non-root.

Do not suppress Trivy findings, mix Forky/Sid packages into Trixie, or edit the Dockerfile before official Trixie fixes, provenance, and compatibility have been reviewed.

## 8. Code review items still open

- `env/fingerprint.py`: `subprocess.check_output(..., shell=True)` uses constant internal commands. A later code-only remediation should prefer argument arrays and `shell=False`.
- `api/public_reproduce_endpoint.py`: the inspected code clones mutable `main`, installs requirements without an explicit `--require-hashes` invocation and without an isolated virtual environment, then executes repository code. No in-repository caller was found in the inspected archive; deployment and external exposure remain unknown.

These are open hardening items, not proof of a deployed exploit.

## 9. Independent human reviews

The four requested independent review tracks remain pending:

- Dimitris Politis
- Anil Machiry
- Annika Seppälä
- Benjamin Wong

Acknowledgements or out-of-office messages are not substantive independent review reports. No report is to be treated as received unless it is attributable, dated, and contains actual review findings.

## 10. Scientific authority

The project remains:

- `REVIEW_ONLY`
- `PROTOCOL_NOT_FROZEN`
- `FORMAL_CALIBRATION_NOT_AUTHORIZED`
- `CONFIRMATORY_EXECUTION_NOT_AUTHORIZED`
- `CLAIM_SUPPORT_NOT_AUTHORIZED`
- `PROMOTION_NOT_AUTHORIZED`
- `REPLICATION_NOT_AUTHORIZED`

No new scientific snapshot, Type-I calibration, confirmatory execution, replication, publication claim, or promotion is authorized by this addendum.

## 11. One conditional manual software-assurance dispatch

Exactly one manual dispatch is conditionally authorized after this V15 documentation commit has been independently checked.

Authorized caller:

`.github/workflows/software-assurance-exact-commit-v1.yml`

Target branch:

`review/type1-v4-remediation`

Required manual input:

`scan_commit = exact V15 commit SHA`

The Review workflow blob SHA inspected before V15:

`134fcbfa344c8f7f775f521420709c2886ac288a`

The Main copy is a different workflow definition and must not be selected.

The Review caller has top-level `contents:read`, validates the Review branch, and requires manual `scan_commit` to equal `GITHUB_SHA`. It calls the Review-branch OSV inventory child using GitHub's same-repository reusable-workflow syntax.

The manual dispatch exposes only `scan_commit`. It does not expose `run_container_review`. The container child is not authorized and must remain skipped.

This authorization does not authorize `replication.yml`, any container build or Trivy job, any scientific workflow, or any other `.yml` file.

Before dispatch, independently verify that:

1. The V15 commit is the exact current Review HEAD.
2. The V15 commit changes only the V15 Markdown and SHA-256 manifest.
3. `main` remains unchanged.
4. The Review software-assurance workflow blob SHA remains `134fcbfa344c8f7f775f521420709c2886ac288a`.
5. The thirteen owner-attested disabled workflows remain disabled, especially Review `Build and Publish Container`.

If any condition fails or cannot be verified, do not dispatch.

## 12. Required next evidence update

After the V15 commit, retain:

- Exact commit SHA and commit URL.
- GitHub compare showing only the two V15 documentation files.
- Confirmation that `main` remains unchanged.
- The one authorized Review software-assurance run URL, job results, and complete artifacts.
- A fresh Review source archive aligned to the V15 commit, with its ZIP integrity and SHA-256 recorded in the Library.

No claim of 100% assurance, complete security closure, scientific validity, or independent peer review is made.
