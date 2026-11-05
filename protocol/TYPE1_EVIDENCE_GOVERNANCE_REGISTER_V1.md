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

## 9. Evidence update — 2026-11-04

This addendum records the later review-branch evidence. It does not overwrite
or retroactively modify the earlier run identities above.

Repository: `AhmedPeaRL/maximal-one`

Exact review commit:
`04023ee26a210756ee4f71d75cfe96dfcd322dbe`

### 9.1 Governance inventory

- Run ID: `41904243262`
- Job ID: `126834528392`
- Job: `governance-inventory`
- Conclusion: `success`
- Artifact ID: `13360111421`
- Artifact name: `type1-v3-v4-governance-inventory-41904243262-1`
- Artifact ZIP SHA-256: `336e0101c5bdee0591cdb5f1ecf23630da7df39d37093f552b07b0f0356a589c`
- Inventory JSON SHA-256: `7bcedac25805046695517a9d137216eb694a0910e2ffe5574a48fc7bba31172f`

Observed review inventory before the governance-register exclusion:
- occurrences: `1640`;
- matched paths: `254`;
- reconciliation: `RECONCILED`;
- missing IDs: `0`;
- duplicate IDs: `0`.

The governance register itself contributed `10` discovery occurrences. The
inventory excluded only the generated occurrence ledger at this commit; it did
not yet exclude this register. The 10 register occurrences are therefore a
known self-reference inflation, not 10 independent execution paths.

Main comparison:
- commit: `fe0daded51229ed88d449c2eb68252455fd4ad7c`;
- occurrences: `583`;
- reconciliation: `RECONCILED`.

### 9.2 Exact review snapshot

- Run ID: `41904544815`
- Job ID: `126835587454`
- Job: `snapshot`
- Conclusion: `success`
- Artifact ID: `13359398622`
- Artifact name: `type1-exact-review-snapshot-41904544815-1`
- Artifact ZIP SHA-256: `499022a0a51b2708d71b71c1be082beb50e4ae23ead02357faf8a9e2e78b5242`
- Review commit: `04023ee26a210756ee4f71d75cfe96dfcd322dbe`
- Inventory artifact ID: `13360111421`
- Inventory JSON SHA-256: `7bcedac25805046695517a9d137216eb694a0910e2ffe5574a48fc7bba31172f`

Snapshot results:
- selected scope: `261` files;
- present files: `261`;
- missing required paths: `0`;
- missing scope paths: `0`;
- scanner exclusions: `1` (the generated occurrence ledger only);
- extraction verification: `verified=true`, `264` files checked, `0` errors.

The governance register is present in the self-contained snapshot at
`source/repository/protocol/TYPE1_EVIDENCE_GOVERNANCE_REGISTER_V1.md` with
SHA-256 `0011edf18babaf41c99d9d23b2a480b97cc6dfeb019bfcf68f35bda1368eacf5`.

The manual adjudication overlay contains zero records. No occurrence was
manually classified or closed by this snapshot.

### 9.3 Priority guard and negative-gate tests

- Run ID: `41904649393`
- Job ID: `126835953700`
- Job: `Priority execution-path guard verification`
- Conclusion: `success`
- Artifact ID: `13359847440`
- Artifact name: `type1-priority-guard-test-evidence-41904649393`
- Artifact ZIP SHA-256: `20c351f2eff96493bb20cc03e083e57fe0ccb2485261a7141f9f4ff5e3f78c6c`

The job ran `15` unit tests successfully. The CLI resume-identity test covered
`19` identity fields and verified rejection without mutating the original
checkpoint or manifest. These are bounded engineering guard tests only.

The workflow explicitly recorded that no standalone runtime-pilot workflow,
no cross-runner workflow, no formal Type-I calibration, and no confirmatory
execution were dispatched by this run.

### 9.4 Three priority execution occurrences

The exact inventory identifies these three execution-capable workflow sites:

| Occurrence ID | Source site | Preliminary human reading |
|---|---|---|
| `HEAD/2f8523fcf7c5/73/4` | `.github/workflows/type1-calibration-runtime-pilot.yml:73` | Exploratory pilot execution entry point; not formal calibration by label or scope |
| `HEAD/40d0253a5dd6/60/6` | `.github/workflows/type1-v4-cross-runner-worker-order.yml:60` | Connected-reference engineering execution entry point |
| `HEAD/40d0253a5dd6/123/9` | `.github/workflows/type1-v4-cross-runner-worker-order.yml:123` | Sharded-worker engineering execution entry point |

The second and third sites are separate invocation occurrences in one workflow,
not separate workflows. The current manual overlay still records all three as
`UNKNOWN` and `OPEN`; this table is a reviewer navigation aid, not a closure
record. The three supplied runs above do not execute these three routes and
cannot close their occurrences.

### 9.5 Outstanding controls and evidence

At commit `04023ee26a210756ee4f71d75cfe96dfcd322dbe`:
- `type1-v4-cross-runner-worker-order.yml` contains a branch and checkout guard
  in each of its three jobs;
- `type1-calibration-runtime-pilot.yml` contains a branch guard before output
  creation and pilot invocation;
- `type1-v4-engineering-equivalence.yml` has `workflow_dispatch` but no explicit
  job-level branch guard;
- `engineering_main()` does not independently enforce the review branch;
- the cross-runner comparator checks `runner_sha256` (runner source-code hash)
  and reports `platform_identity`, but has no required host-instance identity,
  workflow run/job identity, or per-replicate record archive.

These are engineering remediation targets, not completed fixes in the evidence
runs above. Full connected/sharded/merged/resumed equivalence, true distinct
runner execution, per-replicate cross-runner comparison, and upload/download
failure injection remain un demonstrated at this snapshot.

### 9.6 Current decision

`EVIDENCE_CAPTURED_REVIEW_OPEN` remains the decision.

All 1640 pre-remediation inventory occurrences remain open or unknown in the
current snapshot. The 10 self-referential register occurrences are identified
for discovery-only exclusion in the next prospective inventory run. The
register itself must remain in the snapshot and SHA-256 scope.

Formal Type-I calibration remains unauthorized. Confirmatory execution remains
unauthorized. Protocol freeze remains `NOT_FROZEN`. Claim support remains
`false`. Promotion authority remains `false`.


### 9.7 Live GitHub ruleset recheck — 2026-11-04

The live GitHub API was re-read for ruleset `12957369` (`Evolution Gate`).
It remains `active`, with `include: ["~DEFAULT_BRANCH"]` and
`exclude: ["refs/heads/main"]`. The repository API confirms that `main` is
the default branch. GitHub's ruleset semantics require an include match and
then veto any excluded ref; `~DEFAULT_BRANCH` targets the default branch.
Therefore, the current include/exclude combination leaves no effective target
branch. Do not assume this active ruleset currently protects `main`.

The live API currently reports ten required approving reviews, two entries
for the `Evolution Gate` status context (one with integration ID `15368`),
linear history, CodeQL scanning, code quality, Copilot code review, required
deployment environments, required signatures, and a branch-creation rule.
The committed `.github/rulesets/evolution-gate.json` remains a partial/stale
snapshot with zero required approvals and fewer rule types. It does not update
the live GitHub setting.

The branch-protection read endpoint returned HTTP 403 to the available GitHub
connection, so individual legacy branch-protection settings were not verified.
The live ruleset endpoint itself was readable. Owner action is required in
GitHub Settings to choose the intended target branches and feasible approval /
deployment requirements, then re-read the live API and update the committed
snapshot separately. Do not simply remove the `main` exclusion before deciding
whether ten approvals and the deployment requirements are feasible.

The post-remediation occurrence total is intentionally not predeclared as
`1630`: legitimate changes to runner code, tests, and workflow guards may add
new discoverable matches. The acceptance condition for this specific
self-reference fix is structural: the register must be absent from occurrence
entries, present in `excluded_paths` with a reason, and still present in the
snapshot's selected files and SHA-256 manifest. All other newly discoverable
matches remain in scope.
