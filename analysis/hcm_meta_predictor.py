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
    # CORE DECISION ENGINE (UPGRADED)
    # -----------------------------
    def predict(self, history):

        base = self.baseline(history)

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

        try:
            inv_p = invariant_predict(history)
            if np.isfinite(inv_p):
                preds.append(inv_p)
        except:
            pass

        if len(preds) == 0:
            return base

        hcm_pred = float(np.median(preds))

        # -----------------------------
        # 🔥 NEW LOGIC: NONLINEAR ACTIVATION
        # -----------------------------

        confidence = structure_score * pred_score

        # بدل ما نهرب → نزود HCM لما structure يبقى ضعيف
        nonlinear_boost = 1.0 - structure_score

        # دمج الاتنين
        activation = max(confidence, nonlinear_boost * 0.6)

        # clip آمن
        activation = min(0.85, activation)

        # -----------------------------
        # BLENDING
        # -----------------------------
        return float((1 - activation) * base + activation * hcm_pred)
