# Lower Bound on SOS Degree in 1D

## Setting

Let

f_k(x) = (1 - x^2)^k

on the compact interval [-1,1].

Assume representation:

f_k(x) = σ_0(x) + σ_1(x)(1 - x^2)

where σ_0, σ_1 are sums of squares.

---

## Boundary Behavior

At x = 1:

(1 - x^2) vanishes of order 1.

Thus:

f_k(x) vanishes of order k at x = 1.

This follows from:

1 - x^2 = (1 - x)(1 + x)

Local expansion near x = 1 gives leading term proportional to (1 - x)^k.

---

## Consequences for σ_0

Evaluating at x = 1:

f_k(1) = σ_0(1)

But f_k(1) = 0

Hence:

σ_0(1) = 0

Since σ_0 is a sum of squares,
each component must vanish at x = 1.

Therefore σ_0 vanishes with even multiplicity ≥ 2.

To match total multiplicity k,
degree(σ_0) must grow at least linearly in k.

---

## Contribution of σ_1

Since (1 - x^2) has multiplicity 1 at x = 1,
if σ_1 vanishes with multiplicity m,
then:

σ_1(1 - x^2) vanishes with multiplicity m + 1.

To obtain total multiplicity k:

m + 1 ≥ k

Hence m ≥ k - 1.

Since σ_1 is sum of squares,
its vanishing multiplicity is even.

Therefore degree(σ_1) ≥ k - 1.

---

## Conclusion

Any Putinar-type representation of f_k requires
degree growing at least linearly in k.

Thus minimal SOS degree is not uniformly bounded.
