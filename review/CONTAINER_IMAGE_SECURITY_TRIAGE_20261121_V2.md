# Container Image Security Triage — 2026-11-21 V2

## Identity

- Repository: AhmedPeaRL/maximal-one
- Branch: review/type1-v4-remediation
- Current branch commit before this remediation: 3a3d381a5bf5a74f8f7c08aae8d6b467f5d8288f
- Dockerfile remediation commit: a1e6c2c96e5365eaa8bd449c2731c79bdde12068
- Workflow run: 44820794670
- Workflow: .github/workflows/software-assurance-exact-commit-v1.yml
- Disposition: REVIEW ONLY — CONTAINER BUILD FAILED BEFORE IMAGE SCANNING

## Workflow results

- Exact Commit Software Assurance: PASS
- OSV Dependency Inventory: PASS
- Container Review Guard: PASS
- Container Build / CLI / Trivy: FAILURE

## Software assurance evidence

- actionlint 1.7.12: exit code 0
- zizmor 1.30.1: exit code 0
- OpenSSF Scorecard 5.6.0: exit code 0
- Scorecard aggregate score: 9.2
- OSV-Scanner 2.7.1: exit code 0
- OSV JSON validation: PASS
- OSV results array: empty
- Six supported source manifests or lockfiles scanned

These results do not establish that operating-system packages in the container image are vulnerability-free.

## Container build failure

The container build failed during the zlib package checksum verification step.

APT successfully downloaded:

zlib1g=1:1.3.dfsg+really1.3.1-1+deb13u1

The actual downloaded filename was:

zlib1g_1%3a1.3.dfsg+really1.3.1-1+deb13u1_amd64.deb

The Dockerfile expected a filename containing a literal colon rather than the percent-encoded epoch separator.

Consequently, sha256sum could not open the expected filename and the Docker build stopped.

- CLI smoke test: NOT EXECUTED
- Trivy image scan: NOT EXECUTED
- New image vulnerability report: NOT PRODUCED
- zlib CVE closure: NOT ESTABLISHED

## Corrective action

The next Dockerfile revision discovers the downloaded zlib package filename rather than assuming its encoded representation.

The package remains pinned to:

1:1.3.dfsg+really1.3.1-1+deb13u1

The SHA-256 verification remains mandatory:

8c27c342230503b73dfde629642c3b352e87b554e06d60cf58772f236a305ceb

The installed package version must be verified after dpkg installation.

## Previous vulnerability baseline

The previous successful container build and Trivy scan reported:

- HIGH instances: 48
- CRITICAL instances: 0
- Distinct CVEs: 12
- Affected OS packages: 19

These figures are historical baseline evidence only. The current run did not produce a new image scan and therefore does not establish the current vulnerability count.

## Governance

- main remains unchanged.
- review/type1-v4-remediation remains isolated.
- No merge, rebase, or cherry-pick is authorized.
- No publishing workflow is authorized.
- No scientific snapshot is authorized.
- Protocol freeze: NOT_FROZEN.
- Formal calibration: NOT_AUTHORIZED.
- Confirmatory execution: NOT_AUTHORIZED.
- Scientific claim support: NONE.
- Promotion authority: NONE.

This document records software-assurance and container-build evidence only.
