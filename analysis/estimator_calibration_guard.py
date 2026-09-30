from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from analysis.numerical_spectral_verification import (
    estimate_alpha
)


SEEDS = [
    11,
    42,
    101,
    777,
    2025,
]

TARGETS = [
    ("white", 0.0),
    ("pink", 1.0),
    ("brown", 2.0),
    ("high_2_5", 2.5),
    ("high_3", 3.0),
]

N = 2048


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


def main():
    results = []

    for label, target_alpha in TARGETS:

        for seed in SEEDS:

            rng = np.random.default_rng(seed)

            x = generate_colored_noise(
                target_alpha,
                N,
                rng,
            )

            estimated = float(
                estimate_alpha(x)
            )

            if not np.isfinite(estimated):
                raise SystemExit(
                    f"Non-finite estimator result "
                    f"for {label}, seed={seed}."
                )

            error = (
                estimated
                -
                target_alpha
            )

            results.append({
                "type": label,
                "target": float(target_alpha),
                "seed": int(seed),
                "estimated": estimated,
                "signed_error": float(error),
                "abs_error": float(abs(error)),
            })

    summary = []

    for label, target_alpha in TARGETS:

        subset = [
            r
            for r in results
            if r["type"] == label
        ]

        estimates = np.asarray([
            r["estimated"]
            for r in subset
        ])

        errors = np.asarray([
            r["signed_error"]
            for r in subset
        ])

        summary.append({
            "type": label,
            "target": float(target_alpha),
            "n_replicates": int(len(subset)),
            "mean_estimated": float(
                np.mean(estimates)
            ),
            "bias": float(
                np.mean(errors)
            ),
            "mean_abs_error": float(
                np.mean(np.abs(errors))
            ),
            "std_estimated": float(
                np.std(
                    estimates,
                    ddof=1,
                )
            ),
        })

    report = {
        "protocol": {
            "scientific_role":
                "estimator_methodological_calibration",
            "claim_support": False,
            "targets": [
                float(x[1])
                for x in TARGETS
            ],
            "seeds": SEEDS,
            "n": N,
        },
        "summary": summary,
        "replicates": results,
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
        ),
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
