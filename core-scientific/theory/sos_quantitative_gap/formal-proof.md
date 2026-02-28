# Formal Proof

Step 1. (Dual SDP Formulation)

SOS membership is equivalent to feasibility of:

p(x) = v_d(x)^T Q v_d(x),   Q ⪰ 0

Dual problem:

Find y such that:

M_d(y) ⪰ 0
L_y(p) < 0

Step 2. (Separation)

If such y exists, strong duality implies:

p ∉ Σ_d

Step 3. (Quantitative Bound)

Construct y_n such that:

L_{y_n}(p_n) ≤ −γ(n)

Hence for all d < C·g(n):

p_n ∉ Σ_d

Thus:

d_min(p_n) ≥ C·g(n)

□
