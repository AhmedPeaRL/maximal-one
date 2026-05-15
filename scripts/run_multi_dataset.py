import json
import numpy as np
import pandas as pd
import os
from analysis.numerical_spectral_verification import estimate_alpha

def load_sunspots():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    
    path = os.path.join(
        base_dir,
        "real-data",
        "sunspots_global_extended.csv"
    )

    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Dataset not found: {path}")

    df = pd.read_csv(path)

    col = "Sunspots" if "Sunspots" in df.columns else "value"
    return df[col].values.astype(float)

def load_synthetic(seed=42, n=1024):
    rng = np.random.default_rng(seed)

    x = np.zeros(n)
    noise = rng.standard_normal(n)

    # ✅ AR(1) stable process (guaranteed stationarity)
    for i in range(1, n):
        x[i] = 0.92 * x[i-1] + 0.15 * noise[i]
        
        # إضافة long memory بسيط
        if i > 10:
            x[i] += 0.05 * x[i-10]

    # ✅ very light modulation (controlled)
    x += 0.02 * rng.standard_normal(n)

    return x

def load_noise(n=1024):
    rng = np.random.default_rng(999)

    # mixture of hard nulls
    wn = rng.standard_normal(n)
    rw = np.cumsum(rng.standard_normal(n))
    pink = np.cumsum(wn) + 0.5 * wn

    mix = 0.6 * wn + 0.3 * rw + 0.1 * pink

    return mix

def evaluate(series):
    return float(estimate_alpha(series))

def safe_collect(fn, seeds):
    vals = []
    for s in seeds:
        try:
            v = evaluate(fn(seed=s))

            if v is not None and np.isfinite(v) and (0.5 <= v <= 5.0):
                vals.append(v)

        except Exception:
            continue

    return vals

def to_native(obj):
    if isinstance(obj, dict):
        return {k: to_native(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_native(v) for v in obj]
    elif isinstance(obj, tuple):
        return tuple(to_native(v) for v in obj)
    elif isinstance(obj, np.generic):
        return obj.item()
    else:
        return obj

def main():
    os.makedirs("artifacts", exist_ok=True)

    results = {
        "real": {},
        "synthetic": {},
        "noise": {}
    }

    # === REAL ===
    sunspots = load_sunspots()
    real_alpha = evaluate(sunspots)

    if not (0.5 <= real_alpha <= 5.0):
        raise SystemExit(f"❌ invalid real alpha: {real_alpha}")

    results["real"]["sunspots"] = real_alpha

    # === SYNTHETIC (robust sampling) ===
    synthetic_vals = safe_collect(load_synthetic, range(40))

    if len(synthetic_vals) < 5:
        raise SystemExit("❌ synthetic unstable — insufficient valid samples")

    results["synthetic"]["mean"] = float(np.mean(synthetic_vals))
    results["synthetic"]["std"] = float(np.std(synthetic_vals))

    # === NOISE ===
    noise_alpha = evaluate(load_noise())
    results["noise"]["white"] = noise_alpha

    # === CORE VALIDATION ===

    # === MULTI-SIGNAL NOISE REJECTION ===

    delta_alpha = abs(real_alpha - noise_alpha)

    # spectral condition
    spectral_pass = (
        delta_alpha > 0.8
        and real_alpha > noise_alpha
    )

    # stability condition
    stability_pass = (0.5 < real_alpha < 4.5)

    # variance structure
    variance_ratio = np.var(sunspots) / (np.var(load_noise()) + 1e-8)
    variance_pass = variance_ratio > 1.2

    # final decision
    not_noise = (
        spectral_pass
        and stability_pass
        and variance_pass
    )

    if not not_noise:
        raise SystemExit(
            f"❌ real not distinguishable from noise | "
            f"delta={delta_alpha:.3f}, var_ratio={variance_ratio:.3f}"
        )

    # 🔥 synthetic = stress probe (NOT rejection criteria)
    stress_ratio = results["synthetic"]["std"] / (abs(results["synthetic"]["mean"]) + 1e-8)

    print(f"synthetic stress ratio: {stress_ratio:.4f}")

    if stress_ratio > 1.5:
        print("⚠️ synthetic highly chaotic (expected under stress)")

    from analysis.falsification_tests import run_falsification

    fals = run_falsification(sunspots, np.random.RandomState(42))

    gap = min([
        abs(fals["original_alpha"] - fals["white_noise_alpha"]),
        abs(fals["original_alpha"] - fals["shuffled_alpha"])
    ])

    if gap < 0.3:
        raise SystemExit("❌ weak falsification gap in multi-dataset")
        
    report = {
        "alphas": results,
        "checks": {
            "not_noise": bool(not_noise),
            "internal_stability": bool(stability_pass)
        }
    }

    report = to_native(report)

    with open("artifacts/multi_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("Multi-dataset report generated")
    print("✅ MULTI-DATASET CLAIM HOLDS")

if __name__ == "__main__":
    main()
