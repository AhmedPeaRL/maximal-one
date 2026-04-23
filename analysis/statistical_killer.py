import numpy as np
from scipy import stats
import json
import pandas as pd
from analysis.real_null_model import build_null_distribution

df = pd.read_csv("real-data/sunspots_global.csv")
series = df["value"].values

def to_native(x):
    """Convert numpy types to native Python types"""
    if isinstance(x, (np.bool_,)):
        return bool(x)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating,)):
        return float(x)
    return x

def compute_effect_size(real_alpha, null_alphas):
    mean_null = np.mean(null_alphas)
    std_null = np.std(null_alphas)

    if std_null == 0:
        return 0.0

    return float((real_alpha - mean_null) / std_null)


def compute_p_value(real_alpha, null_alphas):
    greater = np.sum(null_alphas >= real_alpha)
    return float(greater / len(null_alphas))


def evaluate_significance(real_alpha, null_alphas):
    effect = compute_effect_size(real_alpha, null_alphas)
    p_value = compute_p_value(real_alpha, null_alphas)

    verdict = {
        "effect_size": to_native(effect),
        "p_value": to_native(p_value),
        "significant": bool((p_value < 0.05) and (effect > 2))
    }

    return verdict


if __name__ == "__main__":
    real_alpha = 1.23
    null_alphas = build_null_distribution(series, n=300)

    result = evaluate_significance(real_alpha, null_alphas)

    print("Statistical Verdict:")
    print(result)

    with open("artifacts/statistical_verdict.json", "w") as f:
        json.dump(result, f, indent=2)
