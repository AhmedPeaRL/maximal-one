import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha

def run_guard(series):
    alpha = estimate_alpha(series)

    if not np.isfinite(alpha):
        raise SystemExit("❌ invalid alpha (NaN)")

    # اختبار حساسية
    perturbed = series + np.random.normal(0, np.std(series)*0.02, len(series))
    alpha_perturbed = estimate_alpha(perturbed)

    if not np.isfinite(alpha_perturbed):
        raise SystemExit("❌ unstable under perturbation")

    delta = abs(alpha - alpha_perturbed)

    if delta > 0.4:
        raise SystemExit("❌ fragile structure")

    print("✅ anti-self-deception guard passed")
