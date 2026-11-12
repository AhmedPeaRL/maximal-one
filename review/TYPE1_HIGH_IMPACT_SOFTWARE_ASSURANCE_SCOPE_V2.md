# Type-I High-Impact Software Assurance Scope V2

## Frozen review identity (source identity only; protocol is not frozen)

- Repository: `AhmedPeaRL/maximal-one`
- Target commit: `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`
- Current main comparison: `e6234f6895e3bc6c10b089a5e4f741f2143bb02f`
- Inventory workflow run/artifact: `43249081611` / `13956859801`
- Inventory SHA-256: `448d7179e2beab25209afd97c31fc12e91b76c8b330eb97fe0c2a56fa212db4a`
- Target ledger SHA-256: `8ba997bed01134c1f7f56f7a0ae0181bdf77f63c64acc873e5e86f2c21e47f4c`
- Exact snapshot workflow run/artifact: `43249503611` / `13958602679`
- Snapshot manifest SHA-256: `755d86e6cb746edc6db8f008368ae2533a4b2b911f004b965336b36401d51159`
- Snapshot inner ZIP SHA-256: `aac17c4a022e01bfb926924de3c1fd485ccb71a7a5186e98ef9e08c7f205c825`
- Inventory and snapshot workflow-definition commit: `d0ec59c0af6f78aee2fdb01f5269067902ce320b`

## Matrix coverage

`TYPE1_HIGH_IMPACT_SOFTWARE_ASSURANCE_EVIDENCE_MATRIX_V2.csv` contains one row for each of the 1,800 target-ledger occurrences. The occurrence-local automated classification is preserved as a discovery aid only. It is not human adjudication.

The high-priority review subset is identified by the existing automated classes:

- `CODE_PATH_REQUIRES_CALL_GRAPH_REVIEW`
- `WORKFLOW_CONTROL_PATH`
- `EXECUTION_CAPABLE_WORKFLOW_CANDIDATE`

Every row remains `OPEN_UNASSESSED` until occurrence-specific evidence is entered. Call paths, token permissions, secrets access, third-party action pins, artifact trust boundaries, and fail-closed behavior are intentionally not guessed or populated from generic test success.

## Required per-occurrence evidence before closure

1. Exact source path, line, and immutable source commit.
2. Direct caller/workflow step and complete reachable call path, including reusable workflows, scripts, composite actions, dispatch/API entry points, and conditional invocation.
3. Trigger conditions, branch/tag/environment restrictions, and whether an untrusted actor can influence inputs.
4. Effective `GITHUB_TOKEN` permissions at workflow and job scope; secrets read/write paths; OIDC permissions; persisted checkout credentials.
5. Every third-party action and reusable workflow, immutable commit pin, permission scope, and supply-chain exposure.
6. Artifact producer run, artifact ID/name/digest, consumer run, download source, validation performed, and whether the artifact can affect an execution or decision.
7. Authorization guard order and explicit fail-closed behavior.
8. A negative test tied to this exact occurrence/call path, with run, job, artifact, and commit identifiers.
9. Reviewer identity, relevant expertise, conflicts, UTC review time, disposition, and closure rationale.

A general passing test, a successful workflow run, or a scanner's clean result is not sufficient to close an occurrence-specific finding.

## Automated tools

A prior assurance V1 run scanned the review-branch checkout (`d0ec59c...`) rather than a worktree at the target commit (`ad106...`). Its findings are preserved as preliminary triage only and are not copied into this matrix. The V2 assurance workflow must verify the exact snapshot artifact, create a Git worktree at the target commit, compare all 289 selected snapshot files against that worktree, and run actionlint, zizmor, and Scorecard against the target worktree. Until that run completes, all scanner fields remain `NOT_RUN_ON_EXACT_TARGET_COMMIT`.

## Authority boundary

This is an evidence-collection register only. It grants no protocol freeze, formal calibration authorization, confirmatory execution authorization, scientific claim support, promotion authority, or adjudication authority.


## Current-source identity note

The current main comparison is commit `e6234f6895e3bc6c10b089a5e4f741f2143bb02f` with 789 reconciled occurrences and 193 distinct inventory paths. The previous 728-count main comparison is retained as historical only. The target population remains 1,800 occurrences; the new and prior target ledger record payloads and occurrence-ID sets were independently compared and found equal, while the inventory identity envelope changed. No row has been human-adjudicated.


## Preliminary exact-snapshot scanner triage (local; not reviewer adjudication)

A local scan of the 38 workflow files present in the exact target snapshot found 5 actionlint diagnostics and 204 zizmor findings (163 High, 37 Medium, 4 Informational). Raw outputs and a location-level triage CSV are included in the package. Scorecard remains pending. These findings are not occurrence closures; the target-worktree GitHub assurance V2 run must repeat the scans and preserve its own run/artifact hashes.
