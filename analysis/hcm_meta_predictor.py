import numpy as np
from statsmodels.tsa.ar_model import AutoReg

from analysis.hcm_phase_space_predictor import HCMPhaseSpacePredictor
from analysis.hcm_structural_predictor import HCMStructuralPredictor
from analysis.invariant_projection_predictor import InvariantProjectionPredictor


class HCMMetaPredictor:

    def __init__(self):
        self.models = [
            HCMPhaseSpacePredictor(delay=2, dim=3),
            HCMStructuralPredictor(delay=2, dim=4),
            InvariantProjectionPredictor(),
        ]

    # -----------------------------
    # 🔥 BASELINE (ANCHOR)
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
    # 🔥 CONFIDENCE ESTIMATION
    # -----------------------------
    def confidence(self, preds):
        preds = np.array(preds)

        if len(preds) < 2:
            return 0.0

        spread = np.std(preds)
        return float(np.exp(-spread))  # أقل spread = ثقة أعلى

    # -----------------------------
    # 🔥 FINAL PREDICT
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

        conf = self.confidence(preds)

        hcm_pred = float(np.mean(preds))

        # 🔥 CONTROLLED BLENDING
        alpha = min(0.5, conf)  # عمره ما يطغى بالكامل

        final = (1 - alpha) * base + alpha * hcm_pred

        # 🔥 STABILITY CLAMP
        std = np.std(history[-30:])
        final = np.clip(final, history[-1] - 2*std, history[-1] + 2*std)

        return float(final)
