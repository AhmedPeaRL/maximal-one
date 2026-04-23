import numpy as np

def block_shuffle(series, block_size=50):
    """
    Stronger null model:
    breaks long-range correlations
    but keeps local structure
    """

    n = len(series)

    blocks = [
        series[i:i+block_size]
        for i in range(0, n, block_size)
    ]

    np.random.shuffle(blocks)

    return np.concatenate(blocks)
