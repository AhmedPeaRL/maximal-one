# Container Image Security Triage — 2026-11-20

## Identity

- Repository: AhmedPeaRL/maximal-one
- Branch: review/type1-v4-remediation
- Scanned commit: 0fe95249512619b982065b8a076cee8e8fa9a110
- Workflow run: 44817344061
- Workflow: .github/workflows/software-assurance-exact-commit-v1.yml
- Disposition: REVIEW ONLY — CONTAINER SECURITY GATE FAILED

## Container evidence

- Python: 3.11.18
- Base: python:3.11.18-slim-trixie
- Base digest: sha256:b701198cb708b68d9413ca67d6311bd97c9389a2c5fe4da0511fc652642366cd
- Detected OS: Debian 13.7
- Runtime user: non-root
- Docker build: PASS
- CLI smoke test: PASS
- Python version assertion: PASS
- Trivy: v0.76.2

## Trivy findings

- HIGH instances: 48
- CRITICAL instances: 0
- Distinct CVE identifiers: 12
- Affected OS packages: 19
- Findings with a fixed version listed: 1
- Findings without a fixed version listed: 47
- Python and Node language-package findings: 0

The 12 CVE identifiers are:

CVE-2025-69720
CVE-2026-119373
CVE-2026-119374
CVE-2026-119379
CVE-2026-16742
CVE-2026-54369
CVE-2026-76642
CVE-2026-78408
CVE-2026-78409
CVE-2026-78410
CVE-2026-85091
CVE-2026-9538

The Trivy gate remains failed. No finding is closed by this document.

## Component-scope observations

- The installed-file inventory contains libsystemd0 and libudev1, but no systemd-homed executable was found. CVE-2026-16742 remains open pending component-level adjudication.
- The installed-file inventory for perl-base did not contain Archive/Tar. CVE-2026-9538 remains open pending component-level adjudication.
- infocmp, nsenter, and mount executables are present in the image inventory.
- These observations are not automatic false-positive decisions.

## OSV inventory

- OSV-Scanner: 2.7.1
- Exit code: 0
- JSON validation: PASS
- Results array: empty
- Six supported manifests or lockfiles scanned.

This result covers the supported source manifests and lockfiles only. It does not establish that operating-system packages in the container image are vulnerability-free.

## Artifact identity

- Assurance artifact: 14670092233
- Assurance ZIP SHA-256:
  f58590be337acc2658f18038dddf36951ddd174906b5c20dc5b385fa65da4b11

- OSV artifact: 14669414343
- OSV ZIP SHA-256:
  1593e32116a21a593a6d3d77b66f0e7aaf465558bd7e9dafb680a8535f866ff4

- Trivy artifact: 14669269599
- Trivy ZIP SHA-256:
  4b3a828989e67aa85bf09e81217da98bf78103e9f7d55fd5afcd6bc4721563ee

## Remediation disposition

The Debian Trixie security update for zlib1g is available at:

1:1.3.dfsg+really1.3.1-1+deb13u1

The package SHA-256 is:

8c27c342230503b73dfde629642c3b352e87b554e06d60cf58772f236a305ceb

The next Dockerfile remediation pins and verifies this package.

The remaining findings require individual component and package review. Do not mix Debian testing packages into the stable image merely to reduce scanner counts. Do not suppress findings using ignore-unfixed or a blanket ignore file.

## Governance

- main remains unchanged.
- review/type1-v4-remediation remains isolated.
- No merge, rebase, or cherry-pick is authorized.
- No new scientific snapshot is authorized.
- Protocol freeze: NOT_FROZEN.
- Formal calibration: NOT_AUTHORIZED.
- Confirmatory execution: NOT_AUTHORIZED.
- Scientific claim support: NONE.
- Promotion authority: NONE.

This document records software-assurance evidence only.
