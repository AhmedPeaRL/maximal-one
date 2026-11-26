# HCM Current Repository State Addendum — V25

- Evidence date: 2026-11-26
- Repository: `AhmedPeaRL/maximal-one`
- Review branch: `review/type1-v4-remediation`
- Evidence baseline SHA: `e4376f4ddd863eb13cbf2aa53b2c16656a1381d5`
- Main SHA: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- Disposition: `REVIEW_ONLY / MAIN_FROZEN / PAT_REVOCATION_LOGGED / HOSTING_VERIFICATION_OPEN / ACTIONS_POLICY_REMEDIATION_REQUIRED / CONTAINER_SECURITY_OPEN / HUMAN_REVIEW_PENDING / SCIENTIFIC_NO_GO`

## 1. Git identity

Read-only GitHub checks on 2026-11-26 returned:

- `main`: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- `review/type1-v4-remediation`: `e4376f4ddd863eb13cbf2aa53b2c16656a1381d5`
- Review comparison: 776 commits ahead and 36 behind Main.
- Merge base: `a9808bd999a7ad902daf15606272529ca9af4580`

Main remains frozen. No merge, rebase, cherry-pick, pull request, deployment, or Main-branch workflow execution is authorized.

The evidence baseline commit is signed and GitHub reports `verification.verified=true`. It changes only `.github/workflows/software-assurance-exact-commit-v1.yml` by three added lines binding the requested target SHA to the dispatch SHA.

## 2. PAT destruction and revocation evidence

Sanitized owner-supplied GitHub Security Log records establish:

- PAT `GH_TOKEN`, token ID `13474885`: `personal_access_token.destroy` and `personal_access_token.access_revoked`.
- PAT `WITNESS_SECRET`, token ID `13473352`: `personal_access_token.destroy` and `personal_access_token.access_revoked`.

Classification: `GITHUB_PAT_DESTROY_AND_ACCESS_REVOCATION_LOGGED`.

These records establish the logged destruction and access-revocation events. They do not constitute an independent local invalid-token test.

## 3. Repository secrets, variables, and environments

Security Log records establish removal of repository Actions secrets:

- `GH_TOKEN`
- `WITNESS_SECRET`
- `GH_REPO`

Repository Actions variables removed:

- `GH_TOKEN`
- `WITNESS_TOKEN`
- `GH_REPO`

The records also establish deletion of nine GitHub Environments:

- `Production – ahmedpearl-maximal-one`
- `Production – maximal-one`
- `Preview – ahmedpearl-maximal-one`
- `Preview – maximal-one`
- `GH_REPO`
- `github-pages`
- `Personal Access Token`
- `WITNESS_SIGNATURE`

The ninth deletion record is included in the source evidence set and must be retained with this addendum.

OAuth token events for the Copilot Chat App and ChatGPT Codex Connector are separate from the two PATs. They are not classified as PATs and are not to be revoked indiscriminately.

GitHub Environment deletion does not establish deletion of hosting-provider environment variables. External hosting configuration and deployed branch identity remain unverified.

## 4. Actions permissions

The supplied Security Log records:

- Allowed actions changed to local actions and workflows only.
- Default workflow token permission set to read.
- Workflow permission to create or approve pull requests set to false.

The latest workflow startup error lists external actions that are not allowed. The currently effective Actions settings were not independently retrieved through the available GitHub read interface.

The next remediation is to use selected actions with exact full-SHA allowlist entries for the required checkout, setup-python, and upload-artifact actions only. No wildcard or broad GitHub-owned/Marketplace permission is authorized. `aquasecurity/trivy-action` is intentionally excluded.

## 5. Workflow definitions and disabled-state evidence

A static inventory inspected 52 YAML workflow definitions at the Review evidence SHA, including trigger declarations and external action references.

The owner confirms that the 13 supplied workflow display names remain disabled. These map to 12 workflow identities because the Main and Review names for `build-image.yml` refer to the same workflow identity.

Classification: `OWNER_ATTESTATION_CURRENT / LIVE_API_STATE_NOT_INDEPENDENTLY_VERIFIED`.

The Review `build-image.yml` contains an unfiltered push trigger. Its disabled state must be checked manually immediately before any Review commit.

Other Review push-triggered workflows have path filters. The proposed exact-assurance workflow and this addendum must not modify their watched paths.

`replication.yml` contains a `contents: write` publishing path and remains unauthorized for dispatch. Disable it until that write path has been redesigned and reviewed.

## 6. Exact-assurance workflow runs

Three manual dispatch attempts on the exact Review SHA `e4376f4ddd863eb13cbf2aa53b2c16656a1381d5` were observed:

- Run `45714298146` — startup failure.
- Run `45714760647` — startup failure.
- Run `45718117700` — startup failure.

For Run `45718117700`:

- Workflow: `software-assurance-exact-commit-v1.yml`
- Branch: `review/type1-v4-remediation`
- Event: `workflow_dispatch`
- Conclusion: `startup_failure`
- Jobs: zero
- Artifacts: zero

No dependency installation, OSV scan, actionlint, zizmor, Scorecard, container build, or Trivy scan was executed by this run.

The action-policy mismatch is a likely startup blocker, but the precise cause is not independently established by a Check Suite diagnostic.

## 7. API route retirement

At the Review evidence SHA, the following routes return a static `410` response with `Cache-Control: no-store`:

- `api/reproduce.js`
- `api/challenge.js`
- `api/dispatch.js`
- `api/public_witness_endpoint.js`

The Review Python reproduction helper fails closed and performs no network, subprocess, or scientific-analysis operation.

The corresponding Main API files still contain dispatch-capable code. The actual deployed branch, hosting-provider environment variables, and external route exposure remain unknown. No deployment or complete hosting retirement is claimed.

## 8. Dependency and container evidence

The Review `requirements-lock.txt` contains:

- 48 uniquely pinned packages.
- 1,327 SHA-256 hash entries.
- No malformed SHA-256 entries in the structural check.

No authorized installation, `pip check`, import test, compileall, or unit-test run has been completed for this evidence SHA.

The Review Dockerfile pins the Python base image by digest, pins the `zlib1g` package version and SHA-256, installs with `--require-hashes`, and runs as a non-root user.

The latest preserved Trivy result remains historical and targets an older image/commit. No current image build or current-SHA Trivy scan is available.

Debian Trixie package remediation remains open. Do not suppress findings or mix Forky/Sid packages into Trixie. A future image scan must be separately authorized and bound to its exact commit.

## 9. Independent human review

The four requested reports remain pending:

- Dimitris Politis
- Anil Machiry
- Annika Seppälä
- Benjamin Wong

No new substantive inbound reviewer report was found in the inspected Gmail search. Benjamin Wong's known out-of-office response indicates possible delay through 2026-11-29.

Automated scans and AI review do not replace these independent human reports.

## 10. Runner redesign

Runner isolation remains open. Required evidence still includes:

- Immutable source SHA binding.
- CPU, memory, process, and time limits.
- Explicit network-egress policy.
- No inherited credentials or token propagation.
- Hash-locked dependencies.
- Deterministic and independently verifiable artifacts.
- Separation of engineering reproducibility from scientific replication.

The current GitHub-hosted runner workflow definitions do not by themselves prove these isolation properties.

## 11. Scientific governance

- Protocol freeze: `NOT_FROZEN`
- Formal calibration: `NOT_AUTHORIZED`
- Confirmatory execution: `NOT_AUTHORIZED`
- Independent replication: `NOT_AUTHORIZED`
- Scientific claim support: `NOT_ESTABLISHED`
- Promotion authority: `NONE`

No scientific workflow, new scientific snapshot, formal calibration, confirmatory execution, replication, or claim promotion is authorized by this addendum.

## 12. Required next actions

1. Preserve Main and all historical Library evidence unchanged.
2. Correct the Review exact-assurance workflow so target validation gates all scan jobs.
3. Remove the container child workflow reference from the software-assurance dispatch path.
4. Apply only the exact SHA allowlist entries required by the non-container assurance workflow.
5. Verify `build-image.yml` is disabled before any Review push.
6. Commit the workflow remediation and this addendum to Review only.
7. Re-read the resulting commit and workflow definitions before separately authorizing one exact-commit assurance run.
8. Verify external hosting configuration and deployment branch without publishing any new service.
9. Continue Debian Trixie tracking and await the four independent human reports.

Final disposition: `REVIEW_ONLY / MAIN_FROZEN / PAT_REVOCATION_LOGGED / HOSTING_VERIFICATION_OPEN / CONTAINER_SECURITY_OPEN / HUMAN_REVIEW_PENDING / NOT_FROZEN / NO_SCIENTIFIC_AUTHORITY`.
