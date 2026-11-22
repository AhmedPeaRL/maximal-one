# Current Repository State Addendum — V8

**Snapshot date:** 2026-11-22 UTC  
**Repository:** `AhmedPeaRL/maximal-one`  
**Working branch:** `review/type1-v4-remediation`  
**Disposition:** `REVIEW_ONLY / DOCUMENTATION_RECONCILIATION / NO_WORKFLOW_AUTHORIZED`

## 1. Evidence and authority boundaries

This addendum distinguishes GitHub API observations, local uploaded archives/artifacts, owner attestations, external Debian security-tracker research, and unresolved items. A successful software scan is not scientific validation. A clean source-manifest inventory is not a container-image scan. A DOI is not peer review or empirical confirmation. An owner attestation is not independent retrieval of a GitHub Actions setting.

## 2. Current GitHub branch state

| Ref | Exact commit |
|---|---|
| `main` | `9749de9253f144eeda9e1b60cb219cfc5f201ecc` |
| `review/type1-v4-remediation` | `b441ce43a9221fc7c0922dd78a7a75777505fb39` |

The `main` commit API record is dated 2026-11-15 and has GitHub signature verification `verified=true`. Main HEAD matches the last previously observed main HEAD. The owner additionally attests that no new main-branch changes or workflow runs were made in the latest rounds.

The comparison between `main` and the review branch reports: diverged; review branch ahead by 724 and behind by 36; merge base `a9808bd999a7ad902daf15606272529ca9af4580`.

Run 36 scanned `99dd702ce4f7569e19b55503506b3bbfe8c920fa`. The comparison from that commit to current review HEAD `b441ce43a9221fc7c0922dd78a7a75777505fb39` reports exactly four commits ahead and exactly four added files:

1. `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261121_V6.md`
2. `evidence/EXACT_ASSURANCE_RUN_44948856035_REVIEW.csv`
3. `docs/publications/ZENODO_API_METADATA_CAPTURE_20261121_V1.csv`
4. `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261121_V7.md`

No application code, workflow YAML, Dockerfile, scientific protocol, or scientific dataset changed in this four-commit delta. It is documentation/evidence-only.

**V7 correction:** V7 was written before its own upload and records the earlier review HEAD `77400bfcd18974a49711138d7061bc93ee9b0040`. V7 is now historical and stale as a current-state document. Preserve V7 as immutable history; this V8 supersedes it. Do not silently rewrite V7.

### Uploaded main archive

The supplied `maximal-one-main.zip` passes ZIP integrity testing and contains 1,166 entries. It contains 52 workflow YAML files under the root `.github/workflows/` tree and two additional YAML files under `core-scientific/.github/workflows/`. SHA-256:

`f59222d0eedd9073ea15ef51b1463c3926e7948fd0e8d417a536c78756634091`

The ZIP contains no `.git` directory or embedded commit SHA. Its name identifies it as a main-branch archive, but the ZIP alone is not a cryptographic binding to exact main HEAD. Use the GitHub API commit SHA as the branch identity anchor.

Direct HTML retrieval of the GitHub profile, branch pages, and GitHub Pages site returned `Cache miss` in this review environment. GitHub API operations succeeded. The rendered Pages site was not independently inspected.

## 3. Workflow run state and artifacts

The latest eight workflow-run records for the review branch show Run 36 as the newest observed run. No run newer than Run 36 was found.

| Run | ID | Scanned commit | Conclusion | Result |
|---|---:|---|---|---|
| 36 | `44948856035` | `99dd702ce4f7569e19b55503506b3bbfe8c920fa` | success | Software assurance and OSV inventory succeeded; container job skipped |
| 35 | `44944152951` | `48b223e8d5192ed133ba1f0e59493b6e36600950` | failure | Software assurance and OSV succeeded; container build and CLI smoke succeeded; Trivy gate failed on HIGH findings |

### Run 36

- Software assurance artifact ID `14724383591`; ZIP SHA-256 `9802a450328b3174047062496c21e10af21a340256764215f013135c804390fd`.
- OSV artifact ID `14725360055`; ZIP SHA-256 `1d3aaa89287d26325e2810b6ad6fc7567cc5a418b759f52cc31c7a883eb6a604`.
- actionlint 1.7.12: exit 0; output empty; three explicit ignores are limited to same-repository reusable-workflow syntax.
- zizmor 1.30.1: exit 0; JSON findings array empty; run was explicitly offline, so this is not a complete online threat assessment.
- OpenSSF Scorecard 5.6.0: 9.2/10. Fuzzing 0/10; License 9/10 because the scanner did not recognize an FSF/OSI license identifier; Token-Permissions 10/10 with three `contents:write` warnings.
- OSV-Scanner 2.7.1: valid JSON, zero findings in supported source manifests. It scanned five Python requirements files and `package-lock.json` (zero packages). It did not scan Debian OS packages or the container image.
- Assurance manifest: `protocol_freeze=NOT_FROZEN`; formal calibration false; confirmatory execution false; claim support false; promotion authority false; authority `NONE`.

Run 36 skipped the container build and Trivy scan. It does not close image security.

### Run 35 container result

Run 35 job `136967775346` built the image and passed the CLI smoke test. Trivy v0.76.2 then returned exit code 1 under the configured `HIGH,CRITICAL`, `ignore-unfixed=false` gate.

- Trivy artifact ID `14723121334`.
- Artifact ZIP SHA-256 `657ba2a2f687611c3ea5643ec128ab2fc1badd3cf0783dd8acba645415f791d7`.
- Extracted JSON size 599,459 bytes.
- Image ID `sha256:57264f61530dd7711c4b30b3f5a869a86c1c66631fb4c1e3d6d19d46b34f5793`.
- Debian 13.7; image size 976,166,912 bytes.
- 50 HIGH vulnerability records, 12 distinct CVEs, zero CRITICAL records.

The detailed package/CVE review is `evidence/CONTAINER_SECURITY_REVIEW_20261122_V1.md`. The container security gate remains OPEN.

## 4. Workflow authority and branch-specific dispatch

**No workflow is authorized to run after the next documentation-only commit.** This includes software assurance, container review, WDC-SILSO source audit, dependency refresh, replication, Type-I calibration, confirmatory analysis, validation, and promotion. Do not dispatch merely because the UI offers a Run button.

The owner reports these 12 workflows remain disabled:

1. Emergent Periodicity Analysis
2. External Verification
3. Reproducible Research Gate
4. SOS Robustness Gate
5. Build and Push Container (current name on `main`)
6. Build and Publish Container (current name on remediation branch)
7. Cross Run Memory Verification
8. Immutable Release Lock
9. Evolution Engine
10. Canonical Sync
11. Cross Architecture Timing Test
12. Cross Architecture Timing

Status: `OWNER_ATTESTATION_NOT_INDEPENDENTLY_VERIFIED`. The GitHub connector used here did not expose server-side workflow enable/disable state. File presence in a branch archive does not establish whether a workflow is enabled or disabled.

### Relevant workflow files inspected read-only

- `.github/workflows/software-assurance-exact-commit-v1.yml` exists on both branches. The review version has `workflow_dispatch`, requires `scan_commit`, has no default, and guards that the input equals the selected review-branch HEAD. The `main` version has stale default SHA `3a158e8f902179cdd543e92153032ae409faaea0`; never use that default for a review scan.
- `run_container_review` is a `workflow_call` input in the review version, not a `workflow_dispatch` input. The container child cannot be enabled through the manual UI input.
- `.github/workflows/dependency-vulnerability-inventory.yml` is `workflow_call` only.
- `.github/workflows/container-cli-smoke-review.yml` is `workflow_call` only, review-branch guarded, and not independently manually dispatchable.
- `.github/workflows/wdc-silso-source-audit-v1.yml` exists on both branches with different definitions; the review version is stricter. It is not authorized to run.
- `.github/workflows/replication.yml` is not one of the owner's 12 disabled workflows, but remains explicitly unauthorized to dispatch or modify. Do not use it as a workaround.

GitHub documents that a `workflow_dispatch` file must exist on the default branch for the manual Run workflow UI to be available, and that the run uses the workflow version associated with the selected ref. Thus a workflow file existing only on the review branch cannot independently expose a Run workflow button while absent from `main`. Do not copy it to `main` merely to expose a button. A review-branch child can be called only by an eligible dispatcher on the selected ref that actually declares the call and exposes the necessary input. The current software-assurance dispatcher does not expose the container child input to manual dispatch.

Official documentation:
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_dispatch
- https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow
- https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows

## 5. Independent human-review status

| Reviewer | Scope | Latest observed correspondence | Status |
|---|---|---|---|
| Demetrios Politis | Prospective Type-I calibration/statistical methods | Request sent; no substantive reply surfaced in searched Gmail results | PENDING |
| Ali Machiry | GitHub Actions and CI/CD security | Request sent; no substantive reply surfaced in searched Gmail results | PENDING |
| Annika Seppälä | Climate-domain independence and HadUKP candidate | Initial request 2026-11-15; scope correction 2026-11-19; no substantive reply surfaced | PENDING |
| Benjamin Wong | Econometric-domain independence and CPIAUCNS pre-gap candidate | Initial request 2026-11-15; automated out-of-office reply 2026-11-15 says conference commitments through 2026-11-29; scope correction sent 2026-11-19; no substantive report surfaced | PENDING |

An automated out-of-office reply is not an independent review. These four scopes are not peer review of the ten conceptual HCM publications; no independent scholarly review of those papers has been established here.

## 6. Zenodo and publication evidence boundary

Owner-supplied JSON for Papers 02–10 reports each record as published, non-draft, public, open, not embargoed, and not deleted. This is classified as `OWNER_SUPPLIED_API_JSON`; direct Zenodo API retrieval and direct published-PDF download were not completed in this review. Previous retrieval attempts returned `Cache miss`, which is not evidence of absence or deletion.

The supplied ten-paper candidate ZIP passes integrity testing and contains ten PDFs plus README.pdf. SHA-256:

`b75f37026ee3cdc04ea79a671d166dfc7ac1b1227a7ee4a72a7f29a98b075562`

All ten candidate PDF MD5 values match the current repository publication registry. This is local candidate-to-registry agreement, not direct Zenodo binary verification. Paper 01 is not in the new Papers 02–10 JSON capture; its DOI/MD5 information comes from the repository registry.

The three separately uploaded working PDFs for Papers 01, 08, and 10 differ byte-for-byte from the corresponding ZIP candidates, while normalized extracted text is identical in each pair. Preserve both objects; do not label them byte-identical.

The full paper-by-paper audit is `docs/publications/HCM_PUBLICATION_CLOSURE_AUDIT_20261122_V1.md`.

## 7. Project Library status and organization

The Project Library was reorganized without deleting any files:

- Created `/Hybrid Consciousness Model - HCM/Historical Evidence/`.
- Moved the superseded V3 and V4 container triage reports, V6 state addendum, V1 Run 36 review register, and the three Run 34 artifacts (software assurance, OSV, and Trivy) into `Historical Evidence`.
- Kept the latest Run 35/36 software-assurance and OSV artifacts, Run 35 Trivy artifact, and Scorecard residual register in `Current Evidence`.
- The candidate folder `Zenodo PDF Candidates - Registry MD5 Match` contains all ten registry-matching candidate PDFs.
- The `Working Manuscripts - Binary Identity Pending` folder currently contains the Paper 01 working PDF. The separate Paper 08 and Paper 10 working PDFs remain in this conversation and have not yet been copied into Library.
- No Library files were deleted.

The four new V8 handoff files could not be uploaded because the Library upload quota returned `throttled` with a 20-hour retry window. They remain available as conversation files/downloads. Retry their Library upload after the quota resets; do not claim they are already in Library.

## 8. Scientific governance — unchanged

- Scientific claim: `UNDER_INVESTIGATION`.
- Protocol freeze: `NOT_FROZEN`.
- Formal Type-I calibration: false / not authorized.
- Confirmatory execution: false / not authorized.
- Claim support: false.
- Promotion authority: false / `NONE`.
- Independent-domain replication: `0/2`.

No new scientific snapshot is authorized. No endpoint calculation, null calibration, confirmatory run, replication run, claim-support update, or promotion is authorized. Do not turn UNKNOWN into NO, backdate, or change a historical threshold to make a prior result pass.

## 9. Required next actions

On `review/type1-v4-remediation` only, add these four files:

1. `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261122_V8.md`
2. `evidence/EXACT_ASSURANCE_RUN_44948856035_REVIEW_V2.csv`
3. `evidence/CONTAINER_SECURITY_REVIEW_20261122_V1.md`
4. `docs/publications/HCM_PUBLICATION_CLOSURE_AUDIT_20261122_V1.md`

Suggested commit message:

`Record V8 state, container security review and publication audit`

Do not edit `main`. Do not modify workflow files, Dockerfile, application code, scientific protocol, datasets, DOI records, or historical evidence. Preserve V6 and V7 as historical records.

After commit: send the exact commit URL; verify only the four intended files were added; verify main is unchanged; verify no workflow ran. **Do not run any `.yml` after this documentation-only commit.** No workflow filename is currently authorized for execution. A future workflow requires a new evidence-based decision specifying exact purpose, branch, commit, inputs, side effects, and containment boundary.

## 10. Closure vocabulary

Use only: `CLOSED_ADMINISTRATIVELY`; `PASS_SCOPE_LIMITED`; `OPEN`; `PENDING_INDEPENDENT_REVIEW`; `OWNER_ATTESTATION_NOT_INDEPENDENTLY_VERIFIED`; `NOT_AUTHORIZED`; `NOT_ESTABLISHED`.

No global 100% assurance, scientific validation, or publication peer-review closure is claimed.
