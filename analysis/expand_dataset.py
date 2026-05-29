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

    extended = []

    cursor = 0

    while len(extended) < target_len:

        window = rng.integers(192, 320)

        start = rng.integers(
            0,
            max(1, len(x) - window)
        )

        segment = x[start:start+window].copy()

        local_std = np.std(segment)

        if local_std < 1e-6:
            continue

        # 🔥 adaptive nonlinear warp
        t = np.linspace(0, 1, len(segment))

        warp = (
            1.0
            + 0.08 * np.sin(2*np.pi*t)
            + 0.04 * np.cos(5*np.pi*t)
        )

        segment = segment * warp

        # 🔥 local stochastic perturbation
        noise = rng.normal(
            0,
            local_std * 0.12,
            len(segment)
        )

        segment = segment + noise

        # 🔥 sparse decorrelation
        if rng.random() < 0.35:
            segment = np.diff(
                segment,
                prepend=segment[0]
            )

        # 🔥 polarity regime switch
        if rng.random() < 0.15:
            segment = -segment

        # 🔥 smooth boundary blending
        if len(extended) > 32:

            overlap = min(32, len(segment))

            prev = np.asarray(
                extended[-overlap:],
                dtype=np.float64
            )

            blend = np.linspace(0, 1, overlap)

            segment[:overlap] = (
                prev * (1 - blend)
                + segment[:overlap] * blend
            )

        extended.extend(segment.tolist())

        cursor += len(segment)

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
