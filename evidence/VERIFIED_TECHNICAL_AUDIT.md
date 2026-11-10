# Verified Technical Audit — Type-I V4 Remediation
**Audit date:** 2026-11-09  
**Repository:** `AhmedPeaRL/maximal-one`  
**Commit inspected:** `8ea2a4a13abfab4d4bf36d2aa64e79dafce87ab6`

## Executive decision

**Engineering remediation: PASS for the specific generated-evidence exclusion defect.**  
**Exact snapshot integrity: PASS for the declared 289-file scope.**  
**Human adjudication: NOT DONE.**  
**Statistical protocol approval/freeze: NOT DONE.**  
**Formal calibration / confirmatory execution: NOT AUTHORIZED.**  
**Claim support / promotion: FALSE.**

This is a bounded technical verification, not a scientific conclusion.

## A. Commit and workflow changes

Commit `8ea2a4a13abfab4d4bf36d2aa64e79dafce87ab6` adds the generated-exclusion regression test to:
- governance audit workflow path filters and compile/test steps;
- implementation snapshot required-file list and path filters;
- snapshot completeness regression test.

The implementation artifact confirms `file_count = 18`; its 18 source files and internal checksums verify. Both `.github` workflow files are included in the snapshot; `include-hidden-files: true` is retained.

## B. Workflow outcomes

| Workflow run | Job | Result |
|---|---:|---|
| `42523663514` | `128862392846` | Success; 31 tests passed |
| `42523663482` | `128862392599` | Success; 18-file implementation snapshot |
| `42523935885` | `128863209001` | Success; binary-safe tests 2/2, generated-exclusion tests 2/2 |
| `42524103929` | `128863716926` | Success; snapshot identity tests 9/9 and exact snapshot uploaded |

Warnings in the logs concern Node.js action runtime deprecations and Python dependency tooling; no test failure or artifact integrity failure was observed in these jobs.

## C. Inventory results

Provenance binds:
- target commit: `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`;
- main commit: `00bbd1fbd6df41b3e988ace75c480ea6232cfb86`;
- inventory workflow-definition commit: `8ea2a4a13abfab4d4bf36d2aa64e79dafce87ab6`;
- inventory run: `42523935885`;
- inventory artifact: `13634199148`.

The target inventory contains 1,800 occurrences across 271 files with matches. Twelve paths were excluded from line-based occurrence discovery: nine generated text files, two earlier explicit exclusions, and one binary ZIP. All twelve are retained in the exact snapshot scope and hash-verified.

The main inventory contains 633 occurrences across 184 files with matches and zero scanner exclusions.

Both reconciliation reports are `RECONCILED`, with exact expected/observed counts and no missing, extra, duplicate, or identity-mismatched IDs.

Every target row remains:
- `status = OPEN`
- `manual_classification = UNKNOWN`
- `reviewer_disposition = PENDING`
- `can_influence_execution = UNKNOWN`
- `guard_fails_closed = UNKNOWN`
- `historical_diagnostic_proposed_governance_status = UNDETERMINED`

The same unresolved defaults apply to all 633 main rows. Manual adjudication overlay records remain zero.

## D. Exact snapshot integrity

The snapshot run checked out the requested target commit rather than the dispatch/workflow-definition commit. The three-way certificate binds:
- target = `ad106...`;
- inventory source = `ad106...`;
- snapshot review = `ad106...`.

The inventory workflow-definition commit and snapshot workflow-definition commit are both `8ea2a4a...`.

Manifest:
- selected scope: 289;
- present: 289;
- missing scope: 0;
- missing required: 0;
- scanner exclusions: 12;
- protocol freeze: `NOT_FROZEN`;
- formal calibration: false;
- confirmatory execution: false;
- claim support: false;
- promotion authority: false.

The nested self-contained archive has 294 ZIP members and passes CRC validation. Its 292 SHA-256 entries all verify. The separate 289 repository-source checksum lines also match the corresponding source files in the nested archive. All twelve scanner-excluded paths are present in the snapshot.

Important field distinction: snapshot manifest `excluded_paths: []` is the missing-scope list and means no selected-scope files were omitted. Scanner exclusions are separately represented by `scanner_exclusions` (count 12).

## E. Current automated-discovery workload

The target inventory labels:
- 3 workflow runner-invocation candidates;
- 253 code-path occurrences requiring call-graph review;
- 118 workflow-control-path occurrences.

The 3 runner candidates are:
1. `.github/workflows/type1-calibration-runtime-pilot.yml:73`
2. `.github/workflows/type1-v4-cross-runner-worker-order.yml:60`
3. `.github/workflows/type1-v4-cross-runner-worker-order.yml:123`

These labels are not proof of authorization or safety. In the exact snapshot, the runtime-pilot workflow is `workflow_dispatch`-triggered and includes a branch guard; the cross-runner workflow restricts push execution to the remediation branch and uses an `--engineering-test` argument. These observations are not enough to declare every reachable path safe. A human governance reviewer must trace the guard implementation, all callers, alternate/legacy workflows, outputs, artifact behavior, and negative tests.

## F. Branch topology

The compare endpoint reports `review/type1-v4-remediation` as diverged from `main`: 350 commits ahead and 19 behind. Do not merge the entire review branch into `main` as a shortcut. The current review snapshot is an immutable historical target; changes to the branch after this snapshot do not alter the snapshot, but any review of those later changes requires a new exact identity.

## G. Remaining blockers before meaningful scientific execution

1. Obtain an attributable independent statistical-methods review against the exact snapshot and digests.
2. Obtain a separate governance/engineering review of execution paths and occurrence evidence.
3. Resolve the acceptance-rule conflict prospectively, including Wilson sidedness, confidence level, threshold rationale, multiplicity, sample size, invalid-attempt handling, and scenario coverage.
4. Preserve historical V1 `NOT_PASSED` outcomes under the historical two-sided rule; do not retrofit the `0.075` ceiling.
5. Record any required amendments in a new prospective version; do not edit the historical snapshot.
6. Freeze the exact amended protocol only after independent review and explicit author decision.
7. Issue a separate execution authorization bound to exact code, workflow, matrix, dependency, and protocol digests.
8. Run formal calibration only after those gates; then pursue independent eligible real-domain replication separately.

No new statistical result, independent replication, or HCM consciousness evidence is produced by these governance workflows.

## H. Public endpoints not verified

The GitHub connector successfully fetched the commit, compare metadata, workflow job summaries/logs, and all three artifacts. Direct browser access to the GitHub profile, GitHub `.git` endpoint, and GitHub Pages endpoint returned cache-miss errors in this session. No full Git clone or live Pages rendering was verified. Do not represent those endpoints as inspected successfully.
