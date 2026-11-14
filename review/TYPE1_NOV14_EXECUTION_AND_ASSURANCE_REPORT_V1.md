# November 14, 2026 — Current-Source Execution and Software Assurance Report

## 1. Scope and authority

Repository: `AhmedPeaRL/maximal-one`

Review branch: `review/type1-v4-remediation`

Execution commit: `c44b5eb607fb16313ade4550fa3d17e76279322c`

Target commit scanned: `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`

Main comparison commit: `160acfc8600b66c7300f2fd0caa500972de740b8`

This report records three completed workflows and their downloaded artifacts. It is an evidence record only.

It does not authorize occurrence adjudication, overlay application, protocol freeze, formal calibration, confirmatory execution, scientific claim support, promotion, or merge to main.

## 2. Completed workflow executions

### 2.1 Human-overlay preflight V5

- Workflow run: `43611117228`
- Job: `132496158534`
- Artifact ID: `14120126520`
- Artifact name: `type1-human-overlay-preflight-v5-43611117228-1`
- GitHub artifact digest: `sha256:c0643587e953ac80e54efd4fe403576e985415ce5dfed9143fae7ad6b5109b42`
- Artifact size: 1,208 bytes
- Internal report: `preflight-v5.json`
- Internal report SHA-256: `445cb6bcda483a15c16f697c795899fc40433123e884400c629fd77529a912f8`

Verified results:

- Current registered inventory and snapshot source identities verified.
- Target occurrence count: 1,800.
- Main comparison occurrence count: 939.
- Preflight CSV rows: 3.
- All three rows are `OPEN` and `PENDING`.
- `adjudications_applied = 0`.
- `authority = NONE`.
- `protocol_freeze = NOT_FROZEN`.
- Formal calibration and confirmatory execution remain unauthorized.
- Claim support and promotion authority remain false.

Occurrence IDs:

1. `refs/audit/target/2f8523fcf7c5/73/4`
2. `refs/audit/target/40d0253a5dd6/60/6`
3. `refs/audit/target/40d0253a5dd6/123/9`

Interpretation: source and pending-CSV preflight completed. No human review or adjudication was performed.

### 2.2 Target batch generation V4

- Workflow run: `43611052131`
- Job: `132495953608`
- Artifact ID: `14120730637`
- Artifact name: `type1-target-1800-batches-current-source-bound-43611052131-1`
- GitHub artifact digest: `sha256:2b4c88f3116b706b5503fa5e34065ab83e0407a9f07c41f7021c5c7e7b244bd1`
- Artifact size: 74,460 bytes
- Batch register: `BATCH_SET_REGISTER.json`
- Batch register SHA-256: `1d5c9ccb9ff73e6e97422be3e81521291e607a0b3b619815e4732a827f74eebe`

Independent artifact checks:

- 72 batch JSON files present.
- 25 occurrence IDs per batch.
- 1,800 occurrence IDs total.
- 1,800 unique IDs; zero duplicates.
- All 72 individual batch-file SHA-256 values match the batch register.
- All 72 canonical occurrence-sequence hashes match.
- Batch IDs are sequential from `BATCH_001` through `BATCH_072`.

Every batch retains:

- `status = NAVIGATION_ONLY_NOT_ADJUDICATED`
- `authority = NONE`
- `protocol_freeze = NOT_FROZEN`
- `formal_calibration_authorized = false`
- `confirmatory_execution_authorized = false`
- `claim_support = false`
- `promotion_authority = false`

Interpretation: source-bound navigation batches were generated and integrity-checked. They are not adjudications, scientific results, or execution authorization.

### 2.3 Software Assurance V3

- Workflow run: `43611097357`
- Job: `132496096128`
- Artifact ID: `14120366991`
- Artifact name: `type1-software-assurance-v3-43611097357-1`
- GitHub artifact digest: `sha256:3344863466d97a7a9144e5dcf28b259db9787e9c1d0bbbb2814b94185fa0c2a4`
- Artifact size: 38,443,043 bytes
- Manifest: `assurance-run-manifest.json`
- Manifest SHA-256: `422c1a1722108b1a74173224af39dd5d043e0f524a1272833210e5d10b638708`

Verified source binding:

- Target commit: `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`
- Review branch commit: `c44b5eb607fb16313ade4550fa3d17e76279322c`
- Snapshot run: `43573374439`
- Snapshot artifact: `14104988338`
- Snapshot archive SHA-256: `78d5ac9ca0dee723255f4684bf0a901613de19c4fec27bb9b621197ae8e1e79e`
- Snapshot certificate SHA-256: `9c3a84c4540bcbcffdf1b2114a577679c15243099816966973e2e15d3da452d1`
- Selected snapshot files: 289
- Scanner worktree was bound to the exact target commit by the workflow verification steps.

All 14 raw-output SHA-256 entries in the assurance manifest match their corresponding files in the downloaded artifact.

Scanner results:

| Scanner | Version | Exit code | Result |
|---|---:|---:|---|
| actionlint | 1.7.12 | 123 | 97 diagnostics |
| zizmor | 1.30.1 | 14 | 205 findings |
| OpenSSF Scorecard | 5.6.0 | 0 | Score 5.7/10 |

actionlint diagnostics:
- 97 total diagnostic headers.
- 92 ShellCheck diagnostics.
- 5 other actionlint diagnostics.

zizmor findings:
- 205 total.
- 164 High severity.
- 37 Medium severity.
- 4 Informational.
- Rule counts: `unpinned-uses` 151; `excessive-permissions` 19; `artipacked` 18; `template-injection` 13; `dangerous-triggers` 2; `cache-poisoning` 1; `superfluous-actions` 1.

Scorecard:
- Overall score: 5.7/10.
- Reported existing vulnerabilities: 73.
- Token-Permissions: 0.
- Pinned-Dependencies: 3.
- Security-Policy: 0.
- Fuzzing: 0.

Limitations:

- Nonzero actionlint and zizmor exit codes are findings, not clean passes.
- The successful workflow conclusion means the scanners completed and their outputs were uploaded; it does not mean the repository passed the scans.
- Scorecard reports `repo.commit = unknown`; its own JSON does not independently attest the scanned commit. The workflow's preceding source verification and the assurance manifest provide the surrounding source-binding evidence.
- The Scorecard JSON does not enumerate the 73 reported vulnerabilities in sufficient detail for individual closure.
- No finding is closed by this report.
- No security issue is declared fixed or harmless without path-specific review and supporting evidence.

## 3. Artifact integrity

The three downloaded ZIP archives passed ZIP integrity checks, and their SHA-256 values matched the GitHub artifact API digests.

The batch register independently verified all 72 batch-file hashes.

The assurance manifest independently verified all 14 raw scanner-output hashes.

## 4. Current decision

The three workflows completed successfully and produced source-bound evidence.

The following remain unchanged:

- Historical Type-I calibration: `NOT_PASSED`.
- Protocol freeze: `NOT_FROZEN`.
- Independent statistical review: pending.
- Independent software assurance review: pending.
- Human occurrence adjudication: pending.
- Formal calibration authorization: false.
- Confirmatory execution authorization: false.
- Scientific claim support: false.
- Promotion authority: false.
- Merge to main: not authorized by this report.

## 5. Mandatory next work

1. Preserve all three workflow artifacts and their original run identities.
2. Obtain independent software-security triage of the actionlint, zizmor, and Scorecard outputs.
3. Review the three preflight occurrence IDs individually using the exact target snapshot and full call paths.
4. Require reviewer expertise, conflict disclosure, reviewed/not-reviewed scope, evidence, rationale, and review timestamp.
5. Keep the CSV rows pending until the required independent review is complete.
6. Do not apply an overlay or convert navigation batches into adjudications automatically.
7. Keep statistical-methods review separate from software-security review.
8. Do not run AR20, freeze the protocol, or authorize confirmatory execution based on these engineering artifacts.

This report is an execution and evidence record only. It grants no scientific or operational authority.
