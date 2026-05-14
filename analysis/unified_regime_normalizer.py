import numpy as np


def enforce_stationarity(x):
    x = np.asarray(x, dtype=np.float64)

    # detrend
    t = np.arange(len(x))
    coeffs = np.polyfit(t, x, 1)
    trend = coeffs[0] * t + coeffs[1]
    x = x - trend

    return x


def variance_stabilize(x):
    x = np.asarray(x, dtype=np.float64)

    std = np.std(x)

    if std < 1e-8:
        raise ValueError("Degenerate variance")

    return x / std


def clip_outliers(x, z=4.0):
    x = np.asarray(x, dtype=np.float64)

    mu = np.mean(x)
    sigma = np.std(x)

    lower = mu - z * sigma
    upper = mu + z * sigma

    return np.clip(x, lower, upper)


def unified_normalize(x):
    x = np.asarray(x, dtype=np.float64)

    x = enforce_stationarity(x)
    x = clip_outliers(x)
    x = variance_stabilize(x)

    return np.asarray(x, dtype=np.float64)
