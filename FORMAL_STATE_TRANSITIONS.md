# Formal State Transitions Specification

System: maximal-one

---

## 1. Transition Trigger

A transition is triggered only when:

- report.json content changes intentionally.

---

## 2. Required Actions For Transition

1. Recompute deterministicArtifactHash.
2. Update SYSTEM_STATE_MANIFEST.json.
3. Append new node to VERSION_MIGRATION_GRAPH.json.
4. Create new release tag:
   v<version>-<artifact_hash>
5. Preserve all previous state records.

---

## 3. Prohibited Actions

- Editing past nodes in migration graph.
- Reusing artifact hashes.
- Mutating tagged releases.
- Silent state modification.

---

## 4. Graph Integrity Rule

VERSION_MIGRATION_GRAPH.json must always form
a valid acyclic graph.

No circular parent references allowed.

---

## 5. Deterministic Supremacy Rule

Artifact hash overrides semantic version naming.

Version labels are human-readable.
Artifact hashes are authoritative.

---

End of Formal State Transitions Specification.
