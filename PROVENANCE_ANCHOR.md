# Provenance Anchor
Status: Canonical Binding Record
Scope: maximal-one
Version: v1.0.0

---

## 1. Release Identifier

Release Tag:

v1.0.0-f5b8c5ec6dcd65434a65209a317fd31fa394d8fc42881cbeb1e3929170deccbe

---

## 2. Deterministic Artifact Hash

deterministicArtifactHash:

f5b8c5ec6dcd65434a65209a317fd31fa394d8fc42881cbeb1e3929170deccbe

Algorithm:
SHA-256

---

## 3. Structural Binding

This release is cryptographically bound through:

scientificHash → compositeSeal → deterministicArtifactHash

As defined in:

FORMAL_REPRODUCIBILITY_NOTE.md

---

## 4. Canonical Commit Reference

The commit associated with this release must match:

f5b8c5ec6dcd65434a65209a317fd31fa394d8fc42881cbeb1e3929170deccbe

If commit hash diverges, this document becomes invalid.

---

## 5. Mutation Rule

If any byte in canonical source changes:

- A new scientificHash must be generated.
- A new compositeSeal must be generated.
- A new deterministicArtifactHash must be generated.
- A new release tag must be created.

This file must then be replaced entirely.

---

## 6. Auditor Instruction

To verify integrity:

1. Clone repository.
2. Checkout tag v1.0.0-f5b8c5ec6dcd65434a65209a317fd31fa394d8fc42881cbeb1e3929170deccbe
3. Recompute all hashes as defined in FORMAL_REPRODUCIBILITY_NOTE.md
4. Confirm equality.

No internal CI access required.

---

End of Record.
