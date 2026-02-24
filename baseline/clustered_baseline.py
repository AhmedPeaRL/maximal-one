import json
import os
import numpy as np


BASELINE_DIR = "baseline"


def load_environment_hash():
    with open("env/environment_hash.txt", "r") as f:
        return f.read().strip()


def baseline_path(env_hash):
    return os.path.join(BASELINE_DIR, f"{env_hash}.json")


def create_baseline(samples):
    """
    samples: list of independent sample arrays
    """

    means = [np.mean(s) for s in samples]
    stds  = [np.std(s)  for s in samples]

    return {
        "mean_mean": float(np.mean(means)),
        "mean_std":  float(np.std(means)),
        "std_mean":  float(np.mean(stds)),
        "std_std":   float(np.std(stds)),
        "n_runs": len(samples)
    }


def save_baseline(env_hash, baseline):
    os.makedirs(BASELINE_DIR, exist_ok=True)
    with open(baseline_path(env_hash), "w") as f:
        json.dump(baseline, f, indent=2)


def load_baseline(env_hash):
    path = baseline_path(env_hash)
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)
