# Current Repository State Addendum — V10

**Snapshot date:** 2026-11-22 UTC  
**Repository:** `AhmedPeaRL/maximal-one`  
**Working branch:** `review/type1-v4-remediation`  
**Disposition:** `REVIEW_ONLY / DOCUMENTATION_RECONCILIATION / NO_WORKFLOW_AUTHORIZED`

## 1. Exact repository identity

The observed repository refs before this V10 commit are:

| Ref | Exact commit |
|---|---|
| `main` | `9749de9253f144eeda9e1b60cb219cfc5f201ecc` |
| `review/type1-v4-remediation` | `237844a6eea6d5055d5eefefde0f1b9c08d99284` |

The current review HEAD has a verified GitHub signature.

The two commits added after the previously recorded review HEAD `84d658a4aec1adb5fb11b9b11b86a1da4bb019c4` contain only:

1. `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261122_V9.md`
2. `docs/publications/HCM_WORKING_MANUSCRIPT_BINARY_IDENTITY_AUDIT_20261122_V1.csv`

No workflow YAML, application code, Dockerfile, scientific protocol, or scientific dataset was changed in these two commits.

The current comparison `main...review/type1-v4-remediation` reports:

- Status: diverged
- Review ahead: 730 commits
- Review behind: 36 commits
- Merge base: `a9808bd999a7ad902daf15606272529ca9af4580`

No merge, rebase, cherry-pick, promotion, or main-branch modification is authorized.

## 2. Workflow status and owner attestation

The owner reports that the following thirteen workflows are disabled in the live repository:

1. Emergent Periodicity Analysis
2. External Verification
3. Reproducible Research Gate
4. SOS Robustness Gate
5. Build and Push Container
6. Build and Publish Container
7. Cross Run Memory Verification
8. Immutable Release Lock
9. Evolution Engine
10. Canonical Sync
11. Cross Architecture Timing Test
12. Cross Architecture Timing
13. Validate Stress

This is recorded as:

`OWNER_ATTESTATION_NOT_INDEPENDENTLY_VERIFIED`

The available GitHub interface did not expose the server-side enabled/disabled state for every workflow. The owner's report is preserved without converting it into independent verification.

## 3. Validate Stress historical run

GitHub recorded Run `45013476170`:

- Workflow: `Validate Stress`
- Branch: `main`
- Commit: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- Event: `schedule`
- Conclusion: `success`
- Created: `2026-11-22T10:39:08Z`
- Job: `stress`, ID `137180672279`
- Uploaded artifacts: none

The workflow executed `npm install` and `npm run validate`.

The validation script generates a deterministic report from hard-coded constants. The `STRESS=true` environment variable is not consumed by that script.

This run is therefore not evidence of a substantive stress test, Type-I calibration, confirmatory analysis, empirical validation, replication, or scientific claim support.

The owner now reports that this workflow is disabled. No later Validate Stress run was observed in the reviewed recent run history.

## 4. Workflow execution authorization

`NO_WORKFLOW_IS_AUTHORIZED_FOR_MANUAL_OR_AUTOMATIC_EXECUTION_BY_THIS ADDENDUM.`

After this V10 documentation-only commit:

- Do not dispatch `software-assurance-exact-commit-v1.yml`.
- Do not dispatch `replication.yml`.
- Do not dispatch dependency or container workflows.
- Do not dispatch Type-I calibration, confirmatory, scientific validation, or promotion workflows.
- Do not use another workflow as a substitute or workaround.

Any future workflow authorization requires a separate explicit decision identifying the exact workflow path, exact branch, exact commit, intended scope, expected artifacts, and permitted side effects.

The review branch remains the only authorized branch for future review-only changes. `main` remains unchanged and must not be used as a target for remediation commits.

## 5. Main snapshot ZIP identity

The uploaded `maximal-one-main.zip` was inspected.

- Snapshot commit recorded inside archive: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- Entries: 1,166
- Archive integrity test: passed
- Size: 1,522,641 bytes
- SHA-256: `f59222d0eedd9073ea15ef51b1463c3926e7948fd0e8d417a536c78756634091`

This is a `main` snapshot, not a review-branch snapshot.

The archive contains a historical system-state manifest dated `2026-02-17`. Its release/build identity must not be interpreted as scientific validation or as closure of the HCM scientific claims.

## 6. Current manuscript binary identity

The review branch now contains:

`docs/publications/HCM_WORKING_MANUSCRIPT_BINARY_IDENTITY_AUDIT_20261122_V1.csv`

The three newly supplied working PDFs have the following identities:

| Paper | Uploaded SHA-256 | Pages |
|---|---|---:|
| 01 | `fb97104ce381683d9721657f3bdd6abe32ce9b2629043b9965826e388724dd29` | 7 |
| 08 | `d65046a5fac10fcb928b014f3df381c85571211ee93f18fde461b7cd254c6912` | 33 |
| 10 | `da954d5bfb7525e6aa3f77771e81f71b08ee1b3fda5b3df945e06943905bd4b5` | 16 |

Their normalized extracted text matches the corresponding local ZIP candidates, but their bytes are not identical.

Paper 01 is byte-identical to the existing Library working copy. Paper 08 and Paper 10 have not yet been added to the Working Manuscripts Library folder.

Local candidate-to-repository-registry MD5 agreement does not establish direct identity with the published Zenodo binaries.

Direct Zenodo API retrieval was attempted for all ten record identifiers, but the available retrieval interface returned inaccessible or cache-miss responses. These failures do not establish record absence or deletion.

Paper 04 and Paper 08 title-to-record associations remain unresolved. Papers 07 and 09 remain distinct records and must not be merged.

## 7. Publication closure status

Administrative archive closure remains open pending direct retrieval and hashing of the published Zenodo binaries, resolution of title associations, and reconciliation of the relevant metadata.

Scientific closure remains `NOT_ESTABLISHED`.

The ten papers are conceptual/theoretical publications, not empirical validation reports. No independent peer review of the ten papers or independent empirical validation of HCM consciousness/causal claims has been established.

No paper may be described as scientifically validated, independently peer reviewed, or empirically confirmed on the basis of repository consistency, local PDF identity, Zenodo metadata, or software assurance alone.

## 8. Human independent review

The four requested review scopes remain pending:

- Demetrios Politis: prospective Type-I statistical-methods review.
- Ali Machiry: GitHub Actions and CI/CD security review.
- Annika Seppälä: climate-domain independence review, with HadUKP EWP as the corrected candidate.
- Benjamin Wong: econometric-domain review, with CPIAUCNS pre-gap as the corrected candidate.

No substantive independent report was found in the reviewed Gmail threads.

Benjamin Wong's automated out-of-office reply dated 2026-11-15 is not a review report.

The climate and economic candidate corrections supersede the earlier HadCET and INDPRO candidate framing. Their independence, provenance, prior-exposure, and null-adequacy questions remain unresolved.

## 9. Container security

Run 36 (`44948856035`) remains the latest observed review-branch software-assurance run.

Its bounded software-assurance and OSV jobs succeeded; its container job was skipped.

Run 35 (`44944152951`) built the container and passed CLI smoke testing, but the Trivy HIGH/CRITICAL gate failed.

The container security gate remains `OPEN`.

Do not modify the Dockerfile, suppress Trivy findings, or mix Debian Forky/Sid packages into the Debian Trixie base without a separately reviewed remediation plan.

## 10. Library status

The Working Manuscripts folder currently contains Paper 01 only.

The Publications and Provenance folder exists but is empty.

The four V8 handoff files are present in the Library root.

Earlier Project Library move/delete operations were rejected. No files were moved or deleted.

No historical evidence or duplicate-looking files are to be deleted solely on the basis of filename or size. Any future cleanup requires byte-level identity confirmation and a supported Project Library operation.

## 11. Required next actions

1. Add this V10 addendum to `review/type1-v4-remediation` only.
2. Preserve V9 and the manuscript identity CSV unchanged.
3. Do not modify `main`.
4. Do not modify workflow YAML, Dockerfile, application code, scientific protocols, datasets, or DOI records.
5. Do not execute any workflow after this documentation-only commit.
6. Send the exact V10 commit URL for read-only verification.
7. After Library upload throttling expires, add Paper 08 and Paper 10 to `Working Manuscripts - Binary Identity Pending`.
8. Obtain direct Zenodo published PDF binaries and hashes.
9. Resolve Paper 04 and Paper 08 title-to-record identity.
10. Await attributable written reports from the four independent reviewers.
11. Keep Type-I calibration, confirmatory execution, replication, claim support, and promotion unauthorized.

## 12. Closure vocabulary

Use only:

- `CLOSED_ADMINISTRATIVELY`
- `PASS_SCOPE_LIMITED`
- `OPEN`
- `PENDING_INDEPENDENT_REVIEW`
- `OWNER_ATTESTATION_NOT_INDEPENDENTLY_VERIFIED`
- `NOT_AUTHORIZED`
- `NOT_ESTABLISHED`

No global 100% assurance, scientific validation, empirical confirmation, or peer-review closure is claimed.
