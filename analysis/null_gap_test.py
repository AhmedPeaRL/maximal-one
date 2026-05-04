import numpy as np
from analysis.falsification_tests import run_falsification


def check_null_gap(series,rng):

    res = run_falsification(series, rng)

    real = res["original_alpha"]
    shuffled = res["shuffled_alpha"]
    phase = res["phase_randomized_alpha"]
    noise = res["white_noise_alpha"]

    gaps = [
        abs(real - shuffled),
        abs(real - phase),
        abs(real - noise)
    ]

    min_gap = min(gaps)

    print("Gaps:", gaps)

    if min_gap < 0.25:
        raise SystemExit("❌ Null separation too weak")

    print("✅ NULL GAP HOLDS")


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv("real-data/sunspots_global.csv")
    col = "Sunspots" if "Sunspots" in df.columns else "value"

    check_null_gap(df[col].values, rng)
