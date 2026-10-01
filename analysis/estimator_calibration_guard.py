from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from analysis.numerical_spectral_verification import (
    estimate_alpha,
)


# ------------------------------------------------------------
# Methodological estimator calibration
#
# This is NOT scientific evidence.
# It does NOT correct the observed alpha.
# It does NOT establish validity on sunspots.
#
# Each target/replicate receives an independent RNG seed.
# The calibration length matches the canonical primary length.
# ------------------------------------------------------------

BASE_SEED = 910000
REPLICATES_PER_TARGET = 100
N = 3328

TARGETS = [
    ("white", 0.0),
    ("pink", 1.0),
    ("brown", 2.0),
    ("high_2_5", 2.5),
    ("high_3", 3.0),
]


def generate_colored_noise(
    alpha,
    n,
    rng,
):
    freqs = np.fft.rfftfreq(n)

    freqs = np.where(
        freqs == 0,
        freqs[1],
        freqs,
    )

    phases = (
        rng.normal(size=len(freqs))
        +
        1j * rng.normal(size=len(freqs))
    )

    scaling = 1.0 / (
        freqs ** (alpha / 2.0)
    )

    spectrum = phases * scaling

    x = np.fft.irfft(
        spectrum,
        n=n,
    )

    std = np.std(x)

    if not np.isfinite(std) or std <= 1e-12:
        raise RuntimeError(
            "Generated calibration signal has invalid variance."
        )

    return (
        x - np.mean(x)
    ) / std


def confidence_interval_95(
    values,
):
    values = np.asarray(
        values,
        dtype=np.float64,
    )

    if len(values) < 2:
        return None, None

    mean = float(
        np.mean(values)
    )

    std = float(
        np.std(
            values,
            ddof=1,
        )
    )

    se = std / np.sqrt(
        len(values)
    )

    return (
        float(mean - 1.96 * se),
        float(mean + 1.96 * se),
    )


def main():
    results = []

    for target_index, (
        label,
        target_alpha,
    ) in enumerate(TARGETS):

        for replicate in range(
            REPLICATES_PER_TARGET
        ):

            seed = (
                BASE_SEED
                +
                target_index * 100000
                +
                replicate
            )

            rng = np.random.default_rng(
                seed
            )

            x = generate_colored_noise(
                target_alpha,
                N,
                rng,
            )

            estimated = float(
                estimate_alpha(x)
            )

            if not np.isfinite(
                estimated
            ):
                raise SystemExit(
                    (
                        "Estimator calibration produced "
                        "a non-finite estimate: "
                        f"type={label}, "
                        f"target={target_alpha}, "
                        f"replicate={replicate}, "
                        f"seed={seed}"
                    )
                )

            signed_error = (
                estimated
                -
                target_alpha
            )

            results.append({
                "type": label,
                "target": float(target_alpha),
                "replicate": int(replicate),
                "seed": int(seed),
                "estimated": estimated,
                "signed_error": float(
                    signed_error
                ),
                "abs_error": float(
                    abs(signed_error)
                ),
            })

    summary = []

    for label, target_alpha in TARGETS:

        subset = [
            item
            for item in results
            if item["type"] == label
        ]

        estimates = np.asarray(
            [
                item["estimated"]
                for item in subset
            ],
            dtype=np.float64,
        )

        errors = np.asarray(
            [
                item["signed_error"]
                for item in subset
            ],
            dtype=np.float64,
        )

        ci_low, ci_high = (
            confidence_interval_95(
                errors
            )
        )

        summary.append({
            "type": label,
            "target": float(target_alpha),
            "n_replicates": int(
                len(subset)
            ),
            "mean_estimated": float(
                np.mean(estimates)
            ),
            "bias": float(
                np.mean(errors)
            ),
            "bias_ci95_low": ci_low,
            "bias_ci95_high": ci_high,
            "mean_abs_error": float(
                np.mean(
                    np.abs(errors)
                )
            ),
            "std_estimated": float(
                np.std(
                    estimates,
                    ddof=1,
                )
            ),
            "min_estimated": float(
                np.min(estimates)
            ),
            "max_estimated": float(
                np.max(estimates)
            ),
        })

    report = {
        "status": "CALIBRATION_COMPLETE_REQUIRES_REVIEW",

        "protocol": {
            "scientific_role":
                "estimator_methodological_calibration",

            "claim_support":
                False,

            "observed_alpha_correction_allowed":
                False,

            "targets": [
                float(target)
                for _, target in TARGETS
            ],

            "replicates_per_target":
                REPLICATES_PER_TARGET,

            "total_replicates":
                len(results),

            "n":
                N,

            "seed_scheme":
                "independent_seed_per_target_and_replicate",

            "base_seed":
                BASE_SEED,

            "generator":
                "finite_sample_fft_colored_noise",

            "primary_process_validity_established":
                False,

            "interpretation":
                (
                    "This calibration quantifies finite-sample "
                    "behavior of the canonical estimator on a "
                    "declared synthetic colored-noise generator. "
                    "It does not establish estimator validity on "
                    "the primary real process, does not justify "
                    "post-hoc correction of observed alpha, and "
                    "does not support scientific claim promotion."
                ),
        },

        "summary":
            summary,

        "replicates":
            results,
    }

    output = Path(
        "artifacts/estimator_calibration.json"
    )

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output.write_text(
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
