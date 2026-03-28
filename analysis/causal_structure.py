import numpy as np

def lagged_correlation(x, max_lag=10):
    corrs = []

    for lag in range(1, max_lag):
        c = np.corrcoef(x[:-lag], x[lag:])[0,1]
        corrs.append((lag, c))

    return corrs

def dominant_lag(corrs):
    corrs = sorted(corrs, key=lambda x: abs(x[1]), reverse=True)
    return corrs[0] if corrs else (0,0)

def extract_causal_signature(series):
    corrs = lagged_correlation(series)

    lag, strength = dominant_lag(corrs)

    return {
        "dominant_lag": int(lag),
        "strength": float(strength)
    }
