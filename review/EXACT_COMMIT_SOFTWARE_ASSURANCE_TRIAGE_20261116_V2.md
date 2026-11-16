# Exact-Commit Software Assurance Triage — 2026-11-16 — V2

## 1. Scope and immutable identity

Repository: `AhmedPeaRL/maximal-one`

Review branch: `review/type1-v4-remediation`

Scanned source commit: `38991af02e4eb9bf4aef52321a0fa18afd660b61`

Workflow definition commit: `38991af02e4eb9bf4aef52321a0fa18afd660b61`

Workflow: `Exact Commit Software Assurance`

Workflow run: `43780951750`

Job: `133017770705`

Artifact: `14188785540`

Artifact name: `exact-commit-software-assurance-43780951750`

Artifact ZIP SHA-256:
`01c300a925547a17d5f983fae9ff9b1ed860bbf94d8e81b98280ab83a3db6c74`

Workflow ref: `refs/heads/review/type1-v4-remediation`

The workflow manifest confirms that the scan target and workflow-definition commit are identical. The exact-commit scanner completed all scanner and artifact-upload steps. Its final gate failed because scanner findings remain.

The commit `38991af02e4eb9bf4aef52321a0fa18afd660b61` has the message:

`Move evolution.yml to disabled workflows directory`

Its only recorded file change is a rename:

- Previous: `.github/workflows/evolution.yml`
- New: `docs/disabled-workflows/evolution.yml`

The commit reports zero additions and zero deletions. This removes that file from GitHub Actions' active workflow directory. It does not establish that all other workflow security findings are closed.

At comparison time, `main` was `9749de9253f144eeda9e1b60cb219cfc5f201ecc`. The review branch remained divergent: 509 commits ahead and 36 behind, with merge base `a9808bd999a7ad902daf15606272529ca9af4580`.

Do not merge, rebase, or force-update `main` as part of this remediation.

## 2. Scanner results

Tool versions:

- actionlint 1.7.12
- zizmor 1.30.1
- OpenSSF Scorecard 5.6.0

| Scanner | Exit code | Interpretation |
|---|---:|---|
| actionlint | 123 | Findings require triage |
| zizmor | 14 | Findings require triage |
| Scorecard | 0 | Scanner completed; findings remain |

### 2.1 actionlint

91 diagnostics were recorded:

- 86 ShellCheck diagnostics:
  - SC2086: 67
  - SC2129: 16
  - SC2002: 1
  - SC2034: 1
  - SC2162: 1
- 4 outdated action-runner references:
  - `.github/workflows/theoretical_validity.yml`: `actions/setup-python@v4`
  - `.github/workflows/reproducible_research.yml`: `actions/setup-python@v4`
  - `.github/workflows/replication.yml`: `actions/checkout@v3`
  - `.github/workflows/replication.yml`: `actions/setup-python@v4`
- 1 constant-false condition:
  - `.github/workflows/scientific-validation.yml`, line 4322.

The largest concentration remains `.github/workflows/scientific-validation.yml` with 76 diagnostics.

Other affected paths include:

- `.github/workflows/legacy/scientific-evaluation.yml`
- `.github/workflows/cross-run-memory-verification.yml`
- `.github/workflows/replication.yml`
- `.github/workflows/theoretical_validity.yml`
- `.github/workflows/null-calibration-audit.yml`
- `.github/workflows/confirmatory-readiness-gate.yml`
- `.github/workflows/model-capacity-sweep.yml`
- `.github/workflows/scientific-claim-promotion.yml`
- `.github/workflows/reproducible_research.yml`
- `.github/workflows/model-capacity-diagnostic.yml`
- `.github/workflows/primary-null-capacity-audit.yml`

These are context-sensitive diagnostics, not 91 equivalent security vulnerabilities. Do not apply blind quoting or bulk shell rewrites.

### 2.2 zizmor

The current scan recorded 180 findings:

| Finding | Previous scan | Current scan |
|---|---:|---:|
| unpinned-uses | 155 | 154 |
| artipacked | 15 | 14 |
| excessive-permissions | 13 | 12 |
| template-injection | 6 | 0 |
| dangerous-triggers | 1 | 0 |
| **Total** | **190** | **180** |

Current severity totals:

- High: 154
- Medium: 26

The current finding categories are unpinned action references, credential persistence through checkout, and excessive permissions. The current report contains no `template-injection` or `dangerous-triggers` findings.

The `evolution.yml` rename is consistent with removal of the previous dangerous-trigger finding.

The revised environment-variable handling in `null-type1-calibration.yml` and `cross-run-memory-verification.yml` is consistent with removal of the prior template-injection findings. This does not close unrelated permission, credential-persistence, or execution-authorization questions in those workflows.

The 14 remaining `artipacked` findings affect:

- `canonical-sync.yml`
- `codeql-analysis.yml`
- `confirmatory-readiness-gate.yml`
- `cross-run-memory-verification.yml`
- `cross_arch_timing.yml`
- `emergent-periodicity.yml`
- `replication.yml`
- `reproducible_research.yml`
- `run.yml`
- `tag-signature-verify.yml`
- `theoretical_validity.yml`
- `timing_cross_arch.yml`
- `validate-stress.yml`
- `core-scientific/.github/workflows/truth-pressure-lock.yml`

The 12 `excessive-permissions` findings affect:

- `confirmatory-readiness-gate.yml`
- `cross-run-memory-verification.yml`
- `cross_arch_timing.yml`
- `emergent-periodicity.yml`
- `replication.yml`
- `reproducible_research.yml`
- `run.yml`
- `tag-signature-verify.yml`
- `theoretical_validity.yml`
- `timing_cross_arch.yml`
- `validate-stress.yml`
- `core-scientific/.github/workflows/truth-pressure-lock.yml`

Do not set `persist-credentials: false` blindly in `cross-run-memory-verification.yml`: that workflow currently performs an authenticated `git push`. Replace its authentication path safely before disabling persisted checkout credentials.

Do not bulk-pin actions using guessed SHA values. Every full SHA must be verified against the intended upstream repository and release/tag, then recorded in a pin-verification register.

### 2.3 OpenSSF Scorecard

Overall score: `5.7`

| Check | Score | Reported reason |
|---|---:|---|
| Binary-Artifacts | 10 | No binaries found |
| Dangerous-Workflow | 10 | No dangerous workflow patterns detected |
| Dependency-Update-Tool | 10 | Update tool detected |
| Fuzzing | 0 | Project is not fuzzed |
| License | 9 | License file detected |
| Packaging | 10 | Packaging workflow detected |
| Pinned-Dependencies | 3 | Dependencies not pinned by hash |
| SAST | 10 | CodeQL detected |
| Security-Policy | 0 | Security policy file not detected |
| Token-Permissions | 0 | Workflow tokens with excessive permissions detected |
| Vulnerabilities | 0 | 73 existing vulnerabilities detected |

The report's 73-vulnerability statement does not by itself establish severity, package identity, exploitability, or remediation status. Each advisory must be identified and reviewed before any closure claim.

Scorecard's local report identifies the temporary local repository path and records its commit as `unknown`. Exact source identity is therefore established by the scanner workflow's target-validation step and assurance manifest, not by Scorecard's local repository metadata alone.

## 3. Raw report integrity

SHA-256 values recorded in the exact-commit manifest:

- actionlint: `482a8f740fd95c62d6f8f60a7e96b6911c2fe29f0f5af0568168a9647f0bdfdb`
- zizmor: `0f3b96a816907a8f2433ffb520eccb5ee4dda3072dbcffe9454bdfc5de8cc104`
- Scorecard: `a17ad06910b919827f5724c633fec6ab9ca58221ba7828b4b7381fa21cd07418`

The downloaded artifact ZIP SHA-256 was independently checked against the digest reported by GitHub's artifact upload log:

`01c300a925547a17d5f983fae9ff9b1ed860bbf94d8e81b98280ab83a3db6c74`

## 4. Exact workflow outcome

The following steps completed successfully:

1. Checkout workflow definition.
2. Validate and materialize exact target.
3. Install pinned scanner versions.
4. Run actionlint.
5. Run zizmor.
6. Run OpenSSF Scorecard.
7. Create exact-commit assurance manifest.
8. Upload scanner evidence.

The final gate failed with:

`SCANNER_FINDINGS_OR_ERRORS_RECORDED; triage required`

This is the expected fail-closed outcome while scanner findings remain. It is not a scanner crash and must not be reported as a passing assurance gate.

## 5. Required next remediation sequence

1. Preserve this V2 record as the current exact-commit scan record. The previous V1 triage document refers to the earlier scan and must remain historical.
2. Remediate the 12 excessive-permission findings one workflow at a time. First inspect each job's write operations, event sources, secrets, and artifact behavior. Apply `contents: read` only where sufficient. Give write permissions only to the exact job and step that require them.
3. Redesign `cross-run-memory-verification.yml` so verification runs with read-only permissions and any history update/push is isolated into a narrowly privileged write path. Do not expose write credentials to dependency installation or untrusted input processing.
4. Review the 14 `artipacked` findings individually. Use `persist-credentials: false` where no authenticated push is needed. Where push is needed, replace the credential path with a step-scoped authentication mechanism and ensure credentials are not included in artifacts or caches.
5. Pin all external actions to verified full commit SHAs. Maintain a register containing action repository, release/tag, resolved SHA, upstream evidence URL, verification date, and reviewer disposition.
6. Fix the four outdated action-runner references using verified supported versions and exact SHAs.
7. Resolve ShellCheck diagnostics in small groups, preserving behavior and testing each modified workflow.
8. Review the constant-false condition at `scientific-validation.yml:4322`; determine whether it is intentionally disabled or dead logic before changing it.
9. Investigate all 73 Scorecard vulnerability detections and record package, advisory, severity, affected version, fixed version, and remediation evidence.
10. Rerun exact-commit software assurance against the new review-branch commit after the above changes.

No remediation is accepted merely because a scanner count decreases. Every finding requires a recorded disposition supported by code review, tests, and exact-commit evidence.

## 6. Calibration and scientific authorization safeguards

The exact-commit assurance manifest explicitly records:

- `protocol_freeze`: `NOT_FROZEN`
- `formal_calibration_authorized`: `false`
- `confirmatory_execution_authorized`: `false`
- `claim_support`: `false`
- `promotion_authority`: `false`
- `authority`: `NONE`

The following remain prohibited:

- Formal Type-I calibration.
- Confirmatory execution.
- Scientific claim promotion.
- Protocol freeze.
- Retrospective alteration of acceptance thresholds.
- Merging the review branch into `main`.

The current `null-type1-calibration.yml` remains fail-closed until a V3-specific runner is reconciled with the V3 protocol and all authorization requirements are independently satisfied. Do not run it as a test or as a shortcut to scientific progress.

The WDC-SILSO source discrepancy remains a separate data-version decision. This software-assurance run does not authorize modifying the local scientific dataset.

## 7. Independent human review status

As of 2026-11-16, the Gmail review search found:

- Dimitris Politis: request sent; no substantive human review received.
- Annika Seppälä: request sent; no substantive human review received.
- Benjamin Wong: request sent; automatic out-of-office response says he is attending events and conferences through November 29; no substantive review received.
- Aditya Machiry: request sent; no substantive human review received.

Do not describe any of these as completed independent reviews. An acknowledgement or automatic reply is not a review report.

## 8. Decision

Status: `SOFTWARE_ASSURANCE_FINDINGS_OPEN`

The current scan demonstrates a reduction from 190 to 180 zizmor findings and removal of the previous template-injection and dangerous-trigger categories. It does not demonstrate a clean security audit.

The next work is security remediation on `review/type1-v4-remediation`, followed by another exact-commit scan.

`main` must remain unchanged during this remediation stage.

No scientific authorization, claim support, protocol freeze, or promotion authority is granted by this record.
