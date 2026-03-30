import numpy as np

def extract_causal_features(history):
    h = np.array(history)

    if len(h) < 20:
        return {
            "trend": 0.0,
            "volatility": 0.0,
            "curvature": 0.0
        }

    trend = np.mean(np.diff(h[-10:]))

    volatility = np.std(h[-20:])

    curvature = np.mean(
        np.abs(np.gradient(np.gradient(h[-10:])))
    )

    return {
        "trend": trend,
        "volatility": volatility,
        "curvature": curvature
    }


def causal_invariant_predict(history):

    f = extract_causal_features(history)

    # 🔥 causal law (NOT fitting)
    prediction = (
        history[-1]
        + 0.6 * f["trend"]
        - 0.2 * f["curvature"]
    )

    # 🔥 stability constraint
    if abs(prediction - history[-1]) > 3 * f["volatility"]:
        prediction = history[-1]

    return float(prediction)
