# Type-I Calibration Acceptance Evidence Ledger V1

**Status:** `IN_PROGRESS_NOT_ACCEPTED`  
**Protocol status:** `DRAFT_PENDING_ATTRIBUTABLE_INDEPENDENT_STATISTICAL_REVIEW`  
**Freeze state:** `NOT_FROZEN`  
**Formal calibration authorized:** `false`  
**Claim support:** `false`  
**Promotion authority:** `false`

## 1. Scope

This ledger tracks evidence for three separate acceptance targets:

1. Production implementation equivalence.
2. Completion of the predeclared technical acceptance plan.
3. Scientific validity and authorization of formal Type-I calibration.

Passing a workflow or a limited test suite does not establish all three targets.

## 2. Verified workflow evidence

- Repository: `AhmedPeaRL/maximal-one`
- Branch: `review/type1-v4-remediation`
- Commit: `cc2847308632f754109d9ca9ba5cb5c6313b417b`
- Workflow run: `39635643168`
- Job: `119345241521`
- Runtime: Python `3.11.15`
- Pilot artifact: `type1-calibration-runtime-pilot`
- Artifact ID: `12361322271`
- Artifact SHA-256 reported by GitHub for the uploaded ZIP:
  `8b01309825cec231b77ffe65a93bcd068cd62f0b3cf19945bea7f5057cc3a899`

Observed workflow outcomes:

- Checkout identity verification: passed.
- Python compilation step: passed.
- Pilot unit tests: 8 passed.
- Production-equivalence test module: 2 passed.
- Exploratory pilot: 2 valid attempts, 0 invalid attempts.
- Artifact and manifest upload: passed.

These observations establish the outcome of this specific workflow run only. The ZIP digest is not the SHA-256 of the JSON payload itself.

## 3. Acceptance status

### A. Production implementation equivalence

Status: `PARTIAL_EVIDENCE_NOT_ESTABLISHED`

Evidence currently available:

- Endpoint comparison against a manually transcribed reference.
- Repeatability of one real null-path replicate with 200 requested surrogates.
- Pilot shard and merge unit tests, including identity and overlap checks.

Remaining requirements:

- Compare the implementation against an independently reviewed, versioned mathematical specification.
- Verify endpoint parameters, null fitting, AIC order selection, stationarity checks, fixed hold-back, surrogate refitting, upper-tail direction, add-one p-value, and invalid-result handling.
- Exercise the real execution path across connected runs, separate shards, reverse-order merge, checkpoint resume, and fresh uninterrupted execution.
- Compare canonical per-replicate records and final merged outputs.
- Test rejection of missing, duplicate, overlapping, mismatched, corrupted, and incomplete artifacts.
- Confirm the production surrogate count and invalid-attempt semantics are enforced end to end.

No equivalence pass may be declared until the required checks have explicit results and retained artifacts.

### B. Acceptance-plan completion

Status: `INCOMPLETE`

For every acceptance criterion, record:

- Criterion identifier and exact requirement.
- Test or artifact path.
- Exact commit SHA.
- Workflow run and attempt.
- Expected result and observed result.
- Pass, fail, blocked, or not run.
- Reviewer and review date, where applicable.

A missing result is not a pass. A failed or invalid attempt must not be silently discarded or replaced.

### C. Formal scientific calibration

Status: `NOT_AUTHORIZED`

The current V4 matrix remains a draft. The runtime pilot uses 200 surrogates and only two outer attempts in one scenario. It is a runtime and reproducibility check, not a Type-I calibration result.

Before formal execution:

- Resolve the estimand and acceptance rule prospectively.
- Obtain attributable independent human statistical review.
- Document the decision on the inherited 0.075 ceiling and the proposed one-sided Wilson upper-bound rule.
- Review all nine DGPs and their stationarity.
- Approve the invalid-attempt policy and Monte Carlo precision.
- Demonstrate production equivalence.
- Approve computational feasibility and artifact retention.
- Freeze the reviewed protocol in a distinct, traceable commit.

The proposed 18,000,000 surrogate draws must not begin as confirmatory calibration until the required authorization is documented.

## 4. Non-negotiable safeguards

- Do not modify `main` as part of this remediation step.
- Do not change acceptance thresholds after inspecting outcomes without a documented prospective amendment.
- Do not backdate review, approval, or protocol freeze.
- Do not treat AI-assisted review as independent human approval.
- Do not set `claim_support`, `promotion_authority`, or formal authorization to `true` without the required evidence and approvals.
- Preserve failures, invalid attempts, manifests, and workflow logs.
- Distinguish software correctness, synthetic operating characteristics, real-domain replication, and support for the broader HCM claim.

## 5. Current decision

`CONTINUE_REMEDIATION`

The latest exploratory workflow is successful. Full production equivalence, acceptance-plan completion, and formal scientific calibration remain unestablished.
