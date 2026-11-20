# Exact-Commit Software Assurance Review Addendum
## 2026-11-20 — Run 44756664520

### 1. Exact identity

Repository: AhmedPeaRL/maximal-one

Branch: review/type1-v4-remediation

Exact commit:
157aa131af808a13ad12d2db0efe57870304f31b

Workflow:
.github/workflows/replication.yml

Run:
44756664520

Event:
workflow_dispatch

The review branch currently resolves to the exact commit above.

Main branch:
9749de9253f144eeda9e1b60cb219cfc5f201ecc

Comparison:
- review branch ahead of main: 684 commits
- review branch behind main: 36 commits
- status: diverged

No merge, cherry-pick, rebase, or main modification is authorized.

### 2. Workflow execution

Observed jobs:

| Job | Result | Job ID |
|---|---|---|
| guard | success | 136358077318 |
| review-head | success | 136358133240 |
| refresh | skipped | 136358134719 |
| publish | skipped | 136358137282 |
| exact-assurance | success | 136358198794 |
| nested OSV inventory | success | 136358198917 |

The observed execution path is consistent with assurance-only mode.

The raw dispatched input value is not independently established by the run record.
The observed skipped refresh and publish jobs are retained as execution evidence.

No dependency refresh or publish operation occurred in this run.

### 3. Artifact identity and integrity

Exact-commit assurance artifact:

ID: 14638386824

SHA-256:
2c49c438b7137784cf9af7fd52e8035fe75ce0b675999ffb91d9f69c816b3af3

OSV inventory artifact:

ID: 14638610504

SHA-256:
7ff96c7656e0d8d72419f711a5e739b39416c214adc8c5030216106778681e65

Both artifacts were downloaded and inspected.

Locally calculated archive SHA-256 values match the GitHub artifact digests.

### 4. Scanner results

#### actionlint 1.7.12

Result: PASS

- exit code: 0
- actionlint report is empty

#### zizmor 1.30.1

Result: PASS WITH SCOPE LIMITATION

- exit code: 0
- zizmor.json = []
- scan completed across the workflow files in the target tree
- execution was offline

Offline execution is not equivalent to every possible online-only audit.

Static scanning examines workflow files regardless of whether their corresponding workflows are enabled or disabled in GitHub settings.

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

Open residuals:

- Dockerfile:1 — python:3.11.8-slim is not digest-pinned.
- Dockerfile:7 — npm install -g npm@10 is not hash-pinned.
- apt-get installs nodejs and npm without explicit package-version pins.
- Fuzzing integration was not detected.
- Scorecard did not recognize the repository license file as an FSF/OSI license.

The Scorecard report metadata identifies its repository path as a temporary exact-target worktree but reports commit = unknown.

The assurance manifest independently records the exact target commit and workflow definition commit as 157aa131af808a13ad12d2db0efe57870304f31b.

This is a provenance limitation inside the Scorecard report itself, not evidence that a different commit was scanned.

Do not blindly apply the image digest suggested by Scorecard.
Select a current appropriate image, assess its vulnerabilities, and then pin the selected digest.

Do not change legal license terms merely to improve scanner recognition.

Fuzzing score 0 indicates missing integration, not a detected vulnerability.

Scorecard Vulnerabilities 10 does not establish that Docker base images or operating-system packages are vulnerability-free.

#### OSV-Scanner 2.7.1

Result: PASS WITH LIMITED SCOPE

- exit code: 0
- JSON validation: true
- top-level JSON object: valid
- results array: present
- results array: empty
- six supported manifests/lockfiles scanned
- five Python manifests reported 48 packages each
- package-lock.json reported zero packages

No findings were returned for the supported manifests and lockfiles scanned.

This does not establish that Docker base-image or operating-system packages are vulnerability-free.

### 5. OSV JSON-validation remediation

The commit modifies:

.github/workflows/dependency-vulnerability-inventory.yml

The previous non-empty-file test was replaced with actual JSON parsing.

The new validation requires:

- valid JSON syntax
- a top-level JSON object
- a results field whose value is an array

The previous fallback that wrote an artificial empty results array after invalid output was removed.

The new implementation was exercised in run 44756664520.

Observed evidence:

- osv-json-valid.txt = json_valid=true
- osv.exit_code = 0
- osv.json results = []

Status:
CLOSED_FOR_THIS_VALIDATION_DEFECT

This closes the identified JSON-validation defect in the inspected workflow implementation.
It does not close the broader dependency or container vulnerability review.

### 6. Docker and dependency residuals

The Dockerfile at this exact commit still contains:

FROM python:3.11.8-slim

RUN apt-get update && apt-get install -y nodejs npm

RUN npm install -g npm@10

These remain open engineering items.

Required future work:

1. Select a current Python base image.
2. Assess the selected image for vulnerabilities.
3. Pin the selected image by digest.
4. Review the provenance and version policy for nodejs and npm.
5. Replace floating npm@10 with a reproducible exact installation method.
6. Rebuild and test the image in an isolated review-branch workflow.
7. Preserve the old Dockerfile and evidence history in Git.

No Dockerfile modification is authorized by this addendum.

### 7. Branch isolation

The review branch currently resolves to:

157aa131af808a13ad12d2db0efe57870304f31b

Main currently resolves to:

9749de9253f144eeda9e1b60cb219cfc5f201ecc

The branch comparison reports:

- ahead: 684
- behind: 36
- status: diverged

No merge, cherry-pick, rebase, or main modification is authorized.

The current run was associated with the review branch and exact commit above.

The absence of recent main workflow runs remains owner-reported and was not independently established by this review.

### 8. Disabled workflows

The repository owner reports that the following twelve workflows remain disabled in GitHub settings:

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

This remains owner attestation, not an independently verified GitHub settings read.

No workflow is authorized for re-enablement by this report.

### 9. Zenodo metadata registry

The supplied archive:

HCM-Papers_Zenodo.zip

contains ten Zenodo JSON record exports.

Archive size:
32284 bytes

Archive SHA-256:
4fc8cf32cdc92057b3bf082fe20648091a36bcfcb7f111cdefae0787bc5d649c

All ten exports report:

- is_published = true
- status = published
- creator = Ahmed Salahuddin
- license = CC BY 4.0
- version index = 1

The exports provide version DOI, parent/concept DOI, title, publication date, PDF filename, file size, and Zenodo MD5.

These metadata are suitable for a provisional DOI registry entry, with source provenance and binary-verification limits preserved.

The local uploaded PDFs for Papers 01, 08, and 10 do not match the Zenodo-export MD5 values.

Therefore:

- Do not claim byte identity for those local PDFs.
- Do not place local PDF SHA-256 values in the published-file SHA-256 field.
- Keep the SHA-256 field empty until the exact published PDF bytes are obtained and hashed.
- Treat repository Markdown manuscript paths as source-document associations, not as binary-equivalent Zenodo PDFs.

Paper 04 has a title mismatch between the Zenodo export and the numbered repository Markdown manuscript.

Papers 07 and 09 have identical Zenodo titles and require separate record-to-manuscript review.

The registry must preserve these distinctions.

### 10. Human independent reviews

Four separate review tracks remain pending:

1. Type-I statistical-methods review.
2. CI/CD security review.
3. Climate-domain candidate review.
4. Economic-domain candidate review.

These are separate scopes and must not be merged into one generic review status.

No substantive independent report is established by this update.

### 11. Scientific and governance authority

The exact-assurance manifest records:

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
- independent scientific replication
- scientific claim validation
- protocol freeze
- promotion authorization

No new scientific snapshot is authorized by this addendum.

### 12. Next execution boundary

No workflow run is authorized immediately.

After the V5 documentation and DOI registry update are committed to:

review/type1-v4-remediation

the exact diff and branch identity must be reviewed.

If the resulting commit contains only documentation, registry, and evidence-archive changes, the only candidate workflow for a later software-assurance refresh is:

.github/workflows/replication.yml

Target branch:

review/type1-v4-remediation

Required input:

assurance_only=true

This workflow may be manually dispatched only after explicit approval following review of the new commit.

Do not manually dispatch nested reusable workflows.

Do not run scientific, calibration, confirmatory, snapshot, or promotion workflows.

Do not run workflows on main.

No scientific snapshot, freeze, claim support, or promotion authority is granted by this addendum.
