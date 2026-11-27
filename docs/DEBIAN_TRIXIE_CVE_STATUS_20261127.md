# Debian Trixie CVE Status — 2026-11-27

## Scope and limitation

This note updates the Debian Security Tracker status for the twelve distinct CVEs in the preserved historical Trivy report (50 HIGH package-level records, zero CRITICAL records). That report is bound to an older image/commit, not the current Review HEAD `c8985c4bfcb6140dbfd081a4eb2faab29fb561af`. No current-image `dpkg-query -W` inventory or exact image digest is available in this evidence set. Therefore, this is a tracker-status update, not a current-image vulnerability determination or exploitability assessment.

## Current Trixie tracker status

| Source package | Historical reported Trixie package version | CVEs | Current tracker status for Trixie |
|---|---|---|---|
| util-linux | `2.41.5-0+deb13u1` | CVE-2026-76642, CVE-2026-78408, CVE-2026-78409, CVE-2026-78410 | Vulnerable; no DSA noted for the listed issues. Fixes shown in Forky/Sid do not establish a Trixie fix. |
| sqlite3 | `3.46.1-7+deb13u2` | CVE-2026-119373, CVE-2026-119374, CVE-2026-119379 | Vulnerable; no DSA noted. Tracker shows fixed versions in Forky/Sid, not Trixie. |
| systemd | `257.13-1~deb13u1` | CVE-2026-16742 | Vulnerable; no DSA noted for Trixie. |
| openssl | `3.5.7-1~deb13u3` | CVE-2026-124709 | Vulnerable and postponed for a future update in Trixie. A newer tracker-listed Trixie source version is not evidence that this CVE is fixed. |
| acl | `2.3.2-2+b1` | CVE-2026-54369 | Vulnerable; no DSA. Tracker notes a fix in unstable/Forky and that the ABI change is not to be backported as an individual patch. |
| ncurses | `6.5+20250216-2` | CVE-2025-69720 | Vulnerable; no DSA (minor issue). |
| perl | `5.40.1-6+deb13u1` | CVE-2026-9538 | Vulnerable and postponed (minor issue). |

## Official Debian tracker references

- https://security-tracker.debian.org/tracker/source-package/util-linux
- https://security-tracker.debian.org/tracker/source-package/sqlite3
- https://security-tracker.debian.org/tracker/source-package/systemd
- https://security-tracker.debian.org/tracker/source-package/openssl
- https://security-tracker.debian.org/tracker/CVE-2026-54369
- https://security-tracker.debian.org/tracker/CVE-2025-69720
- https://security-tracker.debian.org/tracker/CVE-2026-9538

## Required closure evidence

1. Build the exact reviewed Review commit only after a separate authorization.
2. Record the immutable image digest and complete `dpkg-query -W` output, including binary package, version, architecture, and source package where available.
3. Map each Trivy finding to the exact installed binary/source package and version. Record scanner version, vulnerability database timestamp, complete JSON, and artifact SHA-256.
4. Recheck the official Debian Security Tracker for the exact installed Trixie source versions and any official DSA/point-release fix.
5. Verify package provenance, whether affected code is present/reachable, runtime use, reverse dependencies, and compatibility before proposing a Trixie-only fix.
6. Do not mix Forky/Sid packages into Trixie, suppress findings, or infer closure from package-name matches alone. If no Trixie fix exists, preserve the finding as residual risk with owner and review date.

No image build, Dockerfile edit, Trivy scan, publication, or deployment is authorized by this note.
