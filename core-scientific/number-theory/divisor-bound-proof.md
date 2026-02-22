# Lemma: Divisor Upper Bound

Lemma.
For all integers k ≥ 1,

    d(k) ≤ 2√k

where d(k) denotes the number of positive divisors of k.

Proof.

Let k ≥ 1 be an integer.

If d divides k, then k/d also divides k.
Thus divisors come in symmetric pairs (d, k/d).

If d ≤ √k then k/d ≥ √k.
Hence each divisor less than √k pairs with a distinct divisor greater than √k.

There are at most ⌊√k⌋ possible integers ≤ √k.
Each such divisor contributes at most two divisors to the total count.

If k is a perfect square, √k contributes one unpaired divisor.

Therefore:

    d(k) ≤ 2⌊√k⌋ ≤ 2√k

Q.E.D.
