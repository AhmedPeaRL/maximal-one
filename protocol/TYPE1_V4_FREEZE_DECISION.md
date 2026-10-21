# Type-I Calibration V4 — Freeze Decision

**Decision status:** `NOT_APPROVED_PENDING_REVIEW_CLOSURE`
**Protocol:** `HCM_TYPE1_CALIBRATION_V4_DRAFT`
**Working branch:** `review/type1-v4-remediation`

## 1. Authority

This file is a decision template and does not freeze the protocol by its existence.

The V4 protocol must remain `NOT_FROZEN` until the required independent review has been completed, every critical review condition has a documented disposition, and the exact reviewed snapshot has been identified.

## 2. Required preconditions

All items below must be evidenced before a freeze decision can be approved:

* [ ] Attributable independent human statistical review completed.
* [ ] Exact reviewed commit SHA recorded.
* [ ] SHA-256 hashes recorded for all protocol and implementation files in scope.
* [ ] Endpoint definition and invalid-input behavior approved.
* [ ] Null family, fitting procedure, stationarity checks, burn-in, and surrogate-generation rules approved.
* [ ] Sample-size and burn-in discrepancies resolved prospectively.
* [ ] Production surrogate count and valid-surrogate requirements resolved.
* [ ] Type-I acceptance rule and Monte Carlo precision justified prospectively.
* [ ] Invalid attempts, failed fits, missing artifacts, and reruns governed by an explicit policy.
* [ ] Scenario roles, resonance scenarios, exclusions, and multiplicity interpretation approved.
* [ ] Required production-path equivalence evidence inspected and accepted.
* [ ] Runtime and storage feasibility assessed for the approved design.
* [ ] All critical reviewer conditions closed or explicitly blocking.

## 3. Freeze decision record

Complete only after the preconditions are satisfied.

* Decision: `NOT_APPROVED` / `APPROVED`
* Decision date:
* Decision owner:
* Reviewed commit SHA:
* Independent review record:
* Protocol file hashes:
* Implementation file hashes:
* Evidence artifact identifiers:
* Conditions and limitations:
* Rationale:

## 4. State after this template is added

Unless a separate completed freeze decision is recorded:

* `freeze_state = NOT_FROZEN`
* `confirmatory_execution_authorized = false`
* `claim_support = false`
* `promotion_authority = false`

A successful CI run, a draft review, or the presence of this file does not constitute a freeze decision.
