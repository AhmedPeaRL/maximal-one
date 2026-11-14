# Type-I Software Assurance — Finding-Level Triage Package V1

## Identity and scope

- Repository: `AhmedPeaRL/maximal-one`
- Exact scanned source commit: `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`
- Software-assurance workflow run: `43611097357`
- Assurance artifact ID: `14120366991`
- Assurance manifest SHA-256: `422c1a1722108b1a74173224af39dd5d043e0f524a1272833210e5d10b638708`
- Scanner versions: actionlint 1.7.12; zizmor 1.30.1; OpenSSF Scorecard 5.6.0
- This package is a structured triage register, not an independent security audit and not a closure record.
- All rows are initialized `OPEN_UNREVIEWED`; no row is marked fixed, accepted, false positive, or closed.

## Integrity of downloaded evidence

- Assurance ZIP SHA-256: `3344863466d97a7a9144e5dcf28b259db9787e9c1d0bbbb2814b94185fa0c2a4`
- Snapshot ZIP SHA-256: `78d5ac9ca0dee723255f4684bf0a901613de19c4fec27bb9b621197ae8e1e79e`
- Inventory ZIP SHA-256: `509a944552daabfd1e4a33f0cdb234af5efd630702a4f05af9fac742a70e2cd8`
- The assurance manifest records hashes for 14 raw outputs; each was checked against the downloaded artifact.
- All 40 ZIP archives available in the working session at review time passed ZIP CRC/integrity testing; the archive-by-archive SHA-256, byte count, member count, and duplicate-copy count are recorded in `ZIP_ARCHIVE_INTEGRITY_INVENTORY_V1.csv`. This includes older artifact copies from earlier attempts; those older copies were integrity-inventoried, while the current five artifacts and two repository ZIP snapshots were extracted and substantively inspected.
- The uploaded main-branch ZIP identifies `main` at `160acfc8600b66c7300f2fd0caa500972de740b8`; GitHub still reports that exact SHA as the `main` ref. The uploaded review-branch ZIP identifies `c44b5eb607fb16313ade4550fa3d17e76279322c`; commit `283d1b7a1800fdc7a1e63dbd33878827a1b3759e` is its child and is confirmed as the review-branch push head by run `43614085900`. The compare API reports the review commit as diverged from main (463 commits ahead, 34 behind); this is another reason not to merge mechanically.
- The scanner source was the detached exact target commit identified in the assurance manifest; the Scorecard JSON itself reports `repo.commit = unknown` and therefore is not an independent commit attestation.

## Zizmor — 205 findings

- High: 164
- Medium: 37
- Informational: 4

| Rule | Total | High | Medium | Informational |
|---|---:|---:|---:|---:|
| `artipacked` | 18 | 0 | 18 | 0 |
| `cache-poisoning` | 1 | 1 | 0 | 0 |
| `dangerous-triggers` | 2 | 2 | 0 | 0 |
| `excessive-permissions` | 19 | 5 | 14 | 0 |
| `superfluous-actions` | 1 | 0 | 0 | 1 |
| `template-injection` | 13 | 5 | 5 | 3 |
| `unpinned-uses` | 151 | 151 | 0 | 0 |

### Priority order (triage priority, not a confirmed exploitability rating)

1. **P0 — immediate independent review:** High-severity `template-injection`, `excessive-permissions`, `dangerous-triggers`, and `cache-poisoning` rows. Confirm trust boundaries, event source, token scopes, downstream workflow privileges, cache write/read paths, and realistic attacker control.
2. **P1 — supply-chain control:** all 151 High `unpinned-uses` findings. Pin to verified full commit SHAs after checking upstream ownership/release provenance; do not blindly pin arbitrary hashes.
3. **P2 — medium severity:** `artipacked`, medium `excessive-permissions`, and medium `template-injection` findings. Verify credential persistence, artifact contents, and untrusted interpolation paths.
4. **P3 — informational:** informational template-injection and superfluous-action rows; document disposition and remove unused actions where appropriate.

### Important interpretation

The 151 `unpinned-uses` rows are policy findings because references are not pinned to immutable commit hashes; a tag reference is not by itself proof that an action is malicious. It is still a supply-chain reproducibility/integrity weakness that requires controlled pinning. Likewise, severity/confidence values are the scanner's determinations, not a substitute for contextual exploitability analysis.

## Initial high-impact source review (from the exact snapshot)

### A. Untrusted `repository_dispatch` payload interpolated into shell — P0

`/.github/workflows/scientific-validation.yml` contains direct expressions in `run:` at lines 1510, 1529, 3290, and 3294:

- `RAW='${{ toJson(github.event.client_payload) }}'`
- `echo "INPUT: ${{ github.event.client_payload.input }}" ...`
- `echo "${{ github.event.client_payload.input }}" | sha256sum ...`

The workflow accepts `repository_dispatch` events. The payload is external event data and should be treated as untrusted. Inserting it directly into shell source creates a command-injection boundary. The two direct `client_payload.input` interpolations are especially clear. The `toJson(...)` expression inside single-quoted shell assignment is also unsafe because payload content can include characters that terminate or alter shell quoting after expression substitution.

**Required remediation:** remove all `github.event.client_payload` expressions from `run:` scripts. Pass the data through step-level `env:` variables and parse it using a fixed Python/Node script; validate schema, type, and size. For example, use `env: CLIENT_PAYLOAD_JSON: ${{ toJson(github.event.client_payload) }}` and read `os.environ["CLIENT_PAYLOAD_JSON"]` in Python. For scalar input, pass it as an env variable and write/hash it with a fixed script. Never build shell syntax from the payload. Add adversarial tests for single/double quotes, command substitutions, semicolons, newlines, backticks, and `$()`; assert no marker command executes and the stored/hash bytes match the input.

### B. Workflow-wide write permissions — P0

`/.github/workflows/scientific-validation.yml` declares workflow-level permissions at lines 16–23, including `contents: write`, `packages: write`, `pages: write`, `id-token: write`, and `security-events: write`. The workflow also accepts `repository_dispatch` and `pull_request`. A broad permission set is inherited by jobs unless explicitly narrowed. This needs job-by-job least-privilege redesign, not a blanket assumption that every job needs every scope.

**Required remediation:** set the workflow default to `permissions: {}` (or the minimum read-only baseline) and add explicit permissions to each job only after tracing the job's exact operations. Restrict `contents: write` to the specific job that commits/pushes; `pages: write` to the deploy job; `packages: write` to the publishing job; `id-token: write` only to a job using OIDC; `security-events: write` only to the CodeQL/SARIF upload job. Keep write-capable jobs away from untrusted PR/payload execution. Verify with token-permission tests and workflow run logs.

### C. `build-image.yml` publishes on both push and pull_request — P0/P1 review

`/.github/workflows/build-image.yml` has `on: [push, pull_request]`, workflow-level `packages: write`, and a push step for `ghcr.io/...:latest`. This is not merely a static possibility: the new report-only commit `283d1b7a1800fdc7a1e63dbd33878827a1b3759e` on `review/type1-v4-remediation` triggered Build and Push Container run `43614085900` (`event=push`). Both jobs succeeded, including the `Push image` step (job `132505224850`, 16:12:38–16:13:23 UTC). Therefore a push to the review branch ran the registry-publish path. The workflow has no branch restriction on its `push` trigger in the scanned snapshot.

**Required remediation:** separate build/test from publish. PR and review-branch runs should build/test without registry write credentials and without pushing `latest`. Publish only from an explicitly trusted release branch/tag after required checks, in a dedicated job granting `packages: write`. Add a negative test proving review-branch and PR events cannot reach the publish job. Also pin actions and dependencies. Preserve the run as evidence; do not assume the image is harmless or delete it without checking registry tags/digests and downstream consumers.

### D. `workflow_run` downstream trust boundaries — P0

`evolution.yml` and `release-lock.yml` use `workflow_run`. `release-lock.yml` checks out `main`, runs `npm install`, and can push a tag/create a release with `contents: write`. Independently verify the triggering workflow identity, branch/repository, artifact provenance, and whether any untrusted run can influence the downstream release decision. Keep the privileged job restricted to trusted completed workflows and trusted immutable inputs; avoid executing untrusted artifacts or caches.

### E. `artipacked` — 18 Medium findings

These are credential-persistence warnings. Review each checkout's `persist-credentials` setting and whether `.git/config` or a credential-bearing repository state can be captured by artifacts/caches. A finding is not closed merely by adding `persist-credentials: false` at one checkout; verify every flagged path and inspect produced artifacts.

## actionlint — 97 diagnostics

- ShellCheck embedded diagnostics: {aclass['ShellCheck']}
- Other actionlint diagnostics: {aclass['actionlint']}

Rule counts:
- `ACTION_VERSION`: 4
- `IF_COND`: 1
- `SC2002`: 1
- `SC2034`: 1
- `SC2086`: 73
- `SC2129`: 16
- `SC2162`: 1

All 97 individual diagnostics, exact workflow file/line/column, message, source excerpt, and suggested evidence are in `TYPE1_ACTIONLINT_97_DIAGNOSTICS_REGISTER_V1.csv`.

Do not treat ShellCheck's SC2086 as automatically harmless or automatically a defect: inspect whether word splitting/globbing is intended and test the behavior. Do not silence warnings globally. Any suppression must be line-specific, justified, and tested.

## OpenSSF Scorecard — aggregate results

Scorecard reports overall **5.7/10**. The per-check results are in `TYPE1_SCORECARD_CHECKS_REGISTER_V1.csv`.

Notable checks from the raw JSON:

- `Token-Permissions`: 0 — workflow tokens with excessive permissions detected.
- `Pinned-Dependencies`: 3 — dependency not pinned by hash detected.
- `Vulnerabilities`: 0 — 73 existing vulnerabilities detected.
- `Security-Policy`: 0 — security policy file not detected.
- `Fuzzing`: 0 — project is not fuzzed.

**Critical limitation:** the supplied Scorecard JSON reports the count of 73 vulnerabilities but does not enumerate the individual vulnerability identifiers, affected dependency paths, versions, or fix versions. Therefore this package does not fabricate 73 rows. The 73 remain an aggregate unresolved evidence gap. A follow-up must retrieve the actual vulnerability source/report (for example dependency alerts or the exact Scorecard raw finding source) and build a separate CVE/advisory register with package, affected version, patched version, severity, reachability, remediation, and re-scan evidence.

## Mandatory independent review fields

For every row, the reviewer must record:

- reviewer identity and relevant software-security expertise;
- conflicts of interest and AI/tool assistance disclosure;
- exact rows/files and scope actually reviewed;
- disposition: `CONFIRMED`, `NOT_APPLICABLE`, `FALSE_POSITIVE`, `MITIGATED`, or `UNRESOLVED` (do not use `CLOSED` without evidence);
- reasoning and source-level evidence;
- remediation commit and verification run where applicable;
- UTC timestamp and closure evidence URI.

A scanner finding can be closed only after: (1) the code change is present in a new immutable commit, (2) the relevant tests/negative tests pass, (3) the scanner rerun on that exact commit no longer reports the finding or an independent reviewer documents a justified exception, and (4) the independent reviewer signs the disposition. A clean scan alone does not prove the fix is safe.

## Non-negotiable boundaries

- No edits to `main` during this triage.
- No merge to `main` based on this package.
- No protocol freeze, formal calibration, confirmatory execution, scientific claim support, or promotion authority is created by security triage.
- Historical Type-I calibration remains `NOT_PASSED`.
- Do not convert `UNKNOWN` to `NO`.
- Do not mark findings closed by inference, aggregate count, or workflow success.
- Keep software-security review separate from independent statistical-methods review and human occurrence adjudication.
