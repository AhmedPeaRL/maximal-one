# External Reproduction Protocol

## Objective

This document defines the exact procedure required for independent external reproduction of the maximal-one system.

No internal assumptions are allowed.

---

## Requirements

- Clean machine (no prior environment)
- Python 3.11+
- Node.js (18, 20, or 24)
- Git

---

## Step 1 — Clone Repository

```bash
git clone https://github.com/AhmedPeaRL/maximal-one.git
cd maximal-one

## Step 2 — Install Dependencies

python master_experiment.py

## Step 3 — Run Core Experiment

python master_experiment.py

## Step 4 — Validate Output

Expected:
• artifacts/canonical_report.json
• report.hash

Verify:

sha256sum artifacts/canonical_report.json
cat artifacts/report.hash

Hashes must match.

## Step 5 — Run Full Validation Pipeline

npm run validate
npm run verify
npm run stability

## Step 6 — Report Results

Submit:

• canonical_report.json
• report.hash
• environment details

---

## Integrity Condition

Any mismatch invalidates reproduction.

Any success must be independently verifiable.

---

## Scientific Position

External reproduction is REQUIRED before any claim escalation.

Until then:

Status = PROVISIONAL
