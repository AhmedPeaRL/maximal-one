import numpy as np

from analysis.hcm_phase_space_predictor import HCMPhaseSpacePredictor
from analysis.hcm_structural_predictor import HCMStructuralPredictor
from analysis.invariant_projection_predictor import InvariantProjectionPredictor
from analysis.hcm_true_predictor import HCMTruePredictor
from analysis.structural_consensus import structural_consensus

class HCMMetaPredictor:

    def __init__(self):
        self.models = [
            HCMPhaseSpacePredictor(delay=2, dim=3),
            HCMStructuralPredictor(delay=2, dim=4),
            InvariantProjectionPredictor(),
        ]
        self.true_model = HCMTruePredictor()

    def predict(self, history):
       
        preds = []
        
        for m in self.models:
            try:
                p = m.predict(history)
                if np.isfinite(p):
                    preds.append(p)
            except:
                continue

        # 🔥 add true predictor (HIGH PRIORITY)
        try:
            self.true_model.fit(history)
            p_true = self.true_model.predict(history)
            preds.append(p_true * 1.2)  # boost
        except:
            pass

        if len(preds) == 0:
            return history[-1]

        # 🔥 force diversity
        preds = np.array(preds)

        if np.std(preds) < 1e-6:
            noise = np.std(history[-20:]) * 0.2
            preds = preds + np.random.randn(len(preds)) * noise

        return structural_consensus(preds, history)
