from __future__ import annotations
import numpy as np

def autocorrelation(
    x,
    lag=1,
):
    x = np.asarray(
        x,
        dtype=np.float64,
    )

    if (
        x.ndim != 1
        or
        len(x) < lag + 2
        or
        not np.all(np.isfinite(x))
    ):
        return np.nan

    a = x[:-lag]
    b = x[lag:]

    if (
        np.std(a) < 1e-12
        or
        np.std(b) < 1e-12
    ):
        return np.nan

    value = np.corrcoef(
        a,
        b,
    )[0, 1]

    return (
        float(value)
        if np.isfinite(value)
        else np.nan
    )

def distribution_entropy(
    x,
    bins=50,
):
    x = np.asarray(
        x,
        dtype=np.float64,
    )

    if (
        x.ndim != 1
        or
        len(x) < bins
        or
        not np.all(np.isfinite(x))
    ):
        return np.nan

    hist, _ = np.histogram(
        x,
        bins=bins,
    )

    total = np.sum(hist)

    if total <= 0:
        return np.nan

    p = (
        hist.astype(np.float64)
        /
        float(total)
    )

    p = p[p > 0]

    return float(
        -np.sum(
            p * np.log(p)
        )
    )

def predictability_score(series):
    series = np.asarray(
        series,
        dtype=np.float64,
    )

    if (
        series.ndim != 1
        or
        len(series) < 50
        or
        not np.all(np.isfinite(series))
    ):
        return np.nan

    ac = autocorrelation(
        series,
        lag=1,
    )

    entropy = distribution_entropy(
        series
    )

    if not (
        np.isfinite(ac)
        and
        np.isfinite(entropy)
    ):
        return np.nan

    return float(
        abs(ac)
    )


def is_predictable(
    series,
    threshold=0.05,
):
    score = predictability_score(
        series
    )

    if not np.isfinite(score):
        return False, np.nan

    return (
        bool(score > threshold),
        float(score),
    )
