from __future__ import annotations
import numpy as np

def bounded(x):
    """
    Convert a finite numeric value into [0, 1].

    Invalid values contribute zero evidence.
    """

    if x is None:
        return 0.0

    try:
        x = float(x)
    except (TypeError, ValueError):
        return 0.0

    if not np.isfinite(x):
        return 0.0

    return float(
        np.clip(
            x,
            0.0,
            1.0,
        )
    )

def significance_score(p_value):
    """
    Convert statistical significance into a bounded
    positive-evidence component.

    p >= 0.05 contributes ZERO positive significance evidence.

    This function never interprets failure to reject the null
    as positive evidence.
    """

    if p_value is None:
        return 0.0

    try:
        p_value = float(p_value)
    except (TypeError, ValueError):
        return 0.0

    if not np.isfinite(p_value):
        return 0.0

    if p_value >= 0.05:
        return 0.0

    return bounded(
        1.0 - (
            p_value / 0.05
        )
    )

def evidence_fusion(
    alpha_delta,
    p_value,
    scale_dispersion,
    validation_delta,
    falsification_delta,
):
    """
    Conservative evidence aggregation.

    IMPORTANT:
    evidence_score is a diagnostic aggregation only.
    It must NOT override the independent scientific
    consensus gate.
    """

    alpha_score = bounded(
        alpha_delta / 0.50
    )

    p_score = significance_score(
        p_value
    )

    if np.isfinite(scale_dispersion):
        scale_score = bounded(
            1.0 - float(scale_dispersion)
        )
    else:
        scale_score = 0.0

    if np.isfinite(validation_delta):
        validation_score = bounded(
            1.0 - (
                float(validation_delta) / 0.30
            )
        )
    else:
        validation_score = 0.0

    falsification_score = bounded(
        falsification_delta / 0.50
    )

    score = (
        0.15 * alpha_score
        + 0.35 * p_score
        + 0.20 * scale_score
        + 0.15 * validation_score
        + 0.15 * falsification_score
    )

    return {
        "alpha_score": float(alpha_score),
        "p_score": float(p_score),
        "scale_score": float(scale_score),
        "validation_score": float(validation_score),
        "falsification_score": float(falsification_score),
        "evidence_score": float(score),

        # Diagnostic only.
        "structure_detected": bool(
            score >= 0.65
        ),

        "significance_supported": bool(
            np.isfinite(p_value)
            and p_value <= 0.05
        ),

        # Explicit epistemic separation.
        "positive_significance_evidence": bool(
            np.isfinite(p_value)
            and p_value <= 0.05
        ),
    }
