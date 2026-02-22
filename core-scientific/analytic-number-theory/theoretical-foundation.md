# Theoretical Foundation: Divisor Function Upper Bound

## Statement

For all natural numbers n ≥ 1:

    τ(n) ≤ 2√n

where τ(n) denotes the number of positive divisors of n.

---

## Proof (Elementary Pairing Argument)

Let d be a positive divisor of n.

Then there exists a complementary divisor:

    n / d

If d < √n, then n/d > √n.

Thus divisors occur in symmetric pairs around √n:

    (d, n/d)

The number of divisors less than or equal to √n is at most √n.

Each such divisor corresponds to at most one complementary divisor.

Therefore:

    τ(n) ≤ 2√n

If n is a perfect square, √n is counted only once,
so the inequality remains valid.

QED.

---

## Important Clarification

This result is classical and elementary.

The numerical experiments in this repository do NOT attempt
to prove this inequality.

They investigate the asymptotic behaviour of the ratio:

    τ(n) / (2√n)

for large finite N.

Numerical validation is not a substitute for proof.
