# Current Repository State Addendum — 2026-11-21 V5

**Disposition:** `REVIEW_ONLY — V4_RUN_INPUT_MISMATCH_RECORDED — SOFTWARE_ASSURANCE_JOBS_PASSED — CONTAINER_TRIVY_GATE_FAILED — SECURITY_GATE_OPEN — HUMAN_REVIEWS_PENDING — ZENODO_RECORD_VERIFICATION_INCOMPLETE — NO_NEW_SCIENTIFIC_SNAPSHOT`

## 1. Repository identity and branch separation

Repository: `AhmedPeaRL/maximal-one`

Verified main HEAD:

`9749de9253f144eeda9e1b60cb219cfc5f201ecc`

Verified review branch HEAD:

`48b223e8d5192ed133ba1f0e59493b6e36600950`

V4 commit:

`48b223e8d5192ed133ba1f0e59493b6e36600950`

Commit message: `Add Current Repository State Addendum V4`

The V4 commit adds the V4 repository-state addendum on:

`review/type1-v4-remediation`

The commit is GitHub-verified. No V4 change was made to `main`.

Current comparison:

- Status: `diverged`
- Review ahead of main: `718`
- Review behind main: `36`
- Merge base: `a9808bd999a7ad902daf15606272529ca9af4580`

No merge, rebase, cherry-pick, promotion, or pull request is authorized.

The uploaded `maximal-one-main.zip` is a valid archive containing 1,051 files and 3,939,438 uncompressed bytes. Its ZIP archive comment is the exact main HEAD SHA above. Archive SHA-256:

`f59222d0eedd9073ea15ef51b1463c3926e7948fd0e8d417a536c78756634091`

This archive represents the main snapshot, not the review branch.

## 2. Owner-attested workflow status

The repository owner reports that the following 12 workflows remain disabled in the live repository:

1. Emergent Periodicity Analysis
2. External Verification
3. Reproducible Research Gate
4. SOS Robustness Gate
5. Build and Push Container — main name
6. Build and Publish Container — review-branch name
7. Cross Run Memory Verification
8. Immutable Release Lock
9. Evolution Engine
10. Canonical Sync
11. Cross Architecture Timing Test
12. Cross Architecture Timing

This is recorded as owner attestation. The current workflow-state list was not independently retrievable through the available GitHub connector; therefore, no claim of direct state verification is made.

`replication.yml` is not included in the owner-listed 12 workflows and is not authorized for dispatch.

The `Exact Commit Software Assurance` workflow is not included in the owner-listed 12 and was used for run `44944152951`.

## 3. V4 software-assurance run identity

Workflow: `Exact Commit Software Assurance`

Run ID: `44944152951`

Run number: `35`

Event: `workflow_dispatch`

Branch: `review/type1-v4-remediation`

Target commit:

`48b223e8d5192ed133ba1f0e59493b6e36600950`

Conclusion: `failure`

Run URL:

`https://github.com/AhmedPeaRL/maximal-one/actions/runs/44944152951`

Job results:

- Exact-commit software assurance — job `136967646079`: success
- OSV dependency inventory — job `136967646455`: success
- Container review guard — job `136967739516`: success
- Container build, CLI smoke test, and Trivy scan — job `136967775346`: failure

### 3.1 Manual-input scope deviation

The preceding V4 authorization explicitly required:

`run_container_review=false`

The child workflow log for this run records:

`run_container_review=true`

The parent workflow was triggered by `workflow_dispatch`; its manual dispatch definition exposed `run_container_review` with a default of `false`.

Therefore, the actual dispatched value enabled the container child workflow, contrary to the preceding software-only authorization.

This is recorded as:

`MANUAL_DISPATCH_SCOPE_DEVIATION`

The record does not infer the operator's intention. It preserves the actual value shown in the child workflow log.

No retroactive authorization is granted.

## 4. Exact artifact identities

### Exact-commit software assurance

Artifact ID: `14722623446`

Artifact name: `exact-commit-software-assurance-44944152951`

SHA-256:

`10f1d5ac6bfb6c8c52f9c083f91eb85d22506321b9018f6520cbfa8cde916d0c`

### OSV dependency inventory

Artifact ID: `14723121127`

Artifact name: `osv-dependency-inventory-44944152951`

SHA-256:

`731432b4cdbc6d7140e1ed0494cdcf50b46854f69f3112039e8f90d98e07904d`

### Trivy image report

Artifact ID: `14723121334`

Artifact name: `trivy-image-report-44944152951`

SHA-256:

`657ba2a2f687611c3ea5643ec128ab2fc1badd3cf0783dd8acba645415f791d7`

All three artifacts were downloaded and inspected.

## 5. Software-assurance results

Recorded tool versions:

- actionlint `1.7.12`
- zizmor `1.30.1`
- OpenSSF Scorecard `5.6.0`
- OSV-Scanner `2.7.1`

Results:

- actionlint exit code: `0`; diagnostic output empty.
- zizmor exit code: `0`; JSON findings array empty.
- Scorecard exit code: `0`; score `9.2/10`.
- OSV-Scanner exit code: `0`; six supported manifests/lockfiles scanned; results array empty.

Scorecard recorded Fuzzing as `0` and License as `9`; other reported checks were `10`.

The Scorecard JSON identifies the local worktree path but reports the repository commit as `unknown`. Exact target identity is independently recorded by the workflow manifest and checkout validation; Scorecard's own JSON is not treated as independent commit-identity evidence.

The empty OSV results array applies to the supported dependency manifests/lockfiles. It does not establish that the Debian operating-system packages in the container image are vulnerability-free.

The assurance manifest explicitly retains:

- `protocol_freeze=NOT_FROZEN`
- `formal_calibration_authorized=false`
- `confirmatory_execution_authorized=false`
- `claim_support=false`
- `promotion_authority=false`
- `authority=NONE`

Zero scanner exit codes are not a security certification.

## 6. Container build and Trivy result

The review-only container workflow built the local image successfully.

The CLI smoke test passed:

- Python `3.11.18`
- non-root runtime UID verified
- CLI help/entrypoint verified

No registry credentials or publishing step were used. No scientific analysis was run by this smoke test.

Trivy scanned the image:

`maximal-one-cli:48b223e8d5192ed133ba1f0e59493b6e36600950`

Recorded OS: Debian `13.7`

Reported OS package count: `87`

Findings:

- HIGH finding records: `50`
- Distinct CVEs: `12`
- CRITICAL finding records: `0`

The 50 records must not be described as 50 distinct CVEs.

The 12 CVEs are:

- `CVE-2025-69720`
- `CVE-2026-119373`
- `CVE-2026-119374`
- `CVE-2026-119379`
- `CVE-2026-124709`
- `CVE-2026-16742`
- `CVE-2026-54369`
- `CVE-2026-76642`
- `CVE-2026-78408`
- `CVE-2026-78409`
- `CVE-2026-78410`
- `CVE-2026-9538`

The reported source-package families and image versions include:

- ncurses `6.5+20250216-2`
- sqlite3 `3.46.1-7+deb13u2`
- openssl `3.5.7-1~deb13u3`
- systemd `257.13-1~deb13u1`
- acl `2.3.2-2+b1`
- util-linux `2.41.5-0+deb13u1`
- perl `5.40.1-6+deb13u1`

The Debian Security Tracker records these affected package families as vulnerable in Trixie for the CVEs listed above, with some issues marked `no DSA` or `postponed`.

No false-positive suppression, suite mixing, or package removal is authorized.

The Dockerfile remains unchanged. It uses the pinned base image:

`python:3.11.18-slim-trixie@sha256:b701198cb708b68d9413ca67d6311bd97c9389a2c5fe4da0511fc652642366cd`

The Dockerfile explicitly downloads and installs the pinned zlib package. It does not explicitly install the other vulnerable package families; their origin is provisionally attributed to the base image and its OS dependency set pending a complete package inventory.

No Dockerfile edit is authorized until package provenance, necessity, reverse dependencies, runtime use, regression implications, and exact-image scan evidence have been reviewed.

## 7. Scientific governance status

Pinned scientific target remains:

`ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`

Current status remains:

- `alpha_max=NOT_SET`
- `protocol_freeze=NOT_FROZEN`
- `formal_calibration=false`
- `confirmatory=false`
- `claim_support=false`
- `promotion_authority=false`
- independent replication: `0/2`

No new scientific snapshot is authorized.

No Type-I calibration, confirmatory execution, endpoint computation, replication promotion, claim support, or scientific promotion is authorized.

The container scan is software/security evidence only. It is not scientific evidence.

## 8. Independent human review status

Gmail review on 2026-11-21 found:

- Politis: scope/snapshot correction sent 2026-11-19; no substantive review report located.
- Machiry: updated exact V9 snapshot and CI security evidence sent 2026-11-19; no substantive review report located.
- Seppälä: climate scope corrected to HadUKP EWP on 2026-11-19; no substantive review report located.
- Wong: out-of-office response dated 2026-11-15 through 2026-11-29; CPIAUCNS scope correction sent 2026-11-19; no substantive review report located.

All four independent human reports remain pending.

No automated scanner result substitutes for these human reviews.

## 9. Zenodo archive and publication provenance

The uploaded archive:

`HCM_Zenodo_10_Papers(1).zip`

contains ten candidate PDFs and `README.pdf`.

Archive size: `1,115,283` bytes

Archive SHA-256:

`b75f37026ee3cdc04ea79a671d166dfc7ac1b1227a7ee4a72a7f29a98b075562`

ZIP integrity test passed.

The candidate PDFs match the repository publication registry's byte sizes and MD5 values. The separate working copies for Papers 01, 08, and 10 have different binary hashes but identical normalized extracted PDF text to the corresponding candidates.

This is candidate-to-registry matching, not direct Zenodo download verification.

The publication registry and local candidate manifest disagree for Papers 01, 08, and 10:

- Registry CSV: `MD5_MISMATCH_LOCAL_PDF`
- Candidate manifest: `repository_registry_md5_match=YES`

This discrepancy remains open pending direct record/file verification. No registry value is silently changed.

Paper 01 record `18148140` was directly reviewed in the earlier audit; its record metadata, filename, size, and MD5 matched the local candidate. The concept DOI remains registry-sourced rather than independently resolved.

Direct Zenodo access for records 02–10 was not completed in this review. The attempted URLs returned cache misses. A cache miss is not evidence that a record or file does not exist.

For record metadata retrieval, the documented Zenodo endpoint is:

`https://zenodo.org/api/records/{record_id}`

The previously supplied `/access` suffix is not the documented single-record metadata retrieval route.

### Manuscript-source associations

Repository Markdown sources on the review branch:

- Paper 01: `docs/concept/core-scientific/papers/HCM_Paper_01_Presence_Without_Demand.md`
  - Git blob: `b989be7dcb039196796095a7b7a3598660c87332`
- Paper 08: `docs/concept/core-scientific/papers/HCM_Paper_08_Formalism_Without_Control_in_Hybrid_Conscious_Architectures.md`
  - Git blob: `cd9a2341146a6bf0db25d6f5ee3daf504db4017a`
- Paper 10: `docs/concept/core-scientific/papers/HCM_Paper_10_Application_Without_Extraction.md`
  - Git blob: `f99029a9f3f5a21d78baa74caa45f9a38b8dc734`

These are editable repository source representations, not byte-identical published PDFs.

Additional unresolved cases:

- Paper 04 registry title differs from its PDF/Markdown title: `TITLE_MISMATCH_REVIEW_REQUIRED`.
- Paper 08 registry title differs from the PDF/Markdown heading and subtitle arrangement.
- Papers 07 and 09 share a title but have distinct version DOIs, concept DOIs, file sizes, and MD5 values; they remain separate records.

No publication record is merged, renamed, or deleted.

## 10. Project Library status

The `Zenodo PDF Candidates - Registry MD5 Match` folder contains ten candidate PDFs.

The `Working Manuscripts - Binary Identity Pending` folder currently contains the separate Paper 01 working PDF.

The `Current Evidence` folder contains prior V3/V4 security triage and earlier run artifacts. The three artifacts from run `44944152951` have not yet been added to the Library.

Both `HCM_Zenodo_10_Papers.zip` and `HCM_Zenodo_10_Papers(1).zip` are present with the same recorded size. The new archive was materialized; the old archive did not have an authorized raw-byte materialization path. Their binary identity is therefore not established.

No Library file was moved, deleted, or renamed. Project Library mutation was unsupported in the available tool context.

Historical repository ZIPs must not be deleted based on filename or size alone. Their commit identity and binary hashes must be inventoried first.

## 11. Required preventive workflow change

In:

`.github/workflows/software-assurance-exact-commit-v1.yml`

Remove the `run_container_review` input block from `workflow_dispatch.inputs` only.

Retain the `run_container_review` input under `workflow_call.inputs`.

This prevents the manual dispatch form from exposing the optional container execution toggle while preserving the reusable-workflow input interface.

Do not modify `replication.yml`, `container-cli-smoke-review.yml`, any scientific workflow, or the Dockerfile.

This is a preventive workflow-interface change. It does not authorize a container run.

## 12. Next authorized action and explicit limits

After this V5 addendum and the narrow workflow-interface change are committed directly to:

`review/type1-v4-remediation`

one manual software-only run may be performed using:

`.github/workflows/software-assurance-exact-commit-v1.yml`

Required conditions:

- Target branch: `review/type1-v4-remediation`
- `scan_commit`: exact full 40-character SHA of the new commit
- The manual form must expose only `scan_commit`
- `run_container_review` must not appear as a manual dispatch input
- If the workflow state is disabled, do not re-enable it
- If the branch, SHA, or input form differs from these requirements, stop and preserve a screenshot

This one run is limited to actionlint, zizmor, Scorecard, and OSV software-assurance evidence.

It does not authorize the container child workflow, Trivy, any scientific workflow, `replication.yml`, a new scientific snapshot, Type-I calibration, confirmatory execution, publication, claim support, or promotion.

No changes to `main` are authorized.

**Final status:** repository-state documentation may advance; software-assurance verification may proceed once under the stated guard; container security remains open; independent human review remains pending; Zenodo binary identity remains partially unresolved; scientific claim status remains unchanged.
