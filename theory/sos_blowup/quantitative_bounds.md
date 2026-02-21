# Quantitative Degree Growth under Leading Form Degeneracy

## 1. Preliminaries

Let K ⊂ R^n compact.
Let M be an Archimedean quadratic module.

For p ∈ R[x] positive on K,
Putinar's Positivstellensatz ensures existence of SOS representation.

Define:

    deg_min(p)
        = minimal r such that p ∈ M_r

where M_r denotes truncated module degree ≤ 2r.

---

2. Known Upper Bound (Nie–Schweighofer 2007)

Theorem (Nie–Schweighofer).

There exist constants C₁, C₂, α > 0
depending only on dimension and defining polynomials,
such that if:

    m := min_K p > 0,

then

    deg_min(p)
        ≤ C₁ exp( C₂ (‖p‖ / m)^α ).

Citation:
J. Nie and M. Schweighofer,
On the complexity of Putinar’s Positivstellensatz,
Journal of Complexity 23 (2007), 135–150.

---

## 3. Degenerate Family

```markdown
Consider:

    p_ε(x,y)
        = x^4 y^2 + y^4 x^2
          + ε (x^6 + y^6)
          + 1.

Properties:

1) p_ε > 0 for ε > 0.
2) Leading form at ε=0:
       L(x,y)=x^4 y^2 + y^4 x^2
   is positive semidefinite
   but vanishes on axes.
3) Minimal value m_ε → 0
   as ε → 0.

Proof of (3):
Evaluate along axis y=0:
p_ε(x,0)
    = ε x^6 + 1
On sphere x^2+y^2=1, choose y small, gives collapse m_ε ≈ ε.

---

## 4. Blow-up Theorem (Non-Quantitative)

```markdown
Theorem.

Let n ≥ 2.
Let p_ε be as above.

Then:

    deg_min(p_ε) → ∞
    as ε → 0.

Proof:
Fix r. Cone Σ_{2r} is closed in finite dimension. 
If deg_min bounded, limit ε→0 would imply p_0 ∈ Σ_{2r}. 

But p_0 not strictly positive and lies outside interior of SOS cone.
Hence contradiction by compactness.

Therefore for each r exists ε small with p_ε ∉ Σ_{2r}.


