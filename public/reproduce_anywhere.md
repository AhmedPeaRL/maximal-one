# Reproduce maximal-one outside GitHub

This guide allows full independent verification of the system without trusting the original repository.

---

## 1. Requirements

- Python 3.11+
- Node.js 18+

---

## 2. Download minimal reproducibility bundle

Download:

- canonical_report.json
- report.hash
- requirements-lock.txt

---

## 3. Verify integrity

```bash
sha256sum canonical_report.json
Compare with:

cat report.hash
They MUST match.

---

## 4. Install environment
Bash
pip install --require-hashes -r requirements-lock.txt

---

## 5. Run independent verification
Bash
python analysis/independent_verifier.py

---

## 6. Expected result

• alpha (α) should remain stable

• sigma (σ) should remain bounded

If not: → The system is falsified.

---

## 7. Zero trust principle

You are not required to trust:

• the repository

• the author

• GitHub

Only the reproducibility of results matters.
