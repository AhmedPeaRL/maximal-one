# Exact-Commit Software Assurance Review Addendum
## 2026-11-20 — Run 44748633865

### 1. Exact identity

Repository: AhmedPeaRL/maximal-one

Branch: review/type1-v4-remediation

Exact scan commit:
2f73e9f311248d5e61b9db0ecb1e1a27d1bae8c0

Workflow:
.github/workflows/replication.yml

Run:
44748633865

Workflow definition commit:
2f73e9f311248d5e61b9db0ecb1e1a27d1bae8c0

Event:
workflow_dispatch

Run conclusion:
success

The run record confirms that the scan target and workflow definition
were both associated with the exact commit above.

### 2. Execution result

| Job | Result | Job ID |
|---|---|---|
| guard | success | 136330404291 |
| review-head | success | 136330439691 |
| refresh | skipped | 136330442525 |
| publish | skipped | 136330442859 |
| exact-assurance | success | 136330500804 |
| nested OSV inventory | success | 136330501180 |

The observed execution path is consistent with assurance-only mode:

- review branch guard passed
- exact review HEAD verification passed
- dependency refresh was skipped
- publishing was skipped
- exact-commit software assurance completed
- nested OSV inventory completed

The raw run record does not expose the dispatched input value directly.
The job outcomes are retained as execution evidence.

### 3. Artifact identities

Exact assurance artifact:

ID: 14634895405

SHA-256:
8e0722f7ed29c556b52c4a83ecad40c0679404ac27570b3dee3446cd3af7e20e

OSV inventory artifact:

ID: 14633533528

SHA-256:
40a8e61b5fabbdb1a4348395467907789bb8ca45fa66c47058149f10f9f76891

Both archives were downloaded, extracted, and inspected.
Locally calculated archive SHA-256 values match GitHub artifact digests.

### 4. Scanner results

#### actionlint 1.7.12

Result: PASS

- exit code: 0
- actionlint.txt is empty

#### zizmor 1.30.1

Result: PASS

- exit code: 0
- zizmor.json = []
- no findings returned

The workflow invokes zizmor in offline mode.
This is not equivalent to every possible online-only audit.

The static scan examines workflow files regardless of whether
their corresponding workflows are enabled or disabled in GitHub settings.

#### OpenSSF Scorecard 5.6.0

Result: COMPLETED

Overall score: 9.1/10

- Binary-Artifacts: 10
- Dangerous-Workflow: 10
- Dependency-Update-Tool: 10
- Fuzzing: 0
- License: 9
- Packaging: 10
- Pinned-Dependencies: 9
- SAST: 10
- Security-Policy: 10
- Token-Permissions: 10
- Vulnerabilities: 10

Pinned dependency details:

- GitHub Actions: 211/211
- pip: 37/37
- npm: 6/7
- container images: 0/1

Open findings:

- Dockerfile:1 — python:3.11.8-slim is not digest-pinned.
- Dockerfile:7 — npm install -g npm@10 is not hash-pinned.
- apt-get installs nodejs and npm without explicit package-version pins.

The Scorecard-suggested image digest is not automatically approved.
A separate current image and vulnerability assessment is required.

The repository LICENSE file contains MIT License text.
Scorecard nevertheless reports that it did not recognize an FSF or OSI license.
This discrepancy remains open for scanner-recognition review.
Legal license terms must not be changed merely to improve the score.

Fuzzing score 0 indicates no detected fuzzer integration.
It is not a detected vulnerability.

Scorecard Vulnerabilities 10 does not establish that the Docker image
or operating-system packages are vulnerability-free.

#### OSV-Scanner 2.7.1

Result: PASS WITH LIMITED SCOPE

- exit code: 0
- results array = []
- six supported manifests/lockfiles scanned
- five Python manifests reported 48 packages each
- package-lock.json reported zero packages

This run found no findings in the supported manifests and lockfiles scanned.

It does not establish that Docker base-image or operating-system packages
are vulnerability-free.

The current workflow's JSON-validity test only checks whether the output
file is non-empty. It does not parse JSON or validate the results array.

A remediation is proposed in:
.github/workflows/dependency-vulnerability-inventory.yml

The OSV inventory workflow permits scanner exit code 1 as a findings result.
Therefore, a successful job alone must not be interpreted as zero findings.
The actual results JSON must be inspected.

### 5. Branch identity and isolation

Verified main HEAD:

9749de9253f144eeda9e1b60cb219cfc5f201ecc

Verified review branch HEAD:

2f73e9f311248d5e61b9db0ecb1e1a27d1bae8c0

Comparison:

- review branch ahead of main: 681 commits
- review branch behind main: 36 commits
- status: diverged

The comparison from the previous review commit
b402ea0eefaa41f55f7da079df126671c13726b9
to the current commit shows two added documentation/evidence files.

No merge, cherry-pick, or rebase is authorized.

No main modification is authorized.

### 6. Disabled workflows

The repository owner reports that the following twelve workflows
remain disabled in GitHub settings:

- Emergent Periodicity Analysis
- External Verification
- Reproducible Research Gate
- SOS Robustness Gate
- Build and Push Container
- Build and Publish Container
- Cross Run Memory Verification
- Immutable Release Lock
- Evolution Engine
- Canonical Sync
- Cross Architecture Timing Test
- Cross Architecture Timing

This remains owner attestation, not an independently verified
GitHub settings read.

No workflow is authorized for re-enablement by this report.

### 7. Zenodo metadata review

Record 18148140 was publicly accessible during this review.

Its public record page reports:

- DOI: 10.5281/zenodo.18148140
- title: Hybrid Consciousness Model (HCM): Presence Without Demand
- creator: Ahmed Salahuddin
- publication date: 2026-01-04
- version: v1
- license: CC BY 4.0
- file: HCM_Paper_01_Presence_Without_Demand.pdf

The title and filename match the Paper 01 identification.

However, the Zenodo file MD5 is:
a240e99737d9d29c44c7f2fc161ca8b1

The locally uploaded Paper 01 file MD5 is:
24a27ca6b33a0ada641c1f96ed50ab63

The local file SHA-256 is:
fb97104ce381683d9721657f3bdd6abe32ce9b2629043b9965826e388724dd29

The binary identity is therefore not established.
Do not claim that the local file is byte-identical to the Zenodo file.

The other nine supplied record exports could not be retrieved
through the available public browsing route during this review.
Their metadata remains unverified, not absent.

The canonical publication registry remains header-only.
No unverified DOI-to-paper mapping is authorized.

### 8. Independent human reviews

Four separate tracks remain pending:

- Type-I statistical-methods review
- CI/CD security review
- climate-domain candidate review
- economic-domain candidate review

No attributable substantive independent report is established
by the correspondence reviewed for this update.

These review tracks must remain separate.

### 9. Scientific and governance status

The exact assurance manifest records:

- protocol_freeze = NOT_FROZEN
- formal_calibration_authorized = false
- confirmatory_execution_authorized = false
- claim_support = false
- promotion_authority = false
- authority = NONE

This run is software assurance evidence only.

It is not:
- formal Type-I calibration
- confirmatory scientific execution
- independent replication
- scientific claim validation
- promotion authorization

### 10. Next execution boundary

No further workflow run is authorized immediately.

After the proposed OSV JSON-validation remediation and this documentation
are committed to review/type1-v4-remediation:

1. Inspect the exact new commit and complete diff.
2. Verify that main remains unchanged.
3. Verify that no disabled workflow was enabled.
4. Review actionlint and zizmor findings.
5. Only after explicit approval, manually dispatch:
   .github/workflows/replication.yml
   on review/type1-v4-remediation
   with assurance_only=true.
6. Confirm refresh and publish remain skipped.
7. Inspect the exact-assurance and OSV artifacts.

Do not manually dispatch nested reusable workflows.

Do not run scientific, calibration, confirmatory, snapshot,
or promotion workflows.

Do not run workflows on main.

No new scientific snapshot, freeze, claim support,
or promotion authority is granted by this addendum.
