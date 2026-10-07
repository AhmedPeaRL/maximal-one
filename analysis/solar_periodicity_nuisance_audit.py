from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.signal import find_peaks, welch

from analysis.load_real_datasets import load_series


DATASET = Path("real-data/sunspots_full.csv")
OUTPUT = Path(
    "artifacts/solar_periodicity_nuisance_audit.json"
)

FS = 1.0

CANONICAL_BAND = (0.01, 0.05)

SOLAR_PERIOD_MONTHS_REFERENCE = 132.0
SOLAR_FUNDAMENTAL_REFERENCE = (
    1.0 / SOLAR_PERIOD_MONTHS_REFERENCE
)


def spectral_profile(
    x: np.ndarray,
):
    nperseg = min(
        1024,
        len(x),
    )

    if nperseg < 512:
        raise ValueError(
            "Solar nuisance audit requires "
            "at least 512 observations."
        )

    frequencies, power = welch(
        x,
        fs=FS,
        window="hann",
        detrend="linear",
        scaling="density",
        nperseg=nperseg,
        noverlap=nperseg // 2,
        nfft=nperseg,
        return_onesided=True,
        average="mean",
    )

    positive = (
        np.isfinite(frequencies)
        & np.isfinite(power)
        & (frequencies > 0)
    )

    return (
        frequencies[positive],
        power[positive],
    )


def summarize_band(
    frequencies,
    power,
    low,
    high,
):
    mask = (
        (frequencies >= low)
        & (frequencies <= high)
    )

    if not np.any(mask):
        return {
            "available": False,
            "low": low,
            "high": high,
        }

    local_f = frequencies[mask]
    local_p = power[mask]

    peak_index = int(
        np.argmax(local_p)
    )

    return {
        "available": True,
        "low": float(low),
        "high": float(high),
        "frequency_peak": float(
            local_f[peak_index]
        ),
        "power_peak": float(
            local_p[peak_index]
        ),
        "mean_power": float(
            np.mean(local_p)
        ),
        "median_power": float(
            np.median(local_p)
        ),
        "frequency_bin_count": int(
            len(local_f)
        ),
    }


def main():
    x = np.asarray(
        load_series(DATASET),
        dtype=np.float64,
    )

    if len(x) < 512:
        raise SystemExit(
            "Primary sunspot series is too short."
        )

    frequencies, power = spectral_profile(x)

    solar_fundamental = (
        SOLAR_FUNDAMENTAL_REFERENCE
    )

    harmonic_assessment = []

    for harmonic in range(1, 9):
        reference_frequency = (
            solar_fundamental
            * harmonic
        )

        nearest_index = int(
            np.argmin(
                np.abs(
                    frequencies
                    - reference_frequency
                )
            )
        )

        harmonic_assessment.append(
            {
                "harmonic": harmonic,
                "reference_frequency": float(
                    reference_frequency
                ),
                "inside_canonical_band": bool(
                    CANONICAL_BAND[0]
                    <= reference_frequency
                    <= CANONICAL_BAND[1]
                ),
                "nearest_observed_frequency_bin": (
                    float(
                        frequencies[
                            nearest_index
                        ]
                    )
                ),
                "nearest_observed_power": float(
                    power[
                        nearest_index
                    ]
                ),
            }
        )

    result = {
        "scientific_role": "diagnostic_only",
        "claim_support_eligible": False,
        "confirmatory_use": False,

        "dataset": str(DATASET),
        "loader": (
            "analysis.load_real_datasets.load_series"
        ),
        "sample_count": int(len(x)),
        "sampling_frequency_cycles_per_month": FS,

        "canonical_endpoint": {
            "frequency_band": list(
                CANONICAL_BAND
            ),
            "nperseg": min(
                1024,
                len(x),
            ),
            "window": "hann",
            "detrend": "linear",
            "scaling": "density",
            "noverlap_fraction": 0.5,
            "nfft": min(
                1024,
                len(x),
            ),
        },

        "solar_reference": {
            "reference_period_months": (
                SOLAR_PERIOD_MONTHS_REFERENCE
            ),
            "reference_fundamental_frequency": (
                float(
                    solar_fundamental
                )
            ),
        },

        "harmonic_assessment":
            harmonic_assessment,

        "spectral_regions": {
            "canonical_band_0.01_0.05":
                summarize_band(
                    frequencies,
                    power,
                    0.01,
                    0.05,
                ),
            "low_band_0.005_0.01":
                summarize_band(
                    frequencies,
                    power,
                    0.005,
                    0.01,
                ),
            "broad_band_0.005_0.10":
                summarize_band(
                    frequencies,
                    power,
                    0.005,
                    0.10,
                ),
        },

        "interpretation_policy": {
            "no_endpoint_optimization": True,
            "no_band_selection": True,
            "no_posthoc_claim": True,
            "nuisance_treatment_requires_preconfirmation_rule":
                True,
            "current_result_does_not_support_or_falsify_claim":
                True,
            "loader_must_match_canonical_repository_loader":
                True,
        },
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
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "Solar periodicity nuisance audit generated:"
        f" {OUTPUT}"
    )


if __name__ == "__main__":
    main()
