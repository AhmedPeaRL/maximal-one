from __future__ import annotations

import json
from pathlib import Path
import numpy as np

from analysis.load_real_datasets import DATASETS, load_series
from analysis.numerical_spectral_verification import estimate_alpha

OUTPUT = Path(
    "artifacts/independent_domain_replication_gate.json"
)

REQUIRED_DOMAINS = [
    "co2",
    "cosmic_rays",
]

MIN_REQUIRED = 2

def finite(x):
    try:
        return bool(np.isfinite(float(x)))
    except Exception:
        return False

def evaluate_domain(name):
    path = DATASETS[name]

    try:
        x = load_series(path)

        alpha = estimate_alpha(x)

        return {
            "name": name,
            "path": path,
            "rows": int(len(x)),
            "alpha": (
                float(alpha)
                if finite(alpha)
                else None
            ),
            "measurement_valid": finite(alpha),
            "scientific_replication": False,
            "replication_status": (
                "NOT_TESTED"
            ),
            "reason": (
                "A valid alpha measurement alone "
                "does not constitute replication. "
                "The domain must pass the same primary "
                "stochastic-null test independently."
            ),
        }

    except Exception as exc:
        return {
            "name": name,
            "path": path,
            "rows": None,
            "alpha": None,
            "measurement_valid": False,
            "scientific_replication": False,
            "replication_status": "INVALID_MEASUREMENT",
            "reason": str(exc),
        }

def main():
    domains = [
        evaluate_domain(name)
        for name in REQUIRED_DOMAINS
    ]

    passed = sum(
        1
        for item in domains
        if item["scientific_replication"] is True
    )

    report = {
        "status": (
            "REPLICATION_NOT_ESTABLISHED"
            if passed < MIN_REQUIRED
            else "REPLICATION_ESTABLISHED"
        ),
        "scientific_claim_authority": False,
        "minimum_required": MIN_REQUIRED,
        "passed_independent_domains": passed,
        "domains": domains,
        "interpretation": (
            "Independent real-domain replication requires "
            "independent rejection of the same declared "
            "primary stochastic null under the same endpoint "
            "and direction. Measurement validity alone is "
            "never counted as replication."
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
        ) + "\n",
        encoding="utf-8",
    )

    print(
        "=== INDEPENDENT DOMAIN REPLICATION GATE ==="
    )

    print(
        "Passed independent domains:",
        passed,
    )

    print(
        "Required:",
        MIN_REQUIRED,
    )

    print(
        "Status:",
        report["status"],
    )

    print(
        "Saved:",
        OUTPUT,
    )

if __name__ == "__main__":
    main()
