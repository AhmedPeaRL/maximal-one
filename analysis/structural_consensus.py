import numpy as np

def structural_consensus(preds, history):
    
    preds = np.array(preds)

    if len(preds) == 0:
        return history[-1]

    # 🔥 local consistency test
    diffs = np.abs(preds - history[-1])

    # 🔥 structural stability score
    stability = 1 / (diffs + 1e-8)

    # 🔥 normalize
    weights = stability / np.sum(stability)

    # 🔥 entropy penalty (spread awareness)
    entropy = -np.sum(weights * np.log(weights + 1e-8))

    confidence = 1 / (1 + entropy)

    # 🔥 final decision
    pred = np.sum(preds * weights)

    # 🔥 blend with last state if uncertain
    if confidence < 0.3:
        return history[-1]

    return float(pred)
