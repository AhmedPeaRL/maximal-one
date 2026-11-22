# Container Security Review — 2026-11-22 V1

**Repository:** `AhmedPeaRL/maximal-one`  
**Branch under review:** `review/type1-v4-remediation`  
**Evidence run:** `44944152951` (Run 35)  
**Scanned commit:** `48b223e8d5192ed133ba1f0e59493b6e36600950`  
**Status:** `OPEN_SECURITY_GATE / NO_DOCKERFILE_CHANGE_AUTHORIZED`

## 1. Evidence inspected

The Run 35 container job built the image and passed its CLI smoke test. Trivy v0.76.2 then scanned with `severity=HIGH,CRITICAL`, `exit-code=1`, and `ignore-unfixed=false`. The scan step failed because HIGH findings were present; the report uploaded successfully.

- Workflow run: https://github.com/AhmedPeaRL/maximal-one/actions/runs/44944152951
- Artifact ID: `14723121334`
- Artifact ZIP SHA-256: `657ba2a2f687611c3ea5643ec128ab2fc1badd3cf0783dd8acba645415f791d7`
- Image ID: `sha256:57264f61530dd7711c4b30b3f5a869a86c1c66631fb4c1e3d6d19d46b34f5793`
- Image OS: Debian 13.7
- Image size: 976,166,912 bytes
- Findings: 50 HIGH vulnerability records, 12 distinct CVEs, 0 CRITICAL records.

The 50 count is a package-occurrence count, not 50 distinct CVEs. Several CVEs occur in multiple binary packages from the same source package. Run 36 (`44948856035`) skipped the container job and did not create a new Trivy report; it does not supersede Run 35's findings.

## 2. Package/CVE reconciliation

The image's Trivy report identifies these Debian package versions. Debian Security Tracker pages were checked on 2026-11-22. Status below is for Debian 13 `trixie`, not `forky` or `sid`.

| Source package / installed binary package(s) | Installed version in image | CVE(s) | Debian Trixie status at review |
|---|---|---|---|
| `util-linux` (`bsdutils`, `libblkid1`, `liblastlog2-2`, `libmount1`, `libsmartcols1`) | `2.41.5-0+deb13u1` | CVE-2026-76642, CVE-2026-78408, CVE-2026-78409, CVE-2026-78410 | Vulnerable in Trixie; fixes appear in newer unstable/Forky versions, not as a Trixie security fix |
| `acl` (`libacl1`) | `2.3.2-2+b1` | CVE-2026-54369 | Vulnerable in Trixie; tracker notes no DSA and a fix in `2.4.0-1` in unstable |
| `ncurses` (`libncursesw6`) | `6.5+20250216-2` | CVE-2025-69720 | Vulnerable in Trixie; tracker notes no DSA and a fix in a newer unstable version |
| `sqlite3` (`libsqlite3-0`) | `3.46.1-7+deb13u2` | CVE-2026-119373, CVE-2026-119374, CVE-2026-119379 | Trixie remains open/vulnerable in the tracker; newer `3.54.1` packages are shown fixed in Forky/Sid |
| `openssl` (`libssl3t64`) | `3.5.7-1~deb13u3` | CVE-2026-124709 | Trixie remains vulnerable; the tracker lists the issue as unfixed |
| `systemd` (`libsystemd0`) | `257.13-1~deb13u1` | CVE-2026-16742 | Trixie vulnerable; tracker marks the issue postponed/no DSA |
| `perl` (`perl-base`) | `5.40.1-6+deb13u1` | CVE-2026-9538 | Trixie vulnerable; tracker marks the issue postponed pending upstream regressions being resolved |

Primary Debian references:

- util-linux source tracker: https://security-tracker.debian.org/tracker/source-package/util-linux
- CVE-2026-76642: https://security-tracker.debian.org/tracker/CVE-2026-76642
- CVE-2026-54369: https://security-tracker.debian.org/tracker/CVE-2026-54369
- CVE-2025-69720: https://security-tracker.debian.org/tracker/CVE-2025-69720
- sqlite3 source tracker: https://security-tracker.debian.org/tracker/source-package/sqlite3
- CVE-2026-119373: https://security-tracker.debian.org/tracker/CVE-2026-119373
- CVE-2026-119374: https://security-tracker.debian.org/tracker/CVE-2026-119374
- CVE-2026-119379: https://security-tracker.debian.org/tracker/CVE-2026-119379
- openssl source tracker: https://security-tracker.debian.org/tracker/source-package/openssl
- CVE-2026-124709: https://security-tracker.debian.org/tracker/CVE-2026-124709
- systemd source tracker: https://security-tracker.debian.org/tracker/source-package/systemd
- CVE-2026-9538: https://security-tracker.debian.org/tracker/CVE-2026-9538

The tracker lists Trixie as vulnerable for the four util-linux CVEs while newer Forky/Sid versions are fixed; the acl and ncurses issues have no Trixie DSA and fixes in newer unstable versions; the three SQLite issues remain open for Trixie while newer 3.54.1 packages are fixed in Forky/Sid; OpenSSL CVE-2026-124709 remains unfixed for the installed Trixie security version; systemd and Perl issues are postponed in Trixie.

## 3. Dockerfile and build provenance observations

The reviewed remediation-branch Dockerfile pins:

- base image `python:3.11.18-slim-trixie` by digest `sha256:b701198cb708b68d9413ca67d6311bd97c9389a2c5fe4da0511fc652642366cd`;
- `zlib1g=1:1.3.dfsg+really1.3.1-1+deb13u1` by an explicit SHA-256 check;
- Python lockfile installation with `--only-binary=:all:` and `--require-hashes`;
- a non-root runtime user.

Run 35 image metadata reports Python 3.11.18 and Debian 13.7. The findings are in Debian OS packages; the separate Run 36 OSV inventory does not cover these OS packages. The pinned zlib package is not one of the 12 CVEs in this Trivy report. Its package provenance and compatibility remain separate questions; do not infer that pinning zlib resolves the other findings.

## 4. Disposition

1. Keep the container security gate OPEN.
2. Do not suppress the 12 CVEs or change Trivy's HIGH/CRITICAL threshold.
3. Do not import Forky/Sid packages into Debian Trixie.
4. Do not edit the Dockerfile until official Trixie package fixes are available and package provenance, ABI compatibility, and runtime impact have been reviewed.
5. Do not dismiss a package as irrelevant solely because a vulnerability requires a particular feature/configuration. Applicability needs a documented image/runtime attack-surface assessment.
6. After official Trixie updates become available, update only from supported Trixie repositories, record exact package versions and source provenance, rebuild the exact review commit, run the CLI smoke test, and re-scan. That future execution requires explicit authorization.
7. No workflow is authorized to run after the next documentation-only commit.

This report does not claim the image is exploitable in every deployment. It records unresolved scanner findings and Debian package status without dismissing them.
