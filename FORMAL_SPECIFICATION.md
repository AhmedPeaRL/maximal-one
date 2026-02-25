# Formal Specification — maximal-one

## 1. System Definition

Let K be a deterministic kernel defined by:

K(seed, N) → S

Where:
- seed ∈ ℕ
- N ∈ ℕ
- S = {mean, variance, sha256}

K is implemented via a seeded PRNG (Python Random with fixed seed).

---

## 2. Determinism Property

Lemma 1 — Deterministic Reproducibility

For fixed seed and N:

K(seed, N) = K(seed, N)

Proof Sketch:
Given Python’s Mersenne Twister is deterministic for fixed seed,
the generated sequence is identical.
Therefore mean and variance are identical.
Therefore sha256 over canonical JSON is identical.

---

## 3. Statistical Convergence Property

Let theoretical variance V = 1/12.

Theorem 1 — Bounded Statistical Convergence

For sufficiently large N:

| Var_sample − V | < ε

where ε is predefined tolerance.

This is justified by the Law of Large Numbers.

Boundary Condition:
The system does NOT claim invariance across seeds.
It claims convergence within tolerance.

Failure Mode:
If | Var_sample − V | ≥ ε → OUT_OF_STATISTICAL_BOUND

---

## 4. Hash Integrity Property

Lemma 2 — Canonical Hash Stability

Given identical canonical JSON,
sha256(canonical_json) is invariant.

Failure Mode:
Any structural mutation changes hash.

---

## 5. Adversarial Stress Model

Adversary may:
- change seed
- change N
- attempt boundary violation

System survives if:
All samples remain within tolerance bounds.

---

## 6. Non-Claims

The system does NOT claim:
- cryptographic randomness
- theoretical novelty in PRNG
- new probability law

It claims:
Explicit boundary-defined deterministic reproducibility.

---

## 7. Independent Reproduction Protocol

1. Clone repository
2. Run:
   python repro-core/deterministic_kernel.py
   python repro-core/adversarial_test.py
3. Verify identical hash output
4. Verify SURVIVED_ADVERSARIAL_STRESS

---

End of Formal Specification
