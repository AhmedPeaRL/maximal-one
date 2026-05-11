import math
import numpy as np


def deep_freeze(obj, digits=8):

    if isinstance(obj, dict):

        return {
            str(k): deep_freeze(v, digits)
            for k, v in sorted(obj.items())
        }

    if isinstance(obj, list):

        return [
            deep_freeze(x, digits)
            for x in obj
        ]

    if isinstance(obj, tuple):

        return tuple(
            deep_freeze(x, digits)
            for x in obj
        )

    if isinstance(obj, np.ndarray):

        return [
            deep_freeze(x, digits)
            for x in obj.tolist()
        ]

    if isinstance(obj, (np.floating, float)):

        x = float(obj)

        if not math.isfinite(x):
            return None

        return round(x, digits)

    if isinstance(obj, (np.integer, int)):

        return int(obj)

    if isinstance(obj, (np.bool_, bool)):

        return bool(obj)

    return obj
