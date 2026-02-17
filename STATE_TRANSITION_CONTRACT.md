# Formal State Transition Contract
System: maximal-one
Layer: Architectural Continuity Enforcement

---

## 1. Purpose

This document defines the only valid pathways
through which the system state may evolve.

Determinism guarantees reproducibility.
This contract guarantees controlled evolution.

---

## 2. State Definition

The system state is formally defined as:

- core-scientific/
- publication-gate/
- package.json
- package-lock.json
- state-manifest.json
- report.json

Any modification affecting deterministicArtifactHash
constitutes a state mutation.

---

## 3. Valid Transition Conditions

A state mutation is valid only if:

1. Scientific validation passes.
2. Numerical stability verification passes.
3. Manifest consistency check passes.
4. Attestation hash is regenerated.
5. New deterministicArtifactHash is tagged.
6. Previous tag remains immutable.

If any condition fails, transition is invalid.

---

## 4. Immutability Clause

No previously released tag may be altered,
rewritten, or force-pushed.

Historical states are permanent.

---

## 5. Forward-Only Evolution

State transitions must be monotonic.

Rollback is allowed only as:

- A new forward commit
- Referencing prior stable tag
- With explicit justification commit message

---

## 6. External Independence

System validity must remain:

- Platform-independent
- CI-independent
- Toolchain-version agnostic

---

## 7. Zero Anthropomorphism Rule

The system performs computation only.
It possesses no awareness, intent, or subjective state.

All semantic interpretation is external.

---

End of State Transition Contract.
