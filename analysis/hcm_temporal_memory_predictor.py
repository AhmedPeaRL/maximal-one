import numpy as np

class HCMTemporalMemoryPredictor:
    """
    True temporal memory model:
    - builds trajectory memory
    - retrieves nearest past states
    - projects forward
    """

    def __init__(self, window=50, k=5):
        self.window = window
        self.k = k

    def predict(self, history):

        if len(history) < self.window * 2:
            return history[-1]

        x = np.array(history)

        # build trajectories
        patterns = []
        targets = []

        for i in range(len(x) - self.window - 1):
            patterns.append(x[i:i+self.window])
            targets.append(x[i+self.window])

        patterns = np.array(patterns)
        targets = np.array(targets)

        current = x[-self.window:]

        # nearest neighbors
        dists = np.linalg.norm(patterns - current, axis=1)

        idx = np.argsort(dists)[:self.k]

        pred = np.mean(targets[idx])

        return float(pred)
