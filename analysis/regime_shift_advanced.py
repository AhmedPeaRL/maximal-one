import numpy as np

def detect_regime_shift_advanced(signal, window=20, z_thresh=2.5):
    x = np.array(signal)

    if len(x) < window * 3:
        return []

    shifts = []

    global_std = np.std(x) + 1e-8

    for i in range(window, len(x) - window):

        past = x[i-window:i]
        future = x[i:i+window]

        past_mean = np.mean(past)
        future_mean = np.mean(future)

        past_std = np.std(past)
        future_std = np.std(future)

        # 🔥 multi-factor score
        mean_shift = abs(future_mean - past_mean)
        variance_shift = abs(future_std - past_std)

        # 🔥 curvature change
        dx = np.gradient(x[i-window:i+window])
        curvature = np.mean(np.abs(np.gradient(dx)))

        score = (mean_shift + variance_shift + curvature) / global_std

        if score > z_thresh:
            shifts.append({
                "index": int(i),
                "score": float(score),
                "mean_shift": float(mean_shift),
                "variance_shift": float(variance_shift),
                "curvature": float(curvature)
            })

    return shifts
