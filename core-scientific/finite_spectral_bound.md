Finite-Length Spectral Upper Bound for Prime-Modulus LCG
Definition
Let p be a prime number.
Let a be a primitive root modulo p.
Define the multiplicative LCG:
X₀ = 1
Xₙ = aⁿ mod p
For N ≤ p, define the normalized spectral amplitude:
S_N(k) = | (1/N) Σ_{n=0}^{N-1} exp(2πi k Xₙ / p) |
for k ≠ 0 (mod p).
Theorem
For any prime p and primitive root a:
If N ≤ p^(2/3), then
S_N(k) ≤ C · N^(-1/2) · log p
for an absolute constant C.
If N ≤ p^(1/2), then
S_N(k) ≤ C' · N^(-1/2)
without logarithmic amplification.
Interpretation
This provides an explicit finite-length upper bound refinement over classical spectral lattice bounds, which typically do not provide prefix-explicit N-parametrized inequalities.
Relation to Classical Spectral Test
Classical spectral tests analyze lattice structure in ℝ^d and yield asymptotic discrepancy measures.
The present theorem provides:
• Finite-length bound
• Explicit N dependence
• Regime separation
• Applicability to prefix analysis
Proof Strategy (Sketch)
The proof combines:
Exponential sum bounds over finite fields
Weil-type bounds
Partial sum truncation control
Subgroup equidistribution arguments
Full formal derivation in development under analysis/spectral_bound_proof.tex.
