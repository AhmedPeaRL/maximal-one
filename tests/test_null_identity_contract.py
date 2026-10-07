import sys
from pathlib import Path

sys.path.append(
    str(
        Path(__file__).resolve().parents[1]
    )
)

from analysis.null_protocol import (
    load_null_protocol,
)


def test_null_model_and_protocol_are_distinct():
    protocol = load_null_protocol()

    assert (
        protocol["model_id"]
        ==
        "stationary_gaussian_ar_p_aic"
    )

    assert (
        protocol["protocol_id"]
        ==
        "stationary_gaussian_ar_p_aic_v2_exploratory"
    )

    assert (
        protocol["model_id"]
        !=
        protocol["protocol_id"]
    )


def test_null_identity_contract():
    protocol = load_null_protocol()

    assert isinstance(
        protocol["model_id"],
        str,
    )

    assert isinstance(
        protocol["protocol_id"],
        str,
    )

    assert protocol[
        "model_id"
    ].strip()

    assert protocol[
        "protocol_id"
    ].strip()


if __name__ == "__main__":
    test_null_model_and_protocol_are_distinct()
    test_null_identity_contract()
    print(
        "✅ Null identity contract passed."
    )
