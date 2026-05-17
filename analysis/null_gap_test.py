import numpy as np
from analysis.falsification_tests import run_falsification

def check_null_gap(series, rng):

    res = run_falsification(series, rng)

    real = res["original_alpha"]
    shuffled = res["shuffled_alpha"]
    phase = res["phase_randomized_alpha"]
    noise = res["white_noise_alpha"]

    nulls = [shuffled, phase, noise]

    gaps = [abs(real - n) for n in nulls]

    mean_null = np.mean(nulls)
    std_null = np.std(nulls) + 1e-12

    # 🔥 Z-SCORE separation (stronger than raw gap)
    z_score = abs(real - mean_null) / std_null

    print("Gaps:", gaps)
    print("Z-score separation:", z_score)

    # 🔥 adaptive threshold
    if z_score < 1.8:
        raise SystemExit("❌ Null separation too weak (z-score failed)")

    # 🔥 extra guard (closest null)
    min_gap = min(gaps)
    if min_gap < 0.15:
        raise SystemExit("❌ Closest null too قريب من real")

    print("✅ NULL GAP HOLDS (STRONG)")

if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv("real-data/sunspots_global_extended.csv")
    col = "Sunspots" if "Sunspots" in df.columns else "value"
    rng = np.random.RandomState(42)
    
    check_null_gap(df[col].values, rng)
