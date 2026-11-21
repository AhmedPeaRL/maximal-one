# Current Repository State Addendum — 2026-11-21 V1

**Disposition:** `REVIEW_ONLY — SECURITY_GATE_OPEN — HUMAN_REVIEWS_PENDING — NO_WORKFLOW_RUN_AUTHORIZED — NO_NEW_SCIENTIFIC_SNAPSHOT — NO_PROMOTION_AUTHORITY`

## 1. Exact live GitHub identities

Repository: `AhmedPeaRL/maximal-one`  
Default branch (`main`) HEAD: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`  
Review branch (`review/type1-v4-remediation`) HEAD: `bd91473ece3b7b90aedbe21395308a32e9086d9e`  
Comparison: `diverged`; review branch is 709 commits ahead and 36 commits behind `main`.

The GitHub repository metadata confirms `main` is the default branch. The compare operation confirms the above base commit and divergence counts. The exact review HEAD was independently established by comparing `bd91473...` with `review/type1-v4-remediation`: status `identical`, zero commits ahead/behind.

## 2. Newly received documentation commits

The two commits are in sequence and both are reachable from the current review branch HEAD:

1. `a79171747abae5f81e295ce8b0c5d0997d1b56c1` — adds only `review/CONTAINER_IMAGE_SECURITY_TRIAGE_20261121_V4.md`.
2. `bd91473ece3b7b90aedbe21395308a32e9086d9e` — one commit after the first; adds only `evidence/CURRENT_SCORECARD_RESIDUAL_REVIEW_REGISTER_20261121_V6.csv`.

The commit-to-commit comparison reports exactly one added CSV file in the second commit. The comparison from the second commit to the named review branch reports `identical`. Neither of these two commits changes application code, Dockerfile, workflow YAML, datasets, scientific protocol, or `main`.

Canonical commit URLs:
- https://github.com/AhmedPeaRL/maximal-one/commit/a79171747abae5f81e295ce8b0c5d0997d1b56c1
- https://github.com/AhmedPeaRL/maximal-one/commit/bd91473ece3b7b90aedbe21395308a32e9086d9e

## 3. Historical documents that must not be rewritten

V4 was prepared before the two commits and correctly recorded the then-current review HEAD as `a6ec52661bfe07446be9a1de3234cdf253b8ef1a`, 707 ahead / 36 behind. V6 likewise records that prior branch state in `BRANCH-006`. Those statements are historical, not current. Preserve V4 and V6 unchanged. This addendum supersedes only their moving-branch identity statements; it does not supersede their security findings, evidence, or historical scan identities.

The Trivy result remains `FAIL_POLICY_OPEN`: 47 HIGH finding records, 0 CRITICAL, 11 distinct CVEs, 18 binary package names, from the Debian 13.7 image scan. The zlib remediation remains closed only for the exact scanned image and CVE-2026-85091. The other six source-package families remain open pending Trixie fixes and/or evidence-based applicability review.

## 4. Trixie status checked on 2026-11-21

Debian Security Tracker still lists the scanned Trixie source versions as vulnerable for the CVEs relevant to the prior Trivy report:

- util-linux `2.41.5-0+deb13u1`: CVE-2026-76642, CVE-2026-78408, CVE-2026-78409, CVE-2026-78410.
- sqlite3 `3.46.1-7+deb13u2`: CVE-2026-119373, CVE-2026-119374, CVE-2026-119379.
- systemd `257.13-1~deb13u1`: CVE-2026-16742.
- acl `2.3.2-2`: CVE-2026-54369.
- ncurses `6.5+20250216-2`: CVE-2025-69720.
- perl `5.40.1-6+deb13u1`: CVE-2026-9538.

Tracker evidence:
- util-linux: https://security-tracker.debian.org/tracker/source-package/util-linux
- sqlite3: https://security-tracker.debian.org/tracker/source-package/sqlite3
- systemd: https://security-tracker.debian.org/tracker/source-package/systemd
- acl: https://security-tracker.debian.org/tracker/source-package/acl
- ncurses: https://security-tracker.debian.org/tracker/source-package/ncurses
- perl: https://security-tracker.debian.org/tracker/source-package/perl

Do not mix Forky/Sid packages into Trixie, substitute an unverified base, suppress Trivy findings, or assume all records are exploitable. Do not modify the Dockerfile until an appropriate Trixie package update is actually available and its compatibility, provenance, and package installation path have been reviewed.

## 5. Workflow authorization and remediation-only workflow mechanics

**No workflow is authorized now.** The two latest commits are documentation-only. The user reports that no workflow has been run after them; this is an owner statement, not independently verified from a complete Actions run listing in this review.

The only future candidate, after Trixie fixes are available, the Dockerfile change is justified and reviewed, and a separate authorization is given, is:

- Workflow file: `.github/workflows/software-assurance-exact-commit-v1.yml`
- Target branch: `review/type1-v4-remediation`
- `scan_commit`: the exact full 40-character HEAD of that branch at dispatch time
- `run_container_review`: `true`

The parent workflow exists on both `main` and the review branch. The review-branch copy exposes `run_container_review` and invokes the review-only child workflow. The child `.github/workflows/container-cli-smoke-review.yml` exists only on the review branch and declares `workflow_call`, not `workflow_dispatch`; it must not be run directly.

GitHub's `workflow_dispatch` UI requires the workflow to exist on the default branch. Because the `main` copy is older and lacks the `run_container_review` input, select the review branch in the Actions UI and verify that both inputs are actually displayed. If `run_container_review` is absent, stop; do not dispatch with guessed/default values and do not add a dispatcher to `main` as a workaround. A branch-only `workflow_call` child is invoked by the parent on the selected review ref; it is not a standalone Run workflow target.

`replication.yml` is not one of the 12 owner-listed disabled workflows. Its `assurance_only=true` default still runs guard/review-head/exact-assurance jobs; `false` activates dependency refresh and write/publish logic. Do not dispatch or change it.

The user's report that the 12 named workflows remain disabled is retained as owner attestation. The GitHub connector used here did not expose the server-side Actions enabled/disabled settings for independent verification. Do not re-enable any of them.

## 6. Independent human reviews and scientific authority

The latest retrieved Gmail correspondence contains updated scope corrections sent November 19, but no substantive independent review report from any of the four reviewers:

- Politis: statistical-methods review; `alpha_max=NOT_SET`; V4 remains `REVISE_AND_RESUBMIT`; historical V1 remains `NOT_PASSED` under its original two-sided Wilson rule.
- Machiry: CI/CD and GitHub Actions security review; no human security disposition received.
- Seppälä: current climate candidate is HadUKP England and Wales precipitation (EWP), not HadCET. The raw-source SHA discrepancy remains unresolved; no domain is approved.
- Wong: current economic candidate is CPIAUCNS pre-gap through September 2025 (1,353 observations). The full series has a missing 2025-10-01 observation; do not impute, interpolate, carry forward, or silently drop it. Wong's out-of-office reply says delays may occur through November 29.

The pinned scientific target remains `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`. No new snapshot, formal calibration, confirmatory execution, claim support, or promotion is authorized. `protocol_freeze=NOT_FROZEN`; `formal_calibration_authorized=false`; `confirmatory_execution_authorized=false`; `claim_support=false`; `promotion_authority=false`; independent domains `0/2`; replication `0/2`.

## 7. Required next steps

1. Preserve V4 and V6 as historical records; do not rewrite or delete them.
2. Add this addendum to `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261121_V1.md` on `review/type1-v4-remediation` only.
3. Use commit message: `Record current repository state addendum V1`.
4. Do not run any workflow after this documentation-only commit.
5. Send the commit URL and full SHA for verification.
6. Wait for official Trixie fixes and the four human reviews. Reassess package applicability and the Dockerfile before any future assurance run.
7. No `main` changes, merge, rebase, cherry-pick, calibration, confirmatory run, replication run, new snapshot, or promotion.

**Final state:** `REVIEW_ONLY — SECURITY_GATE_OPEN — Trixie_FIXES_PENDING — HUMAN_REVIEWS_PENDING — NO_WORKFLOW_RUN_AUTHORIZED — NO_NEW_SNAPSHOT — NO_PROMOTION_AUTHORITY`.
