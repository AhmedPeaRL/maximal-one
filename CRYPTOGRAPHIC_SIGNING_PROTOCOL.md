# Cryptographic Signing Protocol
System: maximal-one
Layer: Trust Anchoring Extension

---

## 1. Purpose

This protocol introduces personal cryptographic signing
to anchor deterministic states to a human-controlled key.

Determinism ensures consistency.
Signature ensures authorship integrity.

---

## 2. Trust Model

The system distinguishes between:

- Deterministic integrity (hash-based)
- Authorship authenticity (signature-based)

Both layers are independent.

---

## 3. Signing Rule

For every release tag:

1. The deterministicArtifactHash must be signed.
2. The signature must be generated using a private key
   controlled exclusively by the system author.
3. The public key must be published in this repository.

---

## 4. Signature Artifact

Each release must include:

- artifact_hash
- signature
- public_key_fingerprint

---

## 5. Verification Independence

Signature verification must be possible:

- Offline
- Without GitHub
- Without CI
- Using standard cryptographic tools

---

## 6. Revocation Clause

If private key compromise occurs:

- A revocation statement must be committed.
- A new key must be generated.
- Future releases must reference new fingerprint.

---

## 7. Deterministic Supremacy

Signature does not replace deterministic hash.

Hash defines state.
Signature defines authorship.

---

End of Cryptographic Signing Protocol.
