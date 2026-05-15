import numpy as np
import json
import pandas as pd
from analysis.real_null_model import build_null_distribution
from analysis.numerical_spectral_verification import estimate_alpha
from analysis.statistical_guard import robust_p_value, sanity_check

def compute_effect_size(real_alpha, null_alphas):
    mean_null = np.mean(null_alphas)
    std_null = np.std(null_alphas)

    if std_null == 0:
        return 0.0

    return float((real_alpha - mean_null) / std_null)

def compute_p_value(real_alpha, null_alphas):
    sanity_check(null_alphas)
    return robust_p_value(real_alpha, null_alphas)

def evaluate_significance(real_alpha, null_alphas):
    effect = compute_effect_size(real_alpha, null_alphas)
    p_value = compute_p_value(real_alpha, null_alphas)

    return {
        "effect_size": float(effect),
        "p_value": float(p_value),
        "significant": bool((p_value < 0.05) and (effect > 2))
    }

if __name__ == "__main__":
    df = pd.read_csv("real-data/sunspots_global_extended.csv")

    if "value" in df.columns:
        series = df["value"].values
    elif "Sunspots" in df.columns:
        series = df["Sunspots"].values
    else:
        raise ValueError("Dataset must contain 'value' or 'Sunspots' column")
        
    # ✅ الحقيقي
    real_alpha = estimate_alpha(series)

    # ✅ null distribution
    from analysis.null_hierarchy import evaluate_all_nulls

    null_summary = evaluate_all_nulls(series)

    print("=== NULL HIERARCHY ===")
    for k, v in null_summary.items():
        print(k, v)

    # ✅ تنظيف الـ NaNs (مهم جداً)
    null_alphas = null_alphas[np.isfinite(null_alphas)]

    if len(null_alphas) < 30:
        raise ValueError("Null model collapsed → too few valid samples")

    # ✅ احسبهم مرة واحدة
    null_mean = float(np.mean(null_alphas))
    null_std = float(np.std(null_alphas))

    result = evaluate_significance(real_alpha, null_alphas)

    print("=== TRUE STATISTICAL TEST ===")
    print("real_alpha:", real_alpha)
    print("null_mean:", null_mean)
    print("null_std:", null_std)
    print(result)

    # ✅ guard حقيقي
    if np.isnan(null_mean) or np.isnan(null_std):
        raise ValueError("Null model failed → invalid statistical baseline")

    with open("artifacts/statistical_verdict.json", "w") as f:
        json.dump({
            "real_alpha": float(real_alpha),
            "null_mean": null_mean,
            "null_std": null_std,
            **result
        }, f, indent=2)
