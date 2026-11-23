# HCM Current Repository and Evidence State Addendum — V18

- Evidence date: 2026-11-23
- Repository: `AhmedPeaRL/maximal-one`
- Target branch: `review/type1-v4-remediation`
- Scope: post-V17 repository identity, corrected integrity manifests, assurance artifact review, code-hardening findings, container status, human review, and workflow authorization
- Disposition: `REVIEW_ONLY / V17_SUPERSEDED_BY_CURRENT_STATE / MANIFESTS_CORRECTED_PENDING_LOCAL_CHECK / SOFTWARE_ASSURANCE_SCOPE_LIMITED / SECURITY_OPEN / HUMAN_REVIEW_PENDING / SCIENTIFIC_NO_GO`

## 1. Exact live repository identity

GitHub comparison confirms:

- `main`: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- `review/type1-v4-remediation`: `c02d2ceadd06c2f83aed5c607c19c4305ee85009`
- Review is 745 commits ahead of Main and 36 commits behind Main.
- Merge base: `a9808bd999a7ad902daf15606272529ca9af4580`.

Main remains unchanged.

The current Review HEAD is `c02d2ceadd06c2f83aed5c607c19c4305ee85009`. GitHub reports its commit signature as verified.

Its parent is `2d02d9ec6a6dcbd003f798df94f523dfa388990c`.

The final commit `c02d2ce...` adds only:

- `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261123_V17.sha256`

The cumulative comparison from `73c017970490b8a0c382fea707a6b45845664e48` to current Review HEAD reports exactly four changed paths:

1. `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261123_V15.sha256`
2. `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261123_V16.sha256`
3. `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261123_V17.md`
4. `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261123_V17.sha256`

No source code, workflow, Dockerfile, protocol, dataset, or DOI file was changed in this four-file documentation sequence.

## 2. V17 supersession and integrity manifests

V17 is retained as historical evidence, but it is no longer the current-state addendum.

Its repository identity section records Review HEAD `73c017...`, whereas current Review HEAD is `c02d2ce...`.

Its integrity section describes the V15 and V16 manifests as defective and their correction as a future action. Those two manifests have since been corrected.

The corrected V15 Markdown SHA-256 is:

`a85b333b0e08e7c97e233a39305a2928dc705a8aa609078e250f8f755bb3047d`

The corrected V16 Markdown SHA-256 is:

`713eec8feb112b094572fd96a374ce91a29a45762aff820b358936a3d39d7b85`

The expected manifest lines are:

- `a85b333b0e08e7c97e233a39305a2928dc705a8aa609078e250f8f755bb3047d  CURRENT_REPOSITORY_STATE_ADDENDUM_20261123_V15.md`
- `713eec8feb112b094572fd96a374ce91a29a45762aff820b358936a3d39d7b85  CURRENT_REPOSITORY_STATE_ADDENDUM_20261123_V16.md`

The V17 manifest currently contains:

`f9ab547334558ea7ec65dee8a4586fc0ddbe0141c08bc32cb88e330f24593b5a  CURRENT_REPOSITORY_STATE_ADDENDUM_20261123_V17.md`

The V17 manifest and the corrected V15/V16 manifests must all pass a local `sha256sum -c` check against the exact checked-out bytes before this addendum is committed.

## 3. Exact-commit software assurance

The only recent exact-commit assurance run inspected is:

- Run ID: `45239013872`
- Workflow: `Exact Commit Software Assurance`
- Event: `workflow_dispatch`
- Branch: `review/type1-v4-remediation`
- Scan target: `7113f49bfd55576323a22dcb5cd3259a5c7397a6`
- Workflow-definition commit: `7113f49bfd55576323a22dcb5cd3259a5c7397a6`
- Conclusion: `success`

Jobs:

- `137918330794` — exact-commit scan: success.
- `137918331158` — OSV dependency inventory: success.
- `137918677069` — container CLI build and image security: skipped.

The Review-branch exact-assurance workflow blob SHA is:

`134fcbfa344c8f7f775f521420709c2886ac288a`

The Main-branch copy is a different workflow definition, with blob SHA:

`9c703f6a6e24c2e073d5650850489be50ba4ba83`

The Review version must be selected for any authorized Review-branch dispatch.

A bounded GitHub Actions API query after `2026-11-23T18:30:28Z` returned zero additional runs for both Main and Review. This is bounded evidence, not a complete all-time Actions audit.

## 4. Assurance artifacts and residual findings

The following artifacts are present in the ChatGPT Library folder:

`/Hybrid Consciousness Model - HCM/Current Evidence/`

- `exact-commit-software-assurance-45239013872.zip`
- `osv-dependency-inventory-45239013872.zip`

Their independently recomputed SHA-256 values are:

- Exact assurance ZIP: `7791dba1f7f759d7f83e20cf39f1d3f4b6e18023706f51e3787cf554b2897d93`
- OSV ZIP: `4d6124e528869ac1f8615837f3abea9d448311eedf7245089ad00869a9d3e515`

Both ZIP archives pass integrity testing.

Observed results:

- actionlint 1.7.12: exit code 0; empty diagnostics file.
- zizmor 1.30.1: offline audit; exit code 0; empty findings array.
- OpenSSF Scorecard 5.6.0: 9.2/10.
- OSV-Scanner 2.7.1: valid JSON; `results=[]`.

Scorecard residuals:

- Fuzzing: 0/10.
- License: 9/10.
- Token-Permissions: numeric score 10/10, with `contents:write` warnings in:
  - `.github/workflows/canonical-sync.yml`
  - `.github/workflows/cross-run-memory-verification.yml`
  - `.github/workflows/replication.yml`
- SAST: CodeQL configuration detected; this run does not establish that CodeQL executed.

The OSV inventory covers five Python requirements manifests with 48 packages each and a `package-lock.json` with zero packages. It is not a container or operating-system package scan.

The container job was skipped. This run performed no Docker build, CLI smoke test, or Trivy scan.

These results do not establish complete source-code analysis, absence of all vulnerabilities, or security closure.

## 5. Disabled workflow state and authorization

The repository owner reconfirms that these thirteen workflows remain disabled in the live GitHub settings:

1. Emergent Periodicity Analysis
2. External Verification
3. Reproducible Research Gate
4. SOS Robustness Gate
5. Build and Push Container — Main name
6. Build and Publish Container — Review name
7. Cross Run Memory Verification
8. Immutable Release Lock
9. Evolution Engine
10. Canonical Sync
11. Cross Architecture Timing Test
12. Cross Architecture Timing
13. Validate Stress

Classification remains:

`OWNER_ATTESTATION_NOT_INDEPENDENTLY_VERIFIED`

The available inspection does not independently establish the server-side enabled/disabled state of every workflow.

The Review `Build and Publish Container` workflow has an unfiltered `push` trigger. Its disabled state must be visually rechecked immediately before any Review push. If uncertain, do not push.

### One narrowly scoped future dispatch

After the V18 documentation-only commit is pushed and independently verified, exactly one manual dispatch is authorized:

- Workflow file: `.github/workflows/software-assurance-exact-commit-v1.yml`
- Target branch: `review/type1-v4-remediation`
- Event: `workflow_dispatch`
- Input: `scan_commit` must equal the exact V18 commit SHA.
- Selected workflow definition must be the Review version with blob SHA `134fcbfa344c8f7f775f521420709c2886ac288a`.

The Main workflow definition must not be selected.

The manual Review dispatch exposes `scan_commit`; it does not expose `run_container_review`. The container child must remain skipped.

This single dispatch does not authorize any other workflow, container build, Trivy run, scientific analysis, calibration, replication, stress test, publication, or promotion.

If the V18 commit is not the exact Review HEAD, if the workflow blob SHA differs, or if any disabled-workflow state cannot be reconfirmed, do not dispatch.

## 6. Code-hardening and correctness findings

### `env/fingerprint.py`

The file uses `subprocess.check_output(..., shell=True)` for constant internal commands.

This is an avoidable hardening issue, not a demonstrated exploit.

A separate Review-only code patch should:

- Use argument arrays and `shell=False`.
- Use `sys.executable -m pip freeze` so the package inventory belongs to the running interpreter.
- Apply bounded subprocess timeouts.
- Preserve the existing hash serialization unless a separately documented fingerprint-format change is approved.

### `api/public_reproduce_endpoint.py`

The inspected implementation:

- Clones mutable default-branch `main`, rather than a fixed immutable commit.
- Invokes pip without `--require-hashes`, although the requirements lock contains hashes.
- Does not create an isolated virtual environment.
- Executes repository code.
- Has no explicit timeout for clone, install, or execution.
- Treats `TemporaryDirectory` as if it were a complete isolation boundary, which it is not.

The presence of hashes in `requirements-lock.txt` does not mean pip enforces them unless `--require-hashes` is passed.

### `analysis/external_reproduction.py`

The inspected file fetches a fixed public `canonical_report.json`, extracts two values, compares them against hard-coded thresholds, and prints a result.

It does not visibly read the supplied `external_input.json` argument or create the `artifacts/reproduction_result.json` file expected by `public_reproduce_endpoint.py`.

Therefore, based on the inspected files, the current endpoint path does not demonstrate independent reproduction of the submitted payload and may return `no result`.

No in-repository caller was found in the available default-branch code search. Deployment and external exposure remain unknown.

Do not describe this endpoint as a zero-trust sandbox, independent replication, or scientific validation.

Before any endpoint code change, determine whether it is deployed, what route exposes it, what identity invokes it, and what operating-system/container isolation exists.

If external execution is exposed without a real sandbox, disable that execution path until a separately reviewed isolation design is implemented.

## 7. Container and Debian Trixie status

The prior container review remains open.

Run `44944152951` reported:

- 50 HIGH records.
- 12 unique CVEs.
- Zero CRITICAL records.
- Docker build and CLI smoke test succeeded.
- Trivy HIGH/CRITICAL policy failed.

The twelve CVEs remain tracked:

- util-linux: CVE-2026-76642, CVE-2026-78408, CVE-2026-78409, CVE-2026-78410.
- SQLite: CVE-2026-119373, CVE-2026-119374, CVE-2026-119379.
- OpenSSL: CVE-2026-124709.
- systemd: CVE-2026-16742.
- acl: CVE-2026-54369.
- ncurses: CVE-2025-69720.
- Perl: CVE-2026-9538.

The prior official Debian Tracker review did not establish Trixie fixes for the full set. Continue checking official Trixie package status and exact fixed versions.

Do not suppress Trivy findings, mix Forky/Sid packages into Trixie, or edit the Dockerfile until official Trixie fix provenance and compatibility are reviewed.

The previous zlib1g verification remains scoped to the previously scanned image only.

## 8. Library evidence archive status

The current Main archive remains aligned with Main HEAD:

- File: `maximal-one-main-9749de9-20261122.zip`
- Size: 1,522,641 bytes
- SHA-256: `f59222d0eedd9073ea15ef51b1463c3926e7948fd0e8d417a536c78756634091`
- ZIP integrity: passed
- Embedded commit: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`

The current Review archive in the Library is historical/stale:

- File: `maximal-one-review-type1-v4-remediation-abc08a2-20261123.zip`
- Size: 3,484,681 bytes
- SHA-256: `02d43033ff274d3278f49a9119e99fd0a4b3c8fe1338b4b95c75accccb35fbfb`
- ZIP integrity: passed
- Embedded commit: `abc08a203d8649ead0f30ac23c226a6ad91db535`

It must remain preserved as historical evidence and must not be represented as the current Review archive.

After the V18 commit, create and upload a new Review source archive whose embedded commit is the exact V18 commit SHA. Record its size, SHA-256, ZIP integrity, and embedded commit identity. Use a new filename; do not overwrite the historical archive.

## 9. Independent human reviews

The four independent review tracks remain pending:

- Dimitris Politis
- Anil Machiry
- Annika Seppälä
- Benjamin Wong

The latest Gmail review did not surface substantive reviewer reports. Benjamin's out-of-office response is not a review report.

Do not count requests, acknowledgements, corrections, or out-of-office messages as independent review.

A reviewer is complete only after an attributable, dated report with actual findings is received and assessed.

## 10. Scientific authority

The project remains:

- `REVIEW_ONLY`
- `PROTOCOL_NOT_FROZEN`
- `FORMAL_CALIBRATION_NOT_AUTHORIZED`
- `CONFIRMATORY_EXECUTION_NOT_AUTHORIZED`
- `REPLICATION_NOT_AUTHORIZED`
- `CLAIM_SUPPORT_NOT_AUTHORIZED`
- `PROMOTION_NOT_AUTHORIZED`

No new scientific snapshot, Type-I calibration, confirmatory execution, endpoint computation, replication, protocol freeze, publication claim, or promotion is authorized.

No claim of 100% assurance, complete security closure, scientific validity, or independent peer review is made.

## 11. Required next steps

1. Commit this V18 addendum and its SHA-256 manifest on `review/type1-v4-remediation` only.
2. Confirm exactly two paths changed: V18 Markdown and V18 SHA-256 manifest.
3. Confirm Main remains at `9749de9253f144eeda9e1b60cb219cfc5f201ecc`.
4. Confirm V15, V16, V17, and V18 manifests pass local `sha256sum -c`.
5. Confirm Review workflow blob SHA remains `134fcbfa344c8f7f775f521420709c2886ac288a`.
6. Reconfirm all thirteen disabled workflows immediately before pushing.
7. After exact V18 commit verification, perform only the single authorized Review-branch exact-commit software-assurance dispatch described above.
8. Download and preserve the resulting artifacts, verify their ZIP integrity and SHA-256, and upload them to the Library.
9. Upload a new Review source archive aligned to the V18 commit.
10. Handle code hardening, endpoint safety, container remediation, Debian updates, and reviewer findings in separate, independently reviewed workstreams.

No Main changes, workflow-definition changes, Dockerfile changes, scientific execution, or promotion are authorized by this addendum.
