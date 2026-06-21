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
    x = np.asarray(
        x,
        dtype=np.float64
    )

    if len(x) >= target_len:
        return x[:target_len]

    rng = np.random.default_rng(42)

    extended = []

    while len(extended) < target_len:

        block = rng.integers(
            128,
            256
        )

        start = rng.integers(
            0,
            max(1, len(x) - block)
        )

        segment = x[
            start:start+block
        ]

        extended.extend(
            segment.tolist()
        )

    out = np.asarray(
        extended[:target_len],
        dtype=np.float64
    )

    out = out - np.mean(out)

    std = np.std(out)

    if std > 1e-12:
        out = out / std

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
