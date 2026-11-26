# HCM Current Repository State Addendum — V26

- Evidence date: 2026-11-26
- Repository: `AhmedPeaRL/maximal-one`
- Review branch: `review/type1-v4-remediation`
- Exact assurance run: `45731020069`
- Exact run SHA: `66b5c30e94416523710f51886f3ae13e147c4796`
- Main SHA observed: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- Disposition: `REVIEW_ONLY / MAIN_FROZEN / PAT_REVOCATION_LOGGED / LOCK_INSTALL_AND_TESTS_VERIFIED / OSV_INVENTORY_ZERO_RESULTS_REPORTED / ZIZMOR_LOW_FINDINGS_OPEN / CONTAINER_SECURITY_OPEN / HOSTING_VERIFICATION_OPEN / HUMAN_REVIEW_PENDING / NOT_FROZEN / NO_SCIENTIFIC_AUTHORITY`

## 1. Evidence identity and branch separation

The exact assurance run `45731020069` was dispatched on:

- Branch: `review/type1-v4-remediation`
- Commit: `66b5c30e94416523710f51886f3ae13e147c4796`
- Event: `workflow_dispatch`
- Workflow: `.github/workflows/software-assurance-exact-commit-v1.yml`
- Run conclusion: `failure`

GitHub reported the run's exact `head_sha` as `66b5c30e94416523710f51886f3ae13e147c4796`.

GitHub reports the commit signature as verified. Its parent is `363a0f09ac1fc7b6d880c47c57a77fa9ad90cec4`.

The independently read Main SHA remains `9749de9253f144eeda9e1b60cb219cfc5f201ecc`.

Main remains frozen. No merge, rebase, cherry-pick, pull request, deployment, or Main-branch workflow execution is authorized.

This addendum does not authorize any scientific execution or promotion.

## 2. V25 temporal correction

The V25 file was committed at 2026-11-26 00:42:23 UTC.

The `EXTERNAL_SOURCE_URL` repository Actions variable was removed at 2026-11-26 00:44:14 +0200, and the corresponding GitHub Environment was deleted at 2026-11-26 00:44:28 +0200.

These events occurred after the V25 commit. V25 therefore remains an immutable historical snapshot and must not be overwritten.

The nine Environment deletions evidenced by the supplied Security Log records are:

1. `Production – ahmedpearl-maximal-one`
2. `Production – maximal-one`
3. `Preview – ahmedpearl-maximal-one`
4. `Preview – maximal-one`
5. `GH_REPO`
6. `github-pages`
7. `Personal Access Token`
8. `WITNESS_SIGNATURE`
9. `EXTERNAL_SOURCE_URL`

The repository Actions variable `EXTERNAL_SOURCE_URL` was also removed.

## 3. PAT and Actions secret evidence

Sanitized owner-supplied Security Log records establish:

- PAT `GH_TOKEN`, token ID `13474885`: `personal_access_token.destroy` and `personal_access_token.access_revoked`.
- PAT `WITNESS_SECRET`, token ID `13473352`: `personal_access_token.destroy` and `personal_access_token.access_revoked`.

Repository Actions secrets removed:

- `GH_TOKEN`
- `WITNESS_SECRET`
- `GH_REPO`

Repository Actions variables removed:

- `GH_TOKEN`
- `WITNESS_TOKEN`
- `GH_REPO`
- `EXTERNAL_SOURCE_URL`

The records also establish removal of the `WITNESS_SECRET` secret and variable from the `WITNESS_SIGNATURE` Environment before its deletion.

Classification: `GITHUB_PAT_DESTROY_AND_ACCESS_REVOCATION_LOGGED`.

These records establish logged GitHub events. They do not constitute an independent local invalid-token test or prove removal of environment variables from an external hosting provider.

OAuth events associated with Copilot Chat App and ChatGPT Codex Connector are separate from the two PATs and must not be classified as those PATs.

## 4. Exact assurance run results

Run `45731020069` completed with conclusion `failure`.

The latest attempt contained four jobs:

- `Validate exact Review target before scans`: success.
- `Verify exact Python dependency lock`: success.
- `OSV inventory for the exact target commit`: success.
- `Scan exact commit without promotion authority`: failure.

The preflight job successfully validated the Review branch and exact target identity before the scan jobs proceeded.

### 4.1 Dependency lock installation and project tests

The exact dependency-lock job successfully:

- Checked out commit `66b5c30e94416523710f51886f3ae13e147c4796`.
- Set up Python 3.11.15.
- Installed `requirements-lock.txt` using `--require-hashes` and `--only-binary=:all:`.
- Completed `pip check` with `No broken requirements found`.
- Completed all required import checks.
- Completed `compileall`.
- Ran 240 unit tests, ending with `OK`.

This is execution evidence for the exact run SHA. It is not scientific validation, independent replication, or proof of the runner's full isolation.

### 4.2 OSV dependency inventory

OSV-Scanner v2.7.1 was downloaded and its configured SHA-256 checksum verified before execution.

The recursive scan inspected six supported manifest/lockfile paths. The generated JSON was valid and contained an empty `results` array.

Interpretation: no OSV vulnerability results were reported for the scanned manifests in this run.

This does not establish container-image security, Debian package security, closure of Main's Dependabot alerts, or complete vulnerability coverage.

### 4.3 Static workflow assurance

The exact-commit scan reported:

- actionlint 1.7.12: exit code `0`, empty findings output.
- zizmor 1.30.1: exit code `12`, two `self-repository` findings, both Low severity and High confidence.
- OpenSSF Scorecard v5.6.0: exit code `0`, local score `9.2`.

The two zizmor findings relate to the local reusable-workflow reference and the replication-caller reference embedded in the exact-assurance workflow.

The next remediation is to:

- Replace the local reusable-workflow reference with GitHub's `$/` self-repository syntax.
- Remove the unused `workflow_call` entry point from the exact-assurance workflow.
- Remove the replication caller exception from the preflight and scan identity checks.
- Keep the exact-assurance workflow manually dispatchable only from the Review branch.

No finding suppression is authorized.

Scorecard's local output records `repo.commit` as `unknown`; its 9.2 score must not be treated as a complete remote repository assessment.

Scorecard also reports `contents: write` permissions in:

- `.github/workflows/canonical-sync.yml`
- `.github/workflows/cross-run-memory-verification.yml`
- `.github/workflows/replication.yml`

These write paths require separate review. The owner-attested disabled states of Canonical Sync and Cross Run Memory Verification are not independent live API verification.

## 5. Artifact identity and integrity

The run produced two artifacts.

### Exact assurance artifact

- Artifact ID: `15076178169`
- Name: `exact-commit-software-assurance-45731020069`
- Size: 6,699 bytes
- SHA-256: `2f1cf8135e1550bd3f67735369cee51e2e03c08629047b67199b5fe85277d8f1`

### OSV inventory artifact

- Artifact ID: `15076477884`
- Name: `osv-dependency-inventory-45731020069`
- Size: 1,272 bytes
- SHA-256: `07d6993c62cb67e393f10ebcbc03bea00ef638d1fef4871f486917fd5654f408`

Both ZIP files were downloaded and opened. Their locally computed SHA-256 digests match the artifact digests reported by GitHub.

Artifact contents are evidence for this run only. The failed exact-assurance job remains failed; artifact presence does not convert the run to success.

## 6. Workflow state and execution boundaries

The owner confirms that the following 13 workflow display names remain disabled:

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
- Validate Stress

These map to 12 workflow identities because the two container display names refer to the same `build-image.yml` workflow identity.

Classification: `OWNER_ATTESTATION_CURRENT / LIVE_API_STATE_NOT_INDEPENDENTLY_VERIFIED`.

The separate `replication.yml` workflow contains a manual dispatch path and a dependency-refresh/publishing path with write permissions. It is not authorized for dispatch and should remain disabled until redesigned and reviewed.

No scientific workflow is authorized.

## 7. Container and Debian status

No current Docker image build or current-SHA Trivy scan is available from this run.

The OSV result does not replace a container scan.

The Review Dockerfile's base-image digest, Debian Trixie package versions, zlib pin, and non-root execution remain subject to separate package inventory and container-security review.

The previously recorded Debian Trixie CVEs remain open until official Trixie package versions are verified as fixed and the exact image is rescanned. Do not suppress findings or mix Forky/Sid packages into Trixie.

A container scan requires separate approval for its exact SHA, workflow, runner, and inputs.

## 8. Hosting and API retirement

The Review API retirement state previously inspected includes static `410` responses with `Cache-Control: no-store` for the retired JavaScript endpoints.

Main still contains older dispatch-capable handlers in the corresponding API paths.

The public GitHub Pages URL could not be independently fetched during this review. The actual deployed branch, hosting-provider environment variables, and external route exposure remain unverified.

Deleting GitHub Environments and repository variables does not establish removal of external hosting-provider variables.

No deployment or service publication is authorized.

## 9. Independent human review

The four requested independent reports remain pending:

- Dimitris Politis
- Anil Machiry
- Annika Seppälä
- Benjamin Wong

Automated scans and AI review do not replace the requested independent human statistical review.

No formal calibration, confirmatory execution, independent replication, or scientific claim promotion is authorized.

## 10. Runner redesign

Runner isolation remains open.

Required evidence includes:

- Immutable source SHA binding.
- CPU, memory, process, and time limits.
- Explicit network-egress policy.
- No inherited credentials or token propagation.
- Hash-locked dependencies.
- Deterministic and independently verifiable artifacts.
- Separation of engineering reproducibility from scientific replication.

The successful GitHub-hosted runner jobs do not by themselves prove these isolation properties.

## 11. Required next actions

1. Preserve Main, V24, and V25 unchanged.
2. Add this V26 addendum on `review/type1-v4-remediation` only.
3. Correct `.github/workflows/software-assurance-exact-commit-v1.yml` to use the `$/` self-repository reference.
4. Remove `workflow_call` and all replication-caller exceptions from the exact-assurance workflow.
5. Keep the dependency inventory workflow reusable only; do not add a separate manual dispatch path to it.
6. Keep `replication.yml` disabled and unauthorized.
7. Verify `build-image.yml` is disabled immediately before any Review push because it has an unfiltered push trigger.
8. Recheck the 13 owner-attested workflow states before any future commit that could trigger them.
9. Re-read the next Review commit and all affected workflow definitions before separately authorizing one exact-assurance run.
10. For the next run, permit only `.github/workflows/software-assurance-exact-commit-v1.yml`, on `review/type1-v4-remediation`, with `scan_commit` equal to the selected branch SHA.
11. Do not run container, Trivy, replication, calibration, confirmatory, or scientific workflows without separate explicit authorization.
12. Continue external hosting verification, Debian Trixie tracking, runner redesign, and the four independent human reviews.

Final disposition:

`REVIEW_ONLY / MAIN_FROZEN / PAT_REVOCATION_LOGGED / LOCK_INSTALL_AND_TESTS_VERIFIED / OSV_INVENTORY_ZERO_RESULTS_REPORTED / ZIZMOR_LOW_FINDINGS_OPEN / CONTAINER_SECURITY_OPEN / HOSTING_VERIFICATION_OPEN / HUMAN_REVIEW_PENDING / NOT_FROZEN / NO_SCIENTIFIC_AUTHORITY`.
