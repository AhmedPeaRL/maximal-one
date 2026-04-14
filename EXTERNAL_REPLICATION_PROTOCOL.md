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
