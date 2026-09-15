import numpy as np
from analysis.numerical_spectral_verification import (
    estimate_alpha
)
from analysis.temporal_irreversibility import (
    irreversibility_pass
)

def generate_surrogate(series, rng):
    """
    Phase-randomized surrogate.

    The surrogate preserves the Fourier amplitude spectrum
    while randomizing phase. Therefore PSD/alpha comparison
    against this surrogate is diagnostic only.

    The surrogate is useful for testing phase-dependent temporal
    structure, but it must not be treated as an independent
    spectral-separation null.
    """

    series = np.asarray(
        series,
        dtype=np.float64
    )

    if series.ndim != 1:
        raise ValueError(
            "Series must be one-dimensional"
        )

    if not np.all(np.isfinite(series)):
        raise ValueError(
            "Series contains non-finite values"
        )

    fft = np.fft.rfft(series)

    random_phases = np.exp(
        1j * rng.uniform(
            0,
            2 * np.pi,
            len(fft)
        )
    )

    # Preserve the DC component exactly.
    random_phases[0] = 1.0

    new_fft = (
        np.abs(fft)
        * random_phases
    )

    surrogate = np.fft.irfft(
        new_fft,
        n=len(series)
    )

    return np.asarray(
        surrogate,
        dtype=np.float64
    )

def run_null_test(real_series, n=32):
    """
    Run the phase-randomized surrogate diagnostic.

    Scientific interpretation:

    1. Alpha comparison against phase-randomized surrogates is
       diagnostic only because the surrogate preserves the
       Fourier amplitude spectrum.

    2. Temporal irreversibility is evaluated separately.

    3. The function does NOT combine these two diagnostics into
       a single inferential pass/fail verdict.

    4. A successful irreversibility result is reported as evidence
       against the phase-randomized temporal null only.

    5. This function does not establish mechanism, universality,
       HCM causation, or independent replication.
    """

    rng = np.random.RandomState(42)

    real_alpha = estimate_alpha(
        real_series
    )

    if not np.isfinite(real_alpha):
        raise RuntimeError(
            "Real alpha invalid"
        )

    null_alphas = []
    surrogate_pool = []

    for _ in range(n):

        surrogate = generate_surrogate(
            real_series,
            rng
        )

        surrogate_pool.append(
            surrogate
        )

        alpha = estimate_alpha(
            surrogate
        )

        if np.isfinite(alpha):
            null_alphas.append(
                float(alpha)
            )

    null_alphas = np.asarray(
        null_alphas,
        dtype=np.float64
    )

    if len(null_alphas) < 8:
        return {
            "real_alpha": float(real_alpha),
            "null_mean": np.nan,
            "null_std": np.nan,
            "z_score": np.nan,
            "alpha_diagnostic_pass": False,
            "alpha_diagnostic_role": "diagnostic_only",
            "phase_surrogate_interpretation": (
                "PSD-preserving surrogate; alpha comparison "
                "is not an independent spectral test."
            ),
            "irreversibility": {
                "pass": False,
                "reason": "insufficient_surrogates"
            },
            "pass": False,
            "reason": "insufficient_null_samples"
        }

    mean_null = float(
        np.mean(null_alphas)
    )

    std_null = float(
        np.std(null_alphas)
    )

    z_score = (
        (real_alpha - mean_null)
        /
        (std_null + 1e-8)
    )

    # IMPORTANT:
    # Because phase randomization preserves Fourier amplitude,
    # alpha separation here is diagnostic only.
    alpha_diagnostic_pass = bool(
        np.isfinite(z_score)
        and abs(z_score) > 2.0
    )

    print(
        "Real alpha:",
        real_alpha
    )

    print(
        "Phase-surrogate null mean:",
        mean_null
    )

    print(
        "Phase-surrogate null std:",
        std_null
    )

    print(
        "Phase-surrogate alpha z-score:",
        z_score
    )

    print(
        "Valid phase surrogates:",
        len(null_alphas)
    )

    print(
        "Phase-surrogate alpha comparison: "
        "DIAGNOSTIC ONLY"
    )

    irr = irreversibility_pass(
        real_series,
        surrogate_pool
    )

    print(
        "=== IRREVERSIBILITY TEST ==="
    )

    print(
        irr
    )

    return {
        "real_alpha": float(real_alpha),
        "null_mean": mean_null,
        "null_std": std_null,
        "z_score": float(z_score),
        "alpha_diagnostic_pass": alpha_diagnostic_pass,
        "alpha_diagnostic_role": "diagnostic_only",
        "phase_surrogate_interpretation": (
            "PSD-preserving surrogate; alpha comparison "
            "is not an independent spectral test."
        ),
        "irreversibility": irr,
        "pass": bool(
            irr.get("pass", False)
        ),
        "pass_basis": (
            "temporal_irreversibility_against_phase_surrogates"
            if irr.get("pass", False)
            else "none"
        ),
        "valid_samples": int(
            len(null_alphas)
        )
    }
