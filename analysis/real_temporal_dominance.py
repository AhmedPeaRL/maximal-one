import json
import pathlib
import numpy as np
from scipy import stats

ART = pathlib.Path("artifacts")

def load_series(name):
    p = ART / name
    if p.exists():
        return np.array(json.loads(p.read_text()))
    return None

# نحاول نستخدم بيانات حقيقية من pipeline
real = load_series("real_series.json")
model = load_series("model_series.json")

result = {
    "real_temporal_signal": False,
    "improvement": 0.0,
    "p_value": 1.0,
    "n": 0
}

if real is not None and model is not None:
    n = min(len(real), len(model))
    real = real[:n]
    model = model[:n]

    diff = real - model

    improvement = float(np.mean(diff))
    t, p = stats.ttest_1samp(diff, 0)

    result.update({
        "real_temporal_signal": improvement > 0 and p < 1e-5,
        "improvement": improvement,
        "p_value": float(p),
        "n": n
    })

(ART / "real_temporal.json").write_text(json.dumps(result, indent=2))
print(result)
