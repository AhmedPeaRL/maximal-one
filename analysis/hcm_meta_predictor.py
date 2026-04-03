import numpy as np
from statsmodels.tsa.ar_model import AutoReg

from analysis.hcm_phase_space_predictor import HCMPhaseSpacePredictor
from analysis.hcm_structural_predictor import HCMStructuralPredictor
from analysis.invariant_projection_predictor import InvariantProjectionPredictor
from analysis.structure_detector import detect_structure
from analysis.predictability_gate import is_predictable
from analysis.invariant_core import invariant_predict


class HCMMetaPredictor:

    def __init__(self):
        self.models = [
            HCMPhaseSpacePredictor(delay=2, dim=3),
            HCMStructuralPredictor(delay=2, dim=4),
            InvariantProjectionPredictor(),
        ]

    # -----------------------------
    # BASELINE
    # -----------------------------
    def baseline(self, history):
        if len(history) < 20:
            return history[-1]

        try:
            model = AutoReg(history, lags=1, old_names=False).fit()
            pred = model.predict(start=len(history), end=len(history))
            return float(pred[0])
        except:
            return history[-1]

    # -----------------------------
    # 🔥 MODEL SCORING (NEW)
    # -----------------------------
    def score_model(self, history, model):

        if len(history) < 60:
            return 0.0

        errors = []

        for i in range(40, len(history) - 1):
            sub_hist = history[:i]

            try:
                pred = model.predict(sub_hist)
                true = history[i]

                if np.isfinite(pred):
                    errors.append((pred - true) ** 2)
            except:
                continue

        if len(errors) == 0:
            return 0.0

        return 1.0 / (np.mean(errors) + 1e-8)

    # -----------------------------
    # 🔥 COMPETITIVE SELECTION
    # -----------------------------
    def select_best_prediction(self, history):

        scored_preds = []

        for m in self.models:
            try:
                pred = m.predict(history)
                if not np.isfinite(pred):
                    continue

                score = self.score_model(history, m)
                scored_preds.append((score, pred))
            except:
                continue

        # invariant model
        try:
            inv_pred = invariant_predict(history)
            if np.isfinite(inv_pred):
                score = self.score_model(history, self)
                scored_preds.append((score * 0.8, inv_pred))  # slight penalty
        except:
            pass

        if len(scored_preds) == 0:
            return None

        # 🔥 choose BEST, not average
        best = max(scored_preds, key=lambda x: x[0])
        return best[1]

    # -----------------------------
    # FINAL PREDICT
    # -----------------------------
    def predict(self, history):

        base = self.baseline(history)

        structure_score = detect_structure(history)
        predictable, pred_score = is_predictable(history)

        best_pred = self.select_best_prediction(history)

        if best_pred is None:
            return base

        # -----------------------------
        # SMART ACTIVATION
        # -----------------------------
        if not predictable:
            return base

        confidence = structure_score * pred_score

        activation = np.clip(confidence, 0.0, 0.85)

        return float((1 - activation) * base + activation * best_pred)
