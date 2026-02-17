# Threat Model
Status: Structural Risk Declaration
Scope: maximal-one

---

## 1. Cryptographic Threats

### 1.1 SHA-256 Collision

If a practical collision attack against SHA-256 becomes feasible:

All hash guarantees collapse.

Mitigation:
Algorithm migration plan required.

---

## 2. Dependency Threats

Node.js runtime changes may alter:

- JSON serialization order
- Buffer handling
- Hash encoding behavior

Mitigation:
Pin major runtime version (Node 18 LTS).

---

## 3. Supply Chain Risk

Compromised GitHub Actions runner
Compromised dependency source
Malicious workflow injection

Mitigation:
- Minimal dependencies
- Locked workflow definitions
- Public transparency

---

## 4. Repository Integrity Risk

Force-push rewriting history  
Manual modification of generated artifacts  

Mitigation:
Release tag locking  
Manifest cross-verification  

---

## 5. Attestation Scope Limitation

Attestation proves:

Internal consistency.

It does NOT prove:

External scientific truth.

---

## 6. System Boundary

The system guarantees deterministic publication.

It does NOT guarantee:

Scientific correctness  
Philosophical validity  
Ontological truth  

---

End of Threat Model.
