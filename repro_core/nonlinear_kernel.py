#!/usr/bin/env python3
import numpy as np
import json
import hashlib
import argparse

def nonlinear_map(x, gamma, beta):
    # cubic saturation term introduces true nonlinearity
    return gamma * x - beta * (x ** 3)

def simulate(gamma=0.9, beta=0.1, noise_std=0.01, n=50000, seed=42):
    rng = np.random.default_rng(seed)
    x = np.zeros(n)
    for t in range(1, n):
        noise = rng.normal(0, noise_std)
        x[t] = nonlinear_map(x[t-1], gamma, beta) + noise
    return x

def estimate_lyapunov(x, gamma, beta):
    # derivative of nonlinear map
    derivatives = gamma - 3 * beta * (x ** 2)
    return np.mean(np.log(np.abs(derivatives) + 1e-12))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gamma", type=float, default=0.9)
    parser.add_argument("--beta", type=float, default=0.1)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    x = simulate(gamma=args.gamma, beta=args.beta, seed=args.seed)

    lyap = estimate_lyapunov(x, args.gamma, args.beta)

    result = {
        "gamma": args.gamma,
        "beta": args.beta,
        "lyapunov": float(lyap),
        "mean": float(np.mean(x)),
        "variance": float(np.var(x))
    }

    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()
