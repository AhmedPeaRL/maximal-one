import json
import numpy as np
from src.pressure_layers import (
    randomized_seed_sweep,
    sample_size_ladder,
    synthetic_amplitude_sweep
)

def main():
    print("Running randomized seed sweep...")
    seed_results = randomized_seed_sweep()
    print("Mean max_z:", np.mean(seed_results))
    print("Std max_z:", np.std(seed_results))

    print("Running sample size ladder...")
    sizes = [10_000, 20_000, 50_000, 100_000, 200_000, 500_000, 1_000_000]
    ladder_results = sample_size_ladder(sizes)

    print("Running synthetic amplitude sweep...")
    amplitude_results = synthetic_amplitude_sweep()

    all_results = {
        "seed_sweep": seed_results.tolist(),
        "ladder": ladder_results,
        "synthetic": amplitude_results
    }

    with open("pressure_results.json", "w") as f:
        json.dump(all_results, f, indent=2)

if __name__ == "__main__":
    main()
