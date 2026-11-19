# Software Assurance Review — Current Evidence and First High-Risk Dispositions

**Status:** `REVIEW_ONLY — NO_NEW_SNAPSHOT — NO_WORKFLOW_RUN_AUTHORIZED_YET`

**Repository:** `AhmedPeaRL/maximal-one`

## 1. Exact branch and scan identities

- `main` HEAD: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- `review/type1-v4-remediation` observed HEAD: `11877b56a12565cfda714236f87e0212618cd6cf`
- Pinned historical review target: `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`
- Later clean software-assurance run: `44408732399`, scanned commit `1792d735c96622202c3c115701e53bbe49bc99e1`, artifact `14475467384`
- Later OSV run/artifact: `14475298142` (run/artifact identity preserved in the original triage note)
- GitHub compare `1792d735...` → `11877b56...`: exactly two added Markdown documents; no workflow, code, or data changes. Thus the later scanner result applies to the same code/workflow tree as the current review HEAD.
- Current review commit `11877b56...` is signature-verified by GitHub and adds only `protocol/REVIEW_BRANCH_HEAD_CLARIFICATION_20261119.md` relative to its parent.
- Branches remain divergent; no wholesale merge is authorized.

## 2. First-pass technical dispositions: 13 high-risk findings outside the unpinned-action batch

The V2 CSV preserves all 313 original ledger rows and original target evidence. It assigns `FIXED_VERIFIED` to only the 13 high-risk findings below, with remediation commit and current-source evidence. These are AI-assisted technical dispositions, not independent human reviews. The 151 `unpinned-uses` findings are also classified High by the original scanner, but they remain pending as a separate high-volume batch because each action/path still needs an explicit source-to-remediation mapping.

| Finding IDs | Original class | Remediation commit | Verification basis |
|---|---|---|---|
| `ZIZ-006` | Workflow-wide `packages: write` | `1229ce760055de83fc07f77c050a59ce0a26eeb5` | Permission narrowed to main-only publish job; top-level permissions `{}`; current YAML and later clean scan |
| `ZIZ-007` | Inline secret/context interpolation in shell | `1229ce760055de83fc07f77c050a59ce0a26eeb5` | Token moved to environment variable and passed via `printf`; current YAML and later clean scan |
| `ZIZ-036` | `workflow_run` trigger in Evolution Engine | `38991af02e4eb9bf4aef52321a0fa18afd660b61` | Workflow moved outside `.github/workflows`; no active `workflow_run` remains in current review workflow tree |
| `ZIZ-062`, `ZIZ-068` | `workflow_run` trigger and cache-poisoning risk in Release Lock | `552fc196169f4380c86e39208931b90b32dd9627` | GitHub records rename from active workflow path to `docs/disabled-workflows/release-lock.yml.txt`; archive is not a workflow YAML in `.github/workflows` |
| `ZIZ-093`–`ZIZ-096` | Workflow-wide `contents/packages/pages/id-token: write` | `50c1ff079f3cdb2422e99b7fe7599180979e47e7` | Workflow-level grants removed; top-level permissions `{}`; current jobs use narrow scopes; only CodeQL job has `security-events: write` |
| `ZIZ-098`–`ZIZ-101` | Untrusted `client_payload` interpolation into shell | `31b67e357970008bfafe1192c7e419c42c7cc582` | Payload moved to env + Python parser/safe payload boundary; direct shell interpolation removed; boundary test added |

**Do not infer that the other findings are closed.** In particular, 151 `unpinned-uses` findings remain `PENDING_MANUAL_REVIEW` in V2, despite the later `zizmor` run returning an empty findings array. The remaining 300 ledger rows (including these 151) stay pending until their own path/action/remediation mapping is reviewed. The original 205 zizmor, 97 actionlint, and 11 Scorecard records remain intact.

## 3. Later automated evidence — not a substitute for adjudication

The later exact-commit software-assurance artifact for `1792d735...` records:

- actionlint exit code `0`, empty output;
- zizmor exit code `0`, empty findings array;
- Scorecard `8.6/10`, with 0 vulnerabilities reported by its Vulnerabilities check;
- separate OSV Scanner exit code `0`, `results: []` across six supported manifests/lockfiles.

The original target scan remains preserved: Scorecard `5.7/10` and 73 existing vulnerabilities reported by its Vulnerabilities check. No historical result is overwritten or retrospectively reclassified.

## 4. Current review-only workflow observations

- The current review branch still contains `.github/workflows/software-assurance-exact-commit-v1.yml`, with `workflow_dispatch` and `workflow_call`.
- The review-branch manual-dispatch guard requires `GITHUB_REF=refs/heads/review/type1-v4-remediation` and `scan_commit == GITHUB_SHA`.
- The same workflow is called by `.github/workflows/replication.yml`. That caller has its own review-branch guard, but the reusable workflow's current guard only explicitly handles `workflow_dispatch`. Because reusable workflows inherit the caller context (`GITHUB_REF` and `GITHUB_SHA`), the current `replication.yml` publishes a new commit and passes that new SHA to the reusable workflow; this can conflict with the `scan_commit == GITHUB_SHA` test if the caller event context is `workflow_dispatch`. This is a **new current-branch guard correctness/authorization issue**, not one of the 313 historical target findings. The official GitHub documentation states that the `github` context in a reusable workflow is associated with the caller; therefore the caller context matters when this step evaluates `GITHUB_REF`, `GITHUB_SHA`, and `GITHUB_WORKFLOW_REF`. Record it separately as `OPEN` pending the guard repair below and a successful exact-commit scan.
- The manual workflow file exists on `main` (required for GitHub's Actions UI button), but the `main` version differs and does not contain the review-branch guard. If/when a run is authorized, select `review/type1-v4-remediation` in the **Use workflow from / Branch** dropdown and verify the displayed ref before submitting. Never run this workflow against `main`.
- The current UI enabled/disabled state of the 12 workflows is accepted as user-reported; the available read-only GitHub endpoint did not expose the workflow `state` list. Their YAML files remain in repository history/tree; disabling in the UI is not deletion.
- Historical activity: `Reproducible Research Gate` ran on `main` by schedule at `2026-11-19T11:19:30Z` (run `44513785360`); `Build and Publish Container` ran on review HEAD `11877b56...` by push at `2026-11-19T14:40:21Z` (run `44546286399`). These occurred before your present confirmation that both were disabled. No later run appeared in the latest run page retrieved during this review.

## 5. Required code hardening before the next assurance run

**Target branch:** `review/type1-v4-remediation` only.

**File:** `.github/workflows/software-assurance-exact-commit-v1.yml`

Replace only the `env:` and branch-validation part of the step `Validate and materialize exact target` with the patch in `protocol/EXACT_ASSURANCE_CALLER_GUARD_PATCH_20261119.md`. It will:

1. Always require the review branch.
2. For a direct manual dispatch of this workflow, require `scan_commit == GITHUB_SHA`.
3. For the sole current reusable caller `replication.yml`, require `scan_commit` to equal the current remote review-branch HEAD.
4. Reject every unrecognized caller workflow.

This preserves the intended manual exact-HEAD path and the existing dependency-refresh caller without permitting a main-branch invocation. The official GitHub documentation says reusable-workflow context values are inherited from the caller; see [GitHub: Reusing workflow configurations](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations) and [GitHub: Events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows).

After committing this code change, and only then, one run is conditionally authorized:

- Workflow: `.github/workflows/software-assurance-exact-commit-v1.yml`
- Branch selected in Actions UI: `review/type1-v4-remediation`
- Input `scan_commit`: the exact 40-character HEAD SHA of that branch after the patch commit
- Expected behavior: workflow guard passes; actionlint/zizmor/Scorecard scan that exact SHA; artifact records `scan_commit` and `workflow_definition_commit` separately.

Do **not** run `replication.yml`, calibration, scientific validation, null calibration, raw audit, replication promotion, review snapshot, or any of the 12 user-disabled workflows in this round.

## 6. New YAML policy while keeping `main` untouched

Do not add a standalone `workflow_dispatch` YAML only on the review branch and expect it to appear in the Actions UI. GitHub requires the workflow file to exist on the default branch for the UI dispatch button. The safe pattern under the current branch policy is:

- keep an existing dispatcher path on `main` (the exact-assurance workflow already exists there);
- add a new reusable workflow using `workflow_call` on `review/type1-v4-remediation` only;
- have the review-branch version of the existing dispatcher call that reusable workflow;
- choose the review branch in the UI dropdown; keep the main copy unchanged;
- add a strict caller/ref allowlist and exact-commit validation to the reusable workflow itself.

No new YAML file is needed for the immediate patch; edit the existing exact-assurance file on review only.

## 7. Governance state — unchanged

`protocol_freeze=NOT_FROZEN`; `formal_calibration_authorized=false`; `confirmatory_execution_authorized=false`; `claim_support=false`; `promotion_authority=false`; independent secondary domains `0/2`; replication `0/2`; no new snapshot authorized. The four independent human reports remain pending as user-reported; do not represent any as received or sent unless evidenced.
