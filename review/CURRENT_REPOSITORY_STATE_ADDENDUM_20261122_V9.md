# Current Repository State Addendum — V9

**Snapshot date:** 2026-11-22 UTC  
**Repository:** `AhmedPeaRL/maximal-one`  
**Working branch:** `review/type1-v4-remediation`  
**Disposition:** `REVIEW_ONLY / DOCUMENTATION_RECONCILIATION / NO_WORKFLOW_AUTHORIZED`

## 1. Current branch identity

| Ref | Exact commit |
|---|---|
| `main` | `9749de9253f144eeda9e1b60cb219cfc5f201ecc` |
| `review/type1-v4-remediation` | `84d658a4aec1adb5fb11b9b11b86a1da4bb019c4` |

The latest review commit is dated 2026-11-22 14:05:58 UTC. GitHub reports signature verification `verified=true`, reason `valid`.

The comparison `main...review/type1-v4-remediation` reports: diverged; review ahead by 728 commits and behind by 36; merge base `a9808bd999a7ad902daf15606272529ca9af4580`.

No merge, rebase, cherry-pick, promotion, or main-branch modification is authorized.

## 2. Documentation delta after Run 36

Run 36 (`44948856035`) scanned `99dd702ce4f7569e19b55503506b3bbfe8c920fa`.

The comparison from that scan commit to current review HEAD reports eight commits ahead and eight added files:

1. `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261121_V6.md`
2. `evidence/EXACT_ASSURANCE_RUN_44948856035_REVIEW.csv`
3. `docs/publications/ZENODO_API_METADATA_CAPTURE_20261121_V1.csv`
4. `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261121_V7.md`
5. `docs/publications/HCM_PUBLICATION_CLOSURE_AUDIT_20261122_V1.md`
6. `evidence/CONTAINER_SECURITY_REVIEW_20261122_V1.md`
7. `evidence/EXACT_ASSURANCE_RUN_44948856035_REVIEW_V2.csv`
8. `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261122_V8.md`

No workflow YAML, application code, Dockerfile, scientific protocol, or scientific dataset changed in this delta.

V8 is stale by construction: its text records the previous review HEAD `b441ce43a9221fc7c0922dd78a7a75777505fb39`. Preserve V8 and V7 as historical evidence. This V9 supersedes V8.

## 3. Main scheduled workflow run discovered

GitHub Actions recorded `Validate Stress`, Run `45013476170`, on `main`, commit `9749de9253f144eeda9e1b60cb219cfc5f201ecc`.

- Event: `schedule`
- Conclusion: `success`
- Created: `2026-11-22T10:39:08Z`
- Job: `stress` (`137180672279`)
- Artifacts: none

This corrects the earlier broad statement that no recent main workflow run occurred. The event is scheduled, not a manual dispatch. No main-branch commit change was observed.

The workflow runs `npm install` and `npm run validate`. The latter executes `core-scientific/publication-gate/generate-report.cjs`, which constructs a report from hard-coded constants, canonicalizes it, hashes it, and writes two files in the ephemeral runner workspace.

The `STRESS=true` environment variable is not consumed by this script. The run is a deterministic report-generation smoke path, not a stress test, Type-I calibration, confirmatory analysis, empirical test, replication, or scientific validation.

The workflow declares a weekly schedule (`0 3 * * 0`) and no `workflow_dispatch` trigger. It is not among the owner's twelve disabled workflows. Disable it through the repository Actions UI if further scheduled execution is not authorized.

## 4. Workflow authorization

No `.yml` workflow is authorized for manual execution after the next V9 documentation-only commit.

The owner reports twelve workflows remain disabled. Their status remains `OWNER_ATTESTATION_NOT_INDEPENDENTLY_VERIFIED`, because the available GitHub interface did not expose the server-side enable/disable state for each workflow.

`External Verification` (`.github/workflows/run.yml`) declares an hourly schedule. The owner reports it disabled; independent server-side verification remains unavailable.

The review-branch software-assurance dispatcher exists on both branches. Its review version requires `scan_commit` to equal the selected review HEAD. The main version contains a stale default and must not be used for review scanning. The current review dispatcher does not expose `run_container_review` as a manual-dispatch input.

A future review-only reusable workflow can be invoked through a caller that exists on the default branch and on the selected review branch, using the review branch's caller definition and a local reusable-workflow path. This mechanism is not authorized for use now.

## 5. Human review

No substantive independent report was found from Demetrios Politis, Ali Machiry, Annika Seppälä, or Benjamin Wong.

Benjamin Wong's only inbound response located remains an automated out-of-office message dated 2026-11-15, stating conference commitments through 2026-11-29. Automated replies are not independent reviews.

No independent peer review of the ten conceptual HCM papers has been established.

## 6. Publication and manuscript identity

The ten local candidate PDFs match the repository publication registry by MD5. This is local candidate-to-registry agreement, not direct Zenodo published-binary verification.

The newly attached Paper 01, Paper 08, and Paper 10 PDFs have normalized extracted text identical to the corresponding PDFs in the ten-paper ZIP, but their bytes differ from the ZIP candidates.

Paper 01 is byte-identical to the working PDF already stored in Library. Paper 08 and Paper 10 are not yet in the Working Manuscripts Library folder; attempted uploads were throttled.

Paper 04 and Paper 08 title/record associations remain unresolved. Papers 07 and 09 share a title but remain separate DOI records and documents.

The ten papers remain conceptual/theoretical publications, not empirical validation reports. No independent peer review or empirical validation of HCM consciousness/causal claims is established. Administrative archive reconciliation is not scientific closure.

## 7. Container security

Run 36 remains the latest observed review-branch workflow run. It passed bounded software-assurance and OSV jobs; its container job was skipped.

Run 35 (`44944152951`) built the container and passed CLI smoke, but Trivy failed the configured HIGH/CRITICAL gate with 50 HIGH package-occurrence records representing 12 distinct CVEs and zero CRITICAL records.

The container security gate remains OPEN. Do not edit the Dockerfile or mix Forky/Sid packages into Debian Trixie. Do not suppress Trivy findings.

## 8. Library status

The four V8 handoff files are present in the Library root, correcting V8's stale statement that the four files were not in Library.

A `Publications and Provenance` folder was created. File moves and deletions were rejected by the Project Library mutation interface; no files were moved or deleted. Uploads of Paper 08 and Paper 10 were throttled with a four-hour retry window.

Paper 01's existing Library working copy is byte-identical to the newly attached Paper 01 file.

Exact duplicate content was verified for the root V6 addendum and its Historical Evidence copy, the root V1 Run 36 review CSV and its Historical Evidence copy, and three Run 35 artifact ZIPs. No deletion was performed because the Project Library mutation interface rejected the operation.

## 9. Required next actions

1. Disable `Validate Stress` through the repository Actions UI if further scheduled execution is not authorized.
2. Verify that the twelve owner-listed workflows show disabled state in Actions.
3. Add this V9 file and its supporting review records to `review/type1-v4-remediation` only.
4. Do not edit `main`, workflow YAML, Dockerfile, application code, scientific protocol, datasets, or DOI records.
5. After the V9 documentation-only commit, run no `.yml` workflow. Send the exact commit URL for read-only verification.
6. After the Library upload throttle expires, upload Paper 08 and Paper 10 to `Working Manuscripts - Binary Identity Pending`.
7. Wait for attributable written reports from the four independent reviewers.
8. Obtain direct Zenodo PDF binaries and hashes, resolve Paper 04/08 title identity, and complete citation/construct review before any publication-closure claim.

No Type-I calibration, confirmatory execution, replication, claim support, or promotion is authorized.

## 10. Closure vocabulary

Use only: `CLOSED_ADMINISTRATIVELY`, `PASS_SCOPE_LIMITED`, `OPEN`, `PENDING_INDEPENDENT_REVIEW`, `OWNER_ATTESTATION_NOT_INDEPENDENTLY_VERIFIED`, `NOT_AUTHORIZED`, `NOT_ESTABLISHED`.

No global 100% assurance, scientific validation, empirical confirmation, or publication peer-review closure is claimed.
