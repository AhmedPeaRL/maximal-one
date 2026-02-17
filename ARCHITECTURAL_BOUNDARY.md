# Architectural Boundary
Status: Structural Scope Definition
Scope: maximal-one

---

## 1. Scientific Domain

The following directory is canonical scientific content:

core-scientific/

Any byte change within this directory:

- MUST alter scientificHash
- MUST alter compositeSeal
- MUST alter deterministicArtifactHash
- MUST trigger a new release

---

## 2. Non-Scientific Domain

The following are explicitly non-scientific:

- .github/
- README.md
- FORMAL_REPRODUCIBILITY_NOTE.md
- PROVENANCE_ANCHOR.md
- INTEGRITY_MATRIX.md
- RELEASE_PROTOCOL.md
- ARCHITECTURAL_BOUNDARY.md
- package.json
- package-lock.json

Changes in these files:

- MUST NOT alter scientificHash
- MUST NOT alter compositeSeal
- MUST NOT alter deterministicArtifactHash

---

## 3. Hash Scope Rule

scientificHash is computed exclusively from:

core-scientific/

No other directory contributes to hash calculation.

---

## 4. Boundary Invariant

If a non-scientific file alters a hash:

System integrity is considered broken.

If a scientific file changes without altering hash:

System integrity is considered broken.

---

## 5. Conceptual Clarification

This repository separates:

Scientific Meaning Layer  
from  
Operational Infrastructure Layer  

Determinism applies only to the Scientific Meaning Layer.

---

## 6. Structural Philosophy

Meaning must be isolated from mechanism.

Infrastructure may evolve.  
Scientific content must remain byte-explicit.

This boundary guarantees:

Epistemic clarity  
Operational flexibility  
Audit precision  

---

End of Boundary.
