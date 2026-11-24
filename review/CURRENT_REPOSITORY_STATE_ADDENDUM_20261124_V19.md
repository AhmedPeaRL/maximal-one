# HCM Current Repository and Evidence State Addendum — V19

- Evidence date: 2026-11-24
- Repository: `AhmedPeaRL/maximal-one`
- Target branch: `review/type1-v4-remediation`
- Scope: post-V18 repository identity, fingerprint hardening commit, exact-commit assurance run, artifact integrity, current security and governance status
- Disposition: `REVIEW_ONLY / MAIN_UNCHANGED / FINGERPRINT_PATCH_APPLIED_STATIC_REVIEW_ONLY / ASSURANCE_SCOPE_LIMITED / CONTAINER_REVIEW_SKIPPED / SECURITY_OPEN / HUMAN_REVIEW_PENDING / SCIENTIFIC_NO_GO`

## 1. Exact repository identity

GitHub independently reports:

- Main HEAD: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- Review HEAD: `cb8e51a2d915dca9e8bfd5700515afd73e9050e8`
- Review comparison: 748 commits ahead, 36 behind Main.
- Merge base: `a9808bd999a7ad902daf15606272529ca9af4580`.

Main remains unchanged.

The Review HEAD commit `cb8e51a...` is reported by GitHub as signature-verified.

### Post-V18 commit sequence

1. `4fac9c3ff0e79b9f7d2831bc03b6d4bc1ee06eaf`
   - Adds `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261123_V18.md`.
   - Parent: `c02d2ceadd06c2f83aed5c607c19c4305ee85009`.

2. `2b013d745b146de5223e7514df4e59b7bc7f2551`
   - Adds `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261123_V18.sha256`.
   - Parent: `4fac9c3...`.
   - Manifest records the V18 Markdown digest as `9b90169322c59819f38beb8313c57366429c558ae88aa373dfa4dd9687254714`.

3. `cb8e51a2d915dca9e8bfd5700515afd73e9050e8`
   - Modifies only `env/fingerprint.py`.
   - Parent: `2b013d7...`.

The exact GitHub comparison from `c02d2ce...` to `cb8e51a...` reports three changed paths only:

- `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261123_V18.md`
- `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261123_V18.sha256`
- `env/fingerprint.py`

No Main changes were detected in this sequence.

V18 is retained as a historical addendum describing the repository and evidence state at its recorded baseline. V19 is the current-state addendum for the later Review HEAD and assurance run.

## 2. Fingerprint hardening

The Review-only commit `cb8e51a...` changes `env/fingerprint.py`.

Observed improvements:

- Replaces `subprocess.check_output(..., shell=True)` with `subprocess.run` using argument arrays and `shell=False`.
- Uses `sys.executable -m pip freeze`.
- Adds bounded subprocess timeouts.
- Uses explicit text encodings.
- Preserves the existing `json.dumps(data, sort_keys=True)` hash serialization format.

Disposition:

`PATCH_APPLIED / STATIC_SCANNERS_PASS / RUNTIME_VALIDATION_PENDING`

The exact-commit assurance run did not execute dedicated unit tests or a runtime validation of `fingerprint.py`. No claim of behavioral verification or complete hardening closure is made.

## 3. Exact-commit assurance run

Run ID: `45283161110`

- Workflow: `Exact Commit Software Assurance`
- Workflow path: `.github/workflows/software-assurance-exact-commit-v1.yml`
- Event: `workflow_dispatch`
- Branch: `review/type1-v4-remediation`
- Head SHA: `cb8e51a2d915dca9e8bfd5700515afd73e9050e8`
- Scan target: `cb8e51a2d915dca9e8bfd5700515afd73e9050e8`
- Workflow definition commit: `cb8e51a2d915dca9e8bfd5700515afd73e9050e8`
- Conclusion: `success`

Jobs:

- `138072573195` — exact-commit scan: success.
- `138072573592` — OSV dependency inventory: success.
- `138072740323` — container CLI build and image security: skipped.

The Review workflow definition blob remains:

`134fcbfa344c8f7f775f521420709c2886ac288a`

The Main copy is a different workflow definition:

`9c703f6a6e24c2e073d5650850489be50ba4ba83`

The Review workflow exposes `scan_commit` through `workflow_dispatch`. The `run_container_review` input is available only through `workflow_call`, not the manual dispatch interface.

The run targeted `cb8e51a...`, not the V18 documentation commit `2b013d7...`. It is therefore not treated as the previously specified exact-V18-target dispatch. This is recorded as a scope deviation, not as scientific authorization or promotion authority.

No additional workflow dispatch is authorized by this addendum.

## 4. Artifact identity and integrity

### Exact-commit assurance artifact

- Artifact ID: `14871081861`
- File: `exact-commit-software-assurance-45283161110.zip`
- Size: 5,901 bytes
- SHA-256: `45ec9f8c58ccbc0a69821bce986bde81417d7319b5a5f354ac19f56d7c33b6d3`
- ZIP integrity test: passed

Observed scanner results:

- actionlint 1.7.12: exit code 0; empty diagnostics.
- zizmor 1.30.1: exit code 0; empty findings array.
- OpenSSF Scorecard 5.6.0: 9.2/10.

Scorecard residuals:

- Fuzzing: 0/10.
- License: 9/10.
- `contents:write` warnings remain in:
  - `.github/workflows/canonical-sync.yml`
  - `.github/workflows/cross-run-memory-verification.yml`
  - `.github/workflows/replication.yml`
- CodeQL configuration was detected; this artifact does not establish that CodeQL executed.
- Scorecard records the temporary local worktree repository commit as `unknown`.

### OSV dependency inventory artifact

- Artifact ID: `14870202995`
- File: `osv-dependency-inventory-45283161110.zip`
- Size: 1,271 bytes
- SHA-256: `e2695ebfb0cd6915fa249d997aa1dc27caa06d242828504c97b7374a0668af6d`
- ZIP integrity test: passed

OSV-Scanner 2.7.1 produced valid JSON with `results=[]`.

The scan covered five Python requirements manifests with 48 packages each and a `package-lock.json` containing zero packages. This is scoped dependency-manifest evidence, not an operating-system package or container-image scan.

Both newly downloaded artifacts were uploaded to the ChatGPT Library folder:

`/Hybrid Consciousness Model - HCM/Current Evidence/`

Because files with the original names already existed, the Library assigned duplicate-safe names ending in `(1).zip`. No historical artifact was overwritten.

## 5. Container and Debian Trixie status

The container review remains open.

The prior container run `44944152951` reported 50 HIGH records, 12 unique CVEs, and zero CRITICAL records. Its Trivy HIGH/CRITICAL policy failed.

The current run `45283161110` skipped the container job and therefore provides no new Docker build, CLI smoke, or Trivy evidence.

Fresh Debian Security Tracker checks on 2026-11-24 continue to report these Trixie packages as vulnerable:

- OpenSSL — CVE-2026-124709.
- acl — CVE-2026-54369.
- ncurses — CVE-2025-69720.
- Perl — CVE-2026-9538.

The remaining tracked CVEs require individual current-status verification against the exact package versions in the image.

Do not suppress findings, mix Forky/Sid packages into Trixie, or edit the Dockerfile until official Trixie fix provenance and compatibility have been reviewed.

## 6. Reproduction endpoint status

The repository contains `api/public_reproduce_endpoint.py`.

The repository owner attests that it is not deployed, is not connected to a public URL, and is not linked to a live service route.

Classification:

`REPOSITORY_CODE_PRESENT / OWNER_ATTESTED_NOT_DEPLOYED / NOT_INDEPENDENTLY_VERIFIED`

It is not classified as a currently exposed live service based on the available evidence.

Its implementation remains unsuitable for future deployment without a separate security design covering immutable source pinning, dependency hash enforcement, timeouts, execution isolation, resource limits, and network restrictions.

`TemporaryDirectory` is not a security sandbox.

The inspected `analysis/external_reproduction.py` does not visibly consume the submitted payload or create the result file expected by the endpoint. Independent reproduction of a supplied payload is therefore not established.

## 7. Disabled workflows

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

The available connector evidence does not independently establish the server-side enabled/disabled state of every workflow.

The Review `Build and Publish Container` workflow has an unfiltered push trigger. Its disabled state must be visually reconfirmed immediately before any Review push. If uncertain, do not push.

## 8. Review workflow dispatch mechanics

The exact-commit assurance workflow exists on both Main and Review, but the two definitions have different blob SHAs.

For a manual run of this specific workflow, the intended target is the Review branch:

`review/type1-v4-remediation`

The workflow's manual input `scan_commit` must equal the selected branch's `GITHUB_SHA`.

A workflow that exists only on Review and is absent from the default branch cannot be assumed to have a usable manual `Run workflow` button. GitHub documents that `workflow_dispatch` requires the workflow file to exist on the default branch; branch selection can then target another branch. Do not modify Main merely to make an unrelated Review-only workflow dispatchable. Use only a pre-existing, authorized dispatcher/caller when its exact behavior has been reviewed.

## 9. Library evidence archive status

The Main archive remains aligned to Main HEAD:

- `maximal-one-main-9749de9-20261122.zip`
- Embedded commit: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- Size: 1,522,641 bytes
- SHA-256: `f59222d0eedd9073ea15ef51b1463c3926e7948fd0e8d417a536c78756634091`
- ZIP integrity: passed

The previously stored Review archive remains historical/stale:

- `maximal-one-review-type1-v4-remediation-abc08a2-20261123.zip`
- Embedded commit: `abc08a203d8649ead0f30ac23c226a6ad91db535`
- Size: 3,484,681 bytes
- SHA-256: `02d43033ff274d3278f49a9119e99fd0a4b3c8fe1338b4b95c75accccb35fbfb`
- ZIP integrity: passed

Do not represent that Review archive as current. After V19 is committed, create and upload a new Review archive aligned to the exact V19 commit SHA under a new filename.

## 10. Independent human review

The four independent review tracks remain pending:

- Dimitris Politis
- Anil Machiry
- Annika Seppälä
- Benjamin Wong

Recent bounded Gmail searches did not return new matching reviewer correspondence after 2026-11-23. No substantive independent report has been established by this search.

Requests, acknowledgements, and out-of-office messages do not count as independent review reports.

## 11. Scientific authority and no-go status

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

## 12. Required next steps

1. Add this V19 document and its SHA-256 manifest on `review/type1-v4-remediation` only.
2. Ensure exactly two paths are changed by the V19 documentation commit.
3. Verify Main remains at `9749de9253f144eeda9e1b60cb219cfc5f201ecc`.
4. Verify the V15, V16, V17, V18, and V19 manifests locally using `sha256sum -c`.
5. Visually reconfirm all thirteen owner-attested disabled workflows immediately before pushing.
6. Do not dispatch any workflow until the V19 commit and the next exact target have been independently reviewed and separately authorized.
7. Preserve the two newly uploaded artifacts and upload a current Review source archive after the V19 commit.
8. Handle runtime tests for `fingerprint.py`, endpoint redesign, container remediation, Debian updates, and reviewer findings as separate workstreams.

No Main changes, workflow-definition changes, Dockerfile changes, scientific execution, or promotion are authorized by this addendum.
