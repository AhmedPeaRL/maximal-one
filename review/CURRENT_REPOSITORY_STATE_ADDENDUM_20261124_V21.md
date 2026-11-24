# HCM Current Repository and Evidence State Addendum — V21

- Evidence date: 2026-11-24
- Repository: `AhmedPeaRL/maximal-one`
- Target branch: `review/type1-v4-remediation`
- Evidence baseline commit: `b3bf4c82132f686e872f0217a7a198ce71c91a8d`
- Disposition: `REVIEW_ONLY / MAIN_UNCHANGED / V20_EXACT_SCAN_COMPLETED / CONTAINER_SECURITY_OPEN / HUMAN_REVIEW_PENDING / SCIENTIFIC_NO_GO`

## 1. Current Git identities

The current GitHub comparison reports:

- `main` HEAD: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- `review/type1-v4-remediation` HEAD: `b3bf4c82132f686e872f0217a7a198ce71c91a8d`
- Review compared with Main: `diverged`, 752 commits ahead and 36 behind.
- Main remains at the previously verified `9749de...` commit.

The comparison from pre-insertion Review HEAD `406300e4c24c452336581ce3f2680b0fb1eda6d3` to `b3bf4c...` reports exactly two commits and exactly two changed paths:

- `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261124_V20.md`
- `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261124_V20.sha256`

No code, workflow, Dockerfile, dataset, or scientific-protocol path changed in that V20 insertion. The V20 Markdown Git blob SHA is `b833cac84d79fe902c9d4596946f6da1cdc111ea`. Its manifest records SHA-256 `1fcfba245adb520d78be540d2365fd9943ceb60ceab8695df6ac4b7bd5ceea15`.

## 2. Exact-commit software-assurance run 45447848518

Workflow: `.github/workflows/software-assurance-exact-commit-v1.yml`

Review workflow-definition blob SHA: `134fcbfa344c8f7f775f521420709c2886ac288a`

The run manifest and runner logs establish:

- Workflow ref: `refs/heads/review/type1-v4-remediation`
- Workflow-definition commit: `b3bf4c82132f686e872f0217a7a198ce71c91a8d`
- `scan_commit`: `b3bf4c82132f686e872f0217a7a198ce71c91a8d`
- Exact checkout identity matched the requested SHA.

Jobs:

| Job | Result |
|---|---|
| Scan exact commit without promotion authority | `success` |
| OSV inventory for the exact target commit | `success` |
| Container CLI build and image security (review only) | `skipped` |

Artifacts and GitHub-recorded SHA-256 digests:

| Artifact | ID | SHA-256 |
|---|---:|---|
| `exact-commit-software-assurance-45447848518` | `14945909165` | `4ce56da0d4df6187ab82c51e56804ca850775837f1d382d07f788137f05dbfef` |
| `osv-dependency-inventory-45447848518` | `14946876053` | `f6eee6ce50e0848fa23c0bc07bd6a9e052c2b24fd92354abf6b5e1d2be8727b2` |

Both ZIP artifacts were downloaded and locally tested. Their local SHA-256 values matched GitHub's recorded digests, and `unzip -t` reported no compressed-data errors.

### Scanner interpretation

- actionlint `1.7.12`: exit code `0`; `actionlint.txt` is empty. The workflow supplies three explicit ignore patterns for same-repository reusable-workflow references using the `$/` syntax.
- zizmor `1.30.1`: exit code `0`; JSON findings array is empty. It was run with `--offline`; its stderr contains informational audit-completion messages.
- OpenSSF Scorecard `5.6.0`: exit code `0`; score `9.2/10`.
  - Fuzzing: `0/10` — no fuzzer integrations detected.
  - License: `9/10` — a license file exists, but Scorecard does not recognize it as an FSF/OSI license.
  - Token-Permissions: `10/10`, while the details still warn about job-level `contents: write` in `canonical-sync.yml:51`, `cross-run-memory-verification.yml:57`, and `replication.yml:232`.
  - SAST: `10/10` reflects detected CodeQL configuration; it does not independently prove a CodeQL analysis run completed for this commit.
  - Scorecard's local-worktree metadata reports commit `unknown`; the separate assurance manifest binds the target commit and run ID.
- OSV-Scanner `2.7.1`: exit code `0`; valid JSON with `results: []`. It scanned five Python requirements manifests (48 package entries each) and `package-lock.json` (zero packages). This is source-manifest coverage, not an operating-system package scan of the container image.

The assurance manifest itself states `ALL_SCANNER_EXIT_CODES_ZERO_REQUIRES_MANUAL_FINDING_REVIEW`, `protocol_freeze=NOT_FROZEN`, all formal/confirmatory/claim/promotion flags false, and `authority=NONE`.

## 3. Latest available container evidence remains open

The latest retrieved image-security result is run `44944152951`, dated 2026-11-21, targeting the older commit `48b223e8d5192ed133ba1f0e59493b6e36600950`.

- Local image build: passed.
- CLI entrypoint smoke test: passed.
- Trivy HIGH/CRITICAL scan: failed with exit code `1`.
- Debian 13.7 image inventory: 87 OS packages.
- Trivy records: 50 HIGH, zero CRITICAL, 12 distinct CVEs.
- Trivy artifact ID: `14723121334`.
- Trivy artifact SHA-256: `657ba2a2f687611c3ea5643ec128ab2fc1badd3cf0783dd8acba645415f791d7`.

This report is bound to the older image target, not to V20 commit `b3bf4c...`. The 2026-11-24 exact-assurance run skipped its container job and therefore supplied no new image build, CLI smoke, or Trivy result for V20.

The 50 Trivy records are not 50 distinct CVEs; several source-package CVEs recur across multiple binary packages.

## 4. Debian Trixie source-package status

The official Debian Security Tracker was checked on 2026-11-24. The tracked Trixie source-package statuses remain vulnerable for the CVEs represented in the latest image report:

- util-linux: `CVE-2026-76642`, `CVE-2026-78408`, `CVE-2026-78409`, `CVE-2026-78410`
- sqlite3: `CVE-2026-119373`, `CVE-2026-119374`, `CVE-2026-119379`
- systemd: `CVE-2026-16742`
- openssl: `CVE-2026-124709`
- acl: `CVE-2026-54369`
- ncurses: `CVE-2025-69720`
- perl: `CVE-2026-9538`

Official tracker references:

- https://security-tracker.debian.org/tracker/source-package/util-linux
- https://security-tracker.debian.org/tracker/source-package/sqlite3
- https://security-tracker.debian.org/tracker/source-package/systemd
- https://security-tracker.debian.org/tracker/source-package/openssl
- https://security-tracker.debian.org/tracker/CVE-2026-54369
- https://security-tracker.debian.org/tracker/source-package/ncurses
- https://security-tracker.debian.org/tracker/source-package/perl

Do not suppress these findings, mix Forky/Sid packages into Trixie, or change the Dockerfile until official Trixie fix provenance and compatibility are reviewed. A future image must be rebuilt and scanned at its own exact commit; the older Trivy report cannot certify V20.

## 5. Disabled workflows: owner attestation versus independent verification

The owner reconfirms that these thirteen workflows remain disabled in GitHub Actions settings:

1. Emergent Periodicity Analysis
2. External Verification
3. Reproducible Research Gate
4. SOS Robustness Gate
5. Build and Push Container — Main name
6. Build and Publish Container — Review name
7. Cross Run Memory Verification
8. Immutable Release Lock
9. Evolution Engine
10. Canonical Sync
11. Cross Architecture Timing Test
12. Cross Architecture Timing
13. Validate Stress

Classification remains `OWNER_ATTESTATION_NOT_INDEPENDENTLY_VERIFIED`. The available GitHub connector reads repository files, commits, jobs, and artifacts but does not expose the server-side enabled/disabled state for all workflows. YAML presence and trigger definitions do not prove that a workflow is enabled; owner attestation does not independently prove it is disabled.

Several corresponding YAML files remain in the repository. Examples include hourly scheduling in `run.yml` (External Verification), six-hour scheduling in `emergent-periodicity.yml`, daily scheduling in `reproducible_research.yml`, weekly schedules in `cross-run-memory-verification.yml`, `timing_cross_arch.yml`, and `validate-stress.yml`, and push/PR triggers in the container workflow files. Keep all thirteen disabled. Do not infer disabled state from a missing run or from a green scanner result.

`replication.yml` is not one of the thirteen disabled workflows. Its `assurance_only` input defaults to `true`, but setting it to `false` activates dependency refresh and a `contents: write` publishing path. Do not dispatch it or change that input.

The review-only child `container-cli-smoke-review.yml` is `workflow_call` only; it is not a direct `Run workflow` target.

## 6. Manual-dispatch branch controls

The Review copy of `software-assurance-exact-commit-v1.yml` contains a review-branch guard and requires manual `scan_commit` to equal the selected Review branch `GITHUB_SHA`. Its `run_container_review` input exists only under `workflow_call`, not under `workflow_dispatch`; the manual UI therefore does not expose a container-review toggle.

The Main copy is older, has a stale default `scan_commit`, and lacks the Review branch guard and the optional container-review input. Do not run the Main copy or use its default value.

The completed V20 scan was the one permitted exact-commit scan for this round. No further workflow dispatch is authorized now. A future container scan would require official Trixie fixes, a justified and reviewed Dockerfile update, a deliberate parent-workflow dispatch-input change on Review, and separate authorization. If the required input is not visible after selecting the Review branch, stop; do not work around it through Main.

## 7. External reproduction code

The owner attests that `api/public_reproduce_endpoint.py` is not deployed, not connected to a public URL, and not routed through a running service. Classification:

`REPOSITORY_CODE_PRESENT / OWNER_ATTESTED_NOT_DEPLOYED / NOT_INDEPENDENTLY_VERIFIED`

The retrieved function is not an HTTP route or a security sandbox. The same Git blob is present on both Main and Review (`api/public_reproduce_endpoint.py`, blob SHA `6a62578495adabdc4eb8e2878265b089a0329046`). It clones the mutable default branch, installs dependencies at call time, has no subprocess timeout or resource/network isolation, and writes the supplied payload to `external_input.json` before invoking the reproduction script.

The retrieved `analysis/external_reproduction.py` is also byte-identical on Main and Review (Git blob SHA `1a75a7e9dd942af1566734101d841377388420c3`). It does not read the supplied payload path. It fetches a fixed public `canonical_report.json`, tests two fixed fields, prints a pass/fail message, and does not create `artifacts/reproduction_result.json`. That expected result path is absent from the Review branch. Thus the endpoint's expected payload-to-result reproduction contract is not implemented. A Review-only disablement would not remove the unchanged prototype from Main; do not treat such a partial patch as repository-wide closure.

A repository search on the default branch found the `run_external_reproduction` definition but no in-repository caller. This does not prove that no external service or deployment route exists. Separately, `scientific-validation.yml` (the SOS Robustness Gate) contains a non-blocking step invoking `analysis/external_reproduction.py`; that workflow is owner-attested disabled, and its server-side disabled state is not independently verified. If re-enabled, the script would fetch the static report rather than consume the generated `external_input.json`.

Do not deploy or expose either file on either branch. Do not describe the static-report fetch as independent reproduction or validation. Any future repository-wide retirement or hard-disable must be handled as a separately authorized change because the same blobs currently exist on Main and Review.

## 8. Independent human reviews and Gmail status

The four requested independent review tracks remain pending:

- Dimitris Politis — statistical-methods review.
- Anil Machiry — GitHub Actions / CI security review.
- Annika Seppälä — climate-domain review.
- Benjamin Wong — econometric review.

A bounded Gmail search retrieved the outgoing requests and scope corrections, but no attributable substantive review report from any of the four reviewers. Wong's out-of-office reply says he is attending events/conferences through 2026-11-29 and may be delayed. An acknowledgement or out-of-office response is not a review report. This search is bounded evidence, not proof about every mailbox folder or future message.

Do not represent the four reviews as completed. Preserve the current corrected scopes and unresolved data/provenance limitations in each request.

## 9. Library evidence

The Library search/read path successfully retrieved the prior container triage V4, Scorecard residual register V6, and repository addendum V14. These remain historical evidence records. V20 and the current run artifacts were independently retrieved from GitHub during this review. Do not treat an older Library ZIP or V14 record as the current Review HEAD or as the V20 run artifact.

Preserve historical evidence. When Library storage permits, add the two V20 run artifacts and this addendum under a clearly dated current-evidence grouping; do not overwrite older records.

## 10. Scientific authority and no-go

The project remains:

- `REVIEW_ONLY`
- `PROTOCOL_NOT_FROZEN`
- `FORMAL_CALIBRATION_NOT_AUTHORIZED`
- `CONFIRMATORY_EXECUTION_NOT_AUTHORIZED`
- `REPLICATION_NOT_AUTHORIZED`
- `CLAIM_SUPPORT_NOT_AUTHORIZED`
- `PROMOTION_NOT_AUTHORIZED`

No new scientific snapshot, Type-I calibration, confirmatory execution, endpoint computation, replication, protocol freeze, publication claim, or promotion is authorized. Software scanner success is not proof of complete security closure, scientific validity, independent replication, or peer review. No claim of 100% assurance is made.

## 11. Required next steps

1. Preserve Main at `9749de9253f144eeda9e1b60cb219cfc5f201ecc`; do not merge, rebase, cherry-pick, or modify Main.
2. If this addendum is adopted, add only this Markdown file and its matching SHA-256 manifest to `review/type1-v4-remediation` in one atomic documentation-only commit. The scan evidence in this record remains bound to parent commit `b3bf4c...`; this documentation-only commit is not a newly scanned code target.
3. Do not dispatch any workflow after this documentation-only commit.
4. Keep all thirteen owner-listed workflows disabled and visually reconfirm the GitHub settings immediately before any future push; current connector evidence cannot independently verify their server-side state.
5. Do not dispatch `replication.yml`, `scientific-validation.yml`, container build/publish workflows, calibration workflows, or any of the thirteen disabled workflows.
6. Continue monitoring official Debian Trixie fixes; do not change the Dockerfile until fixed package versions and compatibility are verified.
7. Wait for the four attributable human reports. Reconcile their findings before any new scientific snapshot or protocol decision.
8. Keep the reproduction code undeployed. Any future reproduction service requires a separately designed, independently reviewed, strongly isolated execution architecture and explicit authorization.

**Final disposition:** `REVIEW_ONLY — V20_EXACT_SCAN_RECORDED — SECURITY_OPEN — CONTAINER_OPEN — HUMAN_REVIEWS_PENDING — NO_NEW_SCIENTIFIC_SNAPSHOT — NO_WORKFLOW_RUN_AUTHORIZED — NO_PROMOTION_AUTHORITY`.
