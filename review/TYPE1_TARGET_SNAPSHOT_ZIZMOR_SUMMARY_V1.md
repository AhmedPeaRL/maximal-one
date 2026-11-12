# Exact Target Snapshot Static-Analysis Triage V1

**Target commit:** `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`  
**Snapshot run/artifact:** `43249503611` / `13958602679`  
**Snapshot manifest SHA-256:** `755d86e6cb746edc6db8f008368ae2533a4b2b911f004b965336b36401d51159`  
**Workflow files scanned from the extracted snapshot:** 38

This is a local scan of the extracted exact snapshot payload. It is not yet the GitHub Software Assurance V2 worktree run, and it is not a human security review. Raw outputs and a row-level zizmor triage CSV accompany this summary.

## Results

| Tool | Version | Exit code | Findings |
|---|---:|---:|---:|
| actionlint | 1.7.12 | 1 | 5 diagnostics |
| zizmor | 1.30.1 | 14 | 204 findings |
| Scorecard | — | — | Not run on this extracted snapshot |

### actionlint — 5 diagnostics

1. `.github/workflows/replication.yml:18` — `actions/checkout@v3` is too old.
2. `.github/workflows/replication.yml:21` — `actions/setup-python@v4` is too old.
3. `.github/workflows/reproducible_research.yml:15` — `actions/setup-python@v4` is too old.
4. `.github/workflows/scientific-validation.yml:4249` — constant `if: false`; actionlint recommends removing the condition.
5. `.github/workflows/theoretical_validity.yml:18` — `actions/setup-python@v4` is too old.

### zizmor — 204 findings

| Finding | High | Medium | Informational | Total |
|---|---:|---:|---:|---:|
| `unpinned-uses` | 150 | 0 | 0 | 150 |
| `excessive-permissions` | 5 | 14 | 0 | 19 |
| `artipacked` | 0 | 18 | 0 | 18 |
| `template-injection` | 5 | 5 | 3 | 13 |
| `dangerous-triggers` | 2 | 0 | 0 | 2 |
| `cache-poisoning` | 1 | 0 | 0 | 1 |
| `superfluous-actions` | 0 | 0 | 1 | 1 |
| **Total** | **163** | **37** | **4** | **204** |

## High-severity locations requiring first-pass human triage

These are scanner findings, not independently confirmed exploitable vulnerabilities. Review exact context and reachable paths before disposition.

- `.github/workflows/build-image.yml:5` — `packages: write` permission.
- `.github/workflows/build-image.yml:30` — shell interpolation of `secrets.GITHUB_TOKEN` in a Docker login command.
- `.github/workflows/evolution.yml:2` — `workflow_run` trigger after `Evaluation Gate`.
- `.github/workflows/release-lock.yml:2` — `workflow_run` trigger after `Deterministic Scientific Mesh`.
- `.github/workflows/release-lock.yml:24` — `actions/setup-node@v4` cache-related finding.
- `.github/workflows/scientific-validation.yml:16-19` — workflow-level `contents: write`, `packages: write`, `pages: write`, and `id-token: write`.
- `.github/workflows/scientific-validation.yml:1509` and `1528` — `github.event.client_payload` interpolation into shell text.
- `.github/workflows/scientific-validation.yml:3289` and `3293` — external client payload interpolated into shell commands.

The complete finding list, including exact scanner-provided locations and feature snippets, is in `TYPE1_TARGET_SNAPSHOT_ZIZMOR_TRIAGE_V1.csv` and the raw JSON file.

## Required next step

Run `.github/workflows/type1-software-assurance-v2.yml` after it is committed. That workflow verifies the registered inventory and snapshot artifacts, fetches the exact target commit, compares all 289 selected snapshot files with a detached target-commit worktree, and reruns actionlint, zizmor, and Scorecard against that worktree. Only then should the reviewer receive the final scan bundle. None of these findings should be closed by a scanner result alone.
