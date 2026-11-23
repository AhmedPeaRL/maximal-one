# HCM Current Repository and Evidence State Addendum — V16

- Evidence date: 2026-11-23
- Repository: `AhmedPeaRL/maximal-one`
- Scope: post-V15 live branch identity, exact-commit software-assurance run 45239013872, artifact verification, current open security and review items
- Disposition: `REVIEW_ONLY / SOFTWARE_ASSURANCE_RUN_COMPLETED / CONTAINER_REVIEW_SKIPPED / SECURITY_OPEN / HUMAN_REVIEW_PENDING / SCIENTIFIC_NO_GO`

## 1. Exact live repository identity

GitHub API inspection confirms:

- `main`: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- `review/type1-v4-remediation`: `7113f49bfd55576323a22dcb5cd3259a5c7397a6`
- Review is 737 commits ahead of main and 36 commits behind main.
- Merge base: `a9808bd999a7ad902daf15606272529ca9af4580`.

The V15 commit is `7113f49bfd55576323a22dcb5cd3259a5c7397a6`, parent `a647a806d228d98d9860b7802ada0a47e321f2f5`. GitHub reports its signature as verified.

The V15 commit changed exactly one file:

- Added `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261123_V15.md`

The expected companion file was not committed:

- Missing: `review/CURRENT_REPOSITORY_STATE_ADDENDUM_20261123_V15.sha256`

A GitHub Contents API request for that manifest returned 404. Therefore V15's Markdown does not yet have its required repository-side SHA-256 manifest.

V15 Section 1 records the pre-V15 baseline Review HEAD `a647a806...`. This V16 addendum supersedes that value as the current live Review HEAD. No code, workflow, Dockerfile, protocol, dataset, or DOI file was changed by the V15 commit.

## 2. Exact-commit assurance run

GitHub Actions run:

- Run ID: `45239013872`
- Workflow: `Exact Commit Software Assurance`
- Event: `workflow_dispatch`
- Branch: `review/type1-v4-remediation`
- Head SHA: `7113f49bfd55576323a22dcb5cd3259a5c7397a6`
- Conclusion: `success`

The run used the intended Review-branch caller:

`.github/workflows/software-assurance-exact-commit-v1.yml`

The inspected Review workflow blob SHA remains:

`134fcbfa344c8f7f775f521420709c2886ac288a`

The Main copy is a different workflow definition and was not the selected workflow.

Jobs:

- `137918330794` — Scan exact commit without promotion authority: `success`
- `137918331158` — OSV inventory for the exact target commit: `success`
- `137918677069` — Container CLI build and image security: `skipped`

The exact target and workflow-definition commit both equal:

`7113f49bfd55576323a22dcb5cd3259a5c7397a6`

## 3. Assurance artifact identity and results

Artifact `14849598376`:

- Name: `exact-commit-software-assurance-45239013872`
- Size: 5,894 bytes
- SHA-256: `7791dba1f7f759d7f83e20cf39f1d3f4b6e18023706f51e3787cf554b2897d93`

The ZIP was downloaded, its integrity inspected, and its SHA-256 independently recomputed. The result matches GitHub's artifact digest.

Results:

- actionlint 1.7.12: exit code 0; output file empty.
- zizmor 1.30.1: offline workflow audit; exit code 0; JSON findings array empty.
- OpenSSF Scorecard 5.6.0: 9.2/10.

Scorecard residuals:

- Fuzzing: 0/10; no fuzzer integration detected.
- License: 9/10; license file detected, but not an FSF/OSI license.
- Token-Permissions: numeric score 10/10, while the report records `contents:write` warnings in:
  - `.github/workflows/canonical-sync.yml`
  - `.github/workflows/cross-run-memory-verification.yml`
  - `.github/workflows/replication.yml`
- SAST: CodeQL configuration detected; this does not establish that CodeQL ran in this workflow.

The workflow manifest records:

- `protocol_freeze = NOT_FROZEN`
- `formal_calibration_authorized = false`
- `confirmatory_execution_authorized = false`
- `claim_support = false`
- `promotion_authority = false`
- `authority = NONE`

The successful workflow conclusion means the configured scanner-execution gate completed. It does not mean all security risks are closed.

## 4. OSV artifact identity and scope

Artifact `14851360492`:

- Name: `osv-dependency-inventory-45239013872`
- Size: 1,270 bytes
- SHA-256: `4d6124e528869ac1f8615837f3abea9d448311eedf7245089ad00869a9d3e515`

The ZIP was downloaded, its integrity inspected, and its SHA-256 independently recomputed. The result matches GitHub's artifact digest.

OSV-Scanner version: `2.7.1`.

The JSON is valid and contains `results = []`. The scan log reports five Python requirements manifests, each with 48 packages, and one `package-lock.json` with zero packages.

This is scoped source-manifest evidence only. It is not an operating-system package scan, container image scan, or proof of absence of vulnerabilities outside the supported manifests.

## 5. Container review status

The container job in run `45239013872` was skipped. No Docker build, CLI smoke test, or Trivy image scan occurred in this run.

The prior Trivy findings and Debian Trixie status remain open. No container-security closure is claimed by V16.

Do not suppress Trivy findings, mix Forky/Sid packages into Trixie, or edit the Dockerfile until official Trixie package fixes, provenance, and compatibility have been reviewed.

## 6. Bounded Actions audit

For the API query cutoff `created > 2026-11-22T17:11:22Z`:

- `main`: `total_count = 0`
- `review/type1-v4-remediation`: one run, `45239013872`

This is bounded API evidence for the named branches and cutoff, not a complete all-time Actions audit.

## 7. Disabled workflow state

The repository owner reconfirms that the same thirteen workflows remain disabled in the live GitHub settings.

Classification remains:

`OWNER_ATTESTATION_NOT_INDEPENDENTLY_VERIFIED`

The available GitHub repository and Actions inspection does not independently expose the server-side enabled/disabled state of every workflow. Workflow presence or absence of runs does not prove disabled status.

The Review `Build and Publish Container` workflow has an unfiltered `push` trigger. Its disabled state must be visually rechecked immediately before any Review push. If uncertain, do not push.

## 8. Open code-hardening items

The previously inspected code items remain open and were not remediated by this documentation-only commit or the workflow run:

- `env/fingerprint.py`: constant internal commands are passed through `shell=True`; a future code-only remediation should use argument arrays and `shell=False`.
- `api/public_reproduce_endpoint.py`: clones mutable `main`, installs requirements without an explicit `--require-hashes` invocation and without an isolated virtual environment, then executes repository code. Deployment and external exposure remain unknown.

These are hardening findings, not proof of a deployed exploit.

## 9. Independent human reviews

The four requested review tracks remain incomplete.

Current Gmail inspection:

- Dimitris Politis: request found; no substantive review reply found in the current search.
- Annika Seppälä: initial request and a scope correction to HadUKP found; no substantive review reply found.
- Benjamin Wong: out-of-office reply indicates delays through 2026-11-29; a scope correction to CPIAUCNS was sent; no substantive review reply found.
- Anil Machiry: no matching result surfaced in the current Gmail search. This is not proof that no message exists elsewhere or under another address.

No acknowledgement, automated reply, or out-of-office notice counts as an independent scientific review.

## 10. Library evidence status

The currently listed Library Review archive identifies commit `abc08a203d8649ead0f30ac23c226a6ad91db535` and is stale relative to current Review HEAD `7113f49...`.

The current Library does not yet contain:

- A Review source archive aligned to `7113f49...`
- V15 SHA-256 manifest
- V16 addendum and manifest
- Assurance artifact `14849598376`
- OSV artifact `14851360492`

The two new workflow artifacts have been downloaded and locally hash-verified, but Library ingestion remains pending.

## 11. Scientific and promotion restrictions

No new scientific snapshot, Type-I calibration, confirmatory execution, replication, protocol freeze, publication claim, or promotion is authorized.

The assurance run has no scientific authority. Its manifest explicitly records `authority = NONE`.

No claim of 100% assurance, complete security closure, scientific validity, or independent peer review is made.

## 12. Required next step

The next repository change is documentation-only and must be made on:

`review/type1-v4-remediation`

Add the missing V15 SHA-256 manifest and this V16 Markdown with its own SHA-256 manifest.

Do not change `main`, any `.yml` file, Dockerfile, source code, protocol, dataset, or DOI file.

No additional workflow run is authorized by V16. Any future `.yml` execution requires a separate explicit authorization after exact branch, workflow definition, inputs, permissions, and disabled-workflow state have been reviewed.
