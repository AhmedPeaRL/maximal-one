from __future__ import annotations
import numpy as np
from analysis.numerical_spectral_verification import estimate_alpha

DEFAULT_SEED = 42
DEFAULT_PERTURBATION_FRACTION = 0.02
DEFAULT_MAX_DELTA = 0.4

def run_guard(
    series,
    seed: int = DEFAULT_SEED,
    perturbation_fraction: float = DEFAULT_PERTURBATION_FRACTION,
    max_delta: float = DEFAULT_MAX_DELTA,
):
    series = np.asarray(series, dtype=np.float64)

    if series.ndim != 1:
        raise SystemExit("❌ invalid series dimensionality")

    if len(series) < 2:
        raise SystemExit("❌ series too short")

    if not np.all(np.isfinite(series)):
        raise SystemExit("❌ series contains non-finite values")

    series_std = float(np.std(series))

    if not np.isfinite(series_std):
        raise SystemExit("❌ series standard deviation is invalid")

    alpha = estimate_alpha(series)

    if not np.isfinite(alpha):
        raise SystemExit("❌ invalid alpha (NaN)")

    if not np.isfinite(perturbation_fraction) or perturbation_fraction < 0:
        raise SystemExit("❌ invalid perturbation fraction")

    if not np.isfinite(max_delta) or max_delta < 0:
        raise SystemExit("❌ invalid maximum delta")

    rng = np.random.default_rng(seed)

    perturbation = rng.normal(
        loc=0.0,
        scale=series_std * perturbation_fraction,
        size=len(series),
    )

    perturbed = series + perturbation

    alpha_perturbed = estimate_alpha(perturbed)

    if not np.isfinite(alpha_perturbed):
        raise SystemExit("❌ unstable under perturbation")

    delta = abs(
        float(alpha) - float(alpha_perturbed)
    )

    result = {
        "passed": bool(delta <= max_delta),
        "seed": int(seed),
        "perturbation_fraction": float(perturbation_fraction),
        "max_delta": float(max_delta),
        "alpha": float(alpha),
        "alpha_perturbed": float(alpha_perturbed),
        "delta": float(delta),
        "scientific_role": "diagnostic_only",
        "interpretation": (
            "Deterministic perturbation-sensitivity diagnostic. "
            "Passing does not establish mechanism, causality, "
            "universality, or independent reproducibility."
        ),
    }

    if delta > max_delta:
        raise SystemExit(
            "❌ fragile structure: "
            f"delta={delta:.8f} > max_delta={max_delta:.8f}"
        )

    print("✅ anti-self-deception guard passed")
    print(f"   seed={seed}")
    print(f"   alpha={alpha:.8f}")
    print(f"   alpha_perturbed={alpha_perturbed:.8f}")
    print(f"   delta={delta:.8f}")

    return result

if __name__ == "__main__":
    raise SystemExit(
        "This module exposes run_guard(series); "
        "the canonical pipeline should call it explicitly."
    )
