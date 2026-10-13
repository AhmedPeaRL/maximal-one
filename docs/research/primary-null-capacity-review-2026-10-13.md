# Primary Null Capacity Review — 2026-10-13

1. Purpose

This record documents the current primary stochastic-null capacity warning and defines the conditions required before any future confirmatory null-protocol change.

This is a research-governance record. It does not modify scientific inputs, estimator settings, null-model settings, acceptance thresholds, or claim-promotion authority.

---

2. Verified Workflow Context

- Workflow: ".github/workflows/scientific-claim-promotion.yml"
- Verified workflow commit: "6f3430ce9368b956d0c2e35dff1f7bd9c9885ff7"
- Scientific status: "UNDER_INVESTIGATION"
- Scientific claim supported: "false"
- Primary stochastic null rejected: "false"
- Primary stochastic-null p-value: "0.999001"
- Clean-checkout reproducibility verified: "true"
- Adversarial control passed: "true"
- Final promotion allowed: "false"

These execution and governance results do not establish scientific support for the HCM hypothesis.

---

3. Observed Null-Capacity Warning

The primary null-capacity audit reports:

- Primary dataset: "real-data/sunspots_full.csv"
- Sample size: "3328"
- Declared maximum AR order: "20"
- Observed selected order: "20"
- Surrogate refits requested: "1000"
- Valid surrogate refits: "1000"
- Surrogate refits selecting order 20: "937"
- Primary-audit boundary fraction: "0.937"
- Boundary-warning threshold: "0.5"
- Review triggered: "true"
- Preregistered confirmation: "false"

The canonical null-calibration gate separately reports a boundary fraction of "0.947". The reconciliation artifact identifies these as source-scoped estimates from different random streams/seeds. They must remain separately recorded rather than being forced to match.

A diagnostic AR-order scan extending through order 40 reports:

- Best AIC order: "40"
- Scan maximum order: "40"
- Best AIC at scan boundary: "true"
- Scientific role: "diagnostic_only"
- Not the primary null protocol: "true"

The extended diagnostic scan is a capacity warning. It does not authorize replacing the declared maximum order of 20 with 40, nor does it establish that order 40 is an adequate null model.

---

4. Interpretation and Limits

The current evidence indicates that the declared finite-order AR(p) null requires further calibration before stronger confirmatory inference.

The boundary warning does not, by itself:

- support or falsify the HCM hypothesis;
- establish that the observed spectral exponent is scientifically exceptional;
- establish a causal mechanism or universality;
- justify changing the primary endpoint or frequency band;
- justify changing the maximum AR order after observing the results;
- convert permutation diagnostics into a replacement for the primary temporal stochastic null;
- establish independent real-domain replication.

The primary stochastic null has not been rejected under the currently reported test.

---

5. Estimator-Sensitivity Constraint

The estimator-sensitivity audit reports materially different alpha estimates across alternative segmentation and frequency-band configurations.

The canonical configuration remains:

- "nperseg = 1024"
- frequency band: "0.01" to "0.05"
- minimum frequency bins: "20"

Alternative configurations remain diagnostic-only. No configuration may be selected for confirmatory use merely because it produces a more favorable result after inspection.

Any future confirmatory estimator or frequency-band change requires a separately versioned prospective protocol and independent justification.

---

6. Required Review Before a New Confirmatory Run

Before a new confirmatory analysis is authorized, the research record must specify and justify:

1. The scientific question and primary endpoint.
2. The complete null family, including its assumptions and limitations.
3. The model-selection rule and permissible model capacity.
4. The treatment of boundary-selected models and failed or nonstationary fits.
5. The simulation and calibration design, including known-process tests.
6. The type-I error acceptance criteria and their operating characteristics.
7. The number of simulations, random-seed policy, and reproducibility requirements.
8. The handling of temporal dependence, periodicity, gaps, and nuisance structure.
9. The prospective decision rule, including failure conditions.
10. The protocol version and immutable record created before confirmatory outcomes are inspected.

A larger model-order range is not automatically a solution. The adequacy of any proposed null family must be justified and calibrated rather than inferred from a better fit alone.

---

7. Independent Replication Gate

The current workflow reports "0/2" eligible independent replication domains.

The existing candidates remain unapproved for scientific replication for the recorded reasons:

- HadCET and FRED INDPRO: source metadata and data integrity have been reconciled, but source independence and confirmatory null adequacy remain pending.
- CO2: 816 observations, below the declared replication minimum of 1024.
- Cosmic rays: timestamp continuity fails; the longest hourly contiguous run is 486, below 1024, and provenance and shared-nuisance review remain pending.
- Short passenger, temperature, and S&P 500 series: fail the declared structural length requirements.
- The primary sunspot series and its derived extension do not count as independent secondary replication domains.

Measurement validity and computational reproducibility must not be represented as scientific replication.

---

8. Change-Control Rules

Until the prospective review is complete:

- Preserve the current primary endpoint and declared settings.
- Do not edit scientific outputs to make the workflow pass.
- Do not weaken or retrospectively alter the type-I acceptance rule.
- Do not promote diagnostic results to confirmatory evidence.
- Do not approve a candidate domain merely to satisfy the two-domain requirement.
- Keep claim support and promotion authority false.
- Retain the existing failing gate as an explicit record of unresolved requirements.

Any future protocol change must be versioned, justified, tested, and recorded separately before it is used for confirmatory inference.

---

9. Current Decision

Decision: HOLD CONFIRMATORY PROMOTION.

The current implementation has demonstrated reported computational reproducibility and a passing adversarial control, but the primary stochastic null remains unrejected, null calibration remains unresolved, and independent scientific replication has not been established.

The next research action is a prospective null-protocol design and review. It is not a post-hoc parameter change or a claim-promotion attempt.

---

10. Authority

This document is a diagnostic and governance record only.

It does not change the scientific contract, claim-support state, replication eligibility, or promotion authority.
