#!/usr/bin/env python3

import json
from pathlib import Path

import numpy as np
from scipy.signal import welch, find_peaks


DATASET = Path("real-data/sunspots_full.csv")
OUTPUT = Path("artifacts/solar_periodicity_nuisance_audit.json")

FS = 1.0  # samples per month for the canonical monthly series

CANONICAL_BAND = (0.01, 0.05)

SOLAR_PERIOD_MONTHS_REFERENCE = 132.0
SOLAR_FUNDAMENTAL_REFERENCE = 1.0 / SOLAR_PERIOD_MONTHS_REFERENCE


def load_series(path: Path) -> np.ndarray:
    if not path.is_file():
        raise SystemExit(f"Missing dataset: {path}")

    raw = np.genfromtxt(path, delimiter=",", names=True)

    if raw.dtype.names is None:
        raise SystemExit("Dataset has no readable header.")

    names = list(raw.dtype.names)

    numeric_columns = []
    for name in names:
        values = np.asarray(raw[name], dtype=float)
        if np.isfinite(values).sum() >= 512:
            numeric_columns.append((name, values))

    if not numeric_columns:
        raise SystemExit("No usable numeric series found.")

    # Select the longest finite numeric column.
    name, values = max(
        numeric_columns,
        key=lambda item: np.isfinite(item[1]).sum()
    )

    values = values[np.isfinite(values)]

    if len(values) < 512:
        raise SystemExit("Primary series is too short.")

    return values


def spectral_profile(x: np.ndarray):
    frequencies, power = welch(
        x,
        fs=FS,
        window="hann",
        detrend="linear",
        scaling="density",
        nperseg=min(1024, len(x)),
        noverlap=min(512, len(x) // 2),
        nfft=min(1024, len(x)),
        return_onesided=True,
        average="mean",
    )

    positive = (
        np.isfinite(frequencies)
        & np.isfinite(power)
        & (frequencies > 0)
    )

    frequencies = frequencies[positive]
    power = power[positive]

    return frequencies, power


def band_mean(frequencies, power, low, high):
    mask = (
        (frequencies >= low)
        & (frequencies <= high)
    )

    if not np.any(mask):
        return None

    return float(np.mean(power[mask]))


def summarize_band(frequencies, power, low, high):
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

    peak_index = int(np.argmax(local_p))

    return {
        "available": True,
        "low": low,
        "high": high,
        "frequency_peak": float(local_f[peak_index]),
        "power_peak": float(local_p[peak_index]),
        "mean_power": float(np.mean(local_p)),
        "median_power": float(np.median(local_p)),
        "frequency_bin_count": int(len(local_f)),
    }


def main():
    x = load_series(DATASET)

    frequencies, power = spectral_profile(x)

    solar_fundamental = SOLAR_FUNDAMENTAL_REFERENCE

    harmonic_frequencies = [
        solar_fundamental * k
        for k in range(1, 9)
    ]

    harmonic_assessment = []

    for k, frequency in enumerate(
        harmonic_frequencies,
        start=1,
    ):
        harmonic_assessment.append(
            {
                "harmonic": k,
                "reference_frequency": float(frequency),
                "inside_canonical_band": bool(
                    CANONICAL_BAND[0]
                    <= frequency
                    <= CANONICAL_BAND[1]
                ),
                "nearest_observed_frequency_bin": (
                    float(
                        frequencies[
                            np.argmin(
                                np.abs(
                                    frequencies
                                    - frequency
                                )
                            )
                        ]
                    )
                    if len(frequencies)
                    else None
                ),
            }
        )

    band_summary = summarize_band(
        frequencies,
        power,
        CANONICAL_BAND[0],
        CANONICAL_BAND[1],
    )

    low_band_summary = summarize_band(
        frequencies,
        power,
        0.005,
        0.01,
    )

    broad_band_summary = summarize_band(
        frequencies,
        power,
        0.005,
        0.10,
    )

    result = {
        "scientific_role": "diagnostic_only",
        "claim_support_eligible": False,
        "confirmatory_use": False,

        "dataset": str(DATASET),
        "sample_count": int(len(x)),
        "sampling_frequency_cycles_per_month": FS,

        "canonical_endpoint": {
            "frequency_band": list(CANONICAL_BAND),
            "nperseg": min(1024, len(x)),
            "window": "hann",
            "detrend": "linear",
            "scaling": "density",
            "noverlap_fraction": 0.5,
        },

        "solar_reference": {
            "reference_period_months": (
                SOLAR_PERIOD_MONTHS_REFERENCE
            ),
            "reference_fundamental_frequency": (
                float(solar_fundamental)
            ),
        },

        "harmonic_assessment": harmonic_assessment,

        "spectral_regions": {
            "low_band_0.005_0.01": low_band_summary,
            "canonical_band_0.01_0.05": band_summary,
            "broad_band_0.005_0.10": broad_band_summary,
        },

        "interpretation_policy": {
            "no_endpoint_optimization": True,
            "no_band_selection": True,
            "no_posthoc_claim": True,
            "nuisance_treatment_requires_preconfirmation_rule": True,
            "current_result_does_not_support_or_falsify_claim": True,
        },
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

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
