# External Replication Protocol

## Objective
To independently verify whether the observed statistical structure persists outside the original environment.

## Requirements
- Clean environment (no prior repo state)
- Fresh clone of repository
- No access to original secrets

## Steps

1. Clone repository
2. Install dependencies using locked files
3. Run:

```bash
npm ci
python -m analysis.full_pipeline
Compare outputs:
spectral exponent (α)
variance (σ)
final decision
Validation Criteria
Replication is considered valid if:
|α_replica - α_original| < 0.05
decision remains unchanged
hash integrity holds
Reporting
Submit:
report.json
report.hash
environment fingerprint
Interpretation
Replication success does NOT imply intrinsic intelligence.
It only confirms structural persistence under independent conditions.
