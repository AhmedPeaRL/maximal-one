from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

COLUMN_ALIASES = (
    "value",
    "Value",
    "value_mean",
    "signal",
    "Signal",
    "Sunspots",
    "sunspots",
    "random_walk",
    "white_noise",
)

def _read_candidates(path: str | Path) -> list[pd.DataFrame]:
    path = Path(path)

    candidates = []

    # Standard comma-separated CSV.
    try:
        candidates.append(
            pd.read_csv(path)
        )
    except Exception:
        pass

    # Semicolon-separated CSV, including files with no reliable header.
    try:
        candidates.append(
            pd.read_csv(
                path,
                sep=";",
                engine="python",
            )
        )
    except Exception:
        pass

    # Fully raw / headerless semicolon format.
    try:
        candidates.append(
            pd.read_csv(
                path,
                sep=";",
                header=None,
                engine="python",
            )
        )
    except Exception:
        pass

    return candidates

def _numeric_named_column(df: pd.DataFrame) -> np.ndarray | None:
    for name in COLUMN_ALIASES:
        if name in df.columns:
            values = pd.to_numeric(
                df[name],
                errors="coerce",
            ).dropna().to_numpy(dtype=np.float64)

            if len(values) > 0:
                return values

    return None


def _numeric_column_from_frame(df: pd.DataFrame) -> np.ndarray | None:
    numeric = df.apply(
        pd.to_numeric,
        errors="coerce",
    )

    candidates = []

    for col in numeric.columns:
        values = numeric[col].dropna().to_numpy(
            dtype=np.float64
        )

        if len(values) >= 32:
            candidates.append(values)

    if not candidates:
        return None

    # Prefer the longest valid numeric column.
    return max(
        candidates,
        key=len,
    )

def load_numeric_series(
    path: str | Path,
    *,
    min_length: int = 256,
) -> np.ndarray:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}"
        )

    for df in _read_candidates(path):

        values = _numeric_named_column(df)

        if values is None:
            values = _numeric_column_from_frame(df)

        if values is None:
            continue

        values = np.asarray(
            values,
            dtype=np.float64,
        )

        values = values[np.isfinite(values)]

        if len(values) < min_length:
            continue

        if np.std(values) <= 1e-12:
            continue

        return values

    raise ValueError(
        f"No valid numeric series found in {path}"
    )

def describe_dataset(path: str | Path) -> dict:
    series = load_numeric_series(path)

    return {
        "dataset": str(path),
        "rows": int(len(series)),
        "mean": float(np.mean(series)),
        "std": float(np.std(series)),
        "min": float(np.min(series)),
        "max": float(np.max(series)),
    }
