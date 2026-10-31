# HCM Type-I V4 Independent Review Package Index V1

Status: PACKAGE IN PREPARATION
Review branch: review/type1-v4-remediation
Current reviewed candidate commit at package preparation:
b9496c02f38770c57917fd06a5fdfb8016af9142

## 1. Purpose

This index identifies the evidence required for independent
human statistical review of the V4 Type-I calibration candidate.

It distinguishes:
- governance inventory;
- engineering evidence;
- historical statistical results;
- protocol and implementation;
- manual governance classification;
- independent human review;
- protocol freeze and execution authorization.

No item in this index grants scientific or execution authority.

## 2. Current governance state

- V4 protocol: DRAFT_PENDING_REMEDIATION_AND_INDEPENDENT_REVIEW
- Freeze state: NOT_FROZEN
- Acceptance rule: UNRESOLVED
- Confirmatory execution: NOT_AUTHORIZED
- Formal calibration: NOT_AUTHORIZED
- Claim support: false
- Promotion authority: false

## 3. Governance inventory evidence

Latest successful governance inventory available at package preparation:

- Workflow run: 41171524932
- Job: 124450310270
- Review commit: b9496c02f38770c57917fd06a5fdfb8016af9142
- Artifact ID: 13030619492
- Artifact name:
  type1-v3-v4-governance-inventory-41171524932-1
- Artifact SHA-256:
  2537f50195fe17d637b534d4479beacf375b7e9456abecee0a7e01512279ae20

Inventory counts:

Review branch:
- 121 files with matching references
- 804 occurrence matches
- 31 workflow files
- 9 analysis/script files
- 16 test files
- 10 runner invocation candidates

Main:
- commit 116686b03077f2521ab320635a098d5359c8d337
- 69 files with matching references
- 203 occurrence matches
- 26 workflow files
- 7 analysis/script files
- 3 test files
- 5 runner invocation candidates

Interpretation:
These counts are automated pattern matches.
They are not final manual classifications or proof of
the number of executable paths.

A new inventory must be generated after the package files
are committed to the review branch.

## 4. Engineering evidence — separate from calibration

### E12 — Official runner connected/sharded/merged/resumed equivalence

- Workflow run: 41168321353
- Job: 124440601976
- Tested commit: 8a44db02d71612276e8c95256317dae2a7eb6cbe
- Artifact ID: 13031162790
- Artifact SHA-256:
  d5374ef781c28010b84e594be728dd16959a84ef132cdeb798d4712a92980dbc

Recorded scope:
- connected execution;
- alternative shard partitioning;
- merge in normal and reverse order;
- interrupted and resumed execution;
- worker-order equivalence;
- six replicate indices;
- one declared AR(2) engineering scenario;
- 1,000 requested surrogates per replicate;
- tested Python 3.11.15 environment.

The artifact reports:
- mismatches: none in the tested comparisons;
- invalid attempts observed: zero;
- formal_calibration_pass: false;
- confirmatory_execution_authorized: false;
- claim_support: false;
- promotion_authority: false.

Interpretation:
Bounded engineering-path equivalence only.
This is not a nine-scenario Type-I calibration.
It is not evidence that the Type-I error rate is controlled.

### E9 — CLI resume identity rejection

The same engineering artifact contains a resume identity summary
covering 19 declared identity fields.

The recorded tests require mismatched resumes to fail and
preserve checkpoint and manifest hashes.

Interpretation:
Evidence for the tested CLI identity-rejection cases only.

### E8–E11 historical engineering records

Earlier engineering evidence is recorded in the existing
engineering addendum and associated workflow artifacts.

Each item must retain its original run, job, artifact,
commit, scope, and limitations.

Do not combine engineering runs from different commits into
a single claim of full production validation.

## 5. Historical statistical evidence

Historical V1 result:

- Overall status: NOT_PASSED.
- AR(1): 52/1000; two-sided 95% Wilson interval
  [0.039873, 0.067556].
- AR(2): 60/1000; interval
  [0.046896, 0.076471].
- AR(5): 49/1000; exact interval must be taken from
  the original immutable historical artifact.
- AR(10): 73/1000; interval
  [0.058459, 0.090809].

Historical rule:
- two-sided 95% Wilson interval contains 0.05;
- upper endpoint <= 0.075.

The historical overall outcome remains NOT_PASSED.
No historical result may be silently reclassified.

## 6. Protocol materials

Required protocol materials include:

- protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V3.json
- protocol/TYPE1_CALIBRATION_SCENARIO_MATRIX_V4_CANDIDATE.json
- protocol/TYPE1_CALIBRATION_SPEC_V3_CANDIDATE.md
- protocol/TYPE1_CALIBRATION_V4_ACCEPTANCE_RULE_DECISION_REQUEST.md
- protocol/TYPE1_V4_ACCEPTANCE_RULE_DECISION_RECORD.md
- protocol/TYPE1_ACCEPTANCE_RULE_DECISION_RECORD_V2.md
- protocol/TYPE1_CALIBRATION_EXECUTION_AUTHORIZATION.json
- protocol/TYPE1_CALIBRATION_FREEZE_DECISION.json

The V3 candidate's one-sided Wilson proposal must not be
treated as an approved V4 rule.

The V4 candidate currently has no approved acceptance rule.

## 7. Required manual governance evidence

Required:

- protocol/TYPE1_V3_V4_MANUAL_CLASSIFICATION_LEDGER_V2.md
- exact occurrence-level classification for the final inventory;
- workflow and runner call-path review;
- authorization guard-order review;
- negative-test evidence;
- unresolved-path register;
- reviewer attribution and disposition.

The ledger must remain OPEN until every declared occurrence
and discovered execution path has a supported disposition.

## 8. Independent human review

Required:

- protocol/TYPE1_V4_INDEPENDENT_HUMAN_STATISTICAL_REVIEW_REQUEST_V1.md
- reviewer identity and relevant qualifications;
- conflicts and prior involvement;
- exact reviewed commit;
- exact matrix, runner, dependency, and workflow hashes;
- reasoned decision;
- limitations and required amendments;
- attributable written confirmation or signature.

AI-generated analysis is not independent human approval.

## 9. Exact review snapshot

The final package must contain:

- exact review commit SHA;
- exact inventory artifact ID;
- inventory source commit;
- snapshot manifest.json;
- SHA256SUMS.txt;
- missing_required_paths result;
- missing_scope_paths result;
- all required source and protocol files;
- evidence artifact IDs and their source commits.

The inventory artifact must be from the same review commit
as the snapshot target.

An engineering-equivalence artifact is not a governance
inventory artifact and must never be supplied as one.

## 10. Package acceptance checklist

The package is ready to send for independent review only when:

- [ ] final review commit is fixed;
- [ ] governance inventory is regenerated for that commit;
- [ ] inventory artifact provenance matches that commit;
- [ ] exact snapshot is generated;
- [ ] no unexplained missing required paths remain;
- [ ] SHA256SUMS is present;
- [ ] manual occurrence ledger is complete or all unresolved
      items are explicitly disclosed;
- [ ] historical results and failures are preserved;
- [ ] engineering evidence is clearly labeled as engineering;
- [ ] statistical protocol and acceptance-rule conflict are explicit;
- [ ] reviewer identity and conflict disclosure are recorded;
- [ ] reviewer receives the complete immutable package.

## 11. Final authority boundary

Package completion is not protocol approval.

Independent review is not protocol freeze.

Protocol freeze is not execution authorization.

Execution authorization is not proof of HCM.

Each transition requires a separate, attributable decision
bound to an exact commit and exact file hashes.
