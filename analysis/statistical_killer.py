import json
import numpy as np
import pandas as pd

from analysis.real_null_model import build_null_distribution
from analysis.numerical_spectral_verification import estimate_alpha
from analysis.statistical_guard import robust_p_value, sanity_check


OUTPUT = "artifacts/diagnostic_statistical_verdict.json"


def compute_effect_size(real_alpha, null_alphas):
    mean_null = np.mean(null_alphas)
    std_null = np.std(null_alphas)

    if not np.isfinite(std_null) or std_null <= 1e-12:
        raise ValueError(
            "Diagnostic null distribution has zero or non-finite variance."
        )

    return float(
        (real_alpha - mean_null) / std_null
    )


def compute_p_value(real_alpha, null_alphas):
    sanity_check(null_alphas)
    return robust_p_value(
        real_alpha,
        null_alphas
    )


def evaluate_significance(real_alpha, null_alphas):
    effect = compute_effect_size(
        real_alpha,
        null_alphas
    )

    p_value = compute_p_value(
        real_alpha,
        null_alphas
    )

    return {
        "effect_size": float(effect),
        "p_value": float(p_value),
        "significant": bool(
            (p_value < 0.05)
            and
            (effect > 2)
        )
    }


def main():
    df = pd.read_csv(
        "real-data/sunspots_global_extended.csv"
    )

    if "value" in df.columns:
        series = df["value"].values

    elif "Sunspots" in df.columns:
        series = df["Sunspots"].values

    else:
        raise ValueError(
            "Dataset must contain 'value' or 'Sunspots' column"
        )

    real_alpha = estimate_alpha(series)

    DIAGNOSTIC_SEED = 42

    null_alphas = build_null_distribution(
        series,
        n=500,
        seed=DIAGNOSTIC_SEED,
    )

    null_alphas = np.asarray(
        null_alphas,
        dtype=np.float64
    )

    null_alphas = null_alphas[
        np.isfinite(null_alphas)
    ]

    if len(null_alphas) < 30:
        raise ValueError(
            "Diagnostic null model produced too few valid samples."
        )

    sanity_check(null_alphas)

    null_mean = float(
        np.mean(null_alphas)
    )

    null_std = float(
        np.std(null_alphas)
    )

    if (
        not np.isfinite(null_mean)
        or
        not np.isfinite(null_std)
        or
        null_std <= 1e-12
    ):
        raise ValueError(
            "Diagnostic null distribution is invalid or degenerate."
        )

    result = evaluate_significance(
        real_alpha,
        null_alphas
    )

    output = {
        "scientific_claim_authority": False,
        "promotion_authority": False,
        "evidence_role": "diagnostic_only",
        "protocol_role": "non_primary_diagnostic",
        "not_the_canonical_primary_null": True,

        "seed": DIAGNOSTIC_SEED,
        "reproducibility": {
            "deterministic_for_fixed_seed": True,
            "scope": "diagnostic_only",
        },

        "real_alpha": float(real_alpha),
        "null_mean": null_mean,
        "null_std": null_std,

        **result,

        "interpretation": (
            "This artifact is diagnostic only. "
            "It must not be interpreted as the canonical "
            "scientific significance result and must not "
            "override artifacts/canonical_report.json."
        )
    }

    with open(
        OUTPUT,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            output,
            f,
            indent=2
        )

    print(
        json.dumps(
            output,
            indent=2
        )
    )


if __name__ == "__main__":
    main()
