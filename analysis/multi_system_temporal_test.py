import json
import pathlib
import numpy as np

ART = pathlib.Path("artifacts")

def load_series(name):
    p = ART / name
    if p.exists():
        return np.array(json.loads(p.read_text()))
    return None

def autocorr(x, lag=1):
    return np.corrcoef(x[:-lag], x[lag:])[0, 1]

def autocorr_profile(x, max_lag=50):
    return np.array([autocorr(x, lag) for lag in range(1, max_lag)])

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

    if n < 500:
        continue

    real = real[:n]
    model = model[:n]

    ac_real = autocorr_profile(real)
    ac_model = autocorr_profile(model)

    # 🔥 الفرق الحقيقي
    diff = np.abs(ac_real) - np.abs(ac_model)

    score = float(np.mean(diff))

    results[name] = {
        "temporal_score": score,
        "signal": bool(score > 0.01)
    }

signals = [v["signal"] for v in results.values()]
global_signal = sum(signals) >= 1

final = {
    "systems": results,
    "global_signal": bool(global_signal),
    "num_systems": len(results)
}

(ART / "multi_system_temporal.json").write_text(json.dumps(final, indent=2))

print("==== MULTI SYSTEM RESULT ====")
print(json.dumps(final, indent=2))
