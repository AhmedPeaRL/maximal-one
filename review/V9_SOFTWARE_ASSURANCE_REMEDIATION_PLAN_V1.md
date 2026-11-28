# V9 Software Assurance Remediation Plan — V1

**Status:** TRIAGE_REQUIRED — NO FINDINGS CLOSED — NO SECURITY CLEARANCE — NO SCIENTIFIC AUTHORITY

## Scope and immutable provenance

- Repository: `AhmedPeaRL/maximal-one`
- Target scanned commit: `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`
- Review workflow-definition commit: `87160e6469d323187916d375c11300158777d22b`
- Workflow run: `44182949661`
- Artifact: `14372144011` (`type1-software-assurance-v3-44182949661-1`)
- Scanner manifest schema: `HCM_TYPE1_SOFTWARE_ASSURANCE_RUN_V3`
- Manifest status: `TARGET_COMMIT_SCANNED_RESULTS_REQUIRE_TRIAGE_AND_OCCURRENCE_LEVEL_REVIEW`
- Authority: `NONE`; claim support: `false`; promotion authority: `false`; confirmatory execution: `false`; formal calibration: `false`; protocol freeze: `NOT_FROZEN`.

The attached occurrence ledger is a transcription of the 205 Zizmor findings from this exact artifact. It is not a claim that every finding is exploitable. Do not suppress, dismiss, or close a finding solely to improve scanner counts.

## Scanner results

| Scanner | Result | Interpretation |
|---|---:|---|
| Zizmor 1.30.1 | 205 findings: 164 High, 37 Medium, 4 Informational; exit 14 | Open triage items; occurrence-level review required |
| Actionlint 1.7.12 + ShellCheck | 97 diagnostic headers; exit 123 | Includes style/info/warning findings; inspect each exact script context |
| Scorecard 5.6.0 | 5.7/10; exit 0 | 73 reported vulnerabilities; exit 0 is tool execution success, not a clean bill of health |

### Zizmor audit distribution

| Audit | Severity | Count |
|---|---|---:|
| `artipacked` | Medium | 18 |
| `cache-poisoning` | High | 1 |
| `dangerous-triggers` | High | 2 |
| `excessive-permissions` | High | 5 |
| `excessive-permissions` | Medium | 14 |
| `superfluous-actions` | Informational | 1 |
| `template-injection` | High | 5 |
| `template-injection` | Informational | 3 |
| `template-injection` | Medium | 5 |
| `unpinned-uses` | High | 151 |

### Highest-density paths

| Path | Findings |
|---|---:|
| `./.github/workflows/scientific-validation.yml` | 52 |
| `./.github/workflows/scientific-claim-promotion.yml` | 12 |
| `./.github/workflows/type1-v4-cross-runner-worker-order.yml` | 11 |
| `./.github/workflows/null-type1-calibration.yml` | 9 |
| `./.github/workflows/release-lock.yml` | 9 |
| `./.github/workflows/build-image.yml` | 6 |
| `./.github/workflows/cross_arch_timing.yml` | 5 |
| `./.github/workflows/timing_cross_arch.yml` | 5 |
| `./.github/workflows/codeql-analysis.yml` | 4 |
| `./.github/workflows/confirmatory-readiness-gate.yml` | 4 |
| `./.github/workflows/cross-run-memory-verification.yml` | 4 |
| `./.github/workflows/emergent-periodicity.yml` | 4 |
| `./.github/workflows/evolution.yml` | 4 |
| `./.github/workflows/replication.yml` | 4 |
| `./.github/workflows/reproducible_research.yml` | 4 |
| `./.github/workflows/theoretical_validity.yml` | 4 |
| `./.github/workflows/type1-review-snapshot.yml` | 4 |
| `./.github/workflows/validate-stress.yml` | 4 |
| `./core-scientific/.github/workflows/truth-pressure-lock.yml` | 4 |
| `./.github/workflows/acquire-secondary-data.yml` | 3 |
| `./.github/workflows/canonical-sync.yml` | 3 |
| `./.github/workflows/model-capacity-diagnostic.yml` | 3 |
| `./.github/workflows/model-capacity-sweep.yml` | 3 |
| `./.github/workflows/null-calibration-audit.yml` | 3 |
| `./.github/workflows/primary-null-capacity-audit.yml` | 3 |
| `./.github/workflows/run.yml` | 3 |
| `./.github/workflows/tag-signature-verify.yml` | 3 |
| `./.github/workflows/type1-calibration-runtime-pilot.yml` | 3 |
| `./.github/workflows/type1-full-path-equivalence.yml` | 3 |
| `./.github/workflows/type1-priority-occurrence-guard-tests.yml` | 3 |
| `./.github/workflows/type1-v3-v4-governance-audit.yml` | 3 |
| `./.github/workflows/type1-v4-assignment-matrix.yml` | 3 |
| `./.github/workflows/type1-v4-cli-resume-identity.yml` | 3 |
| `./.github/workflows/type1-v4-engineering-equivalence.yml` | 3 |
| `./.github/workflows/prospective-raw-audit.yml` | 2 |
| `./.github/workflows/type1-manual-adjudication-v3.yml` | 2 |
| `./.github/workflows/type1-v3-governance-implementation-snapshot.yml` | 2 |
| `./core-scientific/.github/workflows/witness-proxy.yml` | 1 |

## Required remediation order

### Gate 0 — contain high-impact automation before editing

1. In GitHub Actions UI, manually disable `Build and Push Container` (`.github/workflows/build-image.yml`) until it is redesigned as a build-only workflow with no push credentials or package-write permission. The scanned version grants workflow-level `packages: write`, checks out without `persist-credentials: false`, interpolates GitHub context directly into shell, and logs into/pushes GHCR. Do not pull, run, overwrite, or delete the historical `latest` image as part of this remediation. Preserve its digest and evidence.
2. Manually disable `Immutable Release Lock` (`.github/workflows/release-lock.yml`) until the `workflow_run` trust boundary and tag/release write path are redesigned. It checks out `main`, installs with mutable `npm install`, uses upstream workflow outputs in shell, pushes a tag, and creates a release. Do not test it by triggering it.
3. Keep Main frozen. Do not run any workflows during this remediation stage.

### Gate 1 — eliminate shell-expression injection

For every Zizmor `template-injection` finding, do not place `${{ ... }}` directly inside a `run:` script. Move the expression into a step-level `env:` variable and consume it as a quoted shell variable. For JSON, use an environment variable and write it with Python or `printf '%s'`; do not interpolate raw JSON into shell source. For example, in the two witness-payload steps in `scientific-validation.yml`, use `env: WITNESS_PAYLOAD_JSON: ${{ toJson(github.event.client_payload) }}` and in Bash `RAW="$WITNESS_PAYLOAD_JSON"`. In the later client-payload input steps, use a step-level `env: CLIENT_PAYLOAD_INPUT: ${{ github.event.client_payload.input }}` and `printf '%s\n' "$CLIENT_PAYLOAD_INPUT"` (or pass it through a file opened by Python). In `null-type1-calibration.yml`, move each matrix value used in shell `echo` statements into step-level `env:` variables; quote every expansion. Recheck indentation and each finding location against the exact branch HEAD before editing.

### Gate 2 — permissions and credential persistence

- Remove workflow-level write permissions wherever possible. Set a restrictive workflow default (`permissions: {}`) and grant only the exact permission at the exact job that requires it. For read-only jobs, `contents: read` is usually sufficient; do not assume it is sufficient without checking checkout, artifact, security upload, Pages, package, and deployment operations.
- In `scientific-validation.yml`, do not simply replace all permissions with `contents: read`: the workflow has multiple jobs and currently requests `contents`, `packages`, `pages`, `id-token`, and `security-events` write globally. Build a per-job permission matrix first, then grant only narrowly to jobs that demonstrably need it. Move secrets out of workflow-wide `env`; inject a secret only into the one step that needs it.
- Add `persist-credentials: false` to every checkout that does not explicitly need authenticated Git operations. For jobs that do need writes, prefer a narrowly scoped, short-lived token only at the write step; never leave credentials in the checkout workspace across build or untrusted code execution.
- For the `artipacked` finding in `build-image.yml`, disabling the workflow is the immediate containment. The eventual fix must ensure no `.git` credential material enters the Docker build context or any image layer; add a strict `.dockerignore`, use a clean source export/worktree, and inspect image layers before any republish.

### Gate 3 — pin actions and dependencies

- Resolve every `unpinned-uses` finding in the CSV against the official action repository and an immutable full 40-character commit SHA. Keep a human-readable version comment, e.g. `uses: owner/action@<40-char-reviewed-SHA> # vX.Y.Z`. Never invent or copy an SHA from a similarly named action. Verify the SHA belongs to the intended official repository and release.
- Apply the same pinning to transitive/reusable workflows where supported. Do not mass-replace `@vN` with an unverified SHA.
- Scorecard reports `Pinned-Dependencies = 3`; review lockfiles and all build/install commands. Replace mutable `npm install` with a committed lockfile and `npm ci`; require hash-pinned Python dependencies where compatible.

### Gate 4 — workflow_run, cache, and write-boundary review

- `dangerous-triggers`: review `evolution.yml` and `release-lock.yml`. A `workflow_run` consumer must treat upstream artifacts, branch names, commit SHAs, and outputs as untrusted. Verify expected repository, workflow ID, conclusion, event, branch, and exact commit before consuming any artifact. Do not check out `main` and execute data derived from an untrusted upstream run. Prefer replacing with a manually approved, protected workflow_dispatch or a trusted same-workflow dependency when appropriate.
- `cache-poisoning`: in `release-lock.yml`, do not restore a cache populated by untrusted PR/workflow contexts into a privileged write job. Separate unprivileged validation from privileged release; use no shared cache in the privileged job unless trust boundaries are proven.
- `excessive-permissions`: add explicit least-privilege permissions at workflow/job level, including explicit `permissions: {}` for jobs that need no token. Review each job in the 205-row ledger.

### Gate 5 — Actionlint/ShellCheck and Scorecard

- Use `V9_ACTIONLINT_DIAGNOSTICS_20261117.txt` as the exact 97-diagnostic source. Fix quoting and redirection warnings only after checking intended word splitting/globbing and output semantics. For SC2086, quote scalar variables; if intentional word splitting/globbing is required, document and narrowly suppress with a reason. For SC2129, group appends only if file ordering and failure behavior remain identical. Do not blanket-disable ShellCheck.
- Upgrade the old action references specifically flagged at `reproducible_research.yml`, `theoretical_validity.yml`, and `replication.yml` only after verifying compatibility and pinning immutable SHAs.
- Scorecard also reports `Token-Permissions = 0`, `Vulnerabilities = 0`, `Security-Policy = 0`, `Pinned-Dependencies = 3`, and `Fuzzing = 0`. These are separate workstreams. A score increase is not proof of security. Do not add fuzzing solely to increase a score; first define meaningful fuzz targets and oracle properties. Add a SECURITY.md policy with reporting instructions only after selecting a monitored contact/channel.

## Required evidence for closing each finding

A finding may be marked `FIXED_PENDING_RESCAN` only when all are present: (1) exact path and line/step; (2) original finding ID and scanner evidence; (3) minimal patch; (4) threat model / why the path is safe after patch; (5) regression test or static assertion where feasible; (6) clean scan of the exact patched commit; (7) independent reviewer sign-off. If the finding is not applicable, use `NOT_APPLICABLE_PENDING_REVIEW` with a written rationale and evidence; never silently delete it.

## Human review and scientific boundaries

- All software findings remain open until occurrence-level evidence and independent review exist.
- All three V9 preflight rows remain OPEN/PENDING; zero adjudications have been applied.
- Do not freeze the protocol, authorize formal calibration, authorize confirmatory execution, support the scientific claim, or grant promotion authority through this security remediation.
- The historical Type-I calibration result remains `NOT_PASSED`; no threshold changes, retrospective relabeling, or deletion of historical failures.

## Current disposition

`REMEDIATION_PLAN_ISSUED; CONTAINMENT_REQUIRED; OCCURRENCE_TRIAGE_OPEN; NO_FINDINGS_CLOSED; NO_AUTHORITY; NOT_FROZEN`
