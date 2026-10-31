# Type-I V3/V4 Manual Classification Ledger V2

Status: OPEN — NOT COMPLETE
Review branch: review/type1-v4-remediation
Review target at creation: b9496c02f38770c57917fd06a5fdfb8016af9142
Inventory artifact at creation: 13030619492
Inventory workflow run: 41171524932

## 1. Purpose and authority boundary

This ledger records the manual classification of every relevant
occurrence found by the automated V3/V4 governance inventory,
plus additional execution and authorization paths discovered
through repository-wide call-graph inspection.

The automated inventory is a discovery aid. Its classifications
are not final human classifications.

This ledger does not:
- approve a statistical acceptance rule;
- freeze V3 or V4;
- authorize confirmatory execution;
- establish Type-I error control;
- establish HCM claim support;
- grant promotion authority.

## 2. Inventory baseline

The inventory artifact was generated from:

Review branch:
- ref: review/type1-v4-remediation
- commit: b9496c02f38770c57917fd06a5fdfb8016af9142
- files with matching references: 121
- occurrence matches: 804
- workflow files with matches: 31
- analysis/scripts files with matches: 9
- test files with matches: 16
- runner invocation candidates: 10

Main comparison:
- ref: main
- commit: 116686b03077f2521ab320635a098d5359c8d337
- files with matching references: 69
- occurrence matches: 203
- workflow files with matches: 26
- analysis/scripts files with matches: 7
- test files with matches: 3
- runner invocation candidates: 5

These are automated pattern-match counts, not counts of
independent execution paths or confirmed authorization routes.

The inventory must be regenerated after this ledger is committed.
The final ledger must identify the exact inventory artifact and
source commits used for its completed classification.

## 3. Mandatory classification vocabulary

Every occurrence must receive exactly one primary classification:

- HISTORICAL
- DIAGNOSTIC
- PROPOSAL
- GOVERNANCE
- EXECUTION-CAPABLE-BUT-GATED
- EXECUTION-CAPABLE-UNRESOLVED
- AUTHORIZATION-CONTROL
- TEST-OR-REGRESSION-GUARD
- DOCUMENTATION-ONLY
- UNKNOWN

UNKNOWN is the initial classification.
UNKNOWN must remain OPEN until sufficient evidence supports
a different classification.

Do not infer that a workflow is harmless from a matching line
alone. Inspect the entire workflow and all direct and indirect
calls reachable from it.

## 4. Required occurrence-level record

Create one record for every relevant inventory occurrence.
Do not collapse different lines or files into a single record.

Required fields:

1. Stable occurrence ID.
2. Repository ref.
3. Exact commit SHA.
4. Repository-relative file path.
5. Line number.
6. Exact matched text.
7. Automated inventory classification.
8. Final manual classification.
9. Historical / diagnostic / proposed / governance status.
10. Whether the occurrence can influence execution.
11. Direct caller or workflow step.
12. Indirect call path, if any.
13. Runner entry point or command.
14. Trigger conditions and branch restrictions.
15. Matrix and protocol consumed.
16. Authorization guard and its execution order.
17. Whether the guard fails closed.
18. Negative test proving refusal when unauthorized.
19. Test run, job, artifact, and exact commit.
20. Reviewer disposition.
21. OPEN or CLOSED status.
22. Evidence supporting closure.
23. Reason for any unresolved status.

Suggested stable ID format:

REF-SCOPE / PATH-SHA256-PREFIX / LINE / MATCH-INDEX

IDs must remain stable within the exact inventory snapshot.

## 5. Occurrence table

The table below is a schema example, not a completed classification.
Every inventory occurrence must be added as its own row.

| Occurrence ID | Ref | Commit SHA | Path | Line | Matched text | Automated class | Manual class | Execution influence | Call path / guard | Negative test | Evidence | Status |
|---|---|---|---|---:|---|---|---|---|---|---|---|---|
| REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED | REQUIRED | UNKNOWN | UNKNOWN | REQUIRED | REQUIRED | REQUIRED | OPEN |

No row may be marked CLOSED solely because:
- its workflow completed successfully;
- a test file exists;
- a guard string appears in the source;
- the automated inventory assigned a category;
- the path appears in a documentation file.

## 6. Minimum workflow and runner review

Inspect complete current file contents, triggers, conditions,
commands, called scripts, imported modules, and indirect call paths.

Minimum workflow scope:

- .github/workflows/null-type1-calibration.yml
- .github/workflows/type1-calibration-runtime-pilot.yml
- .github/workflows/type1-full-path-equivalence.yml
- .github/workflows/type1-v3-v4-governance-audit.yml
- .github/workflows/type1-v4-engineering-equivalence.yml
- .github/workflows/type1-v4-cli-resume-identity.yml
- .github/workflows/type1-v4-assignment-matrix.yml
- .github/workflows/type1-v4-cross-runner-worker-order.yml
- .github/workflows/scientific-validation.yml
- .github/workflows/scientific-claim-promotion.yml
- .github/workflows/confirmatory-readiness-gate.yml

The list is a minimum, not a claim of exhaustiveness.
Expand it using the generated inventory and repository call graph.

For each workflow, record:

1. Every trigger, including workflow_dispatch, push, schedule,
   repository_dispatch, and reusable workflow invocation.
2. Every branch and path filter.
3. Every direct runner command.
4. Every indirect script, module, or reusable workflow call.
5. Every matrix and protocol file read.
6. Every environment variable or input affecting authorization.
7. Every authorization guard and its position relative to execution.
8. Whether a bypass path exists.
9. Whether the workflow can set or influence:
   formal_calibration_pass,
   confirmatory_execution_authorized,
   claim_support,
   promotion_authority.
10. The exact negative test and its successful run evidence.

## 7. Minimum code-path review

Inspect at minimum:

- analysis/calibrate_null_type1.py
- analysis/calibrate_null_type1_scenario.py
- analysis/appropriate_stochastic_null.py
- analysis/null_protocol.py
- analysis/type1_calibration_pilot.py
- analysis/type1_execution_artifacts.py
- analysis/merge_type1_execution_shards.py
- analysis/merge_type1_calibration_pilot_shards.py
- analysis/compare_type1_cross_runner.py
- analysis/type1_acceptance_operating_characteristics.py
- scripts/audit_type1_governance_refs.py
- scripts/create_type1_review_snapshot.py

Expand this list whenever imports, subprocess calls, workflow
references, or dynamic invocation reveal additional paths.

## 8. V3/V4 separation

V3 and V4 must be reviewed as separate protocol identities.

Do not silently:
- redirect a V3 workflow to a V4 matrix;
- treat a V3 guard as V4 approval;
- reuse a V3 acceptance rule as an approved V4 rule;
- use an engineering-test flag as confirmatory authorization;
- interpret a successful governance inventory as scientific approval.

Record the exact matrix path and SHA-256 consumed by each
execution-capable path.

## 9. Acceptance-rule conflict — preserve unchanged

Historical rule:
- two-sided 95% Wilson interval must contain nominal alpha 0.05;
- upper endpoint must be no greater than 0.075.

Candidate alternative:
- one-sided 95% Wilson upper bound no greater than 0.075.

These are different rules.

The V3 candidate matrix contains a one-sided 95% Wilson proposal.
The V4 candidate matrix currently leaves acceptance_rule null
and explicitly records the 0.075 ceiling as not justified
or approved.

No rule is approved by this ledger.

Historical results and their original classifications must remain
unchanged. The exact historical AR5 interval must be retrieved
from its original immutable result artifact; do not estimate,
reconstruct, or invent endpoints.

No threshold, confidence rule, scenario, estimator, or invalid-result
policy may be changed after observing results merely to obtain a pass.

## 10. Current governance state

- V3 freeze state: NOT_FROZEN
- V4 freeze state: NOT_FROZEN
- Approved V4 acceptance rule: NONE
- Attributable independent human statistical review: PENDING
- Confirmatory execution authorized: false
- Formal calibration authorized: false
- Claim support: false
- Promotion authority: false

## 11. Closure criteria

This ledger may be marked COMPLETE only when:

1. Every relevant occurrence in the final inventory has a row.
2. Every row has a reasoned manual classification.
3. Every execution-capable path has a documented call path.
4. Every authorization guard has been inspected in execution order.
5. Every unresolved or ambiguous route remains OPEN.
6. Negative tests have actually passed on the reviewed commit.
7. Historical and proposed policy references are distinguished.
8. Review and main commits are recorded exactly.
9. Inventory artifact identity and hashes are recorded.
10. An attributable reviewer has signed off on the classification.

Completion means declared-scope coverage only.
It does not prove the absence of every conceivable execution path,
approve the protocol, authorize execution, or establish HCM.

## 12. Final disposition

Current disposition: OPEN — MANUAL CLASSIFICATION REQUIRED

No protocol freeze.
No confirmatory execution.
No claim promotion.
No retrospective reclassification.
