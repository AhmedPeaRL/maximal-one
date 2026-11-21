# Container Image Security Triage — 2026-11-21 V3

## Identity and scope

- Repository: `AhmedPeaRL/maximal-one`
- Branch: `review/type1-v4-remediation`
- Exact branch HEAD and scanned commit: `aed3109b7a6ba28e956ef5d6db40efa06fb17dae`
- Commit message: `Fix zlib installation in Dockerfile`
- Commit signature: GitHub reports `verified=true`, reason `valid`
- Workflow run: `44828421411`
- Workflow: `.github/workflows/software-assurance-exact-commit-v1.yml`
- Disposition: **REVIEW ONLY — IMAGE BUILT AND CLI SMOKE PASSED; TRIVY POLICY FAILED ON HIGH FINDINGS**

This report supersedes V2 as the current status report. V2 remains a historical record of run `44820794670` and should not be edited retroactively.

## Run and job outcomes

- Exact Commit Software Assurance — job `136606855910`: SUCCESS
- OSV Dependency Inventory — job `136606856228`: SUCCESS
- Container Review Guard — job `136607045949`: SUCCESS
- Container Build / CLI / Trivy — job `136607089034`: FAILURE, solely at the Trivy step because the configured HIGH/CRITICAL threshold returned exit code 1

The build and CLI stages completed before Trivy ran. The workflow uploaded the Trivy JSON report despite the policy failure.

## Dockerfile / zlib remediation verified

The build log confirms:

- APT downloaded `zlib1g=1:1.3.dfsg+really1.3.1-1+deb13u1` from `trixie-security`.
- The downloaded filename used the encoded epoch separator: `zlib1g_1%3a1.3.dfsg+really1.3.1-1+deb13u1_amd64.deb`.
- The Dockerfile's filename discovery found that file.
- `dpkg` installed the exact pinned version and `dpkg-query` verified it.
- The build completed successfully.

The Debian Security Tracker lists `1:1.3.dfsg+really1.3.1-1+deb13u1` as the fixed Trixie security version for CVE-2026-85091. The current Trivy report contains no CVE-2026-85091 record. For this exact image, the zlib version remediation is therefore supported by the package-install log, version assertion, and scan result.

Reference: https://security-tracker.debian.org/tracker/CVE-2026-85091

## CLI smoke evidence

The container CLI smoke test passed:

- `python -m scripts.generate_report --help` displayed the CLI help and the required `--seed` option.
- Runtime Python version assertion passed for Python `3.11.18`.
- Non-root runtime assertion passed (`uid != 0`).
- No scientific analysis was executed; the workflow only requested CLI help and inspected the runtime identity.

## Trivy image scan — current result

Artifact: `trivy-image-report-44828421411` (artifact ID `14674273098`)

- Detected OS: Debian `13.7`
- OS package inventory size reported by Trivy: 87 packages
- HIGH vulnerability records: **47**
- CRITICAL vulnerability records: **0**
- Distinct CVEs: **11**
- Affected OS package names represented in findings: **18**
- Node package result: no vulnerabilities reported
- Python package result: no vulnerabilities reported
- Scan severity filter: `HIGH,CRITICAL`
- `ignore-unfixed`: `false`
- Trivy exit code: `1` (expected policy failure because HIGH findings remain)

Distinct CVEs in the current report:

- `CVE-2025-69720`
- `CVE-2026-119373`
- `CVE-2026-119374`
- `CVE-2026-119379`
- `CVE-2026-16742`
- `CVE-2026-54369`
- `CVE-2026-76642`
- `CVE-2026-78408`
- `CVE-2026-78409`
- `CVE-2026-78410`
- `CVE-2026-9538`

Compared with the previously recorded historical baseline (48 HIGH records, 0 CRITICAL, 12 distinct CVEs, 19 affected OS packages), this run reports 47 HIGH records, 0 CRITICAL, 11 distinct CVEs, and 18 affected OS packages. These are scanner finding counts, not proof that all remaining issues are exploitable in this application.

## Debian Trixie remediation availability check

The Debian Security Tracker pages consulted for this triage currently mark the following source packages as vulnerable in Trixie for the CVEs appearing in the report, with fixes available in newer `forky`/`sid` package lines rather than Trixie's current package versions:

- `util-linux`: CVE-2026-76642, CVE-2026-78408, CVE-2026-78409, CVE-2026-78410
- `sqlite3`: CVE-2026-119373, CVE-2026-119374, CVE-2026-119379
- `systemd`: CVE-2026-16742
- `acl`: CVE-2026-54369
- `ncurses`: CVE-2025-69720
- `perl`: CVE-2026-9538

This is why an unqualified `apt-get upgrade` on the current Trixie base is not an evidence-backed fix for the remaining findings: the relevant Trixie package versions are still listed as vulnerable by Debian's tracker. Do not mix `forky`/`sid` packages into the Trixie image or change to an unverified base image without a separate compatibility and provenance review.

References:

- https://security-tracker.debian.org/tracker/source-package/util-linux
- https://security-tracker.debian.org/tracker/source-package/sqlite3
- https://security-tracker.debian.org/tracker/source-package/systemd
- https://security-tracker.debian.org/tracker/source-package/acl
- https://security-tracker.debian.org/tracker/source-package/ncurses
- https://security-tracker.debian.org/tracker/source-package/perl

## Software-assurance artifacts

Artifact `14675476372`, SHA-256:
`baf6d19d44c5b79dac7c807265d879a6c21d1eaddc879504a8a147eb7b0029f2`

- actionlint `1.7.12`: exit code 0; output file empty
- zizmor `1.30.1`: exit code 0; JSON findings array empty
- OpenSSF Scorecard `5.6.0`: exit code 0; aggregate score `9.2`
- Scorecard's `repo.commit` field is `unknown`; the separate assurance manifest binds `scan_commit` and `workflow_run_id` to the exact target.
- Scorecard Fuzzing check: score 0, no fuzzer integration detected.
- Scorecard License check: score 9; parser did not recognize the LICENSE file as an FSF/OSI license. Do not alter legal text solely to satisfy this parser.
- Scorecard Token-Permissions warnings include `canonical-sync.yml:51`, `cross-run-memory-verification.yml:57`, and `replication.yml:232`.

The owner reports that Canonical Sync and Cross Run Memory Verification remain disabled. That is an owner attestation, not a connector-verified setting. The `replication.yml` workflow is not among the owner's 12 disabled workflows; it defaults `assurance_only=true`, and its write-enabled publish job is guarded by `!inputs.assurance_only`. Do not dispatch it or set `assurance_only=false`.

Scorecard `9.2` and zero scanner exit codes are not a security guarantee or a substitute for manual finding review.

## OSV source dependency inventory

Artifact `14675381458`, SHA-256:
`ea1cb6691d24f9ace73028309fca246f139c8ab0ef5898d882d0a6f8e299139f`

- OSV-Scanner `2.7.1`: exit code 0
- JSON validation: passed
- `results` array: empty
- Six supported source manifests/lockfiles scanned: five Python requirements manifests (48 packages each) and `package-lock.json` (0 packages).

This is source dependency manifest coverage only. It does not establish that OS packages in the container image are vulnerability-free; the Trivy image report is the separate OS-image evidence.

## Artifact integrity

- Software assurance ZIP: `baf6d19d44c5b79dac7c807265d879a6c21d1eaddc879504a8a147eb7b0029f2`
- OSV ZIP: `ea1cb6691d24f9ace73028309fca246f139c8ab0ef5898d882d0a6f8e299139f`
- Trivy ZIP: `42bf569c49c670c4423cce49b923ba8dc4ab0175f6cde074ae1b8a7d9b7d1a84`

## Repository and governance state

- `main` HEAD: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- `review/type1-v4-remediation` HEAD: `aed3109b7a6ba28e956ef5d6db40efa06fb17dae`
- Branches remain diverged: review branch 706 commits ahead and 36 behind `main`.
- No merge, rebase, cherry-pick, or change to `main` is authorized.
- No publishing workflow is authorized.
- No new scientific snapshot is authorized.
- Protocol freeze: `NOT_FROZEN`.
- Formal Type-I calibration: `NOT_AUTHORIZED`.
- Confirmatory execution: `NOT_AUTHORIZED`.
- Scientific claim support: `NONE`.
- Promotion authority: `NONE`.

## Next action

Do not rerun the same workflow merely to obtain another red/green badge. First retain this V3 evidence record and monitor Debian Trixie security updates for the six affected source-package families. Once fixed Trixie package versions are available, update the base image or package pins only with exact version/digest evidence, inspect the Dockerfile and workflow diff, then authorize one exact-commit review run on `review/type1-v4-remediation` using `.github/workflows/software-assurance-exact-commit-v1.yml` with `scan_commit` equal to the then-current full branch HEAD and `run_container_review=true`.

No scientific execution or promotion authority is conferred by this report.
