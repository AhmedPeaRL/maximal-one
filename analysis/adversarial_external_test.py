import numpy as np
import pandas as pd

from analysis.independent_validation import estimate_alpha_welch
from analysis.numerical_spectral_verification import estimate_alpha


def generate_adversarial_signal(n=1000):
    # random walk + structured fake periodic + noise
    x = np.cumsum(np.random.randn(n))
    noise = np.random.randn(n) * 0.5
    fake = np.sin(np.linspace(0, 20, n)) * 0.3
    return x + noise + fake


def is_structured(alpha1, alpha2):
    if not np.isfinite(alpha1) or not np.isfinite(alpha2):
        return False

    # 🔥 بدل absolute agreement → relative consistency
    ratio = abs(alpha1 - alpha2) / (abs(alpha1) + 1e-8)

    return ratio < 0.35


def evaluate(series):
    a_fft = estimate_alpha(series)
    a_welch = estimate_alpha_welch(series)
    return a_fft, a_welch


def run_test():
    # === REAL DATA ===
    real_df = pd.read_csv("real-data/sunspots_global.csv")
    col = "Sunspots" if "Sunspots" in real_df.columns else "value"

    real_series = real_df[col].values

    real_fft, real_welch = evaluate(real_series)
    real_ok = is_structured(real_fft, real_welch)

    print("=== REAL DATA ===")
    print("FFT:", real_fft)
    print("Welch:", real_welch)
    print("Structured:", real_ok)

    if not real_ok:
        raise SystemExit("❌ real data unstable — invalid baseline")

    # === ADVERSARIAL ===
    adv = generate_adversarial_signal(len(real_series))

    adv_fft, adv_welch = evaluate(adv)
    adv_ok = is_structured(adv_fft, adv_welch)

    print("\n=== ADVERSARIAL DATA ===")
    print("FFT:", adv_fft)
    print("Welch:", adv_welch)
    print("Structured:", adv_ok)

    # 🔥 أهم شرط في النظام كله
    if adv_ok:
        raise SystemExit("❌ adversarial mimics structure — REJECTED")

    print("✅ adversarial correctly rejected")


if __name__ == "__main__":
    run_test()
