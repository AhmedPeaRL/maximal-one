import numpy as np

class HCMPhaseSpacePredictor:
    def __init__(self, delay=2, dim=3, k=5):
        self.delay = int(delay)
        self.dim = int(dim)
        self.k = int(k)

        if self.delay < 1:
            raise ValueError("delay must be >= 1")

        if self.dim < 2:
            raise ValueError("dim must be >= 2")

        if self.k < 1:
            raise ValueError("k must be >= 1")

    def reconstruct(self, series):
        """
        Delay-coordinate reconstruction.

        Each row contains:

            [x[i],
             x[i + delay],
             ...
             x[i + (dim-1)*delay]]

        The row is only considered predictive if its true next target
        x[i + dim*delay] exists.
        """
        x = np.asarray(series, dtype=np.float64)

        n = len(x)
        d = self.dim
        tau = self.delay

        required = d * tau + 1

        if n < required:
            return None

        states = []
        targets = []

        max_i = n - d * tau

        for i in range(max_i):
            state = [
                x[i + j * tau]
                for j in range(d)
            ]

            target = x[i + d * tau]

            states.append(state)
            targets.append(target)

        if not states:
            return None

        return (
            np.asarray(states, dtype=np.float64),
            np.asarray(targets, dtype=np.float64),
        )

    def predict(self, history):
        """
        One-step-ahead phase-space prediction.

        The target is explicitly aligned to the temporal future of the
        reconstructed state. No target value is taken from inside the
        state vector.
        """
        if len(history) < max(30, self.dim * self.delay + 2):
            return float(history[-1])

        series = np.asarray(history, dtype=np.float64)

        if not np.all(np.isfinite(series)):
            return float(history[-1])

        if np.std(series) < 1e-12:
            return float(history[-1])

        reconstructed = self.reconstruct(series)

        if reconstructed is None:
            return float(history[-1])

        states, targets = reconstructed

        if len(states) < 5:
            return float(history[-1])

        # Current state must correspond exactly to the latest observed
        # sample in history.
        query = np.asarray(
            [
                series[-1 - j * self.delay]
                for j in range(self.dim - 1, -1, -1)
            ],
            dtype=np.float64,
        )

        distances = np.linalg.norm(
            states - query,
            axis=1,
        )

        finite_mask = np.isfinite(distances) & np.isfinite(targets)

        if not np.any(finite_mask):
            return float(history[-1])

        distances = distances[finite_mask]
        targets = targets[finite_mask]

        k = min(self.k, len(distances))

        idxs = np.argsort(distances)[:k]

        nearest_distances = distances[idxs]
        future_vals = targets[idxs]

        if len(future_vals) == 0:
            return float(history[-1])

        weights = 1.0 / (nearest_distances + 1e-8)
        weight_sum = np.sum(weights)

        if not np.isfinite(weight_sum) or weight_sum <= 0:
            return float(history[-1])

        weights /= weight_sum

        base_pred = float(
            np.sum(future_vals * weights)
        )

        # Local trend diagnostics.
        recent = series[-10:]

        if len(recent) >= 2:
            trend = float(np.mean(np.diff(recent)))
            grad = float(np.mean(np.gradient(recent)))
        else:
            trend = 0.0
            grad = 0.0

        recent_noise = float(
            np.std(series[-20:])
        )

        if not np.isfinite(recent_noise):
            recent_noise = 0.0

        # Controlled local correction.
        deviation = base_pred - series[-1]

        if abs(deviation) < 1e-6:
            deviation = 0.0

        prediction = (
            base_pred
            + 0.2 * trend
            + 0.3 * grad
            + 0.5 * deviation
        )

        # Numerical safety only.
        # This is not a performance optimization.
        if not np.isfinite(prediction):
            return float(history[-1])

        return float(prediction)
