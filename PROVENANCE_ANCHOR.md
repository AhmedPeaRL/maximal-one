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

f5b8c5ec6dcd65434a65209a317fd31fa394d8fc42881cbeb1e3929170deccbe

Algorithm:
SHA-256

---

## 3. Scientific Hash

c17aee57afcbc97ed3aa780144f9d37eac34ef525b09f9df8c024df66d4f5a4c

---

## 4. Composite Seal

0c7a74fe6055d9a1024edc9314a12ea8cdc89f45467196f1e19d75c8527a6ee3

---

## 5. Canonical Commit Reference

Commit at time of anchoring:

287017ce2cbcf0ca77947096050d5d93f5556ef2

Note:

Commit hash and deterministicArtifactHash are distinct values.
The deterministicArtifactHash is derived from scientific content,
not from Git commit identity.

---

## 6. Mutation Rule

If canonical scientific content changes:

- scientificHash must change
- compositeSeal must change
- deterministicArtifactHash must change
- release tag must change
- this file must be fully replaced

---

## 7. Auditor Instruction

To verify integrity:

1. Clone repository
2. Checkout tag:
   v1.0.0-f5b8c5ec6dcd65434a65209a317fd31fa394d8fc42881cbeb1e3929170deccbe
3. Recompute scientificHash
4. Recompute compositeSeal
5. Recompute deterministicArtifactHash
6. Confirm equality

No CI access required.

---

End of Record.
