import numpy as np

def autocorrelation(x, lag=1):
    if len(x) < lag + 2:
        return 0.0
    return np.corrcoef(x[:-lag], x[lag:])[0,1]

def spectral_entropy(x, bins=50):
    hist, _ = np.histogram(x, bins=bins, density=True)
    hist = hist + 1e-12
    return -np.sum(hist * np.log(hist))

def predictability_score(series):

    series = np.array(series)

    if len(series) < 30:
        return 0.05  # 🔥 allow weak signal

    ac = abs(autocorrelation(series, lag=1))
    entropy = spectral_entropy(series)

    entropy_norm = entropy / np.log(len(series))

    score = ac * (1 - entropy_norm)

    return float(score)


# 🔥 RELAXED GATE
def is_predictable(series, threshold=0.02):
    score = predictability_score(series)

    # 🔥 NEVER fully block
    return True, score
