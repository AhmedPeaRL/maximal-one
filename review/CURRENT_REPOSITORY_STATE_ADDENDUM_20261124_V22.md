# HCM Current Repository and Evidence State Addendum — V22

- Evidence date: 2026-11-24
- Repository: `AhmedPeaRL/maximal-one`
- Review branch: `review/type1-v4-remediation`
- Current Review HEAD verified from GitHub ref: `11adf9c6813cae07b515a62db6ec768ca25d1811`
- Current Main HEAD verified from GitHub ref: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- Disposition: `REVIEW_ONLY / MAIN_FROZEN / LEGACY_REPRODUCTION_RETIRED_ON_REVIEW / LOCAL_REGRESSION_TESTS_PASS / READ_ONLY_AUDIT_PENDING / CONTAINER_SECURITY_OPEN / HUMAN_REVIEW_PENDING / SCIENTIFIC_NO_GO`

## 1. Git identity and branch separation

GitHub's current comparison reports Review as diverged from Main, 759 commits ahead and 36 behind, with merge base `a9808bd999a7ad902daf15606272529ca9af4580`. No merge, rebase, cherry-pick, pull request, or Main modification is authorized. Main remains frozen at `9749de...`.

The six commits after `45b647ce2a6d2cbea1fe08e874be60b738f472c1` are, in chronological order:

1. `6b16d7932da5ef02631fe0fd863decad757651d2` — add read-only GitHub audit script.
2. `dd61d16904b300dcf8bf27aa257e16b2aade8f71` — files uploaded.
3. `7ac6d82cec889186d94cb3d76f222c4c1a303857` — files uploaded.
4. `53870321ee0005f23ddfb2326408763705875a52` — retire public reproduction helper.
5. `cf0a1826a6c5b5c455843ba3fdbc82e3363694da` — retire static external reproduction fetcher.
6. `11adf9c6813cae07b515a62db6ec768ca25d1811` — add two regression tests.

The comparison reports seven changed paths: `PATCHES/NOTE.txt`, `analysis/external_reproduction.py`, `api/public_reproduce_endpoint.py`, `docs/HCM_EXTERNAL_REPRODUCTION_SPEC_V1.md`, `docs/HCM_SECURITY_REMEDIATION_PLAN_V1.md`, `tests/test_external_reproduction_retirement.py`, and `tools/hcm_readonly_github_audit.sh`. These changes are on Review only.

## 2. Library snapshot integrity and local validation

Three Review ZIP snapshots were retrieved from the ChatGPT Library. All three passed `unzip -t`. The newest snapshot is 3,541,141 bytes, SHA-256 `94aa5b61c95d5f4219d412595ca861c87873a8d0bb85579bfc4edc31401e4979`, with 1,469 ZIP entries. The two older snapshots have SHA-256 values `3ad6313d9c452dc49a64538ab6d5079054584b7b8f8d4e726888248e51a50784` and `b0dffa41b5d3cca3f703053c74ce86b062aa19219a04507fb4da13f8151af4c4`.

The newest ZIP was extracted. Git blob SHA-1 values for the retired helper files, regression test, audit script, and two new design documents match the corresponding GitHub Review file blobs. The V21 addendum SHA-256 manifest verifies.

Local checks on that extracted snapshot:

- `python -m unittest tests/test_external_reproduction_retirement.py -v`: 2 tests passed.
- `python -m py_compile` on both retired Python modules and the regression test: passed.
- `bash -n tools/hcm_readonly_github_audit.sh`: passed.

These are local checks of the extracted snapshot; they are not a GitHub Actions run and do not establish independent scientific replication.

## 3. Legacy external-reproduction helpers

On Review, `api/public_reproduce_endpoint.py` now fails closed with `PUBLIC_REPRODUCTION_HELPER_RETIRED`; `analysis/external_reproduction.py` now returns exit code 2 and explicitly identifies itself as disabled and not a reproduction. The two local regression tests passed. The retired files are not an HTTP route or an execution sandbox.

Important residual: Main is frozen and retains the old helper implementations. The Review-only retirement therefore does not constitute repository-wide retirement. The owner has stated that no public route or service is deployed; this remains owner attestation, not independently verified deployment evidence. Keep the old Main code unexposed and do not deploy either helper.

## 4. Read-only GitHub audit script defect and correction

Static review of `tools/hcm_readonly_github_audit.sh` found that its Review branch API endpoint used an unescaped slash in `branches/review/type1-v4-remediation`. The GitHub REST branch endpoint requires the branch name to be represented as one URL path segment; the slash must be encoded as `%2F`. The script also captured only Main branch protection, not Review branch protection.

The accompanying V2 script corrects the Review branch path to `review%2Ftype1-v4-remediation` and adds a Review protection read. It continues to use GitHub CLI GET requests only. Static regression tests are included. This correction has not yet been inserted into the repository or executed against GitHub.

The script must preserve API errors as unavailable/unknown. A 403/404 or missing API feature must never be converted into zero alerts or proof that a workflow is disabled.

## 5. Workflow disabled-state reconciliation

The owner currently attests that the thirteen named workflows remain disabled. The GitHub connector used for this review does not expose the Actions workflow-state endpoint, so the current server-side state could not be independently queried in this pass.

A historical Library copy of a GitHub Actions workflow-list response dated 2026-11-21 reported 54 workflows and showed `Validate Stress` as `active`; it listed the other named disabled workflows as `disabled_manually` but did not include a separate `Build and Publish Container` identity. This is historical evidence only and may predate the owner's latest disablement. It creates a concrete item for the fresh read-only audit: verify the current state by workflow `id` and `path`, especially `validate-stress.yml`.

`Build and Push Container` on Main and `Build and Publish Container` on Review both refer to `.github/workflows/build-image.yml`. The audit must compare workflow ID and path rather than treating two branch-specific display names as automatically distinct workflow identities.

Keep the owner status as `OWNER_ATTESTED_DISABLED / CURRENT_SERVER_STATE_PENDING_READ_ONLY_VERIFICATION` until the fresh API output is available. Do not enable, disable, or dispatch any of the thirteen workflows as part of this audit.

## 6. Existing software-assurance run and artifacts

The most recent retrieved exact-commit software-assurance run is run `45447848518` (run number 39), completed successfully on 2026-11-24 at 17:22 UTC. It targeted `b3bf4c82132f686e872f0217a7a198ce71c91a8d`, not the current Review HEAD `11adf9...`. The run predates the six commits listed above and therefore does not validate the newly retired helper code or the read-only audit script.

The exact-commit assurance and OSV artifacts were downloaded from GitHub and ZIP-tested; their SHA-256 values match the V21 evidence manifest:

- Exact-commit assurance ZIP (artifact ID `14945909165`): `4ce56da0d4df6187ab82c51e56804ca850775837f1d382d07f788137f05dbfef`.
- OSV inventory ZIP (artifact ID `14946876053`): `f6eee6ce50e0848fa23c0bc07bd6a9e052c2b24fd92354abf6b5e1d2be8727b2`.

GitHub run metadata confirms the exact-commit scan job and OSV job succeeded; the container CLI/image-security child was skipped. Both artifacts were still unexpired when retrieved; GitHub reported retention through `2027-02-22T17:22:29Z`.

The manifest records actionlint 1.7.12, zizmor 1.30.1, Scorecard 5.6.0; all three exit codes are zero. Actionlint output is empty, zizmor JSON is `[]` in offline mode, and Scorecard is 9.2/10. Scorecard details still warn about `contents: write` in `canonical-sync.yml`, `cross-run-memory-verification.yml`, and `replication.yml`; Fuzzing is 0/10 and License is 9/10. SAST 10/10 indicates CodeQL configuration detection, not proof of a completed CodeQL run. OSV results are empty for the supported manifests scanned; this is not an OS image scan. The manifest retains `protocol_freeze=NOT_FROZEN`, all formal/confirmatory/claim/promotion flags false, and `authority=NONE`.

## 7. Container security and Debian Trixie

The latest container evidence recorded in V21 remains run `44944152951`, targeting older commit `48b223e8d5192ed133ba1f0e59493b6e36600950`: image build and CLI smoke passed; Trivy failed its HIGH/CRITICAL threshold with 50 HIGH records, 0 CRITICAL records, and 12 distinct CVEs. The associated artifact is ID `14723121334`, SHA-256 `657ba2a2f687611c3ea5643ec128ab2fc1badd3cf0783dd8acba645415f791d7`. This is not evidence for current Review HEAD. The downloaded older Trivy report `44828421411` has 47 HIGH records and 11 CVEs; do not substitute it for run 449441.

A fresh check of Debian's official Security Tracker on 2026-11-24 continues to show the Trixie versions represented by the report as vulnerable for the listed CVEs in util-linux, sqlite3, systemd, openssl, acl, ncurses, and perl. Do not mix Forky/Sid packages into Trixie, suppress findings, or change Dockerfile pins based on a package-name-only match. Before remediation, verify the exact installed binary/source package versions, whether affected code is present and reachable, upstream/Debian fix provenance, package compatibility, and reverse dependencies. Then rebuild and scan a new exact Review commit. No such rebuild or scan is authorized now.

## 8. Human review and scientific authority

The four independent reviews remain pending: Dimitris Politis (statistical methods), Anil Machiry (CI/CD security), Annika Seppälä (climate domain), and Benjamin Wong (econometrics). No new attributable report was supplied with this snapshot. An acknowledgement or out-of-office reply does not count as a review.

Scientific status remains `PROTOCOL_NOT_FROZEN / FORMAL_CALIBRATION_NOT_AUTHORIZED / CONFIRMATORY_EXECUTION_NOT_AUTHORIZED / REPLICATION_NOT_AUTHORIZED / CLAIM_SUPPORT_NOT_AUTHORIZED / PROMOTION_NOT_AUTHORIZED`. No new scientific snapshot is authorized.

## 9. Push-trigger preflight

Static inspection of all Review-root workflow definitions found one unfiltered `push` trigger: `.github/workflows/build-image.yml`. The owner reports that this workflow is disabled, but the current server-side state is not independently verified in this pass. Other Review-targeted push workflows have path filters that do not match the V2 kit paths (`tools/hcm_readonly_github_audit.sh`, `tests/test_hcm_readonly_github_audit.py`, the V22 files under `review/`, and the named documentation files under `docs/`). Main-only push workflows filter to Main/evolution branches; tag-only workflows do not match a branch push. This is a static trigger/path review, not a substitute for the current Actions API state.

Therefore run the corrected local read-only audit **before** pushing any V2 commit. If `build-image.yml` is active, its state is unavailable, or any workflow result is ambiguous, do not push; return the audit output for review. If it is confirmed disabled and all relevant states are reconciled, the V2 commit can be considered for Review only. No workflow dispatch is authorized by this addendum.

## 10. Required next steps

1. Keep Main at `9749de...`; no merge, rebase, cherry-pick, or Main edits.
2. Run the corrected audit script from the extracted kit locally, using GitHub CLI GET requests only. No repository commit is needed to run the script.
3. Reconcile all thirteen owner-attested names against current workflow IDs and paths; specifically resolve the historical `Validate Stress` active state and the shared `build-image.yml` identity.
4. Review security alerts, Actions permissions, rulesets, and both branch protections. Unavailable API results remain UNKNOWN.
5. Only after the audit is reviewed and the `build-image.yml` push trigger is confirmed disabled, consider inserting the corrected script, its static regression test, V22 addendum/manifest, and named docs on Review only. Verify the baseline; if HEAD is not `11adf9...`, stop and re-review the diff.
6. Do not run a workflow as part of or after that commit. No `.yml` is authorized in this round.
7. Continue monitoring Debian Trixie fixes and keep container security open until a justified remediation and new exact-commit scan exist.
8. Wait for the four independent reports; no scientific snapshot, calibration, confirmatory analysis, replication, or promotion is authorized.

**Final disposition:** `REVIEW_ONLY — MAIN_FROZEN — REVIEW_RETIREMENT_LOCALLY_TESTED — AUDIT_SCRIPT_CORRECTION_PENDING — CURRENT_WORKFLOW_STATES_UNVERIFIED — CONTAINER_SECURITY_OPEN — HUMAN_REVIEWS_PENDING — SCIENTIFIC_NO_GO — NO_WORKFLOW_RUN_AUTHORIZED`.
