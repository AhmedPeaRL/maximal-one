# HCM Current Repository and Evidence State Addendum — V14

- Evidence date: 2026-11-23
- Repository: `AhmedPeaRL/maximal-one`
- Scope: owner-attestation update and bounded post-V13 repository/archive verification
- Disposition: `REVIEW_ONLY / SECURITY_OPEN / HUMAN_REVIEW_PENDING / NO_WORKFLOW_AUTHORIZED`

## 1. Exact repository state checked for this addendum

The GitHub repository API and compare endpoint report:

- Default branch `main`: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`.
- Review branch `review/type1-v4-remediation`: `abc08a203d8649ead0f30ac23c226a6ad91db535`.
- Review is 735 commits ahead of `main` and 36 commits behind it.
- Merge base: `a9808bd999a7ad902daf15606272529ca9af4580`.
- Current Review commit message: `Record V13 current repository and evidence state`.
- The current Review commit adds exactly two documentation files:
  - `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261123_V13.md`
  - `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261123_V13.sha256`

The V13 files are preserved unchanged. This V14 is a supplemental correction/update; it does not replace or rewrite V12, V1, or V13. No change to `main` is indicated by the current compare result. The owner separately attests that no new changes or workflow runs were made on `main` during the latest rounds.

Commit URL:
`https://github.com/AhmedPeaRL/maximal-one/commit/abc08a203d8649ead0f30ac23c226a6ad91db535`

## 2. Current uploaded archive identity and bounded alignment

### Main archive

- Uploaded filename: `maximal-one-main(20261122-212012).zip`
- SHA-256: `f59222d0eedd9073ea15ef51b1463c3926e7948fd0e8d417a536c78756634091`
- ZIP integrity: pass (`testzip() == None`)
- ZIP comment identifies main commit `9749de9253f144eeda9e1b60cb219cfc5f201ecc`.
- Entries: 1,166; files: 1,051; uncompressed bytes: 3,939,438.

### Current Review archive

- Uploaded filename: `maximal-one-review-type1-v4-remediation(20261123-164909).zip`
- SHA-256: `02d43033ff274d3278f49a9119e99fd0a4b3c8fe1338b4b95c75accccb35fbfb`
- ZIP integrity: pass (`testzip() == None`)
- ZIP comment identifies current Review commit `abc08a203d8649ead0f30ac23c226a6ad91db535`.
- Entries: 1,447; files: 1,325; uncompressed bytes: 22,654,792.
- The archive contains the V13 Markdown and SHA-256 manifest. The document's SHA-256 is `60585ee350438354c4b6f73162bd727a7b3544405e637252201b5d073d8b0b47`; the embedded manifest matches.
- The current archive and GitHub commit are aligned by the ZIP comment, the GitHub commit/file retrieval, and matching Git blob identity for the V13 Markdown. This is not a full byte-for-byte comparison of every file in the archive against every Git tree blob.

Static checks on the current Review archive:

- 52 root workflow YAML definitions parsed successfully with PyYAML; zero parse errors.
- 41 root workflow files contain `workflow_dispatch`.
- 572 Python files passed `ast.parse`.
- 157 JSON files parsed successfully.

These are bounded syntax/inventory checks. They do not prove semantic correctness, workflow enablement, runtime behavior, security closure, or scientific validity.

## 3. Owner's updated 13-workflow disabled attestation

After the V13 commit, the repository owner explicitly reconfirmed that **all 13** of the following workflows remain disabled in the live GitHub system:

1. Emergent Periodicity Analysis
2. External Verification
3. Reproducible Research Gate
4. SOS Robustness Gate
5. Build and Push Container — current name on `main`
6. Build and Publish Container — current name on `review/type1-v4-remediation`
7. Cross Run Memory Verification
8. Immutable Release Lock
9. Evolution Engine
10. Canonical Sync
11. Cross Architecture Timing Test
12. Cross Architecture Timing
13. Validate Stress

Evidence classification: `OWNER_ATTESTATION_NOT_INDEPENDENTLY_VERIFIED`.

This explicitly resolves the omission in V13: `Validate Stress` is included in the current owner attestation. The current `validate-stress.yml` definitions on both `main` and Review are schedule-only, with cron `0 3 * * 0`; neither has `workflow_dispatch`. The owner attests the workflow is disabled. The YAML definition alone cannot establish its GitHub enabled/disabled setting.

The owner also attests:
- no new changes or workflow runs were made on `main` during the latest rounds;
- no newer scientific snapshot has been submitted;
- no workflow has been run after the previously documented V12 boundary;
- the four requested independent human review reports remain outstanding.

These are owner statements, not independently exhaustive GitHub audit-log proofs.

## 4. Workflow authorization — none

**No `.yml` workflow is authorized to run at current Review HEAD `abc08a203d8649ead0f30ac23c226a6ad91db535`.** This includes workflows with `workflow_dispatch`, reusable workflows, scheduled workflows, and workflows not included in the 13-item disabled list.

In particular:

- Do not dispatch `replication.yml` as a workaround.
- Do not enable any workflow to obtain a scan or build.
- Do not run Type-I preflight, batch generation, calibration, confirmatory, replication, scientific-claim, or publication workflows.
- Do not create a pull request or another push-triggered event as a substitute for an explicitly authorized workflow.
- No `.yml` file is being nominated for execution in this addendum.

The Review `.github/workflows/build-image.yml` currently has an unfiltered `push` trigger. If enabled, a documentation-only push to Review can trigger build and stability-check jobs. Its publish job is restricted to `main`. The owner attests this workflow is disabled. **Before any future Review push, the owner must manually re-check that `Build and Publish Container` is still disabled.** This is a hard precondition, not a workflow-run authorization.

The Main `.github/workflows/build-image.yml` is a separate, older `Build and Push Container` workflow with `push` and `pull_request` triggers. No `main` change or push is authorized.

## 5. Bounded Gmail check and independent reviewers

Targeted Gmail searches for GitHub Actions notifications after 2026-11-22 returned no matching messages in the connected mailbox. The latest relevant GitHub Actions notifications found by the searches inspected here were dated before that cutoff (including the previously documented runs on 2026-11-20 and 2026-11-21).

This is a bounded mailbox search, not a complete GitHub Actions run enumeration. The current connector surface did not provide a complete all-event workflow-run listing. The owner's no-post-V12-run attestation is retained separately.

Targeted searches for recent inbound correspondence from two known reviewer addresses and for recent inbound review-report terms returned no new substantive review report. The project owner reports that all four requested independent reviews remain pending. Reviewer status remains `PENDING`; do not infer rejection, silence beyond the searched mailbox scope, or acceptance.

## 6. Evidence Library access

The project-specific Library folder was successfully listed at:

`/Hybrid Consciousness Model - HCM/Current Evidence/`

It contains the Zenodo paper archive, the combined Termux verification source/transcript, Trivy reports for runs `44828421411` and `44944152951`, OSV inventories, exact-commit assurance artifacts, and the V6 residual review register. The current Review ZIP supplied in this turn is a conversation upload and is not represented here as already stored in the Library.

The earlier Zenodo binary result remains `PASS_SCOPE_LIMITED`: the owner-supplied Termux transcript reports matching sizes, PDF signatures, Zenodo MD5 values, Registry MD5 values for the ten paper PDFs, and SHA-256 recomputation against the separately stored Library archive. This does not establish independent acquisition by the assistant from Zenodo, scientific validity, or peer review. The verification script should be hardened to fail closed before reuse.

## 7. Security and scientific gates remain open

The prior V13 findings remain in force:

- Container security remains `OPEN`. The latest preserved Trivy report records 50 HIGH finding records across 12 unique CVEs and zero CRITICAL findings. The Debian Security Tracker check dated 2026-11-23 found all 12 CVEs still marked vulnerable for the Trixie package versions present in that image.
- Do not suppress Trivy findings, mix Forky/Sid packages into Trixie, or change the Dockerfile until official Trixie fixes, package provenance, and compatibility are reviewed.
- The historical Docker build filename issue appears addressed by the current `find`-based filename discovery, but no later authorized build has verified the fix.
- The `reports/` directory creation defect in the always-run exact-assurance manifest step remains a documented future workflow remediation item; no YAML edit or run is authorized here.
- `env/fingerprint.py` still has a bounded hardening recommendation to replace constant `shell=True` subprocess calls with argv lists and `shell=False`.
- `api/public_reproduce_endpoint.py` remains a latent high-priority risk before any exposure because it clones mutable `main`, installs dependencies without `--require-hashes` or an isolated virtual environment, and executes repository code. Deployment/external exposure remains unknown.

Scientific status remains unchanged:

- Type-I protocol freeze: `NOT_FROZEN`.
- Formal calibration: `NOT_AUTHORIZED`.
- Confirmatory execution: `NOT_AUTHORIZED`.
- Replication: `NOT_AUTHORIZED`.
- Scientific claim support/promotion: `NOT_ESTABLISHED / NONE`.
- Independent peer review: `PENDING` (four requested reports).
- No new scientific snapshot is authorized or required by this V14 addendum.

## 8. Required next actions

1. Preserve V12, V1, and V13 unchanged.
2. If adopting this V14, add only the two V14 documentation files to `review/type1-v4-remediation`; do not change `main`.
3. Immediately before that Review push, manually verify `Build and Publish Container` remains disabled. Do not push if that setting cannot be confirmed.
4. After a V14 documentation commit, do not run any workflow. No `.yml` is authorized.
5. Continue preserving current Trivy/OSV/assurance evidence and monitor official Debian Trixie security updates; do not modify the Dockerfile or suppress findings without a separately reviewed and authorized remediation.
6. Keep all four independent human reviews pending until actual reports are received and assessed.
7. Do not authorize protocol freeze, calibration, confirmatory execution, replication, or scientific claim promotion until independent review and formal governance requirements are satisfied.

No claim of 100% assurance, complete security closure, scientific truth, empirical confirmation, or completed peer review is made.
