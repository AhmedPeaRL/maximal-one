from __future__ import annotations
import numpy as np

class HCMPhaseSpacePredictor:
    def __init__(
        self,
        delay=2,
        dim=3,
        k=5,
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

    def reconstruct(self, series):
        x = np.asarray(
            series,
            dtype=np.float64,
        )

        if x.ndim != 1:
            return None

        if not np.all(np.isfinite(x)):
            return None

        n = len(x)
        required = (
            self.dim * self.delay + 1
        )

        if n < required:
            return None

        states = []
        targets = []
        indices = []

        max_i = n - self.dim * self.delay

        for i in range(max_i):

            state = [
                x[i + j * self.delay]
                for j in range(self.dim)
            ]

            target = x[
                i + self.dim * self.delay
            ]

            states.append(state)
            targets.append(target)
            indices.append(i)

        if not states:
            return None

        return (
            np.asarray(
                states,
                dtype=np.float64,
            ),
            np.asarray(
                targets,
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
            30,
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

        std = np.std(series)

        if not np.isfinite(std) or std < 1e-12:
            return self._fail(
                "degenerate_history"
            )

        reconstructed = self.reconstruct(
            series
        )

        if reconstructed is None:
            return self._fail(
                "reconstruction_failed"
            )

        states, targets, indices = (
            reconstructed
        )

        if len(states) < self.k:
            return self._fail(
                "insufficient_states"
            )

        query = np.asarray(
            [
                series[
                    -1 - j * self.delay
                ]
                for j in range(
                    self.dim - 1,
                    -1,
                    -1,
                )
            ],
            dtype=np.float64,
        )

        if not np.all(
            np.isfinite(query)
        ):
            return self._fail(
                "nonfinite_query"
            )

        scales = np.std(
            states,
            axis=0,
        )

        if not np.all(
            np.isfinite(scales)
        ):
            return self._fail(
                "invalid_state_scales"
            )

        scales = np.where(
            scales < 1e-12,
            1.0,
            scales,
        )

        states_scaled = states / scales
        query_scaled = query / scales

        distances = np.linalg.norm(
            states_scaled - query_scaled,
            axis=1,
        )

        query_index = (
            len(series)
            - self.dim * self.delay
        )

        eligible = (
            np.isfinite(distances)
            &
            np.isfinite(targets)
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

        valid_distances = (
            distances[eligible]
        )

        valid_targets = (
            targets[eligible]
        )

        k = min(
            self.k,
            len(valid_distances),
        )

        if k < 1:
            return self._fail(
                "no_valid_neighbors"
            )

        nearest = np.argsort(
            valid_distances
        )[:k]

        nearest_distances = (
            valid_distances[nearest]
        )

        nearest_targets = (
            valid_targets[nearest]
        )

        zero = (
            nearest_distances <= 1e-12
        )

        if np.any(zero):
            prediction = float(
                np.mean(
                    nearest_targets[zero]
                )
            )
        else:
            weights = (
                1.0
                /
                nearest_distances
            )

            weight_sum = np.sum(
                weights
            )

            if (
                not np.isfinite(weight_sum)
                or
                weight_sum <= 0
            ):
                return self._fail(
                    "invalid_neighbor_weights"
                )

            weights /= weight_sum

            prediction = float(
                np.sum(
                    nearest_targets
                    *
                    weights
                )
            )

        if not np.isfinite(
            prediction
        ):
            return self._fail(
                "nonfinite_prediction"
            )

        self.last_status = "ok"

        return prediction
