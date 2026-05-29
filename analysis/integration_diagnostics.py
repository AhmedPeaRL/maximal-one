import numpy as np

def integration_score(series):
    series = np.asarray(
        series,
        dtype=np.float64
    )

    if len(series) < 32:
        return np.nan

    raw_std = np.std(series)

    diff_std = np.std(
        np.diff(series)
    ) + 1e-12

    ratio = raw_std / diff_std

    return float(ratio)

def classify_process(series):
    ratio = integration_score(series)

    if not np.isfinite(ratio):
        return "INVALID"

    if ratio > 20:
        return "INTEGRATED"

    if ratio > 8:
        return "PERSISTENT"

    return "STATIONARY"
