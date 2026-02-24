import numpy as np
from env.fingerprint import collect_environment, compute_hash
from baseline.clustered_baseline import (
    create_baseline,
    save_baseline,
    load_baseline,
)
from spc.spc_v2 import spc_check


def generate_sample(n=1_000_000):
    return np.random.normal(0, 1, n)


def main():
    env_data = collect_environment()
    env_hash = compute_hash(env_data)

    sample = generate_sample()

    baseline = load_baseline(env_hash)

    if baseline is None:
        print("Creating baseline for environment:", env_hash)
        baseline = create_baseline(sample)
        save_baseline(env_hash, baseline)
        return

    result = spc_check(sample, baseline)

    print("Environment:", env_hash)
    print(result)


if __name__ == "__main__":
    main()
