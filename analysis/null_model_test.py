import numpy as np
import json
from .numerical_spectral_verification import estimate_alpha

def generate_null(series_length=512):
    return np.random.normal(0, 1, series_length)

def extract_alpha(w):
    """
    Robust extractor:
    يسمح بـ dict أو float أو أي شكل تاني
    """
    if isinstance(w, dict):
        return w.get("alpha", None)
    elif isinstance(w, (int, float)):
        return float(w)
    else:
        return None

def compare_alpha(real_alpha, null_alpha):
    return abs(real_alpha - null_alpha)

def main():

    with open("artifacts/windowed_spectral.json") as f:
        data = json.load(f)

    results = {}

    for name, windows in data.items():

        diffs = []

        alphas = windows.get("alphas", [])

        for w in alphas:

            real_alpha = extract_alpha(w)

            # Skip invalid entries
            if real_alpha is None:
                continue

            null_series = generate_null()
            null_alpha = estimate_alpha(null_series)

            diffs.append(compare_alpha(real_alpha, null_alpha))

        # حماية من empty list
        if len(diffs) == 0:
            mean_sep = 0.0
        else:
            mean_sep = float(np.mean(diffs))

        results[name] = {
            "mean_separation": mean_sep,
            "samples_used": len(diffs)
        }

    with open("artifacts/null_comparison.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Null model comparison completed.")


if __name__ == "__main__":
    main()
