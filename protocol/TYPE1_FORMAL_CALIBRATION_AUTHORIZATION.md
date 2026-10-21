# Type-I Calibration V4 — Formal Execution Authorization

**Authorization status:** `NOT_AUTHORIZED`
**Protocol:** `HCM_TYPE1_CALIBRATION_V4_DRAFT`

## 1. Separation of decisions

This record is separate from the protocol freeze decision.

A frozen protocol does not automatically authorize formal execution. This file does not grant authorization unless its fields are completed, reviewed, and explicitly approved by the authorized decision-maker after the freeze gate has been satisfied.

## 2. Mandatory authorization fields

Complete only after protocol freeze:

* Authorization decision: `NOT_AUTHORIZED` / `AUTHORIZED`
* Decision date:
* Authorized decision-maker:
* Frozen protocol commit SHA:
* SHA-256 hashes of the approved protocol and implementation files:
* Independent statistical review record:
* Freeze decision record:
* Approved scenario matrix version:
* Approved endpoint and null implementation versions:

## 3. Prespecified execution design

The approved authorization must explicitly state:

* Outer repetitions per scenario.
* Requested and minimum required valid surrogates per test.
* Master seed and deterministic seed derivation.
* Scenario list and execution order policy.
* The exact Type-I estimand and rejection rule.
* The acceptance criterion and its statistical justification.
* Handling of invalid outer attempts and failed surrogate fits.
* Handling of missing, duplicate, overlapping, corrupted, or mismatched records.
* Whether reruns are allowed and how they are recorded.
* Multiplicity policy and the scope of any overall conclusion.
* Required logs, manifests, hashes, and retained artifacts.

No field may be inferred from a successful pilot or silently borrowed from a different protocol version.

## 4. Stop conditions

The approved plan must define when execution stops. At minimum, stop and preserve evidence if:

* The running commit differs from the authorized commit.
* A protocol or implementation hash does not match.
* The scenario configuration differs from the frozen specification.
* Required surrogates cannot be produced under the approved policy.
* Any invalid attempt or integrity failure is being silently omitted or replaced.
* The expected execution identity, manifests, or shard records cannot be verified.
* The actual execution deviates from the authorized design.

A stop condition is not a pass. Preserve the failed run and document the reason.

## 5. Current authorization state

Until a separate, completed authorization is approved:

* `confirmatory_execution_authorized = false`
* `claim_support = false`
* `promotion_authority = false`
* Formal calibration: `NOT AUTHORIZED`

The exploratory pilot and engineering-equivalence tests do not grant formal calibration authority.
