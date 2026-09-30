![Power Test](https://img.shields.io/badge/power-unknown-lightgrey)
![Multi Seed Sweep](https://github.com/AhmedPeaRL/maximal-one/actions/workflows/multi-seed-sweep.yml/badge.svg)

# maximal-one

"maximal-one" is a reproducible computational research framework for
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

The current canonical result remains:

UNDER INVESTIGATION

The primary real dataset is:

"real-data/sunspots_full.csv"

with:

"N = 3328"

The canonical Welch spectral exponent is approximately:

"alpha = 2.525347"

The authoritative primary stochastic null is a stationary Gaussian AR(p)
surrogate family with AIC order selection over orders 1 through 20.

The current primary Monte Carlo result is:

"p = 0.999001"

Therefore the primary stochastic null is not rejected.

Scientific claim promotion is consequently blocked.

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

"p = 0.0002"

is diagnostic-only and does not replace the primary stochastic-null result.

---

## Null Calibration Status

The current primary AR surrogate analysis reports a high boundary-selection
fraction:

"0.965"

This indicates that the declared finite AR order range requires additional
calibration before stronger model-adequacy conclusions are drawn.

The calibration warning is not interpreted as evidence for the hypothesis.

---

## Independent Replication

Two independent real domains currently have valid measurements.

However, measurement validity is not replication.

The authoritative replication gate requires independent domain-level rejection
of the same primary stochastic null under the same endpoint, direction, tail,
and null family.

The current replication result is:

"0 / 2"

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

UNDER INVESTIGATION

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

## Experimental Assault Layer

The repository now includes:

- Multi-seed sweep experiment (50 seeds)
- Public CSV dataset export
- Statistical power analysis against α = 1/2
- Replication assault stress test

All outputs are stored in:

    /data/

All experiments are under:

    /experiments/

---

## Baseline Comparison

All spectral results are compared against:

- White noise (α ≈ 0.5)
- Fractional Brownian Motion (H = 0.5–0.9)
- AR(1) processes

This ensures deviations are not misinterpreted as structure.

---

## Power Test Result

Latest statistical test output is stored under:

    data/power_result.txt

---

## Current Status

This repository does not claim evidence of consciousness.

Current validated result:

- Reproducible spectral persistence
- Cross-method agreement
- Cross-seed stability
- Deterministic replay

Open questions:

- Statistical significance remains weak
- Independent third-party reproduction required
- Additional datasets required

---

## Current Scientific Status

The current implementation does not establish the
Constrained Spectral Persistence Hypothesis.

The canonical primary dataset produces a spectral
exponent of approximately 2.525 under the declared
Welch estimator.

A permutation null is rejected, but permutation-null
separation is explicitly diagnostic and is not the
authoritative scientific endpoint.

The declared primary stochastic short-memory null
is not rejected. The current Monte Carlo p-value is
approximately 0.999.

In addition, the AR-order selection procedure reaches
the declared maximum order, indicating that the current
finite-order stochastic-null specification requires
further calibration.

Therefore the scientific claim remains:

UNDER INVESTIGATION.

Clean-checkout computational reproducibility has been
demonstrated for the declared computational pipeline.
This is not independent scientific replication,
independent laboratory replication, or causal evidence.

No current result establishes HCM causation,
consciousness, universality, predictive market advantage,
or mechanism.

---

## Research Position

See: core-scientific/research_position.md

---

## External Reproducibility (Critical Requirement)

This system is NOT considered scientifically valid until:

- Reproduced independently
- Verified outside original environment
- Confirmed by external observers

See:

/external/REPRODUCE.md

---

## Execution

```bash
pip install -r requirements.txt
python master_experiment.py

All outputs are deterministic under controlled seeds and constrained environments, subject to reproducibility limits of underlying infrastructure.
