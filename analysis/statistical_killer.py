import numpy as np
from scipy import stats
import json

with open("artifacts/statistical_verdict.json", "w") as f:
    json.dump(result, f, indent=2)

def compute_effect_size(real_alpha, null_alphas):
    mean_null = np.mean(null_alphas)
    std_null = np.std(null_alphas)

    if std_null == 0:
        return 0

    return (real_alpha - mean_null) / std_null


def compute_p_value(real_alpha, null_alphas):
    greater = np.sum(null_alphas >= real_alpha)
    return greater / len(null_alphas)


def evaluate_significance(real_alpha, null_alphas):
    effect = compute_effect_size(real_alpha, null_alphas)
    p_value = compute_p_value(real_alpha, null_alphas)

    verdict = {
        "effect_size": effect,
        "p_value": p_value,
        "significant": p_value < 0.05 and effect > 2
    }

    return verdict


if __name__ == "__main__":
    # Dummy example (replace with real pipeline output)
    real_alpha = 1.23
    null_alphas = np.random.normal(1.0, 0.05, 1000)

    result = evaluate_significance(real_alpha, null_alphas)

    print("Statistical Verdict:")
    print(result)
