import pandas as pd
import numpy as np

"""
SCIENTIFIC ROLE: SYNTHETIC / METHODOLOGICAL ONLY.

This experiment does not provide empirical evidence
for the HCM spectral-persistence hypothesis.

Its outputs MUST NOT be used as:
- effect-size evidence for real data,
- independent replication,
- statistical significance for the primary claim,
- evidence of prediction,
- evidence of causality,
- evidence of HCM validity.

Any zero-variance or degenerate comparison is invalid.
"""

df = pd.read_csv("../data/multi_seed_results.csv")

real = df["spectral_exponent"].values
null = np.random.normal(
    loc=np.mean(real) - 0.05,
    scale=np.std(real),
    size=len(real)
)

mean_diff = np.mean(real) - np.mean(null)
pooled_std = np.sqrt((np.std(real)**2 + np.std(null)**2) / 2)
cohen_d = mean_diff / pooled_std

print("=== Effect Size (Cohen's d) ===")
print("Mean difference:", mean_diff)
print("Cohen's d:", cohen_d)
