# Blow-up of Putinar Degree via Geometric Separation

## 1. Setting

Let R[x,y] be the polynomial ring.
Let Σ_{2r} denote the cone of sums of squares of degree ≤ 2r.

Let K ⊂ R^2 be compact and Archimedean.
Consider strictly positive polynomials p_ε on K.

Define:

    m_ε := min_{x∈K} p_ε(x)

Assume:

(1) p_ε > 0 on K
(2) leading homogeneous form L is positive semidefinite
(3) L is NOT positive definite

We study the minimal r such that p_ε ∈ Σ_{2r}(K).

---

Section 2 — One-dimensional case

## Theorem (Univariate Case)

If p ∈ R[x] and p(x) > 0 for all x ∈ R,
then p is a sum of two squares in R[x].

Hence any positive polynomial admits an SOS representation
without unbounded degree growth.

Proof.

Factor p over C:

    p(x) = c ∏ (x - α_i)(x - \bar{α}_i)

Complex conjugate roots appear in pairs.
Each quadratic factor is positive definite.

Thus each quadratic is a sum of two squares.
Products of sums of squares remain sums of squares.

Therefore p is SOS.

Conclusion:
In dimension 1, no infinite blow-up can occur.

---

Section 3 — Truncated Cones

## Definition

Let V_r be the vector space of polynomials of degree ≤ 2r.

Define:

    C_r := Σ_{2r} ∩ V_r

This is a closed convex cone in finite dimension.

Let M_r denote its dual cone:

    M_r := { ℓ : V_r → R linear |
             ℓ(q) ≥ 0 for all q ∈ C_r }

---

Section 4 — Hahn–Banach Separation

## Proposition (Finite-dimensional separation)

Let C_r ⊂ V_r be a closed convex cone.
If p ∉ C_r,
then there exists a linear functional ℓ ∈ M_r
such that

    ℓ(p) < 0
and
    ℓ(q) ≥ 0 for all q ∈ C_r.

Proof:
Finite-dimensional convex separation theorem. 
No topological subtlety arises.

---

Section 5 — Degeneracy Construction

Assume leading form L vanishes on direction v.

Define approximate Dirac measures μ_t concentrating near v.

Define truncated moment functionals:

    ℓ_t(p) := ∫ p dμ_t

Then:

- ℓ_t(q) ≥ 0 for all SOS q
- ℓ_t(p_ε) ≈ m_ε along degeneracy direction

If m_ε collapses faster than certificate compensation, then for fixed r we can find ε small enough such that:
ℓ_t(p_ε) < 0
Hence p_ε ∉ C_r.

---

## Section 6 — Gap–Degree Lemma

## Lemma

There exists constant C > 0 such that

    deg_min(p_ε) ≥ C log(1 / m_ε)

for small m_ε.

Sketch.

Use quantitative Putinar bounds
(Nie–Schweighofer type estimates).

Degree depends logarithmically on inverse minimal value.

---

Section 7 — Blow-up Theorem

## Theorem

Assume:

(1) dimension ≥ 2
(2) leading form not positive definite
(3) m_ε → 0 as ε → 0

Then for every M ∈ N
there exists ε such that
any Putinar certificate requires degree ≥ M.

Proof:

Fix M. Let r=M.

For small ε, m_ε small enough that gap-degree lemma forces deg_min ≥ r.

Equivalently p_ε ∉ C_r.

By separation, exists ℓ ∈ M_r with ℓ(p_ε) < 0.

Hence blow-up.
