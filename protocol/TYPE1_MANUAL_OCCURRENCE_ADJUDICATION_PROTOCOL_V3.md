# Type-I V4 — Manual Occurrence Adjudication Protocol V3

## Status

REVIEW_PROTOCOL_ONLY_NOT_ADJUDICATION_NOT_AUTHORIZATION

V3 adds enforceable second-human-review requirements. It does not classify occurrences, freeze a protocol, authorize calibration, or support a scientific claim.

## 1. Immutable evidence batch

Target commit:
e41fb7392b58198e8a4d8fa28b470b12b6ad2c31

Target occurrences: 1711

Main comparison commit:
9a3390acedbb146111be64f9a45a00b41a85be25

Main occurrences: 622

Inventory SHA-256:
7171edb8da35b46a470e819626266f497983f4dee77c32ecc8aac2f82b9f86ec

Inventory run/artifact:
42354217305 / 13565989377

Snapshot run/artifact:
42354390832 / 13566373101

Keep target and main populations separate. Never silently regenerate, renumber, or rebind a batch after inventory changes.

## 2. Primary review and conflict disclosure

A repository author may conduct a disclosed primary review.

The author must disclose authorship and relevant intellectual, financial, supervisory, collaboration, and other conflicts.

AI systems may prepare navigation notes and evidence summaries, but cannot sign as human reviewers or provide independent human adjudication.

## 3. High-impact definition

A record is high-impact if:

- can_influence_execution == YES

OR its classification is one of:

- EXECUTION_ENTRY_POINT
- EXECUTION_CALLER
- WORKFLOW_TRIGGER_OR_CONTROL
- AUTHORIZATION_GUARD

UNRESOLVED influence or classification must never be downgraded to low-impact by inference.

## 4. Mandatory second human reviewer

Every V3 record contains a second_review object.

Allowed statuses:

- NOT_REQUIRED
- PENDING
- AGREED
- DISAGREED

Low-impact records may use NOT_REQUIRED with an explicit rationale.

High-impact records may remain OPEN with PENDING or DISAGREED.

A high-impact record may be CLOSED only when:

1. second_review.status == AGREED
2. The second reviewer is a distinct human from the primary reviewer.
3. Both reviewers disclose conflicts and roles.
4. The second reviewer records a timestamp and rationale.
5. Closure evidence is present.
6. The required negative test has passed.

AI, automated agents, and model outputs cannot serve as the second reviewer.

Disagreement remains OPEN. It must never be averaged or silently overwritten.

## 5. Closure requirements

CLOSED requires:

- Exact caller and execution-path evidence.
- Trigger and branch-condition evidence.
- Runner entry-point evidence.
- Actual authorization and guard-order evidence.
- A specific negative test with observed result.
- Run, job, artifact, and commit provenance.
- Exact closure references.
- A passed negative test.

UNRESOLVED, MISSING, NOT_YET_IDENTIFIED, unknown caller paths, and missing negative tests remain OPEN.

## 6. Non-authority safeguards

This adjudication workflow must never change:

protocol_freeze = NOT_FROZEN
formal_calibration_authorized = false
confirmatory_execution_authorized = false
claim_support = false
promotion_authority = false

## 7. Immutable batches

Use batches of 25–50 exact occurrence IDs.

Each batch records:

- Batch number
- Target commit
- Inventory SHA-256
- Count
- First and last occurrence ID
- SHA-256 of the canonical UTF-8 sequence of IDs

Canonical batch input means one occurrence ID per line, including the final newline.

Keep batch inputs and decisions as separate artifacts.

## 8. Completion

A population is complete only if every expected ID appears exactly once, no extras or duplicates exist, every record has an explicit disposition, every high-impact record has a second-review state, and every CLOSED record satisfies all closure gates.

CLOSED means only that the occurrence role was documented under this protocol. It does not establish code safety, protocol approval, statistical validity, or truth of the HCM claim.
