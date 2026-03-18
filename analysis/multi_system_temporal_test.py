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

systems = {
    "sunspots": ("sunspots_real.json", "sunspots_model.json"),
    "climate": ("climate_real.json", "climate_model.json"),
    "internet": ("internet_real.json", "internet_model.json"),
    "eeg": ("eeg_real.json", "eeg_model.json"),
}

results = {}

for name, (r_file, m_file) in systems.items():

    real = load_series(r_file)
    model = load_series(m_file)

    if real is None or model is None:
        continue

    n = min(len(real), len(model))

    if n < 200:
        continue

    real = real[:n]
    model = model[:n]

    diff = real - model

    improvement = float(np.mean(diff))
    t, p = stats.ttest_1samp(diff, 0)

    results[name] = {
        "improvement": float(improvement),
        "p_value": float(p),
        "n": int(n),
        "signal": bool(improvement > 0 and p < 1e-5)
    }

# 🔥 meta decision
signals = [v["signal"] for v in results.values()]
global_signal = sum(signals) >= 2

final = {
    "systems": results,
    "global_signal": bool(global_signal),
    "num_systems": len(results)
}

(ART / "multi_system_temporal.json").write_text(json.dumps(final, indent=2))

print("==== MULTI SYSTEM RESULT ====")
print(json.dumps(final, indent=2))
