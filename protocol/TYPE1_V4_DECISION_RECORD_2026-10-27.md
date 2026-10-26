# V4 Decision Record — 2026-10-27

## Decision

**Disposition: HOLD — NO FORMAL V4 CONFIRMATORY EXECUTION**

Decision scope: governance, engineering readiness, and the
prospective Type-I acceptance-rule decision.

Decision status: AI-assisted recommendation pending attributable
independent human statistical review. This record is not itself
independent statistical approval.

## 1. Consequences of this decision

Permitted:
- Engineering-only CLI, checkpoint, identity, artifact-integrity,
  shard-merging, and execution-order tests.
- Documentation and governance regression tests.
- Runtime and resource measurements that remain explicitly
  non-confirmatory.
- Preservation and analysis of historical evidence under the
  rule originally applied to each historical result.

Not permitted:
- Formal V4 Type-I calibration.
- Treating engineering equivalence as a Type-I calibration pass.
- Treating the value 0.075 as an approved acceptance threshold.
- Setting claim_support or promotion_authority to true.
- Changing historical outcomes, denominators, thresholds, or
  failure classifications to obtain a pass.
- Merging the review branch into main as a substitute for
  scientific approval.

The expected consequence is continued delay of confirmatory
claims until the remaining gates are resolved. This is preferable
to producing a formally successful run whose acceptance rule,
execution identity, or governance authority is not established.

## 2. Engineering evidence considered

Repository: AhmedPeaRL/maximal-one

Review branch:
review/type1-v4-remediation

CLI identity-test commit:
8164fc0d6b5364703574367f8ff52e6ec01f8ec1

CLI identity-test workflow:
https://github.com/AhmedPeaRL/maximal-one/actions/runs/40401666237

CLI identity-test job:
https://github.com/AhmedPeaRL/maximal-one/actions/runs/40401666237/job/121848811028

Alternative-partition workflow:
https://github.com/AhmedPeaRL/maximal-one/actions/runs/40401149060

Observed results:
- Artifact-integrity tests passed.
- Merger rejection tests passed.
- Synthetic resume-identity tests passed.
- The official CLI identity-rejection test passed.
- The bounded connected/sharded/merged/resumed equivalence test passed.
- The tested full-path procedure compared records across the
  tested partition and resume paths.

These are engineering results for the exact tested configurations.
They do not establish scientific calibration, null-model adequacy,
or HCM claim support.

The CLI identity test defines 19 identity fields. It constructs a
checkpoint through the engineering CLI and tests one field mutation
at a time. It requires a non-zero exit status, non-empty output,
and unchanged checkpoint and manifest bytes across the rejected
resume attempt.

Remaining limitations must not be concealed:
- The test currently accepts any non-zero exit code and any
  non-empty output; it should assert the expected identity-mismatch
  diagnostic and the expected exit code explicitly.
- The byte comparison covers the candidate checkpoint immediately
  before and after the rejected resume. A stronger test must retain
  an untouched baseline checkpoint and verify its bytes remain
  unchanged while each mutated candidate is tested separately.
- The existing partition tests run within the same workflow job.
  They do not establish invariance across distinct hosted runners
  or different worker environments.
- Successful bounded engineering execution is not formal V4
  calibration and does not freeze the V4 protocol.

## 3. Acceptance-rule conflict

Two rules must remain distinguishable.

Historical rule:
The two-sided 95% Wilson interval must contain nominal alpha 0.05,
and its upper endpoint must be <= 0.075.

V3 candidate rule:
The one-sided 95% Wilson upper confidence bound must be <= 0.075;
the two-sided interval is reported but does not decide acceptance.

These rules are not interchangeable. The historical rule remains
the rule used to interpret the historical runs to which it applied.
No historical outcome may be relabelled under a later rule.

The V4 acceptance rule remains UNRESOLVED and NOT_APPROVED.

The value 0.075 is not approved merely because it appears in
historical policy or candidate implementation code. It allows an
upper tolerance 50% above nominal alpha 0.05. A reviewer must
justify whether that tolerance is acceptable for the intended
scientific decision and what consequences follow from accepting it.

No prospective V4 rule is selected by this record. The required
decision is a single explicit rule, approved before confirmatory
execution, with its estimand, interval sidedness, confidence level,
threshold, scenario aggregation, invalid-attempt treatment,
and failure conditions all specified.

## 4. Required independent review

Before V4 freeze, an attributable independent human statistician
must document:

1. Relevant expertise and conflicts of interest.
2. Exact reviewed commit and matrix digest.
3. Target estimand and interpretation.
4. The proposed Type-I acceptance rule and interval sidedness.
5. The decision-consequence rationale for the tolerance boundary.
6. Operating characteristics and Monte Carlo precision.
7. The nine-scenario design and its limitations.
8. The policy for invalid attempts and incomplete surrogate counts.
9. The rule for aggregating scenario outcomes.
10. The implementation-equivalence and resource-feasibility evidence.
11. An explicit APPROVE, REVISE, or REJECT disposition.

An AI-generated draft, the project author's own review, or a
successful CI workflow must not be represented as independent
external statistical approval.

## 5. Required engineering gates

Before any formal authorization request:

- [ ] CLI rejection asserts the expected diagnostic and exit code.
- [ ] The untouched baseline checkpoint and manifest remain
      byte-identical throughout all mismatch tests.
- [ ] Every required identity field is tested independently.
- [ ] Logs and per-field outcomes are retained as artifacts.
- [ ] Alternative shard partitions produce identical canonical
      per-replicate records.
- [ ] Permuted replicate-to-worker assignment produces identical
      scientific records for every replicate.
- [ ] Worker-assignment testing distinguishes same-runner scheduling
      from actual multi-runner execution.
- [ ] Requested denominator N is preserved; no attempt is silently
      dropped or replaced.
- [ ] Invalid attempts retain their status and failure reason.
- [ ] V3/V4 workflow-separation regression tests pass.
- [ ] All historical failures remain preserved and correctly labelled.

## 6. Authorization state

Until the independent review, engineering gates, protocol freeze,
and separate authorization decision are complete:

freeze_state = NOT_FROZEN
confirmatory_execution_authorized = false
claim_support = false
promotion_authority = false
formal_calibration = NOT_AUTHORIZED

A later approval must identify its exact commit and protocol hashes.
It applies prospectively only to the explicitly approved protocol
and must not retroactively alter historical results.
