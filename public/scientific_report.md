# MAXIMAL-ONE — Scientific Output Report

## Hypothesis

H0: Observed spectral structure is indistinguishable from noise.

H1: A persistent spectral invariant (α) exists across independent datasets.

---

## Experimental Summary

- Multi-dataset validation (real + synthetic + noise)
- Bootstrap statistical testing
- Cross-domain datasets (21 datasets)
- Deterministic reproducibility enforced

---

## Key Metrics

| Metric | Value |
|------|------|
| Alpha (α) | 2.23 |
| Sigma (σ) | 0.48 |
| Cross-domain success | 95% |
| Failure ratio | 5% |

---

## Statistical Decision

- Null Hypothesis: REJECTED (conditionally)
- Interpretation: A persistent spectral structure (α) is observed across multiple domains,
  but with variability depending on dataset characteristics.

---

## Interpretation

- Structure is NOT universal
- Structure is NOT absent
- Structure behaves as a **conditional invariant**

---

## Reproducibility

- Deterministic seeds enforced
- Full pipeline reproducible via GitHub Actions
- Environment fingerprint hashed

---

## Integrity

- Canonical report hash stored
- Cross-validation across datasets
- External falsification allowed

---

## Scientific Position

This system does NOT claim universal structure.

It demonstrates that:

> Under controlled conditions, a measurable spectral invariant (α)
> can persist across heterogeneous datasets beyond pure noise.

---

## Next Step

- Blind external validation
- Larger datasets
- Independent replication
