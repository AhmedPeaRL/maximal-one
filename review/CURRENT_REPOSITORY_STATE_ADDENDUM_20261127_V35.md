# HCM Current Repository and Evidence Addendum — V35

- Evidence date: 2026-11-27
- Repository: `AhmedPeaRL/maximal-one`
- Main HEAD: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- Review HEAD before this proposed patch: `c8985c4bfcb6140dbfd081a4eb2faab29fb561af`
- Disposition: `MAIN_FROZEN / REVIEW_ONLY / AUDIT_PATCH_PREPARED_NOT_COMMITTED / WORKFLOW_STATE_RECHECK_REQUIRED / NO_WORKFLOW_RUN_AUTHORIZED`

## 1. Scope and non-actions

This addendum records read-only inspection and a proposed narrow Review patch. No repository write, commit, push, workflow dispatch/rerun, deployment, publication, merge, rebase, cherry-pick, or settings mutation was performed while preparing it. Main remains frozen. The patch is not authorized for commit until the current `build-image.yml` workflow state is independently rechecked through the corrected GET-only audit.

## 2. Exact repository identity

- Main ref: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`.
- Review ref: `c8985c4bfcb6140dbfd081a4eb2faab29fb561af`.
- Review tree: `30a532bdfa98057ba41859ada53c68206b0292ee`.
- Main tree: `9c6afb051275b40d0c0522ebab0422c070dd8763`.
- Review commit parent: `f7068c2d396a8446b5d333a9dd125d6679b3753f`.
- GitHub reports the Review commit signature as verified/valid.

The current proposed patch must be based on this exact Review HEAD. If the branch moves, stop and re-review all diffs and path-trigger consequences before applying it.

## 3. V2 workflow inventory archive

The user-supplied Termux archive was materialized, extracted, and verified:

- Archive: `hcm-workflow-inventory-audit-v2.tar.gz`
- Archive SHA-256: `3defba9fb2b35c8f5c4a808aa60cbbe362e8bd262f2d609e189d53e726ff277f`
- Size: 157,484 bytes
- Observation: `2026-11-27T16:41:42Z`
- Internal SHA256SUMS: all twelve listed file hashes re-verified.
- API records: 54 total; 41 active; 13 `disabled_manually`; zero other disabled states in that snapshot.
- All thirteen required unique paths were present in the API response and marked `disabled_manually`.
- Main and Review tree responses were not truncated.

The user re-attests that the thirteen paths remain disabled. The archived API response is still a point-in-time observation, not a permanent guarantee. The connected GitHub fetch interface does not expose the Actions workflow-list endpoint in this inspection; a fresh authenticated Termux GET-only response is required before a Review push.

## 4. Workflow ID/path reconciliation

- Workflow ID `380113480`, `.github/workflows/acquire-secondary-data.yml`, is present in both branch trees. It is not an orphan.
- Workflow ID `398736460`, `.github/workflows/type1-v4-cross-runner-worker-order.yaml`, is absent from both exact branch trees. Fetching that exact path at Review SHA `c8985c4...` returns 404. The direct GitHub workflow-detail API endpoint could not be queried through the connected fetch interface. Preserve this as `ORPHAN_API_RECORD_CANDIDATE / CURRENT_DETAIL_UNRESOLVED`; do not delete, enable, disable, or dispatch it based on absence from the trees alone.
- The `.yml` sibling path is a separate existing workflow file: `.github/workflows/type1-v4-cross-runner-worker-order.yml`, ID `398009319`, present in both branch trees.
- `.github/workflows/build-image.yml` has one API workflow identity, ID `237168758`, despite branch-specific display names. Main calls it `Build and Push Container`; Review calls it `Build and Publish Container`. Do not count the two display names as two independent workflow IDs.

## 5. Trigger and permission review

The trigger/permission-level inspection covered the 37 API-registered active workflow files present in the Review tree, the additional root workflow-call/pull-request definitions, and the two nested `core-scientific/.github/workflows/` definitions. This was a static source review, not a complete independent code-security audit of every job or action.

Key findings:

1. `.github/workflows/build-image.yml` on Review has an unfiltered `push:` trigger. If active, a push to Review starts the image build and stability-check jobs. The `publish` job is explicitly gated to `github.ref == refs/heads/main`; therefore a Review push does not satisfy that publish condition, but it still runs the build and stability checks. The API snapshot reported this workflow as `disabled_manually` at `2026-11-27T16:41:42Z`; the user re-attests it remains disabled. **Do not push until a fresh API GET confirms the disabled state.**
2. Other Review-targeted push workflows inspected use path filters. The proposed audit-tool, test, review-addendum, and documentation paths do not match those reviewed filters. This does not neutralize the unfiltered `build-image.yml` trigger.
3. `software-assurance-exact-commit-v1.yml` is manual-dispatch only. The path exists on both Main and Review. The Main copy is older and contains a stale default `scan_commit`; the Review copy requires the exact `scan_commit` input and enforces the Review branch/exact-SHA guard. Any later candidate run must select Review and enter the exact full Review HEAD SHA.
4. `container-cli-smoke-review.yml` and `dependency-vulnerability-inventory.yml` are `workflow_call` only; they are not direct manual Run workflow targets.
5. `scientific-evaluation.yml` and `evaluation.yml` are pull-request-only. `core-scientific/.github/workflows/truth-pressure-lock.yml` pushes only on Main. `core-scientific/.github/workflows/witness-proxy.yml` is manual but is not authorized.
6. No workflow is authorized to run in this round. `replication.yml`, all scientific/calibration/adjudication workflows, the worker-order workflow, and the thirteen manually disabled paths remain prohibited from dispatch.

## 6. Live ruleset and branch metadata

Read-only GitHub API queries returned:

- `Evolution Gate`, ruleset ID `12957369`: active; applies to the default branch; requires pull-request review, required status checks, linear history, CodeQL/code-quality checks, required deployments, and signed commits; no bypass actors; current user cannot bypass.
- `Review Branch Integrity`, ruleset ID `27684653`: active; applies to `refs/heads/review/type1-v4-remediation`; blocks branch deletion and non-fast-forward updates; no bypass actors; current user cannot bypass.
- Review branch metadata reports `protected: true`; its legacy branch-protection subobject reports `enabled: false`, consistent with protection being provided by the active ruleset rather than legacy branch protection.
- The Main legacy branch-protection endpoint returned HTTP 403 `Resource not accessible by integration`. Actions permissions endpoints and security-alert endpoints were not available through this connected fetch interface. These remain `UNKNOWN`, not empty or safe.

## 7. Run 48 artifact review

Run `45897518209` (`Exact Commit Software Assurance`, run number 48) targeted `f7068c2d396a8446b5d333a9dd125d6679b3753f`, not current Review HEAD `c8985c4...`.

Job outcomes:

- Exact Review target preflight: success.
- Exact-commit scanner job: success.
- OSV dependency inventory: success.
- Dependency-lock verification/test job: cancelled while its combined dependency/test step was still running; logs show many passing tests but no final unittest summary.
- Overall run: `CANCELLED_INCOMPLETE`, neither PASS nor FAIL.

Artifacts were downloaded and inspected:

| Artifact | ID | ZIP SHA-256 | Result |
|---|---:|---|---|
| Exact-commit software assurance | `15154845796` | `d6b7e7c861062c52d328000b9edfd1dca73b029f093eebd080d5c290b3488d8a` | actionlint 1.7.12 exit 0/empty output; zizmor 1.30.1 exit 0/empty JSON; Scorecard 5.6.0 score 9.2/10, with Fuzzing 0/10 |
| OSV dependency inventory | `15153862809` | `647393c4ee23d97bd45c9f35d11d09ac7eff9c9789eb9614576c3c33591c2e5e` | OSV-Scanner v2.7.1 exit 0; valid JSON with no findings in the six supported requirements manifests scanned |

The OSV scan is source-manifest/lockfile evidence, not an OS-package or container-image scan. Scorecard's `Vulnerabilities` check and OSV's empty results do not close the historical Trivy image findings. The artifacts are evidence for `f7068c2...` only, not `c8985c4...`.

## 8. Container and runner security

Current Review Dockerfile blob: `fe8dd29e9ef30a58d795e33d903b250ddf12b4e8`. It pins `python:3.11.18-slim-trixie` by digest, verifies a pinned `zlib1g` Debian package SHA-256, and runs as UID/GID 10001. It does not upgrade the complete base-image OS package set.

Current `container-cli-smoke-review.yml` blob: `0130ec93f5eab60429e7db18af3f20daeab59ed4`. It is `workflow_call` only. It runs `docker build` and `docker run --rm` without explicit CPU, memory, PID, disk, or network limits; it does not prove host credential isolation, child-process secret isolation, or artifact secret scrubbing; it does not save a complete `dpkg-query -W` inventory or the immutable image digest. Its Trivy step checks HIGH/CRITICAL only with `ignore-unfixed=false`. This is a smoke/scan helper, not an isolated runner and not container-security closure.

Required future runner evidence remains: ephemeral isolated runner, cgroup/resource limits, network allowlist, no host credentials, minimal read-only token or no token in child processes, canary tests, artifact leak tests, CPU/memory/PID/disk/network boundary tests, full logs, exact image digest, and complete package inventory. No container workflow is authorized now.

## 9. Debian Trixie tracker update

The official Debian Security Tracker was checked on 2026-11-27. It continues to mark the listed Trixie packages vulnerable for the twelve historical Trivy CVEs across util-linux, sqlite3, systemd, openssl, acl, ncurses, and perl. Some fixes are visible only in Forky/Sid/unstable; several Trixie entries are `no-dsa` or postponed. The historical installed versions are not a current-image inventory. See `docs/DEBIAN_TRIXIE_CVE_STATUS_20261127.md` for the package/CVE table and tracker references.

Do not mix Forky/Sid packages into Trixie, suppress findings, or claim closure without an exact image digest, full `dpkg-query -W` inventory, and package-level Debian tracker mapping.

## 10. Credentials, hosting, and Library evidence

- The prior GitHub/Pages evidence reports Pages built from Main with HTTPS and HTTP 200; it is not a Review deployment.
- Prior Vercel connector evidence reports project `maximal-one` as `live:false` and the Review deployment for `c8985c4...` as `CANCELED` with target `null`. A prior project-scoped environment query returned no listed project variables; team-shared variables, other projects, integrations, external services, and local credentials were not fully audited.
- A repository secret name `EXTERNAL_SOURCE_URL` was reported in prior user-side API output; its value was not inspected. Do not request or print any secret value.
- Previous owner-supplied security-log evidence records PAT revocation/destruction; it is not an independent invalid-token test. Verify privately only if the old token is already stored locally, without printing or sharing it.
- Library V33 and V34 remain historical/current indexes respectively. Prior attempts to move Project-managed Library artifacts through the personal Library mutation API were unsupported. Do not delete or overwrite historical evidence; preserve exact files and add a new dated index rather than rewriting V33/V34.

## 11. Scientific and human-review status

- Confirmatory protocol: `NOT_FROZEN`.
- Formal Type-I calibration: `NOT_AUTHORIZED`.
- Power target/adequacy: not independently established.
- Confirmatory execution and independent replication: `NOT_AUTHORIZED`.
- Claim support and promotion authority: `NONE`.
- Independent eligible real-domain replication: not established (0/2 in the preserved record).
- Four specialist reports remain pending: Dimitris Politis (statistical methods), Anil Machiry (CI/CD security), Annika Seppälä (climate domain), and Benjamin Wong (econometrics).

No new reviewer follow-up or scientific snapshot was sent. Engineering scanner success is not scientific confirmation or independent human review.

## 12. Proposed narrow patch and closure criteria

| Change | File | Base blob SHA-1 | Reason | Required test | Closure criterion |
|---|---|---|---|---|---|
| Replace | `tools/hcm_readonly_github_audit.sh` | `280e8f8790a892a058ef13718ce1e63eadc0dea9` | URL-encode Review branch path; capture Review branch head and protection; query orphan ID `398736460` and known ID `380113480`; retain GET-only semantics | `bash -n`; ShellCheck if installed; static regression tests | All API calls explicitly GET; correct encoded path used for branch and protection; raw errors preserved; no mutation/dispatch command; authenticated run produces timestamped outputs and hashes |
| Replace | `tests/test_hcm_readonly_github_audit.py` | `f19dc5666c093eb6cfb8aff389b9bf1732be60b6` | Enforce the corrected URL, branch/protection captures, direct ID queries, run-history queries, GET-only behavior, and no mutation paths | `python -m unittest tests/test_hcm_readonly_github_audit.py -v` | All tests pass locally without network calls |
| Add | `docs/HCM_WORKFLOW_EXECUTION_POLICY_V2.md` | New file | Preserve Main freeze, no-run authorization, push guard, and the sole future exact-assurance candidate | Markdown review against live branch/ruleset evidence | No ambiguous authorization; candidate remains explicitly not approved |
| Add | `docs/DEBIAN_TRIXIE_CVE_STATUS_20261127.md` | New file | Update official Trixie tracker status without claiming current-image applicability | Link/status review against official Debian tracker | Each CVE is mapped to a source package and current Trixie status; image inventory explicitly marked stale |
| Add | `docs/HCM_SECURITY_TRIAGE_REGISTER_V2.csv` | New file | Maintain risk owners, evidence, and closure criteria | CSV parse and field-count validation | Every open risk has evidence and a falsifiable closure requirement |
| Add | `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261127_V35.md` plus `.sha256` | New file | Preserve exact current state, artifacts, trigger review, patch rationale, tests, and closure criteria | SHA-256 verification and independent review | Hash matches exact file bytes; no historical addendum overwritten |

This patch intentionally does not change `.gitignore`, any workflow YAML, Dockerfile, scientific source/protocol, Main, or hosting settings. The `.gitignore` credential-hygiene change is deferred to a separately reviewed patch because it is not required to correct the read-only audit and must preserve the tracked benign `.npmrc` configuration.

## 13. Required order of operations

1. Before any commit, run the corrected local audit from Termux with GitHub CLI GET requests only. Confirm `build-image.yml` remains `disabled_manually`; preserve raw JSON, access/error flags, branch heads, both branch-protection responses, rulesets, alert access results, exact workflow ID details, timestamp, and SHA-256.
2. If the workflow inventory is unavailable, `build-image.yml` is active, any required state is ambiguous, or the branch SHA differs from `c8985c4...`, do not commit. Return the evidence for review.
3. Run local syntax/static tests on the patch. Do not run any GitHub Actions workflow as part of the patch.
4. Only after the fresh API state is reconciled may the exact patch be committed to `review/type1-v4-remediation`. Main remains untouched.
5. After the commit, verify the full new Review SHA and all changed blob SHAs. Do not dispatch a workflow automatically.
6. A later `software-assurance-exact-commit-v1.yml` run may be considered only after separate explicit approval, on Review, with `scan_commit` equal to the exact new Review HEAD. It is not authorized by this addendum.

**Final disposition:** `PATCH_PREPARED_NOT_COMMITTED / FRESH_WORKFLOW_STATE_CHECK_REQUIRED / MAIN_FROZEN / NO_WORKFLOW_RUN_AUTHORIZED / CONTAINER_SECURITY_OPEN / SCIENTIFIC_NO_GO / HUMAN_REVIEWS_PENDING`.

## 14. Offline patch-preparation tests

The proposed patch was tested locally without GitHub network calls:

- `bash -n tools/hcm_readonly_github_audit.sh`: passed.
- `python -m unittest discover -s tests -v`: 10 tests passed.
- `HCM_SECURITY_TRIAGE_REGISTER_V2.csv`: parsed successfully, 13 data rows and 7 columns.
- Mocked GitHub CLI smoke test: passed using synthetic GET responses; generated branch/run summaries, access/error flags, `meta.txt`, and `SHA256SUMS`; every output checksum verified. No real network call was made.
- ShellCheck: not installed in the preparation environment; no ShellCheck pass is claimed.
- No GitHub Actions workflow was run, and no repository state was changed.

The exact new-file SHA-256 values and Git blob SHA-1 values are recorded in `review/HCM_PATCH_MANIFEST_20261127_V35.md` and the package `SHA256SUMS`. The V35 addendum has a separate `.sha256` companion.
