# Divisor Function Upper Bound – Formal Theoretical Development

## Notation

Let n ∈ ℕ, n ≥ 1.

Define:

    τ(n) := |{ d ∈ ℕ : d | n }|

the number of positive divisors of n.

Let √n denote the positive real square root of n.

---

# Lemma 1 (Divisor Pairing Lemma)

Let n ∈ ℕ, n ≥ 1.
If d divides n, then n/d also divides n.

Moreover, the mapping:

    d ↦ n/d

is an involution on the set of positive divisors of n.

## Proof

If d | n, then ∃ k ∈ ℕ such that:

    n = d k

Thus:

    k = n/d

Hence n/d is a positive divisor of n.

Further:

    n / (n/d) = d

so the map is its own inverse.

∎

---

# Lemma 2 (Square Root Separation)

Let n ∈ ℕ, n ≥ 1.
If d is a positive divisor of n and d < √n,
then:

    n/d > √n.

If n is not a perfect square, no divisor equals √n.

If n is a perfect square, √n is the unique fixed point
of the involution d ↦ n/d.

## Proof

If d < √n, then:

    d² < n

Dividing both sides by d:

    d < n/d

Thus:

    n/d > √n

The fixed point condition:

    d = n/d  ⇒  d² = n  ⇒  d = √n

This occurs only if n is a perfect square.

∎

---

# Proposition 1 (Upper Bound via Pairing)

Let n ∈ ℕ, n ≥ 1.

Then the number of divisors of n satisfies:

    τ(n) ≤ 2 ⌊√n⌋

## Proof

By Lemma 1, divisors are partitioned into pairs:

    (d, n/d)

By Lemma 2, for each divisor d ≤ √n,
there is at most one complementary divisor ≥ √n.

The number of integers ≤ √n is ⌊√n⌋.

Thus the number of divisors ≤ √n
is at most ⌊√n⌋.

Each produces at most one complementary divisor.

Hence:

    τ(n) ≤ 2 ⌊√n⌋

If n is a perfect square,
√n contributes only once,
so the inequality still holds.

∎

---

# Theorem (Classical Divisor Upper Bound)

For all natural numbers n ≥ 1:

    τ(n) ≤ 2√n

## Proof

From Proposition 1:

    τ(n) ≤ 2 ⌊√n⌋

Since:

    ⌊√n⌋ ≤ √n

we obtain:

    τ(n) ≤ 2√n

This proof does not rely on finite sampling,
asymptotic estimates,
statistical regression,
or numerical experimentation.

It is purely combinatorial and holds for all n ∈ ℕ.

∎

---

# Remark on Sharpness

The bound 2√n is not asymptotically sharp.

In fact, much stronger bounds are known:

    τ(n) = o(n^ε)  for every ε > 0

The maximal order of τ(n) is substantially smaller
than √n for large n.

The present theorem establishes only a universal elementary bound.

---

# Separation of Concerns

The numerical modules in this repository:

    stability/divisor_asymptotic_study.py
    stability/asymptotic_statistical_analysis.py

do NOT attempt to prove this theorem.

They study finite-sample behaviour of:

    τ(n) / (2√n)

over bounded ranges of n.

The theoretical validity of the inequality
does not depend on those computations.
