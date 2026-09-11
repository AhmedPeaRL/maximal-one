from __future__ import annotations
import json
import os
import numpy as np
import pandas as pd

BASE_DATASET = "real-data/sunspots_full.csv"

EXTENDED_DATASET = (
    "real-data/sunspots_global_extended.csv"
)

WHITE_NOISE = "real-data/white_noise.csv"
RANDOM_WALK = "real-data/random_walk.csv"
SHUFFLED_SUNSPOTS = "real-data/shuffled_sunspots.csv"

PROVENANCE_FILE = (
    "real-data/derived_provenance.json"
)

SEED = 42
CONTROL_LENGTH = 1024
EXTENDED_LENGTH = 3327

def require_base_dataset():
    if not os.path.exists(BASE_DATASET):
        raise SystemExit(
            f"❌ Missing canonical base dataset: "
            f"{BASE_DATASET}"
        )

def load_sunspots():
    df = pd.read_csv(
        BASE_DATASET,
        sep=";",
        engine="python",
        header=None,
    )

    if df.shape[1] < 4:
        raise SystemExit(
            "❌ Canonical sunspot dataset has fewer "
            "than 4 columns"
        )

    series = pd.to_numeric(
        df.iloc[:, 3],
        errors="coerce",
    ).dropna().to_numpy(
        dtype=np.float64
    )

    if len(series) < 300:
        raise SystemExit(
            "❌ Canonical sunspot dataset too short: "
            f"{len(series)}"
        )

    if not np.all(np.isfinite(series)):
        raise SystemExit(
            "❌ Canonical sunspot dataset contains "
            "non-finite values"
        )

    if np.std(series) < 1e-6:
        raise SystemExit(
            "❌ Canonical sunspot dataset is degenerate"
        )

    return series

def build_extended(series):
    """
    Build a deterministic derived control.

    IMPORTANT:
    This dataset is NOT independent evidence.

    When the source contains enough observations, the
    extended dataset is a deterministic prefix of the
    canonical source dataset.

    It MUST NOT be counted as an independent real domain.
    """

    if len(series) >= EXTENDED_LENGTH:

        extended = series[
            :EXTENDED_LENGTH
        ].copy()

        construction = (
            "deterministic_prefix"
        )

        print(
            "ℹ️ Derived dataset constructed as "
            "deterministic prefix of canonical "
            "primary dataset"
        )

    else:

        rng = np.random.default_rng(
            SEED
        )

        chunks = []
        total = 0

        while total < EXTENDED_LENGTH:

            block = int(
                rng.integers(
                    128,
                    256,
                )
            )

            max_start = max(
                1,
                len(series) - block,
            )

            start = int(
                rng.integers(
                    0,
                    max_start,
                )
            )

            segment = series[
                start:
                start + block
            ]

            if len(segment) == 0:
                raise SystemExit(
                    "❌ Failed to construct "
                    "deterministic derived dataset"
                )

            chunks.append(segment)
            total += len(segment)

        extended = np.concatenate(
            chunks
        )[:EXTENDED_LENGTH]

        construction = (
            "deterministic_segment_concatenation"
        )

    extended = np.asarray(
        extended,
        dtype=np.float64,
    )

    if not np.all(
        np.isfinite(extended)
    ):
        raise SystemExit(
            "❌ Derived dataset contains "
            "non-finite values"
        )

    extended = (
        extended -
        np.mean(extended)
    )

    std = np.std(extended)

    if std <= 1e-12:
        raise SystemExit(
            "❌ Derived dataset became degenerate"
        )

    extended = extended / std

    pd.DataFrame(
        {
            "Sunspots": extended
        }
    ).to_csv(
        EXTENDED_DATASET,
        index=False,
    )

    return extended, construction

def build_controls(extended):
    rng = np.random.default_rng(
        SEED
    )

    white_noise = rng.standard_normal(
        CONTROL_LENGTH
    )

    random_walk = np.cumsum(
        rng.standard_normal(
            CONTROL_LENGTH
        )
    )

    shuffled_sunspots = rng.permutation(
        extended
    )

    pd.DataFrame(
        {"value": white_noise}
    ).to_csv(
        WHITE_NOISE,
        index=False,
    )

    pd.DataFrame(
        {"value": random_walk}
    ).to_csv(
        RANDOM_WALK,
        index=False,
    )

    pd.DataFrame(
        {"value": shuffled_sunspots}
    ).to_csv(
        SHUFFLED_SUNSPOTS,
        index=False,
    )

def validate_outputs():
    required = [
        EXTENDED_DATASET,
        WHITE_NOISE,
        RANDOM_WALK,
        SHUFFLED_SUNSPOTS,
    ]

    for path in required:

        if not os.path.exists(path):
            raise SystemExit(
                "❌ Required canonical input was "
                f"not generated: {path}"
            )

        if os.path.getsize(path) <= 0:
            raise SystemExit(
                f"❌ Canonical input is empty: {path}"
            )

    extended = pd.read_csv(
        EXTENDED_DATASET
    )

    if "Sunspots" not in extended.columns:
        raise SystemExit(
            "❌ Extended dataset missing "
            "canonical Sunspots column"
        )

    if len(extended) != EXTENDED_LENGTH:
        raise SystemExit(
            "❌ Extended dataset length mismatch: "
            f"{len(extended)} != {EXTENDED_LENGTH}"
        )

    for path in (
        WHITE_NOISE,
        RANDOM_WALK,
        SHUFFLED_SUNSPOTS,
    ):

        df = pd.read_csv(path)

        if "value" not in df.columns:
            raise SystemExit(
                f"❌ Control dataset missing value "
                f"column: {path}"
            )

        if len(df) < 256:
            raise SystemExit(
                f"❌ Control dataset too short: {path}"
            )

        values = df[
            "value"
        ].to_numpy(
            dtype=np.float64
        )

        if not np.all(
            np.isfinite(values)
        ):
            raise SystemExit(
                "❌ Control dataset contains "
                f"non-finite values: {path}"
            )

def write_provenance(
    source_rows,
    derived_rows,
    construction,
):
    provenance = {
        "dataset": EXTENDED_DATASET,
        "source_dataset": BASE_DATASET,
        "source_rows": int(source_rows),
        "derived_rows": int(derived_rows),
        "seed": SEED,
        "construction": construction,

        "status": "derived_control",

        "independent_real_domain": False,

        "eligible_for_cross_domain_replication": (
            False
        ),

        "eligible_for_primary_claim_evidence": (
            False
        ),

        "interpretation": (
            "This dataset is deterministically derived "
            "from the canonical sunspot dataset and "
            "must never be counted as an independent "
            "real-world replication."
        ),
    }

    with open(
        PROVENANCE_FILE,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            provenance,
            f,
            indent=2,
            sort_keys=True,
        )

def main():
    require_base_dataset()

    os.makedirs(
        "real-data",
        exist_ok=True,
    )

    series = load_sunspots()

    extended, construction = (
        build_extended(series)
    )

    write_provenance(
        source_rows=len(series),
        derived_rows=len(extended),
        construction=construction,
    )

    build_controls(
        extended
    )

    validate_outputs()

    print(
        "✅ Canonical derived inputs prepared"
    )

    print(
        f"   base rows: {len(series)}"
    )

    print(
        f"   extended rows: {len(extended)}"
    )

    print(
        f"   control length: {CONTROL_LENGTH}"
    )

    print(
        f"   deterministic seed: {SEED}"
    )

    print(
        "   replication status: "
        "NOT INDEPENDENT"
    )

if __name__ == "__main__":
    main()
