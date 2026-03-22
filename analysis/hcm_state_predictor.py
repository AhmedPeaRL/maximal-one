import numpy as np


class HCMStatePredictor:
    """
    HCM Phase-Space Aware Predictor
    - builds embedding
    - tracks nearest states
    - predicts via local attractor dynamics
    """

    def __init__(self, embed_dim=3, delay=2, k=5):
        self.embed_dim = embed_dim
        self.delay = delay
        self.k = k

    def embed(self, series):
        N = len(series)
        M = N - (self.embed_dim - 1) * self.delay

        if M <= 0:
            return None

        X = np.zeros((M, self.embed_dim))

        for i in range(self.embed_dim):
            X[:, i] = series[i * self.delay:i * self.delay + M]

        return X

    def fit(self, series):
        self.series = np.array(series)
        self.embedded = self.embed(self.series)

    def predict(self, history):

        if len(history) < (self.embed_dim * self.delay):
            return history[-1]

        emb = self.embed(np.array(history))

        if emb is None or len(emb) < self.k:
            return history[-1]

        current = emb[-1]

        distances = np.linalg.norm(emb[:-1] - current, axis=1)

        idx = np.argsort(distances)[:self.k]

        future_vals = []

        for i in idx:
            if i + 1 < len(self.series):
                future_vals.append(self.series[i + 1])

        if len(future_vals) == 0:
            return history[-1]

        return float(np.mean(future_vals))
