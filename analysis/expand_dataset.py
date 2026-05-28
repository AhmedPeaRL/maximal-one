import os
import pandas as pd
import numpy as np

INPUT_PATH = "real-data/sunspots_full.csv"
OUTPUT_PATH = "real-data/sunspots_global_extended.csv"

if not os.path.exists(INPUT_PATH):
    raise SystemExit(f"❌ Missing dataset: {INPUT_PATH}")

# 🔥 FIX REAL HEADER ISSUE
df = pd.read_csv(
    INPUT_PATH,
    sep=";",
    engine="python",
    header=None
)

# 🔥 canonical names
df.columns = [
    "year",
    "month",
    "decimal_year",
    "sunspots",
    "std",
    "obs",
    "flag"
]

series = pd.to_numeric(
    df["sunspots"],
    errors="coerce"
).dropna().values

series = series.astype(np.float64)

if len(series) < 300:
    raise SystemExit("❌ Dataset too small")

if np.std(series) < 1e-6:
    raise SystemExit("❌ Degenerate dataset")

def extend_realistic(x, target_len=3327):

    x = np.asarray(x, dtype=np.float64)

    if len(x) >= target_len:
        return x[:target_len]

    rng = np.random.default_rng(42)

    extended = list(x)

    while len(extended) < target_len:

        start = rng.integers(
            0,
            len(x) - 256
        )

        segment = x[start:start+256].copy()

        # 🔥 preserve local variance
        local_std = np.std(segment)

        if local_std < 1e-6:
            continue

        # 🔥 minimal perturbation
        noise = rng.normal(
            0,
            local_std * 0.05,
            len(segment)
        )

        segment = segment + noise

        extended.extend(segment.tolist())

    out = np.asarray(
        extended[:target_len],
        dtype=np.float64
    )

    return out


extended = extend_realistic(
    series,
    target_len=3327
)

pd.DataFrame({
    "Sunspots": extended
}).to_csv(
    OUTPUT_PATH,
    index=False
)

print("✅ extended dataset generated:", len(extended))
