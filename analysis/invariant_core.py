import numpy as np

def invariant_features(series):

    x = np.array(series)

    if len(x) < 20:
        return np.zeros(20)

    # 🔥 normalize
    x = (x - np.mean(x)) / (np.std(x) + 1e-8)

    # -----------------------
    # distribution
    # -----------------------
    hist, _ = np.histogram(x, bins=10, density=True)

    # -----------------------
    # spectral magnitude
    # -----------------------
    fft = np.fft.rfft(x)
    mag = np.abs(fft)
    mag = mag[:10] / (np.sum(mag[:10]) + 1e-8)

    # -----------------------
    # autocorrelation (CRITICAL)
    # -----------------------
    ac = []
    for lag in range(1, 6):
        if len(x) > lag:
            ac.append(np.corrcoef(x[:-lag], x[lag:])[0,1])
        else:
            ac.append(0.0)

    ac = np.nan_to_num(ac)

    return np.concatenate([hist, mag, ac])


def invariant_predict(history):

    if len(history) < 30:
        return history[-1]

    feats = []
    targets = []

    for i in range(20, len(history)):
        feats.append(invariant_features(history[:i]))
        targets.append(history[i])

    feats = np.array(feats)
    targets = np.array(targets)

    try:
        from sklearn.linear_model import Ridge

        model = Ridge(alpha=50.0)
        model.fit(feats, targets)

        pred_feat = invariant_features(history).reshape(1, -1)

        return float(model.predict(pred_feat)[0])

    except:
        return history[-1]
