# SOS Degree Growth Experiment

## Objective

This experiment studies the relationship between:

    vanishing order at boundary
and
    minimal SOS degree required for representation.

We do NOT claim any theorem.

We perform numerical experiments only.

---

## Mathematical Setup

Let:

    K = ℝ
    S = { x ∈ ℝ | 1 - x² ≥ 0 }

This is the interval [-1,1].

Define polynomial family:

    f_k(x) = (1 - x²)^k + ε

where:
    k ∈ ℕ
    ε > 0 small (strict positivity enforcement)

We test:

What is the minimal SOS degree required to certify:

    f_k ∈ M

where:

    M = { σ₀ + σ₁ (1 - x²) }

σ_i ∈ Σ (SOS polynomials)

---

## Numerical Goal

For increasing k:

1. Attempt SOS decomposition
2. Record minimal feasible SOS degree
3. Measure scaling behaviour

---

## What This Is

• Empirical scaling study
• Numerical convex optimization experiment
• Exploratory computational algebra

---

## What This Is NOT

• Not a proof of degree bounds
• Not a general Positivstellensatz result
• Not a theoretical breakthrough claim

---

## Expected Output

A dataset:

    k vs minimal_degree

for further analysis.
