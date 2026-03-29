import numpy as np

def detect_structure(series):

    x = np.array(series)

    if len(x) < 50:
        return 0.0

    # autocorrelation decay
    autocorr = np.corrcoef(x[:-1], x[1:])[0,1]

    # entropy
    hist, _ = np.histogram(x, bins=20, density=True)
    hist = hist + 1e-8
    entropy = -np.sum(hist * np.log(hist))

    # variance stability
    var_ratio = np.std(x[-20:]) / (np.std(x[:20]) + 1e-8)

    score = (
        0.4 * abs(autocorr) +
        0.3 * (1 / (1 + entropy)) +
        0.3 * (1 / (1 + abs(var_ratio - 1)))
    )

    return float(score)
