# HCM Current Repository State Addendum — V27

- Evidence date: 2026-11-26
- Repository: `AhmedPeaRL/maximal-one`
- Review branch: `review/type1-v4-remediation`
- Main SHA observed: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- Review HEAD verified: `53c0276a5c9b186ce2d502a4aa8a65bca3ab6bba`
- V26 commit: `a46992ead14e07adfabb275105f746ead0510f92`
- Latest remediation commit: `53c0276a5c9b186ce2d502a4aa8a65bca3ab6bba`
- Previous assurance run: `45731020069`
- Assurance run SHA: `66b5c30e94416523710f51886f3ae13e147c4796`

## 1. Branch identity and immutability

The current Review branch HEAD was independently resolved as:

`53c0276a5c9b186ce2d502a4aa8a65bca3ab6bba`

Comparison against V26 commit `a46992ead14e07adfabb275105f746ead0510f92` shows exactly one subsequent commit, modifying only:

`.github/workflows/software-assurance-exact-commit-v1.yml`

Main remains at:

`9749de9253f144eeda9e1b60cb219cfc5f201ecc`

Main remains frozen. No merge, rebase, cherry-pick, pull request, deployment, or workflow execution on Main is authorized.

V24, V25, and V26 remain immutable historical records.

## 2. Security Log chronology and PAT evidence

The owner-supplied sanitized GitHub Security Log records establish nine Environment deletions:

1. `Production – ahmedpearl-maximal-one`
2. `Production – maximal-one`
3. `Preview – ahmedpearl-maximal-one`
4. `Preview – maximal-one`
5. `GH_REPO`
6. `github-pages`
7. `Personal Access Token`
8. `WITNESS_SIGNATURE`
9. `EXTERNAL_SOURCE_URL`

The repository Actions variable `EXTERNAL_SOURCE_URL` was removed at 2026-11-26 02:44:14 +0200. Its GitHub Environment was deleted at 02:44:28 +0200.

Both events occurred after V25 was committed. V25 remains unchanged.

The supplied records establish:

- PAT `GH_TOKEN`, ID `13474885`: `personal_access_token.destroy` and `personal_access_token.access_revoked`.
- PAT `WITNESS_SECRET`, ID `13473352`: `personal_access_token.destroy` and `personal_access_token.access_revoked`.

Repository Actions secrets removed:

- `GH_TOKEN`
- `WITNESS_SECRET`
- `GH_REPO`

Repository Actions variables removed:

- `GH_TOKEN`
- `WITNESS_TOKEN`
- `GH_REPO`
- `EXTERNAL_SOURCE_URL`

The `WITNESS_SIGNATURE` Environment records also establish removal of its `WITNESS_SECRET` secret and variable before Environment deletion.

Classification:

`GITHUB_PAT_DESTROY_AND_ACCESS_REVOCATION_LOGGED`

These are logged GitHub events supplied by the repository owner. They do not establish an independent invalid-token test, nor do they prove that external hosting-provider credentials or environment variables have been removed.

## 3. Workflow disablement attestation

The owner confirms that the following 14 workflow display names remain disabled:

1. Emergent Periodicity Analysis
2. External Verification
3. Reproducible Research Gate
4. SOS Robustness Gate
5. Build and Push Container — Main display name
6. Build and Publish Container — Review display name
7. Cross Run Memory Verification
8. Immutable Release Lock
9. Evolution Engine
10. Canonical Sync
11. Cross Architecture Timing Test
12. Cross Architecture Timing
13. Validate Stress
14. Cross-Architecture Replication

The 14 display names correspond to 13 workflow file identities after accounting for branch-specific display-name changes:

- The two container names correspond to `build-image.yml`.
- `Cross-Architecture Replication` on Main and `Python 3.11.15 Dependency Refresh (Review Branch)` on Review correspond to `replication.yml`.

Classification:

`OWNER_ATTESTATION_CURRENT / LIVE_API_STATE_NOT_INDEPENDENTLY_VERIFIED`

The following files remain especially sensitive:

- `.github/workflows/build-image.yml`: unfiltered `push:` trigger.
- `.github/workflows/replication.yml`: manual dispatch and dependency refresh/publishing path with `contents: write`.
- `.github/workflows/canonical-sync.yml`: publishing job with `contents: write`.
- `.github/workflows/cross-run-memory-verification.yml`: scheduled/manual workflow with a `contents: write` recording job.

No dispatch of these workflows is authorized.

## 4. Previous exact assurance run

Run `45731020069`:

- Branch: `review/type1-v4-remediation`
- SHA: `66b5c30e94416523710f51886f3ae13e147c4796`
- Event: `workflow_dispatch`
- Conclusion: `failure`

Successful jobs:

- Exact Review target preflight.
- Python dependency lock installation and verification.
- OSV dependency inventory.

Failed job:

- Exact commit software assurance scan.

The dependency lock job installed `requirements-lock.txt` with `--require-hashes` and `--only-binary=:all:`, completed `pip check`, required imports, and compileall, then passed 240 unit tests.

OSV-Scanner v2.7.1 scanned six supported manifest/lockfile paths. The output JSON was valid and contained an empty `results` array.

This is limited dependency-inventory evidence, not container or Debian package assurance.

## 5. Artifact identity and hashes

Exact assurance artifact:

- ID: `15076178169`
- Size: 6,699 bytes
- SHA-256: `2f1cf8135e1550bd3f67735369cee51e2e03c08629047b67199b5fe85277d8f1`

OSV inventory artifact:

- ID: `15076477884`
- Size: 1,272 bytes
- SHA-256: `07d6993c62cb67e393f10ebcbc03bea00ef638d1fef4871f486917fd5654f408`

Both ZIP artifacts were downloaded and opened during the current review. Locally computed SHA-256 values matched GitHub artifact digests.

The exact assurance artifact reports:

- actionlint 1.7.12: exit code 0.
- zizmor 1.30.1: exit code 12, two `self-repository` findings, Low severity and High confidence.
- OpenSSF Scorecard 5.6.0: local score 9.2, with repository commit identity `unknown`.

The Scorecard score is not a complete remote repository assessment.

## 6. Remediation commit review

Commit `53c0276a5c9b186ce2d502a4aa8a65bca3ab6bba` changed only:

`.github/workflows/software-assurance-exact-commit-v1.yml`

The patch correctly:

- Replaced the local reusable workflow reference with GitHub's `$/` self-repository syntax.
- Removed the `workflow_call` trigger.
- Kept `workflow_dispatch` as the only trigger.
- Removed the replication caller exception from exact SHA validation.
- Required the target SHA to equal `GITHUB_SHA`.

However, a remaining inconsistency was identified:

`.github/workflows/replication.yml` still contains an `exact-assurance` job that invokes the exact assurance workflow using a local reusable-workflow reference.

This caller is incompatible with the removal of `workflow_call` from the called workflow. It also leaves the second `self-repository` finding present in the prior zizmor report.

The required next patch must:

1. Remove the `review-head` job from `replication.yml`.
2. Remove the `exact-assurance` job from `replication.yml`.
3. Keep `replication.yml` disabled and unauthorized.
4. Remove unused `WORKFLOW_REF` environment variables from the Exact Assurance preflight and scan steps.
5. Preserve the Review-only SHA and branch guards.
6. Preserve `$/` syntax for the reusable OSV inventory workflow.

No finding suppression is authorized.

The next commit must be inspected and linted before any workflow execution is considered.

## 7. GitHub manual dispatch limitation

GitHub documents that `workflow_dispatch` only receives events when the workflow file exists on the repository's default branch. The Actions UI's Run workflow control also requires the workflow file on the default branch.

The current Exact Assurance workflow exists on Review, not Main.

Main must remain frozen. Therefore, do not add a copy or stub of this workflow to Main merely to enable the Run workflow button.

A separate isolated assurance-runner repository is the preferred future mechanism. Its default branch can contain the manually dispatched runner, which checks out the target repository at an exact immutable SHA with read-only permissions and no inherited credentials.

No workflow dispatch is authorized in this addendum.

## 8. Container, Debian, and hosting status

No current-SHA Docker build or Trivy container scan has been performed.

The OSV inventory does not establish Debian Trixie package security.

Previously recorded Trixie CVEs remain open until official Trixie package versions are checked and the exact image is rescanned. Do not suppress findings or mix Forky/Sid packages into Trixie.

The public GitHub Pages URL could not be independently fetched. External hosting provider, deployed branch, external environment variables, and retired-route exposure remain unverified.

No deployment or publication is authorized.

## 9. Independent human review and scientific authority

The four requested independent reports remain pending:

- Dimitris Politis
- Anil Machiry
- Annika Seppälä
- Benjamin Wong

No formal calibration, confirmatory execution, independent scientific replication, scientific claim support, or promotion is authorized.

Protocol status remains:

`NOT_FROZEN`

Scientific authority remains:

`NONE`

## 10. Runner redesign

Runner isolation remains open.

Required evidence includes:

- Immutable source SHA binding.
- CPU, memory, process, and time limits.
- Explicit network-egress policy.
- No inherited credentials or token propagation.
- Hash-locked dependencies.
- Deterministic, independently verifiable artifacts.
- Separation of engineering reproducibility from scientific replication.

Successful GitHub-hosted runner jobs do not prove these isolation properties.

## 11. Required next actions

1. Preserve Main, V24, V25, and V26 unchanged.
2. Apply the remaining workflow corrections on Review only.
3. Remove the stale reusable caller from `replication.yml`.
4. Remove unused `WORKFLOW_REF` environment variables from Exact Assurance.
5. Keep all 14 owner-attested workflow display names disabled.
6. Verify `build-image.yml` is disabled immediately before any future Review push.
7. Add V27 on Review only.
8. Commit to `review/type1-v4-remediation` only.
9. Send the exact new commit SHA for independent read-only review.
10. Do not dispatch any workflow until a separate exact-run authorization is issued.
11. Do not run container, Trivy, replication, calibration, confirmatory, or scientific workflows.
12. Continue Debian Trixie verification, external hosting verification, runner redesign, and the four independent human reviews.

Final disposition:

`REVIEW_ONLY / MAIN_FROZEN / PAT_REVOCATION_LOGGED / 9_GITHUB_ENVIRONMENT_DELETIONS_LOGGED / 14_OWNER_ATTESTED_WORKFLOW_NAMES_DISABLED / EXACT_ASSURANCE_REMEDIATION_PARTIAL / REPLICATION_CALLER_INCOMPATIBILITY_OPEN / CONTAINER_SECURITY_OPEN / HOSTING_VERIFICATION_OPEN / HUMAN_REVIEW_PENDING / NOT_FROZEN / NO_SCIENTIFIC_AUTHORITY`.
