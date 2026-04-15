# Independent Reproduction Protocol

## Objective
Reproduce the full scientific pipeline without author involvement.

---

## Method 1 — Zero Knowledge Reproduction

1. Send POST request:
POST /api/public_witness_endpoint

Body:
```json
{
  "input": "any arbitrary signal"
}

2. Wait for GitHub Actions run

3. Verify:

• artifacts/canonical_report.json

• report.hash

• public/live_truth.json

## Method 2 — Full Local Reproduction

git clone https://github.com/AhmedPeaRL/maximal-one
cd maximal-one

npm ci
pip install -r requirements-lock.txt

python -m analysis.global_scientific_verdict

## Expected Outcome

• Deterministic or controlled divergence behavior

• Spectral structure persistence

• No manual intervention required

## Falsification Condition

If:

• structure disappears

• results diverge beyond tolerance

• system fails under adversarial inputs

→ Claim is rejected
