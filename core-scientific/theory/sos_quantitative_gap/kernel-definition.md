# Probabilistic Kernel Construction

Define perturbation:

ξ_n ~ N(0, σ_n^2 I)

Define random polynomial:

p_n^*(x) = p_n(x) + ξ_n(x)

Probability space:

Ω = coefficient space
F = Borel σ-algebra
P = Gaussian measure

Define estimator:

d̂_n = min { d : SDP_d(p_n^*) feasible }

Kernel:

K_n(d) = P(d̂_n ≤ d)

This induces a distribution over minimal SOS degrees.
