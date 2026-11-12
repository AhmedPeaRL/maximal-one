# Type-I High-Impact Software Assurance Scope V1

## Frozen review identity (source identity only; protocol is not frozen)

- Repository: `AhmedPeaRL/maximal-one`
- Target commit: `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`
- Current main comparison: `fe949fc4a11d245f08846d7eece97e8c1d26a3f8`
- Inventory workflow run/artifact: `43199940422` / `13934996445`
- Inventory SHA-256: `4e721c8dd55425c0d25dd043c3ec8433c4a4b96d1c11d6d4cb94acfaabb774b3`
- Target ledger SHA-256: `244e27410b76b799be39be3939df840a93b5d16234827c549914945a877f3b16`
- Exact snapshot workflow run/artifact: `43200187487` / `13934059710`
- Snapshot manifest SHA-256: `bed97717964c43412dbceeac0fa0db4a0c3fdaec390509093eca2953be4aef64`
- Snapshot inner ZIP SHA-256: `40bba7ef5b623e2a93a4bd3b658e5b59ee69b16ebd0abd8df455d07cb68684da`
- Inventory and snapshot workflow-definition commit: `2c228430b32b489d22e92298cc2edca6098acffb`

## Matrix coverage

`TYPE1_HIGH_IMPACT_SOFTWARE_ASSURANCE_EVIDENCE_MATRIX_V1.csv` contains one row for each of the 1,800 target-ledger occurrences. The occurrence-local automated classification is preserved as a discovery aid only. It is not human adjudication.

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

As of preparation of this matrix, `actionlint`, `zizmor`, and `scorecard` were not installed in the available execution environment and no results are claimed. The matrix records all three as `NOT_RUN`. A later assurance run must record exact tool versions, invocation arguments, repository commit, configuration, exit code, raw output artifact, and any suppressions. Pin any GitHub Actions used to immutable commit SHAs; do not use floating tags for security scanning.

## Authority boundary

This is an evidence-collection register only. It grants no protocol freeze, formal calibration authorization, confirmatory execution authorization, scientific claim support, promotion authority, or adjudication authority.
