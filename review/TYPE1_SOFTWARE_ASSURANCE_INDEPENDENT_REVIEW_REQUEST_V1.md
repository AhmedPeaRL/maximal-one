# Independent Software-Assurance Review Request V1

## Requested review

Please conduct an independent, occurrence-specific software assurance review of the Type-I governance and execution-control surface in `AhmedPeaRL/maximal-one`.

**Target source commit:** `ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876`  
**Exact snapshot run/artifact:** `43249503611` / `13958602679`  
**Snapshot manifest SHA-256:** `755d86e6cb746edc6db8f008368ae2533a4b2b911f004b965336b36401d51159`  
**Inner snapshot ZIP SHA-256:** `aac17c4a022e01bfb926924de3c1fd485ccb71a7a5186e98ef9e08c7f205c825`  
**Inventory run/artifact:** `43249081611` / `13956859801`  
**Inventory SHA-256:** `448d7179e2beab25209afd97c31fc12e91b76c8b330eb97fe0c2a56fa212db4a`  
**Target occurrence population:** 1,800  
**High-priority review subset:** 374 (253 code-path, 118 workflow-control, 3 execution-capable workflow candidates)

The snapshot certificate reports 289/289 selected files present, no missing required or scope paths, 292 extraction checks, and no extraction errors. These are identity and packaging checks, not proof of execution safety.

## Reviewer independence and qualifications

Please state:
1. Your identity and relevant professional experience in GitHub Actions security, CI/CD supply-chain security, Python execution paths, or equivalent software assurance.
2. Any financial, professional, collaborative, authorship, or other conflicts of interest.
3. Whether you reviewed the exact target commit and the full 289-file snapshot, and what you did not review.
4. Whether your review was independent of the project author and implementation authors.

## Required review method

Use the V2 evidence matrix as a navigation register, not as a pre-adjudicated finding list. For every occurrence you close, cite occurrence ID, exact path/line, target commit, evidence, and rationale. At minimum, examine:

- Workflow triggers, branch/tag/environment conditions, dispatch/API entry points, reusable workflows, composite actions, scripts, and reachable call paths.
- Effective workflow/job `GITHUB_TOKEN` permissions, secrets exposure, OIDC permissions, checkout credential persistence, and untrusted-input boundaries.
- Third-party actions and reusable workflow references, immutable pins, and supply-chain exposure.
- Artifact producer/consumer run identity, artifact ID/name/digest, download source, validation, and trust boundary.
- Authorization-guard ordering and fail-closed behavior.
- Negative tests tied to the exact occurrence and reachable execution path, with run/job/artifact/commit evidence.

Scanner output (actionlint, zizmor, Scorecard) is triage evidence only. A passing generic test or clean scanner result does not close an occurrence. Findings must remain OPEN when the call path, guard behavior, or evidence is incomplete. Do not infer that an UNKNOWN classification is safe or non-executable.

## Required deliverable

Return a signed or attributable report containing:
- Exact reviewed commit and snapshot hashes.
- Reviewer identity, expertise, conflicts, review date/time UTC, and reviewed/not-reviewed scope.
- Findings grouped by severity and occurrence ID.
- Complete path/call-graph evidence and relevant token/secrets/artifact analysis.
- Negative-test evidence and reproducible steps for each proposed closure.
- Explicit unresolved items and limitations.
- A clear decision: PASS, PASS_WITH_OPEN_ITEMS, or NOT_PASSED, with rationale.

Do not authorize statistical calibration, confirmatory execution, protocol freeze, scientific claim support, or promotion. Those decisions are outside this software review.
