# Prospective Null-Protocol Design Record

Date: 2026-10-13
Status: "DRAFT_FOR_INDEPENDENT_REVIEW"
Scientific role: Protocol design and governance only
Confirmatory authorization: Not granted
Claim-promotion authority: Not granted

---

1. Purpose

This record defines the decisions that must be resolved before a new confirmatory analysis of the Constrained Spectral Persistence Hypothesis can be authorized.

It responds to the primary-domain AR model-capacity review, unresolved stochastic-null adequacy, incomplete Type-I error calibration, and the absence of two eligible independent secondary real-domain replications.

This document does not establish that the current null model is adequate or inadequate. It does not establish, support, or falsify the scientific hypothesis.

---

2. Current Evidence Boundary

The current record reports that:

- The primary stochastic null has not been rejected under the currently reported test.
- The current AR(p) null family is exploratory and is not frozen for confirmatory inference.
- The primary-domain capacity diagnostic reported 937 maximum-order selections among 1,000 valid surrogate refits under the recorded configuration.
- Type-I error calibration did not pass every declared synthetic scenario.
- Two eligible independent secondary real-domain replications have not been established.
- Computational reproducibility and scientific replication are distinct requirements.
- Historical results affected by post-observation protocol amendments must not be represented as preregistered confirmatory evidence.

These statements describe the recorded state. They do not determine which alternative null family, if any, is scientifically appropriate.

---

3. Decisions Required Before Protocol Freeze

Every item below must be resolved, justified, versioned, and reviewed before a new confirmatory outcome is examined.

3.1 Scientific question and endpoint

- Primary scientific question: UNRESOLVED
- Primary endpoint: "canonical_primary_alpha"
- Estimator and preprocessing configuration: retain the existing declared configuration unless a prospective, independently justified amendment is approved.
- Direction of the alternative: "greater_than_null"
- Primary frequency band: "0.01–0.05"
- Any proposed change must state its scientific rationale, implementation consequences, and validation requirements.

No endpoint or configuration may be selected because it produces a more favorable result in the existing data.

3.2 Null-family specification

- Candidate null family: REQUIRES FORMAL REVIEW
- Scientific assumptions: NOT YET APPROVED
- Treatment of nonstationarity: NOT YET APPROVED
- Treatment of periodicity and nuisance structure: NOT YET APPROVED
- Model-selection procedure and capacity: NOT YET APPROVED
- Treatment of boundary-selected fits and failed fits: NOT YET APPROVED
- Evidence required to establish null adequacy: NOT YET APPROVED

The existing AR(p) family must not be declared adequate solely because its order range is expanded or its boundary-saturation rate decreases.

Any alternative family must be justified by its assumptions and suitability for the scientific question, not by whether it weakens or removes the observed result.

3.3 Calibration plan

Before confirmatory execution, specify:

1. The data-generating processes used for calibration and why they represent relevant failure modes.
2. The number of simulated datasets and the random-seed policy.
3. The complete Type-I error acceptance rule and its operating characteristics.
4. The handling of multiple scenarios and the interpretation of scenario-level failures.
5. The minimum valid simulation count and the handling of failed or invalid fits.
6. The calibration of power under explicitly specified alternatives.
7. The independent checks that will verify implementation correctness.

The current acceptance rule must not be weakened retrospectively to turn existing failed scenarios into passes.

3.4 Replication design

At least two independent secondary real-world domains remain required by the current scientific contract.

For each proposed domain, document:

- Original source and retrieval method.
- Raw-file identity and checksum.
- Timestamp, cadence, gap, and missing-data handling where applicable.
- Measurement and estimator eligibility.
- Independence from the primary domain and from other proposed replication domains.
- Potential shared nuisance structure.
- Use of the same endpoint, approved null family, and alternative direction.
- The predeclared domain-level decision rule.

Measurement validity, source integrity, and computational reproducibility do not by themselves establish scientific replication.

No domain may be approved solely to satisfy the required count.

3.5 Prospective decision rule

The protocol must specify before the confirmatory run:

- The exact primary test and tail.
- The significance threshold.
- The minimum valid surrogate count.
- The rule for invalid fits and missing results.
- The handling of model-capacity warnings.
- The required internal-consistency and estimator-sensitivity checks.
- The required independent replication outcomes.
- The conditions under which the claim remains under investigation.
- The conditions under which the result is inconclusive or the protocol fails validation.

No post-observation adjustment may be represented as preregistered evidence.

---

4. Required Independent Review

The proposed protocol requires review by a qualified researcher who can assess the time-series assumptions, null adequacy, calibration design, and replication independence.

The review record must identify:

- Reviewer role and relevant expertise.
- The exact protocol revision reviewed.
- Substantive objections and their resolution.
- Remaining limitations.
- Whether the reviewer recommends approval, revision, or rejection.

Until such review is documented, the protocol remains a draft. This document does not claim that independent review has already occurred.

---

5. Versioning and Change Control

The approved protocol, if one is eventually produced, must have:

- A unique version identifier.
- A complete specification of data eligibility and preprocessing.
- Immutable references to the relevant source data and code revision.
- A recorded rationale for each protocol choice.
- A documented validation and calibration plan.
- A dated approval record created before the new confirmatory outcomes are inspected.

The current dataset and previously observed outcomes cannot be retroactively converted into a preregistered confirmation by writing a new protocol after the fact.

A materially changed null family or endpoint requires fresh validation and a clearly identified new analysis.

---

6. Explicit Non-Actions

This design record does not authorize:

- Changing the production claim-support flag.
- Changing claim-promotion authority.
- Weakening Type-I error thresholds.
- Expanding the AR order range without justification and calibration.
- Replacing the primary stochastic null with a permutation diagnostic.
- Treating synthetic controls as real-domain replication.
- Reusing historical outcomes as fresh confirmatory evidence.
- Treating a successful workflow run as proof of the scientific hypothesis.

---

7. Exit Criteria for Protocol Design

Protocol design may be considered ready for independent review only when the scientific question, null assumptions, model-capacity policy, calibration plan, replication criteria, failure conditions, and change-control rules are fully specified.

Confirmatory execution remains unauthorized until the protocol has been independently reviewed, frozen prospectively, and linked to a fresh validation plan.

---

8. Current Decision

Decision: CONTINUE PROTOCOL DESIGN; HOLD CONFIRMATORY PROMOTION.

The immediate objective is to resolve the scientific and statistical design questions transparently, not to obtain a passing workflow status.

The current hypothesis remains under investigation. No conclusion about HCM causation, mechanism, or universality follows from the present spectral results.

This document is a governance and planning artifact only. It does not modify the scientific contract or grant claim-promotion authority.
