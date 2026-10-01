from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from analysis.numerical_spectral_verification import (
    estimate_alpha,
)


PRIMARY_PATH = Path(
    "real-data/sunspots_full.csv"
)

OUTPUT = Path(
    "artifacts/estimator_sensitivity_audit.json"
)

SEED = 20261001

BANDS = [
    {
        "name": "canonical",
        "freq_min": 0.01,
        "freq_max": 0.05,
    },
    {
        "name": "wider_low",
        "freq_min": 0.005,
        "freq_max": 0.05,
    },
    {
        "name": "narrow_low",
        "freq_min": 0.01,
        "freq_max": 0.03,
    },
    {
        "name": "wider",
        "freq_min": 0.01,
        "freq_max": 0.10,
    },
    {
        "name": "mid",
        "freq_min": 0.02,
        "freq_max": 0.10,
    },
    {
        "name": "higher",
        "freq_min": 0.05,
        "freq_max": 0.20,
    },
]


def load_primary():
    df = pd.read_csv(
        PRIMARY_PATH,
        sep=";",
        header=None,
        engine="python",
        on_bad_lines="skip",
    )

    if df.shape[1] < 4:
        raise SystemExit(
            "Estimator sensitivity audit: "
            "primary dataset has fewer than four columns."
        )

    x = pd.to_numeric(
        df.iloc[:, 3],
        errors="coerce",
    ).dropna().to_numpy(
        dtype=np.float64
    )

    if len(x) < 256:
        raise SystemExit(
            "Estimator sensitivity audit: "
            "primary series is too short."
        )

    if not np.all(np.isfinite(x)):
        raise SystemExit(
            "Estimator sensitivity audit: "
            "primary series contains non-finite values."
        )

    return x


def estimate_with_band(
    x,
    freq_min,
    freq_max,
):
    return estimate_alpha(
        x,
        freq_min=freq_min,
        freq_max=freq_max,
    )


def half_series_sensitivity(
    x,
    freq_min,
    freq_max,
):
    half = x[: len(x) // 2]

    full_alpha = estimate_with_band(
        x,
        freq_min,
        freq_max,
    )

    half_alpha = estimate_with_band(
        half,
        freq_min,
        freq_max,
    )

    if not (
        np.isfinite(full_alpha)
        and np.isfinite(half_alpha)
    ):
        return {
            "full_alpha": None,
            "half_alpha": None,
            "absolute_difference": None,
        }

    return {
        "full_alpha": float(full_alpha),
        "half_alpha": float(half_alpha),
        "absolute_difference": float(
            abs(
                float(full_alpha)
                -
                float(half_alpha)
            )
        ),
    }


def main():

    x = load_primary()

    results = []

    canonical_alpha = None

    for item in BANDS:

        sensitivity = half_series_sensitivity(
            x,
            item["freq_min"],
            item["freq_max"],
        )

        alpha = sensitivity["full_alpha"]

        if item["name"] == "canonical":
            canonical_alpha = alpha

        results.append({
            "name": item["name"],
            "freq_min": item["freq_min"],
            "freq_max": item["freq_max"],
            "alpha": alpha,
            "half_series": sensitivity,
        })

    nperseg_sensitivity = []

    # This section intentionally uses scipy directly.
    # It does not modify the canonical estimator.
    from scipy.signal import welch

    x0 = x - np.mean(x)
    std = np.std(x0)

    if std <= 1e-12:
        raise SystemExit(
            "Estimator sensitivity audit: "
            "primary variance is degenerate."
        )

    x0 = x0 / std

    for nperseg in [256, 512, 1024, 2048]:

        effective = min(
            int(nperseg),
            len(x0),
        )

        if effective < 128:
            nperseg_sensitivity.append({
                "requested_nperseg": int(nperseg),
                "effective_nperseg": int(effective),
                "alpha": None,
                "status": "too_short",
            })
            continue

        freqs, psd = welch(
            x0,
            nperseg=effective,
            noverlap=effective // 2,
            nfft=effective,
            window="hann",
            detrend="linear",
            scaling="density",
            return_onesided=True,
            average="mean",
        )

        mask = (
            (freqs > 0.01)
            &
            (freqs < 0.05)
            &
            np.isfinite(freqs)
            &
            np.isfinite(psd)
            &
            (psd > 0)
        )

        selected_f = freqs[mask]
        selected_psd = psd[mask]

        if len(selected_f) < 20:
            nperseg_sensitivity.append({
                "requested_nperseg": int(nperseg),
                "effective_nperseg": int(effective),
                "alpha": None,
                "frequency_bins": int(len(selected_f)),
                "status": "insufficient_frequency_bins",
            })
            continue

        coeffs = np.polyfit(
            np.log(selected_f),
            np.log(selected_psd),
            1,
        )

        alpha = float(-coeffs[0])

        nperseg_sensitivity.append({
            "requested_nperseg": int(nperseg),
            "effective_nperseg": int(effective),
            "alpha": alpha,
            "frequency_bins": int(len(selected_f)),
            "status": "valid",
        })

    valid_band_alphas = [
        item["alpha"]
        for item in results
        if item["alpha"] is not None
    ]

    band_range = None

    if valid_band_alphas:
        band_range = float(
            max(valid_band_alphas)
            -
            min(valid_band_alphas)
        )

    valid_segment_alphas = [
        item["alpha"]
        for item in nperseg_sensitivity
        if item["alpha"] is not None
    ]

    segment_range = None

    if valid_segment_alphas:
        segment_range = float(
            max(valid_segment_alphas)
            -
            min(valid_segment_alphas)
        )

    report = {
        "status": "DIAGNOSTIC_ONLY",

        "scientific_claim_authority": False,

        "claim_support": False,

        "protocol": {
            "primary_dataset": str(
                PRIMARY_PATH
            ),
            "seed": SEED,
            "canonical_frequency_band": [
                0.01,
                0.05,
            ],
            "canonical_nperseg": 1024,
            "purpose": (
                "Quantify estimator sensitivity without "
                "changing the canonical estimator or "
                "selecting a preferred result post hoc."
            ),
        },

        "canonical_alpha": canonical_alpha,

        "frequency_band_sensitivity": {
            "results": results,
            "alpha_range": band_range,
        },

        "nperseg_sensitivity": {
            "results": nperseg_sensitivity,
            "alpha_range": segment_range,
        },

        "interpretation": {
            "canonical_result_is_not_replaced": True,
            "posthoc_parameter_selection_prohibited": True,
            "posthoc_alpha_correction_prohibited": True,
            "sensitivity_is_not_replication": True,
            "sensitivity_is_not_null_rejection": True,
            "sensitivity_is_not_claim_support": True,
        },

        "next_protocol_requirement": (
            "Any confirmatory estimator settings must be "
            "declared before fresh confirmation data are "
            "analyzed. The present audit is post-observation "
            "and cannot be represented as preregistered "
            "confirmation."
        ),
    }

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT.write_text(
        json.dumps(
            report,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            report,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
