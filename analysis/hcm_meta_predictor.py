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

    def baseline(self, history):
        if len(history) < 20:
            return history[-1]

        try:
            model = AutoReg(history, lags=1, old_names=False).fit()
            pred = model.predict(start=len(history), end=len(history))
            return float(pred[0])
        except:
            return history[-1]

    def score_model_fast(self, history, model):

        if len(history) < 80:
            return 0.0

        errors = []

        indices = np.linspace(40, len(history) - 2, 25).astype(int)

        for i in indices:
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

    def select_best_prediction(self, history):

        scored_preds = []

        for m in self.models:
            try:
                pred = m.predict(history)
                if not np.isfinite(pred):
                    continue

                score = self.score_model_fast(history, m)
                scored_preds.append((score, pred))
            except:
                continue

        try:
            inv_pred = invariant_predict(history)
            if np.isfinite(inv_pred):
                scored_preds.append((0.6, inv_pred))  # 🔥 increased weight
        except:
            pass

        if len(scored_preds) == 0:
            return None

        best = max(scored_preds, key=lambda x: x[0])
        return best[1]

    def predict(self, history):

        base = self.baseline(history)

        structure_score = detect_structure(history)
        predictable, pred_score = is_predictable(history)

        best_pred = self.select_best_prediction(history)

        if best_pred is None:
            return base

        # 🔥 CRITICAL CHANGE: DO NOT KILL SIGNAL
        confidence = structure_score * (0.5 + 0.5 * pred_score)

        # 🔥 allow stronger activation
        activation = np.clip(confidence, 0.15, 0.95)

        return float((1 - activation) * base + activation * best_pred)
