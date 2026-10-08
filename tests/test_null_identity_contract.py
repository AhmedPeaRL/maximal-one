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


def test_null_result_identity():
    import numpy as np

    from analysis.appropriate_stochastic_null import (
        parametric_short_memory_null,
    )

    protocol = load_null_protocol()

    rng = np.random.default_rng(
        42
    )

    x = (
        np.sin(
            np.arange(600)
            / 20.0
        )
        +
        rng.normal(
            0.0,
            0.1,
            600,
        )
    )

    result = (
        parametric_short_memory_null(
            x,
            0.5,
            rng,
            trials=200,
        )
    )

    assert result[
        "null_model"
    ] == protocol[
        "model_id"
    ]

    assert result[
        "null_protocol_id"
    ] == protocol[
        "protocol_id"
    ]

    assert result[
        "null_model"
    ] != result[
        "null_protocol_id"
    ]


if __name__ == "__main__":
    test_null_model_and_protocol_are_distinct()
    test_null_identity_contract()
    test_null_result_identity()

    print(
        "✅ Null identity contract passed:"
        " model_id, protocol_id, and generated-result identity."
    )
