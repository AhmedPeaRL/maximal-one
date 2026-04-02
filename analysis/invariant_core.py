import numpy as np

def invariant_features(series):

    x = np.array(series)

    if len(x) < 10:
        return np.array([0.0])

    # 🔥 distribution invariant
    mean = np.mean(x)
    std = np.std(x) + 1e-8

    norm = (x - mean) / std

    # 🔥 histogram signature
    hist, _ = np.histogram(norm, bins=20, density=True)

    # 🔥 spectral invariant (magnitude only)
    fft = np.fft.rfft(norm)
    mag = np.abs(fft)

    # 🔥 compress
    feat = np.concatenate([
        hist[:10],
        mag[:10]
    ])

    return feat


def invariant_predict(history):

    if len(history) < 20:
        return history[-1]

    feats = []

    for i in range(10, len(history)):
        feats.append(invariant_features(history[:i]))

    feats = np.array(feats)

    target = history[10:]

    try:
        from sklearn.linear_model import Ridge

        model = Ridge(alpha=1.0)
        model.fit(feats, target)

        pred_feat = invariant_features(history).reshape(1, -1)

        return float(model.predict(pred_feat)[0])

    except:
        return history[-1]
