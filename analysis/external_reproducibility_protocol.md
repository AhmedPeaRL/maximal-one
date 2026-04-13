# External Reproducibility Protocol

## Objective

To validate that all results produced by maximal-one
can be independently reproduced outside the original repository environment.

## Requirements

An external researcher must:

1. Clone the repository
2. Install dependencies
3. Execute:

    python master_experiment.py

4. Verify:

    - spectral outputs
    - report hash
    - statistical conclusions

## Validation Criteria

Reproduction is considered valid if:

- spectral exponent α deviation < 0.02
- report hash matches OR is explainably divergent
- statistical decision remains identical

## Failure Conditions

Reproduction fails if:

- outputs cannot be generated
- significant deviation occurs without explanation
- environment dependency causes instability

## Declaration

This repository does not claim validity
until external reproduction is confirmed.
