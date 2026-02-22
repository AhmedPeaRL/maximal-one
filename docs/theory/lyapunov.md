# Discrete-Time Lyapunov Stability Assumptions

We assume:

1. A ∈ R^{n×n}
2. Spectral radius ρ(A) < 1
3. Q ≻ 0

Then there exists unique P ≻ 0 solving:

Aᵀ P A − P = −Q

We numerically verify:

V(x_{k+1}) − V(x_k) ≤ −α ||x||²

with α = λ_min(Q).
