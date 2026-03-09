import json
import os
import numpy as np
import pandas as pd

OUTPUT = "artifacts/chaos_discovery.json"


def hurst_exponent(ts):
    lags = range(2, 50)
    tau = [np.std(np.subtract(ts[lag:], ts[:-lag])) for lag in lags]
    poly = np.polyfit(np.log(lags), np.log(tau), 1)
    return poly[0] * 2.0


def detect_chaos(series):

    series = np.array(series)

    if len(series) < 200:
        return None

    h = hurst_exponent(series)

    chaotic = h > 0.55

    return {
        "hurst": float(h),
        "chaotic_signature": chaotic
    }


def scan():

    results = []

    if not os.path.exists("real-data"):
        return results

    for f in os.listdir("real-data"):

        if not f.endswith(".csv"):
            continue

        path = os.path.join("real-data", f)

        try:
            df = pd.read_csv(path)

            col = df.columns[0]

            series = df[col].values

            r = detect_chaos(series)

            if r:
                r["dataset"] = f
                results.append(r)

        except Exception:
            continue

    return results


def main():

    results = scan()

    os.makedirs("artifacts", exist_ok=True)

    with open(OUTPUT, "w") as f:
        json.dump(results, f, indent=2)

    print(json.dumps({"discoveries": len(results)}))


if __name__ == "__main__":
    main()
