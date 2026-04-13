import json
import argparse
import random
import math
import os
import traceback
import time

def nonlinear_measure(x):
    return x**2 + 3*x + 7

def compute_stability(seed):
    random.seed(seed)
    values = [random.random() for _ in range(1000)]
    transformed = [nonlinear_measure(v) for v in values]
    
    mean = sum(transformed) / len(transformed)
    variance = sum((v - mean) ** 2 for v in transformed) / len(transformed)
    std = math.sqrt(variance)
    
    return mean, std

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--canonical", action="store_true")
    args = parser.parse_args()

    os.makedirs("artifacts", exist_ok=True)

    try:
        mean, std = compute_stability(args.seed)

        alpha = mean / (std + 1e-12)

        report = {
            "spectral_profile": {
            "estimated_alpha": float(alpha),
            "bootstrap_std": float(std)
            },
            "metadata": {
                "seed": args.seed
            }
        }

        with open("artifacts/canonical_report.json", "w") as f:
            json.dump(report, f, sort_keys=True, separators=(',',':'))
            
        print("✅ Report generated")

     except Exception as e:
         fallback = {
             "status": "partial",
             "error": str(e),
             "trace": traceback.format_exc(),
             "timestamp": time.time()
          }

          with open("artifacts/canonical_report.json", "w") as f:
              json.dump(fallback, f)

          print("⚠️ Fallback report generated")

    if name == "main":
        main()
