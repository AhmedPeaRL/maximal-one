import json
import numpy as np
from pathlib import Path

# === LOAD REPORT ===
report_path = Path("artifacts/canonical_report.json")

if not report_path.exists():
    raise RuntimeError("Missing canonical_report.json")

with open(report_path) as f:
    report = json.load(f)

alpha = report.get("spectral_profile", {}).get("estimated_alpha")
std = report.get("spectral_profile", {}).get("bootstrap_std")

if alpha is None or std is None:
    raise RuntimeError("Missing spectral data")

# === SAMPLE ===
np.random.seed(42)
samples = np.random.normal(loc=alpha, scale=std, size=10000)

# === STATS ===
result = {
    "alpha": float(alpha),
    "std": float(std),
    "min_sample": float(np.min(samples)),
    "max_sample": float(np.max(samples)),
    "mean": float(np.mean(samples)),
    "p5": float(np.percentile(samples, 5)),
    "p50": float(np.percentile(samples, 50)),
    "p95": float(np.percentile(samples, 95))
}

Path("artifacts").mkdir(exist_ok=True)

with open("artifacts/alpha_debug.json", "w") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=2))
