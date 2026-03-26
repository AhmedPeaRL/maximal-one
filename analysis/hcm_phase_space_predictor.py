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

        # nearest neighbor
        distances = np.linalg.norm(emb[:-1] - target, axis=1)
        idx = np.argmin(distances)

        # project forward
        if idx + 1 < len(series):
            return float(series[idx + 1])

        return history[-1]
