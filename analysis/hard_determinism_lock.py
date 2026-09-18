from __future__ import annotations
import os
import random
import numpy as np

SEED = 42

# ------------------------------------------------------------
# Deterministic process environment
# ------------------------------------------------------------

os.environ["PYTHONHASHSEED"] = str(SEED)

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

# Prevent common BLAS implementations from silently
# increasing parallelism.
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
os.environ.setdefault("BLIS_NUM_THREADS", "1")

# ------------------------------------------------------------
# Randomness
# ------------------------------------------------------------

random.seed(SEED)
np.random.seed(SEED)

# ------------------------------------------------------------
# Explicit scope
# ------------------------------------------------------------

DETERMINISM_SCOPE = {
    "seed": SEED,
    "python_hash_seed": str(SEED),
    "cpu_thread_locks": True,
    "numpy_seeded": True,
    "python_random_seeded": True,
    "gpu_determinism": False,
    "multi_node_determinism": False,
    "bitwise_cross_hardware_guarantee": False,
}

def determinism_manifest():
    return dict(DETERMINISM_SCOPE)

print("HARD DETERMINISM LOCK ACTIVE")
print("Determinism scope:", DETERMINISM_SCOPE)
