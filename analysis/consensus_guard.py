import numpy as np

def consensus_check(
    alpha_fft,
    alpha_welch,
    p_value,
    dispersion
):

    if not (
        np.isfinite(alpha_fft)
        and
        np.isfinite(alpha_welch)
    ):
        return False

    if abs(
        alpha_fft
        -
        alpha_welch
    ) > 0.30:
        return False

    if p_value > 0.05:
        return False

    if dispersion > 0.40:
        return False

    return True
