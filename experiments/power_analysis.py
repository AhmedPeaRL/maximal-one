import numpy as np
import pandas as pd
from scipy import stats

def main():
    df = pd.read_csv("../data/multi_seed_results.csv")

    # نستخدم spectral_exponent بدلاً من mu_boot
    alphas = df["spectral_exponent"].values

    mean_alpha = np.mean(alphas)
    std_alpha = np.std(alphas, ddof=1)

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
