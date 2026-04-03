import numpy as np
import json
from pathlib import Path

from analysis.anti_triviality_structure_test import (
    generate_structured_series,
    destroy_local_predictability,
    evaluate
)
from analysis.hcm_meta_predictor import HCMMetaPredictor

ART = Path("artifacts")
ART.mkdir(exist_ok=True)


def run_once(seed):
    np.random.seed(seed)

    base = generate_structured_series()
    corrupted = destroy_local_predictability(base)

    model = HCMMetaPredictor()

    mse_clean = evaluate(base, model)
    mse_corrupt = evaluate(corrupted, model)

    return float(mse_clean < mse_corrupt)


def main():

    seeds = list(range(30))  # 🔥 عدد التجارب
    results = []

    for s in seeds:
        r = run_once(s)
        results.append(r)

    success_rate = sum(results) / len(results)

    result = {
        "samples": len(results),
        "success_rate": success_rate,
        "passes_threshold": success_rate > 0.7
    }

    print("=== HARD TEST (MULTI RUN) ===")
    print(json.dumps(result, indent=2))

    (ART / "anti_triviality_hard.json").write_text(
        json.dumps(result, indent=2)
    )


if __name__ == "__main__":
    main()
