# Formal Reproducibility Note
Version: 1.0  
Status: Deterministic Verified  
Scope: maximal-one v1.0.0  

---

## 1. Purpose

This document formally defines the reproducibility guarantees of the maximal-one publication pipeline.

It specifies the deterministic relationships between:

- scientificHash
- compositeSeal
- deterministicArtifactHash
- release tag

This note contains no interpretive language.  
Only structural properties are described.

---

## 2. Deterministic Construction

Let:

S = canonical scientific source  
H_s = SHA256(S)  
H_c = SHA256(H_s || manifest || invariants)  
H_d = SHA256(H_s || H_c)

Where:

- H_s = scientificHash
- H_c = compositeSeal
- H_d = deterministicArtifactHash
- "||" denotes byte-level concatenation
- SHA256 denotes FIPS 180-4 compliant hashing

Then:

For any execution environment E₁, E₂ …

If canonical source S is identical byte-for-byte, then:

H_d(E₁) = H_d(E₂)

---

## 3. Environmental Independence

The deterministicArtifactHash is independent of:

- CI runner region
- Execution host
- Machine architecture
- Runtime container identity
- Temporal execution variance

Provided that:

- Canonical source bytes remain unchanged
- Hashing algorithm implementation is standard-compliant

---

## 4. Immutability Condition

If any single byte of S changes:

ΔS ≠ 0  ⇒  H_s changes  
H_s change ⇒ H_c changes  
H_c change ⇒ H_d changes  

Therefore:

The release tag bound to H_d cannot remain valid under mutation.

---

## 5. Collision Assumption

Security properties rely on SHA-256 collision resistance.

Assumption:

No feasible second-preimage attack exists under current cryptographic knowledge.

If SHA-256 is ever broken, the protocol must upgrade to a stronger hash function.

---

## 6. Idempotent Release Lock

Release tag format:

vX.Y.Z-{deterministicArtifactHash}

If a release with identical deterministicArtifactHash exists:

No duplicate release is created.

This guarantees idempotent publication behavior.

---

## 7. Reproducibility Claim

Given:

- Public repository
- Public hashing algorithm
- Public manifest

Any independent auditor can:

1. Recompute scientificHash
2. Recompute compositeSeal
3. Recompute deterministicArtifactHash
4. Verify release tag integrity

Without reliance on internal CI state.

---

## 8. Conclusion

The maximal-one pipeline produces:

A deterministic, environment-independent, cryptographically bound publication artifact.

This is a structural guarantee.

No metaphysical claims are made.

---
