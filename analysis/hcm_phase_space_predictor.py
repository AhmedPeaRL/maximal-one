import numpy as np

class HCMPhaseSpacePredictor:
    def __init__(self, delay=2, dim=3, k=5, theiler_window=None):
        self.delay = int(delay)
        self.dim = int(dim)
        self.k = int(k)

        if self.delay < 1:
            raise ValueError("delay must be >= 1")

        if self.dim < 2:
            raise ValueError("dim must be >= 2")

        if self.k < 1:
            raise ValueError("k must be >= 1")

        if theiler_window is None:
            theiler_window = self.dim * self.delay

        self.theiler_window = int(theiler_window)

        if self.theiler_window < 1:
            raise ValueError("theiler_window must be >= 1")

    def reconstruct(self, series):
        x = np.asarray(series, dtype=np.float64)

        if x.ndim != 1:
            raise ValueError("series must be one-dimensional")

        if not np.all(np.isfinite(x)):
            return None

        n = len(x)
        d = self.dim
        tau = self.delay

        required = d * tau + 1

        if n < required:
            return None

        states = []
        targets = []
        indices = []

        max_i = n - d * tau

        for i in range(max_i):
            state = [
                x[i + j * tau]
                for j in range(d)
            ]

            target = x[i + d * tau]

            states.append(state)
            targets.append(target)
            indices.append(i)

        if not states:
            return None

        return (
            np.asarray(states, dtype=np.float64),
            np.asarray(targets, dtype=np.float64),
            np.asarray(indices, dtype=np.int64),
        )

    def predict(self, history):
        series = np.asarray(history, dtype=np.float64)

        if len(series) < max(
            30,
            self.dim * self.delay + 2,
        ):
            return float(series[-1])

        if not np.all(np.isfinite(series)):
            return float(series[-1])

        if np.std(series) < 1e-12:
            return float(series[-1])

        reconstructed = self.reconstruct(series)

        if reconstructed is None:
            return float(series[-1])

        states, targets, indices = reconstructed

        if len(states) < 5:
            return float(series[-1])

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

        finite = (
            np.isfinite(distances)
            & np.isfinite(targets)
        )

        # Theiler exclusion:
        # do not use training states temporally adjacent
        # to the query state.
        query_start = len(series) - self.dim * self.delay

        eligible = (
            finite
            & (
                np.abs(indices - query_start)
                > self.theiler_window
            )
        )

        if not np.any(eligible):
            return float(series[-1])

        valid_distances = distances[eligible]
        valid_targets = targets[eligible]

        k = min(self.k, len(valid_distances))

        if k < 1:
            return float(series[-1])

        nearest = np.argsort(valid_distances)[:k]

        nearest_distances = valid_distances[nearest]
        future_values = valid_targets[nearest]

        if len(future_values) == 0:
            return float(series[-1])

        # Explicit exact-match handling.
        zero = nearest_distances <= 1e-12

        if np.any(zero):
            prediction = float(
                np.mean(future_values[zero])
            )
        else:
            weights = 1.0 / nearest_distances
            weight_sum = np.sum(weights)

            if (
                not np.isfinite(weight_sum)
                or weight_sum <= 0
            ):
                return float(series[-1])

            weights /= weight_sum

            prediction = float(
                np.sum(
                    future_values * weights
                )
            )

        if not np.isfinite(prediction):
            return float(series[-1])

        return prediction
