# Type-I V4 Review Handoff — Current Identity Addendum
Date: 2026-11-11

Status: REVIEW REQUEST ONLY — NOT APPROVED

## 1. Exact source identity

Repository: AhmedPeaRL/maximal-one

Review branch:
refs/heads/review/type1-v4-remediation

Current review-branch implementation commit:
a3412a9d10dd4b70d8603840edc2d931dd089c56

Current main comparison commit:
0fa531bc844b1891f0574564add8eef5e20813d8

Exact candidate source commit:
ad106dddd2b6c9a57c90bd5bdd9f4530fe7ac876

The candidate source commit, inventory source commit, and
snapshot review commit are all bound to ad106.

The workflow-definition commit is recorded separately.
It is a3412a9d10dd4b70d8603840edc2d931dd089c56.
It must not be conflated with the candidate source commit.

## 2. Latest inventory evidence

Workflow run:
42909270943

Artifact:
13807285083

Inventory artifact:
https://github.com/AhmedPeaRL/maximal-one/actions/runs/42909270943/artifacts/13807285083

Inventory JSON SHA-256:
b30db3cb254f276a6d2707cbdbc4bef06f1dad92c4063c7098eedaae84154c92

Target ledger SHA-256:
fcbc907daa1357570a20d592239a33c27deec9fb66e4bf60210cfaf9540fc976

Main ledger SHA-256:
9801d468bbd698e5978d66decd6888e857be918e8a0fa143ded4bb35bdd2abb2

Target:
- 1,800 occurrence records
- 271 distinct inventory paths

Main:
- 711 occurrence records
- 189 distinct inventory paths

The classification counts are occurrence records, not unique paths
and not human adjudications.

## 3. Exact target snapshot

Workflow run:
42909613428

Artifact:
13806352229

Snapshot artifact:
https://github.com/AhmedPeaRL/maximal-one/actions/runs/42909613428/artifacts/13806352229

Outer artifact ZIP SHA-256:
f53f36d58370b5e813a506f98ec93e58ca0c75d4274e1b3d2e06af69eda9f88b

Nested self-contained snapshot ZIP SHA-256:
0da0416e06ec85a9df8f38ed2b98accf6cb3426db5f3246e1452ee4cb03a3be5

Snapshot manifest SHA-256:
c79ff2a455e2597de93ab7ccb7ef55b6f805996b7ad93e7df57b0badbd520de1

Selected files: 289
Present files: 289
Missing required paths: 0
Missing scope paths: 0
Manual overlay records: 0

The three-way certificate binds:
- target_commit = ad106...
- inventory_source_commit = ad106...
- snapshot_review_commit = ad106...

Inventory workflow run: 42909270943
Snapshot workflow run: 42909613428

Both workflow-definition commits are recorded as a3412...

## 4. Human overlay and batch status

Human overlay preflight:
- Workflow run: 42907797383
- Artifact: 13805283527
- Status: IDENTITY_VERIFIED_PENDING_HUMAN_REVIEW
- Rows: 3
- All rows OPEN and PENDING
- Adjudications applied: 0
- Authority: NONE

Batch generation:
- Workflow run: 42908163975
- Artifact: 13806520959
- Batches: 72
- Batch size: 25
- Unique occurrence IDs: 1,800
- All 72 batch hashes verified
- Status: NAVIGATION_ONLY_NOT_ADJUDICATED
- Authority: NONE

The existing population register pins the earlier internally
consistent inventory/snapshot pair 42870936071 / 42871210051.
The later runs 42909270943 / 42909613428 are additional
re-verification evidence. Do not replace only one pinned ID.

## 5. Manual review population

The first three priority occurrences are:

1. refs/audit/target/2f8523fcf7c5/73/4
2. refs/audit/target/40d0253a5dd6/60/6
3. refs/audit/target/40d0253a5dd6/123/9

Their CSV records remain OPEN/PENDING until a human reviewer
completes the required fields.

AI systems may assist with code navigation and evidence summaries.
They cannot act as human reviewers or second reviewers.

All three are high-impact candidates because they invoke
execution-capable paths. A distinct human second review is required
before any high-impact record can be CLOSED.

## 6. Statistical review status

V4 remains:
- NOT_FROZEN
- confirmatory_execution_authorized = false
- claim_support = false
- promotion_authority = false

The acceptance rule remains unresolved.
The historical two-sided 95% Wilson results remain unchanged.
The historical 0.075 ceiling is not approved for V4.

No supplied workflow run is a formal V4 Type-I calibration.

## 7. Supersession note

This addendum supersedes only obsolete operational identity
instructions in earlier handoff documents where they refer to
the previous main commit or previous inventory/snapshot runs.

It does not rebind or overwrite the historical V3 ledger,
the e41fb population, or any historical batch.
