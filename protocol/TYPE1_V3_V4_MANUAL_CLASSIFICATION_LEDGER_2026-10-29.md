# Type-I V3/V4 Manual Classification Ledger

Status: INCOMPLETE — MANUAL REVIEW REQUIRED

Review branch: review/type1-v4-remediation

Review target:
- Review commit: `d49c428ad9633739db1c17c28ea1e9793a69c40f`
- Main comparison commit: `12f12e024a2e4d6eb7ec2e3232f77cde94af3b9a`
- Governance inventory artifact ID: `12866603073`
- Review files with matching references: `115`
- Main files with matching references: `67`
- Reviewer and review date: REQUIRED

## 1. Purpose

This ledger classifies the actual occurrences found by the automated
two-ref inventory. It is not a scientific approval, protocol freeze,
or authorization to execute formal calibration.

Do not infer that the automated inventory is exhaustive merely because
the workflow succeeded.

## 2. Required classifications

Assign each relevant occurrence exactly one primary class:

- HISTORICAL
- DIAGNOSTIC
- PROPOSAL
- GOVERNANCE
- EXECUTION-CAPABLE-BUT-GATED

For every execution-capable path, record its exact runner invocation,
trigger conditions, fail-closed guard, and regression test.

## 3. Occurrence ledger

Copy every relevant occurrence from the generated inventory into
the table below. Do not summarize multiple paths as one occurrence.

| Branch commit | File and line | Matched text | Class | Can reach runner? | Guard and regression test | Reviewer disposition |
|---|---|---|---|---|---|---|
| REQUIRED | REQUIRED | REQUIRED | PENDING | UNKNOWN | REQUIRED | OPEN |

Add one row for every occurrence of:
- `0.075`
- V3 and V4 matrix identifiers
- acceptance-rule constants and decision fields
- `confirmatory_execution_authorized`
- `formal_calibration_pass`
- runner entry points and indirect calls to them

## 4. Required workflow review

At minimum, inspect the complete current contents and call paths of:

- `.github/workflows/null-type1-calibration.yml`
- `.github/workflows/type1-v4-engineering-equivalence.yml`
- `.github/workflows/type1-v4-cli-resume-identity.yml`
- `.github/workflows/type1-v4-assignment-matrix.yml`
- `.github/workflows/type1-v4-cross-runner-worker-order.yml`
- `.github/workflows/type1-v3-v4-governance-audit.yml`
- `.github/workflows/type1-calibration-runtime-pilot.yml`
- `.github/workflows/scientific-validation.yml`
- `.github/workflows/scientific-claim-promotion.yml`
- `.github/workflows/confirmatory-readiness-gate.yml`

This list is a minimum review set, not a claim that no other workflow
can reach a calibration runner. Expand it using the actual inventory
and repository call graph.

For each workflow, record:
1. Every trigger and branch/path filter.
2. Every runner invocation, direct or indirect.
3. The matrix and protocol identity consumed.
4. The authorization checks executed before the runner.
5. Whether the workflow can set or influence formal-pass, claim-support,
   promotion-authority, or confirmatory-authorization state.
6. The exact negative test proving unauthorized execution is refused.

## 5. Acceptance-rule conflict

Preserve the historical rule and its historical results unchanged.

Historical rule:
- Two-sided 95% Wilson interval must contain nominal alpha = 0.05.
- Upper endpoint must be <= 0.075.

Candidate alternative:
- One-sided 95% Wilson upper bound <= 0.075.

These are different rules. Neither this ledger nor engineering CI
approves the candidate alternative.

Prospective decision:
- Approved V4 acceptance rule: NONE
- Independent human statistical reviewer: NOT PROVIDED
- Reviewer expertise and conflicts: NOT PROVIDED
- Reviewed commit and matrix digest: NOT PROVIDED
- Decision rationale: PENDING
- Effective date: PENDING
- Formal execution authorization: NOT GRANTED

Do not change 0.075, the confidence-bound rule, or historical
classifications after observing results in order to make a result pass.

## 6. Required fail-closed state

Until an attributable independent human statistical review and an
explicit prospective governance decision are complete:

- freeze_state = NOT_FROZEN
- confirmatory_execution_authorized = false
- claim_support = false
- promotion_authority = false
- formal calibration = NOT AUTHORIZED

Do not delete historical workflows or results to hide a conflict.
Do not silently repoint a V3 workflow to a V4 candidate.
Do not treat an engineering workflow as a formal calibration run.

## 7. Closure criteria

This ledger may be marked COMPLETE only after:
- Every occurrence in the generated inventory has a disposition.
- Every workflow and runner path has been inspected.
- Every execution-capable path has a documented fail-closed guard.
- The corresponding negative tests have actually passed.
- The reviewed branch commits and inventory artifact are recorded.
- The unresolved acceptance-rule decision remains explicitly unresolved
  until a qualified independent human reviewer provides an attributable
  prospective recommendation.

Completion of this inventory does not itself approve the acceptance
rule or authorize formal execution.
