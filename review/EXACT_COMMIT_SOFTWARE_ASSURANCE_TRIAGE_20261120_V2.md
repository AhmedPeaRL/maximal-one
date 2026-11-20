# Exact-Commit Software Assurance Review Addendum
## 2026-11-20 — Run 44732932113

### 1. Exact identity

Repository: AhmedPeaRL/maximal-one

Branch: review/type1-v4-remediation

Exact scan commit:
1ed8e1aeccd9e9cd8cecf674d8bd07c28c0953f5

Workflow:
.github/workflows/replication.yml

Run:
44732932113

The GitHub run record confirms:
- head_branch = review/type1-v4-remediation
- head_sha = 1ed8e1aeccd9e9cd8cecf674d8bd07c28c0953f5
- workflow_definition_commit = 1ed8e1aeccd9e9cd8cecf674d8bd07c28c0953f5

### 2. Execution result

| Job | Result | Job ID |
|---|---|---|
| guard | success | 136277009229 |
| review-head | success | 136277042845 |
| refresh | skipped | 136277045280 |
| publish | skipped | 136277044834 |
| exact-assurance | failure | 136277109953 |
| nested OSV inventory | success | 136277110121 |

The assurance-only path did not execute dependency refresh or publishing.

GitHub resolved both same-repository reusable workflows at the exact target commit:
- software-assurance-exact-commit-v1.yml
- dependency-vulnerability-inventory.yml

### 3. Artifact identities

Exact assurance artifact:
14626344663

SHA-256:
abbae87cdfcde90f7dad6242bde3f489d5ce5cfa799ff4e3122ea01244d86711

OSV artifact:
14627126576

SHA-256:
01b44ef6fdfdd0c80f2c1e394144009be43827ee9a4f9a9dc0a46526c8cd93b4

### 4. Scanner results

#### actionlint 1.7.12

Result: NOT PASSED

Exit code: 123.

Exactly two diagnostics remain:
- replication.yml:428
- software-assurance-exact-commit-v1.yml:24

Both concern GitHub's same-repository $/ reusable workflow syntax.

The target configuration file exists, but its current ignore regex uses incorrect escaping. The workflow invocation also passes target files using paths outside the target worktree root, preventing the path-specific configuration from matching as intended.

Required remediation:
- retain the $/ references
- use \$ in the YAML single-quoted regex
- run actionlint from inside TARGET_DIR
- pass workflow paths relative to the target root
- explicitly load TARGET_DIR/.github/actionlint.yaml
- retain all unrelated actionlint checks

#### zizmor 1.30.1

Result: PASS

- exit code: 0
- zizmor.json: []
- no findings returned

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

The remaining pinned-dependency findings are:
- Dockerfile:1 — python:3.11.8-slim without digest
- Dockerfile:7 — npm install -g npm@10

No image digest is approved without a separate image-level vulnerability assessment.

The License score remains 9 despite canonical MIT text being present. This is retained as a scanner-recognition residual, not a reason to alter legal terms blindly.

Fuzzing remains an optional engineering gap, not a detected vulnerability.

#### OSV-Scanner 2.7.1

Result: PASS WITH LIMITED SCOPE

- exit code: 0
- results: []
- six supported manifests/lockfiles scanned
- five Python manifests reported 48 packages each
- package-lock.json reported zero packages

This scan does not establish that Docker base-image or operating-system packages are vulnerability-free.

### 5. Branch isolation

The current comparison reports:
- main HEAD: 9749de9253f144eeda9e1b60cb219cfc5f201ecc
- review branch: 675 commits ahead and 36 behind main
- branch state: diverged

No merge, cherry-pick, or rebase is authorized.

No change to main is authorized by this addendum.

### 6. Disabled workflows

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

This is recorded as owner attestation, not as an independently verified settings read.

### 7. Scientific and governance status

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

### 8. Independent human reviews

Four review tracks remain pending:
- Type-I statistical-methods review
- CI/CD security review
- climate-domain candidate review
- economic-domain candidate review

An out-of-office response was received for the economic-domain reviewer, indicating possible delays through November 29, 2026.

No attributable substantive review report is recorded in the checked correspondence as of this addendum.

### 9. Next execution boundary

No workflow is authorized until the next exact remediation commit has been reviewed.

After review, the only permitted workflow is:

.github/workflows/replication.yml

Target branch:
review/type1-v4-remediation

Required input:
assurance_only = true

Expected:
- guard: success
- review-head: success
- refresh: skipped
- publish: skipped
- exact-assurance: success
- OSV inventory: success

If assurance_only is absent or unchecked, cancel the run.

Do not manually run either reusable workflow.

No scientific workflow, calibration workflow, snapshot workflow, promotion workflow, dependency-refresh mode, or main-branch workflow is authorized by this addendum.
