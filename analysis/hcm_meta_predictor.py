import numpy as np

try:
    from statsmodels.tsa.ar_model import AutoReg
    HAS_STATSMODELS = True
except Exception:
    HAS_STATSMODELS = False

from analysis.hcm_phase_space_predictor import (
    HCMPhaseSpacePredictor,
)
from analysis.hcm_structural_predictor import (
    HCMStructuralPredictor,
)

class HCMMetaPredictor:
    def __init__(
        self,
        validation_points=8,
        minimum_history=60,
    ):
        self.validation_points = int(
            validation_points
        )

        self.minimum_history = int(
            minimum_history
        )

        self.models = [
            (
                "phase_space",
                HCMPhaseSpacePredictor(
                    delay=2,
                    dim=3,
                ),
            ),
            (
                "structural",
                HCMStructuralPredictor(
                    delay=2,
                    dim=4,
                ),
            ),
        ]

        self.last_diagnostics = {}

    # --------------------------------------------------
    # Baselines
    # --------------------------------------------------

    @staticmethod
    def persistence(history):
        return float(history[-1])

    @staticmethod
    def autoreg1(history):
        if (
            not HAS_STATSMODELS
            or len(history) < 20
        ):
            return None

        try:
            model = AutoReg(
                np.asarray(
                    history,
                    dtype=np.float64,
                ),
                lags=1,
                old_names=False,
            ).fit()

            pred = model.predict(
                start=len(history),
                end=len(history),
            )

            value = float(pred[0])

            if np.isfinite(value):
                return value

        except (
            ValueError,
            np.linalg.LinAlgError,
            FloatingPointError,
        ):
            pass

        return None

    # --------------------------------------------------
    # Candidate scoring
    # --------------------------------------------------

    def score_model(
        self,
        history,
        model,
    ):
        """
        Expanding-window validation inside the
        already observed history.

        Lower MSE is better.
        """

        n = len(history)

        if n < self.minimum_history:
            return np.nan

        start = max(
            40,
            n - self.validation_points - 1,
        )

        indices = list(
            range(start, n - 1)
        )

        errors = []

        for i in indices:

            sub_history = history[:i]

            try:
                pred = model(
                    sub_history
                )
            except Exception:
                continue

            if pred is None:
                continue

            if not np.isfinite(pred):
                continue

            true = float(
                history[i]
            )

            errors.append(
                (float(pred) - true) ** 2
            )

        if len(errors) < 4:
            return np.nan

        return float(
            np.mean(errors)
        )

    # --------------------------------------------------
    # Selection
    # --------------------------------------------------

    def select_best_prediction(
        self,
        history,
    ):

        candidates = []

        # Persistence baseline
        persistence_score = self.score_model(
            history,
            self.persistence,
        )

        persistence_pred = (
            self.persistence(history)
        )

        if np.isfinite(
            persistence_score
        ):
            candidates.append(
                (
                    persistence_score,
                    "persistence",
                    persistence_pred,
                )
            )

        # AR(1) baseline
        ar_score = self.score_model(
            history,
            self.autoreg1,
        )

        ar_pred = self.autoreg1(
            history
        )

        if (
            ar_pred is not None
            and np.isfinite(ar_score)
        ):
            candidates.append(
                (
                    ar_score,
                    "ar1",
                    ar_pred,
                )
            )

        # HCM candidates
        for name, model in self.models:
            def predictor(
                sub_history,
                m=model,
            ):
                return m.predict(
                    sub_history
                )

            score = self.score_model(
                history,
                predictor,
            )

            try:
                pred = model.predict(
                    history
                )
            except Exception:
                continue

            if (
                np.isfinite(score)
                and np.isfinite(pred)
            ):
                candidates.append(
                    (
                        score,
                        name,
                        float(pred),
                    )
                )

        if not candidates:
            self.last_diagnostics = {
                "selection": "none",
                "reason": "no_valid_candidate",
            }

            return float(
                history[-1]
            )

        # Lower validation MSE wins.
        candidates.sort(
            key=lambda item: item[0]
        )

        best_score, best_name, best_pred = (
            candidates[0]
        )

        self.last_diagnostics = {
            "selection": best_name,
            "validation_mse": float(
                best_score
            ),
            "candidate_count": len(
                candidates
            ),
            "candidates": [
                {
                    "name": name,
                    "validation_mse": float(score),
                }
                for score, name, _ in candidates
            ],
        }

        return float(best_pred)

    # --------------------------------------------------
    # Final prediction
    # --------------------------------------------------

    def predict(self, history):
        history = np.asarray(
            history,
            dtype=np.float64,
        )

        if len(history) == 0:
            raise ValueError(
                "history must not be empty"
            )

        if not np.all(
            np.isfinite(history)
        ):
            raise ValueError(
                "history contains non-finite values"
            )

        if len(history) < self.minimum_history:
            self.last_diagnostics = {
                "selection": "persistence",
                "reason": "insufficient_history",
            }

            return float(
                history[-1]
            )

        return self.select_best_prediction(
            history
        )
