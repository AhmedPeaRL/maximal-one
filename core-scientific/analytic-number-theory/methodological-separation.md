# Methodological Separation: Proof vs Computation

## 1. Theoretical Layer

The inequality:

    τ(n) ≤ 2√n

is established via a purely combinatorial argument
(divisor pairing).

This layer:

- does not use floating point arithmetic
- does not depend on finite truncation
- does not require asymptotic estimation
- holds for all n ∈ ℕ

---

## 2. Computational Layer

The scripts:

    divisor_asymptotic_study.py
    asymptotic_statistical_analysis.py

investigate empirical properties such as:

- decay rate of τ(n)/(2√n)
- stabilization of running supremum
- monotonic smoothing behaviour

These are observational studies,
not logical proofs.

---

## 3. Why Keep Both?

Theoretical results guarantee correctness.

Computational experiments explore structure.

They answer different questions.

Conflating them would be a category error.

---

## 4. Research Direction

Interesting open directions include:

- extremal growth of τ(n)
- structure of highly composite numbers
- refined upper bounds
- connections to Robin-type inequalities

These require analytic number theory,
not finite sampling.
