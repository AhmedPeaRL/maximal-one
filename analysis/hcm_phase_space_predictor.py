import numpy as np

class HCMPhaseSpacePredictor:

    def __init__(self, delay=2, dim=3):
        self.delay = delay
        self.dim = dim

    def reconstruct(self, series):
        n = len(series)
        d = self.dim
        tau = self.delay

        if n < d * tau:
            return None

        embedded = []
        for i in range(n - d * tau):
            point = [series[i + j * tau] for j in range(d)]
            embedded.append(point)

        return np.array(embedded)

    def predict(self, history):
        if len(history) < 30:
            return history[-1]

    series = np.array(history)

    emb = self.reconstruct(series)
   
    if emb is None or len(emb) < 5:
        return history[-1]

    target = emb[-1]

    distances = np.linalg.norm(emb[:-1] - target, axis=1)

    # 🔥 NEW: take k-nearest instead of 1
    k = min(5, len(distances))
    idxs = np.argsort(distances)[:k]

    future_vals = []
    for idx in idxs:
        if idx + 1 < len(series):
            future_vals.append(series[idx + 1])

    if not future_vals:
        return history[-1]

    # 🔥 weighted average (closer = stronger)
    d = distances[idxs] + 1e-8
    weights = 1 / d
    weights /= np.sum(weights)

    return float(np.sum(np.array(future_vals) * weights))
