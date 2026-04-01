import numpy as np
from statsmodels.tsa.ar_model import AutoReg

from analysis.hcm_phase_space_predictor import HCMPhaseSpacePredictor
from analysis.hcm_structural_predictor import HCMStructuralPredictor
from analysis.invariant_projection_predictor import InvariantProjectionPredictor
from analysis.structure_detector import detect_structure


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
    # 🔥 FILTER BAD PREDICTIONS
    # -----------------------------
    def filter_preds(self, preds, history):
        preds = np.array(preds)

        if len(preds) == 0:
            return preds

        last = history[-1]
        std = np.std(history[-30:]) + 1e-8

        # ❗ remove extreme deviations
        mask = np.abs(preds - last) < 2 * std

        filtered = preds[mask]

        if len(filtered) == 0:
            return np.array([last])  # fallback

        return filtered

    # -----------------------------
    # 🔥 CONFIDENCE
    # -----------------------------
    def confidence(self, preds):
        if len(preds) < 2:
            return 0.0

        spread = np.std(preds)
        return float(np.exp(-spread))

    # -----------------------------
    # 🔥 MAIN
    # -----------------------------
    def predict(self, history):

    base = self.baseline(history)

    structure = detect_structure(history)

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

    preds = self.filter_preds(preds, history)

    preds = np.array(preds)

    hcm_pred = float(np.mean(preds))

    # -----------------------------
    # 🔥 direction agreement
    # -----------------------------
    directions = np.sign(preds - history[-1])
    agreement = np.mean(directions == np.sign(hcm_pred - history[-1]))

    # -----------------------------
    # 🔥 confidence
    # -----------------------------
    conf = self.confidence(preds)

    # -----------------------------
    # 🔥 structure factor
    # -----------------------------
    structure_factor = min(1.0, structure * 1.5)

    # -----------------------------
    # 🔥 improved alpha
    # -----------------------------
    alpha = min(0.7, conf * structure_factor * (0.5 + 0.5 * agreement))

    # -----------------------------
    # 🔥 micro edge boost
    # -----------------------------
    delta = hcm_pred - base
    if abs(delta) < np.std(history[-30:]) * 0.1:
        hcm_pred += delta * 0.5

    final = (1 - alpha) * base + alpha * hcm_pred

    # -----------------------------
    # 🔥 stability clamp
    # -----------------------------
    std = np.std(history[-30:]) + 1e-8
    final = np.clip(final, history[-1] - 1.5*std, history[-1] + 1.5*std)

    return float(final)
