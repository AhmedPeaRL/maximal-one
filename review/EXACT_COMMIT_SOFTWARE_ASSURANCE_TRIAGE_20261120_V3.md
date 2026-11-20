# Exact-Commit Software Assurance Review Addendum
## 2026-11-20 — Run 44743450399

### 1. Exact identity

Repository: AhmedPeaRL/maximal-one

Branch: review/type1-v4-remediation

Exact scan commit:
b402ea0eefaa41f55f7da079df126671c13726b9

Workflow:
.github/workflows/replication.yml

Run:
44743450399

Workflow definition commit:
b402ea0eefaa41f55f7da079df126671c13726b9

The GitHub run record confirms:
- event = workflow_dispatch
- head_branch = review/type1-v4-remediation
- head_sha = b402ea0eefaa41f55f7da079df126671c13726b9
- scan_commit = b402ea0eefaa41f55f7da079df126671c13726b9
- workflow_definition_commit = b402ea0eefaa41f55f7da079df126671c13726b9

### 2. Execution result

| Job | Result | Job ID |
|---|---|---|
| guard | success | 136312646214 |
| review-head | success | 136312687052 |
| refresh | skipped | 136312690052 |
| publish | skipped | 136312691157 |
| exact-assurance | success | 136312783536 |
| nested OSV inventory | success | 136312783873 |

The observed execution path is consistent with assurance-only mode:
- branch guard passed
- exact review HEAD identity passed
- dependency refresh was skipped
- publishing was skipped
- exact-commit assurance completed successfully
- nested OSV inventory completed successfully

The raw workflow run record does not expose the dispatched input value directly. The job outcomes are retained as execution evidence.

### 3. Artifact identities

Exact assurance artifact:
14631119425

Archive SHA-256:
910f42c8e6aa521abf40e3faa4d0c9eb24fd0b87beaa58e6dd960a1ec3fc8aad

OSV artifact:
14632316340

Archive SHA-256:
7e3943078b33664e0e099132c6193c17976abada3013bb8511718c24a9efbab5

Both archives were downloaded and inspected.

### 4. Scanner results

#### actionlint 1.7.12

Result: PASS

- exit code: 0
- actionlint.txt is empty
- previous two same-repository $/ compatibility diagnostics no longer appear

The remediation retains the GitHub $/ reusable-workflow references and uses:
- a narrow path-specific ignore configuration
- correctly escaped dollar-sign regex
- target-worktree-root execution
- workflow paths relative to the target root
- explicit target configuration path

This closes the previously observed actionlint compatibility diagnostics for this exact commit.

#### zizmor 1.30.1

Result: PASS

- exit code: 0
- zizmor.json = []
- no findings returned

This is a scan of workflow files in the target commit. It does not independently establish whether workflows are enabled or disabled in GitHub settings.

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

Remaining Scorecard pinned-dependency findings:
- Dockerfile:1 — python:3.11.8-slim is not digest-pinned
- Dockerfile:7 — npm install -g npm@10 is not hash-pinned

Manual Dockerfile review also observed that apt-get installs nodejs and npm without explicit package-version pinning.

No image digest is approved without a separate image-level vulnerability assessment.

Fuzzing score 0 is an integration gap, not a detected vulnerability.

License score 9 is retained as a scanner-recognition residual. Legal license terms must not be changed merely to improve the score.

#### OSV-Scanner 2.7.1

Result: PASS WITH LIMITED SCOPE

- exit code: 0
- results array = []
- six supported manifests/lockfiles scanned
- five Python manifests reported 48 packages each
- package-lock.json reported zero packages

This scan does not establish that Docker base-image or operating-system packages are vulnerability-free.

### 5. Branch isolation

Current GitHub branch comparison:

- main HEAD:
  9749de9253f144eeda9e1b60cb219cfc5f201ecc

- review branch HEAD:
  b402ea0eefaa41f55f7da079df126671c13726b9

- review branch ahead of main: 679 commits
- review branch behind main: 36 commits
- comparison status: diverged

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

A static zizmor scan of workflow files does not verify GitHub workflow enablement state.

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

### 8. Remaining engineering and security gaps

The following items remain open:

1. Container base image is not digest-pinned.
2. npm global installation is not hash-pinned.
3. apt-installed nodejs/npm package versions are not explicitly pinned.
4. Docker image and operating-system package vulnerability scanning has not been demonstrated by this run.
5. Scorecard Fuzzing remains 0 because no fuzzer integration was detected.
6. Scorecard License remains 9 despite the repository license file.
7. Zenodo DOI metadata has not yet been independently reconciled against the publication files.
8. Independent human reviews remain pending.

No open item is silently treated as closed by the successful workflow result.

### 9. Independent human reviews

Four separate review tracks remain pending:

- Type-I statistical-methods review
- CI/CD security review
- climate-domain candidate review
- economic-domain candidate review

No attributable substantive independent review report is recorded in the correspondence checked on 2026-11-20.

The economic-domain reviewer previously indicated possible delays through November 29, 2026.

### 10. Zenodo integration and DOI registry

A GitHub notification dated 2026-11-20 reports that the official Zenodo OAuth application was authorized with:

- admin:repo_hook
- read:org
- read:user
- user:email

These scopes are consistent with Zenodo's documented GitHub integration permissions.

The notification does not establish that the maximal-one repository is enabled for archiving in Zenodo.

The current publication registry remains header-only.

No DOI-to-paper mapping is approved until public record metadata is verified against the corresponding paper, version, authors, and license.

### 11. Next execution boundary

The assurance-only run on this exact commit succeeded.

No additional workflow run is required immediately.

For any subsequent code or workflow remediation:

- target branch must remain review/type1-v4-remediation
- inspect the exact new commit before execution
- only .github/workflows/replication.yml may be manually dispatched under the current authorization boundary
- assurance_only must be true
- refresh and publish must remain skipped
- do not manually run either nested reusable workflow
- do not run scientific, calibration, confirmatory, snapshot, or promotion workflows
- do not run workflows on main

A new image-security workflow, if later justified, must be separately designed, statically reviewed, committed only to the review branch, and explicitly authorized before execution.

No scientific authority or promotion authority is granted by this addendum.
