from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

from analysis.numerical_spectral_verification import (
    estimate_alpha,
)
from analysis.independent_validation import (
    periodogram_alpha_estimation,
)
from analysis.strong_null_model import (
    generate_strong_null,
)
from analysis.separation_test import (
    separation_score,
)

OUTPUT = Path(
    "artifacts/adversarial_control.json"
)

def generate_adversarial_signal(
    n,
    rng,
):
    wn = rng.standard_normal(n)

    high_freq = np.sin(
        np.linspace(
            0,
            80 * np.pi,
            n,
        )
    )

    burst = np.zeros(n)

    idx = rng.integers(
        0,
        n,
        25,
    )

    burst[idx] = rng.normal(
        0,
        8,
        len(idx),
    )

    return (
        wn
        + 0.4 * high_freq
        + burst
    )

def persistence_score(series):
    series = np.asarray(
        series,
        dtype=np.float64,
    )

    if len(series) < 256:
        return 0.0

    raw_std = np.std(series)

    diff_std = (
        np.std(np.diff(series))
        + 1e-12
    )

    ratio = raw_std / diff_std

    ac1 = np.corrcoef(
        series[:-1],
        series[1:],
    )[0, 1]

    return float(
        0.6 * np.tanh(ac1)
        +
        0.4 * np.tanh(ratio / 10)
    )

def main():
    real_path = Path(
        "real-data/sunspots_global_extended.csv"
    )

    if not real_path.exists():
        raise SystemExit(
            "❌ Derived adversarial input is missing"
        )

    df = pd.read_csv(
        real_path
    )

    column = (
        "Sunspots"
        if "Sunspots" in df.columns
        else "value"
    )

    real_series = (
        df[column]
        .to_numpy(dtype=np.float64)
    )

    rng = np.random.default_rng(
        42
    )

    adversarial = (
        generate_adversarial_signal(
            len(real_series),
            rng,
        )
    )

    null_rng = np.random.default_rng(
        42042
    )

    nulls = [
        generate_strong_null(
            len(adversarial),
            null_rng,
        )
        for _ in range(100)
    ]

    sep = separation_score(
        adversarial,
        nulls,
    )

    fft_alpha = (
        periodogram_alpha_estimation(
            adversarial
        )
    )

    welch_alpha = (
        estimate_alpha(
            adversarial
        )
    )

    persistence = (
        persistence_score(
            adversarial
        )
    )

    finite = (
        np.isfinite(fft_alpha)
        and
        np.isfinite(welch_alpha)
    )

    method_delta = (
        abs(
            float(fft_alpha)
            -
            float(welch_alpha)
        )
        if finite
        else None
    )

    spectral_mimic = False

    if (
        finite
        and method_delta <= 0.5
        and 0.6
        <= (
            float(fft_alpha)
            +
            float(welch_alpha)
        ) / 2.0
        <= 2.2
        and persistence > 0.55
        and sep is not None
    ):
        psd = (
            np.abs(
                np.fft.rfft(
                    adversarial
                )
            )
            ** 2
        )

        concentration = (
            np.max(psd)
            /
            (np.mean(psd) + 1e-12)
        )

        if concentration >= 10:
            spectral_mimic = True

    passed = not spectral_mimic

    result = {
        "passed": bool(passed),
        "role": "adversarial_control",
        "scientific_claim_authority": False,
        "seed": 42,
        "input_role": "derived_adversarial_probe",
        "fft_alpha": (
            float(fft_alpha)
            if np.isfinite(fft_alpha)
            else None
        ),
        "welch_alpha": (
            float(welch_alpha)
            if np.isfinite(welch_alpha)
            else None
        ),
        "method_delta": (
            float(method_delta)
            if method_delta is not None
            else None
        ),
        "persistence_score": float(
            persistence
        ),
        "spectral_mimic_detected": bool(
            spectral_mimic
        ),
        "interpretation": (
            "Adversarial probe did not satisfy "
            "the predefined mimic condition."
            if passed
            else
            "Adversarial probe mimicked the "
            "declared structural condition."
        ),
    }

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT.write_text(
        json.dumps(
            result,
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    print(
        "Adversarial control:",
        "PASS" if passed else "FAIL",
    )

    if not passed:
        raise SystemExit(
            "❌ Adversarial control failed"
        )

if __name__ == "__main__":
    main()
