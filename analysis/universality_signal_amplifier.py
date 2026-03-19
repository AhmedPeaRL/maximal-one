import json
import numpy as np
import os

INPUT = "artifacts/universality_features.json"
OUTPUT = "artifacts/universality_amplified.json"


def load_features():
    if not os.path.exists(INPUT):
        return []
    with open(INPUT) as f:
        return json.load(f)


def normalize(v):
    v = np.array(v, dtype=float)
    if len(v) == 0:
        return v
    m = np.mean(v)
    s = np.std(v)
    if s == 0:
        return v * 0
    return (v - m) / s


def compute_weighted_signature(features):
    alpha = [f["spectral_alpha"] for f in features if f["spectral_alpha"] is not None]
    entropy = [f["entropy_rate"] for f in features if f["entropy_rate"] is not None]
    hurst = [f["hurst_exponent"] for f in features if f["hurst_exponent"] is not None]

    alpha_n = normalize(alpha)
    entropy_n = normalize(entropy)
    hurst_n = normalize(hurst)

    combined = []

    for i in range(min(len(alpha_n), len(entropy_n), len(hurst_n))):
        val = (
            0.4 * alpha_n[i] +
            0.3 * entropy_n[i] +
            0.3 * hurst_n[i]
        )
        combined.append(val)

    return np.array(combined)


def signal_strength(sig):
    if len(sig) < 5:
        return 0.0

    mean = np.mean(sig)
    std = np.std(sig)

    if std == 0:
        return 0.0

    return float(abs(mean) / std)


def main():
    feats = load_features()

    if not feats:
        print("No features found.")
        return

    sig = compute_weighted_signature(feats)

    strength = signal_strength(sig)

    result = {
        "amplified_strength": strength,
        "count": len(sig),
        "note": "amplified universality signal"
    }

    os.makedirs("artifacts", exist_ok=True)

    with open(OUTPUT, "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
