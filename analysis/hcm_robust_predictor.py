import numpy as np

class HCMRobustPredictor:

    def __init__(self, embed_dim=5, delay=2, k=12):
        self.embed_dim = embed_dim
        self.delay = delay
        self.k = k

    # -----------------------------
    # Invariant preprocessing
    # -----------------------------

    def normalize(self, x):
        return (x - np.mean(x)) / (np.std(x) + 1e-8)

    def detrend(self, x):
        t = np.arange(len(x))
        coeffs = np.polyfit(t, x, 1)
        trend = coeffs[0]*t + coeffs[1]
        return x - trend

    def robust_transform(self, series):
        s = self.detrend(series)
        s = self.normalize(s)

        # rank transform (very powerful ضد noise)
        ranks = np.argsort(np.argsort(s))
        return ranks / len(ranks)

    # -----------------------------
    # Embedding
    # -----------------------------

    def embed(self, series):
        emb = []
        for i in range(len(series) - self.delay * self.embed_dim):
            emb.append([
                series[i + j*self.delay]
                for j in range(self.embed_dim)
            ])
        return np.array(emb)

    # -----------------------------
    # Fit
    # -----------------------------

    def fit(self, history):
        series = np.array(history)

        transformed = self.robust_transform(series)

        self.series = transformed
        self.embedded = self.embed(transformed)

    # -----------------------------
    # Predict
    # -----------------------------

    def predict(self, history):

        if len(history) < 80:
            return history[-1]

        self.fit(history)

        if len(self.embedded) < self.k + 2:
            return history[-1]

        base = self.embedded[:-1]
        target = self.embedded[1:]
        current = self.embedded[-1]

        # robust distance (L1 بدل L2)
        dists = np.sum(np.abs(base - current), axis=1)

        idx = np.argsort(dists)[:self.k]

        X = base[idx]
        Y = target[idx]

        # median prediction (robust جدًا)
        pred = np.median(Y[:, -1])

        # map back to original scale
        window = np.array(history[-100:])
        pred = pred * np.std(window) + np.mean(window)

        return float(pred)
