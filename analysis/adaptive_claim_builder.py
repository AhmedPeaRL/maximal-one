from __future__ import annotations
import json
from pathlib import Path

REPORT_PATH = Path(
    "artifacts/canonical_report.json"
)

OUTPUT_PATH = Path(
    "artifacts/exploration_claim.json"
)

def main():
    if not REPORT_PATH.exists():
        raise SystemExit(
            "❌ canonical_report.json is missing"
        )

    with REPORT_PATH.open(
        "r",
        encoding="utf-8",
    ) as f:
        report = json.load(f)

    alpha = float(
        report["spectral_profile"]["estimated_alpha"]
    )

    sigma = float(
        report["spectral_profile"]["bootstrap_std"]
    )

    margin = 0.03

    claim = {
        "role": "exploration_only",
        "authoritative": False,
        "scientific_proof_allowed": False,
        "source": "observed_report",
        "expected_result": {
            "alpha_range": [
                alpha - margin,
                alpha + margin,
            ],
            "max_sigma": max(
                0.05,
                sigma * 1.5,
            ),
        },
        "epistemic_guard": {
            "adaptive_truth_threshold": True,
            "allowed_for_scientific_proof": False,
            "allowed_for_exploration": True,
            "overwrites_strict_claim": False,
        },
    }

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_PATH.open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            claim,
            f,
            indent=2,
            sort_keys=True,
        )

    print(
        "Exploration claim generated:",
        OUTPUT_PATH,
    )

    print(
        "Scientific proof contract unchanged:"
        " core-scientific/strict_claim.json"
    )

if __name__ == "__main__":
    main()
