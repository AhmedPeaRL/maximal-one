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
    # CONFIDENCE WEIGHTING
    # -----------------------------
    def confidence_weight(self, preds):
        if len(preds) < 2:
            return 0.0

        spread = np.std(preds)
        return float(np.exp(-spread))

    # -----------------------------
    # MAIN
    # -----------------------------
    def predict(self, history):

        base = self.baseline(history)

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

        # 🔥 بدل median فقط → weighted blend
        hcm_pred = float(np.mean(preds))

        std = np.std(history[-30:]) + 1e-8

        deviation = abs(hcm_pred - base)

        # 🔥 key idea:
        # سيب مساحة للنموذج يخرج بره baseline
        if deviation < 0.05 * std:
            # blend بدل collapse
            alpha = 0.3
            return float((1 - alpha) * base + alpha * hcm_pred)

        # 🔥 strong signal → خليه يسيطر
        if deviation > 0.2 * std:
            return hcm_pred

        # 🔥 منطقة وسط
        alpha = 0.6
        return float((1 - alpha) * base + alpha * hcm_pred)
