# Hybrid Consciousness Model:
## Statistical Structural Validation via Multi-Seed Spectral Analysis

### Abstract

We test whether the HCM generative process produces statistically distinguishable spectral structure compared to:

1. Gaussian Random Walk (Null)
2. Fractional Brownian Motion
3. Alternative parametric baselines

Across 50 independent seeds, we compute:

- Spectral exponent
- Hurst exponent (DFA)
- Bayesian model evidence
- Statistical power
- Null ensemble t-tests

### Hypothesis

H1:
The HCM spectral exponent distribution differs significantly from null and FBM baselines.

H0:
No statistically significant difference exists.

### Methods

All experiments are reproducible via:
`.github/workflows/multi-seed-sweep.yml`

Data:
`/data/`

### Falsification Criteria

The model fails if:

- p-value > 0.05 (null ensemble)
- Bayes factor < 3 consistently
- Power < 0.8
- Hurst ≈ 0.5 across seeds

### Results

See:
- power_result.txt
- null_test.txt
- fbm_comparison.txt
- model_comparison.txt
- hurst.txt

### Conclusion

This preprint presents infrastructure-level validation.
Scientific validity depends strictly on statistical outcome, not philosophical framing.
