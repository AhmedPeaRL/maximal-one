import numpy as np
import json
from pathlib import Path

ART = Path("artifacts")

def detect_pattern(series):

    diffs = np.diff(series)

    mean = np.mean(diffs)
    std = np.std(diffs)

    return {
        "mean_drift": float(mean),
        "volatility": float(std),
        "signal_to_noise": float(abs(mean)/(std+1e-8))
    }

def run_discovery(series):

    patterns = detect_pattern(series)

    score = patterns["signal_to_noise"]

    result = {
        "pattern": patterns,
        "discovered": score > 0.5
    }

    ART.mkdir(exist_ok=True)

    (ART / "discovery.json").write_text(json.dumps(result, indent=2))

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    import pandas as pd

    path = "real-data/sunspots_global_prepared.csv"

    if not Path(path).exists():
        print("Dataset missing")
        exit(0)

    df = pd.read_csv(path)

    run_discovery(df.values.squeeze())
