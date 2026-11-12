# Independent Software Assurance Review Scope — V1

- **Project:** Hybrid Consciousness Model (HCM)  
- **Repository:** AhmedPeaRL/maximal-one  
- **Review branch:** `review/type1-v4-remediation`  
- **Status:** DRAFT — NOT APPROVED  
- **Purpose:** Independent human review of software assurance and GitHub Actions security.

## 1. Review objective

Determine whether the identified high-impact execution paths and associated GitHub Actions workflows enforce the documented authorization, provenance, integrity, and fail-closed requirements.

This review is limited to software assurance. It does not evaluate or endorse the scientific HCM hypothesis, statistical calibration results, or claim-promotion decisions.

## 2. Required review domains

### A. Workflow entry points and trust boundaries

Inspect:
- Workflow triggers and event types.
- Branch and ref restrictions.
- Pull request and fork behavior.
- `workflow_dispatch`, `workflow_run`, and artifact-driven execution.
- Untrusted event payloads and expression interpolation.
- Reusable workflow invocation and trust boundaries.

### B. Authorization and permissions

Inspect:
- `GITHUB_TOKEN` permissions at workflow and job level.
- Least-privilege enforcement.
- Write permissions and protected-branch boundaries.
- Environment approvals and deployment restrictions.
- Secrets availability and exposure paths.
- Credential persistence and runner isolation.

### C. Software supply-chain integrity

Inspect:
- Third-party Action pinning to immutable commit SHAs.
- Reusable workflow pinning.
- Dependency and tool version pinning.
- Artifact provenance and digest verification.
- Artifact download path and untrusted archive handling.
- Cache poisoning and cross-run contamination risks.

### D. Call-graph and execution-path audit

For every selected high-impact occurrence, trace:

`workflow trigger → workflow job → step → shell/script entry point → imported modules → data/artifact outputs → downstream gate`

Record:
- Exact file path and line range.
- Entry point and all identified callers.
- Inputs and trust classification.
- Filesystem and network side effects.
- Secrets and token access.
- Output artifacts and their consumers.
- Authorization checks and failure behavior.
- Tests and evidence supporting the conclusion.

Unresolved or untraced paths must remain OPEN or UNKNOWN. UNKNOWN must never be converted to NO without evidence.

### E. Negative and fail-closed tests

Verify that:
- Wrong branch or commit identities are rejected.
- Wrong inventory or snapshot hashes are rejected.
- Missing or malformed provenance is rejected.
- Unauthorized execution paths cannot apply adjudications.
- A preflight-only run cannot mutate adjudication records.
- Failed verification cannot produce claim-promotion authority.
- Historical records remain unchanged when a new overlay is processed.

## 3. Required tools and limitations

The review may use `actionlint`, `zizmor`, OpenSSF Scorecard, `pinact`, custom static checks, and manual source tracing.

Tool output is evidence, not an independent assurance conclusion. The reviewer must inspect relevant findings, limitations, and false positives.

## 4. Required evidence

The review package must include:
- Exact reviewed commit and branch.
- Snapshot manifest and SHA-256 checksums.
- Workflow run and job IDs.
- Artifact IDs and artifact hashes.
- Tool versions and commands.
- Test results and logs.
- Call-graph coverage matrix.
- Open findings and unresolved limitations.

## 5. Required human reviewer declaration

The reviewer must declare:
- Name and institutional affiliation.
- Relevant technical expertise.
- Any actual or potential conflicts of interest.
- Whether the review was independent.
- Exact snapshot and hashes reviewed.
- Scope limitations.
- Findings and recommended remediation.
- Explicit decision: ACCEPT, ACCEPT WITH CONDITIONS, or REJECT.

## 6. Non-authorization statement

Passing automated checks does not constitute independent human review.

This document does not authorize statistical calibration, confirmatory execution, scientific claim support, or promotion authority.

**Current status:** AWAITING INDEPENDENT HUMAN REVIEW.
