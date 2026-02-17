# Algorithm Migration Policy
Status: Cryptographic Continuity Plan
Scope: maximal-one

---

## 1. Current Cryptographic Basis

The system currently relies on:

SHA-256

For:

- scientificHash
- compositeSeal
- deterministicArtifactHash

---

## 2. Trigger Conditions for Migration

Migration must be initiated if:

- A practical SHA-256 collision attack is demonstrated.
- NIST formally deprecates SHA-256.
- A preimage attack becomes computationally feasible.
- Major security advisories redefine SHA-256 as unsafe.

---

## 3. Migration Principles

Any migration must preserve:

- Determinism
- Backward verifiability
- Release identity traceability

---

## 4. Dual-Hash Transition Model

During migration:

Both hashes must be generated:

- SHA-256 (legacy)
- New algorithm (e.g., SHA-3-256)

Example structure:

{
  "scientificHash_sha256": "...",
  "scientificHash_sha3_256": "..."
}

---

## 5. Release Identity During Transition

Release identity becomes:

Version + Primary Hash + Secondary Hash

Until SHA-256 is formally retired.

---

## 6. Backward Compatibility

All historical releases remain valid.

They are evaluated under the cryptographic assumptions valid at time of release.

---

## 7. Structural Commitment

Cryptographic strength is a dependency.

Determinism is the invariant.

---

End of Migration Policy.
