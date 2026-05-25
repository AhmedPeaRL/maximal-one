import os
import pandas as pd
import numpy as np

INPUT_PATH = "real-data/sunspots_full.csv"
OUTPUT_PATH = "real-data/sunspots_global_extended.csv"

if not os.path.exists(INPUT_PATH):
    raise SystemExit(f"❌ Missing dataset: {INPUT_PATH}")

df = pd.read_csv(INPUT_PATH, sep=";", engine="python")
df = df.dropna(axis=1, how="all")

series = None
for col in df.columns:
    col_lower = col.lower()

    # 🚫 تجاهل الأعمدة الزمنية
    if any(k in col_lower for k in ["year", "date", "month"]):
        continue

    s = pd.to_numeric(df[col], errors="coerce").dropna().values

    if len(s) > 300 and np.std(s) > 1e-3:
        # 🔥 استبعد الأعمدة شبه الثابتة
        if np.unique(s[:50]).shape[0] < 10:
            continue

        series = s
        break

if series is None:
    raise SystemExit("❌ No usable numeric column found")

series = series.astype(np.float64)

def extend_realistic(x, target_len=3327):
    x = np.asarray(x, dtype=np.float64)

    if len(x) >= target_len:
        return x[:target_len]

    rng = np.random.default_rng(42)

    extended = list(x)

    while len(extended) < target_len:
        segment = x.copy()

        # noise خفيف
        noise = rng.normal(0, np.std(x)*0.05, len(segment))
        segment = segment + noise

        # phase randomization بسيط
        fft = np.fft.rfft(segment)
        phase = rng.uniform(0, 2*np.pi, len(fft))
        fft = np.abs(fft) * np.exp(1j * phase)
        segment = np.fft.irfft(fft, n=len(segment))

        # 🔥 أهم نقطة: no recursive blending
        extended.extend(segment.tolist())

    extended = np.array(extended[:target_len], dtype=np.float64)

    # 🔥 preserve low-frequency structure
    trend = np.linspace(-0.5, 0.5, len(extended))
    extended = extended + 0.15 * trend

    # normalize gently بدون قتل structure
    mean = np.mean(extended)
    std = np.std(extended) + 1e-12

    extended = (extended - mean) / std

    # preserve spectral shape
    extended = extended + 0.1 * trend
    
    return extended
    
extended = extend_realistic(series, target_len=3327)

pd.DataFrame({"value": extended}).to_csv(OUTPUT_PATH, index=False)

print("✅ extended dataset generated:", len(extended))
