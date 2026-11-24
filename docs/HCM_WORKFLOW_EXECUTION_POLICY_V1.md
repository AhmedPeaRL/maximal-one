# HCM workflow execution policy — current Review round

## Current authorization

**No GitHub Actions workflow is authorized to run in this round.** The next commit is a Review-only code/documentation update to correct a read-only audit script and record evidence. Run the audit locally through GitHub CLI GET requests; do not dispatch a workflow.

The thirteen workflow names owner-attested as disabled remain prohibited from dispatch. `replication.yml` is also prohibited: its `assurance_only` default is true, but setting it false enables dependency refresh and a write/publish path. The fact that a workflow appears active in the Actions list does not grant permission to run it.

## Future candidate, not currently authorized

After the read-only audit is reviewed and a separate approval is given, the only candidate to consider for a software-only exact-commit check is:

`.github/workflows/software-assurance-exact-commit-v1.yml`

Target ref must be `review/type1-v4-remediation`, and the `scan_commit` input must equal the exact current Review HEAD selected in the GitHub UI. The workflow has a Review-branch guard. The manual `workflow_dispatch` interface exposes `scan_commit` only; `run_container_review` exists only under `workflow_call`, so the manual UI cannot turn on the container job. This candidate is not approved for this round.

## Review-only workflows and manual dispatch

- `container-cli-smoke-review.yml`: `workflow_call` only; no direct Run workflow button.
- `dependency-vulnerability-inventory.yml`: `workflow_call` only; no direct Run workflow button.
- `scientific-evaluation.yml`: `pull_request` only; no manual dispatch.
- `evaluation.yml`: `pull_request` only; no manual dispatch.

A workflow that exists only on Review cannot be assumed to appear in the manual Run workflow menu because GitHub requires the workflow file to exist on the default branch for `workflow_dispatch`. Do not copy a Review-only workflow into Main to work around this; Main is frozen. If a future need arises, use an already-existing, separately reviewed Review-branch caller where appropriate, or defer until a separately authorized architecture change.

## User interface safety

If a future run is explicitly approved, select the exact workflow and the Review branch in the Run workflow dropdown. Verify the selected branch name and full SHA before entering inputs. If the Review branch is absent, the input set differs from the reviewed file, or the guard is not visible in the source, stop. Never choose Main, never dispatch `replication.yml`, and never use a `contents: write` path as an audit substitute.
