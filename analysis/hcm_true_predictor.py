import numpy as np

class HCMTruePredictor:
    def __init__(self, k=5):
        self.k = k

    def fit(self, series):
        self.series = np.array(series)

    def predict(self, history):
        h = np.array(history)

        if len(h) < 10:
            return h[-1]

        # 🔥 embedding
        emb_dim = 3
        delay = 1

        X = []
        y = []

        for i in range(len(h) - emb_dim - delay):
            X.append(h[i:i+emb_dim])
            y.append(h[i+emb_dim])

        if len(X) < self.k:
            return h[-1]

        X = np.array(X)
        y = np.array(y)

        query = h[-emb_dim:]

        # 🔥 nearest neighbors
        dists = np.linalg.norm(X - query, axis=1)
        idx = np.argsort(dists)[:self.k]

        # 🔥 weighted prediction (مش average عادي)
        weights = 1 / (dists[idx] + 1e-8)
        weights /= weights.sum()

        pred = np.sum(weights * y[idx])

        # 🔥 ANTI-COLLAPSE: force deviation
        if abs(pred - h[-1]) < 1e-12:
            pred += np.std(h[-20:]) * 0.1

        return float(pred)
