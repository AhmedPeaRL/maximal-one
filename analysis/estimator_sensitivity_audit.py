from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.signal import welch


DATASET = Path("real-data/sunspots_full.csv")
OUTPUT = Path("artifacts/estimator_sensitivity_audit.json")

CANONICAL_BAND = (0.01, 0.05)
CANONICAL_NPERSEG = 1024
MIN_BINS = 20

BANDS = [
    (0.005, 0.05),
    (0.01, 0.03),
    (0.01, 0.05),
    (0.01, 0.10),
    (0.02, 0.10),
    (0.05, 0.20),
]

NPERSEGS = [
    256,
    512,
    1024,
    2048,
]


def load_sunspots() -> np.ndarray:
    if not DATASET.exists():
        raise FileNotFoundError(
            f"Missing canonical dataset: {DATASET}"
        )

    df = pd.read_csv(
        DATASET,
        sep=";",
        header=None,
        engine="python",
        on_bad_lines="skip",
    )

    if df.shape[1] < 4:
        raise ValueError(
            "sunspots_full.csv must contain the canonical "
            "sunspot signal in column 3."
        )

    values = pd.to_numeric(
        df.iloc[:, 3],
        errors="coerce",
    ).dropna().to_numpy(
        dtype=np.float64
    )

    if len(values) < 128:
        raise ValueError(
            "Canonical dataset is too short."
        )

    if not np.all(np.isfinite(values)):
        raise ValueError(
            "Canonical dataset contains non-finite values."
        )

    return (
        values - np.mean(values)
    ) / np.std(values)


def estimate_alpha(
    series: np.ndarray,
    freq_min: float,
    freq_max: float,
    requested_nperseg: int,
):
    effective_nperseg = min(
        requested_nperseg,
        len(series),
    )

    if effective_nperseg < 128:
        return {
            "valid": False,
            "reason": "effective_nperseg_below_128",
        }

    freqs = np.fft.rfftfreq(
        effective_nperseg
    )

    available_bins = int(
        np.sum(
            (freqs > freq_min)
            &
            (freqs < freq_max)
        )
    )

    if available_bins < MIN_BINS:
        return {
            "valid": False,
            "reason": "fewer_than_minimum_frequency_bins",
            "available_bins": available_bins,
            "effective_nperseg": effective_nperseg,
        }

    noverlap = effective_nperseg // 2

    freqs, psd = welch(
        series,
        nperseg=effective_nperseg,
        noverlap=noverlap,
        nfft=effective_nperseg,
        window="hann",
        detrend="linear",
        scaling="density",
        return_onesided=True,
        average="mean",
    )

    mask = (
        (freqs > freq_min)
        &
        (freqs < freq_max)
        &
        np.isfinite(freqs)
        &
        np.isfinite(psd)
        &
        (psd > 0)
    )

    selected_freqs = freqs[mask]
    selected_psd = psd[mask]

    if len(selected_freqs) < MIN_BINS:
        return {
            "valid": False,
            "reason": "fewer_than_minimum_finite_bins",
            "available_bins": int(len(selected_freqs)),
            "effective_nperseg": effective_nperseg,
        }

    log_f = np.log(selected_freqs)
    log_psd = np.log(selected_psd)

    slope = float(
        np.polyfit(
            log_f,
            log_psd,
            1,
        )[0]
    )

    alpha = float(-slope)

    peak_index = int(
        np.argmax(selected_psd)
    )

    peak_frequency = float(
        selected_freqs[peak_index]
    )

    median_psd = float(
        np.median(selected_psd)
    )

    peak_to_median = (
        float(selected_psd[peak_index])
        / median_psd
        if median_psd > 0
        else None
    )

    return {
        "valid": bool(np.isfinite(alpha)),
        "alpha": alpha,
        "available_bins": int(
            len(selected_freqs)
        ),
        "effective_nperseg": int(
            effective_nperseg
        ),
        "peak_frequency": peak_frequency,
        "peak_to_median_psd": peak_to_median,
    }


def main():
    series = load_sunspots()

    records = []

    for freq_min, freq_max in BANDS:
        for nperseg in NPERSEGS:

            result = estimate_alpha(
                series,
                freq_min,
                freq_max,
                nperseg,
            )

            record = {
                "frequency_band": [
                    float(freq_min),
                    float(freq_max),
                ],
                "requested_nperseg": int(
                    nperseg
                ),
                **result,
            }

            record["is_canonical"] = (
                freq_min == CANONICAL_BAND[0]
                and
                freq_max == CANONICAL_BAND[1]
                and
                nperseg == CANONICAL_NPERSEG
            )

            records.append(record)

    canonical = next(
        r
        for r in records
        if r["is_canonical"]
    )

    valid_alphas = [
        r["alpha"]
        for r in records
        if r.get("valid")
        and np.isfinite(r.get("alpha", np.nan))
    ]

    output = {
        "status": "DIAGNOSTIC_ONLY",
        "scientific_claim_authority": False,
        "promotion_authority": False,

        "purpose": (
            "Prospective methodological sensitivity audit of "
            "the spectral exponent estimator. This audit does "
            "not modify the canonical endpoint and does not "
            "constitute scientific claim evidence."
        ),

        "canonical_protocol": {
            "frequency_band": list(
                CANONICAL_BAND
            ),
            "nperseg": CANONICAL_NPERSEG,
            "minimum_frequency_bins": MIN_BINS,
            "alpha": canonical.get("alpha"),
        },

        "sensitivity_grid": {
            "bands": [
                list(x)
                for x in BANDS
            ],
            "npersegs": NPERSEGS,
        },

        "results": records,

        "summary": {
            "valid_configurations": len(
                valid_alphas
            ),
            "minimum_alpha": (
                float(min(valid_alphas))
                if valid_alphas
                else None
            ),
            "maximum_alpha": (
                float(max(valid_alphas))
                if valid_alphas
                else None
            ),
            "alpha_range": (
                float(max(valid_alphas)
                      - min(valid_alphas))
                if valid_alphas
                else None
            ),
        },

        "interpretation": (
            "Estimator sensitivity is reported rather than "
            "corrected away. A materially different result "
            "under a reasonable alternative band or segmentation "
            "must be treated as methodological sensitivity. "
            "No favorable configuration may replace the canonical "
            "endpoint after observing the data."
        ),

        "prospective_rule": (
            "Any future change to the estimator, frequency band, "
            "segmentation rule, or endpoint requires an explicit "
            "protocol revision before fresh confirmation data are "
            "used for claim promotion."
        ),
    }

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT.write_text(
        json.dumps(
            output,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "Estimator sensitivity audit completed."
    )
    print(
        "Status: DIAGNOSTIC_ONLY"
    )
    print(
        "Canonical alpha:",
        canonical.get("alpha"),
    )


if __name__ == "__main__":
    main()
