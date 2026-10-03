from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.signal import welch

from analysis.load_real_datasets import load_series


DATASET = Path("real-data/sunspots_full.csv")
OUTPUT = Path("artifacts/estimator_sensitivity_audit.json")

BANDS = [
    [0.005, 0.05],
    [0.01, 0.03],
    [0.01, 0.05],
    [0.01, 0.10],
    [0.02, 0.10],
    [0.05, 0.20],
]

NPERSEGS = [
    256,
    512,
    1024,
    2048,
]

EXPECTED_ALPHA_RANGE = [0.05, 3.0]
CANONICAL_BAND = [0.01, 0.05]
CANONICAL_NPERSEG = 1024
MIN_BINS = 20


def estimate(series, nperseg, fmin, fmax):
    series = np.asarray(series, dtype=np.float64)

    if series.ndim != 1:
        raise ValueError("series must be one-dimensional")

    if not np.all(np.isfinite(series)):
        raise ValueError("series contains non-finite values")

    if len(series) < nperseg:
        return {
            "finite": False,
            "reason": "series_shorter_than_nperseg",
            "nperseg": int(nperseg),
            "frequency_min": float(fmin),
            "frequency_max": float(fmax),
        }

    freqs, psd = welch(
        series,
        fs=1.0,
        window="hann",
        nperseg=nperseg,
        noverlap=nperseg // 2,
        nfft=nperseg,
        detrend="linear",
        return_onesided=True,
        scaling="density",
        average="mean",
    )

    mask = (
        (freqs >= fmin)
        & (freqs <= fmax)
        & np.isfinite(freqs)
        & np.isfinite(psd)
        & (freqs > 0)
        & (psd > 0)
    )

    bins = int(np.sum(mask))

    if bins < MIN_BINS:
        return {
            "finite": False,
            "reason": "insufficient_frequency_bins",
            "nperseg": int(nperseg),
            "frequency_min": float(fmin),
            "frequency_max": float(fmax),
            "frequency_bins": bins,
        }

    log_frequency = np.log(freqs[mask])
    log_power = np.log(psd[mask])

    slope, intercept = np.polyfit(
        log_frequency,
        log_power,
        1,
    )

    alpha = float(-slope)

    selected_freqs = freqs[mask]
    selected_psd = psd[mask]

    peak_index = int(np.argmax(selected_psd))
    peak_frequency = float(selected_freqs[peak_index])

    median_psd = float(np.median(selected_psd))

    peak_to_median = (
        float(selected_psd[peak_index] / median_psd)
        if median_psd > 0
        else None
    )

    return {
        "finite": bool(np.isfinite(alpha)),
        "nperseg": int(nperseg),
        "frequency_min": float(fmin),
        "frequency_max": float(fmax),
        "frequency_bins": bins,
        "alpha": alpha,
        "peak_frequency_in_band": peak_frequency,
        "peak_to_median_psd_ratio": peak_to_median,
    }


def main():
    series = load_series(str(DATASET))

    results = []

    for band in BANDS:
        fmin, fmax = band

        for nperseg in NPERSEGS:
            result = estimate(
                series,
                nperseg,
                fmin,
                fmax,
            )

            result["canonical_configuration"] = bool(
                nperseg == CANONICAL_NPERSEG
                and band == CANONICAL_BAND
            )

            results.append(result)

    canonical = next(
        item
        for item in results
        if item["canonical_configuration"]
    )

    canonical_alpha = canonical.get("alpha")

    if (
        canonical.get("finite") is not True
        or canonical_alpha is None
        or not np.isfinite(float(canonical_alpha))
    ):
        raise SystemExit(
            "Canonical estimator configuration did not produce "
            "a finite alpha."
        )

    for item in results:
        item["valid"] = bool(
            item.get("finite") is True
            and item.get("alpha") is not None
            and np.isfinite(float(item["alpha"]))
        )

    alpha_in_declared_range = bool(
        result.get("valid") is True
        and EXPECTED_ALPHA_RANGE[0]
        <= float(result["alpha"])
        <= EXPECTED_ALPHA_RANGE[1]
    )

    valid_alphas = [
        float(item["alpha"])
        for item in results
        if item.get("valid") is True
    ]

    if not valid_alphas:
        raise SystemExit(
            "Estimator sensitivity audit produced no valid "
            "alpha configurations."
        )

    minimum_alpha = min(valid_alphas)
    maximum_alpha = max(valid_alphas)

    payload = {
        "schema_version": "1.0",

        "status": "DIAGNOSTIC_ONLY",

        "scientific_claim_authority": False,

        "promotion_authority": False,

        "dataset": {
            "path": str(DATASET),
            "length": int(len(series)),
        },

        "canonical_protocol": {
            "nperseg": CANONICAL_NPERSEG,
            "frequency_band": CANONICAL_BAND,
            "alpha": float(canonical_alpha),
            "minimum_frequency_bins": MIN_BINS,
        },

        "sensitivity_grid": {
            "frequency_bands": BANDS,
            "npersegs": NPERSEGS,
        },

        "results": results,

        "summary": {
            "minimum_alpha": minimum_alpha,
            "maximum_alpha": maximum_alpha,
            "alpha_range": (
                maximum_alpha - minimum_alpha
            ),
            "valid_configurations": len(valid_alphas),
        },

        "interpretation": (
            "This audit evaluates sensitivity of the spectral "
            "exponent to estimator segmentation and frequency "
            "band choices. It does not modify the canonical "
            "endpoint and must not be used to select a favorable "
            "endpoint after observing the result. Any change to "
            "the confirmatory estimator or frequency band requires "
            "an explicitly versioned prospective protocol."
        ),

        "prospective_change_required": True,

        "prospective_rule": (
            "Any future change to the estimator, frequency band, "
            "segmentation rule, or endpoint requires an explicit "
            "protocol revision before fresh confirmation data are "
            "used for claim promotion."
        ),

        "purpose": (
            "Prospective methodological sensitivity audit of the "
            "spectral exponent estimator. This audit does not "
            "modify the canonical endpoint and does not constitute "
            "scientific claim evidence."
        ),
    }

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )

    print(
        "Estimator sensitivity audit written to",
        OUTPUT,
    )

    print(
        "Valid configurations:",
        len(valid_alphas),
    )

    print(
        "Minimum alpha:",
        minimum_alpha,
    )

    print(
        "Maximum alpha:",
        maximum_alpha,
    )

    print(
        "Alpha range:",
        maximum_alpha - minimum_alpha,
    )


if __name__ == "__main__":
    main()
