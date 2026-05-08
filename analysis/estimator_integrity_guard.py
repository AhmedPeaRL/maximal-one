import numpy as np

MAX_ALLOWED_ALPHA = 4.5
MAX_SATURATION_RATIO = 0.15


def validate_alpha_distribution(alphas):

    alphas = np.asarray(alphas, dtype=np.float64)

    finite = alphas[np.isfinite(alphas)]

    if len(finite) == 0:
        raise SystemExit("❌ No finite alpha values")

    saturated = np.sum(
        finite >= MAX_ALLOWED_ALPHA
    )

    ratio = saturated / len(finite)

    print(f"Saturated ratio: {ratio:.4f}")

    if ratio > MAX_SATURATION_RATIO:
        raise SystemExit(
            "❌ Estimator saturation too high"
        )

    print("✅ ESTIMATOR INTEGRITY HOLDS")


if __name__ == "__main__":

    sample = np.array([
        5.0,
        2.1,
        1.8,
        2.0,
        0.9,
        3.9
    ])

    validate_alpha_distribution(sample)
