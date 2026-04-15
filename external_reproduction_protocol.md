# External Reproduction Protocol (Critical Layer)

## Purpose
This document defines how an **independent external agent** can reproduce,
challenge, or falsify the system WITHOUT relying on internal trust.

---

## Minimal Reproduction Path

### Step 1 — Clone Repository

```bash
git clone https://github.com/ahmedpearl/maximal-one
cd maximal-one

## Step 2 — Install Dependencies

npm ci
pip install --require-hashes -r requirements-lock.txt

## Step 3 — Run Full Validation

npm run validate
npm run verify
npm run stability

python -m analysis.global_scientific_verdict

## Step 4 — Verify Determinism

Compare hashes:

• node_report.hash

• report.hash

Across:

• Node 18

• Node 20

• Node 24

Expected:

• Either strict equality OR controlled divergence

---

## External Falsification Path

To challenge the system:

• Modify datasets (controlled perturbation)

• Inject adversarial noise

• Break invariants intentionally

Then re-run:

python -m analysis.self_attack_protocol
python -m analysis.external_hostile_validation

---

## Acceptance Criteria

System is considered provisionally valid IF:

• No falsification survives

• Deterministic behavior is preserved

• External anchors remain consistent

• Statistical thresholds are maintained

---

## Rejection Criteria

System is rejected IF:

• Any reproducible falsification succeeds

• Hash integrity breaks

• External anchor mismatch occurs

• Predictions fail under blind test

# Critical Constraint

This system MUST be reproducible WITHOUT the author.

No internal explanation is allowed as dependency.

---

## Contact

# If reproduction succeeds or fails:

Open issue or submit report with:

• Environment details

• Hash outputs

• Divergence fingerprints
