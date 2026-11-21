# Current Repository, Security, and Governance Audit — 2026-11-21 V4

**Status:** `REVIEW_ONLY — NO_WORKFLOW_RUN_AUTHORIZED — NO_NEW_SCIENTIFIC_SNAPSHOT`

## 1. Current GitHub identities

- Repository: `AhmedPeaRL/maximal-one`
- Default branch `main` HEAD: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- Review branch HEAD: `a6ec52661bfe07446be9a1de3234cdf253b8ef1a`
- Review branch parent: `aed3109b7a6ba28e956ef5d6db40efa06fb17dae`
- Compare against main: `diverged`; review branch `707` commits ahead and `36` behind.
- Main has not changed from the verified `9749de...` commit.
- `a6ec526...` is GitHub signature-verified (`verified=true`, reason `valid`) and changes only one Markdown file: `review/CONTAINER_IMAGE_SECURITY_TRIAGE_20261121_V3.md` (155 additions, 0 deletions). It does not change code, data, Dockerfile, workflows, or scientific protocol.

### Correction to V3

V3 was prepared against `aed3109...` and then committed as `a6ec526...`. Consequently, after that commit, V3's internal statement that `aed3109...` was the current branch HEAD and that the branch was 706 commits ahead became stale. The correct distinction is:

- scanned/code commit for run `44828421411`: `aed3109...`
- current documentation-only branch HEAD: `a6ec526...`
- current branch divergence: 707 ahead / 36 behind.

V3 remains a historical record. This V4 corrects its branch identity and current disposition; it does not rewrite V3.

## 2. Uploaded ZIP snapshots and artifacts inspected

### Repository ZIPs

- `maximal-one-main.zip`: 1,051 files; SHA-256 `f59222d0eedd9073ea15ef51b1463c3926e7948fd0e8d417a536c78756634091`.
- `maximal-one-review-type1-v4-remediation.zip`: 1,296 files; SHA-256 `68ae27708c3d1475a738cf6df79f25d463fc151ba4aac42a7c618b1a8555f1d5`.
- The review ZIP does not contain V3; it is a pre-`a6ec526...` source snapshot. The current GitHub branch contains V3 at `review/CONTAINER_IMAGE_SECURITY_TRIAGE_20261121_V3.md`.
- ZIPs are snapshots, not live clones. The branch and file identities above were separately checked through GitHub.

### Run `44828421411`

Workflow: `.github/workflows/software-assurance-exact-commit-v1.yml`
Scanned code commit: `aed3109b7a6ba28e956ef5d6db40efa06fb17dae`

| Job | Job ID | Result |
|---|---:|---|
| Exact Commit Software Assurance | `136606855910` | SUCCESS |
| OSV Dependency Inventory | `136606856228` | SUCCESS |
| Container Review Guard | `136607045949` | SUCCESS |
| Container Build / CLI / Trivy | `136607089034` | FAILURE at Trivy policy threshold |

Artifacts:

- Software assurance artifact `14675476372`; SHA-256 `baf6d19d44c5b79dac7c807265d879a6c21d1eaddc879504a8a147eb7b0029f2`.
- OSV artifact `14675381458`; SHA-256 `ea1cb6691d24f9ace73028309fca246f139c8ab0ef5898d882d0a6f8e299139f`.
- Trivy image artifact `14674273098`; SHA-256 `42bf569c49c670c4423cce49b923ba8dc4ab0175f6cde074ae1b8a7d9b7d1a84`.

## 3. What the scanner results actually establish

### Software assurance

- actionlint `1.7.12`: exit code `0`; output file empty. The workflow explicitly supplies three ignore patterns for the new GitHub `$/` self-repository reusable-workflow syntax. GitHub's current documentation accepts this syntax; it is not a YAML defect.
- zizmor `1.30.1`: exit code `0`; JSON findings array empty; run was offline.
- OpenSSF Scorecard `5.6.0`: exit code `0`; overall score `9.2/10`.
- Scorecard's Fuzzing check is `0`; License is `9`; Token-Permissions is `10`, but its detail list still warns about job-level `contents: write` in `canonical-sync.yml:51`, `cross-run-memory-verification.yml:57`, and `replication.yml:232`.
- Scorecard's `repo.commit` metadata is `unknown`; the separate assurance manifest binds the scan commit and run ID.
- Scorecard's Vulnerabilities check reports zero within its own check scope. This does not override the separate Trivy OS-image scan.
- The workflow's success criterion checks scanner exit codes. A zero exit code means the tool completed; it is not equivalent to zero warnings, zero vulnerabilities, or a security certification.

### OSV source dependency inventory

- OSV-Scanner `2.7.1`: exit code `0`; valid JSON; `results: []`.
- Six supported manifests/lockfiles were scanned: five Python requirements files (48 package entries each) and `package-lock.json` (0 packages).
- This is source-manifest coverage only. It is not the OS package inventory inside the Docker image.

### Container build and CLI smoke

The image build succeeded. The Dockerfile pins:

`python:3.11.18-slim-trixie@sha256:b701198cb708b68d9413ca67d6311bd97c9389a2c5fe4da0511fc652642366cd`

The zlib installation step downloaded and checksum-verified `zlib1g=1:1.3.dfsg+really1.3.1-1+deb13u1`; `dpkg-query` verified that exact installed version. The build log confirms the encoded APT filename was found and installed.

The CLI smoke passed:

- `python -m scripts.generate_report --help` exposed `--seed`.
- Python runtime assertion passed for `3.11.18`.
- Non-root assertion passed (`uid != 0`).
- No scientific analysis ran.

Debian's tracker lists the exact zlib Trixie security version above as fixed for CVE-2026-85091. This specific zlib remediation is closed for the scanned image, based on the package download, checksum, installed-version assertion, and scan result.

### Trivy image result — still OPEN / policy FAILED

- Image OS: Debian `13.7`; inventory: 87 OS packages.
- HIGH finding records: `47`.
- CRITICAL finding records: `0`.
- Distinct CVEs: `11`.
- Binary package names represented: `18`.
- Node and Python package results: no vulnerabilities reported.
- Severity filter: `HIGH,CRITICAL`; `ignore-unfixed=false`; Trivy exit code `1`.

The 47 are scanner finding records, not 47 distinct CVEs. Several source-package CVEs are repeated across binary packages belonging to the same Debian source package. They must not be described as 47 independently established exploitable application flaws.

Distinct CVEs:

- `CVE-2025-69720` — ncurses
- `CVE-2026-119373`, `CVE-2026-119374`, `CVE-2026-119379` — sqlite3
- `CVE-2026-16742` — systemd
- `CVE-2026-54369` — acl
- `CVE-2026-76642`, `CVE-2026-78408`, `CVE-2026-78409`, `CVE-2026-78410` — util-linux
- `CVE-2026-9538` — perl / Archive::Tar

The installed Trixie source-package versions in the scan are:

- util-linux `2.41.5-0+deb13u1`
- sqlite3 `3.46.1-7+deb13u2`
- systemd `257.13-1~deb13u1`
- acl `2.3.2-2`
- ncurses `6.5+20250216-2`
- perl `5.40.1-6+deb13u1`

As checked on 2026-11-21, Debian's Security Tracker still marks these six source-package families as vulnerable in Trixie for the listed CVEs; fixed versions are shown in newer Forky/Sid lines. Do not mix Forky/Sid packages into Trixie, switch to an unverified base, or suppress findings merely to turn the gate green. Wait for Trixie fixes or conduct a separate, documented package/component applicability and VEX assessment. Do not label a finding false positive without evidence.

## 4. Workflow and branch governance

The owner attests that the following 12 workflows remain disabled in GitHub Actions settings:

1. Emergent Periodicity Analysis
2. External Verification
3. Reproducible Research Gate
4. SOS Robustness Gate
5. Build and Push Container (main name)
6. Build and Publish Container (review-branch name)
7. Cross Run Memory Verification
8. Immutable Release Lock
9. Evolution Engine
10. Canonical Sync
11. Cross Architecture Timing Test
12. Cross Architecture Timing

This remains an owner attestation, not independent verification of GitHub's server-side enabled/disabled state. Some YAML files remain under `.github/workflows` with schedule, push, or `workflow_dispatch` triggers. In the review branch, Evolution Engine and Immutable Release Lock have been moved outside `.github/workflows` into `docs/disabled-workflows/`; main still contains their workflow files. Do not re-enable any of the 12.

`replication.yml` is **not** one of the 12 disabled workflows. It defaults `assurance_only=true`, but that default still runs a guard, review-head check, and reusable read-only assurance scan. Setting it false activates dependency refresh and write/publish logic. Do not dispatch it or change the default.

The review-only child `.github/workflows/container-cli-smoke-review.yml` is `workflow_call` only; it is not a direct Run workflow target. It requires the review branch and `review_only=true`, builds locally without registry credentials, runs CLI smoke, and scans with Trivy.

The parent `.github/workflows/software-assurance-exact-commit-v1.yml` exists on both branches. The main copy is older, has a stale default `scan_commit`, and does not include `run_container_review`. The review copy includes the review-branch guard, exact-HEAD validation, and optional `run_container_review` input. GitHub supports `$/` same-repository reusable-workflow references; the child is called from the parent on the same commit.

**No workflow is authorized now.** When a later container scan is justified by Trixie security updates and a reviewed Dockerfile change, the only candidate is the parent exact-commit assurance workflow, on `review/type1-v4-remediation`, with `scan_commit` set to the exact then-current full branch HEAD and `run_container_review=true`. If the UI does not expose that input after selecting the review branch, stop and obtain a screenshot; do not dispatch with guessed/default values and do not modify main to work around it without a separate decision.

For a workflow file present only on the remediation branch:

- A `workflow_dispatch` file must exist on the default branch for the Actions UI's Run workflow button.
- A branch-only `workflow_call` child cannot be run directly; it must be called by a parent workflow that is dispatched on the selected review ref.
- Do not add a new dispatcher to main merely for convenience. Use an existing default-branch dispatcher where its selected-branch implementation and inputs are verified; otherwise stop for a deliberate, isolated dispatcher decision.

## 5. Human review and scientific status

Four independent human review tracks remain pending; no attributable review report has been received in the searched Gmail threads as of 2026-11-21:

- Politis — statistical-methods review. The Nov 19 correction points to V9 target `ad106...`, V4 draft and candidate matrices, `alpha_max=NOT_SET`, and historical V1 `NOT_PASSED`. No formal calibration is authorized.
- Machiry — GitHub Actions/CI security review. The Nov 19 follow-up supplies V9 snapshot and exact-target software-assurance evidence. No human security disposition received.
- Seppälä — climate-domain review. The candidate was corrected from HadCET to HadUKP EWP. A raw-source SHA discrepancy remains unresolved; no climate domain is approved for replication.
- Wong — econometric review. The candidate was corrected from INDPRO to a separately defined CPIAUCNS pre-gap window. October 2025 is missing in the full series and must not be imputed or silently dropped. Wong's out-of-office reply says delays may occur through November 29; no substantive review received.

The pinned scientific target remains `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`; the V9 snapshot is historical and preserved. No new snapshot is authorized. `alpha_max=NOT_SET`; the V4 candidate matrix remains `REVISE_AND_RESUBMIT`; historical V1 remains `NOT_PASSED` under its original rule. Approved independent secondary domains `0/2`; replication `0/2`.

The following remain unchanged:

- `protocol_freeze=NOT_FROZEN`
- `formal_calibration_authorized=false`
- `confirmatory_execution_authorized=false`
- `claim_support=false`
- `promotion_authority=false`
- manual adjudication overlay records `0`

## 6. HCM manuscript files inspected

The three supplied PDFs are conceptual manuscripts, not evidence of the Docker/security result or of empirical validation:

- Paper 01, *Presence Without Demand*: explicitly states that it provides no empirical validation, benchmarks, or experimental results.
- Paper 08 (filename: `HCM_Paper_08_When_Measurement_Approaches_the_Thresholdes`), titled *Formalism Without Control in Hybrid Conscious Architectures* with the subtitle *When Measurement Becomes Pressure: Limits of Quantification in Hybrid Conscious Fields*: argues for formal description without allowing formalism to become an internal control imperative; it is a conceptual/philosophical argument, not an empirical test.
- Paper 10 (filename: `HCM_Paper_10_Application_Without_Extraction`), titled *Reframing Application as Presence Within the Hybrid Consciousness Model*: argues for non-extractive, non-coercive application and explicitly does not claim that such systems are conscious.

Local binary identities:

| File | MD5 | SHA-256 |
|---|---|---|
| Paper 01 | `24a27ca6b33a0ada641c1f96ed50ab63` | `fb97104ce381683d9721657f3bdd6abe32ce9b2629043b9965826e388724dd29` |
| Paper 08 | `a69b11345fb4d83abe5bf3e58d9d10ff` | `d65046a5fac10fcb928b014f3df381c85571211ee93f18fde461b7cd254c6912` |
| Paper 10 | `62ef82c7c2efeea2dc10a20366dfadf5` | `da954d5bfb7525e6aa3f77771e81f71b08ee1b3fda5b3df945e06943905bd4b5` |

These local MD5s match the local-file values in the existing residual register and differ from the Zenodo-recorded MD5 values listed there. Treat the supplied PDFs as working copies; do not represent them as byte-identical published Zenodo binaries until the exact published files are retrieved and verified.

## 7. Library handling

- The `Current Evidence` Library folder now contains V3, V4, V6, and the three run-448284 artifact ZIPs. V4 and V6 were successfully uploaded.
- The `Working Manuscripts - Binary Identity Pending` folder was created. Paper 01 uploaded successfully; Paper 08 and Paper 10 uploads failed because the Library storage limit was reached. Both remain available as attachments in this conversation but are not yet in that Library folder.
- A second V3 copy at the project root was read and byte-for-byte text-compared with the V3 copy under `Current Evidence`; the contents are identical. The attempted deletion failed because that root item is a Project attachment, which `files.manage_library` cannot mutate. No Project attachment was deleted.
- Raw-byte materialization of older ZIP archive pairs failed with an authorization-path warning. Equal file size or similar names are not proof of duplicate bytes. No historical archive was deleted.
- Preserve V2 and V3 as historical records. V4 and V6 are the current audit records. Do not attempt further Library uploads until storage has been safely freed through an authorized Library-only cleanup.

## 8. Required next steps

1. No code change, Dockerfile change, workflow dispatch, calibration, confirmatory execution, snapshot, merge, or main-branch update now.
2. Add this V4 report to `review/CONTAINER_IMAGE_SECURITY_TRIAGE_20261121_V4.md` on `review/type1-v4-remediation` only.
3. Add the V6 residual register to `evidence/CURRENT_SCORECARD_RESIDUAL_REVIEW_REGISTER_20261121_V6.csv` on the same branch; preserve V5 as historical.
4. Documentation-only commit message: `Record current security and governance audit V4`.
5. Send the resulting commit URL and full SHA. Do not run any workflow after this documentation-only commit.
6. Keep Paper 08 and Paper 10 in the current conversation until Library storage is safely freed; then upload them to `Working Manuscripts - Binary Identity Pending`.
7. Continue monitoring the six Debian Trixie source-package families and wait for the four independent human reports. A future exact-commit container assurance run requires actual Trixie fix availability, a justified Dockerfile update, a reviewed diff, and separate authorization.

**Final disposition:** `REVIEW_ONLY — SECURITY_GATE_OPEN — HUMAN_REVIEWS_PENDING — NO_NEW_SNAPSHOT — NO_WORKFLOW_RUN_AUTHORIZED — NO_PROMOTION_AUTHORITY`.
