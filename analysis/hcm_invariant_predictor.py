import numpy as np


class HCMInvariantPredictor:

    def __init__(self, embed_dim=4, delay=2, k=10):
        self.embed_dim = embed_dim
        self.delay = delay
        self.k = k

    def embed(self, series):
        embedded = []
        for i in range(len(series) - self.delay * self.embed_dim):
            point = [
                series[i + j * self.delay]
                for j in range(self.embed_dim)
            ]
            embedded.append(point)
        return np.array(embedded)

    def normalize(self, x):
        return (x - np.mean(x)) / (np.std(x) + 1e-8)

    def fit(self, history):

        series = np.array(history)
        self.raw_series = series

        norm = self.normalize(series)

        self.series = norm
        self.embedded = self.embed(norm)

        # --- invariant scaling ---
        self.local_scale = np.std(norm[-100:]) + 1e-8

    def predict(self, history):

        if len(history) < 60:
            return history[-1]

        self.fit(history)

        if len(self.embedded) < self.k + 2:
            return history[-1]

        current = self.embedded[-1]

        # distance with weighting (geometry aware)
        weights = np.linspace(1.0, 2.0, self.embed_dim)
        dists = np.linalg.norm((self.embedded - current) * weights, axis=1)

        idx = np.argsort(dists)[1:self.k+1]

        X = self.embedded[idx]
        Y = self.embedded[idx + 1]

        # --- robust local mapping ---
        try:
            A, _, _, _ = np.linalg.lstsq(X, Y, rcond=None)
        except:
            return history[-1]

        next_state = current @ A

        # --- invariant projection ---
        pred = np.median(Y[:, -1])

        # combine both (structure + invariant)
        alpha = 0.7
        pred = alpha * pred + (1 - alpha) * next_state[-1]

        # denormalize using local invariant scale
        window = history[-100:]
        pred = pred * np.std(window) + np.mean(window)

        return float(pred)
