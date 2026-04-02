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
    # CORE DECISION ENGINE
    # -----------------------------
    def predict(self, history):

        base = self.baseline(history)

        # 🔥 STRUCTURE DETECTION
        structure_score = detect_structure(history)

        predictable, pred_score = is_predictable(history)

        preds = []

        for m in self.models:
            try:
                p = m.predict(history)
                if np.isfinite(p):
                    preds.append(p)
            except:
                continue

        # 🔥 ADD INVARIANT MODEL
        try:
            inv_p = invariant_predict(history)
            if np.isfinite(inv_p):
                preds.append(inv_p)
        except:
            pass

        if len(preds) == 0:
            return base

        preds = np.array(preds)
        hcm_pred = float(np.median(preds))

        std = np.std(history[-30:]) + 1e-8

        deviation = abs(hcm_pred - base)

        # =============================
        # 🔥 REGIME SWITCH LOGIC
        # =============================

        # 🔥 ALWAYS USE HCM SIGNAL

        alpha = 0.3 + 0.5 * structure_score + 0.3 * pred_score
        alpha = max(0.2, min(0.95, alpha))

        return float((1 - alpha) * base + alpha * hcm_pred)
