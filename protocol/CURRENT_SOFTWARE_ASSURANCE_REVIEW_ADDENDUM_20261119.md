# Current Software-Assurance Review Addendum

- **Date:** 2026-11-19  
- **Repository:** `AhmedPeaRL/maximal-one`  
- **Run:** `44594759111`  
- **Disposition:** REVIEW ONLY — NO NEW SNAPSHOT — NO SCIENTIFIC AUTHORITY

## 1. Exact identity

- main HEAD: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- review HEAD: `a6a9e7db76daf5bb912ea29709ac4f3af1dfb827`
- run event: `workflow_dispatch`
- run branch: `review/type1-v4-remediation`
- scan commit: `a6a9e7db76daf5bb912ea29709ac4f3af1dfb827`
- workflow definition commit: `a6a9e7db76daf5bb912ea29709ac4f3af1dfb827`
- exact assurance job: `135809945438`
- OSV job: `135809946280`

## 2. Exact assurance results

- actionlint 1.7.12: exit 0; empty diagnostics.
- zizmor 1.30.1: exit 0; findings array `[]`.
- OpenSSF Scorecard 5.6.0: exit 0; score 8.6/10.
- OSV-Scanner 2.7.1: exit 0; `results: []` for six detected supported manifests/lockfiles.

These results do not automatically close historical findings.

## 3. Scorecard residuals

The following remain OPEN pending targeted source review:

- Token-Permissions: 9/10; excessive workflow token permissions detected.
- Pinned-Dependencies: 9/10; a dependency not pinned by hash detected.
- Security-Policy: 4/10; policy maturity requires review.
- Fuzzing: 0/10; fuzzing is absent and applicability must be assessed.

The Scorecard JSON does not identify the exact offending path for Token-Permissions or Pinned-Dependencies. Do not guess or modify files without identifying the exact source.

## 4. Historical finding ledger

The V2 ledger remains unchanged:

- 313 unique original findings.
- 13 FIXED_VERIFIED.
- 300 PENDING_MANUAL_REVIEW.
- 0 FALSE_POSITIVE.
- 0 ACCEPTED_RISK.
- 151 high-severity unpinned-uses findings remain pending.

The clean current zizmor output does not retrospectively close these historical rows. Each row requires path/action-specific evidence.

## 5. Caller guard

- Manual workflow_dispatch path: FIXED_VERIFIED by run `44594759111`.
- Reusable replication.yml caller path: OPEN / NOT EXERCISED.

Do not run the full replication workflow merely to test the reusable caller because it can publish a dependency-lock commit. Use an isolated non-mutating guard test.

## 6. Branch and workflow policy

- Keep `main` unchanged.
- Do not merge the divergent branches.
- Keep the 12 user-reported disabled workflows disabled.
- No new snapshot is authorized.
- No calibration, confirmatory execution, promotion, or scientific claim is authorized.

The current review branch is reported unprotected by the GitHub branch endpoint. Review appropriate branch protection rules without disrupting the controlled review workflow.

## 7. Next gate

No new workflow run is authorized now.

After an actual code repair on `review/type1-v4-remediation`, the only candidate is:

`.github/workflows/software-assurance-exact-commit-v1.yml`

Run it on the review branch with `scan_commit` equal to the exact new 40-character HEAD SHA.

Do not run `replication.yml`, the 12 disabled workflows, scientific validation, calibration, promotion, or snapshot workflows.

## 8. Governance

- protocol_freeze: NOT_FROZEN
- formal_calibration_authorized: false
- confirmatory_execution_authorized: false
- claim_support: false
- promotion_authority: false
- authority: NONE

The four independent human reports remain pending as reported by the user.
