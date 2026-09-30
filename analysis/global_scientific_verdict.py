from __future__ import annotations

import json
from pathlib import Path


ART = Path("artifacts")


def load(name):
    path = ART / name

    if not path.exists():
        return None

    try:
        return json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )
    except Exception:
        return None


def main():
    canonical = load(
        "canonical_report.json"
    )

    calibration = load(
        "null_calibration_gate.json"
    )

    replication = load(
        "independent_domain_replication_gate.json"
    )

    replay = load(
        "external_replay_verification.json"
    )

    if canonical is None:
        status = "INVALID_PIPELINE"
        reason = [
            "canonical_report_missing"
        ]
    else:
        status = "UNDER_INVESTIGATION"

        reason = []

        primary_null = (
            canonical.get(
                "appropriate_stochastic_null",
                {}
            )
        )

        if not primary_null.get(
            "reject_at_0_05",
            False
        ):
            reason.append(
                "primary_stochastic_null_not_rejected"
            )

        if (
            calibration is None
            or
            calibration.get("status")
            !=
            "CALIBRATION_NOT_REJECTED"
        ):
            reason.append(
                "null_calibration_not_established"
            )

        if (
            replication is None
            or
            replication.get("status")
            !=
            "REPLICATION_ESTABLISHED"
        ):
            reason.append(
                "independent_domain_replication_not_established"
            )

        if (
            replay is None
            or
            replay.get(
                "computational_reproducibility_verified"
            )
            is not True
        ):
            reason.append(
                "clean_checkout_reproducibility_not_verified"
            )

    result = {
        "status": status,

        "scientific_claim_authority": False,
        "promotion_authority": False,

        "passed": False,

        "predictive_pass": False,

        "final_score": 0.0,
        "score_ratio": 0.0,

        "confidence": None,
        "confidence_level": None,

        "layer": "under_investigation",

        "decision": "DO_NOT_PROMOTE",

        "reasons": reason,

        "methodology": {
            "scoring_disabled": True,
            "deterministic_noise_disabled": True,
            "heuristic_bonuses_disabled": True,
            "manual_confidence_disabled": True,
            "scientific_verdict_source":
                "canonical_machine_gates_only"
        },

        "interpretation": (
            "This artifact is a compatibility state "
            "surface only. It is not a statistical "
            "inference engine and carries no scientific "
            "claim authority."
        )
    }

    ART.mkdir(
        parents=True,
        exist_ok=True
    )

    (
        ART / "global_verdict.json"
    ).write_text(
        json.dumps(
            result,
            indent=2,
            sort_keys=True
        ) + "\n",
        encoding="utf-8"
    )

    print(
        json.dumps(
            result,
            indent=2
        )
    )


if __name__ == "__main__":
    main()
