# Kernel Derivation Roadmap
## Toward Analytical Derivation of α*

### Premise

The spectral exponent α* ≈ 1.8 appears stable under large seed ensembles.
However, empirical stability alone is insufficient for theoretical breakthrough.

The objective of this roadmap is to derive α* analytically from the kernel
structure rather than estimate it numerically.

---

## Phase I — Kernel Formalization

Let K(θ) define the deterministic bounded feedback operator:

X_{t+1} = F(X_t, θ) + ε_t

We must explicitly:

1. Define F symbolically.
2. Prove boundedness.
3. Prove contractive expectation.
4. Characterize memory depth M.

Deliverable:
A symbolic expression of the operator spectrum.

---

## Phase II — Linearization & Spectral Approximation

Linearize around equilibrium:

X_{t+1} ≈ J X_t + ε_t

Where J is the Jacobian of F.

Tasks:
- Compute eigenvalues of J.
- Determine if spectral density follows S(f) ~ f^(-α).
- Derive α from eigen-structure analytically.

---

## Phase III — AR-Reduction Impossibility Proof

We must prove that no finite-order AR(p) model can
replicate the observed α* under identical constraints.

Deliverables:
- Fit AR(p) family for p ∈ [1,20]
- Show BIC dominance fails asymptotically
- Provide divergence bound

---

## Phase IV — Structural Perturbation

Perturb θ infinitesimally:

θ → θ + δ

If α* shifts smoothly, we derive:

dα/dθ

If α* remains invariant, we prove kernel universality.

---

## Explicit Success Criterion

This roadmap succeeds only if:

α* is derived analytically from kernel structure
AND
AR(p) reducibility is disproven
AND
result holds across bounded perturbations

---

Empirical stability is necessary but never sufficient.
Analytical inevitability is the only path to breakthrough.
