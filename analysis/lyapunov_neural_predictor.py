import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler


class LyapunovNeuralPredictor:

    def __init__(self, lag=5):
        self.lag = lag
        self.scaler = StandardScaler()
        self.model = MLPRegressor(
            hidden_layer_sizes=(32, 32),
            activation="tanh",
            solver="adam",
            max_iter=2000,
            random_state=42
        )

    def _embed(self, series):
        X, y = [], []

        for i in range(len(series) - self.lag - 1):
            X.append(series[i:i+self.lag])
            y.append(series[i+self.lag])

        return np.array(X), np.array(y)

    def fit(self, series):

        X, y = self._embed(series)

        Xs = self.scaler.fit_transform(X)

        self.model.fit(Xs, y)

    def predict(self, series):

        X, _ = self._embed(series)

        Xs = self.scaler.transform(X)

        return self.model.predict(Xs)


def estimate_lyapunov(series):

    diffs = np.abs(np.diff(series))

    diffs = diffs[diffs > 1e-8]

    if len(diffs) == 0:
        return 0

    return float(np.mean(np.log(diffs)))
