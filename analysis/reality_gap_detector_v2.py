import numpy as np
import json
from pathlib import Path

ART = Path("artifacts")


def load_series():
    path = Path("real-data/sunspots_global_prepared.csv")
    if not path.exists():
        return None

    import pandas as pd
    df = pd.read_csv(path)
    return df.values.squeeze()


# -----------------------------
# Multi-scale structure detection
# -----------------------------

def autocorr_strength(series, lag=1):
    return np.corrcoef(series[:-lag], series[lag:])[0, 1]


def multi_scale_signal(series):
    scales = [1, 2, 3, 5, 8, 13]
    scores = []

    for s in scales:
        try:
            scores.append(abs(autocorr_strength(series, lag=s)))
        except:
            pass

    return np.mean(scores)


# -----------------------------
# Entropy vs structure
# -----------------------------

def entropy_estimate(series):
    hist, _ = np.histogram(series, bins=50, density=True)
    hist = hist + 1e-12
    return -np.sum(hist * np.log(hist))


# -----------------------------
# Core detection logic
# -----------------------------

def detect_gap(series):

    if len(series) < 300:
        return {"skipped": True}

    signal_strength = multi_scale_signal(series)
    entropy = entropy_estimate(series)

    structure_ratio = signal_strength / (entropy + 1e-9)

    gap_exists = structure_ratio < 0.02

    return {
        "signal_strength": float(signal_strength),
        "entropy": float(entropy),
        "structure_ratio": float(structure_ratio),
        "reality_check_passed": not gap_exists,
        "gap_detected": bool(gap_exists),
        "severity": (
            "high" if structure_ratio < 0.005 else
            "moderate" if structure_ratio < 0.02 else
            "low"
        )
    }


# -----------------------------
# Main
# -----------------------------

def main():

    series = load_series()

    if series is None:
        result = {"skipped": True}
    else:
        result = detect_gap(series)

    ART.mkdir(exist_ok=True)
    (ART / "reality_gap_detector_v2.json").write_text(
        json.dumps(result, indent=2)
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
