# Release Protocol
Status: Mandatory Procedure
Scope: maximal-one

---

## 1. Trigger Condition

A new release must be created if and only if:

Canonical scientific content changes by at least one byte.

No release is created for:
- CI environment changes
- Dependency reinstallation
- Runner updates
- Region changes

---

## 2. Mandatory Sequence

Step 1:
Modify canonical scientific content.

Step 2:
Commit changes to main branch.

Step 3:
Allow CI to compute:
- scientificHash
- compositeSeal
- deterministicArtifactHash

Step 4:
Verify that deterministicArtifactHash differs from previous release.

Step 5:
Update the following files completely:

- PROVENANCE_ANCHOR.md
- INTEGRITY_MATRIX.md

All hash values must be replaced with the new computed values.

Step 6:
Commit updated files.

Step 7:
Allow release-lock workflow to create:

vX.Y.Z-{deterministicArtifactHash}

---

## 3. Version Increment Rule

Versioning format:

vMAJOR.MINOR.PATCH-{hash}

Increment rules:

MAJOR:
Breaking scientific structural change.

MINOR:
Scientific expansion without structural break.

PATCH:
Correction without conceptual expansion.

---

## 4. Prohibited Actions

Do not:

- Manually create GitHub releases.
- Manually create tags.
- Edit release metadata after creation.
- Reuse an existing deterministicArtifactHash.

---

## 5. Integrity Condition

A release is valid only if:

- deterministicArtifactHash matches CI output
- Tag exists and is unique
- PROVENANCE_ANCHOR.md matches current values
- INTEGRITY_MATRIX.md matches current values

If any mismatch exists:

Release is considered invalid.

---

## 6. Audit Resilience

Following this protocol guarantees:

- Deterministic reproducibility
- Clear provenance tracking
- Structural version control
- Environment independence

---

End of Protocol.
