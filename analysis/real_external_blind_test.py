import requests
import pandas as pd
import numpy as np
import json
import os

from analysis.numerical_spectral_verification import estimate_alpha
from analysis.adaptive_alpha_validator import adaptive_alpha_pass
from analysis.real_null_comparison import run_null_test
from analysis.bootstrap_alpha_stability import (
    bootstrap_alpha_distribution
)
from analysis.independent_validation import compare_methods

URL = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/daily-min-temperatures.csv"

def preflight_check(series):
    fft_alpha, welch_alpha = compare_methods(series)

    if not np.isfinite(fft_alpha) or not np.isfinite(welch_alpha):
        raise SystemExit("❌ invalid alpha from methods")

    if abs(fft_alpha - welch_alpha) > 0.5:
        raise SystemExit("❌ method disagreement — unstable alpha")

    return fft_alpha, welch_alpha
    
def fetch_external():

    local_path = "real-data/daily-min-temperatures.csv"

    if os.path.exists(local_path):

        df = pd.read_csv(local_path)

    else:

        print("🌐 Fetching REAL external data...")

        response = requests.get(
            URL,
            timeout=10
        )

        response.raise_for_status()

        os.makedirs(
            "real-data",
            exist_ok=True
        )

        with open(local_path, "wb") as f:
            f.write(response.content)

        df = pd.read_csv(local_path)

    # normalize column names
    df.columns = [
        str(c).strip().lower()
        for c in df.columns
    ]

    print("Detected columns:", df.columns.tolist())

    candidate_columns = [
        "close",
        "value",
        "temp",
        "temperature",
        "sunspots",
        "signal"
    ]

    selected = None

    for c in candidate_columns:

        if c in df.columns:
            selected = c
            break

    # fallback:
    # first numeric column
    if selected is None:

        numeric_cols = (
            df.select_dtypes(
                include=[np.number]
            ).columns.tolist()
        )

        if len(numeric_cols) > 0:
            selected = numeric_cols[0]

    if selected is None:

        raise ValueError(
            f"No usable numeric column found. "
            f"Columns={df.columns.tolist()}"
        )

    print(
        f"Using column: {selected}"
    )

    values = (
        df[selected]
        .dropna()
        .values
        .astype(np.float64)
    )

    if len(values) < 128:

        raise ValueError(
            "External dataset too small"
        )

    return values

def is_valid_segment(x):
    if np.std(x) < 1e-3:
        return False
    if np.max(x) - np.min(x) < 1e-2:
        return False
    return True

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
    fft_alpha, welch_alpha = preflight_check(data)
    # keep original data, don't overwrite it
    window = 512
    stride = 128
    segments = [
        data[i:i+window]
        for i in range(0, len(data) - window + 1, stride)
    ]
    
    alphas = []

    for seg in segments:
        
        a = estimate_alpha(seg)

        if np.isfinite(a):
            alphas.append(a)

    alphas = np.asarray(
        alphas,
        dtype=np.float64
    )

    if len(alphas) < 3:
        
        raise RuntimeError(
            "Insufficient valid alpha windows"
        )

    # === ROBUST TRAIN/TEST SPLIT ===

    segments = [s for s in segments if is_valid_segment(s)]

    last_k = 3

    train_pool = segments[:-last_k]
    test_pool = segments[-last_k:]

    def safe_alpha(s):
        a = estimate_alpha(s)
        return a if np.isfinite(a) else None

    train_alphas = [safe_alpha(s) for s in train_pool]
    test_alphas = [safe_alpha(s) for s in test_pool]

    train_alphas = [a for a in train_alphas if a is not None]
    test_alphas = [a for a in test_alphas if a is not None]

    if len(train_alphas) < 3 or len(test_alphas) < 2:
        raise RuntimeError("Insufficient robust alpha samples")

    alpha_train = float(np.median(train_alphas))
    alpha_test = float(np.median(test_alphas))

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

    bootstrap = bootstrap_alpha_distribution(
        train_pool,
            np.random.RandomState(42)
    )

    alpha_sigma = bootstrap["std"]

    print(
        "Bootstrap alpha sigma:",
        alpha_sigma
    )

    result = adaptive_alpha_pass(
        alpha_train,
        alpha_test,
        alpha_sigma
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
