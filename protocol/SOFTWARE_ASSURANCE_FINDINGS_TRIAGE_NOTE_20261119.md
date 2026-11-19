# Exact-target software-assurance findings ledger — 2026-11-19

**Status:** `TRIAGE_REGISTER — NOT A CLOSURE DECISION — NO WORKFLOW AUTHORITY`

## Immutable evidence identities

- Repository: `AhmedPeaRL/maximal-one`
- Pinned target scanned: `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`
- Target scan run/artifact: `44182949661` / `14372144011`
- Target artifact SHA-256: `f88d5f18b91b0c6b97aa63aef8dc3f9cc4c7f3b1de83abce4f07addea72b182c`
- Target snapshot run/artifact: `43762349962` / `14180143511`
- Snapshot archive SHA-256: `caa75810be3463ddf09c6d379bd6685337bbee6be62284bf8fc877768b43364e`
- Later review-branch assurance run: `44408732399`
- Later scan commit: `1792d735c96622202c3c115701e53bbe49bc99e1`
- Later assurance artifact: `14475467384` (SHA-256 `bf5b299477b13f39929cc04a97e5c46ba5f812536fd7bd987380c2db05a080e5`)
- Later OSV artifact: `14475298142` (SHA-256 `d6e16a021dafc992faaa368834c56fc6967dbc604154a8ec13db916b8a327aaf`)
- Current review-branch head observed: `11877b56a12565cfda714236f87e0212618cd6cf`
- Current main head observed: `9749de9253f144eeda9e1b60cb219cfc5f201ecc`
- Main ZIP SHA-256: `f59222d0eedd9073ea15ef51b1463c3926e7948fd0e8d417a536c78756634091` (1,166 ZIP entries)
- Current review ZIP SHA-256: `14d0fc7bbbb023301fc5f57a87c3b3a4bb3ded6038d59bfc8351910467fa6ea7` (1,392 ZIP entries)
- The accompanying ZIP inventory CSV contains a stale review-ZIP row (`29062...`, 1,390 entries); the actual uploaded ZIP was re-hashed and its contents were checked against GitHub file blob SHAs.

## Register contents

- Zizmor: 205 target findings — {'High': 164, 'Medium': 37, 'Informational': 4}
- actionlint: 97 diagnostic headers
- OpenSSF Scorecard: 11 repository-level checks
- Total ledger rows: 313

The CSV contains the exact target path, line range, rule/severity, workflow route where supplied by zizmor, and the original finding text. It also records a conservative source-text comparison against the current review-branch ZIP and the later automated scan. In that comparison, 190 findings have source text no longer present at the old location, 13 findings refer to workflow paths removed/renamed out of `.github/workflows`, and 2 permission-key strings remain but are now job-scoped rather than workflow-scoped. All 205 remain `PENDING_MANUAL_REVIEW`; these mechanical comparisons are not closure decisions.

## Later automated evidence

On `1792d735c96622202c3c115701e53bbe49bc99e1`, the later assurance artifact records:
- actionlint exit code `0`, empty output;
- zizmor exit code `0`, empty findings array;
- Scorecard `8.6/10`;
- OSV Scanner exit code `0`, `results: []` across six supported manifests/lockfiles.

The later scan is remediation-context evidence, not an independent human adjudication of each original target finding. The target Scorecard run scored `5.7/10` and reported `73 existing vulnerabilities` in its Vulnerabilities check; the later Scorecard run scored `8.6/10` and reported `0 existing vulnerabilities`. OSV Scanner returned `results: []` with exit code `0` across six supported manifests/lockfiles. The comparison from `1792d735c96622202c3c115701e53bbe49bc99e1` to `11877b56a12565cfda714236f87e0212618cd6cf` contains only two documentation additions; no workflow or code file changed in those two commits.

## How to complete each row

For each original target finding, a human reviewer must set exactly one disposition only after inspecting the relevant target and current source:

- `FIXED_VERIFIED` — identify the remediation commit and cite the exact changed lines plus the later scan evidence.
- `OPEN` — the unsafe condition remains or the remediation is incomplete.
- `FALSE_POSITIVE` — provide a technical explanation specific to the finding and workflow context.
- `ACCEPTED_RISK` — provide owner, rationale, compensating controls, scope, and review/expiry date.

Do not use `NOT_REPRODUCED` as a final disposition. Do not infer closure from a zero exit code, a changed line number, a renamed path, a disabled UI toggle, or a Scorecard score. Preserve the original target finding and historical scanner output.

## Current preliminary comparison notes

- Two previous workflow-level permission findings have corresponding permission keys only at job scope in the current review source: `packages: write` in the publish job of `build-image.yml`, and `security-events: write` in the `core-proof` job of `scientific-validation.yml`, which runs CodeQL init/analyze. Confirm each job's actual need and trigger scope before marking `FIXED_VERIFIED`.
- The previous `evolution.yml` and `release-lock.yml` findings refer to paths removed from `.github/workflows` on the review branch; their files were moved under `docs/disabled-workflows/`. Confirm the current workflow directory and ensure no equivalent active workflow remains before closure.
- The remaining source-text changes require occurrence-by-occurrence review. The ledger deliberately does not label them fixed, false positive, or accepted risk.

## Authorization

This register does not authorize any workflow run, new snapshot, scientific calibration, confirmatory execution, claim support, or promotion. No workflow is authorized by this document.
