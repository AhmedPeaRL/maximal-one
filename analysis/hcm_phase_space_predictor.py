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

        k = min(5, len(distances))
        idxs = np.argsort(distances)[:k]

        future_vals = []
        valid_distances = []

        for idx in idxs:
            if idx + 1 < len(series):
                future_vals.append(series[idx + 1])
                valid_distances.append(distances[idx])

        if not future_vals:
            return history[-1]

        future_vals = np.array(future_vals)
        valid_distances = np.array(valid_distances) + 1e-8

        # ✅ weights صح
        weights = 1 / valid_distances
        weights /= np.sum(weights)

        base_pred = float(np.sum(future_vals * weights))

        # ✅ trend component
        trend = np.mean(np.diff(history[-10:]))

        # ✅ noise stabilizer
        noise = np.std(history[-20:])
        stochastic = np.random.normal(0, 0.01 * noise)

        # 🔥 local causal gradient
        grad = np.mean(np.gradient(history[-10:]))

        # 🔥 phase-aware correction
        phase_signal = np.sin(history[-1]) * 0.05

        # 🔥 final composition
        return base_pred + 0.3 * trend + 0.2 * grad + phase_signal + stochastic
