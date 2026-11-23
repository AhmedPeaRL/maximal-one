# HCM Current Repository and Evidence State Addendum — V17

- Evidence date: 2026-11-23
- Repository: `AhmedPeaRL/maximal-one`
- Scope: post-V16 documentation state, exact branch identity, integrity-manifest correction, assurance artifacts, open security findings, human review, and scientific authorization status
- Disposition: `REVIEW_ONLY / DOCUMENTATION_INTEGRITY_CORRECTION_REQUIRED / SOFTWARE_ASSURANCE_SCOPE_LIMITED / SECURITY_OPEN / HUMAN_REVIEW_PENDING / SCIENTIFIC_NO_GO`

## 1. Exact live repository identity

GitHub API inspection confirms:

- `main`: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- `review/type1-v4-remediation`: `73c017970490b8a0c382fea707a6b45845664e48`
- Review is 741 commits ahead of main and 36 commits behind main.
- Merge base: `a9808bd999a7ad902daf15606272529ca9af4580`.

The Main HEAD remains unchanged.

The current Review HEAD is signed and GitHub reports its signature as verified.

## 2. Documentation commits after V15

The four commits after `7113f49bfd55576323a22dcb5cd3259a5c7397a6` are:

- `53e96467b6641f12de7112193a240e638559b858` — added V16 Markdown.
- `df07b294ddf5e71dbbfbc8beb8178452e1964262` — initially added V15 manifest.
- `62dec08b761bddf28adb3fb59a86ffe5aab945a0` — modified V15 manifest.
- `73c017970490b8a0c382fea707a6b45845664e48` — added V16 manifest.

GitHub reports the commits as signed and verified.

The comparison from `7113f49...` to `73c017...` reports exactly these three changed paths:

- `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261123_V15.sha256`
- `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261123_V16.md`
- `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261123_V16.sha256`

No source-code, workflow, Dockerfile, protocol, dataset, or DOI file was changed in this documentation sequence.

## 3. Integrity-manifest correction

An independent SHA-256 recomputation was performed on the UTF-8 contents retrieved from GitHub.

The computed SHA-256 for V15 Markdown is:

`a85b333b0e08e7c97e233a39305a2928dc705a8aa609078e250f8f755bb3047d`

The computed SHA-256 for V16 Markdown is:

`713eec8feb112b094572fd96a374ce91a29a45762aff820b358936a3d39d7b85`

The currently committed V15 manifest contains only 60 hexadecimal characters and is incomplete.

The currently committed V16 manifest contains the V15 Markdown hash rather than the V16 Markdown hash.

Therefore neither current manifest is accepted as a valid integrity verification record.

The required corrected manifest contents are:

- V15 manifest: the 64-character V15 hash above, followed by two spaces and `CURRENT_REPOSITORY_STATE_ADDENDUM_20261123_V15.md`.
- V16 manifest: the 64-character V16 hash above, followed by two spaces and `CURRENT_REPOSITORY_STATE_ADDENDUM_20261123_V16.md`.

The correction must be recomputed from the actual checked-out files in Termux. The result must pass `sha256sum -c`.

## 4. Exact-commit software-assurance run

Run ID: `45239013872`

- Workflow: `Exact Commit Software Assurance`
- Event: `workflow_dispatch`
- Branch: `review/type1-v4-remediation`
- Target commit: `7113f49bfd55576323a22dcb5cd3259a5c7397a6`
- Workflow-definition commit: `7113f49bfd55576323a22dcb5cd3259a5c7397a6`
- Overall conclusion: `success`

The Review workflow blob SHA remains:

`134fcbfa344c8f7f775f521420709c2886ac288a`

The Main copy is a different definition and must not be substituted.

Jobs:

- `137918330794` — exact-commit scan: success.
- `137918331158` — OSV dependency inventory: success.
- `137918677069` — container build and image security: skipped.

No additional workflow run is authorized by this addendum.

## 5. Assurance artifact identities and scope

Exact assurance artifact:

- Artifact ID: `14849598376`
- Size: 5,894 bytes
- SHA-256: `7791dba1f7f759d7f83e20cf39f1d3f4b6e18023706f51e3787cf554b2897d93`

OSV artifact:

- Artifact ID: `14851360492`
- Size: 1,270 bytes
- SHA-256: `4d6124e528869ac1f8615837f3abea9d448311eedf7245089ad00869a9d3e515`

Both artifacts were downloaded again, their ZIP integrity was checked, and their SHA-256 values were independently recomputed. Both matched GitHub's artifact digests.

Observed scanner results:

- actionlint 1.7.12: exit code 0, empty output.
- zizmor 1.30.1: offline audit, exit code 0, empty findings array.
- OpenSSF Scorecard 5.6.0: 9.2/10.
- OSV-Scanner 2.7.1: valid JSON, `results=[]`.

Scorecard residuals:

- Fuzzing: 0/10.
- License: 9/10.
- Token-Permissions: numeric score 10/10, but `contents:write` warnings remain in canonical-sync, cross-run-memory-verification, and replication workflows.
- SAST: CodeQL configuration was detected; this run does not establish that CodeQL executed.

The OSV report covers five Python requirements manifests with 48 packages each and a `package-lock.json` with zero packages.

These results do not establish complete source-code analysis, absence of all vulnerabilities, or security closure.

The container child was skipped. This run performed no Docker build, CLI smoke test, or Trivy image scan.

## 6. Library evidence status

The following two artifacts have now been uploaded to:

`/Hybrid Consciousness Model - HCM/Current Evidence/`

- `exact-commit-software-assurance-45239013872.zip`
- `osv-dependency-inventory-45239013872.zip`

The Library listing confirms both files are present.

The Main source archive remains aligned to Main HEAD `9749de9253f144eeda9e1b60cb219cfc5f201ecc`.

The current Review archive in the Library remains:

`maximal-one-review-type1-v4-remediation-abc08a2-20261123.zip`

It identifies commit `abc08a203d8649ead0f30ac23c226a6ad91db535` and is stale relative to current Review HEAD `73c017...`.

It must remain available as historical evidence, but must not be described as the current Review source archive.

A new Review source archive aligned to the post-correction Review HEAD remains pending.

## 7. Disabled workflows

The repository owner reconfirms that the following thirteen workflows remain disabled in the live GitHub settings:

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

Classification:

`OWNER_ATTESTATION_NOT_INDEPENDENTLY_VERIFIED`

The available inspection does not independently establish the server-side enabled/disabled state of every workflow.

The Review `Build and Publish Container` workflow has an unfiltered `push` trigger. Its disabled state must be visually rechecked before any future Review push. If uncertain, do not push.

## 8. Workflow authorization and branch restrictions

No `.yml` file is authorized to run after the V16 documentation sequence.

The previously authorized exact-commit software-assurance dispatch has already been consumed by run `45239013872`.

In particular:

- `replication.yml` is not authorized as a workaround or alternate caller.
- `canonical-sync.yml` is not authorized.
- `cross-run-memory-verification.yml` is not authorized.
- `build-image.yml` is not authorized.
- `container-cli-smoke-review.yml` is not authorized.
- `dependency-vulnerability-inventory.yml` is not independently dispatchable; it is a reusable `workflow_call` child.
- No scientific, calibration, replication, stress, or promotion workflow is authorized.

The existing exact-assurance caller exposes `scan_commit` through `workflow_dispatch`. Its `run_container_review` input is available through `workflow_call`, defaults to false, and is not exposed by the manual dispatch interface.

A future Review-only reusable child can be invoked by a parent workflow using same-repository local workflow syntax, for example:

`uses: ./.github/workflows/example-review-child.yml`

The child can exist only on Review. The manually dispatchable parent must be available through a workflow path present on the default branch, and the operator must select the Review branch in the GitHub workflow interface. The selected Review definition must be inspected before execution.

If no appropriate dispatchable parent exists on the default branch, do not add one to Main without separate explicit authorization.

This architecture note does not authorize any new workflow or execution.

## 9. Open code-hardening findings

`env/fingerprint.py`:

- Uses `subprocess.check_output(..., shell=True)` for constant internal commands.
- Recommended future remediation: argument arrays, `shell=False`, and `sys.executable -m pip freeze`.
- This is a hardening issue, not evidence of a demonstrated exploit.

`api/public_reproduce_endpoint.py`:

- Clones mutable `main`.
- Installs dependencies without an explicit `--require-hashes` invocation.
- Does not create an isolated virtual environment.
- Executes repository code after installation.
- A temporary directory is not a security sandbox.
- No in-repository caller was found in the inspected source; deployment and external exposure remain unknown.

Future remediation requires a separately reviewed, exact-commit patch. A true zero-trust execution boundary would require immutable source identity, hash-checked dependencies, isolated execution, and operating-system or container-level restrictions.

## 10. Container and Debian Trixie status

The prior container review remains open.

Run `44944152951` reported:

- 50 HIGH records.
- 12 unique CVEs.
- Zero CRITICAL records.
- Docker build and CLI smoke test succeeded.
- Trivy HIGH/CRITICAL policy failed.

The twelve unique CVEs are:

- util-linux: CVE-2026-76642, CVE-2026-78408, CVE-2026-78409, CVE-2026-78410.
- SQLite: CVE-2026-119373, CVE-2026-119374, CVE-2026-119379.
- OpenSSL: CVE-2026-124709.
- systemd: CVE-2026-16742.
- acl: CVE-2026-54369.
- ncurses: CVE-2025-69720.
- Perl: CVE-2026-9538.

The latest official Debian Tracker review recorded no established Trixie fix for these findings.

Do not suppress Trivy findings, mix Forky/Sid packages into Trixie, or edit the Dockerfile until official Trixie fix provenance and compatibility are reviewed.

The prior zlib1g package verification remains scoped to the previously scanned image only.

## 11. Independent human reviews

The four requested review tracks remain pending:

- Dimitris Politis: request found; no substantive review report surfaced.
- Anil Machiry: requests and an updated evidence message found; no substantive review report surfaced.
- Annika Seppälä: HadUKP scope correction sent; no substantive review report surfaced. The raw-source identity discrepancy remains unresolved.
- Benjamin Wong: out-of-office response indicates possible delays through 2026-11-29; no substantive review report surfaced.

Acknowledgements, sent requests, and out-of-office messages are not independent reviews.

No reviewer is to be counted as having completed a review without an attributable, dated report containing actual findings.

## 12. Scientific authority

The project remains:

- `REVIEW_ONLY`
- `PROTOCOL_NOT_FROZEN`
- `FORMAL_CALIBRATION_NOT_AUTHORIZED`
- `CONFIRMATORY_EXECUTION_NOT_AUTHORIZED`
- `REPLICATION_NOT_AUTHORIZED`
- `CLAIM_SUPPORT_NOT_AUTHORIZED`
- `PROMOTION_NOT_AUTHORIZED`

No new scientific snapshot, Type-I calibration, confirmatory execution, replication, endpoint computation, protocol freeze, or publication claim is authorized.

No claim of 100% assurance, complete security closure, scientific validity, or independent peer review is made.

## 13. Required next action

The next repository commit must be documentation-only on:

`review/type1-v4-remediation`

It must:

1. Correct the V15 SHA-256 manifest.
2. Correct the V16 SHA-256 manifest.
3. Add this V17 Markdown file.
4. Add the V17 SHA-256 manifest generated from the exact saved bytes.

No changes to Main, any `.yml` file, Dockerfile, source code, protocol, dataset, or DOI file are authorized.

No workflow run is authorized after this documentation commit.

Before pushing, visually recheck all thirteen owner-attested disabled workflows, especially the Review Build and Publish Container workflow.

After the commit, record its exact SHA, URL, parent, changed-file list, manifest checks, Main HEAD, Review workflow blob SHA, and updated Library archive identity.
