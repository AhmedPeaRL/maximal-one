import numpy as np

def robust_p_value(real_alpha, null_alphas):
    """
    Prevent fake zero p-values
    """

    n = len(null_alphas)

    greater = np.sum(null_alphas >= real_alpha)

    # Add-one smoothing (CRITICAL)
    p = (greater + 1) / (n + 1)

    return float(p)


def sanity_check(null_alphas):
    """
    Detect collapsed null distribution
    """

    std = np.std(null_alphas)

    if std < 1e-3:
        raise RuntimeError("Null distribution collapsed → invalid test")

    return True
