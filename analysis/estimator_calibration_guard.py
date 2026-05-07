import json
import numpy as np
import pandas as pd

from analysis.numerical_spectral_verification import (
    estimate_alpha
)

np.random.seed(42)

EXPECTED = [
    ("white", 0.0),
    ("pink", 1.0),
    ("brown", 2.0),
]

N = 2048


def generate_colored_noise(alpha, n):

    freqs = np.fft.rfftfreq(n)

    freqs[0] = freqs[1]

    phases = np.random.normal(
        size=len(freqs)
    ) + 1j * np.random.normal(
        size=len(freqs)
    )

    scaling = 1 / (freqs ** (alpha / 2))

    spectrum = phases * scaling

    x = np.fft.irfft(
        spectrum,
        n=n
    )

    x = (x - np.mean(x)) / np.std(x)

    return x


results = []

for label, target_alpha in EXPECTED:

    x = generate_colored_noise(
        target_alpha,
        N
    )

    estimated = estimate_alpha(x)

    error = abs(
        estimated - target_alpha
    )

    results.append({
        "type": label,
        "target": target_alpha,
        "estimated": float(estimated),
        "abs_error": float(error)
    })

mean_error = np.mean([
    r["abs_error"]
    for r in results
])

report = {
    "mean_abs_error": float(mean_error),
    "results": results
}

with open(
    "artifacts/estimator_calibration.json",
    "w"
) as f:

    json.dump(
        report,
        f,
        indent=2
    )

print(json.dumps(
    report,
    indent=2
))

if mean_error > 0.35:
    raise SystemExit(
        "❌ estimator calibration failed"
    )

print(
    "✅ estimator calibration stable"
)
