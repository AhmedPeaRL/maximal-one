# Null Nuisance Preservation Matrix

## Scientific role

This document defines the structure that a future primary stochastic
null must preserve or explicitly account for before confirmatory use.

It is a methodological adequacy rule.

It is not claim-supporting evidence.

---

## Current primary-domain warning

The primary dataset is a temporal solar-activity series.

The declared canonical spectral band is:

`0.01-0.05 cycles per month`.

A reference approximately decadal component may occur below the
lower canonical boundary, while harmonics of that component may enter
the canonical band.

Therefore, exclusion of the fundamental frequency alone is not
sufficient to establish nuisance separation.

---

## Required nuisance dimensions

Before confirmatory null freezing, the candidate null assessment MUST
state how it treats:

1. low-frequency persistence;
2. autocorrelation;
3. partial autocorrelation;
4. known approximately decadal periodic structure;
5. harmonics of known periodic structure;
6. spectral leakage;
7. finite-sample frequency resolution;
8. detrending effects;
9. temporal aggregation;
10. effective sample size;
11. residual temporal dependence.

---

## Preservation principle

The null must preserve temporal structure that is considered nuisance
under the hypothesis.

The null must not automatically preserve the hypothesized effect itself.

The distinction between nuisance structure and hypothesized structure
must be specified before confirmatory inference.

---

## Prohibited procedure

The project MUST NOT:

- choose nuisance components because they increase the p-value;
- remove periodic components because they reduce apparent evidence;
- retain periodic components because they increase apparent evidence;
- change the frequency band after inspecting the endpoint;
- choose a null family after inspecting the confirmatory endpoint.

---

## Candidate adequacy

For every candidate null family, the repository must record:

- fitted parameters;
- admissibility constraints;
- residual autocorrelation;
- residual partial autocorrelation;
- residual whiteness diagnostics;
- effective observations;
- boundary saturation;
- periodic-component treatment;
- surrogate validity rate;
- finite-sample calibration.

---

## Decision separation

Null adequacy is a model-validation problem.

Scientific endpoint rejection is an inferential problem.

They MUST remain separate.

A model is not adequate because it gives a favorable p-value.

A model is not inadequate because it gives an unfavorable p-value.

---

## Freeze rule

After the candidate family and nuisance-treatment rule are selected
according to the declared adequacy criteria, the complete protocol MUST
be frozen before confirmatory data are analyzed.

Any later amendment is exploratory.

---

## HCM boundary

This document makes no inference about:

- HCM causation;
- consciousness;
- NEF;
- new physics;
- universality;
- mechanism.

It is strictly a statistical validation protocol.
