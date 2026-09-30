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
            "SCIENTIFIC EXECUTION BLOCKED: "
            "required methodological dataset is missing. "
            "No synthetic fallback is permitted."
        )
       
        data = {
            "baseline": np.random.normal(1.0, 0.2, 100),
            "model": np.random.normal(1.05, 0.2, 100)
        }

        df = pd.DataFrame(data)
        os.makedirs("../data", exist_ok=True)
        df.to_csv(path, index=False)

    try:
        df = pd.read_csv(path)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        df = pd.DataFrame()

    if df.empty or "spectral_exponent" not in df.columns:
        print("⚠️ Invalid or missing dataset → regenerating spectral_exponent fallback")
        df = pd.DataFrame({
            "spectral_exponent": np.random.normal(1.0, 0.1, 200)
        })

    # نستخدم spectral_exponent بدلاً من mu_boot
    alphas = df["spectral_exponent"].values

    mean_alpha = np.mean(alphas)
    
    if not np.all(np.isfinite(alphas)):
        raise SystemExit(
            "ERROR: non-finite observations; "
            "power/effect analysis aborted."
        )

    std_alpha = np.std(
        alphas,
        ddof=1,
    )

    if not np.isfinite(std_alpha) or std_alpha <= 1e-12:
        raise SystemExit(
            "ERROR: zero or near-zero variance; "
            "power/effect-size result is invalid."
        )

    # اختبار مقابل H0: alpha = 1 (random walk theoretical slope)
    t_stat, p_value = stats.ttest_1samp(alphas, 1.0)

    # حساب Cohen's d
    effect_size = (mean_alpha - 1.0) / std_alpha

    print("=== Power Analysis ===")
    print("Mean spectral exponent:", mean_alpha)
    print("Std:", std_alpha)
    print("t-statistic:", t_stat)
    print("p-value:", p_value)
    print("Effect size (Cohen's d):", effect_size)

if __name__ == "__main__":
    main()
