import numpy as np

def select_best_model(preds, history):

    preds = np.array(preds)

    if len(preds) == 0:
        return history[-1]

    last = history[-1]

    # 🔥 deviation from last state
    diffs = np.abs(preds - last)

    # 🔥 stability (local consistency)
    stability = 1 / (diffs + 1e-8)

    # 🔥 temporal momentum (NEW)
    trend = np.mean(np.diff(history[-10:]))
    momentum_alignment = 1 / (np.abs(preds - (last + trend)) + 1e-8)

    # 🔥 curvature sensitivity (NEW)
    curvature = np.mean(np.abs(np.gradient(np.gradient(history[-15:]))))
    curvature_alignment = 1 / (np.abs(preds - (last + curvature)) + 1e-8)

    # 🔥 combine signals
    score = (
        0.4 * stability +
        0.3 * momentum_alignment +
        0.3 * curvature_alignment
    )

    # 🔥 normalize
    weights = score / np.sum(score)

    # 🔥 entropy awareness
    entropy = -np.sum(weights * np.log(weights + 1e-8))

    confidence = 1 / (1 + entropy)

    # 🔥 if uncertain → DO NOT collapse to persistence
    if confidence < 0.25:
        # 🔥 choose most structurally different prediction
        diversity = np.abs(preds - last)
        idx = np.argmax(diversity)
        return float(preds[idx])

    # 🔥 final weighted prediction
    return float(np.sum(preds * weights))
