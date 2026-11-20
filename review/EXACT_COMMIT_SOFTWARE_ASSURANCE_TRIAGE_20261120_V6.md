# Exact-Commit Software Assurance Review Addendum
## 2026-11-20 — Run 44763200012

### 1. Exact identity

Repository: `AhmedPeaRL/maximal-one`

Branch: `review/type1-v4-remediation`

Exact target commit:

`337f5267585fc551d104131b755387b49e91408f`

Workflow:

`.github/workflows/replication.yml`

Run ID: `44763200012`

Event: `workflow_dispatch`

The exact-assurance manifest records both `scan_commit` and `workflow_definition_commit` as the exact target commit above.

Main HEAD observed during review:

`9749de9253f144eeda9e1b60cb219cfc5f201ecc`

Review branch comparison:

- ahead of main: 688 commits
- behind main: 36 commits
- status: diverged

The comparison from `157aa131af808a13ad12d2db0efe57870304f31b` to this target contains four commits. The changes include the V5 triage report, V5 residual register, Zenodo publication registry update, and Zenodo export archive.

No merge, rebase, cherry-pick, or main modification is authorized.

### 2. Workflow execution

Observed jobs:

| Job | Result | Job ID |
|---|---|---|
| guard | success | 136380860744 |
| review-head | success | 136380916758 |
| refresh | skipped | 136380919920 |
| publish | skipped | 136380920599 |
| exact-assurance | success | 136381045239 |
| nested OSV inventory | success | 136381045494 |

The observed execution path is consistent with assurance-only mode.

The raw dispatched input value is not independently established by the available run record. The skipped refresh and publish jobs are retained as execution evidence.

No dependency refresh or publish operation occurred in this run.

### 3. Artifact identity and integrity

Exact-commit assurance artifact:

ID: `14642347571`

Size: 5969 bytes

Locally calculated ZIP SHA-256:

`8bb842a421d7487a58c8f52ebd6ab0954659a124d352573a70b911a001c19d24`

OSV inventory artifact:

ID: `14642372373`

Size: 1271 bytes

Locally calculated ZIP SHA-256:

`939ef68073cd65f8fc787acf9b025e182f53e75cab4881f608253e9e60dfeee8`

Both downloaded ZIP archives were opened and their contents inspected.

These hashes identify the downloaded ZIP files in this review.

### 4. Scanner results

#### actionlint 1.7.12

- exit code: 0
- report file empty

#### zizmor 1.30.1

- exit code: 0
- JSON findings: `[]`
- offline execution
- workflow files were scanned regardless of GitHub enabled/disabled settings

Offline execution does not establish every possible online-only check.

#### OpenSSF Scorecard 5.6.0

- exit code: 0
- overall score: 9.1/10

Reported scores:

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

- Dockerfile base image is not digest-pinned.
- npm global installation is not hash-pinned.
- Fuzzing integration was not detected.
- Scorecard did not recognize the license file as an FSF/OSI license.
- Token-Permissions details report job-level `contents: write` in canonical-sync, cross-run-memory-verification, and replication publish path.
- Scorecard report metadata identifies a temporary local worktree and reports commit as `unknown`.

The exact-assurance manifest separately records the target commit and workflow definition commit. This does not erase the Scorecard report-level provenance limitation.

Do not blindly apply the digest suggested by Scorecard. Verify the selected image, its provenance, platform, and vulnerabilities before pinning it.

Do not alter legal license terms merely to improve scanner recognition.

### 5. OSV dependency inventory

OSV-Scanner version: 2.7.1

Exit code: 0

JSON validation: `json_valid=true`

The JSON output is a top-level object with a `results` array. The array is empty.

Six supported manifests/lockfiles were scanned:

- five Python manifests, each reporting 48 packages
- `package-lock.json`, reporting zero packages

No findings were returned for the supported manifests and lockfiles scanned.

This does not establish that Docker base-image layers or operating-system packages are vulnerability-free.

### 6. Docker and dependency residuals

The Dockerfile still contains:

- `FROM python:3.11.8-slim`
- apt installation of `nodejs` and `npm` without explicit version pins
- `npm install -g npm@10`

These remain open engineering items.

Required future work:

1. Establish the runtime Python requirement.
2. Establish the compatible Node.js and npm versions.
3. Select a current official base image and verify its provenance.
4. Assess the selected image for vulnerabilities.
5. Pin the selected image by digest.
6. Replace floating package installation with a reproducible version policy.
7. Rebuild and test in an isolated review-branch workflow.
8. Preserve the previous Dockerfile and all historical evidence.

No Dockerfile modification is authorized by this addendum.

### 7. Workflow write permissions

Scorecard details report write permissions in:

- `.github/workflows/canonical-sync.yml`
- `.github/workflows/cross-run-memory-verification.yml`
- `.github/workflows/replication.yml`

The first two contain review-branch write paths. The replication workflow contains a publish job with `contents: write`.

The owner reports that the twelve designated workflows remain disabled. This is owner attestation, not an independently verified settings read.

No workflow is authorized for re-enablement.

### 8. Zenodo archive and publication registry

The review branch contains:

`evidence/HCM-Papers_Zenodo.zip`

The archive was previously inspected as ten Zenodo JSON record exports.

Archive SHA-256 from the supplied original upload:

`4fc8cf32cdc92057b3bf082fe20648091a36bcfcb7f111cdefae0787bc5d649c`

The publication registry is present at:

`docs/publications/HCM_ZENODO_PUBLICATIONS.csv`

Known unresolved metadata/binary issues remain:

- Local PDFs for Papers 01, 08, and 10 do not match the Zenodo-export MD5 values.
- Paper 04 has an unresolved title/manuscript association mismatch.
- Papers 07 and 09 share a Zenodo title and require separate record-to-manuscript review.
- Published PDF SHA-256 values remain unverified and must not be populated using non-identical local PDFs.

The uploaded Zenodo JSON exports support metadata review, not automatic proof of binary identity for the published PDFs.

### 9. Scientific and governance authority

The exact-assurance manifest records:

- protocol_freeze = `NOT_FROZEN`
- formal_calibration_authorized = `false`
- confirmatory_execution_authorized = `false`
- claim_support = `false`
- promotion_authority = `false`
- authority = `NONE`

This run is software-assurance evidence only.

It is not formal Type-I calibration, confirmatory scientific execution, independent scientific replication, scientific claim validation, protocol freeze, or promotion authorization.

No new scientific snapshot is authorized by this addendum.

### 10. Human independent reviews

The four independent review tracks remain pending unless and until substantive reports are received and independently assessed:

1. Type-I statistical methods.
2. CI/CD security.
3. Climate-domain review.
4. Economic-domain review.

These scopes remain separate.

### 11. Next execution boundary

No further workflow run is authorized immediately.

The next engineering task is a review-only Docker and container dependency remediation design. It must be based on verified runtime requirements, official image provenance, and a reproducible package-version policy.

After the remediation commit is created on:

`review/type1-v4-remediation`

the exact diff and branch identity must be reviewed before another workflow run.

If the resulting commit is approved for software assurance, the only candidate orchestrator is:

`.github/workflows/replication.yml`

Target branch:

`review/type1-v4-remediation`

Required input:

`assurance_only=true`

Do not manually dispatch nested reusable workflows.

Do not run scientific, calibration, confirmatory, snapshot, or promotion workflows.

Do not run workflows on `main`.

No scientific snapshot, freeze, claim support, or promotion authority is granted by this addendum.
