import numpy as np

def structural_consensus(preds, history):

    preds = np.array(preds)

    if len(preds) == 0:
        return history[-1]

    last = history[-1]

    # 🔥 deviation awareness
    deviations = preds - last

    # 🔥 kill trivial predictions
    mask = np.abs(deviations) > 1e-6

    if np.sum(mask) > 0:
        preds = preds[mask]
        deviations = deviations[mask]

    # 🔥 if all trivial → force escape
    if len(preds) == 0:
        std = np.std(history[-20:])
        return float(last + np.sign(np.random.randn()) * std * 0.1)

    # 🔥 weight by magnitude (not closeness)
    weights = np.abs(deviations) + 1e-8
    weights /= np.sum(weights)

    pred = np.sum(preds * weights)

    return float(pred)
