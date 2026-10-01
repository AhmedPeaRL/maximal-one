from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

from analysis.load_real_datasets import load_series
from analysis.strong_null_model import permutation_null
from analysis.numerical_spectral_verification import estimate_alpha


DATASET = Path(
    "real-data/sunspots_full.csv"
)

OUTPUT = Path(
    "artifacts/permutation_determinism_audit.json"
)

SEED = 303
TRIALS = 400


def stable_digest(values):
    payload = json.dumps(
        values,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")

    return hashlib.sha256(
        payload
    ).hexdigest()


def run_once(series):
    rng = np.random.default_rng(
        SEED
    )

    alphas = []

    for _ in range(TRIALS):

        sample = permutation_null(
            series,
            rng,
        )

        alpha = estimate_alpha(
            sample
        )

        if np.isfinite(alpha):
            alphas.append(
                float(
                    np.round(
                        float(alpha),
                        8,
                    )
                )
            )

    if not alphas:
        raise RuntimeError(
            "No finite permutation alpha values produced."
        )

    mean = float(
        np.round(
            np.mean(alphas),
            8,
        )
    )

    std = float(
        np.round(
            np.std(alphas),
            8,
        )
    )

    return {
        "count": len(alphas),
        "mean_alpha": mean,
        "std_alpha": std,
        "first_values": alphas[:20],
        "digest": stable_digest(
            alphas
        ),
    }


def main():

    if not DATASET.exists():
        raise SystemExit(
            f"Missing dataset: {DATASET}"
        )

    series = load_series(
        DATASET
    )

    first = run_once(
        series
    )

    second = run_once(
        series
    )

    exact_match = (
        first["digest"]
        ==
        second["digest"]
    )

    report = {
        "status": (
            "DETERMINISTIC_WITHIN_RUN"
            if exact_match
            else "NONDETERMINISTIC_WITHIN_RUN"
        ),
        "scientific_claim_authority": False,
        "promotion_authority": False,
        "scientific_role": "diagnostic_only",
        "dataset": str(DATASET),
        "seed": SEED,
        "trials": TRIALS,
        "first": first,
        "second": second,
        "exact_digest_match": exact_match,
        "interpretation": (
            "This audit tests deterministic replay of the "
            "same permutation diagnostic within the same "
            "runtime. It does not establish scientific "
            "significance, replication, or cross-platform "
            "reproducibility."
        ),
    }

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT.write_text(
        json.dumps(
            report,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "=== PERMUTATION DETERMINISM AUDIT ==="
    )

    print(
        "Exact digest match:",
        exact_match,
    )

    if not exact_match:
        raise SystemExit(
            "Permutation diagnostic is not deterministic "
            "under identical seed and runtime conditions."
        )


if __name__ == "__main__":
    main()
