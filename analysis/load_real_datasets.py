from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

DATASETS = {
    "sunspots": "real-data/sunspots_full.csv",
    "co2": "real-data/co2_atmospheric_clean.csv",
    "passengers": "real-data/airline_passengers.csv",
    "cosmic_rays": "real-data/cosmic_rays_clean.csv",
    "extended": "real-data/sunspots_global_extended.csv",
    "temperature": "real-data/temperature_global.csv",
    "sp500": "real-data/sp500.csv",
}

def _normalize(series):
    series = pd.to_numeric(
        series,
        errors="coerce",
    )

    series = (
        series
        .replace(
            [np.inf, -np.inf],
            np.nan,
        )
        .dropna()
    )

    if len(series) == 0:
        raise ValueError(
            "no finite numeric observations"
        )

    values = series.to_numpy(
        dtype=np.float64
    )

    mean = float(
        np.mean(values)
    )

    std = float(
        np.std(values)
    )

    if std < 1e-12:
        raise ValueError(
            "degenerate numeric series"
        )

    return (
        (values - mean)
        / std
    )

def load_series(path):
    path = str(path)
    p = Path(path)

    if not p.exists():
        raise ValueError(
            f"Missing file: {path}"
        )

    lower = path.lower()

    # ============================================================
    # CANONICAL SUNSPOT DATASET
    #
    # Format:
    # year;
    # month;
    # decimal_date;
    # monthly_mean_sunspot_number;
    # monthly_std;
    # number_of_observations;
    # indicator
    #
    # The scientific signal is column 3 (zero-based).
    # Metadata/control columns MUST NOT be selected automatically.
    # ============================================================

    if "sunspots_full" in lower:

        df = pd.read_csv(
            p,
            sep=";",
            header=None,
            engine="python",
            on_bad_lines="skip",
        )

        if df.shape[1] < 4:
            raise ValueError(
                "sunspots_full requires at least four columns"
            )

        return _normalize(
            df.iloc[:, 3]
        )

    # ============================================================
    # DERIVED SUNSPOT CONTROL
    # ============================================================

    if "sunspots_global_extended" in lower:

        df = pd.read_csv(p)

        for column in (
            "Sunspots",
            "sunspots",
            "value",
        ):
            if column in df.columns:
                return _normalize(
                    df[column]
                )

        raise ValueError(
            "extended sunspot dataset has no recognised signal column"
        )

    # ============================================================
    # CO2
    # ============================================================

    if "co2_atmospheric_clean" in lower:

        df = pd.read_csv(p)

        if "value" not in df.columns:
            raise ValueError(
                "CO2 dataset requires value column"
            )

        return _normalize(
            df["value"]
        )

    # ============================================================
    # AIRLINE PASSENGERS
    # ============================================================

    if "airline_passengers" in lower:

        df = pd.read_csv(p)

        if "Passengers" not in df.columns:
            raise ValueError(
                "airline dataset requires Passengers column"
            )

        return _normalize(
            df["Passengers"]
        )

    # ============================================================
    # COSMIC RAYS
    # ============================================================

    if "cosmic_rays_clean" in lower:

        df = pd.read_csv(p)

        if "value" not in df.columns:
            raise ValueError(
                "cosmic-ray dataset requires value column"
            )

        return _normalize(
            df["value"]
        )

    # ============================================================
    # GLOBAL TEMPERATURE
    # ============================================================

    if "temperature_global" in lower:

        df = pd.read_csv(
            p,
            skiprows=1,
        )

        if "J-D" not in df.columns:
            raise ValueError(
                "temperature dataset requires J-D column"
            )

        return _normalize(
            df["J-D"]
        )

    # ============================================================
    # S&P 500
    # ============================================================

    if "sp500" in lower:

        df = pd.read_csv(p)

        close_column = next(
            (
                column
                for column in df.columns
                if "close" in str(column).lower()
            ),
            None,
        )

        if close_column is None:
            raise ValueError(
                "SP500 dataset requires a Close column"
            )

        return _normalize(
            df[close_column]
        )

    # ============================================================
    # CONSERVATIVE GENERIC FALLBACK
    #
    # Never select a metadata column simply because it has
    # the largest variance.
    # ============================================================

    df = pd.read_csv(
        p,
        sep=None,
        engine="python",
        quoting=3,
        on_bad_lines="skip",
    )

    df.columns = [
        str(column).strip().lower()
        for column in df.columns
    ]

    excluded_tokens = (
        "date",
        "month",
        "year",
        "count",
        "flag",
        "quality",
        "index",
    )

    preferred_tokens = (
        "value",
        "signal",
        "measurement",
        "close",
        "temperature",
        "passengers",
    )

    preferred = [
        column
        for column in df.columns
        if any(
            token in column
            for token in preferred_tokens
        )
        and not any(
            token in column
            for token in excluded_tokens
        )
    ]

    candidates = (
        preferred
        if preferred
        else [
            column
            for column in df.columns
            if not any(
                token in column
                for token in excluded_tokens
            )
        ]
    )

    for column in candidates:

        series = (
            pd.to_numeric(
                df[column],
                errors="coerce",
            )
            .replace(
                [np.inf, -np.inf],
                np.nan,
            )
            .dropna()
        )

        if len(series) < 80:
            continue

        if (
            np.std(
                series.to_numpy(
                    dtype=np.float64
                )
            )
            < 1e-6
        ):
            continue

        return _normalize(
            series
        )

    raise ValueError(
        f"No valid numeric signal column in {path}"
    )

def load_all():
    output = {}

    for name, path in DATASETS.items():

        try:

            output[name] = load_series(
                path
            )

            print(
                f"Loaded: {name}"
            )

        except Exception as exc:

            print(
                f"Failed: {name} ({exc})"
            )

    return output
