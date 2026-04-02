import numpy as np
from statsmodels.tsa.ar_model import AutoReg

from analysis.hcm_phase_space_predictor import HCMPhaseSpacePredictor
from analysis.hcm_structural_predictor import HCMStructuralPredictor
from analysis.invariant_projection_predictor import InvariantProjectionPredictor
from analysis.structure_detector import detect_structure
from analysis.predictability_gate import is_predictable


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

        if len(preds) == 0:
            return base

        preds = np.array(preds)
        hcm_pred = float(np.median(preds))

        std = np.std(history[-30:]) + 1e-8

        deviation = abs(hcm_pred - base)

        # =============================
        # 🔥 REGIME SWITCH LOGIC
        # =============================

        # 🟢 LOW STRUCTURE → STAY BASELINE
        if structure_score < 0.1:
            return base

        # 🟡 WEAK PREDICTABILITY → CONSERVATIVE BLEND
        if not predictable:
            alpha = 0.2
            return float((1 - alpha) * base + alpha * hcm_pred)

        # 🔴 STRONG STRUCTURE → BREAK BASELINE HARD
        if structure_score > 0.3 and pred_score > 0.1:
            return hcm_pred

        # 🟠 MID ZONE → ADAPTIVE
        alpha = min(0.8, structure_score + pred_score)
        return float((1 - alpha) * base + alpha * hcm_pred)
