import json
from pathlib import Path


ART = Path("artifacts")


def load(name):
    path = ART / name

    if not path.exists():
        return None

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def main():
    canonical = load(
        "canonical_report.json"
    )

    if canonical is None:
        raise RuntimeError(
            "canonical_report.json is missing"
        )

    scientific = canonical.get(
        "scientific_interpretation",
        {}
    )

    primary_null = canonical.get(
        "appropriate_stochastic_null",
        {}
    )

    public = {
        "status": "under_investigation",

        "scientific_claim_authority": False,

        "claim": (
            "Constrained Spectral Persistence Hypothesis "
            "remains under investigation."
        ),

        "primary_stochastic_null": {
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
                )
        },

        "claim_support_gate":
            bool(
                scientific.get(
                    "claim_support_gate",
                    False
                )
            ),

        "interpretation":
            scientific.get(
                "claim_status",
                "under_investigation"
            ),

        "promotion_allowed": False
    }

    (
        ART / "public_signal.json"
    ).write_text(
        json.dumps(
            public,
            indent=2,
            sort_keys=True
        ) + "\n",
        encoding="utf-8"
    )

    print(
        json.dumps(
            public,
            indent=2
        )
    )


if __name__ == "__main__":
    main()
