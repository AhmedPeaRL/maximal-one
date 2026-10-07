from __future__ import annotations

import json
from pathlib import Path


CLAIM_PATH = Path(
    "core-scientific/strict_claim.json"
)


def load_null_protocol():

    if not CLAIM_PATH.exists():
        raise SystemExit(
            f"Missing strict claim specification: {CLAIM_PATH}"
        )

    claim = json.loads(
        CLAIM_PATH.read_text(
            encoding="utf-8"
        )
    )

    protocol = claim.get(
        "stochastic_null_protocol",
        {}
    )

    protocol_id = protocol.get(
        "protocol_id"
    )

    null_family = protocol.get(
        "null_family"
    )

    model_id = protocol.get(
        "model_id",
        "stationary_gaussian_ar_p_aic",
    )

    alternative = protocol.get(
        "alternative",
        {}
    )

    endpoint = alternative.get(
        "endpoint",
        protocol.get("endpoint")
    )

    direction = alternative.get(
        "direction"
    )

    tail = alternative.get(
        "tail"
    )

    if not isinstance(
        protocol_id,
        str
    ) or not protocol_id.strip():

        raise SystemExit(
            "strict_claim.stochastic_null_protocol.protocol_id "
            "is missing or invalid"
        )

    if not isinstance(
        model_id,
        str
    ) or not model_id.strip():

        raise SystemExit(
            "strict_claim.stochastic_null_protocol.model_id "
            "is missing or invalid"
        )

    if not isinstance(
        null_family,
        str
    ) or not null_family.strip():

        raise SystemExit(
            "strict_claim.stochastic_null_protocol.null_family "
            "is missing or invalid"
        )

    if not isinstance(
        endpoint,
        str
    ) or not endpoint.strip():

        raise SystemExit(
            "strict_claim.stochastic_null_protocol alternative "
            "endpoint is missing or invalid"
        )

    if not isinstance(
        direction,
        str
    ) or not direction.strip():

        raise SystemExit(
            "strict_claim.stochastic_null_protocol alternative "
            "direction is missing or invalid"
        )

    if not isinstance(
        tail,
        str
    ) or not tail.strip():

        raise SystemExit(
            "strict_claim.stochastic_null_protocol alternative "
            "tail is missing or invalid"
        )

    return {
        "protocol_id": protocol_id,
        "model_id": model_id,
        "null_family": null_family,
        "endpoint": endpoint,
        "direction": direction,
        "tail": tail,
    }


def protocol_id():

    return load_null_protocol()[
        "protocol_id"
    ]


def model_id():

    return load_null_protocol()[
        "model_id"
    ]


def null_family():

    return load_null_protocol()[
        "null_family"
    ]


def test_endpoint():

    return load_null_protocol()[
        "endpoint"
    ]


def direction():

    return load_null_protocol()[
        "direction"
    ]


def tail():

    return load_null_protocol()[
        "tail"
    ]


if __name__ == "__main__":

    print(
        json.dumps(
            load_null_protocol(),
            indent=2,
            sort_keys=True,
        )
    )
