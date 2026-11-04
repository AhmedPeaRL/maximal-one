# Type-I Evidence Governance Register V1

- **Repository:** `AhmedPeaRL/maximal-one`  
- **Review branch:** `review/type1-v4-remediation`  
- **Review commit:** `6eccb96af1cc04e99e93e9731cc5c4b99c34437c`  
- **Register status:** `EVIDENCE_CAPTURED_REVIEW_OPEN`  
- **Protocol freeze:** `NOT_FROZEN`  
- **Formal calibration authorization:** `false`  
- **Confirmatory execution authorization:** `false`  
- **Claim support:** `false`  
- **Promotion authority:** `false`

## 1. Purpose and authority

This register preserves the identity, provenance, and current adjudication status of the Type-I V3/V4 review evidence.

It is an evidence index and governance record only.

It does not:
- approve any occurrence classification;
- authorize formal Type-I calibration;
- authorize confirmatory execution;
- freeze a statistical protocol;
- establish scientific claim support;
- grant claim-promotion authority.

No workflow success may be interpreted as scientific approval.

## 2. Immutable review identity

| Field | Value |
|---|---|
| Repository | `AhmedPeaRL/maximal-one` |
| Review branch | `review/type1-v4-remediation` |
| Exact review commit | `6eccb96af1cc04e99e93e9731cc5c4b99c34437c` |
| Uploaded review ZIP | `maximal-one-review-type1-v4-remediation(20261104-185610).zip` |
| Uploaded ZIP SHA-256 | `4f81dcb5efdee83ef5b1945a3d1ab479cf49859bf038c5e6ba9d37351f4cb081` |
| Uploaded ZIP entries | `1227` |
| Uploaded ZIP uncompressed size | `5359873` bytes |
| Snapshot selected files | `260` |
| Snapshot present files | `260` |
| Snapshot missing required paths | `0` |
| Snapshot missing scope paths | `0` |
| Snapshot extraction verification | `verified=true`, `263` files checked, `0` errors |

The 260 selected repository files in the self-contained snapshot were compared against the uploaded ZIP and matched byte-for-byte.

The uploaded ZIP hash identifies that archive. The exact Git commit identity is established separately by the GitHub workflow and snapshot metadata.

## 3. Workflow evidence index

### 3.1 Governance inventory

- Run ID: `41862429343`
- Job ID: `126687640893`
- Job name: `governance-inventory`
- Conclusion: `success`
- Branch: `review/type1-v4-remediation`
- Commit: `6eccb96af1cc04e99e93e9731cc5c4b99c34437c`
- Artifact ID: `13340032892`
- Artifact name: `type1-v3-v4-governance-inventory-41862429343-1`
- Artifact SHA-256: `47937b4755af3bf6c75cee2c12bf4ef84b6a7e59cabd26bb20efc975dfe4f238`

Evidence contents:
- exact-commit reference inventory;
- exact-commit occurrence ledger;
- main-branch occurrence ledger;
- separate reconciliation reports.

Review inventory:
- occurrence count: `1630`;
- matched paths: `253`;
- reconciliation status: `RECONCILED`;
- missing occurrence IDs: `0`;
- duplicate occurrence IDs: `0`;
- identity field mismatches: `0`.

Main inventory:
- source commit: `fe0daded51229ed88d449c2eb68252455fd4ad7c`;
- occurrence count: `583`;
- reconciliation status: `RECONCILED`.

Reconciliation authority:
`NO_CLASSIFICATION_OR_EXECUTION_AUTHORITY`

### 3.2 Exact review snapshot

- Run ID: `41862918575`
- Job ID: `126689424015`
- Job name: `snapshot`
- Conclusion: `success`
- Branch: `review/type1-v4-remediation`
- Commit: `6eccb96af1cc04e99e93e9731cc5c4b99c34437c`
- Artifact ID: `13339773571`
- Artifact name: `type1-exact-review-snapshot-41862918575-1`
- Artifact SHA-256: `fce4d05a0056bb35be5e9e4b888f1c9776722944fd8219080347bfbe3f017284`

Snapshot metadata:
- schema: `HCM_TYPE1_REVIEW_SNAPSHOT_V3`;
- inventory artifact ID: `13340032892`;
- inventory source commit: `6eccb96af1cc04e99e93e9731cc5c4b99c34437c`;
- inventory JSON SHA-256: `a4045cf3da37451d7090c69ef22abdcae995ea329b1a4492c153d55731f6cd0d`;
- inventory occurrences: `1630`;
- selected scope: `260`;
- present files: `260`;
- missing required paths: `0`;
- missing scope paths: `0`;
- protocol freeze: `NOT_FROZEN`;
- formal calibration authorized: `false`;
- confirmatory execution authorized: `false`;
- claim support: `false`;
- promotion authority: `false`.

The manual adjudication overlay contains zero records. All 1630 occurrence records remain `UNKNOWN` and `OPEN`.

### 3.3 Priority guard verification

- Run ID: `41883085539`
- Job ID: `126760325020`
- Job name: `Priority execution-path guard verification`
- Conclusion: `success`
- Branch: `review/type1-v4-remediation`
- Commit: `6eccb96af1cc04e99e93e9731cc5c4b99c34437c`
- Artifact ID: `13350268226`
- Artifact name: `type1-priority-guard-test-evidence-41883085539`
- Artifact SHA-256: `74620b23ef7d475dd31074a0339ce3807c220cc18fc3b384a62ce7ca84f9812f`

Test:
`OFFICIAL_CLI_RESUME_IDENTITY_REJECTIONS_V2`

Results:
- identity fields tested: `19`;
- rejected resume attempts: `19`;
- expected rejection diagnostics observed: `19`;
- checkpoint hashes unchanged after rejection: `true`;
- manifest hashes unchanged after rejection: `true`;
- test status: `PASS`.

Interpretation:
Engineering rejection evidence only. This is not Type-I calibration.

Execution boundary explicitly recorded by the workflow:
- no standalone runtime-pilot workflow was dispatched;
- no cross-runner GitHub Actions workflow was dispatched;
- no formal Type-I calibration was invoked;
- no confirmatory execution was authorized.

## 4. Occurrence inventory status

The exact-commit inventory contains `1630` occurrences across `253` paths.

Automated classification counts:

| Automated classification | Count |
|---|---:|
| Protocol or documentation reference | 432 |
| Governance reference | 391 |
| Code path requiring call-graph review | 244 |
| Test or guard | 186 |
| Policy or historical reference | 143 |
| Workflow reference | 133 |
| Workflow control path | 84 |
| Other reference | 14 |
| Execution-capable workflow candidate | 3 |

These are discovery classifications, not human adjudications.

Current manual state:
- manually classified: `0`;
- manually closed: `0`;
- open or unknown: `1630`.

The three execution-capable candidate occurrences are located in:
1. `.github/workflows/type1-calibration-runtime-pilot.yml`
2. `.github/workflows/type1-v4-cross-runner-worker-order.yml` — connected reference invocation
3. `.github/workflows/type1-v4-cross-runner-worker-order.yml` — sharded worker invocation

The two cross-runner invocations are separate occurrence sites in one workflow, not two independent workflows.

## 5. Mandatory unresolved work

The following items remain OPEN.

### A. Manual occurrence adjudication
- review each occurrence in its source context;
- identify direct callers and indirect call paths;
- identify workflow triggers and branch restrictions;
- identify consumed protocol and matrix identities;
- identify execution authority and guard order;
- identify negative tests and their evidence;
- record reviewer disposition and closure evidence.

### B. Three priority execution paths
Trace the runtime-pilot, connected-reference, and sharded-worker invocations from workflow entry through Python CLI, function calls, identity validation, execution, and artifact output.

### C. Authorization boundaries
Verify that every unauthorized state fails closed, including wrong branch, commit, protocol, matrix, seed schedule, runner identity, platform, Python version, dependency lock, sample size, repetition range, scenario coefficients, and checkpoint identity.

### D. Execution-mode equivalence
Separately verify:
- connected execution;
- sharded execution;
- merged execution;
- resumed execution;
- worker-order invariance;
- artifact-loss behavior;
- failed-attempt behavior;
- denominator preservation;
- per-replicate record equality.

### E. Runner independence
Distinguish:
- repeated execution on one runner;
- separate jobs on the same runner class;
- execution on genuinely distinct GitHub-hosted runner instances;
- independent execution environments.

A different job ID alone is not proof of independent runner execution.

### F. Statistical authority
Keep engineering equivalence, Type-I calibration, confirmatory execution, and scientific claim support as separate decisions.

No engineering PASS may automatically authorize a statistical or scientific decision.

## 6. Evidence closure rule

An occurrence may be marked `CLOSED` only when its record contains:
1. exact occurrence ID;
2. exact source commit;
3. path and line;
4. human classification;
5. direct and indirect call-path evidence;
6. protocol and matrix identity;
7. guard and authorization-order evidence;
8. negative-test reference;
9. run, job, and artifact references;
10. relevant hashes;
11. reviewer disposition;
12. explicit closure rationale.

Missing evidence must remain `OPEN`.

`UNKNOWN` must never be silently converted to `NO`.

A workflow success must never silently close an occurrence.

## 7. Decision preservation

Any future protocol or acceptance-rule amendment must:
- identify the previous decision;
- preserve its original evidence;
- state the reason for amendment;
- identify the new prospective scope;
- record the exact commit and artifact hashes;
- preserve historical failures;
- avoid retrospective reclassification as confirmatory evidence.

## 8. Current governance decision

**Decision:** `EVIDENCE_CAPTURED_REVIEW_OPEN`

The three reviewed workflows provide successful evidence capture, snapshot verification, and bounded CLI resume-identity rejection tests.

The occurrence review is not complete.

The three priority execution paths are not yet independently closed.

Cross-runner execution and full execution-mode equivalence are not yet demonstrated by the three supplied runs.

Formal Type-I calibration remains unauthorized.

Confirmatory execution remains unauthorized.

Scientific claim support remains false.

Promotion authority remains false.

**Next authorized work:** manual occurrence adjudication and complete execution-path tracing, followed by separately controlled engineering-equivalence tests and independent statistical review.

**No scientific or confirmatory authority is granted by this register.**
