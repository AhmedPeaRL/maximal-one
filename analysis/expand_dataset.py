import os
import pandas as pd
import numpy as np

output_path = "real-data/sunspots_global_extended.csv"

if not os.path.exists("real-data/sunspots_global.csv"):
    raise SystemExit("❌ base dataset missing")

df = pd.read_csv("real-data/sunspots_global.csv")
series = df.iloc[:, 0].values.astype(np.float64)

rng = np.random.default_rng(42)

# =========================
# 🔥 MULTI-SCALE PRESERVATION
# =========================

def generate_multiscale_series(base, rng, repeats=4):

    base = np.asarray(base, dtype=np.float64)
    n = len(base)

    # 🔥 FFT
    fft = np.fft.rfft(base)
    mag = np.abs(fft)

    # 🔥 phase randomization (لكن محافظ على spectrum)
    new_series = []

    for _ in range(repeats):

        phases = rng.uniform(0, 2*np.pi, len(fft))
        phases[0] = 0.0
        if n % 2 == 0:
            phases[-1] = 0.0

        new_fft = mag * np.exp(1j * phases)

        s = np.fft.irfft(new_fft, n=n)

        # 🔥 slight perturbation بدون كسر scale
        noise = rng.normal(0, np.std(s)*0.02, n)
        s = s + noise

        new_series.append(s)

    return np.concatenate(new_series)
    
extended = generate_multiscale_series(series, rng, repeats=6)

# 🔥 final normalization (global)
extended = (extended - np.mean(extended)) / (np.std(extended) + 1e-12)

pd.DataFrame({"Sunspots": extended}).to_csv(output_path, index=False)

print("✅ extended dataset generated (MULTI-SCALE PRESERVED):", len(extended))
