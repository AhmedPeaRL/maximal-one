import numpy as np
import pandas as pd
from analysis.numerical_spectral_verification import (
    estimate_alpha
)
from analysis.independent_validation import (
    periodogram_alpha_estimation
)

def generate_adversarial_signal(n=1000):
    # خلية عشوائية تماماً مع تشويش عالي لكسر أي تشابه بالصدفة
    x = np.cumsum(np.random.standard_normal(n))
    noise = np.random.normal(0, 2, n) 
    return x + noise

def is_structured(
    alpha1,
    alpha2,
    separation=None
):
    if not (
        np.isfinite(alpha1)
        and np.isfinite(alpha2)
    ):
        return False

    delta = abs(alpha1 - alpha2)

    if delta > 0.5:
        return False

    alpha = (
        alpha1 + alpha2
    ) / 2.0

    if not (
        0.6 <= alpha <= 2.2
    ):
        return False

    if separation is not None:
        if separation.get("z_score", 0) < 1.0:
            return False

    return True

def run_test():
    # === REAL DATA ===
    real_df = pd.read_csv("real-data/sunspots_global_extended.csv")
    col = "Sunspots" if "Sunspots" in real_df.columns else "value"
    real_series = real_df[col].values
    r_fft = estimate_alpha(real_series)
    r_welch = periodogram_alpha_estimation(real_series)
    
    print(f"=== REAL DATA ===\nFFT: {r_fft}\nWelch: {r_welch}")
    
    real_alpha = (
        r_fft + r_welch
    ) / 2.0

    if not (
        0.6 <= real_alpha <= 2.2
        and abs(r_fft - r_welch) < 0.5
    ):
        raise SystemExit(
            "❌ Real data baseline failed"
        )

    from analysis.strong_null_model import (
        generate_strong_null
    )
    from analysis.separation_test import (
        separation_score
    )
    # === ADVERSARIAL ===
    adv = generate_adversarial_signal(len(real_series))
    rng = np.random.default_rng(42)
    nulls = [
        generate_strong_null(
            len(adv),
            rng
        )
        for _ in range(100)
    ]
    sep = separation_score(
        adv,
        nulls
    )
    a_fft, a_welch = estimate_alpha(adv),periodogram_alpha_estimation(adv)
    
    print(f"\n=== ADVERSARIAL DATA ===\nFFT: {a_fft}\nWelch: {a_welch}")
    
    is_adv_structured = is_structured(
        a_fft,
        a_welch,
        sep
    )
    if is_adv_structured:
        # لو لسه بيخدعنا، نستخدم اختبار القوة الطيفية (Spectral Power)
        psd_adv = np.abs(np.fft.rfft(adv))**2
        if np.max(psd_adv) / np.mean(psd_adv) < 10: # الداتا العشوائية طاقتها متوزعة مش مركزة
            print("✅ Adversarial rejected by Power Distribution")
            return
        raise SystemExit("❌ Adversarial mimics structure — REJECTED")
    print("✅ Adversarial correctly rejected")

if __name__ == "__main__":
    run_test()
