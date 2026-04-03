import numpy as np

def invariant_features(series):

    x = np.array(series)

    if len(x) < 30:
        return np.zeros(30)

    # normalize
    x = (x - np.mean(x)) / (np.std(x) + 1e-8)

    feats = []

    # -----------------------
    # 1. distribution
    # -----------------------
    hist, _ = np.histogram(x, bins=12, density=True)
    feats.extend(hist)

    # -----------------------
    # 2. spectral (extended)
    # -----------------------
    fft = np.fft.rfft(x)
    mag = np.abs(fft)
    mag = mag[:15] / (np.sum(mag[:15]) + 1e-8)
    feats.extend(mag)

    # -----------------------
    # 3. autocorrelation
    # -----------------------
    for lag in range(1, 8):
        if len(x) > lag:
            feats.append(np.corrcoef(x[:-lag], x[lag:])[0,1])
        else:
            feats.append(0.0)

    # -----------------------
    # 🔥 4. nonlinear curvature (CRITICAL)
    # -----------------------
    dx = np.diff(x)
    ddx = np.diff(dx)

    curvature = np.mean(np.abs(ddx))
    feats.append(curvature)

    # -----------------------
    # 🔥 5. local energy bursts
    # -----------------------
    window = 10
    energies = []

    for i in range(len(x) - window):
        segment = x[i:i+window]
        energies.append(np.var(segment))

    if energies:
        feats.append(np.mean(energies))
        feats.append(np.std(energies))
    else:
        feats.extend([0.0, 0.0])

    # -----------------------
    # 🔥 6. nonlinear mixing indicator
    # -----------------------
    nonlinear_mix = np.mean(np.tanh(x) * x)
    feats.append(nonlinear_mix)

    # -----------------------
    # 🔥 7. recurrence density
    # -----------------------
    threshold = 0.5
    rec = np.abs(x[:, None] - x[None, :]) < threshold
    feats.append(np.mean(rec))

    return np.nan_to_num(np.array(feats))


def invariant_predict(history):

    if len(history) < 40:
        return history[-1]

    feats = []
    targets = []

    for i in range(30, len(history)):
        feats.append(invariant_features(history[:i]))
        targets.append(history[i])

    feats = np.array(feats)
    targets = np.array(targets)

    try:
        from sklearn.linear_model import Ridge

        # 🔥 stronger model
        model = Ridge(alpha=10.0)
        model.fit(feats, targets)

        pred_feat = invariant_features(history).reshape(1, -1)
        feats = np.clip(feats, -5, 5)
        
        return float(model.predict(pred_feat)[0])
        
    except:
        return history[-1]
