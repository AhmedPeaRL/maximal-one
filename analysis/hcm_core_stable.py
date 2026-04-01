import numpy as np

def stable_structure_signal(history):
    recent = np.array(history[-20:])
    
    drift = np.mean(np.diff(recent))
    volatility = np.std(recent)
    curvature = np.mean(np.abs(np.gradient(np.gradient(recent))))
    
    return drift, volatility, curvature


def invariant_anchor(history):
    return float(history[-1])


from analysis.hcm_attractor_predictor import HCMAttractorPredictor

_model = HCMAttractorPredictor(dim=4, delay=2, k=6)

def stable_predict(history):

    if len(history) < 50:
        return history[-1]

    try:
        _model.fit(history)
        return _model.predict(history)
    except:
        return history[-1]
