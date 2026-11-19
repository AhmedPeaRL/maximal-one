# Exact-assurance caller guard patch — review branch only

**Target branch:** `review/type1-v4-remediation`

**File:** `.github/workflows/software-assurance-exact-commit-v1.yml`

**Edit only this step:** `Validate and materialize exact target`.

Replace the current `env:` and the initial branch-check block with the following. Keep the later SHA-format check, `git fetch --no-tags origin "$SCAN_COMMIT"`, worktree creation, and exact-commit equality checks unchanged.

```yaml
        env:
          SCAN_COMMIT: ${{ inputs.scan_commit }}
          WORKFLOW_REF: ${{ github.workflow_ref }}
        run: |
          set -euo pipefail

          EXPECTED_REF="refs/heads/review/type1-v4-remediation"

          if [[ "$GITHUB_REF" != "$EXPECTED_REF" ]]; then
            echo "BLOCKED: exact software assurance is restricted to the review branch."
            exit 1
          fi

          case "$WORKFLOW_REF" in
            */.github/workflows/software-assurance-exact-commit-v1.yml@refs/heads/review/type1-v4-remediation)
              if [[ "$SCAN_COMMIT" != "$GITHUB_SHA" ]]; then
                echo "BLOCKED: manual scan_commit must equal the selected review branch HEAD."
                exit 1
              fi
              ;;

            */.github/workflows/replication.yml@refs/heads/review/type1-v4-remediation)
              git fetch --no-tags origin "$EXPECTED_REF"
              REMOTE_REVIEW_HEAD="$(git rev-parse FETCH_HEAD)"
              if [[ "$SCAN_COMMIT" != "$REMOTE_REVIEW_HEAD" ]]; then
                echo "BLOCKED: reusable scan_commit must equal the current remote review branch HEAD."
                exit 1
              fi
              ;;

            *)
              echo "BLOCKED: unrecognized caller workflow: $WORKFLOW_REF"
              exit 1
              ;;
          esac
```

## Why this is needed

The workflow supports both direct `workflow_dispatch` and `workflow_call`. The current review-branch version is also called by `.github/workflows/replication.yml`, whose publish job can create a new commit and pass that new SHA to the reusable scan. The reusable workflow receives the caller's GitHub context. A single `scan_commit == GITHUB_SHA` condition for every `workflow_dispatch` context can therefore reject the legitimate post-publish SHA. Conversely, leaving `workflow_call` without an explicit caller/ref allowlist weakens the callee's own branch boundary.

This patch distinguishes the two approved caller paths and rejects all others. It does not change scientific code, data, thresholds, historical results, or main.

## Validation after editing

1. Commit this patch on `review/type1-v4-remediation` only.
2. Record the resulting 40-character HEAD SHA.
3. Do not run anything on `main`.
4. The only conditionally authorized next run is `.github/workflows/software-assurance-exact-commit-v1.yml` with the review branch selected and `scan_commit` equal to that exact new HEAD.
5. Send the run URL, artifact URL, and manifest showing `scan_commit` and `workflow_definition_commit` separately.
