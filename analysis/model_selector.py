import numpy as np

def select_best_model(preds, history):
    
    preds = np.array(preds)
    
    if len(preds) == 0:
        return history[-1]

    last = history[-1]

    # 🔥 deviation from last state
    diffs = np.abs(preds - last)

    # 🔥 stability score (lower diff = more stable)
    stability = 1 / (diffs + 1e-8)

    # 🔥 sharpness (variance awareness)
    spread = np.std(preds)

    # 🔥 dominance rule
    best_idx = np.argmax(stability)

    best_pred = preds[best_idx]

    # 🔥 if spread is high → trust strongest model only
    if spread > np.std(history[-20:]):
        return float(best_pred)

    # 🔥 otherwise blend lightly
    weights = stability / np.sum(stability)
    return float(np.sum(preds * weights))
