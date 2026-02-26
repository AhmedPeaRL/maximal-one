# Seed Extremality Conjecture

Let S_N be the deterministic kernel state defined in theorem_core.tex.

We define:

    V_N(seed) = empirical variance of S_N under fixed seed.

Conjecture:
There exists a seed σ* such that:

    limsup_{N→∞} N * V_N(σ*) = C

and for all other seeds σ ≠ σ*:

    limsup_{N→∞} N * V_N(σ) < C

This is currently an open conjecture.

The workflow does NOT assume this statement.
It is numerically explored but not analytically proven.
