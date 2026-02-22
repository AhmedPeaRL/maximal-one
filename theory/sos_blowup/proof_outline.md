# Proof Outline (Strictly Classical Foundations)

## Step 1 — Archimedean Compactness

Assume:

    N - ∑ x_i² ∈ M.

Then S is compact.

This is standard in real algebraic geometry.

---

## Step 2 — Strict Positivity

Assume:

    f > 0 on S.

Apply Putinar’s Positivstellensatz:

    f ∈ M.

No modification or extension is claimed beyond the classical theorem.

---

## Step 3 — Local Blow-up Expansion

Assume:

    f ∈ C²
    f(x₀) = 0
    ∇f(x₀) = 0
    D²f(x₀) positive definite

Then by Taylor expansion:

    f(x) = ½ (x - x₀)^T D²f(x₀) (x - x₀) + o(‖x - x₀‖²)

Hence:

    f(x) ≥ c ‖x - x₀‖²  locally

for some c > 0.

This establishes quadratic blow-up behavior.

---

## Step 4 — Functional Construction (Explicit)

Define the evaluation functional:

    L_p : R → ℝ
    L_p(f) = f(p)

This is linear.

For SOS polynomials:

    L_p(σ²) ≥ 0.

Hence L_p is positive on Σ.

No non-classical extension of moment duality is claimed.

---

## Asymptotics

Under (B1–B3):

    f(x) ~ Q₂(x - x₀)

Quadratic growth rate.

No higher-order uniform bounds are claimed.

---

## Gaps Explicitly Closed

• Compactness derived from Archimedean assumption.
• Local asymptotics derived from Taylor theorem.
• SOS representation derived from classical Putinar theorem.

No new theorem is claimed beyond these.
