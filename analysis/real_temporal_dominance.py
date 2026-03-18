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

    if n < 50:
        print("Too few samples — skipping temporal dominance")
    else:
        real = real[:n]
        model = model[:n]

        diff = real - model

        improvement = float(np.mean(diff))

        try:
            t, p = stats.ttest_1samp(diff, 0)
        except Exception as e:
            print("Stat test failed:", e)
            t, p = 0.0, 1.0

        result.update({
            "real_temporal_signal": bool(improvement > 0 and p < 1e-5),
            "improvement": float(improvement),
            "p_value": float(p),
            "n": int(n)
        })

# 🔒 enforce JSON-safe types بالكامل
result = json.loads(json.dumps(result))

(ART / "real_temporal.json").write_text(json.dumps(result, indent=2))

print("==== REAL TEMPORAL RESULT ====")
print(json.dumps(result, indent=2))
