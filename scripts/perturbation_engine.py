#!/usr/bin/env python3

import random
import sys

NOISE_LEVEL = 0.05  # 5%

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: perturbation_engine.py <score>")
        sys.exit(1)

    score = float(sys.argv[1])
    noise = score * NOISE_LEVEL * random.uniform(-1, 1)
    perturbed = score + noise
    print(perturbed)
