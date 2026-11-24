#!/usr/bin/env bash
# HCM read-only GitHub audit. GET requests only; never enables/disables workflows,
# changes settings, writes repository contents, dispatches workflows, or merges PRs.
set -Eeuo pipefail

REPO="${1:-AhmedPeaRL/maximal-one}"
OUT="${2:-hcm-readonly-audit-$(date -u +%Y%m%dT%H%M%SZ)}"

for cmd in gh jq; do
  command -v "$cmd" >/dev/null 2>&1 || {
    printf 'ERROR: required command not found: %s\n' "$cmd" >&2
    exit 2
  }
done

mkdir -p "$OUT"
printf 'Repository: %s\nOutput: %s\n' "$REPO" "$OUT"

# Verify authentication without saving credentials or token material.
gh auth status >/dev/null

capture_paginated() {
  local endpoint="$1" output="$2"
  if gh api --method GET --paginate --slurp "$endpoint" \
      >"$OUT/${output}.pages.json" 2>"$OUT/${output}.error.txt"; then
    printf 'AVAILABLE\n' >"$OUT/${output}.access.txt"
  else
    local msg
    msg="$(tr '\n' ' ' <"$OUT/${output}.error.txt" | cut -c1-1000)"
    jq -n --arg status "UNAVAILABLE_OR_NOT_ENABLED_OR_FORBIDDEN" \
          --arg detail "$msg" '{status:$status,detail:$detail}' \
      >"$OUT/${output}.json"
    printf 'UNAVAILABLE_OR_NOT_ENABLED_OR_FORBIDDEN\n' >"$OUT/${output}.access.txt"
  fi
}

capture_single() {
  local endpoint="$1" output="$2"
  if gh api --method GET "$endpoint" \
      >"$OUT/${output}.json" 2>"$OUT/${output}.error.txt"; then
    printf 'AVAILABLE\n' >"$OUT/${output}.access.txt"
  else
    local msg
    msg="$(tr '\n' ' ' <"$OUT/${output}.error.txt" | cut -c1-1000)"
    jq -n --arg status "UNAVAILABLE_OR_NOT_ENABLED_OR_FORBIDDEN" \
          --arg detail "$msg" '{status:$status,detail:$detail}' \
      >"$OUT/${output}.json"
    printf 'UNAVAILABLE_OR_NOT_ENABLED_OR_FORBIDDEN\n' >"$OUT/${output}.access.txt"
  fi
}

# Repository metadata and branch heads.
capture_single "repos/$REPO" "repository"
capture_single "repos/$REPO/branches/main" "main_branch"
capture_single "repos/$REPO/branches/review%2Ftype1-v4-remediation" "review_branch"

# The workflow list includes each workflow's authoritative API state:
# active, disabled_manually, or disabled_inactivity.
capture_paginated "repos/$REPO/actions/workflows?per_page=100" "workflows"
if [[ "$(cat "$OUT/workflows.access.txt")" == "AVAILABLE" ]]; then
  jq '[.[] | .workflows[]? |
       {id,name,path,state,created_at,updated_at}]' \
    "$OUT/workflows.pages.json" >"$OUT/workflows.json"
  jq '{
        total: length,
        by_state: (group_by(.state) | map({(.[0].state): length}) | add // {}),
        active: [.[] | select(.state == "active")],
        disabled: [.[] | select(.state != "active")]
      }' "$OUT/workflows.json" >"$OUT/workflow_state_summary.json"
fi

# Security alert collections. A permission error or disabled feature is recorded,
# not silently treated as an empty alert list.
capture_paginated "repos/$REPO/dependabot/alerts?per_page=100" "dependabot_alerts"
capture_paginated "repos/$REPO/code-scanning/alerts?per_page=100" "code_scanning_alerts"
capture_paginated "repos/$REPO/secret-scanning/alerts?per_page=100" "secret_scanning_alerts"

for name in dependabot_alerts code_scanning_alerts secret_scanning_alerts; do
  if [[ "$(cat "$OUT/${name}.access.txt")" == "AVAILABLE" ]]; then
    jq '[.[][]?]' "$OUT/${name}.pages.json" >"$OUT/${name}.json"
    jq '{
      total: length,
      by_state: (group_by(.state // .resolution // "unspecified")
                 | map({((.[0].state // .[0].resolution // "unspecified")): length})
                 | add // {}),
      by_severity: (group_by(.security_advisory.severity // .rule.security_severity_level // "unspecified")
                    | map({((.[0].security_advisory.severity // .[0].rule.security_severity_level // "unspecified")): length})
                    | add // {})
    }' "$OUT/${name}.json" >"$OUT/${name}_summary.json"
  fi
done

# Policy/configuration read endpoints. Some require repository admin permission.
capture_single "repos/$REPO/actions/permissions" "actions_permissions"
capture_single "repos/$REPO/actions/permissions/workflow" "workflow_permissions"
capture_paginated "repos/$REPO/rulesets?includes_parents=true&per_page=100" "rulesets"
capture_single "repos/$REPO/branches/main/protection" "main_branch_protection"
capture_single "repos/$REPO/branches/review%2Ftype1-v4-remediation/protection" "review_branch_protection"

cat >"$OUT/README.txt" <<EOF
HCM READ-ONLY GITHUB AUDIT
Repository: $REPO
Generated UTC: $(date -u +%Y-%m-%dT%H:%M:%SZ)

This audit uses GitHub CLI GET requests only.
It does not modify repository files/settings, enable/disable workflows,
dispatch or rerun workflows, create releases, or merge pull requests.

Review these files:
- workflows.json and workflow_state_summary.json
- dependabot_alerts.json and dependabot_alerts_summary.json
- code_scanning_alerts.json and code_scanning_alerts_summary.json
- secret_scanning_alerts.json and secret_scanning_alerts_summary.json
- actions_permissions.json, workflow_permissions.json
- rulesets.pages.json
- main_branch_protection.json and review_branch_protection.json

Any *_access.txt value other than AVAILABLE means the relevant API result
could not be established. Check the adjacent *.error.txt file. Do NOT
interpret unavailable/forbidden/disabled as "zero findings" or "disabled".

Secret-scanning API output contains alert metadata, not secret values.
Do not publish this directory publicly; review it for private repository
metadata before sharing.
EOF

printf '\nAudit completed. No write or workflow-dispatch operation was issued.\n'
printf 'Review: %s/workflows.json\n' "$OUT"
printf 'Review access flags: %s/*_access.txt\n' "$OUT"
