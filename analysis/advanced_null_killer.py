import numpy as np
from statsmodels.tsa.arima_process import ArmaProcess
from analysis.numerical_spectral_verification import estimate_alpha

def generate_arima_like(series, n=1000):
    ar = np.array([1, -0.9])  # strong autocorrelation
    ma = np.array([1])
    arma = ArmaProcess(ar, ma)
    return arma.generate_sample(nsample=len(series))

def generate_fbm_like(series):
    np.random.seed(42)
    noise = np.random.normal(0,1,len(series))
    return np.cumsum(noise)

def advanced_null_test(series, n=50):
    real_alpha = estimate_alpha(series)

    models = {
      "ARIMA_like": [],
      "FBM_like": []
    }

    for _ in range(n):
      models["ARIMA_like"].append(estimate_alpha(generate_arima_like(series)))
      models["FBM_like"].append(estimate_alpha(generate_fbm_like(series)))

    results = {}

    for k,v in models.items():
      v = np.array(v)
      z = (real_alpha - np.mean(v)) / (np.std(v)+1e-12)

      results[k] = {
          "mean": float(np.mean(v)),
          "std": float(np.std(v)),
          "z_score": float(z),
          "irreducible": abs(z) > 2.5
      }

    return real_alpha, results

if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv("real-data/sunspots_global.csv")

    if "value" not in df.columns:
        raise ValueError("Dataset must contain 'value' column")

    series = df["value"].values

    real_alpha, res = advanced_null_test(series)

    print("=== ADVANCED NULL TEST ===")
    print("Real alpha:", real_alpha)

    for model, stats in res.items():
        print(f"\n[{model}]")
        print("mean:", stats["mean"])
        print("std:", stats["std"])
        print("z_score:", stats["z_score"])
        print("irreducible:", stats["irreducible"])

    print("=== END ===")
