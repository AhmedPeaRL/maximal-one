![Power Test](https://img.shields.io/badge/power-unknown-lightgrey)
![Multi Seed Sweep](https://github.com/AhmedPeaRL/maximal-one/actions/workflows/multi-seed-sweep.yml/badge.svg)

# maximal-one

maximal-one is a reproducible experimental framework for testing the hypothesis:

> H0: Deterministic static cloud deployments exhibit no intrinsic periodic structure beyond known computational artifacts.

The system performs:

- Controlled metric acquisition
- Spectral analysis
- Statistical significance testing
- Cross-run reproducibility validation
- Artifact persistence for auditability

## Scientific Position

This system is considered incomplete until independently reproduced outside its original execution environment.

This repository does NOT assume emergent structure.

It attempts to falsify the null hypothesis using reproducible computation.

If no statistically significant structure survives artifact elimination,
the null hypothesis stands.

If structure persists across:

- device environments
- independent runs
- bootstrap randomization
- artifact removal controls

then further investigation is justified.

## No Ontological Claims

This repository does not claim:

- metaphysical emergence
- hidden universal structure
- fundamental reinterpretation of cloud systems

It only tests measurable statistical deviation from white noise.

## Core Principle

Reproducibility > Interpretation
Data > Narrative
Falsifiability > Desire

---

New Theorem – Finite Spectral Upper Bound

See core-scientific/finite_spectral_bound.md.

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

## Baseline Comparison

All spectral results are compared against:

- White noise (α ≈ 0.5)
- Fractional Brownian Motion (H = 0.5–0.9)
- AR(1) processes

This ensures deviations are not misinterpreted as structure.

## Power Test Result

Latest statistical test output is stored under:

    data/power_result.txt

## Research Position

See: core-scientific/research_position.md

## Execution

```bash
pip install -r requirements.txt
python master_experiment.py

All outputs are deterministic under controlled seeds and constrained environments, subject to reproducibility limits of underlying infrastructure.
