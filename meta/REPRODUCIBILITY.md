# Reproducibility Statement

All computational experiments in maximal-one are deterministic.

## Deterministic Lock
- Hashing: SHA-256
- Environment fingerprint included
- No randomness without fixed seed

## Replication Steps

1. Clone repository
2. Run:
   python master_experiment.py --seed 42
3. Compare output hash with published hash

If mismatch occurs, system state is invalid.
