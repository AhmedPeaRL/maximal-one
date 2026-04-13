# Source Disentanglement Protocol

## Purpose

To determine whether observed spectral structure arises from:

1. Computational artifacts
2. Infrastructure-level determinism
3. Emergent constrained behavior

## Method

### Layer 1 — Synthetic Null Expansion

Inject controlled pseudo-random processes with identical execution constraints.

Compare spectral profile divergence.

---

### Layer 2 — Infrastructure Drift Injection

Run identical experiment across:

- Different CPU architectures
- Different cloud providers
- Local machine vs container

Measure stability of α.

---

### Layer 3 — Algorithmic Perturbation

Introduce minimal code perturbations:

- reorder loops
- change memory allocation patterns

Check spectral invariance.

---

## Decision Logic

If structure:

- survives all layers → non-trivial persistence
- collapses under perturbation → artifact origin

---

## Status

ACTIVE — required before any ontological escalation
