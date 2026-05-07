import requests
import pandas as pd
import numpy as np
import json
import os

from analysis.numerical_spectral_verification import estimate_alpha
from analysis.adaptive_alpha_validator import adaptive_alpha_pass
from analysis.real_null_comparison import run_null_test

URL = "https://raw.githubusercontent.com/datasets/finance-vix/master/data/vix-daily.csv"


def fetch_external():

    local_path = "real-data/vix.csv"

    if os.path.exists(local_path):
        df = pd.read_csv(local_path)

    else:
        print("🌐 Fetching REAL external data...")

        response = requests.get(URL, timeout=10)
        response.raise_for_status()

        os.makedirs("real-data", exist_ok=True)

        with open(local_path, "wb") as f:
            f.write(response.content)

        df = pd.read_csv(local_path)

    df.columns = [c.strip().lower() for c in df.columns]

    for col in df.columns:

        if "close" in col:

            values = (
                df[col]
                .dropna()
                .values
                .astype(np.float64)
            )

            if len(values) < 128:
                raise ValueError(
                    "External dataset too small"
                )

            return values

    raise ValueError("No close column found")


def stable_normalize(x):

    x = np.asarray(x, dtype=np.float64)

    mu = np.mean(x)
    sigma = np.std(x)

    if sigma < 1e-12:
        raise ValueError("Degenerate variance")

    x = (x - mu) / sigma

    return np.asarray(x, dtype=np.float64)


def bind_external_result(classification, values):

    os.makedirs("artifacts", exist_ok=True)

    payload = {
        "type": classification,
        "source": "external_blind_test",
        "length": int(len(values)),
        "mean": float(np.mean(values)),
        "std": float(np.std(values))
    }

    with open(
        "artifacts/external_witness.json",
        "w"
    ) as f:
        json.dump(payload, f, indent=2)


def run_test():

    np.random.seed(42)

    data = fetch_external()

    # 🔥 normalization before analysis
    data = stable_normalize(data)

    split = int(len(data) * 0.7)

    train = data[:split]
    test = data[split:]

    alpha_train = estimate_alpha(train)
    alpha_test = estimate_alpha(test)

    print("Alpha train:", alpha_train)
    print("Alpha test :", alpha_test)

    if not np.isfinite(alpha_train):

        classification = "unmeasurable_train"

        bind_external_result(classification, data)

        raise SystemExit(
            "❌ Invalid train alpha"
        )

    if not np.isfinite(alpha_test):

        classification = "unmeasurable_test"

        bind_external_result(classification, data)

        raise SystemExit(
            "❌ Invalid test alpha"
        )

    sigma_est = np.std(train)

    result = adaptive_alpha_pass(
        alpha_train,
        alpha_test,
        sigma_est
    )

    print("Drift:", result["drift"])
    print("Tolerance:", result["tolerance"])
    print("Relative:", result["relative"])

    if not result["pass"]:

        classification = (
            "adaptive_drift_failure"
        )

        bind_external_result(
            classification,
            data
        )

        raise SystemExit(
            "❌ Adaptive drift validation failed"
        )

    print("✅ Adaptive stability confirmed")

    print("=== NULL MODEL TEST ===")

    # 🔥 run null test on TRAIN regime only
    null_result = run_null_test(train)

    print(
        "Null test result:",
        null_result
    )

    if not null_result["pass"]:

        classification = "noise_like"

        bind_external_result(
            classification,
            data
        )

        with open(
            "artifacts/external_classification.json",
            "w"
        ) as f:

            json.dump({
                "type": classification,
                "alpha": float(
                    null_result["real_alpha"]
                ),
                "z_score": float(
                    null_result["z_score"]
                )
            }, f, indent=2)

        raise SystemExit(
            "❌ Null model not rejected"
        )

    classification = "structured"

    bind_external_result(
        classification,
        data
    )

    with open(
        "artifacts/external_classification.json",
        "w"
    ) as f:

        json.dump({
            "type": classification,
            "alpha": float(
                null_result["real_alpha"]
            ),
            "z_score": float(
                null_result["z_score"]
            )
        }, f, indent=2)

    print(
        "✅ Structure exceeds null expectation"
    )

    print(
        "✅ External blind stability confirmed"
    )


if __name__ == "__main__":
    run_test()
