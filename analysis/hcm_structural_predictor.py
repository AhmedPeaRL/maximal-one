import numpy as np

class HCMStructuralPredictor:

    def __init__(self, delay=2, dim=4, k=8):
        self.delay = delay
        self.dim = dim
        self.k = k

    def embed(self, series):
        n = len(series)
        d = self.dim
        tau = self.delay

        if n < d * tau + 1:
            return None

        X = []
        Y = []

        for i in range(n - d * tau - 1):
            vec = [series[i + j * tau] for j in range(d)]
            target = series[i + d * tau]

            X.append(vec)
            Y.append(target)

        return np.array(X), np.array(Y)

    def predict(self, history):

        if len(history) < 50:
            return history[-1]

        series = np.array(history)

        data = self.embed(series)
        if data is None:
            return history[-1]

        X, Y = data

        query = np.array([series[-1 - i*self.delay] for i in range(self.dim)][::-1])

        # distance
        dists = np.linalg.norm(X - query, axis=1)

        idx = np.argsort(dists)[:self.k]

        Xn = X[idx]
        Yn = Y[idx]

        # 🔥 local linear regression (THE KEY)
        try:
            A = np.hstack([Xn, np.ones((len(Xn),1))])
            coeffs = np.linalg.lstsq(A, Yn, rcond=None)[0]

            pred = np.dot(query, coeffs[:-1]) + coeffs[-1]

        except:
            pred = np.mean(Yn)

        # 🔥 stability clamp
        std = np.std(series[-30:])
        return float(np.clip(pred, series[-1] - 3*std, series[-1] + 3*std))
