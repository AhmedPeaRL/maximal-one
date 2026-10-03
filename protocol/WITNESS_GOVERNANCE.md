# Witness Governance

## Purpose

Witnesses are provenance and runtime-observation artifacts.

They are not, by themselves, scientific evidence.

---

## Epistemic separation

The repository enforces the following distinctions:

- CI witness != external scientific evidence
- CI witness != independent replication
- CI witness != canonical scientific result
- CI witness != scientific claim support
- CI witness != causal evidence
- CI witness != HCM validation

---

## CI storage policy

Runtime witnesses generated during GitHub Actions execution are stored as
workflow artifacts.

They must not be continuously committed into the scientific repository tree.

The repository therefore does not use `data/external/witness_*.json` as a
rolling CI log.

---

## Scientific provenance

A genuinely external scientific observation may be incorporated only through
an explicitly declared provenance protocol.

Such an artifact must identify:

1. its external source,
2. acquisition time,
3. acquisition method,
4. integrity information,
5. whether it is independently generated,
6. whether it is scientifically relevant,
7. whether it is part of a declared replication protocol.

A CI-generated witness cannot satisfy these requirements merely because it
has a timestamp or cryptographic hash.

---

## Claim authority

No witness artifact has authority to promote the scientific claim.

Scientific claim promotion remains governed by the declared scientific
validation protocol and its machine-gated requirements.

---

## Retention

Routine CI witnesses use GitHub Actions artifact retention rather than
permanent repository history.

Historical scientific provenance, when genuinely required, should be
preserved as an explicit release-level provenance bundle rather than as an
unbounded sequence of per-run witness files.
