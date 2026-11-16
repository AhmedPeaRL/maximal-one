# Exact-Commit Software Assurance Triage — 2026-11-16

## 1. Scope and identity

Repository: `AhmedPeaRL/maximal-one`

Review branch: `review/type1-v4-remediation`

Scanned commit: `040465de7e0d0d0a035b1a0b50018979875166b9`

Workflow definition commit: `040465de7e0d0d0a035b1a0b50018979875166b9`

Workflow run: `43776261910`

Job: `133003134817`

Artifact: `14186925016`

Artifact SHA-256: `7fd5109091254b9345f7c77588cd94449091aba07e39c25326a160e6a17cfa23`

This scan used the exact review-branch commit as its target. The workflow log confirms that the checked-out review branch resolved to the scanned commit.

## 2. Scanner results

| Scanner | Version | Exit code | Result |
|---|---:|---:|---|
| actionlint | 1.7.12 | 123 | Findings require triage |
| zizmor | 1.30.1 | 14 | Findings require triage |
| OpenSSF Scorecard | 5.6.0 | 0 | Scanner completed; findings remain |

### 2.1 actionlint

91 diagnostics were recorded:

- 86 ShellCheck diagnostics:
  - SC2086: 67
  - SC2129: 16
  - SC2002: 1
  - SC2034: 1
  - SC2162: 1
- 4 outdated action-runner references.
- 1 constant-false condition.

The largest concentration was in `.github/workflows/scientific-validation.yml` (76 diagnostics).

Other affected workflows included:

- `scientific-evaluation.yml`
- `cross-run-memory-verification.yml`
- `replication.yml`
- `theoretical_validity.yml`
- `null-calibration-audit.yml`
- `confirmatory-readiness-gate.yml`
- `model-capacity-sweep.yml`
- `scientific-claim-promotion.yml`
- `reproducible_research.yml`
- `model-capacity-diagnostic.yml`
- `primary-null-capacity-audit.yml`

These are diagnostics, not 91 equivalent security vulnerabilities. Each shell finding requires context-sensitive review.

### 2.2 zizmor

190 findings:

| Finding | Count |
|---|---:|
| unpinned-uses | 155 |
| artipacked | 15 |
| excessive-permissions | 13 |
| template-injection | 6 |
| dangerous-triggers | 1 |

Severity totals:

- High: 156
- Medium: 33
- Informational: 1

Notable locations:

- `.github/workflows/evolution.yml`: dangerous trigger.
- `.github/workflows/null-type1-calibration.yml`: five template-injection findings.
- `.github/workflows/cross-run-memory-verification.yml`: one template-injection finding.
- `.github/workflows/scientific-validation.yml`: 43 zizmor findings.

### 2.3 OpenSSF Scorecard

Overall score: `5.7`

Reported check results:

- Binary-Artifacts: 10
- Dangerous-Workflow: 10
- Dependency-Update-Tool: 10
- Fuzzing: 0
- License: 9
- Packaging: 10
- Pinned-Dependencies: 2
- SAST: 10
- Security-Policy: 0
- Token-Permissions: 0
- Vulnerabilities: 0

The report states that 73 existing vulnerabilities were detected. Their individual identities and severity must be reviewed before any closure claim.

## 3. Verified report hashes

The exact-commit manifest recorded:

- actionlint report SHA-256: `482a8f740fd95c62d6f8f60a7e96b6911c2fe29f0f5af0568168a9647f0bdfdb`
- zizmor report SHA-256: `158a07b1d41bc027227116a4b6eca4322db31ba85d335a58dcb27845b93d5a69`
- Scorecard report SHA-256: `baba723bd3201aeb59cbb69fa4c97641320c02ef830cfc65135cd23a3a12f7c8`

## 4. Authority and scientific status

The generated manifest explicitly records:

- `protocol_freeze`: `NOT_FROZEN`
- `formal_calibration_authorized`: `false`
- `confirmatory_execution_authorized`: `false`
- `claim_support`: `false`
- `promotion_authority`: `false`
- `authority`: `NONE`

No scientific claim is promoted by this software-assurance run.

No calibration or confirmatory execution is authorized by this record.

## 5. Required remediation order

1. Review and remediate the dangerous workflow trigger in `evolution.yml`.
2. Remove direct expression interpolation into shell scripts in the six template-injection locations.
3. Review the 13 excessive-permission findings and apply least-privilege permissions.
4. Review the 15 artipacked findings. Do not disable checkout credential persistence in workflows that require authenticated pushes without replacing that authentication path safely.
5. Pin external Actions to verified full commit SHAs. Do not invent or guess SHA values.
6. Resolve the actionlint and ShellCheck diagnostics in small, reviewable groups.
7. Investigate the 73 Scorecard vulnerability findings and record package identity, advisory, severity, and remediation status.
8. Rerun exact-commit software assurance against the new review-branch commit after remediation.

## 6. Non-authorized actions

This record does not authorize:

- formal Type-I calibration;
- confirmatory execution;
- scientific claim promotion;
- protocol freeze;
- changing historical acceptance thresholds;
- merging the review branch into `main`.

The WDC-SILSO data discrepancy remains a separate data-version decision. This scan does not authorize replacing or extending the frozen local dataset.

## 7. Review status

Status: `SOFTWARE_ASSURANCE_FINDINGS_OPEN`

The scanner execution is reproducible evidence of findings at the exact commit above. It is not a passing security audit.

Independent human reports remain pending. No human review should be represented as received until an actual substantive report is available.

Next gate: security remediation on `review/type1-v4-remediation`, followed by a new exact-commit scan.

`main` must remain unchanged during this remediation stage.
