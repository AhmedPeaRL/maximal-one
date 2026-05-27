from decimal import Decimal, ROUND_HALF_UP
import numpy as np

FIXED_DIGITS = 6

def freeze_float(x, digits=FIXED_DIGITS):
    if x is None:
        return None

    if isinstance(x, (np.floating, float)):
        if not np.isfinite(x):
            return None

        q = Decimal(str(float(x))).quantize(
            Decimal("1." + ("0" * digits)),
            rounding=ROUND_HALF_UP
        )

        return float(q)

    return x

def recursively_freeze(obj):
    if isinstance(obj, dict):
        return {
            str(k): recursively_freeze(v)
            for k, v in sorted(obj.items())
        }

    if isinstance(obj, list):
        return [
            recursively_freeze(v)
            for v in obj
        ]

    if isinstance(obj, tuple):
        return tuple(
            recursively_freeze(v)
            for v in obj
        )

    if isinstance(obj, np.ndarray):
        return [
            recursively_freeze(v)
            for v in obj.tolist()
        ]

    return freeze_float(obj)
