# Deterministic Kernel Formal Definition

The Python implementation in:

repro-core/deterministic_kernel.py

must implement a bounded function:

    f : ℕ → ℝ

such that:

    |f(k)| ≤ M

This boundedness condition is REQUIRED 
for the variance bound theorem to hold.

Any future modification that violates boundedness 
invalidates the analytical proof.

This document is the formal binding layer 
between code and theorem.
