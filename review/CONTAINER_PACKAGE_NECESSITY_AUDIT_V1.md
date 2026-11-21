# Container Package Necessity Audit V1

Status: ANALYSIS_ONLY
Target branch: review/type1-v4-remediation
Target image base:
python:3.11.18-slim-trixie

## Purpose

Determine whether each vulnerable OS package is required
by the final application runtime, can be removed safely,
or requires an upstream security fix.

This audit does not authorize Dockerfile changes,
workflow execution, vulnerability suppression,
or scientific execution.

## Scope

The audit covers the exact image findings previously
reported by Trivy for:

- util-linux
- sqlite3
- systemd
- acl
- ncurses
- perl

The zlib remediation is tracked separately and must
not be generalized to unrelated packages.

## Required evidence per package

1. Installed binary package names and versions.
2. Corresponding Debian source package and version.
3. Reverse dependencies in the installed image.
4. Files and shared libraries provided by the package.
5. Whether application code or runtime dependencies
   actually require those files.
6. Whether removal is technically possible.
7. Runtime and regression tests required after removal.
8. Trivy result against the exact rebuilt image digest.
9. Debian Security Tracker status at audit time.
10. Independent reviewer disposition.

## Decision categories

- REQUIRED_RUNTIME
- REQUIRED_BUILD_ONLY
- POTENTIALLY_REMOVABLE
- REMOVAL_TEST_REQUIRED
- UPSTREAM_FIX_REQUIRED
- ALTERNATIVE_BASE_CANDIDATE
- UNKNOWN

UNKNOWN must never be converted into NOT_REQUIRED
without direct evidence.

## Acceptance criteria

No package may be removed solely to reduce scanner findings.

A removal candidate must pass:

- dependency integrity checks
- Python runtime checks
- CLI smoke tests
- application regression tests
- non-root execution checks
- reproducibility checks
- exact-image vulnerability scanning

No finding may be suppressed or reclassified
without documented technical evidence.

## Authorization boundary

This document is analysis-only.

No Dockerfile modification, workflow dispatch,
image publication, or branch promotion is authorized
by this document.
