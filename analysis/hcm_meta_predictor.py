from __future__ import annotations
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

    @staticmethod
    def persistence(history):
        if len(history) == 0:
            return np.nan

        return float(history[-1])

    @staticmethod
    def autoreg1(history):

        if (
            not HAS_STATSMODELS
            or len(history) < 20
        ):
            return np.nan

        try:
            model = AutoReg(
                np.asarray(
                    history,
                    dtype=np.float64,
                ),
                lags=1,
                old_names=False,
            ).fit()

            prediction = float(
                model.predict(
                    start=len(history),
                    end=len(history),
                )[0]
            )

            if np.isfinite(
                prediction
            ):
                return prediction

        except (
            ValueError,
            np.linalg.LinAlgError,
            FloatingPointError,
        ):
            pass

        return np.nan

    def score_model(
        self,
        history,
        predictor,
    ):
        n = len(history)

        if n < self.minimum_history:
            return np.nan

        start = max(
            40,
            n
            -
            self.validation_points
            -
            1,
        )

        errors = []

        for i in range(
            start,
            n - 1,
        ):
            sub_history = history[:i]

            try:
                prediction = predictor(
                    sub_history
                )
            except Exception:
                continue

            if prediction is None:
                continue

            if not np.isfinite(
                prediction
            ):
                continue

            truth = float(
                history[i]
            )

            errors.append(
                (
                    float(prediction)
                    -
                    truth
                ) ** 2
            )

        if len(errors) < 4:
            return np.nan

        return float(
            np.mean(errors)
        )

    def select_best_prediction(
        self,
        history,
    ):
        candidates = []

        candidate_failures = []

        baseline_models = [
            (
                "persistence",
                self.persistence,
            ),
            (
                "ar1",
                self.autoreg1,
            ),
        ]

        for name, predictor in (
            baseline_models
        ):
            score = self.score_model(
                history,
                predictor,
            )

            try:
                prediction = predictor(
                    history
                )
            except Exception:
                prediction = np.nan

            if (
                np.isfinite(score)
                and
                np.isfinite(prediction)
            ):
                candidates.append(
                    (
                        float(score),
                        name,
                        float(prediction),
                    )
                )
            else:
                candidate_failures.append(
                    name
                )

        for name, model in self.models:
            def predictor(
                sub_history,
                current_model=model,
            ):
                return current_model.predict(
                    sub_history
                )

            score = self.score_model(
                history,
                predictor,
            )

            try:
                prediction = model.predict(
                    history
                )
            except Exception:
                prediction = np.nan

            if (
                np.isfinite(score)
                and
                np.isfinite(prediction)
            ):
                candidates.append(
                    (
                        float(score),
                        name,
                        float(prediction),
                    )
                )
            else:
                candidate_failures.append(
                    name
                )

        if not candidates:
            self.last_diagnostics = {
                "selection": None,
                "status": "failed",
                "reason": "no_valid_candidate",
                "candidate_failures": (
                    candidate_failures
                ),
            }

            return np.nan

        candidates.sort(
            key=lambda item: (
                item[0],
                item[1],
            )
        )

        best_score, best_name, best_prediction = (
            candidates[0]
        )

        self.last_diagnostics = {
            "selection": best_name,
            "status": "ok",
            "selected_prediction": float(
                best_prediction
            ),
            "validation_mse": float(
                best_score
            ),
            "candidate_count": len(
                candidates
            ),
            "candidate_failures": (
                candidate_failures
            ),
            "candidates": [
                {
                    "name": name,
                    "validation_mse": float(
                        score
                    ),
                }
                for score, name, _ in candidates
            ],
            "selection_basis": (
                "lowest_expanding_origin_validation_mse"
            ),
            "hcm_selected": bool(
                best_name
                in {
                    "phase_space",
                    "structural",
                }
            ),
        }

        return float(
            best_prediction
        )

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
                "selection": None,
                "status": "not_evaluable",
                "reason": "insufficient_history",
            }

            return np.nan

        return self.select_best_prediction(
            history
        )
