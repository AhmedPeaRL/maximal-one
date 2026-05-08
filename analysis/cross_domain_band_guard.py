import os
import numpy as np
import pandas as pd

from analysis.numerical_spectral_verification import (
    estimate_alpha
)

DATA_DIR = "real-data"


def load_numeric_series(path):

    df = pd.read_csv(path)

    for col in df.columns:

        if pd.api.types.is_numeric_dtype(
            df[col]
        ):

            x = (
                df[col]
                .dropna()
                .values
            )

            if len(x) < 64:
                continue

            x = np.asarray(
                x,
                dtype=np.float64
            )

            std = np.std(x)

            if std < 1e-8:
                continue

            x = (
                x - np.mean(x)
            ) / std

            return x

    return None


def main():

    alphas = []

    for file in os.listdir(DATA_DIR):

        if not file.endswith(".csv"):
            continue

        path = os.path.join(
            DATA_DIR,
            file
        )

        try:

            series = load_numeric_series(
                path
            )

            if series is None:
                continue

            alpha = estimate_alpha(
                series
            )

            if not np.isfinite(alpha):
                continue

            # reject saturation artifacts
            if alpha >= 4.95:
                continue

            alphas.append(alpha)

            print(
                f"{file}: {alpha:.6f}"
            )

        except Exception as e:

            print(
                f"{file}: skipped ({e})"
            )

    if len(alphas) < 5:

        raise SystemExit(
            "❌ insufficient valid datasets"
        )

    median = float(
        np.median(alphas)
    )

    std = float(
        np.std(alphas)
    )

    print("\nBand summary")
    print("Median:", median)
    print("STD:", std)

    if std > 1.25:
        raise SystemExit(
            "❌ cross-domain instability"
        )

    print(
        "✅ Cross-domain band holds"
    )


if __name__ == "__main__":
    main()
