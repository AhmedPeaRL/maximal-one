import numpy as np

class HCMDynamicalPredictor:

    def __init__(self, embed_dim=3, delay=2, k=8):
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

    def fit(self, history):
        series = np.array(history)

        series = (series - np.mean(series)) / (np.std(series) + 1e-8)

        self.series = series
        self.embedded = self.embed(series)

    def predict(self, history):

        if len(history) < 50:
            return history[-1]

        # --- smart caching ---
        if not hasattr(self, "_last_len") or self._last_len != len(history):
            self.fit(history)
            self._last_len = len(history)

        if len(self.embedded) < self.k + 2:
            return history[-1]

        current = self.embedded[-1]

        dists = np.linalg.norm(self.embedded - current, axis=1)
        idx = np.argsort(dists)[1:self.k+1]

        X = self.embedded[idx]
        Y = self.embedded[idx + 1]

        # --- local linear map ---
        try:
            A, _, _, _ = np.linalg.lstsq(X, Y, rcond=None)
        except:
            return history[-1]

        next_state = current @ A

        pred = next_state[-1]

        # denormalize
        window = history[-100:]
        pred = pred * np.std(window) + np.mean(window)

        return float(pred)
