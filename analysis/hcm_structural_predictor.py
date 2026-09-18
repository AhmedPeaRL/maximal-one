from __future__ import annotations
import numpy as np

class HCMStructuralPredictor:
    def __init__(
        self,
        delay=2,
        dim=4,
        k=8,
        theiler_window=None,
        ridge=1e-6,
    ):
        self.delay = int(delay)
        self.dim = int(dim)
        self.k = int(k)
        self.ridge = float(ridge)

        if self.delay < 1:
            raise ValueError("delay must be >= 1")

        if self.dim < 2:
            raise ValueError("dim must be >= 2")

        if self.k < 1:
            raise ValueError("k must be >= 1")

        if self.ridge < 0:
            raise ValueError("ridge must be >= 0")

        if theiler_window is None:
            theiler_window = self.dim * self.delay

        self.theiler_window = int(
            theiler_window
        )

        if self.theiler_window < 1:
            raise ValueError(
                "theiler_window must be >= 1"
            )

        self.last_status = "not_run"
        self.last_reason = None

    def _fail(self, reason):
        self.last_status = "failed"
        self.last_reason = reason
        return np.nan

    def embed(self, series):
        x = np.asarray(
            series,
            dtype=np.float64,
        )

        if x.ndim != 1:
            return None

        if not np.all(
            np.isfinite(x)
        ):
            return None

        required = (
            self.dim * self.delay + 1
        )

        if len(x) < required:
            return None

        X = []
        Y = []
        indices = []

        max_i = (
            len(x)
            - self.dim * self.delay
        )

        for i in range(max_i):

            X.append(
                [
                    x[
                        i + j * self.delay
                    ]
                    for j in range(
                        self.dim
                    )
                ]
            )

            Y.append(
                x[
                    i
                    +
                    self.dim * self.delay
                ]
            )

            indices.append(i)

        if not X:
            return None

        return (
            np.asarray(
                X,
                dtype=np.float64,
            ),
            np.asarray(
                Y,
                dtype=np.float64,
            ),
            np.asarray(
                indices,
                dtype=np.int64,
            ),
        )

    def predict(self, history):
        self.last_status = "running"
        self.last_reason = None

        series = np.asarray(
            history,
            dtype=np.float64,
        )

        if len(series) < max(
            50,
            self.dim * self.delay + 2,
        ):
            return self._fail(
                "insufficient_history"
            )

        if not np.all(
            np.isfinite(series)
        ):
            return self._fail(
                "nonfinite_history"
            )

        embedded = self.embed(
            series
        )

        if embedded is None:
            return self._fail(
                "embedding_failed"
            )

        X, Y, indices = embedded

        if len(X) < self.k:
            return self._fail(
                "insufficient_embedded_states"
            )

        query = np.asarray(
            [
                series[
                    -1 - i * self.delay
                ]
                for i in range(self.dim)
            ][::-1],
            dtype=np.float64,
        )

        if not np.all(
            np.isfinite(query)
        ):
            return self._fail(
                "nonfinite_query"
            )

        scales = np.std(
            X,
            axis=0,
        )

        if not np.all(
            np.isfinite(scales)
        ):
            return self._fail(
                "invalid_scales"
            )

        scales = np.where(
            scales < 1e-12,
            1.0,
            scales,
        )

        Xs = X / scales
        qs = query / scales

        distances = np.linalg.norm(
            Xs - qs,
            axis=1,
        )

        query_index = (
            len(series)
            - self.dim * self.delay
        )

        eligible = (
            np.isfinite(distances)
            &
            np.isfinite(Y)
            &
            (
                np.abs(
                    indices - query_index
                )
                >
                self.theiler_window
            )
        )

        if not np.any(eligible):
            return self._fail(
                "no_theiler_eligible_neighbors"
            )

        valid_indices = np.where(
            eligible
        )[0]

        k = min(
            self.k,
            len(valid_indices),
        )

        if k < 2:
            return self._fail(
                "insufficient_neighbors"
            )

        nearest = valid_indices[
            np.argsort(
                distances[
                    valid_indices
                ]
            )[:k]
        ]

        Xn = Xs[nearest]
        Yn = Y[nearest]

        A = np.column_stack(
            [
                Xn,
                np.ones(len(Xn)),
            ]
        )

        try:
            lhs = (
                A.T @ A
            )

            if self.ridge > 0:
                regularizer = (
                    np.eye(
                        lhs.shape[0],
                        dtype=np.float64,
                    )
                )

                # Do not regularize the intercept.
                regularizer[-1, -1] = 0.0

                lhs = (
                    lhs
                    +
                    self.ridge
                    *
                    regularizer
                )

            rhs = A.T @ Yn

            coeffs = np.linalg.solve(
                lhs,
                rhs,
            )

            prediction = float(
                np.dot(
                    qs,
                    coeffs[:-1],
                )
                +
                coeffs[-1]
            )

        except (
            np.linalg.LinAlgError,
            ValueError,
            FloatingPointError,
        ):
            return self._fail(
                "local_regression_failed"
            )

        if not np.isfinite(
            prediction
        ):
            return self._fail(
                "nonfinite_prediction"
            )

        self.last_status = "ok"

        return prediction
