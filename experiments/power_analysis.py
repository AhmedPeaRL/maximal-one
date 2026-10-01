import numpy as np
import pandas as pd
import os
from scipy import stats

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

def main():
    path = "../data/multi_seed_results.csv"

    if not os.path.exists(path):
        raise SystemExit(
            "SCIENTIFIC INTEGRITY STOP: "
            "required dataset is missing. "
            "Synthetic fallback generation is forbidden."
        )

    try:
        df = pd.read_csv(path)
    except Exception as exc:
        raise SystemExit(
            "SCIENTIFIC INTEGRITY STOP: "
            f"required dataset could not be read: {exc}"
        )

    if df.empty:
        raise SystemExit(
            "SCIENTIFIC INTEGRITY STOP: "
            "required dataset is empty."
        )

    if "spectral_exponent" not in df.columns:
        raise SystemExit(
            "SCIENTIFIC INTEGRITY STOP: "
            "required spectral_exponent column is missing. "
            "Synthetic fallback generation is forbidden."
        )

    alphas = (
        pd.to_numeric(
            df["spectral_exponent"],
            errors="coerce",
        )
        .to_numpy(
            dtype=float
        )
    )

    if not np.all(
        np.isfinite(alphas)
    ):
        raise SystemExit(
            "SCIENTIFIC INTEGRITY STOP: "
            "non-finite spectral_exponent values."
        )

    if len(alphas) < 2:
        raise SystemExit(
            "SCIENTIFIC INTEGRITY STOP: "
            "insufficient observations."
        )

    std_alpha = np.std(
        alphas,
        ddof=1,
    )

    if not np.isfinite(
        std_alpha
    ) or std_alpha <= 1e-12:
        raise SystemExit(
            "SCIENTIFIC INTEGRITY STOP: "
            "zero or near-zero variance."
        )

    mean_alpha = np.mean(
        alphas
    )

    # This is a methodological diagnostic only.
    # It is NOT the current primary HCM hypothesis test.
    t_stat, p_value = (
        stats.ttest_1samp(
            alphas,
            1.0,
        )
    )

    effect_size = (
        mean_alpha - 1.0
    ) / std_alpha

    print(
        "=== Methodological Power Diagnostic ==="
    )

    print(
        "Mean spectral exponent:",
        mean_alpha,
    )

    print(
        "Std:",
        std_alpha,
    )

    print(
        "t-statistic:",
        t_stat,
    )

    print(
        "p-value:",
        p_value,
    )

    print(
        "Effect size:",
        effect_size,
    )

    print(
        "SCIENTIFIC ROLE: diagnostic-only"
    )

    print(
        "PRIMARY CLAIM AUTHORITY: false"
    )
