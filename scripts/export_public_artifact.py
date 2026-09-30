import json
import os
import shutil
from datetime import datetime, timezone


CANONICAL = "artifacts/canonical_report.json"
OUTPUT = "public/artifact.json"


def load_json(path):
    if not os.path.exists(path):
        return None

    with open(
        path,
        encoding="utf-8"
    ) as f:
        return json.load(f)


def build_artifact():
    report = load_json(
        CANONICAL
    )

    if report is None:
        raise RuntimeError(
            "canonical_report.json is required"
        )

    scientific = report.get(
        "scientific_interpretation",
        {}
    )

    primary_null = report.get(
        "appropriate_stochastic_null",
        {}
    )

    artifact = {
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),

        "scientific_claim": {
            "status":
                scientific.get(
                    "claim_status",
                    "under_investigation"
                ),

            "claim_support_gate":
                bool(
                    scientific.get(
                        "claim_support_gate",
                        False
                    )
                ),

            "scientific_claim_authority":
                False
        },

        "primary_stochastic_null": {
            "model":
                primary_null.get(
                    "null_model"
                ),

            "p_value":
                primary_null.get(
                    "p_value_mc_add_one"
                ),

            "rejected":
                bool(
                    primary_null.get(
                        "reject_at_0_05",
                        False
                    )
                ),

            "scientific_role":
                "primary_stochastic_null_gate"
        },

        "promotion": {
            "allowed": False,
            "reason":
                "Scientific claim remains under investigation."
        },

        "epistemic_guard": {
            "causality_claimed": False,
            "universality_claimed": False,
            "hcm_causation_claimed": False,
            "market_advantage_claimed": False,
            "consciousness_claimed": False
        }
    }

    return artifact


def main():
    os.makedirs(
        "public",
        exist_ok=True
    )

    artifact = build_artifact()

    with open(
        OUTPUT,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            artifact,
            f,
            indent=2
        )

    # Canonical report may remain publicly visible
    # as the primary evidence record.
    if os.path.exists(CANONICAL):
        shutil.copy(
            CANONICAL,
            "public/latest.json"
        )

    print(
        json.dumps(
            artifact,
            indent=2
        )
    )


if __name__ == "__main__":
    main()
