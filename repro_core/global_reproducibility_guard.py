# repro_core/global_reproducibility_guard.py

import os
import numpy as np
import random
import hashlib

SEED = 42

def enforce_global_determinism():
    os.environ["PYTHONHASHSEED"] = str(SEED)
    random.seed(SEED)
    np.random.seed(SEED)

    try:
        import torch
        torch.manual_seed(SEED)
        torch.use_deterministic_algorithms(True)
    except Exception:
        pass

def canonical_float(x, precision=15):
    return float(f"{x:.{precision}f}")

def deterministic_hash(obj):
    payload = str(obj).encode()
    return hashlib.sha256(payload).hexdigest()

if __name__ == "__main__":
    enforce_global_determinism()
    print("Deterministic guard active.")
