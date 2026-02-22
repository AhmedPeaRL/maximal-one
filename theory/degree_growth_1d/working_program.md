# Working Program: 1D SOS Degree Growth

## Setting

K = ℝ  
S = { x ∈ ℝ | 1 - x² ≥ 0 } = [-1,1]

f_k(x) = (1 - x²)^k + ε

ε > 0 fixed small.

---

## Known (Classical)

Any polynomial strictly positive on [-1,1]
admits representation:

f = σ₀ + σ₁ (1 - x²)

σ_i sums of squares.

Existence is not in question.

---

## Problem

Determine asymptotic growth of minimal degree of σ₀, σ₁
as k → ∞.

---

## Numerical Goal

Compute:

d(k) = minimal SOS degree

Test scaling law:

Is d(k) ~ Ck ?
Is d(k) bounded?
Is d(k) superlinear?

---

## Theoretical Direction

Lower bound approach:

1. Analyze vanishing multiplicity at boundary x = ±1.
2. Study derivative constraints.
3. Use Gram matrix rank constraints.

Upper bound approach:

Construct explicit SOS candidate.
