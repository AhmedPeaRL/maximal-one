import numpy as np
from sklearn.neighbors import NearestNeighbors

class HCMAttractorPredictor:

    def __init__(self, dim=4, delay=2, k=6):
        self.dim = dim
        self.delay = delay
        self.k = k

    def embed(self, series):
        N = len(series) - self.delay * (self.dim - 1)
        if N <= 0:
            return None

        embedded = np.zeros((N, self.dim))

        for i in range(self.dim):
            embedded[:, i] = series[i*self.delay : i*self.delay + N]

        return embedded

    def fit(self, series):
        emb = self.embed(series)
        if emb is None:
            self.nn = None
            return

        self.emb = emb
        self.targets = series[self.delay*self.dim:]

        self.nn = NearestNeighbors(n_neighbors=self.k)
        self.nn.fit(emb)

    def predict(self, history):

        if self.nn is None or len(history) < self.delay * self.dim:
            return history[-1]

        vec = []

        for i in range(self.dim):
            vec.append(history[-1 - i*self.delay])

        vec = np.array(vec[::-1]).reshape(1, -1)

        distances, indices = self.nn.kneighbors(vec)

        neighbors = self.targets[indices[0]]

        weights = 1 / (distances[0] + 1e-8)
        weights /= np.sum(weights)

        return float(np.dot(weights, neighbors))
