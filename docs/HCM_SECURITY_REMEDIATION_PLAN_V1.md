# HCM Review-Branch Security Remediation Plan — V1

**Target repository:** `AhmedPeaRL/maximal-one`  
**Target branch:** `review/type1-v4-remediation`  
**Baseline commit observed:** `45b647ce2a6d2cbea1fe08e874be60b738f472c1`  
**Main branch policy:** frozen; no commits, merges, rebases, cherry-picks, or settings changes  
**Execution policy:** no workflow dispatch/re-run, no public deployment, no release/promotion

## 1. Objective and evidence standard

This plan seeks a defensible, bounded security assessment and remediation record. It does not promise mathematical proof that a repository is free of every vulnerability.

A finding may be closed only with evidence tied to an exact commit and a documented disposition:
- `FIXED_AND_RETESTED`
- `NOT_APPLICABLE_WITH_EVIDENCE`
- `ACCEPTED_WITH_OWNER_AND_EXPIRY`
- `OPEN`
- `BLOCKED_BY_PERMISSION_OR_TOOLING`

A scanner exit code of zero is not equivalent to zero findings, and zero findings in one scanner is not a security certification.

## 2. First operation: read-only inventory

Run `tools/hcm_readonly_github_audit.sh` from a trusted local shell with GitHub CLI authenticated for the repository. It issues GET requests only.

The inventory captures:
- authoritative Actions workflow states (`active`, `disabled_manually`, `disabled_inactivity`);
- Dependabot, code-scanning, and secret-scanning alert metadata;
- repository Actions permissions and workflow permissions;
- branch rulesets and Main branch protection where the token can read them;
- branch heads for Main and Review.

If an API collection is unavailable, forbidden, or disabled, record it as unknown. Never translate API access failure into an empty alert list or a verified disabled state.

The user-provided 13-workflow list must be reconciled against the API's actual `id`, `name`, and `path` values. Workflow filenames and YAML display names can differ. The final evidence register should include all three identifiers and the exact returned `state`.

## 3. Existing evidence — limitations

The previously reviewed V20 exact-commit software assurance run scanned `b3bf4c82132f686e872f0217a7a198ce71c91a8d`, not V21. It ran actionlint, zizmor, Scorecard, and OSV inventory. Scanner exit codes were zero, but the manifest explicitly required manual finding review. It is not a scan of the V21 commit.

The previously reviewed Trivy report was for older commit `48b223e8d5192ed133ba1f0e59493b6e36600950`. It recorded HIGH findings in Debian Trixie packages. It is not a scan of the current Review branch head.

The current Review Dockerfile pins a Python 3.11.18 slim Trixie base image and includes a zlib package pin/hash. This is not evidence that the complete OS package set is currently vulnerability-free.

The current `.github/dependabot.yml` configures monthly updates for pip, npm, Docker, and GitHub Actions. Configuration presence does not prove that Dependabot alerts/security updates are enabled or that all alert APIs are readable.

## 4. Required review domains

### 4.1 GitHub account/repository controls
- Dependabot alerts and security updates state.
- Code scanning availability and alert state.
- Secret scanning availability and alert state.
- Actions allowed-actions policy and default workflow token permissions.
- Branch protection/rulesets for Main and Review.
- Environment protection and deployment branch restrictions (manual UI/API evidence may be required).
- Repository visibility and collaborator permissions.

### 4.2 CI/CD supply-chain controls
- Pin third-party Actions to immutable full commit SHAs.
- Review every workflow's `permissions:` block and reduce to least privilege.
- Review `pull_request_target`, `workflow_run`, `repository_dispatch`, `workflow_dispatch`, reusable workflows, artifact trust, cache trust, and privileged contexts.
- Identify every `contents: write`, package publish, deployment, release, and secret-bearing job.
- Validate all reusable workflow `uses:` references. A local reusable workflow must use `./.github/workflows/<file>.yml`; malformed references must not be hidden by actionlint ignore rules.
- Review concurrency, timeouts, checkout credential persistence, untrusted expression interpolation, and artifact provenance.

### 4.3 Source and dependency security
- Scan every supported manifest/lockfile, including nested projects.
- Confirm the scanner actually recognized package counts; an empty package inventory is not proof of no vulnerabilities.
- Run static analysis and tests on an exact immutable commit.
- Review unsafe deserialization, shell/process invocation, path traversal, temporary files, archive extraction, network fetching, and untrusted inputs.
- Review Python dependency hashes and package provenance.
- Keep OS package scanning separate from language dependency scanning.

### 4.4 Container
- Rebuild only on explicit approval and only from the Review branch.
- Use Debian Trixie packages only; do not mix testing/unstable packages to suppress findings.
- Record base-image digest, package inventory, Trivy version/database timestamp, report hash, and exact source commit.
- Treat unresolved HIGH/CRITICAL findings as open unless a documented, evidence-based exception is approved.
- Do not publish to GHCR or deploy the image during this phase.

## 5. Immediate code observations to preserve

At the V1 baseline:
- `api/public_reproduce_endpoint.py` is a Python helper, not an HTTP route. Its previous implementation cloned a mutable branch, installed dependencies at request time, had no subprocess timeout/resource boundary, and expected a result file not produced by the called helper.
- `analysis/external_reproduction.py` fetched a fixed static JSON report and checked two fields. It did not execute the scientific pipeline or consume the request payload.
- `analysis/true_independent_reproduction.py` is materially closer to a clean-checkout computational replay: it requires `GITHUB_SHA`, checks out that SHA, rebuilds canonical inputs, runs the report generator, and compares normalized output. However, it uses the same repository implementation and same workflow runner; it explicitly sets implementation/laboratory/scientific independence to false. It must not be called independent scientific replication.
- `.github/workflows/software-assurance-exact-commit-v1.yml` contains local reusable workflow references written as `$/.github/workflows/...`; the valid GitHub syntax is `./.github/workflows/...`. The existing actionlint ignore rules suppress these malformed references. This should be corrected in a separate Review-only workflow patch, but not executed without explicit run approval.
- The same assurance workflow defines `run_container_review` under `workflow_call`, but not under `workflow_dispatch`. A manual dispatch therefore cannot explicitly select that container job as currently authored.

## 6. No-go conditions

Do not:
- modify Main;
- merge Review into Main;
- enable any of the 13 workflows;
- dispatch, rerun, or invoke any workflow;
- set `replication.yml` assurance-only mode to false;
- publish a container, package, release, report, or public reproduction service;
- perform calibration or confirmatory scientific execution;
- declare the protocol frozen or promote scientific claims.

## 7. Exit criteria for this security workstream

Security workstream may be described as `REVIEWED_WITH_RECORDED_RESIDUAL_RISK` only after:
1. workflow states are verified from the Actions API and reconciled by workflow ID/path;
2. all available security-alert collections have been retrieved and triaged;
3. unavailable collections/settings are separately documented;
4. every workflow and privileged job has a least-privilege review;
5. dependency and container scans are tied to the exact Review commit;
6. all findings have evidence-backed dispositions;
7. independent reviewer objections are reconciled.

No single scan or script can establish universal absence of vulnerabilities.
