import numpy as np

def consensus_check(
    alpha_fft,
    alpha_welch,
    p_value,
    dispersion,
    evidence_score,
    independent_real_domains=0,
):
    """
    Conservative scientific consensus gate.
    
    Important:
    - A reproducible estimate is not the same as statistical significance.
    - Null rejection is required for "supported".
    - At least two genuinely independent real domains are required
    for a cross-domain replication claim.
    """

    diagnostics = []

    if not (
        np.isfinite(alpha_fft)
        and np.isfinite(alpha_welch)
    ):
        diagnostics.append("invalid_alpha")

    if np.isfinite(alpha_fft) and np.isfinite(alpha_welch):
        delta = abs(
            float(alpha_fft) - float(alpha_welch)
        )
    else:
        delta = np.inf

    if delta > 0.30:
        diagnostics.append("method_disagreement")

    if not np.isfinite(dispersion):
        diagnostics.append("invalid_scale_dispersion")
    elif dispersion > 0.40:
        diagnostics.append("scale_instability")

    if not np.isfinite(p_value):
        diagnostics.append("invalid_p_value")
    elif p_value > 0.05:
        diagnostics.append("null_not_rejected")

    if independent_real_domains < 2:
        diagnostics.append("independent_real_replication_missing")

    passed = len(diagnostics) == 0

    if passed:
        status = "consensus_validated"
    elif (
        "null_not_rejected" in diagnostics
        or "independent_real_replication_missing" in diagnostics
    ):
        status = "under_investigation"
    else:
        status = "inconclusive"

    return {
        "passed": bool(passed),
        "status": status,
        "diagnostics": diagnostics,
        "agreement_delta": (
            float(delta)
            if np.isfinite(delta)
            else None
        ),
        "independent_real_domains": int(
            independent_real_domains
        ),
        "null_rejected": bool(
            np.isfinite(p_value) and p_value <= 0.05
        ),
    }
