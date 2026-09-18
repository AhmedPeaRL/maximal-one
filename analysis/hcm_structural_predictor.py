import numpy as np

class HCMStructuralPredictor:
    def __init__(
        self,
        delay=2,
        dim=4,
        k=8,
        theiler_window=None,
    ):
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

    def embed(self, series):
        x = np.asarray(series, dtype=np.float64)

        if x.ndim != 1:
            return None

        if not np.all(np.isfinite(x)):
            return None

        n = len(x)
        d = self.dim
        tau = self.delay

        if n < d * tau + 1:
            return None

        X = []
        Y = []
        indices = []

        max_i = n - d * tau

        for i in range(max_i):

            X.append([
                x[i + j * tau]
                for j in range(d)
            ])

            Y.append(
                x[i + d * tau]
            )

            indices.append(i)

        if not X:
            return None

        return (
            np.asarray(X, dtype=np.float64),
            np.asarray(Y, dtype=np.float64),
            np.asarray(indices, dtype=np.int64),
        )

    def predict(self, history):
        series = np.asarray(history, dtype=np.float64)

        if len(series) < 50:
            return float(series[-1])

        if not np.all(np.isfinite(series)):
            return float(series[-1])

        data = self.embed(series)

        if data is None:
            return float(series[-1])

        X, Y, indices = data

        query = np.asarray(
            [
                series[-1 - i * self.delay]
                for i in range(self.dim)
            ][::-1],
            dtype=np.float64,
        )

        if len(X) < 3:
            return float(series[-1])

        scales = np.std(X, axis=0)

        if not np.all(np.isfinite(scales)):
            return float(series[-1])

        scales = np.where(
            scales < 1e-12,
            1.0,
            scales,
        )

        X_scaled = X / scales
        query_scaled = query / scales

        dists = np.linalg.norm(
            X_scaled - query_scaled,
            axis=1,
        )

        query_start = len(series) - self.dim * self.delay

        eligible = (
            np.isfinite(dists)
            & np.isfinite(Y)
            & (
                np.abs(indices - query_start)
                > self.theiler_window
            )
        )

        if not np.any(eligible):
            return float(series[-1])

        valid_indices = np.where(eligible)[0]

        k = min(
            self.k,
            len(valid_indices),
        )

        nearest = valid_indices[
            np.argsort(
                dists[valid_indices]
            )[:k]
        ]

        Xn = X[nearest]
        Yn = Y[nearest]

        if len(Yn) < 2:
            return float(Yn[0])

        try:
            A = np.hstack([
                Xn,
                np.ones(
                    (len(Xn), 1),
                    dtype=np.float64,
                ),
            ])

            coeffs = np.linalg.lstsq(
                A,
                Yn,
                rcond=None,
            )[0]

            pred = (
                np.dot(
                    query,
                    coeffs[:-1],
                )
                + coeffs[-1]
            )

        except (np.linalg.LinAlgError, ValueError, FloatingPointError):
            return float(series[-1])

        if not np.isfinite(pred):
            return float(series[-1])

        return float(pred)
