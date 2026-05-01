import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha

def predict_next_trend(series):
    series = np.asarray(series)
    
    alpha = estimate_alpha(series)
    
    if np.isnan(alpha):
        return None

    # simple rule:
    if alpha > 2:
        return "persistent_trend"
    elif alpha > 1:
        return "moderate_memory"
    else:
        return "random_like"

def evaluate_prediction(series, split_ratio=0.8):
    n = len(series)
    split = int(n * split_ratio)

    train = series[:split]
    test = series[split:]

    prediction = predict_next_trend(train)

    if prediction is None:
        return {"valid": False}

    # crude validation logic
    actual_variance = np.var(test)

    result = {
        "prediction": prediction,
        "variance": float(actual_variance),
        "valid": True
    }

    return result
