# Type-I Branch Identity and Artifact Ledger — 2026-11-03

Authority: Artifact identity and inventory reconciliation only.
Scientific approval: NONE.
Protocol freeze: NOT FROZEN.
Confirmatory execution: NOT AUTHORIZED.

## 1. Exact source identities

Repository: AhmedPeaRL/maximal-one

Main:
- Branch: main
- Commit: 3899c6aa5a0d0f486bb3e78373d9b04d9ae155f6

Review:
- Branch: review/type1-v4-remediation
- Commit: e8e127259e475b06599d3f5fc550cd6a616a127f

These refs are separate. Never reassign a run or artifact
from one branch to the other.

## 2. Main negative execution test

- Run: 41334991587
- Job: 124932813848
- Scenario job: 124932872243
- Run conclusion: failure
- Preparation job: failure
- Scenario job: skipped
- Artifacts: zero

Disposition:
EXPECTED_FAIL_CLOSED_BEHAVIOR_OBSERVED.

This is not a successful calibration run.

## 3. Review-branch governance inventory

- Run: 41349619676
- Job: 124976784699
- Commit: e8e127259e475b06599d3f5fc550cd6a616a127f
- Artifact: 13100800974
- Artifact ZIP SHA-256:
c31764a100654eef4fe7a71dbdca7a187bac452db303ad89f5d4a55a6ff27799

Inventory results:
- Review branch: 1,532 occurrence records; RECONCILED.
- Main branch: 563 occurrence records; RECONCILED.

All review-branch records remain:
manual_classification = UNKNOWN
status = OPEN
reviewer_disposition = PENDING

All main-branch records remain:
manual_classification = UNKNOWN
status = OPEN
reviewer_disposition = PENDING

Reconciliation proves occurrence identity and coverage only.
It does not establish manual review, call-path safety,
guard ordering, or scientific approval.

## 4. Review-branch exact snapshot

- Run: 41349751627
- Job: 124977174577
- Commit: e8e127259e475b06599d3f5fc550cd6a616a127f
- Artifact: 13099834438
- ZIP SHA-256:
440529730ba5111baef36abf4429b3de8dd41f24cf4c11b170f1ee4d0ce57c5f

Manifest SHA-256:
7b7aa0d1409048779ee324a80a69b37d755c9539d23beb5d6fbac16585695a16

SHA256SUMS.txt SHA-256:
71e9f6a60bed0b0e3f92d594d446bcc0b68a46a1cd0c70f37e98d788c1c72528

Snapshot identity:
- Inventory source commit: e8e127259e475b06599d3f5fc550cd6a616a127f
- Inventory artifact: 13100800974
- Inventory paths: 242
- Required anchors: 40
- Selected paths: 249
- Present files: 249
- Missing required paths: 0
- Missing scope paths: 0
- Scanner exclusions: 1

The ZIP contains manifest.json and SHA256SUMS.txt.
It is not a source-code bundle.

## 5. Authority boundary

RECONCILED does not mean REVIEWED, SAFE, APPROVED, or FROZEN.

No review-branch evidence establishes the same controls
on main.

No merge, force push, protocol freeze, formal calibration,
claim support, or promotion is authorized by this ledger.

Current disposition:

BOTH_INVENTORIES_RECONCILED;
HUMAN_CLASSIFICATION_OPEN;
CALL_GRAPH_REVIEW_OPEN;
V4_NOT_FROZEN;
FORMAL_CALIBRATION_NOT_AUTHORIZED;
CLAIM_SUPPORT_FALSE;
PROMOTION_AUTHORITY_FALSE.
