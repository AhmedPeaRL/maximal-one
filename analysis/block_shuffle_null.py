import numpy as np

def block_shuffle(
    series,
    rng,
    block_size=None,
):
    n = len(series)

    blocks = [
        series[i:i+block_size]
        for i in range(0, n, block_size)
    ]

    np.random.shuffle(blocks)

    return np.concatenate(blocks)
