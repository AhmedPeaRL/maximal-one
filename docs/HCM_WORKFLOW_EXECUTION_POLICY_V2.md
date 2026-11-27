# HCM Workflow Execution Policy — V2

- Evidence date: 2026-11-27
- Repository: `AhmedPeaRL/maximal-one`
- Main: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- Review: `c8985c4bfcb6140dbfd081a4eb2faab29fb561af`
- Status: `MAIN_FROZEN / REVIEW_ONLY / NO_WORKFLOW_RUN_AUTHORIZED`

## 1. Current authorization

No GitHub Actions workflow is authorized to run in this round. This policy does not authorize a dispatch, rerun, deployment, publication, settings change, merge, or Main modification.

All thirteen unique workflow paths owner-attested as `disabled_manually` remain prohibited from dispatch. The latest independently hash-verified workflow inventory archive observed those states at `2026-11-27T16:41:42Z`; the owner has re-attested that they remain disabled. A new authenticated GET-only Actions workflow-list response is still required before a Review commit because `.github/workflows/build-image.yml` has an unfiltered `push` trigger.

## 2. Main and Review boundaries

- `main` is frozen at `9749de9253f144eeda9e1b60cb219cfc5f201ecc`.
- All proposed source/documentation changes are Review-only on `review/type1-v4-remediation`.
- No merge, rebase, cherry-pick, force-push, PR merge, deployment, or Main change is authorized.
- The active `Review Branch Integrity` ruleset blocks branch deletion and non-fast-forward updates; do not attempt to bypass it.

## 3. Trigger safety

`.github/workflows/build-image.yml` on Review has an unfiltered `push` trigger. If active, a Review push starts its build and stability-check jobs. Its publish job is explicitly gated to `refs/heads/main`, but that does not make the Review push harmless. The API inventory reported this path as `disabled_manually` at the timestamp above; the user currently re-attests that state. Do not push until a fresh GET-only workflow inventory independently confirms it remains disabled.

Other Review-targeted push workflows inspected in this round use path filters. The proposed patch paths are not among those filters. This static path review does not override the broad `build-image.yml` trigger.

## 4. Only future candidate to consider

After the patch is committed to Review, its full SHA is inspected, the current workflow states are independently reconciled, and a separate explicit approval is given, the only candidate to consider is:

`.github/workflows/software-assurance-exact-commit-v1.yml`

Run target:
- Branch selector: `review/type1-v4-remediation`
- Input `scan_commit`: exact full Review HEAD SHA being reviewed
- Never select Main

The workflow path exists on Main and Review, so the manual workflow menu can expose it. The Main copy is older and has a stale default SHA; the selected Review branch and explicit exact SHA are mandatory. This is a candidate only, not authorization.

## 5. Workflows not manually runnable or not authorized

- `container-cli-smoke-review.yml`: `workflow_call` only; no direct manual Run workflow target.
- `dependency-vulnerability-inventory.yml`: `workflow_call` only; no direct manual Run workflow target.
- `scientific-evaluation.yml` and `evaluation.yml`: `pull_request` only.
- `core-scientific/.github/workflows/truth-pressure-lock.yml`: push to Main only.
- `core-scientific/.github/workflows/witness-proxy.yml`: manual dispatch, but not authorized.
- `replication.yml`, every scientific/calibration/adjudication workflow, the worker-order workflow, and all thirteen manually disabled paths: prohibited from dispatch in this round.

A Review-only workflow cannot be made manually runnable by copying it into Main. Do not change Main to expose a Run workflow button. If a future Review-only operation needs manual initiation, it must be called by an already reviewed dispatch-capable workflow whose path exists on the default branch, or deferred until a separately approved architecture change.

## 6. Evidence and result classification

- `success` on an individual job is not a successful overall workflow run when another required job is cancelled or skipped.
- A cancelled run is `CANCELLED_INCOMPLETE`, not PASS and not FAIL, unless the complete logs establish a different classification.
- Scanner exit code zero does not establish container security, scientific validity, protocol freeze, independent replication, or promotion authority.
- `disabled_manually` is a timestamped state, not a permanent guarantee. Preserve timestamp, workflow ID, path, name, state, branch SHAs, raw API response, normalized inventory, and SHA-256 for every monitoring snapshot.

## 7. Explicit prohibitions

Do not dispatch or rerun `build-image.yml`, `replication.yml`, any scientific/calibration/confirmatory workflow, the worker-order workflow, `container-cli-smoke-review.yml`, or any other workflow in this round. Do not build or publish a container. Do not change Dockerfile pins, suppress CVEs, mix Debian Forky/Sid packages into Trixie, or deploy.
