# Debian Trixie CVE status note — 2026-11-24

Scope: the 12 distinct CVEs in the latest preserved Trivy image report (run 44944152951). This is a source-package tracker status review, not a reachability or exploitability assessment for the HCM container.

| Source package | Representative installed Trixie version in Trivy inventory | CVEs in report | Trixie tracker status at review |
|---|---|---|---|
| util-linux | `2.41.5-0+deb13u1` (related binaries include epoch/revision variants) | CVE-2026-76642, CVE-2026-78408, CVE-2026-78409, CVE-2026-78410 | Vulnerable / no DSA noted for these entries |
| sqlite3 | `3.46.1-7+deb13u2` | CVE-2026-119373, CVE-2026-119374, CVE-2026-119379 | Vulnerable / no DSA (minor issue) |
| systemd | `257.13-1~deb13u1` | CVE-2026-16742 | Vulnerable / no DSA / postponed |
| openssl | `3.5.7-1~deb13u3` | CVE-2026-124709 | Vulnerable |
| acl | `2.3.2-2+b1` | CVE-2026-54369 | Vulnerable / no DSA |
| ncurses | `6.5+20250216-2` | CVE-2025-69720 | Vulnerable / no DSA (minor issue) |
| perl | `5.40.1-6+deb13u1` | CVE-2026-9538 | Vulnerable / postponed (minor issue) |

The Trivy artifact contains 50 HIGH package records, zero CRITICAL records, and 12 distinct CVEs. The 50 records are repeated package-level findings, not 50 unique vulnerabilities. The exact artifact ZIP SHA-256 is `657ba2a2f687611c3ea5643ec128ab2fc1badd3cf0783dd8acba645415f791d7`.

Official tracker pages checked:

- https://security-tracker.debian.org/tracker/source-package/util-linux
- https://security-tracker.debian.org/tracker/source-package/sqlite3
- https://security-tracker.debian.org/tracker/source-package/systemd
- https://security-tracker.debian.org/tracker/source-package/openssl
- https://security-tracker.debian.org/tracker/CVE-2026-54369
- https://security-tracker.debian.org/tracker/CVE-2025-69720
- https://security-tracker.debian.org/tracker/CVE-2026-9538

Do not install packages from Forky/Sid into a Trixie base. Do not suppress Trivy findings merely because they are difficult to patch in Trixie. The next remediation step is a package-level review of the exact image inventory: source package, binary package, installed version, package origin, whether the vulnerable component/code is present, runtime use, reverse dependencies, and any official Trixie fix or explicit Debian no-DSA/postponed disposition. If a fix is unavailable for Trixie, record the residual risk with an owner and review date; do not claim closure.

A new image build and Trivy scan must be bound to the new exact Review commit. No image build, workflow run, or Dockerfile edit is authorized by this note.
