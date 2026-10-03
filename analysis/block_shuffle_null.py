from __future__ import annotations

import numpy as np


DEFAULT_BLOCK_SIZE = 50


def block_shuffle(
    series,
    rng,
    block_size=DEFAULT_BLOCK_SIZE,
):
    """
    Return a seeded block-shuffled surrogate.

    This function is diagnostic-only.

    The caller owns the RNG so that the surrogate sequence is
    reproducible for a declared seed.
    """
    series = np.asarray(series)

    if series.ndim != 1:
        raise ValueError(
            "series must be one-dimensional"
        )

    if len(series) == 0:
        raise ValueError(
            "series must not be empty"
        )

    if (
        not isinstance(
            block_size,
            (int, np.integer),
        )
        or isinstance(block_size, bool)
    ):
        raise TypeError(
            "block_size must be an integer"
        )

    block_size = int(block_size)

    if block_size < 1:
        raise ValueError(
            "block_size must be >= 1"
        )

    if (
        rng is None
        or not hasattr(rng, "permutation")
    ):
        raise TypeError(
            "rng must be a numpy.random.Generator"
        )

    blocks = [
        series[i:i + block_size]
        for i in range(
            0,
            len(series),
            block_size,
        )
    ]

    order = rng.permutation(
        len(blocks)
    )

    return np.concatenate(
        [
            blocks[int(i)]
            for i in order
        ]
    )
