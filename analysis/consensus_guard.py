import numpy as np

def consensus_check(
    alpha_fft,
    alpha_welch,
    p_value,
    dispersion,
    evidence_score
):

    diagnostics = []

    if not (
        np.isfinite(alpha_fft)
        and
        np.isfinite(alpha_welch)
    ):
        diagnostics.append(
            "invalid_alpha"
        )

    delta = abs(
        alpha_fft
        -
        alpha_welch
    )

    if delta > 0.30:
        diagnostics.append(
            "method_disagreement"
        )

    if dispersion > 0.40:
        diagnostics.append(
            "scale_instability"
        )

    if p_value > 0.05:
        diagnostics.append(
            "weak_statistics"
        )

    passed = len(diagnostics) == 0

    if passed:
        status = "supported"
    elif "weak_statistics" in diagnostics:
        status = "under_investigation"
    else:
        status = "inconclusive"

    return {
        "passed": passed,
        "status": status,
        "diagnostics": diagnostics,
        "agreement_delta": float(delta),
    }
