# State Evolution Model
System: maximal-one
Type: Deterministic Evolution Layer

---

## 1. Foundational Principle

State evolution must be:

- Explicit
- Versioned
- Hash-anchored
- Non-ambiguous

No implicit transitions are permitted.

---

## 2. State Definition

A valid system state consists of:

- report.json
- state-manifest.json
- SYSTEM_STATE_MANIFEST.json
- Deterministic artifact hash
- Scientific hash

Together these define a canonical state snapshot.

---

## 3. State Transition Rule

A state transition is valid only if:

1. report.json changes
2. deterministicArtifactHash changes
3. A new release tag is generated
4. SYSTEM_STATE_MANIFEST.json is updated
5. Migration metadata is recorded

If any condition is missing,
transition is invalid.

---

## 4. Non-Linear Evolution Clause

Multiple future states may branch from a valid state.

Each branch must:

- Maintain deterministic integrity
- Declare parent state hash
- Generate unique artifact hash

---

## 5. Evolution Integrity Constraint

No state may modify:

- Past tagged releases
- Historical manifest entries

History is immutable.
Evolution is additive.

---

## 6. End Condition

If deterministic integrity fails,
state evolution halts.

Manual repair required.

---

End of State Evolution Model.
