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

URL = (
    "https://raw.githubusercontent.com/"
    "jbrownlee/Datasets/master/"
    "daily-min-temperatures.csv"
)

WINDOW = 512
STRIDE = 128
TRAIN_RATIO = 0.80

MIN_TRAIN_WINDOWS = 3
MIN_TEST_WINDOWS = 2

def preflight_check(series):
    result = compare_methods(series)

    if not isinstance(result, dict):
        raise SystemExit(
            "compare_methods() returned an unexpected object"
        )

    required_keys = {
        "welch_alpha",
        "fft_alpha",
        "delta",
        "finite",
        "agreement",
        "threshold",
    }

    missing = required_keys - set(result.keys())

    if missing:
        raise SystemExit(
            "compare_methods() missing required fields: "
            + ", ".join(sorted(missing))
        )

    fft_alpha = float(result["fft_alpha"])
    welch_alpha = float(result["welch_alpha"])
    delta = float(result["delta"])

    if not (
        np.isfinite(fft_alpha)
        and np.isfinite(welch_alpha)
        and np.isfinite(delta)
    ):
        raise SystemExit(
            "invalid alpha from methods"
        )

    if delta > 0.50:
        raise SystemExit(
            "method disagreement — unstable alpha"
        )

    print(
        "Training preflight:",
        f"FFT={fft_alpha}",
        f"Welch={welch_alpha}",
        f"delta={delta}"
    )

    return fft_alpha, welch_alpha

def fetch_external():
    local_path = (
        "real-data/"
        "daily-min-temperatures.csv"
    )

    if os.path.exists(local_path):
        df = pd.read_csv(local_path)

    else:
        print("Fetching REAL external data...")

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

    df.columns = [
        str(c).strip().lower()
        for c in df.columns
    ]

    print(
        "Detected columns:",
        df.columns.tolist()
    )

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
            "No usable numeric column found. "
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

    if len(values) < WINDOW * 4:
        raise ValueError(
            "External dataset too small for temporal holdout"
        )

    if not np.all(np.isfinite(values)):
        raise ValueError(
            "External dataset contains non-finite values"
        )

    return values

def is_valid_segment(x):
    x = np.asarray(
        x,
        dtype=np.float64
    )

    if len(x) < WINDOW:
        return False

    if not np.all(np.isfinite(x)):
        return False

    if np.std(x) < 1e-3:
        return False

    if np.max(x) - np.min(x) < 1e-2:
        return False

    return True

def make_windows(series):
    series = np.asarray(
        series,
        dtype=np.float64
    )

    windows = [
        series[i:i + WINDOW]
        for i in range(
            0,
            len(series) - WINDOW + 1,
            STRIDE
        )
    ]

    return [
        s
        for s in windows
        if is_valid_segment(s)
    ]

def minimum_series_length_for_windows(
    window,
    stride,
    required_windows
):
    if required_windows < 1:
        raise ValueError(
            "required_windows must be >= 1"
        )

    return (
        window
        + (required_windows - 1) * stride
    )

def bind_external_result(
    classification,
    values,
    metadata=None
):
    os.makedirs(
        "artifacts",
        exist_ok=True
    )

    payload = {
        "type": classification,
        "source": "external_blind_test",
        "length": int(len(values)),
        "mean": float(np.mean(values)),
        "std": float(np.std(values))
    }

    if metadata is not None:
        payload["metadata"] = metadata

    with open(
        "artifacts/external_witness.json",
        "w"
    ) as f:
        json.dump(
            payload,
            f,
            indent=2
        )

def write_external_classification(
    classification,
    alpha,
    z_score
):
    os.makedirs(
        "artifacts",
        exist_ok=True
    )

    with open(
        "artifacts/external_classification.json",
        "w"
    ) as f:
        json.dump(
            {
                "type": classification,
                "alpha": float(alpha),
                "z_score": float(z_score)
            },
            f,
            indent=2
        )

def run_test():
    np.random.seed(42)

    data = fetch_external()

    if not np.isfinite(np.std(data)):
        raise SystemExit(
            "degenerate external data"
        )

    if np.std(data) < 1e-6:
        raise SystemExit(
            "degenerate external data"
        )

    # ========================================================
    # TRUE TEMPORAL HOLDOUT
    # ========================================================
    #
    # The raw external series is split BEFORE any windowing.
    #
    # Training occupies the first 80%.
    # Testing occupies the final 20%.
    #
    # Therefore no training window can overlap a test window.
    #
    # No preprocessing is fitted on the complete series.
    #
    # The canonical spectral estimator performs its own
    # centering and variance normalization.
    #

    split_index = int(
        len(data) * TRAIN_RATIO
    )

    train_raw = data[:split_index]
    test_raw = data[split_index:]

    minimum_train_length = (
        minimum_series_length_for_windows(
            WINDOW,
            STRIDE,
            MIN_TRAIN_WINDOWS
        )
    )

    minimum_test_length = (
        minimum_series_length_for_windows(
            WINDOW,
            STRIDE,
            MIN_TEST_WINDOWS
        )
    )

    if len(train_raw) < minimum_train_length:
        raise RuntimeError(
            "Insufficient raw training data: "
            f"{len(train_raw)} < "
            f"{minimum_train_length}"
        )

    if len(test_raw) < minimum_test_length:
        raise RuntimeError(
            "Insufficient raw test data: "
            f"{len(test_raw)} < "
            f"{minimum_test_length}"
        )

    train_pool = make_windows(
        train_raw
    )

    test_pool = make_windows(
        test_raw
    )

    if len(train_pool) < MIN_TRAIN_WINDOWS:
        raise RuntimeError(
            "Insufficient valid training windows: "
            f"{len(train_pool)} < "
            f"{MIN_TRAIN_WINDOWS}"
        )

    if len(test_pool) < MIN_TEST_WINDOWS:
        raise RuntimeError(
            "Insufficient valid held-out test windows: "
            f"{len(test_pool)} < "
            f"{MIN_TEST_WINDOWS}"
        )

    print(
        "External total length:",
        len(data)
    )

    print(
        "Temporal split index:",
        split_index
    )

    print(
        "Training length:",
        len(train_raw)
    )

    print(
        "Held-out test length:",
        len(test_raw)
    )

    print(
        "Minimum training length:",
        minimum_train_length
    )

    print(
        "Minimum held-out test length:",
        minimum_test_length
    )

    print(
        "Training windows:",
        len(train_pool)
    )

    print(
        "Held-out test windows:",
        len(test_pool)
    )

    # ========================================================
    # TRAIN-ONLY PREFLIGHT
    # ========================================================

    train_series = np.concatenate(
        train_pool
    )

    preflight_check(
        train_series
    )

    def safe_alpha(series):
        alpha = estimate_alpha(series)

        if np.isfinite(alpha):
            return float(alpha)

        return None

    train_alphas = [
        safe_alpha(s)
        for s in train_pool
    ]

    test_alphas = [
        safe_alpha(s)
        for s in test_pool
    ]

    train_alphas = [
        a
        for a in train_alphas
        if a is not None
    ]

    test_alphas = [
        a
        for a in test_alphas
        if a is not None
    ]

    if len(train_alphas) < MIN_TRAIN_WINDOWS:
        raise RuntimeError(
            "Insufficient robust alpha training samples"
        )

    if len(test_alphas) < MIN_TEST_WINDOWS:
        raise RuntimeError(
            "Insufficient robust alpha test samples"
        )

    alpha_train = float(
        np.median(train_alphas)
    )

    alpha_test = float(
        np.median(test_alphas)
    )

    print(
        "Alpha train:",
        alpha_train
    )

    print(
        "Alpha test :",
        alpha_test
    )

    if not np.isfinite(alpha_train):
        classification = (
            "unmeasurable_train"
        )

        bind_external_result(
            classification,
            data
        )

        raise SystemExit(
            "Invalid train alpha"
        )

    if not np.isfinite(alpha_test):
        classification = (
            "unmeasurable_test"
        )

        bind_external_result(
            classification,
            data
        )

        raise SystemExit(
            "Invalid test alpha"
        )

    # ========================================================
    # TRAIN-ONLY BOOTSTRAP
    # ========================================================

    bootstrap = bootstrap_alpha_distribution(
        train_series,
        np.random.RandomState(42)
    )

    alpha_sigma = bootstrap.get(
        "std",
        np.nan
    )

    if not np.isfinite(alpha_sigma):
        raise SystemExit(
            "Invalid bootstrap sigma"
        )

    print(
        "Bootstrap alpha sigma:",
        alpha_sigma
    )

    # ========================================================
    # PREDECLARED ADAPTIVE DRIFT TEST
    # ========================================================

    result = adaptive_alpha_pass(
        alpha_train,
        alpha_test,
        alpha_sigma
    )

    print(
        "Drift:",
        result["drift"]
    )

    print(
        "Tolerance:",
        result["tolerance"]
    )

    print(
        "Relative:",
        result["relative"]
    )

    metadata = {
        "train_ratio": TRAIN_RATIO,
        "window": WINDOW,
        "stride": STRIDE,
        "minimum_train_windows": MIN_TRAIN_WINDOWS,
        "minimum_test_windows": MIN_TEST_WINDOWS,
        "minimum_train_length": minimum_train_length,
        "minimum_test_length": minimum_test_length,
        "train_windows": len(train_pool),
        "test_windows": len(test_pool),
        "alpha_train": alpha_train,
        "alpha_test": alpha_test,
        "alpha_sigma": float(alpha_sigma),
        "drift": float(result["drift"]),
        "tolerance": float(result["tolerance"]),
        "relative": float(result["relative"]),
        "validator_reason": result["reason"]
    }

    if not result["pass"]:
        classification = (
            "adaptive_drift_failure"
        )

        bind_external_result(
            classification,
            data,
            metadata
        )

        raise SystemExit(
            "Adaptive drift validation failed"
        )

    print(
        "Adaptive stability confirmed"
    )

    # ========================================================
    # NULL MODEL TEST
    # ========================================================

    print(
        "=== NULL MODEL TEST ==="
    )

    null_result = run_null_test(
        train_series
    )

    print(
        "Null test result:",
        null_result
    )

    if not null_result["pass"]:
        classification = "noise_like"

        bind_external_result(
            classification,
            data,
            metadata
        )

        write_external_classification(
            classification,
            null_result["real_alpha"],
            null_result["z_score"]
        )

        raise SystemExit(
            "Null model not rejected"
        )

    classification = "structured"

    bind_external_result(
        classification,
        data,
        metadata
    )

    write_external_classification(
        classification,
        null_result["real_alpha"],
        null_result["z_score"]
    )

    print(
        "Structure exceeds null expectation"
    )

    print(
        "External blind stability confirmed"
    )

if __name__ == "__main__":
    run_test()
