import numpy as np

def select_best_model(preds, history):

    preds = np.array(preds)

    if len(preds) == 0:
        return history[-1]

    last = history[-1]

    diffs = np.abs(preds - last)

    # 🔥 بدل ما نقرب من last → نعاقب القرب الشديد
    anti_persistence = diffs + 1e-8

    trend = np.mean(np.diff(history[-10:]))

    momentum_alignment = 1 / (np.abs(preds - (last + trend)) + 1e-8)

    curvature = np.mean(np.abs(np.gradient(np.gradient(history[-15:]))))
    curvature_alignment = 1 / (np.abs(preds - (last + curvature)) + 1e-8)

    score = (
        0.5 * anti_persistence +   # 🔥 قلبناها
        0.3 * momentum_alignment +
        0.2 * curvature_alignment
    )

    weights = score / np.sum(score)

    entropy = -np.sum(weights * np.log(weights + 1e-8))
    confidence = 1 / (1 + entropy)

    # 🔥 لو uncertainty عالي → forced divergence
    if confidence < 0.3:

        spread = np.std(preds)

        exploration = preds + np.random.normal(0, spread * 0.3, size=len(preds))

        idx = np.argmax(np.abs(exploration - last))
        return float(exploration[idx])

    return float(np.sum(preds * weights))
