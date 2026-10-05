![Scientific Claim Promotion Gate](https://github.com/AhmedPeaRL/maximal-one/actions/workflows/scientific-claim-promotion.yml/badge.svg)

# maximal-one

`"maximal-one"` is a reproducible computational research framework for
investigating the Constrained Spectral Persistence Hypothesis.

The current hypothesis asks whether a spectral persistence signature can
remain distinguishable from an appropriately specified stochastic null model
under a declared validation protocol.

The repository is explicitly falsification-oriented.

A scientific claim is not promoted because a spectral pattern is visually
interesting, because a diagnostic statistic is significant, or because
multiple internal checks agree.

---

## Current Scientific Position

The repository remains UNDER INVESTIGATION.

- The primary real dataset is:

`real-data/sunspots_full.csv`

with:

`N = 3328`

- The canonical Welch spectral exponent historically measured
for the primary dataset was approximately:

`alpha = 2.525347`

- The historical pre-repair primary stochastic-null analysis reported:

`p = 0.999001`.

This value is retained only for provenance.

It is not a current confirmatory result and must not be used for
scientific claim promotion.

The repaired protocol requires a fresh primary reanalysis before a
new p-value can acquire confirmatory status.

- The AR order-comparison protocol was subsequently repaired
under:

`ar_order_comparison_holdback_v1`

using a fixed:

`hold_back = 20`

for all candidate AR orders.

- The post-observation repair is explicitly non-preregistered
and therefore does not constitute confirmatory evidence.

- A fresh primary reanalysis and fresh null calibration are
required before any scientific interpretation of the repaired
procedure.

- The scientific claim remains blocked.

- No historical pre-repair p-value may be used to promote the claim.

---

## Diagnostic Versus Inferential Evidence

The repository contains several secondary diagnostics.

These include:

- permutation-null analysis
- scale analysis
- perturbation stability
- cross-method comparison
- separation diagnostics
- predictive diagnostics
- adversarial controls

These diagnostics are deliberately separated from scientific claim
authority.

In particular, the current permutation result:

`"p = 0.0002"`

is diagnostic-only and does not replace the primary stochastic-null result.


### Why two different p-values appear

- The repository reports two statistically distinct null procedures.

- The permutation-null result `(p ≈ 0.0002)` is diagnostic only. It tests
exchangeability of temporal ordering and is not the authoritative
scientific endpoint.

- The primary scientific endpoint uses the declared fitted stationary
Gaussian AR(p) null with AIC order selection and surrogate refitting.
The historical pre-repair primary stochastic-null analysis
reported `p = 0.999001`.

This value is historical, non-confirmatory, and must not be
used as the current primary-null decision.

- These values are therefore not contradictory: they answer different
null-model questions. The primary stochastic null controls scientific
claim support; the permutation result remains diagnostic only.

---

## Null Calibration Status

The AR order-selection procedure is under active model-capacity
review.

The historical pre-repair boundary-selection result is
superseded and must not be reused as confirmatory evidence.

The repository now uses the declared repair:

`ar_order_comparison_holdback_v1`

with:

`hold_back = 20`

for candidate-order comparison.

The calibration audit of known stationary AR processes is
diagnostic-only. Passing those calibration cases does not by
itself establish that the fitted primary sunspot null is
adequate.

The primary sunspot null therefore remains subject to a separate
fresh capacity audit.

No capacity diagnostic is permitted to establish or falsify
the scientific hypothesis by itself.

---

## Independent Replication

Two independent real domains currently have valid measurements.

However, measurement validity is not replication.

The authoritative replication gate requires independent domain-level rejection
of the same primary stochastic null under the same endpoint, direction, tail,
and null family.

The current replication result is:

`"0 / 2"`

Therefore independent scientific replication is not established.

---

## Computational Reproducibility

The repository currently supports clean-checkout computational reproduction
with matching report structure and fingerprint under the declared environment.

This does not constitute:

- independent scientific replication
- independent implementation replication
- laboratory replication
- causal evidence
- mechanism
- universality

---

## Epistemic Boundary

The repository does not currently establish:

- consciousness
- HCM causation
- NeuroEnergetic Field existence
- universal law
- novel physics
- causal mechanism
- universal applicability
- market advantage

These remain hypotheses requiring independent empirical testing.

---

## Core Principle

- Reproducibility > interpretation
- Data > narrative
- Falsifiability > desire
- Negative results remain valid results
- Diagnostic evidence must never silently become claim evidence

The system is designed to preserve the possibility that the hypothesis is
wrong.

---

## External Reproduction

The project should be considered scientifically incomplete until independent
researchers can reproduce or falsify the relevant result outside the original
execution environment.

External reproduction is therefore a research objective, not a promotional
badge.

---

## Scientific Status

`UNDER INVESTIGATION`

No current workflow should promote the hypothesis while the authoritative
primary stochastic-null gate remains un-rejected.

---

## Formal Layer

The formal hypothesis, theorem structure,
boundary conditions, and falsifiability framework
are defined under:

    /formal/

This separates experimental computation
from formal scientific claim structure.

---

## Baseline Comparison

All spectral results are compared against:

- White noise `(α ≈ 0.5)`
- Fractional Brownian Motion `(H = 0.5–0.9)`
- AR(1) processes

This ensures deviations are not misinterpreted as structure.

---

## Power Analysis

No current power value is presented as evidence for the scientific
claim.

Future power analysis must be tied to the final prospectively declared
primary endpoint, null family, effect definition, sample structure, and
`type-I-error` procedure.

A power calculation against an unrelated diagnostic null must not be
used as a substitute for calibration of the primary stochastic null.

---

## Current Status

This repository does not claim evidence of consciousness.

The current canonical measurement is:

- Welch spectral exponent: approximately `2.525347`
- The historical pre-repair primary stochastic-null analysis
reported `p = 0.999001`.

This value is historical, non-confirmatory, and must not be
used as the current primary-null decision.

- Independent scientific replication: not established
- Clean-checkout computational reproducibility: distinct from scientific replication

The current result is therefore:

`UNDER INVESTIGATION`

Secondary diagnostics must not be promoted to primary scientific evidence.

---

## Current Scientific Status

- The current implementation does not establish the
Constrained Spectral Persistence Hypothesis.

- The canonical primary dataset produces a spectral
exponent of approximately `2.525` under the declared
Welch estimator.

- A permutation null is rejected, but permutation-null
separation is explicitly diagnostic and is not the
authoritative scientific endpoint.

- The current repaired implementation has not yet produced
a valid fresh confirmatory decision for the primary stochastic
short-memory null.

The historical pre-repair result is retained only for provenance
and is not treated as current inferential evidence.

Therefore the scientific claim remains blocked.

- In addition, the AR-order selection procedure reaches
the declared maximum order, indicating that the current
finite-order stochastic-null specification requires
further calibration.

- Therefore the scientific claim remains:

`UNDER INVESTIGATION`.

- Clean-checkout computational reproducibility has been
demonstrated for the declared computational pipeline.
This is not independent scientific replication,
independent laboratory replication, or causal evidence.

- No current result establishes HCM causation,
consciousness, universality, predictive market advantage,
or mechanism.

---

## Research Position

See: `core-scientific/research_position.md`

---

## External Reproducibility (Critical Requirement)

This system is NOT considered scientifically valid until:

- Reproduced independently
- Verified outside original environment
- Confirmed by external observers

See:

`/external/REPRODUCE.md`

---

## Execution

The canonical scientific pipeline must be run through the declared
canonical-report workflow, not through the legacy `master_experiment.py`
script.

The resulting report is subject to the repository's scientific gates, including:

- JSON integrity validation
- canonical report identity and consistency checks
- estimator sensitivity validation
- primary stochastic-null testing
- dataset eligibility validation
- independent-domain replication requirements
- adversarial controls
- clean-checkout computational reproducibility checks

master_experiment.py is retained as legacy experimental code and is not the authoritative scientific execution path.

No output from the legacy experiment should be interpreted as evidence for the current scientific claim.

For the canonical primary report:

```bash
python scripts/prepare_canonical_inputs.py
python scripts/generate_report.py --seed 42 --canonical
