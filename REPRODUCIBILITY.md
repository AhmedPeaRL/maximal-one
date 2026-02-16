# Reproducibility Protocol – maximal-one

This repository is cryptographically sealed and reproducible.

## Requirements

- Node.js 18.x
- npm 10.x

---

## Expected Outcome

• Multi-Seed Gate: PASSED

• Report integrity verified

• Independent audit: VERIFIED

• Release snapshot generated in:
core-scientific/release-lock/

## Deterministic Guarantee

If the canonical source remains unchanged, the following must remain identical:

• scientificHash

• compositeSeal

• deterministicArtifactHash

• releaseHash

Any deviation indicates mutation or corruption.

## Scientific Integrity Model

The system guarantees:

• Deterministic artifact identity

• Stable multi-seed envelope

• Independent reproducibility

• Cryptographic release immutability

This repository is designed for verification, not trust.

---

## 60-Second Verification

```bash
npm install
npm run validate
npm run verify
npm run audit
npm run freeze
