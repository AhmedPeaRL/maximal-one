from __future__ import annotations
import numpy as np

DEFAULT_MAX_METHOD_DELTA = 0.30
DEFAULT_MAX_SCALE_DISPERSION = 0.40
DEFAULT_MAX_P_VALUE = 0.05
DEFAULT_MIN_INDEPENDENT_REAL_DOMAINS = 2

def consensus_check(
    alpha_fft,
    alpha_welch,
    p_value,
    dispersion,
    evidence_score,
    independent_real_domains=0,
    max_method_delta=DEFAULT_MAX_METHOD_DELTA,
    max_scale_dispersion=DEFAULT_MAX_SCALE_DISPERSION,
    max_p_value=DEFAULT_MAX_P_VALUE,
    min_independent_real_domains=(
        DEFAULT_MIN_INDEPENDENT_REAL_DOMAINS
    ),
):
    """
    Conservative scientific consensus gate.

    The gate evaluates evidence; it does not manufacture evidence.

    Thresholds are explicit inputs so that the canonical scientific
    specification can remain the single source of truth.

    Important distinctions:

    - Reproducibility is not inferred from statistical significance.
    - Null rejection is necessary but not sufficient.
    - Cross-method agreement is necessary.
    - Scale stability is necessary.
    - Independent real-domain replication is required.
    - evidence_score remains diagnostic and cannot override a
      failed scientific gate.
    """

    diagnostics = []

    try:
        max_method_delta = float(
            max_method_delta
        )

        max_scale_dispersion = float(
            max_scale_dispersion
        )

        max_p_value = float(
            max_p_value
        )

        min_independent_real_domains = int(
            min_independent_real_domains
        )
    except (
        TypeError,
        ValueError,
    ):
        return {
            "passed": False,
            "status": "invalid_configuration",
            "diagnostics": [
                "invalid_consensus_configuration"
            ],
            "agreement_delta": None,
            "independent_real_domains": int(
                independent_real_domains
            ),
            "null_rejected": False,
        }

    if not (
        np.isfinite(max_method_delta)
        and max_method_delta >= 0
    ):
        diagnostics.append(
            "invalid_method_delta_threshold"
        )

    if not (
        np.isfinite(max_scale_dispersion)
        and max_scale_dispersion >= 0
    ):
        diagnostics.append(
            "invalid_scale_threshold"
        )

    if not (
        np.isfinite(max_p_value)
        and 0 < max_p_value <= 1
    ):
        diagnostics.append(
            "invalid_p_value_threshold"
        )

    if min_independent_real_domains < 1:
        diagnostics.append(
            "invalid_replication_threshold"
        )

    if not (
        np.isfinite(alpha_fft)
        and
        np.isfinite(alpha_welch)
    ):
        diagnostics.append(
            "invalid_alpha"
        )

    if (
        np.isfinite(alpha_fft)
        and
        np.isfinite(alpha_welch)
    ):
        delta = abs(
            float(alpha_fft)
            -
            float(alpha_welch)
        )
    else:
        delta = np.inf

    if (
        np.isfinite(delta)
        and
        np.isfinite(max_method_delta)
        and
        delta > max_method_delta
    ):
        diagnostics.append(
            "method_disagreement"
        )

    if not np.isfinite(dispersion):
        diagnostics.append(
            "invalid_scale_dispersion"
        )
    elif (
        np.isfinite(max_scale_dispersion)
        and
        dispersion > max_scale_dispersion
    ):
        diagnostics.append(
            "scale_instability"
        )

    if not np.isfinite(p_value):
        diagnostics.append(
            "invalid_p_value"
        )
    elif (
        np.isfinite(max_p_value)
        and
        p_value > max_p_value
    ):
        diagnostics.append(
            "null_not_rejected"
        )

    if (
        int(independent_real_domains)
        <
        min_independent_real_domains
    ):
        diagnostics.append(
            "independent_real_replication_missing"
        )

    passed = (
        len(diagnostics) == 0
    )

    if passed:
        status = (
            "consensus_validated"
        )

    elif (
        "null_not_rejected"
        in diagnostics
        or
        "independent_real_replication_missing"
        in diagnostics
    ):
        status = (
            "under_investigation"
        )

    elif (
        "scale_instability"
        in diagnostics
        or
        "method_disagreement"
        in diagnostics
    ):
        status = (
            "inconclusive"
        )

    else:
        status = (
            "invalid_configuration"
            if any(
                item.startswith("invalid_")
                for item in diagnostics
            )
            else
            "inconclusive"
        )

    return {
        "passed": bool(passed),

        "status": status,

        "diagnostics": diagnostics,

        "agreement_delta": (
            float(delta)
            if np.isfinite(delta)
            else None
        ),

        "max_method_delta":
            float(max_method_delta),

        "max_scale_dispersion":
            float(max_scale_dispersion),

        "max_p_value":
            float(max_p_value),

        "min_independent_real_domains":
            int(
                min_independent_real_domains
            ),

        "independent_real_domains":
            int(independent_real_domains),

        "null_rejected": bool(
            np.isfinite(p_value)
            and
            p_value <= max_p_value
        ),

        "evidence_score_diagnostic_only":
            True,

        "evidence_score":
            (
                float(evidence_score)
                if np.isfinite(evidence_score)
                else None
            ),
    }
