import numpy as np

def bounded(x):
    if x is None:
        return 0.0

    if not np.isfinite(x):
        return 0.0

    return float(
        np.clip(
            x,
            0.0,
            1.0
        )
    )

def evidence_fusion(
    alpha_delta,
    p_value,
    scale_dispersion,
    validation_delta,
    falsification_delta
):

    alpha_score = bounded(
        alpha_delta / 0.50
    )

    p_score = bounded(
        1.0 - p_value
    )

    scale_score = bounded(
        1.0 - scale_dispersion
    )

    validation_score = bounded(
        1.0 - (
            validation_delta / 0.30
        )
    )

    falsification_score = bounded(
        falsification_delta / 0.50
    )

    score = (
        0.25 * alpha_score
        + 0.25 * p_score
        + 0.20 * scale_score
        + 0.15 * validation_score
        + 0.15 * falsification_score
    )

    return {
        "alpha_score": float(alpha_score),
        "p_score": float(p_score),
        "scale_score": float(scale_score),
        "validation_score": float(validation_score),
        "falsification_score": float(
            falsification_score
        ),
        "evidence_score": float(score),
        "structure_detected": bool(
            score >= 0.65
        )
    }
