# HCM Current Repository State Addendum — V28

- Evidence date: 2026-11-26
- Repository: `AhmedPeaRL/maximal-one`
- Review branch: `review/type1-v4-remediation`
- Main HEAD: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- Review HEAD: `35943a7d3b2677280d27fa283d4b7c106e2cec81`
- V26 commit: `a46992ead14e07adfabb275105f746ead0510f92`
- V27 commit: `346233258be95734525dddf69e0032506d4f77aa`
- Prior exact-assurance run: `45731020069`, target `66b5c30e94416523710f51886f3ae13e147c4796`

## 1. Scope and branch identity

Read-only inspection only. No repository write, commit, workflow dispatch/rerun, deployment, or settings change was performed.

The Review ref resolves to `35943a7d3b2677280d27fa283d4b7c106e2cec81`. Main remains at `9749de9253f144eeda9e1b60cb219cfc5f201ecc`.

Comparison from V26 to current Review reports five commits ahead, zero behind. The five commits are:
1. `53c0276a5c9b186ce2d502a4aa8a65bca3ab6bba` — exact-assurance refactor.
2. `d7c6e5897ec64e7df7096a8eef15fb97f827696c` — remove unused `WORKFLOW_REF`.
3. `a8d4c54ffcff043b61b44a833d64b78415d6e517` — remove `review-head` and `exact-assurance` jobs from `replication.yml`.
4. `346233258be95734525dddf69e0032506d4f77aa` — add V27.
5. `35943a7d3b2677280d27fa283d4b7c106e2cec81` — change the `assurance_only` input description.

Preserve V24–V27 unchanged. V28 corrects stale statements in V27; it does not rewrite V27.

## 2. V27 accuracy correction

V27 was added after commits `d7c6e589...` and `a8d4c54...` had already removed the unused environment variables and obsolete jobs. Therefore, V27's claims that `WORKFLOW_REF`, `review-head`, and `exact-assurance` remained were stale when V27 was added.

V27 also says the exact-assurance workflow exists on Review but not Main. That is incorrect: the same path exists on Main with an older definition. The Main copy has a stale default `scan_commit` (`3a158e8f902179cdd543e92153032ae409faaea0`) and lacks the current Review-specific exact-SHA guard. Do not run the Main copy.

## 3. Current Review workflow inspection

### Exact Commit Software Assurance

`.github/workflows/software-assurance-exact-commit-v1.yml` on Review:

- `workflow_dispatch` only; no `workflow_call`.
- Global permission `contents: read`.
- Requires `refs/heads/review/type1-v4-remediation`.
- Requires the supplied 40-character `scan_commit` to equal `GITHUB_SHA`.
- Checks checkout identity against the requested SHA.
- Uses `$/` for the reusable OSV inventory workflow.
- No `WORKFLOW_REF` remains.
- Jobs: preflight, OSV inventory, dependency-lock verification, exact-commit scan.
- Does not call the container CLI/Trivy child and does not perform a container scan.

This is the only candidate for a future, separately authorized Review-only engineering-assurance run. It is not authorized to run now.

### Dependency Refresh workflow

`.github/workflows/replication.yml` on Review:

- Manual `workflow_dispatch` only.
- `review-head` and `exact-assurance` jobs are absent.
- Dependency refresh and a `contents: write` publish job remain.
- `refresh` and `publish` are gated by `!inputs.assurance_only`; the default is `true`.
- With `assurance_only=true`, the guard runs but refresh and publish are skipped. It does not run Exact Commit Software Assurance.
- The current description `Read-only assurance mode.` is misleading.

Required description:

`When true, skip dependency refresh and publishing; this workflow does not run Exact Commit Software Assurance.`

Keep this workflow disabled. Do not dispatch it or set `assurance_only=false`.

### Other workflow definitions

- Review `build-image.yml` has unfiltered `push:` and `pull_request` triggers; its Main-only publishing job has `packages: write`.
- Review `container-cli-smoke-review.yml` is `workflow_call` only and contains Trivy.
- Review `dependency-vulnerability-inventory.yml` is `workflow_call` only and is called by the exact-assurance parent.
- Main `build-image.yml` has `push` and `pull_request` triggers.
- Main `replication.yml` remains the older `Cross-Architecture Replication` workflow with `workflow_dispatch`.

No workflow was dispatched.

## 4. Manual dispatch branch-selection correction

The exact-assurance path exists on both Main and Review. GitHub's `workflow_dispatch` prerequisite is therefore satisfied because the workflow exists on the default branch. In the Actions UI, a future authorized run can select `review/type1-v4-remediation` in the branch selector and provide the exact full Review HEAD SHA. Never select Main for this task.

This is not permission to dispatch. Separate authorization must identify the exact workflow path, branch, full SHA, and inputs after read-only review.

## 5. Workflow disablement evidence

The owner attests that these 14 display names remain disabled:

1. Emergent Periodicity Analysis
2. External Verification
3. Reproducible Research Gate
4. SOS Robustness Gate
5. Build and Push Container — Main
6. Build and Publish Container — Review
7. Cross Run Memory Verification
8. Immutable Release Lock
9. Evolution Engine
10. Canonical Sync
11. Cross Architecture Timing Test
12. Cross Architecture Timing
13. Validate Stress
14. Cross-Architecture Replication

These map to 13 workflow file identities because branch-specific display names share `build-image.yml` and `replication.yml`.

Classification: `OWNER_ATTESTATION_CURRENT / LIVE_API_STATE_NOT_INDEPENDENTLY_VERIFIED`.

The available GitHub read connector did not expose the workflow-state listing endpoint. The Actions-runs query for the exact current SHA returned an empty list; that does not prove the workflows are disabled. A Vercel check run is not a GitHub Actions run.

Before any future Review push, independently verify the server-side state of all 13 workflow identities and all push-triggered workflows. If any relevant workflow is active or unverifiable, do not push.

## 6. Current commit check and hosting signal

For SHA `35943a7d3b2677280d27fa283d4b7c106e2cec81`:
- Actions workflow-runs query filtered by `head_sha` returned no runs.
- Vercel App check run `139981675572`, `Vercel Preview Comments`, concluded `success`.
- This is not evidence of a successful deployment, production release, environment-variable removal, or route retirement.
- The check-run payload identifies the Vercel GitHub App and lists broad app-level declared permissions. These are not proof of effective installation permissions granted to this repository.

External hosting provider, deployed branch, active domains, deployment history, environment variables, and public route exposure remain unverified. Do not expose credential values.

## 7. Security Log and PAT evidence

Sanitized owner-supplied GitHub Security Log records:
- PAT `GH_TOKEN`, ID `13474885`: `personal_access_token.destroy` and `personal_access_token.access_revoked`.
- PAT `WITNESS_SECRET`, ID `13473352`: `personal_access_token.destroy` and `personal_access_token.access_revoked`.
- Repository secrets `GH_TOKEN`, `WITNESS_SECRET`, `GH_REPO` removed.
- Repository variables `GH_TOKEN`, `WITNESS_TOKEN`, `GH_REPO`, `EXTERNAL_SOURCE_URL` removed.
- Nine GitHub Environments deleted, including `EXTERNAL_SOURCE_URL`.

Classification: `GITHUB_PAT_DESTROY_AND_ACCESS_REVOCATION_LOGGED`.

These are owner-supplied logged events. They are not an independent invalid-token test and do not prove hosting-provider credentials or environment variables were removed. Never paste, transmit, or print PAT values.

## 8. Dependency lock

Current Review `requirements-lock.txt`:
- Blob: `e61adc7c533b685f5c5881153b7f410d2adcce18`
- 48 pinned packages.
- 1,327 SHA-256 hash entries.

Run `45731020069` on older SHA `66b5c30e94416523710f51886f3ae13e147c4796` installed with `--require-hashes` and `--only-binary=:all:`, passed `pip check`, imports, compileall, and 240 unit tests. This is evidence for that older SHA, not a fresh test of `35943a7...`.

The OSV inventory for run `45731020069` produced valid JSON with `results: []`. It covers source manifests/lockfiles, not Debian OS packages. It does not establish Dependabot alert closure.

## 9. Container and Debian Trixie

Current Review Dockerfile pins:

`python:3.11.18-slim-trixie@sha256:b701198cb708b68d9413ca67d6311bd97c9389a2c5fe4da0511fc652642366cd`

It separately pins and SHA-256-verifies `zlib1g=1:1.3.dfsg+really1.3.1-1+deb13u1`.

Dockerfile blob: `fe8dd29e9ef30a58d795e33d903b250ddf12b4e8`.

No current-SHA Docker build or Trivy scan was performed. The latest preserved V4 Trivy evidence is bound to an older image and records 50 HIGH finding records, zero CRITICAL records, and 12 distinct CVEs. It is not a scan of `35943a7...`.

The official Debian Security Tracker was rechecked on 2026-11-26. The tracked Trixie package families remain vulnerable for:
- util-linux: CVE-2026-78408, CVE-2026-78409, CVE-2026-78410, CVE-2026-76642.
- sqlite3: CVE-2026-119373, CVE-2026-119374, CVE-2026-119379.
- systemd: CVE-2026-16742.
- openssl: CVE-2026-124709.
- acl: CVE-2026-54369.
- ncurses: CVE-2025-69720.
- perl: CVE-2026-9538.

Some issues are `no-dsa` or postponed. Do not suppress findings or mix Forky/Sid packages into Trixie. Close findings only when the exact image's installed package identity and official Trixie fixed version support closure.

## 10. Human review and scientific authority

The four reports remain pending:
- Dimitris Politis — statistical methods.
- Anil Machiry — GitHub Actions / CI security.
- Annika Seppälä — climate domain.
- Benjamin Wong — econometrics.

Protocol status: `NOT_FROZEN`.
Formal calibration, confirmatory execution, independent scientific replication, claim support, and promotion remain unauthorized. Scientific authority: `NONE`.

## 11. Library evidence

Library search/read successfully retrieved historical V24, V21, V14, V6, and container V4 records. They remain useful historical evidence, not current Review snapshots. The targeted search did not surface V25/V26 Library records; that does not prove they are absent. Preserve historical evidence and organize current evidence under a dated `Current Evidence` grouping without overwriting older records.

## 12. Required next actions

1. Preserve Main at `9749de9253f144eeda9e1b60cb219cfc5f201ecc`; do not modify, merge, rebase, cherry-pick, or deploy it.
2. Preserve V24–V27 unchanged.
3. On Review only, correct the misleading `assurance_only` description in `replication.yml` using the exact wording in section 3.
4. Add this V28 record as a separate file on Review only.
5. Before pushing, independently verify all 13 workflow identities are disabled and inspect all Review push triggers. Stop if any relevant state is active or unverifiable.
6. Commit only to `review/type1-v4-remediation`; send the resulting full SHA for read-only review.
7. Do not run `replication.yml`, `build-image.yml`, `container-cli-smoke-review.yml`, Trivy, scientific workflows, calibration, confirmatory execution, or replication.
8. After the new SHA is reviewed, the only candidate for separate authorization is `.github/workflows/software-assurance-exact-commit-v1.yml`, with branch `review/type1-v4-remediation` and `scan_commit` equal to that exact full SHA. This is a candidate, not current authorization.
9. Verify Vercel project, deployment, environment, and branch state through the hosting provider before claiming credential removal or deployment status.
10. Continue Debian Trixie monitoring; do not change the base image or suppress CVEs without exact package evidence and a separately reviewed patch.
11. Obtain and assess all four independent reports before any scientific governance upgrade.

Final disposition:

`REVIEW_ONLY / MAIN_FROZEN / CURRENT_REVIEW_HEAD_35943A7 / V27_STALE_AND_PRESERVED / WORKFLOW_CALLER_CLEANUP_CONFIRMED_IN_SOURCE / 14_OWNER_ATTESTED_DISPLAY_NAMES_DISABLED / LIVE_WORKFLOW_STATE_UNVERIFIED / EXACT_ASSURANCE_CANDIDATE_NOT_AUTHORIZED / VERCEL_DEPLOYMENT_UNVERIFIED / PAT_REVOCATION_LOGGED / CONTAINER_SECURITY_OPEN / TRIXIE_CVES_OPEN / HUMAN_REVIEW_PENDING / NOT_FROZEN / NO_SCIENTIFIC_AUTHORITY`.
