import numpy as np
import pandas as pd
import json
import os
import sys

OUTPUT = "artifacts/lyapunov_estimate.json"


def largest_lyapunov(series, delay=2, emb_dim=3):

    series = np.array(series)
    n = len(series)

    if n < 200:
        return None

    embedded = []

    for i in range(n - delay * emb_dim):
        vec = [series[i + j * delay] for j in range(emb_dim)]
        embedded.append(vec)

    embedded = np.array(embedded)

    distances = []
    divergences = []

    for i in range(len(embedded) - 10):

        ref = embedded[i]

        d = np.linalg.norm(embedded - ref, axis=1)
        d[i] = np.inf

        j = np.argmin(d)

        if abs(j - i) < 10:
            continue

        for k in range(1,5):

            if i+k >= len(embedded) or j+k >= len(embedded):
                break

            dist = np.linalg.norm(embedded[i+k] - embedded[j+k])

            if dist > 0:
                distances.append(k)
                divergences.append(np.log(dist))

    if len(distances) < 10:
        return None

    coef = np.polyfit(distances, divergences, 1)

    return float(coef[0])


def main():

    if len(sys.argv) < 2:
        print("dataset required")
        sys.exit(1)

    path = sys.argv[1]

    df = pd.read_csv(path)

    series = df[df.columns[0]].values

    lle = largest_lyapunov(series)

    os.makedirs("artifacts", exist_ok=True)

    result = {
        "dataset": path,
        "largest_lyapunov": lle,
        "chaotic": bool(lle and lle > 0)
    }

    with open(OUTPUT,"w") as f:
        json.dump(result,f,indent=2)

    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
